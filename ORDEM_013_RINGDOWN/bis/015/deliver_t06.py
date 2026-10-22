"""Audit T06 scopes, quoted prior declarations and numerical stability."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,sys
B=Path(__file__).resolve().parents[2];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';D=B/'bis/015/t06';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
x=json.loads((D/'RESULT.json').read_bytes());assert x['status']=='T06_NONBLIND_PROFILE_DIAGNOSTIC_NOT_PHYSICAL_TEST' and len(x['jackknife'])==33
prior=[]
for e in x['prior_contract']:
    d=e['df220_prior'];texts=[s for t in d['declarations'] for s in t['text']]
    # Parse descriptive text only. Never evaluate a release's configuration string.
    found=[]
    for s in texts:
        if s.startswith('Uniform(') or 'domega220 = Uniform(' in s:
            fragment=s if s.startswith('Uniform(') else s.split('domega220 = ',1)[1].split(')',1)[0]+')'
            lo=re.search(r'minimum=([-+0-9.]+)',fragment);hi=re.search(r'maximum=([-+0-9.]+)',fragment)
            if lo and hi:found.append((float(lo[1]),float(hi[1])))
    assert found and len(set(found))==1,e['event']
    prior.append(dict(event=e['event'],declared_uniform_bounds=list(found[0]),joint_factorization=d['joint_factorization'],status='DECLARADO_TEXT_NOT_INDEPENDENTLY_VALIDATED'))
assert all(t['joint_factorization']=='OPEN' for t in prior)
summary={}
for kind in ['gaussian','kde']:
    js=[z[kind] for z in x['jackknife']]
    summary[kind]=dict(LRT_range=[min(z['LRT'] for z in js),max(z['LRT'] for z in js)],upper_range=[min(z['sigma_upper_nominal_profile90'] for z in js),max(z['sigma_upper_nominal_profile90'] for z in js)])
audit=dict(at=datetime.now(timezone.utc).isoformat(),status='T06_DIAGNOSTIC_SCOPE_AUDITED',result_sha256=sha(D/'RESULT.json'),prior_declarations=prior,jackknife_summary=summary,
    warning='Uniform prior is DECLARADO and joint factorization OPEN; smoothing leaks beyond prior edges. This is a sensitivity diagnostic, not normalized population inference or physical confidence limit.',
    maximum_exact_logL_compression_error=max(abs(v['logL_compression_error']) for v in x['exact_mixture_controls']))
save(D/'AUDIT.json',audit);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
g=x['results']['gaussian'];k=x['results']['kde']
text=f'''[REAL — diagnóstico NÃO-CEGO executado; DERIVED condicional — perfil de dispersão, sem p físico]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {opening}

T06 PAGO como diagnóstico nos33 posteriores completos arquivados. Média comum perfilada, dispersão não negativa. Gaussiana: LRT={g['LRT']:.9f}, σ_pop_MLE={g['sigma_pop_MLE']:.9f}, μ={g['mu_MLE']:.9f}; KDE/amostras: LRT={k['LRT']:.9f}, σ_pop_MLE={k['sigma_pop_MLE']:.9f}, μ={k['mu_MLE']:.9f}. Os pesos informacionais1/σ_i⁴ foram reportados, sem multiplicar novamente a contribuição de cada evento à likelihood.

Limite de perfil no nível nominal Δ(2logL)=2,705543: gaussiana {g['sigma_upper_nominal_profile90']:.9f}, KDE {k['sigma_upper_nominal_profile90']:.9f}. O0,0243 transportado anteriormente não foi copiado: diferenças {g['sigma_upper_nominal_profile90']-.0243:+.9f} e {k['sigma_upper_nominal_profile90']-.0243:+.9f}. Estes são níveis de perfil, NÃO intervalos físicos com cobertura demonstrada; σ_jit físico=null. Média, seleção, prior de publicação e transferência de jitter precisam de calibração.

Sensibilidade e controles:33 exclusões individuais; faixas de limite nominal gaussiano {summary['gaussian']['upper_range']}, KDE {summary['kde']['upper_range']}. KDE usa Scott; compressão512 conferida com2048 e avaliação da mistura de TODAS as amostras nos pontos críticos (erro máximo logL={audit['maximum_exact_logL_compression_error']:.8g}). Fracção de centros além3σ={x['observed_center_jump_fraction']:.9f}; média das fracções posteriores além3σ={x['posterior_mean_jump_fraction']:.9f}; objetos diferentes, ambos em RESULT.json.

Ressalva de fonte:33 priors marginais têm declaração textual Uniform conferida; fatoração conjunta permanece OPEN. A KDE suavizada pode ultrapassar as bordas. Nenhum desses fatos autoriza tratar o diagnóstico como likelihood física plenamente normalizada. Comparação é NÃO-CEGA, não entra no teste registrado, não muda gate ou veredito. O ringdown compra condição, não σ.

ResultadoSHA256 {sha(D/'RESULT.json')}; auditoriaSHA256 {sha(D/'AUDIT.json')}; códigoSHA256 {sha(B/'bis/015/measure_t06.py')}. CPU{x['cpu_seconds']:.6f}s, parede{x['wall_seconds']:.6f}s, horas pesadas0; axiomasN/A. Reprodução: /opt/lal_env/bin/python -B bis/015/measure_t06.py, saída única, recusa repetição. PróximoT11.
'''
write(OUT/'ENTREGA_015_T06_rota_IV.md',text.encode())
write(D/'REAPROVEITAMENTO_T06.md',b'[REAL - reutilizacao]\n33 posteriores extraidos, pin no E7_FINAL_EXECUTION_V1; nenhuma extracao nova, nenhuma PE e nenhum dado cego. A forma do LRT gaussiano reutiliza a convencao de media perfilada da rotaIV; a KDE e apenas diagnostico de sensibilidade. Prior conjunto e calibracao fisica continuam OPEN.\n')
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{audit["at"]} — B/T06 PAGO diagnóstico:33 posteriores e33 jackknifes, LRT0 nas duas leituras estatísticas; CPU{x["cpu_seconds"]:.6f}s, horas pesadas0. AberturaSHA256 {opening}. PróximoT11.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=audit['at'],own_live_process=None,own_live_processes=[],T06_delivery=str(D/'RESULT.json'),next='T11 neutrino_m2_reader from pinned cache/casa/um.py AST/text only, reproduce frozen hash and2.9528540277; thenT12 E7 and allocation. T06 completed, no live process, R7 absent. Three D6 egress permissions still pending.');save(q,c,True)
print(json.dumps(dict(status=audit['status'],jackknife=summary)))
