import ast,copy,json,math,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"candidate"))
from bancada.evidence_checks import finite_number,nested_deltas,validate_fit
from bancada.regua import Livro,ESTATUTOS,guarda,p_de_z,z_de_p
NAMES=("H0","ombh2","omch2","beta","c")
ALPHA_FINE_CODATA_2018=7.2973525693e-3
BETA=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
tree=ast.parse((ROOT/"candidate/bancada/evidencia.py").read_text(encoding="utf-8"))
selected=ast.Module(body=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="Evidencia"],type_ignores=[])
ns=dict(math=math,NOMES_THETA=NAMES,_conj=lambda c:list(c or ["synthetic"]),
        opcoes_de=lambda o:dict(o or {}),rotulo_opcoes=lambda o:"SYNTHETIC_TEST_ONLY",
        validate_fit=validate_fit,finite_number=finite_number,nested_deltas=nested_deltas,
        ESTATUTOS=ESTATUTOS,guarda=guarda,p_de_z=p_de_z,z_de_p=z_de_p)
exec(compile(selected,"candidate/bancada/evidencia.py","exec"),ns)
Evidencia=ns["Evidencia"]
def fit(chi,success=True,sigma=.1):
    return dict(chi2=chi,sucesso=success,theta={k:0.0 for k in NAMES},sigma_JtJ={"beta":sigma},gl=5)
