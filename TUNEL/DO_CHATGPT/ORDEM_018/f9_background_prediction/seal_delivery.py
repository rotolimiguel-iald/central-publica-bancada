"""Seal preparation-only artifacts and append central memories with byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
CENTRAL=Path(r'C:\IALD\Central de Patentes')
REQUEST='f132a1d5-7477-405d-963b-b1659db63328'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
 p=HERE/name;b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();t=p.with_name(p.name+'.new')
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)
def text_new(name,text):
 p=HERE/name;t=p.with_name(p.name+'.new');b=text.encode()
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)

for item in json.loads((HERE/'SOURCES.json').read_text())['files']:
 p=Path(item['path']);assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],str(p)
validation=json.loads((HERE/'VALIDACAO_PREPARACAO.json').read_text())
assert validation['status']=='PASS' and validation['science_runs']==0
assert validation['engine_sha256']==sha(HERE/'background_controls.py')
assert validation['protocol_sha256']==sha(HERE/'PROTOCOL.json')
body=f'''## 06/10/2026 — F9: preparação do motor de fundo e prior integral

[INPUT] Unidade delegada `{REQUEST}`: preparar qualificação cosmológica somente teórica, sem rodar ciência, abrir composto observado, rede/Work/modelos ou reexecutar E45/PSD/projeto linear/nuisance. Pasta `{HERE}`.

[REAL — documental/estrutural] NPZ histórico conferido em bytes e eixos: tabela bruta11×21×21, suporte útil H0[60,76], wb[.02025,.02475], wc[.102,.138]. Prior candidato comum H0[50,90], wb[.015,.03], wc[.08,.18], normalização3/50, densidade50/3. Suporte útil ocupa4,32% do volume do prior (95,68% sem cobertura); não é massa posterior. Falha de tabela/solver não vira likelihood zero nem prior truncado.

[REAL — metadados] WSL /opt/lal_env: CAMB2.0.4, NumPy2.5.3, SciPy1.18.1, arquivos/binário do pacote com hashes lidos. CAMB não importado. BBN PRIMAT2024 tem domínio de parâmetros que cobre o prior. Python Windows atual sem as bibliotecas; venv antigo ringdown sem CAMB. Retratos anteriores não substituem esta consulta.

[INPUT/OPEN — candidato explícito] FLRW plano Λ, w=−1, TCMB2.7255, mnu.06 em uma espécie, N_eff3.046/referência3.044, BBN PRIMAT2024 e RECFAST planck. Configuração proposta, não ratificada nem demonstrada idêntica à tabela histórica/compressão CMB. Toda previsão por uma instância CAMB: H/DM/DH/DV, rstarCMB e rdragBAO distintos; E(1089.95) da lei e E(zstarCAMB) separados. A receita histórica de E tratava neutrino por aproximação; magnitude da diferença não medida. H5 candidato só rdBAO livre130..160, CMB padrão, não EDE.

[REAL — preparação; OPEN — numerics] Contrato e código para5pontos teóricos×2precisões, máximo10solves futuros, sem repetição automática. Nove controles estruturais passaram, zero cosmologia. Recomendação CAMB direto no piloto; tabela ampliada na mesma resolução teria76.797nós com padding, custo ainda não medido. Cinco campos sozinhos não cobrem H(z)/E/distâncias consistentes. Nem os futuros cinco pontos certificam precisão de todo prior ou evidência.

[ENTREGA] `PARECER_MOTOR_DE_FUNDO.md`, `PROTOCOL.json`, `background_controls.py`, `VALIDACAO_PREPARACAO.json`, metadados e `MANIFESTO_ENTREGA.json`. Código SHA256 {sha(HERE/'background_controls.py')}; protocolo SHA256 {sha(HERE/'PROTOCOL.json')}. ROOT avalia antes de executar teoria. Nenhum centro observado, fit, χ², evidência, sigma, kernel, gate ou original alterado. Não duplicar esta unidade.
'''
text_new('MEMORIA_DA_UNIDADE.md','# Memória da unidade — append-only\n\n'+body)
helper=CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL/record_universe_delivery.py'
spec=importlib.util.spec_from_file_location('safe_memory_append',helper);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
paths=[CENTRAL/'memory'/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
paths += [CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL'/n for n in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md')]
marker='F9_BACKGROUND_PREPARATION_'+REQUEST
for p in paths:mod.append(p,body,marker)
new('MEMORY_RECEIPT.json',{'marker':marker,'updated':[str(p) for p in paths],'method':'byte backup immediately before append; CAS and temporary atomic replacement','own_memory':str(HERE/'MEMORIA_DA_UNIDADE.md')})
files=[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.iterdir()) if p.is_file() and '.bak_' not in p.name and '.new' not in p.name and p.name not in ('MANIFESTO_ENTREGA.json','FINAL_CHECK.json','RECIBO_MAPA.json')]
new('MANIFESTO_ENTREGA.json',{'request_id':REQUEST,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_VALIDATED_STRUCTURALLY_NOT_RUN','solver_calls':0,'observed_inputs':False,'files':files})
print(json.dumps({'files':len(files),'manifest_sha256':sha(HERE/'MANIFESTO_ENTREGA.json'),'report_sha256':sha(HERE/'PARECER_MOTOR_DE_FUNDO.md'),'protocol_sha256':sha(HERE/'PROTOCOL.json'),'engine_sha256':sha(HERE/'background_controls.py')}))