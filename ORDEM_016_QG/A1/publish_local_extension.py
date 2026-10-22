from pathlib import Path
import datetime,hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
stamp=datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.rename(p)
def append(p,b):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+stamp.strftime('%Y%m%d_%H%M%S_%f')),old)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(old+b)
    assert t.read_bytes()==old+b
    t.replace(p)
cases=[('minimal_imports','WindowLemmasVerbatim.lean','window_lemmas_01'),
       ('minimal_imports','WindowCoefficientVerbatim.lean','window_coefficient_01'),
       ('probes','StressTensorDataLocal_v2.lean','local_stress_02')]
entries=[]
args=[]
for folder,name,label in cases:
    droot=root/'A1'/folder
    p=droot/name
    log=droot/(label+'.log')
    rec=droot/(label+'.json')
    d=json.loads(rec.read_text())
    assert d['rc']==0 and not d['newer_kernel_files'] and not d['scan_errors']
    assert d['source_sha256']==sha(p) and d['log_sha256']==sha(log)
    args += [str(p),str(log)]
    entries.append({'source':str(p),'source_sha256':sha(p),'log':str(log),'log_sha256':sha(log),
      'receipt':str(rec),'receipt_sha256':sha(rec),'wall_seconds':d['wall_seconds'],
      'cpu_seconds':d['cpu_user_seconds']+d['cpu_kernel_seconds']})
a=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),*args],capture_output=True)
assert a.returncode==0,a.stdout+a.stderr
create(root/'A1/local_extension_axioms.json',a.stdout)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
data={'utc':stamp.isoformat(),'opening_sha256':opening,'entries':entries,'audit_sha256':sha(root/'A1/local_extension_axioms.json'),
 'scope':'Proposal on expectation-valued tensors; conditional inheritance/rejection; not operator locality',
 'remaining':['A-1.b1 awaiting provider-constrained delegation; no job submitted',
 'A-1.a original aggregate reproduction remains measured memory failure; selected literal chunks recompiled']}
create(root/'A1/local_extension_manifest.json',json.dumps(data,ensure_ascii=False,indent=2).encode())
files='\n'.join(f'- {e["source"]}, SHA256 {e["source_sha256"]}\n  Log {e["log"]}, SHA256 {e["log_sha256"]}\n  Comando/recibo {e["receipt"]}, SHA256 {e["receipt_sha256"]}' for e in entries)
text=f'''[REAL] A-1.c — extensão tipada e rejeição do tensor forjado.

Abertura SHA256: {opening}

[DERIVED — proposta compilada, fora do kernel] StressTensorDataLocal W B estende exatamente StressTensorData W, acrescentando simetria, conservação em teste e covariância sob B:WedgeBoostRep W. Na convenção (+---), exige para todo teste suave compacto f a integrabilidade de cada T_mu,nu * sinal_mu * derivada_mu(f), e a soma das quatro integrais igual a zero. A condição de integrabilidade evita que a integral totalizada esconda divergência. A transformação dos índices covariantes usa o boost inverso e seu transposto.

Preservação: os corpos originais de 22 lemas de janela/controle foram recompilados literalmente em dois recortes, sem substituir suas provas. O primeiro tem 21 declarações; o segundo reutiliza o lema existente de TriadMaster para o coeficiente 8πG. Oito corolários da extensão compilaram: primeira lei, Bekenstein–Hawking, Clausius, coeficiente 8πG, cancelamento de κ, controles afim/exponencial e rejeição do tensor forjado. A aplicação ocorre sobre o MESMO ContratoH3, lendo L.toStressTensorData, sem construir um substituto.

O controle b2 é recusado precisamente por symmetric: o H3 inicial não trivial e a simetria da fonte inicial implicam um ponto admissível onde o tensor forjado não é simétrico. Logo não existe extensão local proposta cuja projeção seja esse tensor. Isto não prova existência do H3 inicial ou da extensão.

[OPEN — alcance] Local no nome segue a ordem; o tipo ainda fala de EXPECTATIVAS. Não constrói distribuição de operadores, afiliação à rede, domínio comum, sesquilinearidade ou microcausalidade. B é índice explícito: numa aplicação física deve ser o boost do mesmo H2; os corolários de janela não usam essa identificação. Conservação/covariância são exigências novas, não derivadas gratuitamente do H3. As paredes H2 não dependem de T; as paredes H3 afim/exponencial foram efetivamente especializadas. Não foi recompilado aqui todo o arquivo agregado de paredes legadas, cuja reprodução A-1.a permanece com MEDIDA de memória.

Auditoria: 30 declarações, trio permitido, zero sorry/axioma novo, rc 0 em todos os três recibos. Fonte v1 e suas evidências preservadas; v2 amplia somente os corolários, não corrige falha. Recursos dos três passes: {sum(e['wall_seconds'] for e in entries):.6f}s parede, {sum(e['cpu_seconds'] for e in entries):.6f}s CPU. B pesada 0h. Nenhuma chamada externa nesta entrega. Comandos integrais e limites de cada passe nos recibos.

{files}

Manifesto: A1/local_extension_manifest.json SHA256 {sha(root/'A1/local_extension_manifest.json')}.
Auditoria: A1/local_extension_axioms.json SHA256 {sha(root/'A1/local_extension_axioms.json')}.

Não move H2/H3/import-H3 ou gate. A adoção do refinamento continua com a gerência. Próximo: finalizar A-1.b1 com a rota orquestrada e consolidar A-1.
'''
create(out/'ENTREGA_016_A1c_extensao_tensor.md',text.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{stamp.isoformat()} | A-1.c | PAGO no escopo de proposta: extensão, herança de janelas/controles H3 e rejeição b2; localidade de operadores OPEN | {sum(e["wall_seconds"] for e in entries)/3600:.9f}h parede; {sum(e["cpu_seconds"] for e in entries)/3600:.9f}h CPU; B pesada 0h; A-1.b1 pendente e A-1.a MEDIDA.\n'.encode())
print(json.dumps({'audited':sum(x['n_declaracoes_auditadas'] for x in json.loads(a.stdout)), 'report_sha256':sha(out/'ENTREGA_016_A1c_extensao_tensor.md')}))