class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.book=Livro(Path(self.tmp.name)/"synthetic.sqlite3")
        self.ev=Evidencia(SimpleNamespace(beta_tgl=BETA),self.book)
    def tearDown(self):self.tmp.cleanup()
    def comparison(self,fits):
        with patch.object(self.ev,"_ajuste",side_effect=fits):
            return self.ev.comparar(conjuntos=["synthetic"])
    def assert_failure(self,fits):
        with patch.object(self.book,"corrige",wraps=self.book.corrige) as correction:
            with self.assertRaises(ValueError):self.comparison(fits)
            correction.assert_not_called()
        last=self.book.resumo()["ultimas"][0]
        self.assertIsNone(last["p_local"]);self.assertIsNone(last["estatistica"])
        self.assertEqual(last["estatuto"],"DIAGNOSTICO_INVALIDO_SEM_SIGNIFICANCIA")
        self.assertEqual(self.book.n_familias_de_teste(),0)
    def test_failed_fit_each_model(self):
        for index in range(3):
            with self.subTest(index=index):
                data=[fit(12.),fit(9.),fit(5.)];data[index]["sucesso"]=False
                self.assert_failure(data)
    def test_success_must_be_boolean_true(self):
        for value in (None,1,"true","false"):
            with self.subTest(value=value):
                self.assert_failure([fit(12.,value),fit(9.),fit(5.)])
    def test_bad_chi2_is_not_a_signal(self):
        for value in (float("nan"),float("inf"),-1.,True,"4"):
            with self.subTest(value=str(value)):
                self.assert_failure([fit(value),fit(9.),fit(5.)])
    def test_invalid_theta_stops_before_warmstart(self):
        data=fit(12.);del data["theta"]["H0"]
        self.assert_failure([data])
    def test_nonfinite_theta(self):
        data=fit(12.);data["theta"]["c"]=float("nan")
        self.assert_failure([data])
    def test_free_minimum_must_not_be_worse_than_either_fixed(self):
        self.assert_failure([fit(12.),fit(4.),fit(5.)])
        self.assert_failure([fit(4.),fit(12.),fit(5.)])
    def test_tiny_negative_is_not_silently_clipped(self):
        self.assert_failure([fit(12.),fit(1.),fit(math.nextafter(1.,math.inf))])
    def test_valid_comparison_keeps_signed_fixed_difference(self):
        out=self.comparison([fit(12.),fit(9.),fit(5.)])
        self.assertEqual(out["delta_chi2"]["tgl_menos_lcdm"],-3.)
        self.assertAlmostEqual(out["significancia"]["p_local"],math.erfc(math.sqrt(2.)),places=14)
        self.assertEqual(out["hipoteses_significancia"]["nula"],"TGL_BETA_FIXO")
        self.assertEqual(out["hipoteses_significancia"]["alternativa"],"BETA_LIVRE")
        self.assertFalse(out["hipoteses_significancia"]["regularidade_verificada"])
        self.assertIsNone(out["significancia"]["p_global"])
        json.dumps(out,allow_nan=False)
    def test_equal_nested_minima_is_zero_local(self):
        out=self.comparison([fit(5.),fit(5.),fit(5.)])
        self.assertEqual(out["significancia"]["p_local"],1.)
        self.assertEqual(out["significancia"]["z_local"],0.)
        self.assertIsNone(out["significancia"]["z_global"])
    def test_failed_adjustment_has_no_wald_output(self):
        with patch.object(self.ev,"_ajuste",return_value=fit(5.,False)):
            with self.assertRaises(ValueError):self.ev.ajustar(["synthetic"])
        self.assertIsNone(self.book.resumo()["ultimas"][0]["p_local"])
    def test_bad_wald_sigma_is_rejected(self):
        for value in (0.,-1.,float("nan"),float("inf"),True):
            with self.subTest(sigma=str(value)),patch.object(self.ev,"_ajuste",return_value=fit(5.,sigma=value)):
                with self.assertRaises(ValueError):self.ev.ajustar(["synthetic"])
    def test_missing_covariance_is_not_zero_sigma(self):
        data=fit(5.);data["sigma_JtJ"]={}
        with patch.object(self.ev,"_ajuste",return_value=data):out=self.ev.ajustar(["synthetic"])
        self.assertNotIn("significancia",out)
        self.assertNotIn("beta_tgl_em_sigma_JtJ",out)
    def test_probability_validation(self):
        for p in (float("nan"),float("inf"),-.1,1.1,True):
            with self.subTest(p=str(p)),self.assertRaises(ValueError):self.book.corrige(p)
    def test_sidak_illustration_never_populates_global(self):
        for n in (1,7,1000):
            with self.subTest(n=n),patch.object(self.book,"n_familias_de_teste",return_value=n):
                r=self.book.corrige(.05)
                self.assertAlmostEqual(r["sidak_ilustrativo"]["p"],1-.95**n,places=12)
                self.assertFalse(r["global_calibrated"]);self.assertIsNone(r["p_global"]);self.assertIsNone(r["z_global"])
    def test_probability_zero_has_no_infinite_z(self):
        r=self.book.corrige(0.)
        self.assertIsNone(r["z_local"]);self.assertIsNone(r["sidak_ilustrativo"]["z"])
        json.dumps(r,allow_nan=False)
    def test_uncertainty_fields_are_finite_positive(self):
        for field in NAMES:
            for value in (float("nan"),float("inf"),0.,-1.):
                with self.subTest(field=field,value=str(value)):
                    data=fit(12.);data["sigma_JtJ"][field]=value
                    self.assert_failure([data])
    def test_subnormal_probability_has_no_infinite_z(self):
        r=self.book.corrige(math.nextafter(0.,1.))
        self.assertIsNone(r["z_local"])
        self.assertEqual(r["local_status"],"NUMERICAL_LIMIT_NO_FINITE_Z")
        json.dumps(r,allow_nan=False)
    def test_connections_close_and_roll_back(self):
        with self.assertRaises(RuntimeError):
            with self.book._con() as c:
                c.execute("INSERT INTO consultas (estatuto) VALUES ('SYNTHETIC_ROLLBACK')")
                raise RuntimeError("synthetic")
        self.assertEqual(self.book.resumo()["total"],0)
        with self.assertRaises(Exception):c.execute("SELECT 1")
    def test_small_probability_stays_nonzero(self):
        with patch.object(self.book,"n_familias_de_teste",return_value=7):r=self.book.corrige(1e-100)
        self.assertGreater(r["sidak_ilustrativo"]["p"],0.)
        self.assertAlmostEqual(r["sidak_ilustrativo"]["p"]/1e-100,7.)
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    summary={"tests":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),
             "scope":"AST class harness with mocked fit results and temporary SQLite; no motor, fits, GPU, HTTP, production imports or observations"}
    print(json.dumps(summary));sys.exit(not result.wasSuccessful())
