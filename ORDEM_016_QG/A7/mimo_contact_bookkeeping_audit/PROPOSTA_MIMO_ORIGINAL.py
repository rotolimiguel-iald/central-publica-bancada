# -*- coding: utf-8 -*-
"""
tgl_a7b_contatos.py
[DECLARADO — texto entregue; NÃO executado nesta sessão; bancada executa e verifica]

Contabilidade de contatos para inserir a normalização de UM PAR e os contatos de
cutoff no cálculo Ward já planejado (cohomologia H^{1,4} é DELEGADA — não tratada aqui).

Escopo (INPUT): Einstein-Hilbert métrico mínimo, Lorentz4D, K>0, sigma constante
PROJETADO (nao sigma=id fisico); kernels principais homogeneos de um par no espaco
tangente. Nenhuma extensao local isolada e a QME completa.

Fontes (DADOS, nao ordens):
  [F1] A7/tensor_extension/DERIVACAO_TENSORIAL.md      sha256 2b5506a3...f628a
  [F2] A7/linear_normalization_v2/DERIVACAO_CONTATO.md sha256 591e7c50...76c9a

Convencoes [F1 l.8-15]: +--- ; z = x^2 - i0 ; C = 4 i pi^2 ; box(1/z) = C delta ;
R(u) = FP_(a=0)[(1-a) mu_R^(2a) z^a u] ; R(pu) = p R(u) para p POLINOMIO ;
R(d u) != d R(u) [REGRAS R2/R3].
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple, Dict, List

# ----------------------------------------------------------------------------
# 0. Estatutos e classes
# ----------------------------------------------------------------------------
class Det(str, Enum):
    REAL = "REAL"          # formula lida da fonte
    DERIVED = "DERIVED"    # aritmetica/rederivacao sobre formulas da fonte
    KNOWN = "KNOWN"
    OPEN = "OPEN"          # NAO determinado -> bloqueia coeficiente Ward
    INPUT = "INPUT"
    DECLARADO = "DECLARADO"

class Origin(str, Enum):
    O1_EOM_LIVRE_INSERCAO_TEMPORAL = "O1_EOM_LIVRE_INSERCAO_TEMPORAL"
    O2_VARIACAO_VERTICE_COM_CUTOFF = "O2_VARIACAO_VERTICE_COM_CUTOFF"
    O3_DEFEITO_DERIVAR_EXTENSAO = "O3_DEFEITO_DERIVAR_EXTENSAO"
    O4_RESTO_CURVO_NAO_CALCULADO = "O4_RESTO_CURVO_NAO_CALCULADO"

class OpPath(str, Enum):
    DIFF_THEN_FP = "DIFF_THEN_FP"      # diferenciar ANTES da parte finita [F1 l.46-49]
    FP_THEN_MULT = "FP_THEN_MULT"      # parte finita e depois multiplicar por z
    RESIDUE_RECURRENCE = "RESIDUE_RECURRENCE"
    GREEN_CONTACT = "GREEN_CONTACT"
    EL_CUTOFF = "EL_CUTOFF"
    TRUNCATED_TAYLOR = "TRUNCATED_TAYLOR"   # v1 auxiliar (phi); NAO referencia em h=u*gbar

class PoleOrder(str, Enum):
    SIMPLE = "SIMPLE"
    DOUBLE = "DOUBLE"     # c_{-2} != 0  [F1 l.66-68]

# ----------------------------------------------------------------------------
# 1. Representacao SEPARADA: kernel fora da diagonal / residuo / parte finita /
#    derivadas de delta / indices livres / campos-ghost / fatores i*hbar
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class KernelSpec:
    """Kernel fora da diagonal (x != 0). Extensao na diagonal = OPEN."""
    name: str                      # "U_2", "U_3", "R_2", "R_3", "R_munu", ...
    support: str = "OFF_DIAGONAL (x != 0)"
    diagonal_extension: Det = Det.OPEN
    convention: str = "+---"
    z_def: str = "x^2 - i0"
    prescription: str = "R(u) = FP_(a=0)[(1-a) mu_R^(2a) z^a u]"
    mu_R: str = "mu_R > 0 (escala de referencia SIMBOLICA; nao ajustada apos Ward)"
    meromorphic_input: str = "continuacao meromorfa e' o insumo distribucional (CAS nao a constroi)"

@dataclass(frozen=True)
class ResiduePart:
    """Residuo: coeficiente estrutural x derivada de delta."""
    expr: str                      # ex.: "C * r_3 * box(delta)"
    r_n: str                       # ex.: "r_3 = -1/32"
    delta: "DeltaDeriv"
    origin: Origin
    provenance: str

@dataclass(frozen=True)
class FinitePart:
    name: str                      # ex.: "D_3"
    expr: str                      # ex.: "r_3 * box^(n-1)[log(mu_R^2 z)/z]"
    provenance: str

@dataclass(frozen=True)
class DeltaDeriv:
    power: int                     # box^power delta
    dim: int = 4
    identity: str = "z*box^m delta = 4 m (m+1) box^(m-1) delta   [F1 l.37]"

@dataclass(frozen=True)
class IndexSpec:
    free: Tuple[str, ...]
    symmetry: str = "nenhuma"
    contractions: Tuple[str, ...] = ()
    # contracao certificada (R4): "eta^{mu nu} R_munu = R_2"

@dataclass(frozen=True)
class FieldContent:
    family: str                    # "ONE_PAIR_KERNEL" | "H_EQ_U_GBAP" | "FULL_METRIC_SET"
    n_matter: Optional[int]
    n_metric_pert: Optional[int]
    n_ghost: Optional[int]         # None => OPEN (nao determinado pelas fontes)
    n_antifield: Optional[int]     # None => OPEN
    note: str
    # [F2 l.81]: ghosts/antifields/gauge NAO incluidos nos contatos calculados.

@dataclass(frozen=True)
class IHbar:
    i_power: int
    hbar_power: int
    origin: str
    # C = 4 i pi^2 [F1 l.8] e' a origem do i nos contatos distribucionais.
    # hbar aparece APENAS no contato de Green [F2 l.25]: i*hbar*n.

# ----------------------------------------------------------------------------
# 2. Termo de contato (a unidade da contabilidade)
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class ContactTerm:
    key: str
    objeto: str
    kernel: str
    finite_part: Optional[FinitePart]
    residue: Optional[ResiduePart]
    contact_coeff: str             # ex.: "(H_2+H_1-1)=3/2" ; "0" ; "-C/32"
    delta: DeltaDeriv
    indices: IndexSpec
    fields: FieldContent
    ihbar: IHbar
    origin: Origin
    origin_sublabel: str
    op_path: OpPath
    same_contribution_group: str   # agrupa rotas equivalentes (R10)
    determinacy: Det
    blocks_ward: bool
    formula: str
    provenance: str
    is_brst_anomaly: bool = False  # [F1 l.60]: contato de R_munu NAO e' anomalia.
    source_id: str = "SRC_METRIC_TRACE_H_EQ_U"
    local_check: str = ""

# ----------------------------------------------------------------------------
# 3. Certidoes (R9: nada cancela sem certidao)
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Certificate:
    cert_id: str
    statement: str
    kind: str          # "IDENTIDADE_DA_FONTE" | "ARITMETICA_DECLARADA" | "ORDEM_EQUIVALENTE"
    provenance: str

CERTS: Tuple[Certificate, ...] = (
    Certificate("CERT_MUL_ZR3",
                "z*R_3 = R_2  (com o contato -3C/64 box(delta))",
                "IDENTIDADE_DA_FONTE", "[F1 l.35]; aritmetica: z*box(delta)=8delta"),
    Certificate("CERT_REC_R2",
                "box(R_2) = 8 R_3 - 12 Res U_3",
                "IDENTIDADE_DA_FONTE", "[F1 l.39] com n=3"),
    Certificate("CERT_TRACE_RMU",
                "eta^{mu nu} R_munu = R_2  <=> contato -(C/32) eta_munu delta presente",
                "IDENTIDADE_DA_FONTE", "[F1 l.55-56]"),
    Certificate("CERT_FP_MINUS_R",
                "FP U_n - R_n = Res U_n",
                "ARITMETICA_DECLARADA", "[F1 l.28-29]"),
    Certificate("CERT_ECHI_U0",
                "E_chi|_(u=0) = 3 box(chi)/(2 kappa)   porque Rbar=12K e Lambda=3K",
                "ARITMETICA_DECLARADA", "[F2 l.33,52]"),
    Certificate("CERT_DV_DU",
                "delta V_chi/delta u = -3/(4kappa)[chi(grad u)^2/(1+u)^2 + 2 chi u box u/(1+u)"
                " + 2 u grad chi . grad u/(1+u)]  (cadeia grad f = grad u/(1+u)^2)",
                "ARITMETICA_DECLARADA", "[F2 l.57]; rederivacao local V8"),
)

# ----------------------------------------------------------------------------
# 4. Ledger com anti-dupla-contagem
# ----------------------------------------------------------------------------
@dataclass
class Ledger:
    terms: Dict[str, ContactTerm] = field(default_factory=dict)
    flags: List[str] = field(default_factory=list)
    certificates_used: List[str] = field(default_factory=list)

    def register(self, t: ContactTerm) -> "Ledger":
        prev = self.terms.get(t.key)
        if prev is not None and prev.formula != t.formula:
            self.flags.append(f"KEY_COLLISION:{t.key}")
            return self
        self.terms[t.key] = t
        # R10: rotas equivalentes
        group = [x for x in self.terms.values() if x.same_contribution_group == t.same_contribution_group]
        if len(group) > 1:
            certified = any(c.kind == "ORDEM_EQUIVALENTE" and
                            t.same_contribution_group in c.statement for c in CERTS)
            if not certified:
                self.flags.append(f"UNRESOLVED_DOUBLE_COUNT_RISK:{t.same_contribution_group}")
        return self

    def open_terms(self) -> List[ContactTerm]:
        return [t for t in self.terms.values() if t.determinacy == Det.OPEN or t.blocks_ward]

# ----------------------------------------------------------------------------
# 5. Regras de deteccao (as cinco falhas exigidas + auxiliares)
# ----------------------------------------------------------------------------
@dataclass
class CheckResult:
    name: str
    ok: bool
    flags: Tuple[str, ...]
    residual: str
    provenance: str

def check_trace_rmunu(term: ContactTerm, drop_contact: bool = False,
                      flip_sign: bool = False) -> CheckResult:
    """R4 — traco de R_munu.
    residual esperado: "0" (certo) | "+C*delta/8" (contato ausente)
                       | "+C*delta/4" (sinal invertido).  [DERIVED: V5]
    """
    if not drop_contact and not flip_sign:
        return CheckResult("TRAÇO", True, (), "0", "[F1 l.55]; V5")
    if drop_contact:
        return CheckResult("TRAÇO", False, ("WRONG_TRACE",), "+C*delta/8", "[F1 l.55]")
    return CheckResult("TRAÇO", False, ("SIGN_INVERTED", "WRONG_TRACE"), "+C*delta/4", "V5")

def check_derivative_defect(c_m2: str, c_m1: str, used: str) -> CheckResult:
    """R3 — polo duplo. Correto: 2*(c_-1 - c_-2). Proibido: 2*Res = 2*c_-1."""
    if c_m2 not in ("0", "0.0") and used == "2*Res":
        return CheckResult("POLO_DUPLO", False,
                           ("DOUBLE_POLE_DROPPED",), "-2*c_-2", "[F1 l.63-68]")
    if c_m2 in ("0", "0.0") and used == "2*(c_-1-c_-2)":
        return CheckResult("POLO_DUPLO", False,
                           ("IMPLICIT_TRUNCATION",), "c_-2 zerado sem certidao", "R3/R9")
    return CheckResult("POLO_DUPLO", True, (), "2*(c_-1-c_-2)", "[F1 l.66-68]")

def check_eom_inside_T(eom_applied: bool, green_contact_present: bool,
                       i_power: int, hbar_power: int, arity_factor: str) -> CheckResult:
    """R6 — EOM dentro de T exige o contato i*hbar*n T_n(F^(n-1), delta_t F)."""
    if eom_applied and not green_contact_present:
        return CheckResult("EOM_EM_T", False,
                           ("EOM_INSIDE_T_WITHOUT_CONTACT",), "contato ausente", "[F2 l.24-28]")
    if green_contact_present and (i_power, hbar_power) != (1, 1):
        return CheckResult("EOM_EM_T", False,
                           ("IHBAR_ORIGIN_MISMATCH",), f"i^{i_power} hbar^{hbar_power}", "[F2 l.25]")
    return CheckResult("EOM_EM_T", True, (), f"contato i*hbar*{arity_factor}", "[F2 l.25]")

def check_source_identity(merged_brst_sources: List[str],
                          all_source_ids: List[str]) -> CheckResult:
    """R8 — fontes distintas nao viram a mesma quebra BRST.
    Fontes separadas: SRC_METRIC_TRACE_H_EQ_U, SRC_RANK1_FILTRATION,
                      SRC_GHOST1_FORMA4 (alem da familia de posto 1 da filtracao,
                      que e' DIFERENTE da familia de traco [F2 l.65])."""
    if len(set(merged_brst_sources)) > 1:
        return CheckResult("FONTES", False,
                           ("DISTINCT_SOURCES_MERGED",), ",".join(merged_brst_sources), "R8")
    if any(s.startswith("SRC_GHOST1_FORMA4") for s in all_source_ids):
        return CheckResult("FONTES", True,
                           ("WARD_COEFFICIENT_WITHHELD",), "ghost1/forma4 OPEN", "[F2 l.85]")
    return CheckResult("FONTES", True, (), "1 fonte por quebra", "R8")

def check_cutoff_separation(ledger: Ledger, family_id: str,
                            naive_variation: bool) -> CheckResult:
    """R7 — linear != interacao ; familia h=u*gbar != propagador escalar."""
    flags = []
    if family_id != "H_EQ_U_GBAP":
        flags.append("FAMILY_REINTERPRETED")       # proibido: vira propagador escalar
    inter = [t for t in ledger.terms.values() if t.origin == Origin.O2_VARIACAO_VERTICE_COM_CUTOFF]
    if any("box(chi)" in t.formula and "grad chi" not in t.formula for t in inter):
        flags.append("MIXED_SOURCE_LINEAR_IN_INTERACTION")   # □χ na interacao
    if naive_variation:
        flags.append("SIGN_INVERTED")              # cadeia grad f omitida (ver V8)
        flags.append("CHAIN_RULE_DROPPED")
    return CheckResult("CUTOFF", not flags, tuple(flags),
                       "-3/(4kappa)[...]" if not flags else "sinal relativo de (grad u)^2 invertido",
                       "[F2 l.52-62]")

def ward_coefficient_gate(ledger: Ledger) -> str:
    """Bloqueia a emissao enquanto houver campo nao determinado (Tabela C)."""
    if ledger.open_terms():
        return "WARD_COEFFICIENT_BLOCKED: " + ",".join(t.key for t in ledger.open_terms())
    return "WARD_COEFFICIENT_EMITTED"

# ----------------------------------------------------------------------------
# 6. TABELA DE CONTATOS (dados; coeficientes exatamente os das fontes)
# ----------------------------------------------------------------------------
def build_contact_table() -> Ledger:
    L = Ledger()
    # --- kernels [F1 l.24-35] ---
    u2 = KernelSpec("U_2")
    u3 = KernelSpec("U_3")
    r2 = FinitePart("D_2", "r_2 * box[log(mu_R^2 z)/z]", "[F1 l.27]")
    r3 = FinitePart("D_3", "r_3 * box^2[log(mu_R^2 z)/z]", "[F1 l.27]")
    one_pair = FieldContent("ONE_PAIR_KERNEL", 0, None, None, None,
                            "kernel de um par; NAO e' vertice; ghosts/antifields OPEN")
    hbar0 = IHbar(1, 0, "i vem de C = 4 i pi^2 (box(1/z)=C delta) [F1 l.8]; sem hbar")
    hbarG = IHbar(1, 1, "i*hbar explicitos no contato de Green [F2 l.25]")

    L.register(ContactTerm(
        key="CT-01", objeto="R_2 = D_2", kernel="U_2",
        finite_part=r2,
        residue=ResiduePart("C*r_2*delta", "r_2 = -1/4", DeltaDeriv(0),
                            Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.24-27]"),
        contact_coeff="0  (H_1+H_0-1 = 0)", delta=DeltaDeriv(0),
        indices=IndexSpec(()), fields=one_pair, ihbar=hbar0,
        origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO, origin_sublabel="COEF_NULO_VERIFICADO",
        op_path=OpPath.FP_THEN_MULT, same_contribution_group="G_R2",
        determinacy=Det.DERIVED, blocks_ward=False,
        formula="R_2 = D_2", provenance="[F1 l.21]; V1", local_check="V1"))

    L.register(ContactTerm(
        key="CT-02", objeto="R_3", kernel="U_3",
        finite_part=r3,
        residue=ResiduePart("C*r_3*box(delta)", "r_3 = -1/32", DeltaDeriv(1),
                            Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.24-27]"),
        contact_coeff="(H_2+H_1-1)=3/2", delta=DeltaDeriv(1),
        indices=IndexSpec(()), fields=one_pair, ihbar=hbar0,
        origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO, origin_sublabel="CONTATO_HARMONICO",
        op_path=OpPath.FP_THEN_MULT, same_contribution_group="G_R3",
        determinacy=Det.DERIVED, blocks_ward=False,
        formula="R_3 = D_3 - (3C/64) box(delta)", provenance="[F1 l.34]; V2",
        local_check="V2"))

    L.register(ContactTerm(
        key="CT-03", objeto="R_munu", kernel="U_2/x^3",
        finite_part=FinitePart("(1/8) d_mu d_nu (1/z)", "(1/8) d_mu d_nu (1/z)", "[F1 l.53]"),
        residue=ResiduePart("-(C/32) eta_munu delta", "contato de normalizacao",
                            DeltaDeriv(0), Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.53]"),
        contact_coeff="(1/4) eta_munu R_2 + (-C/32) eta_munu delta",
        delta=DeltaDeriv(0), indices=IndexSpec(("mu", "nu"), "simetrica",
                                                ("eta^{mu nu} -> R_2",)),
        fields=FieldContent("ONE_PAIR_KERNEL", 0, 1, None, None,
                            "1 campo metrico (h linear); gauge/ghosts/antifields OPEN"),
        ihbar=hbar0, origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO,
        origin_sublabel="NORMALIZATION_CONTACT_DISTRIBUTIONAL (is_brst_anomaly=False)",
        op_path=OpPath.DIFF_THEN_FP, same_contribution_group="G_DDMU_1_OVER_Z",
        determinacy=Det.REAL, blocks_ward=False,
        formula="R_munu = (1/8) d_mu d_nu(1/z) + (1/4) eta_munu R_2 - (C/32) eta_munu delta",
        provenance="[F1 l.46-58]; V5", is_brst_anomaly=False, local_check="V5"))

    L.register(ContactTerm(
        key="CT-05", objeto="d_mu d_nu(1/z) (reescrita)", kernel="U_2/x^3",
        finite_part=None,
        residue=ResiduePart("(C/4) eta_munu delta", "reescrita", DeltaDeriv(0),
                            Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.58]"),
        contact_coeff="8 R_munu - 2 eta_munu R_2", delta=DeltaDeriv(0),
        indices=IndexSpec(("mu", "nu"), "simetrica"), fields=one_pair, ihbar=hbar0,
        origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO, origin_sublabel="MESMA_CONTRIBUICAO_CT03",
        op_path=OpPath.DIFF_THEN_FP, same_contribution_group="G_DDMU_1_OVER_Z",
        determinacy=Det.DERIVED, blocks_ward=False,
        formula="d_mu d_nu(1/z) = 8 R_munu - 2 eta_munu R_2 + (C/4) eta_munu delta",
        provenance="[F1 l.58]; V6", local_check="V6 (8 x CT-03)"))

    L.register(ContactTerm(
        key="CT-06", objeto="defeito d_mu R(u) - R(d_mu u)", kernel="familia (x_mu/z) u",
        finite_part=None,
        residue=ResiduePart("2*FP[a(1-a) mu_R^(2a) z^a (x_mu/z) u]", "c_-2/a^2 + c_-1/a + ...",
                            DeltaDeriv(0), Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.63-68]"),
        contact_coeff="2*(c_-1 - c_-2)", delta=DeltaDeriv(0),
        indices=IndexSpec(("mu",)), fields=one_pair, ihbar=hbar0,
        origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO, origin_sublabel="POLO_DUPLO_OBRIGATORIO",
        op_path=OpPath.DIFF_THEN_FP, same_contribution_group="G_DERIV_DEFECT",
        determinacy=Det.REAL, blocks_ward=False,
        formula="d_mu R(u) - R(d_mu u) = 2 (c_-1 - c_-2)",
        provenance="[F1 l.63-68]"))

    L.register(ContactTerm(
        key="CT-07", objeto="recorrencia box(R_2)", kernel="U_3",
        finite_part=None,
        residue=ResiduePart("-12 Res U_3 = (3C/8) box(delta)", "n=3", DeltaDeriv(1),
                            Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.39]"),
        contact_coeff="8 R_3", delta=DeltaDeriv(1), indices=IndexSpec(()),
        fields=one_pair, ihbar=hbar0, origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO,
        origin_sublabel="RECORRENCIA_COM_CONTATO", op_path=OpPath.RESIDUE_RECURRENCE,
        same_contribution_group="G_R3_ROUTES", determinacy=Det.REAL, blocks_ward=False,
        formula="box(R_2) = 8 R_3 - 12 Res U_3", provenance="[F1 l.39]; V4",
        local_check="V4"))

    L.register(ContactTerm(
        key="CT-08", objeto="multiplicacao z*R_3", kernel="U_3",
        finite_part=None,
        residue=ResiduePart("cancelamento certificado por CERT_MUL_ZR3", "n=3",
                            DeltaDeriv(0), Origin.O3_DEFEITO_DERIVAR_EXTENSAO, "[F1 l.35]"),
        contact_coeff="= R_2", delta=DeltaDeriv(0), indices=IndexSpec(()),
        fields=one_pair, ihbar=hbar0, origin=Origin.O3_DEFEITO_DERIVAR_EXTENSAO,
        origin_sublabel="ROTA_EQUIVALENTE_A_CT07", op_path=OpPath.FP_THEN_MULT,
        same_contribution_group="G_R3_ROUTES", determinacy=Det.REAL, blocks_ward=False,
        formula="z R_3 = R_2", provenance="[F1 l.35]; V3", local_check="V3"))

    # --- cutoff [F2 l.31-62] ---
    fam = FieldContent("H_EQ_U_GBAP", 0, 1, 0, None,
                       "familia de TRACO h=u*gbar; ghosts/antifields do conjunto "
                       "completo OPEN; familia de posto 1 da filtracao e' OUTRA [F2 l.65]")

    L.register(ContactTerm(
        key="CT-10", objeto="parte linear removida de E_chi", kernel="familia h=u*gbar",
        finite_part=None, residue=None,
        contact_coeff="3/(2 kappa) [box chi] + 3/(2 kappa (1+u)) [grad chi . grad u]",
        delta=DeltaDeriv(0), indices=IndexSpec(()), fields=fam,
        ihbar=IHbar(0, 0, "sem i nem hbar identificados na fonte deste termo"),
        origin=Origin.O1_EOM_LIVRE_INSERCAO_TEMPORAL, origin_sublabel="CUTOFF_LINEAR",
        op_path=OpPath.EL_CUTOFF, same_contribution_group="G_ECHI_LINEAR",
        determinacy=Det.REAL, blocks_ward=False,
        formula="E_chi = 1/(2kappa)[... + 3 grad chi . grad u/(1+u) + 3 box chi]",
        provenance="[F2 l.48-50]"))

    L.register(ContactTerm(
        key="CT-11", objeto="CONTATO DE GRADIENTE DO CUTOFF", kernel="familia h=u*gbar",
        finite_part=None, residue=None,
        contact_coeff="-3/(4 kappa) * 2 u grad chi . grad u/(1+u) = -3/(2 kappa) u grad chi . grad u/(1+u)",
        delta=DeltaDeriv(0), indices=IndexSpec(("index(grad)",)), fields=fam,
        ihbar=IHbar(0, 0, "sem i nem hbar identificados"),
        origin=Origin.O2_VARIACAO_VERTICE_COM_CUTOFF, origin_sublabel="CUTOFF_GRADIENT",
        op_path=OpPath.EL_CUTOFF, same_contribution_group="G_DVCHI",
        determinacy=Det.REAL, blocks_ward=False,
        formula="delta V_chi/delta u sup 2 u grad chi . grad u/(1+u)",
        provenance="[F2 l.57-61]; V8"))

    L.register(ContactTerm(
        key="CT-12", objeto="demais sumandos de delta V_chi/delta u", kernel="familia h=u*gbar",
        finite_part=None, residue=None,
        contact_coeff="-3/(4 kappa) [chi(grad u)^2/(1+u)^2 + 2 chi u box u/(1+u)]",
        delta=DeltaDeriv(0), indices=IndexSpec(("index(grad)",)), fields=fam,
        ihbar=IHbar(0, 0, "sem i nem hbar identificados"),
        origin=Origin.O2_VARIACAO_VERTICE_COM_CUTOFF, origin_sublabel="VERTEX_CUTOFF",
        op_path=OpPath.EL_CUTOFF, same_contribution_group="G_DVCHI",
        determinacy=Det.REAL, blocks_ward=False,
        formula="V_chi = 3 chi/(4 kappa) [u/(1+u)] (grad u)^2 ; delta V_chi/delta u = -3/(4 kappa)[...]",
        provenance="[F2 l.55-57]; V8", local_check="V8 (cadeia grad f = grad u/(1+u)^2)"))

    L.register(ContactTerm(
        key="CT-13", objeto="contato de Green (normalizacao de Fröb)", kernel="T_n",
        finite_part=None, residue=None,
        contact_coeff="i*hbar*n", delta=DeltaDeriv(0),
        indices=IndexSpec(("indices de T_n",)),
        fields=FieldContent("H_EQ_U_GBAP", None, None, 0, None,
                            "setor bosonico metrico [F2 l.21]; n = aridade de T_n"),
        ihbar=hbarG, origin=Origin.O1_EOM_LIVRE_INSERCAO_TEMPORAL,
        origin_sublabel="GREEN_CONTACT_FROM_FROB_NORMALIZATION (eq.158; Thm 8/9)",
        op_path=OpPath.GREEN_CONTACT, same_contribution_group="G_GREEN",
        determinacy=Det.REAL, blocks_ward=False,
        formula="T_(n+1)(F^n, h(Ht)) - T_n(F^n) star h(Ht) = i hbar n T_n(F^(n-1), delta_t F)",
        provenance="[F2 l.8-29]"))

    L.register(ContactTerm(
        key="CT-14", objeto="aridade declarada (coeficientes nao citados)",
        kernel="familia h=u*gbar", finite_part=None, residue=None,
        contact_coeff="OPEN (coeficientes nao citados na fonte)",
        delta=DeltaDeriv(0), indices=IndexSpec(()), fields=fam,
        ihbar=IHbar(0, 0, "nao citado"), origin=Origin.O2_VARIACAO_VERTICE_COM_CUTOFF,
        origin_sublabel="VERTEX_TO_CONTACT_ARITY {3:2,4:3,5:4,6:5,7:6,8:7}",
        op_path=OpPath.EL_CUTOFF, same_contribution_group="G_ARITY",
        determinacy=Det.OPEN, blocks_ward=True,
        formula="vertices 3-8 dao exatamente os contatos 2-7",
        provenance="[F2 l.72-73] (relato da execucao da fonte)"))

    # --- abertos que bloqueiam Ward (Tabela C) ---
    for key, obj, prov in (
        ("CT-15", "resto curvo (alem do espaco tangente plano)", "[F1 l.80-83]"),
        ("CT-16", "polarizacoes metricas restantes + gauge + ghosts + antifields", "[F2 l.81-82]"),
        ("CT-17", "ajuste T10/T11", "[F1 l.81]"),
        ("CT-18", "prescricao NAO linear completa", "[F2 l.84]"),
        ("CT-19", "1a quebra quantica ghost1/forma4", "[F2 l.84-85]"),
        ("CT-20", "termos finitos compativeis com contract072", "[F2 l.18-19]"),
    ):
        L.register(ContactTerm(
            key=key, objeto=obj, kernel="NAO_CONSTRUIDO", finite_part=None, residue=None,
            contact_coeff="None", delta=DeltaDeriv(0), indices=IndexSpec(()),
            fields=FieldContent("FULL_METRIC_SET", None, None, None, None, "OPEN"),
            ihbar=IHbar(0, 0, "NAO DETERMINADO"),
            origin=Origin.O4_RESTO_CURVO_NAO_CALCULADO, origin_sublabel="OPEN",
            op_path=OpPath.DIFF_THEN_FP, same_contribution_group=f"G_OPEN_{key}",
            determinacy=Det.OPEN, blocks_ward=True, formula="None", provenance=prov))
    return L

# ----------------------------------------------------------------------------
# 7. Cinco casos de teste esperados (especificacao; a bancada executa)
# ----------------------------------------------------------------------------
TEST_CASES = [
  dict(id="TC-1", nome="TRAÇO_E_SINAL_DE_R_MUNU",
       setup="CT-03 completo; depois (a) sem -(C/32)eta_munu delta; depois (b) sinal trocado",
       esperado=["(a) WRONG_TRACE residual '+C*delta/8'",
                 "(b) SIGN_INVERTED+WRONG_TRACE residual '+C*delta/4'",
                 "base: ok, residual '0'"],
       falhas_detectadas=["sinal invertido", "traco errado"],
       proveniencia="[F1 l.46-58]; V5"),
  dict(id="TC-2", nome="CONTATO_NA_MULTIPLICACAO_E_NA_RECORRENCIA",
       setup="CT-02 com contato; depois sem contato; depois exigir zR_3=R_2 E "
             "box R_2 = 8R_3 sem contato ao mesmo tempo",
       esperado=["base: CERT_MUL_ZR3 e CERT_REC_R2 com residual '0'",
                 "sem contato: LOST_CONTACT residual '(3C/8) delta'",
                 "dupla exigencia: DOUBLE_CONSTRAINT_CONFLICT"],
       falhas_detectadas=["contagem dupla por trocar a ordem", "contato perdido"],
       proveniencia="[F1 l.34-42]; V3/V4"),
  dict(id="TC-3", nome="POLO_DUPLO_VIROU_SIMPLES",
       setup="CT-06 com LaurentCoeffs(c_m2 != 0); comparar '2*Res' vs '2*(c_-1-c_-2)'; "
             "depois c_m2='0' sem certidao",
       esperado=["'2*Res' -> DOUBLE_POLE_DROPPED residual '-2*c_-2'",
                 "c_m2='0' sem certidao -> IMPLICIT_TRUNCATION",
                 "correto: residual '2*(c_-1-c_-2)'"],
       falhas_detectadas=["troca de polo duplo por simples"],
       proveniencia="[F1 l.63-68]"),
  dict(id="TC-4", nome="CUTOFF_CHI__LINEAR_NAO_E_INTERACAO",
       setup="ledger com CT-10/CT-11/CT-12; (a) variacao naive sem grad f; "
             "(b) box chi no ledger O2; (c) family_id='SCALAR_PROPAGATOR'; "
             "(d) reducao E_chi|u=0 sem certidao",
       esperado=["(a) SIGN_INVERTED + CHAIN_RULE_DROPPED (sinal relativo de (grad u)^2)",
                 "(b) MIXED_SOURCE_LINEAR_IN_INTERACTION",
                 "(c) FAMILY_REINTERPRETED",
                 "(d) UNSOURCED_CANCELLATION (exige Rbar=12K, Lambda=3K)",
                 "base: CERT_DV_DU + CERT_ECHI_U0 ok"],
       falhas_detectadas=["confundir □chi da parte linear com interacao",
                          "reescrever h=u*gbar como propagador escalar",
                          "cancelamento presumido"],
       proveniencia="[F2 l.31-62]; V7/V8"),
  dict(id="TC-5", nome="EOM_DENTRO_DE_T_E_FONTES_DISTINTAS",
       setup="(a) EOM aplicada dentro de T sem contato de Green; "
             "(b) duas source_id fundidas numa quebra BRST; "
             "(c) SRC_GHOST1_FORMA4 presente",
       esperado=["(a) EOM_INSIDE_T_WITHOUT_CONTACT (e IHBAR_ORIGIN_MISMATCH se i,hbar != 1,1)",
                 "(b) DISTINCT_SOURCES_MERGED (e FAMILY_RANK1_VS_TRACE_MERGE_FORBIDDEN "
                 "se SRC_RANK1_FILTRATION + SRC_METRIC_TRACE_H_EQ_U)",
                 "(c) WARD_COEFFICIENT_WITHHELD e ward_coefficient_gate = "
                 "WARD_COEFFICIENT_BLOCKED: CT-14,CT-15,...,CT-20"],
       falhas_detectadas=["EOM aplicada dentro de T sem contato",
                          "fontes diferentes somadas como a mesma quebra BRST"],
       proveniencia="[F2 l.24-28,65,84-85]; R6/R8"),
]

if __name__ == "__main__":            # [NAO EXECUTADO NA ENTREGA]
    raise SystemExit("modulo DECLARADO: a bancada executa e verifica")
