"""Record exact local audit and the new provider staging without claiming dispatch."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'kimi_external_first_jet_review/local_audit'
ORCH=H/'orchestration_current_completion'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,raw,existing=False):
    if p.exists():
        assert existing,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert t.read_bytes()==raw and len(raw)>0;t.replace(p)
    assert p.read_bytes()==raw
def put(p,v,existing=False):atomic(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def text(p,t):atomic(p,t.encode('utf-8'))
res=json.loads((D/'results.json').read_bytes());cat=json.loads((ORCH/'prepared_units.json').read_bytes())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
text(D/'DERIVACAO.md',f'''[DERIVED — auditoria algébrica exata; resposta externa parcialmente aceita, Q2 OPEN]

O parecer Kimi foi lido integralmente. Seus40 canais ghost de primeira derivada
coincidem exatamente com G.vertex(BASIS[k])[1][rho] já existente. Portanto não
criamos novo motor para esse conteúdo. A dimensão do primeiro jato é10+40=50.
A montagem localizada posterior já usa esses slots; a extensão proposta responde
a um retrato anterior do motor bilocal, não a uma ausência em todas as rotas.

As listas A/B/M de tensores têm postos3/7/6; com simetria algébrica adicional de
troca de pares,5. Enumeramos todas as partições de índices livres em pares delta
e singles r (4 padrões de posto3,10 de posto4), simetrizamos e verificamos
SIMBOLICAMENTE cada identidade de expansão em todos os componentes. A solução
numérica exata num ponto fornece coeficientes candidatos; a igualdade polinomial
posterior é que comprova o span. O posto nesse ponto comprova independência;
rotação e escala estendem a independência aos r!=0 para coeficientes radiais.
O alcance é o ansatz construído de delta/r. Não invocamos literatura não lida
como prova de cobertura de todo tensor admissível. Auto-adjunção formal de um
operador diferencial não substitui conferir a simetria algébrica de pares.

Correções ao lado do parecer recebido:
1. G.vertex(T10) levanta IndexError: a API pede16 entradas da matriz4x4.
   LABELS é a parametrização de10 componentes, BASIS efetua a expansão correta.
2. Controle C3 do parecer é falso: para val(T01)=1, esquerda1, direita2.
   Dividir o teste em metades e simultaneamente mudar m de2 para1 duplica o peso.
3. Em x=X-Y, derivada emY é partial_Y z=-2x; o sinal positivo do §4.1 é o deX.
4. T_X independe deY em frame fixo. A proibição de qualquer transporte é excessiva:
   um caminho escolhido dá transporte definido; em vizinhança normal convexa,
   pode-se escolher a geodésica única. Mudança de frame é permitida quando o
   tensor dual e as conexões acompanham a transformação. O teste exato mostra
   tr(P^-1 T P P^-1 O P)=tr(TO), mas mudar sóT altera o par por -3t²-12t.
5. Ric=3Kg não fixa o segundo jato de um TESTE h arbitrário: em fundo plano,
   h11=Y0² tem h=Dh=0 na origem e partial00 h11=2. Uma extensão especial do teste
   deve ser declarada; não se transfere a equação do fundo ao teste.

O parecer distingue declaração e execução, o que foi preservado. Foram
{res['checks']} verificações CAS exatas, rc0, CPU{res['cpu_seconds']}s.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/audit_kimi_external_first_jet.py.
Nenhuma alteração dos engines, nenhum ajuste de coeficientes, nenhum gate movido.
Não calcula Q2, termos suaves, curvatura completa nem extensão lorentziana.
O consumo desse Kimi já estava no LEDGER: não registramos outra chamada.

Abertura sha256: {opening}.
''')
text(OUT/'ENTREGA_016_A7b_auditoria_Kimi_primeiro_jato.md',f'''[DERIVED — auditoria local; Q2 OPEN]

Aceitos os40 canais derivativos já disponíveis e o span simbólico das bases
3/7/6 (5 com troca de pares). Não foi necessário criar novo motor.
Recusados o controle de multiplicidade C3 (1 contra2), a chamadaT10 na API16,
o sinal de derivadaY e a extensão indiscriminada de condições do fundo ao teste.
Mudanças de frame exigem transformar também o dual; transporte não é proibido
por si só. {res['checks']} verificações exatas, rc0, CPU{res['cpu_seconds']}s.

Prova, controles e artefatos: {D/'DERIVACAO.md'} e manifest.json.
Resposta externa preservada; uso já contabilizado, nenhuma nova chamada na auditoria.
Não altera um.py, kernel ou gate. Próximo: correntes mista b-h e ghost e pesos.
Abertura sha256: {opening}.
''')
text(OUT/'ENTREGA_016_MEDIDA_Kimi_primeiro_jato_controles.md',f'''[DERIVED — correções mensuradas de especificação externa]

Tentativa: conferir contra motor e CAS o parecer bilocal de primeiro jato do Kimi.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/audit_kimi_external_first_jet.py.
rc0. Evidência results.json: {D/'results.json'}, sha256 {sha(D/'results.json')}.
128checks; CPU{res['cpu_seconds']}s. C3 dá1 contra2 e vertex(T10) levantaIndexError.
Y tem sinal oposto aX; segundo jato externo não decorre de Ric do fundo.
Os40 canais e as bases passaram. Sem chamada externa nova, sem custo novo
de fornecedor nesta auditoria; assinatura antiga não tratada como custo zero.
Próximo ramo da mesma A7b: inserções das correntes localizadas e pesos de Wick.
Abertura sha256: {opening}.
''')
text(ORCH/'DISTRIBUICAO.md',f'''[INPUT + REAL — tarefas preparadas, rotas conferidas; execução não presumida]

Pedido do operador: distribuir mais tarefas, principalmente ao Kimi.
Três unidades novas e independentes dentro de A7.b:
- Kimi: inserção da corrente mista b-h, incluindo normalização do propagador.
- Kimi: pesos combinatórios e sinais da Ward a partir da ação BV graduada.
- MiMo: duas contrações dirigidas da corrente de três campos ghost.

UUIDs, hashes, fontes e prévias estão em prepared_units.json/manifest.json.
A coordenação única recebeu o catálogo pela ferramenta oficial. Os recibos
de aceitação/admissão/execução devem ser conferidos separadamente: a preparação
fez ZERO chamadas a executores. Cinco admissões e uma execução por provedor
permanecem; FIFO interno não se altera. Nova revisão não repete4d terminal.
DeepSeek70e9 já autorizado permanece candidato para a terceira via disponível.
Bancada faz integração e CAS; saídas de modelos permanecem DECLARADO até revisão.
Abertura sha256: {opening}.
''')
arts=[Path(__file__),D/'DERIVACAO.md',D/'manifest.json',D/'results.json',
    OUT/'ENTREGA_016_A7b_auditoria_Kimi_primeiro_jato.md',
    OUT/'ENTREGA_016_MEDIDA_Kimi_primeiro_jato_controles.md']
put(D/'delivery_manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
    checks=res['checks'],cpu_seconds=res['cpu_seconds'],rc=0,gate_changed=False,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in arts]))
ledger=OUT/'LEDGER_016.jsonl'
events=[dict(at=now.isoformat(),event='KIMI_FIRST_JET_LOCAL_AUDIT',target='A7.b',
    checks=res['checks'],cpu_seconds=res['cpu_seconds'],rc=0,
    manifest_sha256=sha(D/'delivery_manifest.json'),remote_call=False),
    dict(at=now.isoformat(),event='CURRENT_COMPLETION_THREE_UNITS_PREPARED',target='A7.b',
    request_ids=[u['request_id'] for u in cat],catalog_sha256=sha(ORCH/'prepared_units.json'),
    executor_calls=0,status='SENT_TO_COORDINATOR_FOR_STAGING')]
atomic(ledger,ledger.read_bytes()+b''.join((json.dumps(e,ensure_ascii=False)+'\n').encode('utf-8') for e in events),True)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
elapsed=(now-datetime.fromisoformat('2026-09-25T13:43:15.684781+00:00')).total_seconds()/3600
atomic(progress,progress.read_bytes()+f'\r\n- {now.isoformat()} A7.b PROGRESS/MEDIDA: Kimi primeiro jato128checks CPU{res["cpu_seconds"]}s; bancada desde recibo anterior{elapsed:.6f}h; três unidades2Kimi+1MiMo preparadas; zero chamadas externas novas nesta preparação/auditoria; Q2 OPEN.\r\n'.encode('utf-8'),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now.isoformat(),completed_this_turn=['Kimi external-first-jet audit128checks; accepted40W1 and symbolic3/7/6/5basis; correctedC3/API/Ysign/frame/secondjet','Prepared2Kimi+1MiMo current-diagram units; awaiting coordinator staging receipt'],
    pending_scientific_review=None,next=[
    'Obtain current_completion staging receipt; no duplicate provider transitions',
    'Contract Jgf mixed b-h and directed ghost currents; derive diagram weights',
    'A7b deadline20:32UTC; curvature,smooth,tadpole,higher arities remain',
    'Continue A7c/d,A8,ORDEM015PartB and final full audit'],
    pending_orchestration='Kimi aea running;3Kimi waiting;MiMo934328 admitted awaiting corrected parser/new audited process;MiMo4d failed terminal;DeepSeek70e9 staging',
    kimi_external_first_jet_audit_manifest=str(D/'delivery_manifest.json'),
    current_completion_orchestration_catalog=str(ORCH/'prepared_units.json'))
put(p,v,True)
print(json.dumps(dict(manifest=str(D/'delivery_manifest.json'),catalog=str(ORCH/'prepared_units.json'),
    checks=res['checks'],opening_sha256=opening,gate_changed=False)))
