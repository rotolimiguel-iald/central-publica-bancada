"""Prepare a distinct loop localization review, with equations only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import uuid

H = Path(__file__).resolve().parent
D = H / 'orchestration_loop_localization'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
D.mkdir(exist_ok=False)

def put(path, obj):
    assert not path.exists()
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    tmp.replace(path)

prompt = r'''ORDEM_016, A7.b: revisão independente da localização de BOLHAS,
distinta da unidade da fonte A.c+B.Dc. Memória científica comum obrigatória.
Não há anexos de código. Resposta DECLARADO até conferência local.

PERGUNTA ÚNICA: qual é a identidade completa, incluindo contatos, para
integrar por partes os dois extremos de uma bolha com jatos externos de
primeira ordem, quando cada extremo tem um cutoff independente?

Trabalhe inicialmente no espaço plano euclidiano de dimensão quatro, sem
inferir continuação lorentziana. Escreva D_X^0=D_Y^0=id, D_X^i=partial_Xi,
D_Y^j=partial_Yj. Índices mu,nu percorrem {0,1,2,3,4}, com os quatro
índices não zero denotando direções espaciais. Os índices tensoriais são
suprimidos, mas a simetria h_ab=h_ba deve ser preservada em uma aplicação.
U^{mu nu}(X,Y) é o kernel não reduzido de uma bolha. Antes da extensão:
 I=integral dX dY chiX(X) chiY(Y)
            (D_X^mu h(X)) U^{mu nu}(X,Y) D_Y^nu(Gc)(Y),
onde (Gc)_ab=partial_Ya c_b+partial_Yb c_a.
Cada U representa uma contração já normalizada. Não invente fatores de
simetria, nem suponha que U seja um propagador único.
R é extensão linear que comuta com multiplicação suave;
C_D(f)=R(Df)-D R(f). Adjunção sobre distribuições estendidas é EXATA.

Para expressar a variação no índice c_b, podem-se usar, para cada jato
externo mu, kernels F0^mu_{ab} e F1^{mu j}_{ab} e multiplicidade
m_ab=1 se a=b,2 caso contrário. O coeficiente após adjunção em Y é
 W_Y^mu=sum_a 2/m_ab [-partial_Ya(chiY R(F0^mu_ab))
             +sum_j partial_Ya partial_Yj(chiY R(F1^{mu j}_ab))].
Depois da adjunção em X o coeficiente de h é
 P=chiX W_Y^0 - sum_i partial_Xi(chiX W_Y^i).
Defina Q=R da expressão inteiramente análoga fora da diagonal, usando F
em lugar de R(F). Derive P-Q em termos de C_partialX, C_partialY e
C_partialYa partialYj. Não comute R com derivadas silenciosamente.

Entregue fórmula que uma bancada possa aplicar diretamente aos kernels
não reduzidos, com todos os termos dchiY,d2chiY,dchiX e cruzados; se uma
forma compacta os inclui implicitamente, expanda um caso para mostrar.
Explique precisamente quais dados são irrecuperáveis se só guardamos
W_Y^mu com chiY=1. Dê um contraexemplo simples a reconstruir a resposta
localizada apenas multiplicando esse W reduzido por chiY.

Controle quantitativo independente: em R4, z=|X-Y|² e f=z^-2, use
R f=FP_a[(1-a)mu_scale^(2a) z^a f], CE=-4pi².
Res(z^(a-n))/CE=-(q²)^(n-2)/[4^(n-1)(n-1)!(n-2)!], n>=2,
x_i multiplica como -partial_qi; q simboliza derivadas de delta.
Escolha F1^{11}=f e demais F zero e compare chiY=1 com cutoff cujo
primeiro jato na diagonal é não nulo. Calcule ao menos um contato de
primeira e de segunda derivada, identificando o sinal X versus Y.

O objetivo é a álgebra de localização que servirá igualmente a bolhas
métricas e ghost, não recalcular seus vértices nem provar cancelamento
entre elas. Curvatura, corrente completa de Einstein-Hilbert e aridade
BRST superior permanecem dados adicionais. Não concluir Q2=0, não
propor novo ramo nem promover identidades formais a confirmação física.
'''
request_id = str(uuid.uuid4())
constraints = dict(mission_id='ORDEM_016', branch_id='A-7.b',
    lemma_id='unreduced_loop_double_cutoff_jet_adjoint_identity',
    role='skeptic', required_provider='mimo', max_calls=1,
    max_cost_usd=None, max_output_tokens=131072)
payload = dict(operation='submit', request_id=request_id,
               prompt=prompt, execution_constraints=constraints)
path = D / 'mimo_loop_localization_submit.json'
put(path, payload)
sha = hashlib.sha256(path.read_bytes()).hexdigest()
put(D / 'origin_receipt.json', dict(at=datetime.now(timezone.utc).isoformat(),
    thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
    request_id=request_id, payload=str(path), payload_sha256=sha,
    status='PREPARED_NOT_SUBMITTED', attachments=[],
    scope='Mathematical loop localization; not blocked DeepSeek code review'))
run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE / 'transport_cli.py')],
    input=json.dumps(dict(operation='preview_execution', prompt=prompt,
                         execution_constraints=constraints), ensure_ascii=False),
    text=True, capture_output=True, encoding='utf-8', cwd=BASE)
result = json.loads(run.stdout)
put(D / 'preview.json', dict(returncode=run.returncode, response=result))
assert run.returncode == 0 and result.get('selected') == 'mimo', result.get('selected')
catalog = [dict(provider='mimo', lemma=constraints['lemma_id'], request_id=request_id,
    payload=str(path), payload_sha256=sha, prompt_chars=len(prompt),
    selected=result['selected'], status='PREPARED_NOT_SUBMITTED',
    after='Existing MiMo f7f59797; single coordinator, no duplicate call')]
put(D / 'prepared_units.json', catalog)
print(json.dumps(catalog, ensure_ascii=False))
