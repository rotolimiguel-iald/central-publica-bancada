"""Write a new, source-linked data-availability inventory; never edit originals."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
FILES = ['CONSULTA_F72_R1.txt', 'DATA_AVAILABILITY_R1.json', 'DATA_AVAILABILITY_R1.md', 'INVENTORY_RECEIPT_R1.json']
for filename in FILES:
    if (ROOT / filename).exists():
        raise FileExistsError(ROOT / filename)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_new(name, data):
    encoded = data.encode('utf-8') if isinstance(data, str) else data
    with (ROOT / name).open('xb') as stream:
        stream.write(encoded)
    assert (ROOT / name).read_bytes() == encoded
    return {'path': str(ROOT / name), 'bytes': len(encoded), 'sha256': sha(encoded)}

started = datetime.now(timezone.utc).isoformat()
command = [sys.executable, '-B', r'C:\IALD\NOS_VIVO\consultar.py', '--unidade', 'F7.2']
run = subprocess.run(command, capture_output=True, check=False)
if run.returncode:
    raise RuntimeError(f'Nos Vivo read failed: {run.returncode}: {run.stderr.decode(errors="replace")}')
query_artifact = write_new(FILES[0], run.stdout)
source = ROOT.parent.parent / 'F7.2' / 'V2_STAGING' / 'TABELA_DE_PODER_POR_CANAL_V2.md'
source_bytes = source.read_bytes()
source_record = {'path': str(source), 'sha256': sha(source_bytes), 'bytes': len(source_bytes), 'read_scope': 'entire local table; no PDFs opened', 'reused': 'F7.2 already catalogs n=-2 and the JUNO damping bound; operator matching and compatible likelihood remain OPEN. The present survey only adds availability and identifies September update.', 'historical_text_warning': 'This pinned V2 contains staging-status and section-anchor text superseded by later additive errata. No deployment status is inferred here; Eq.6 is in III.B of the paper.'}

sources = [
 {'id':'S1','title':'JUNO first measurement, Nature 654,343-348 (2026)','url':'https://www.nature.com/articles/s41586-026-10538-z','doi':'10.1038/s41586-026-10538-z','published':'2026-06-10','consulted_utc_date':'2026-10-09','anchors':['Data availability','Code availability','Supplementary information'],'verified_access':'publisher HTML','available':['source-data links for Figures 3,4 and Extended Data Figure 2','Supplementary Data ZIP link'],'not_public_per_source':['raw detector data','collaboration simulation and raw-analysis code'],'not_verified':['ZIP contents, detector response matrix, full nuisance covariance, likelihood payload'],'download_status':'No source-data bytes downloaded; web ZIP click returned an internal error. No checksum asserted.','inference':'Figure-level release is useful but its existence does not certify a complete likelihood for an arbitrary new dissipator.'},
 {'id':'S2','title':'JUNO updated oscillation measurement and mass ordering indication','url':'https://arxiv.org/html/2609.37895v1','doi':'10.48550/arXiv.2609.37895','published':'2026-09-29','consulted_utc_date':'2026-10-09','anchors':['analysis Eq.(1)','detector response paragraphs','Figure 3'],'verified_access':'full arXiv HTML','available':['paper describes 207.2 live days and 8294 IBD candidates','joint JUNO,TAO,Daya Bay chi-square and nuisance construction'],'not_verified':['numerical release for the updated JUNO/TAO spectra, response matrices and covariance'],'download_status':'Paper HTML only; no observed tables downloaded.','inference':'The newer exposure cannot be substituted into the June decoherence bound without reanalysis. Failure to locate a numerical release in this survey is not proof of its absence.'},
 {'id':'S3','title':'KamLAND official release collection','url':'https://www.awa.tohoku.ac.jp/KamLAND/2013_result_data_release/2013PRD.html','published':'2013 result; release page updated 2020-07-21','consulted_utc_date':'2026-10-09','anchors':['2013 chi-square map','4th release Prompt Energy Spectrum','2nd release Event List and Other Relevant Constants'],'verified_access':'official HTML pages','related_urls':['https://www.awa.tohoku.ac.jp/KamLAND/4th_result_data_release/4th_result_data_release.html','https://www.awa.tohoku.ac.jp/KamLAND/datarelease/2ndresult.html'],'available':['2013: standard-parameter chi-square map advertised,57MB','2011: prompt-energy histogram advertised,0.1MeV bins,observed/reactor/background columns,efficiency incorporated','2005: candidate energies and monthly livetime,backgrounds,fission flux and approximate resolution advertised'],'not_verified':['data-file bytes','complete correlated response and nuisance likelihood for a new dephasing model'],'download_status':'Release landing pages only; no event list,histogram or large chi-square map downloaded.','inference':'A chi-square map only in standard oscillation parameters is not a likelihood in Gamma. Histogram reconstruction requires model validation.'},
 {'id':'S4','title':'Beccaria and Ternes: damping with first JUNO data','url':'https://arxiv.org/html/2606.13362v1','doi':'10.48550/arXiv.2606.13362','published':'2026-06-11','consulted_utc_date':'2026-10-09','anchors':['II Eq.(1)','III.B Eq.(6)','IV.B Eq.(13)','Table I'],'verified_access':'full arXiv HTML','available':['GLoBES and Poisson-plus-pulls analysis specification','published conditional 90% CL n=-2 bound,gamma<4.1e-27GeV'],'texture':{'gamma21':'gamma','gamma31':'gamma','gamma32':0,'E0_GeV':1,'n':-2,'delta_chi2':2.71,'solar_prior':'sin^2(theta12)=0.308 +/- 0.020; compare profiles with/without'},'not_verified':['authors numerical likelihood or code release'],'download_status':'HTML only in this unit; F7.2 earlier custody is not re-certified here.','inference':'Matching exponent n=-2 alone is insufficient. A double commutator with H generally has rates proportional to squared mass-squared splittings, not this equality/zero texture.'},
 {'id':'S5','title':'Wright et al.: Ia deflagration-to-detonation neutrino prediction','url':'https://arxiv.org/html/1605.01408v2','doi':'10.1103/PhysRevD.94.025026','published':'2016-07-19; arXiv v2 2016-08-22','consulted_utc_date':'2026-10-09','anchors':['IV.1 Eq.(10)','V Eq.(11)','VI.1','VI.2 Table2'],'verified_access':'full arXiv HTML','available':['model N100nu time,energy,flavor,trajectory predictions in article','JUNO-like interaction expectation at10kpc:0.014 NMO,0.032 IMO before efficiency loss'],'not_verified':['machine-readable N100nu flux files','joint observed Ia neutrino/bolometric sample'],'download_status':'Article only; no simulation flux file downloaded.','inference':'The model already takes vacuum propagation to Earth as decohered. Additional pure dephasing in the same mass basis after complete decoherence cannot alter the populations; effects in matter/production require a separate calculation.'},
 {'id':'S6','title':'SNOwGLoBES official repository','url':'https://github.com/SNOwGLoBES/snowglobes','related_urls':['https://github.com/SNOwGLoBES/snowglobes/tree/master/fluxes','https://github.com/SNOwGLoBES/snowglobes/blob/master/doc/tex_src/snowglobes_1.1.tex'],'published':'living repository,not commit-pinned in this survey','consulted_utc_date':'2026-10-09','anchors':['repository directories','fluxes listing','manual Supernova Neutrino Fluxes'],'verified_access':'repository HTML and manual text','available':['cross-sections,efficiencies,smearing and flux example directories','Livermore/GKVM examples and pinched-flux generator'],'not_verified':['full repository bytes or commit','N100nu flux in repository','operational build'],'download_status':'No clone,installation or execution.','inference':'Suitable for a synthetic forecast after a physical flux and operator are supplied; representative response does not replace experiment-specific response/covariance.'}
]

payload = {'unit':'F8.2.NU2','claim_event':618,'author':'codex-gerente-tgl / nu2_data_sources','created_utc':datetime.now(timezone.utc).isoformat(),'status':'DERIVED_DOCUMENTARY_AVAILABILITY_SURVEY','existing_local_source':source_record,'nos_vivo':{'command':command,'exit_code':run.returncode,'artifact':query_artifact,'initial_sandbox_attempt':'Denied before execution; read succeeded after permitted escalation.'},'sources':sources,'scope':{'observed_fit_executed':False,'raw_data_downloaded':False,'provider_called':False,'original_modified':False,'memory_modified':False,'bench_modified':False,'writes':'Only new derived files inside this unit/data_inventory'},'recommendation':'First derive and test the exact TGL rate texture in a synthetic reactor spectrum. Keep Ia as a separate source/in-matter branch; no 5sigma result is inferred from published upper limits.'}
json_artifact = write_new(FILES[1], json.dumps(payload, ensure_ascii=False, indent=2)+'\n')

note = '''# F8.2.NU2 — disponibilidade de dados de neutrinos, R1

Unidade reivindicada pela coordenação, evento 618. Autor: Codex / nu2_data_sources. Consulta em 09/10/2026.

## O que a casa já tem

[REAL documental] O Nós Vivo F7.2 foi consultado antes desta nota; devolveu F7.2 FECHADA e localizou as tabelas do canal n=-2. A TABELA_DE_PODER_POR_CANAL_V2.md foi lida: ela já registra o limite JUNO e mantém SEM_LIMITE_TGL até ligar operador e likelihood. Reaproveitamos esse alcance. Seu antigo estado de staging não é usado; a âncora vigente da Eq.(6) é III.B. Caminho, hash lido dos bytes e recibo da consulta estão no JSON vizinho.

## Seis entradas primárias

1. **JUNO 59,1 dias.** [Artigo Nature](https://www.nature.com/articles/s41586-026-10538-z), publicado em 10/06/2026. Data availability oferece source data de Fig.3,4 e Extended2; código e dados brutos não são públicos. Há link de ZIP suplementar, mas seu conteúdo não foi conferido (o clique pelo navegador de pesquisa falhou). [OPEN] Matriz completa de resposta/covariância e likelihood do pacote.
2. **JUNO atualizado.** [arXiv:2609.37895v1](https://arxiv.org/html/2609.37895v1), 29/09/2026: 207,2 dias e 8.294 candidatos, ajuste conjunto JUNO–TAO–Daya Bay. Eq.(1) explicita resposta, covariâncias e nuisances. Não localizamos release numérica correspondente nesta consulta. Isso não prova inexistência. Não se substitui a exposição no limite de junho sem reanálise.
3. **KamLAND oficial.** [Coleção 2013](https://www.awa.tohoku.ac.jp/KamLAND/2013_result_data_release/2013PRD.html) anuncia mapa chi-quadrado usual (57 MB). A [release 2011](https://www.awa.tohoku.ac.jp/KamLAND/4th_result_data_release/4th_result_data_release.html) anuncia histograma observado/predições/fundos com eficiência incorporada. A [release 2005](https://www.awa.tohoku.ac.jp/KamLAND/datarelease/2ndresult.html) anuncia energias individuais, livetime mensal, fundos, fissão e resolução aproximada. Nenhuma tabela de eventos foi baixada. [DERIVED] Mapa apenas nos parâmetros usuais não é likelihood em Gamma; recálculo exige reproduzir o padrão.
4. **Textura do limite JUNO.** [Beccaria–Ternes](https://arxiv.org/html/2606.13362v1), 11/06/2026, §§II,III.B,IV.B: GLoBES, Poisson+pulls e comparação com/sem prior solar. O limite 4,1e-27 GeV,90%CL,Delta chi2=2,71 é para gamma21=gamma31,gamma32=0,n=-2,E0=1GeV. [DERIVED] O duplo comutador com H geralmente tem gammaij proporcional a (Delta mij^2)^2. Coincidência do expoente não transfere a cota à TGL.
5. **Ia simulada.** [Wright2016 v2](https://arxiv.org/html/1605.01408v2), §IV.1 Eq.(10): propagação ao detector já decoerida na base massiva. A Tabela2 prevê para JUNO-like 0,014/0,032 interações NMO/IMO a10kpc, antes de perda por eficiência, no modelo N100nu. Não localizamos arquivo de fluxo N100nu nem amostra observada conjunta Ia–neutrinos–bolometria. [DERIVED condicional] Dephasing adicional na mesma base após decoerência completa não altera populações. Produção/matéria são rotas diferentes.
6. **Ferramenta de previsão.** [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes): código,seções de choque,eficiências e smearing; listagem fluxes com Livermore/GKVM e gerador pinched. N100nu não apareceu nessa listagem. Repositório não foi clonado,pinado ou executado. Respostas são representativas; não certificam a resposta detalhada do aparelho.

## Alcance e próximo passo

[REAL documental] Consultamos HTML/artigos e metadados das releases. Nenhum evento,histograma bruto ou matriz experimental foi aberto para ajuste. Não há hash alegado dos downloads externos porque os bytes não foram custodiados nesta unidade; os URLs e limites de acesso estão explícitos. Foram escritos apenas artefatos derivados novos nesta pasta. Originais,memórias,Bancada e kernel não foram alterados.

[PROPOSTA] Derivar primeiro a textura de taxas TGL e medi-la no sintético de reatores. A rota Ia requer fluxo de produção e tratamento em matéria; as fontes consultadas não entregam uma amostra observada conjunta para esse teste. Nenhum limite publicado foi convertido em significância TGL, e não se obteve 5sigma nesta etapa.
'''
note_artifact = write_new(FILES[2], note)
receipt = {'unit':'F8.2.NU2','claim_event':618,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'writer':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes())},'artifacts':[query_artifact,json_artifact,note_artifact],'source':source_record,'all_new_exclusive_creation':True,'no_remote_data_bytes_custody':True}
receipt_artifact = write_new(FILES[3], json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'artifacts':receipt['artifacts']+[receipt_artifact]}, ensure_ascii=False, indent=2))
