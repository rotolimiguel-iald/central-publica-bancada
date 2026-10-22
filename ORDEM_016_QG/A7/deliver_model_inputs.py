from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[1]
OUT = CHAT / 'TUNEL/DO_CHATGPT'
DEST = HERE / 'model_inputs'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
    raw = value if isinstance(value, bytes) else (
        value.encode('utf-8') if isinstance(value, str)
        else json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))
    if p.exists():
        old = p.read_bytes()
        if old == raw:
            return
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(p)

result = json.loads((DEST/'results.json').read_bytes())
assert result['status'] == 'PASS_INPUT_CHECKS_ONLY'
assert all(row['ok'] for row in result['checks'])
assert all(row['detected'] for row in result['negative_controls'])
assert result['source_sha256'] == sha(HERE/'model_input_checks.py')
assert result['plan_sha256'] == sha(DEST/'PRE_REGISTER.json')
plan = json.loads((DEST/'PRE_REGISTER.json').read_bytes())
for path,pin in plan['sources'].items():
    assert sha(Path(path)) == pin
opening = sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
now = datetime.now(timezone.utc).isoformat()

note = r'''[DERIVED — especialização algébrica; REAL — CAS exato dos operadores de entrada]

# A7.b — modelo mínimo e dados livres conferidos

## 1. O modelo fixado pela087

Usamos um aberto Lorentziano orientado e globalmente hiperbólico de um espaço-forma4D.
A convenção desta conta é R_abcd=K(g_ac g_bd−g_ad g_bc), K>0; portanto Ric=3K g,
R=12K. κ é real não nulo. A ação restrita é S_EH=−(2κ)⁻¹∫μ_g(R−2Λ).
O requisito on-shell fixa Λ=3K: G+Λg=(Λ−3K)g. Isso é condição do modelo de teste,
não identificação de Λ com um dado observacional ou com a Λ=3/4 do outro fundo.

O setor087 projeta sigma constante ao complexo métrico mínimo. A restrição clássica
φ(x)=φ0 dá ∂φ=0, T_sigma=0 e equação sigma satisfeita para qualquer métrica. Ela é
preservada por difeomorfismos, sφ=c·∂φ=0. Portanto o setor restrito é consistente
classicamente. Não se conclui equivalência com integrar os campos sigma no funcional
quântico da teoria completa.

Um fundo φ0 constante, SEM a projeção, admite ξ em T_φ0 S³, com três componentes.
Em coordenadas normais do alvo, a parte quadrática é

    S_sigma,2 = (c_m/2)∫μ_g g^{μν} δ_ij ∂μ ξ^i ∂ν ξ^j.

O CAS confere essa Hessiana numa carta explícita (sqrt(1−t²|ξ|²),tξ), que tem a mesma
derivada tangente e Hessiana de ação on-shell da carta exponencial nessa ordem. Não
se identifica essa carta com Exp em ordens superiores. A Hessiana temporal é c_m I3.
Assim, manter o fundo constante não apaga três propagadores. Um determinante de
matéria eventualmente obtido integrando-os não é, em geral, uma constante métrica;
essa integração não foi feita aqui.

## 2. Hessiana métrica e ghosts

Seja I_tr h=h−g tr(h)/2; I_tr²=id em4D. De Donder Cν(h)=∇μ(I_tr h)μν.
A fonte066 dá H_gf=(2κ)⁻¹[−□I_tr h/2+L_R h+Λh], com C*=−D,
ell=1/(2κ), e H_gf=H+ell C*C. Nas convenções acima,

    R_μρνσ h^{ρσ}=K(g_μν tr h−h_μν),
    L_R h=−2K h+(K/2)g tr h,
    B=−I_tr/(4κ),
    P=B⁻¹H_gf: P h=□h−2K h+2K g tr h,
    Q=CK: Qv=□v+3Kv.

Aqui o K da curvatura não é o mapa de gauge K_gauge(v)=L_v g nem o gerador modular.
O CAS calcula o endomorfismo de ordem zero sobre as dez componentes: −2K no setor
sem traço (multiplicidade9), +6K no setor de traço (multiplicidade1). Isto NÃO é o
espectro global da EDP, não escolhe estado e não prova estabilidade/positividade.
Os inversos de H_gf devem conservar B: G_H=G_P B⁻¹.

Em símbolos principais, com p covetor arbitrário, C(K_gauge v)=p²v,
δG_pr(K_gauge v)=0 e o termo de gauge cancela a parte não mínima. O CAS verifica
essas identidades como polinômios, sem impor p²≠0. A Ward diferencial com curvatura
é a identidade escrita da fonte; não foi substituída por essa verificação principal.

Na ordem(c,barc), Hessiana Grassmann e inverso são respectivamente
[[0,−Q],[Q,0]] e [[0,G_Q],[−G_Q,0]]. A multiplicação formal preserva os contatos
QG_Q=G_QQ=id. O teste matricial não constrói G_Q nem uma extensão renormalizada.
Antifields continuam fontes externas sem propagadores; auxiliar b não ganha laços.

## 3. O contrato do cálculo que ainda falta fixar

A7.b exige uma prescrição temporal antes do coeficiente de quebra, não apenas esses
operadores livres. A escolha de referência Hadamard/Wick, extensões às diagonais,
escala e termos locais finitos, junto de T10/T11 e contatos, ainda deve ser registrada.
Somente então se pode extrair a primeira ordem em ħ, ghost1/forma4, e conferir
sa_N+d_H b_N=0 no complexo correspondente. Nenhum coeficiente de anomalia foi
calculado nesta etapa. A existência de H4(s) clássico não fornece tal coeficiente.

[KNOWN — leitura primária delimitada] Hollands, §§3.4–3.6 e Teorema2, fornece exemplos
de extensão analítica e descreve a liberdade por uma hierarquia local D_n; não fixa
uma escolha única para este teste gravitacional. Seu exemplo escalar tem fatores
numéricos suprimidos, portanto não será copiado como coeficiente gravitacional.
Fonte: https://arxiv.org/html/0705.3340v4 (lido24/09/2026).
O HTML de Fröb1803.10235v3 consultado está truncado no início da seção2: os
Teoremas3/6/7 não foram verificados nessa consulta e permanecem remissões das fontes
locais, não uma nova leitura primária completa.

Não houve alteração de um.py/kernel/gate, prova Lean nova ou transporte ao fundo
físico sigma=id. Estes dados preparam a prescrição; não satisfazem sozinhos A7.b.
'''
save(DEST/'DERIVACAO_OPERADORES.md', note)
receipt = dict(status='REAL_LOCAL_INPUT_AUDIT', at=now, opening_sha256=opening,
               command='A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/model_input_checks.py',
               rc=0, rc_evidence='exec_command returned exit_code=0 in this goal turn',
               checks=len(result['checks']),negative_controls=len(result['negative_controls']),
               wall_seconds=result['wall_seconds'],cpu_seconds=result['cpu_seconds'],
               artifacts=[dict(path=str(p),sha256=sha(p)) for p in
                          [HERE/'model_input_checks.py',DEST/'PRE_REGISTER.json',
                           DEST/'results.json',DEST/'DERIVACAO_OPERADORES.md']],
               result_file_is='Structured result written by executed script, not a captured stdout log',
               quantum_anomaly_computed=False,products_prescription_fixed=False,gate_changed=False)
save(DEST/'manifest.json',receipt)
save(OUT/'ENTREGA_016_A7b_entradas_operador.md', f'''[REAL — CAS de entradas; DERIVED — especialização no modelo087]

# A7.b — operadores do modelo truncado conferidos

Abertura SHA256: `{opening}`.

CAS SymPy {result['sympy_version']}, rc0: {receipt['checks']} checks exatos e {receipt['negative_controls']} controles negativos. Máquina: {result['wall_seconds']:.6f}s parede/{result['cpu_seconds']:.6f}s CPU. Não é cálculo de anomalia.

Para R_abcd=K(g_ac g_bd−g_ad g_bc), Ric=3K g e sigma constante projetado087, a condição on-shell exige Λ=3K. Em de Donder, a Hessiana normalizada é P h=□h−2Kh+2Kg tr(h), e Qv=□v+3Kv. O endomorfismo métrico separa nove direções sem traço e uma de traço. Conservar B=−I_tr/(4κ) nos propagadores é obrigatório. Esses autovalores locais não são espectro/estabilidade global.

O confronto de modelos foi explícito: apenas fixar o FUNDO sigma constante mantém três flutuações com termo cinético não nulo. O setor mínimo087 as retira por restrição, operação diferente de integração quântica. Não se usou o extrator do fundo sigma=id para afirmar identidade entre os dois.

Controles recusam Λ incompatível com o fundo, perda do termo de traço, sinal de normalização errado, termo de gauge não cancelado, inverso ghost sem graduação e confusão entre fundo constante e ausência de flutuações. O CAS confere símbolos principais e contrações algébricas; os teoremas de propagação são referências escritas, não verificados numericamente aqui.

Derivação: `{DEST/'DERIVACAO_OPERADORES.md'}`. Manifesto SHA256 `{sha(DEST/'manifest.json')}`; fonte, pré-registro e resultado estruturado pinados nele. Reprodução: executar o script em cópia com diretório model_inputs novo, pois ele recusa sobrescrever resultados.

A7.b permanece EM ANDAMENTO: prescrição completa, coeficiente quântico, Wess–Zumino e admissibilidade do contratermo não foram calculados. As quatro unidades de revisão/preparação aguardam a fila existente. Próximo: fixar extensões e normalizações antes da conta. Não move gate.
''')
marker = 'A7B_METRIC_INPUTS_EXACT_20260924'
ledger = OUT/'LEDGER_016.jsonl'
raw = ledger.read_bytes()
if marker.encode() not in raw:
    event = dict(event=marker,at=now,manifest=str(DEST/'manifest.json'),
                 manifest_sha256=sha(DEST/'manifest.json'),external_execution=False,
                 machine_wall_seconds=result['wall_seconds'],machine_cpu_seconds=result['cpu_seconds'])
    save(ledger,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs = {}
for line in ledger.read_text(encoding='utf-8-sig').splitlines():
    if not line.strip(): continue
    e=json.loads(line)
    cost=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id')or e.get('job_id')or e.get('request_id')or e.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now} — A7.b EM ANDAMENTO: operadores mínimos087 derivados; {receipt["checks"]} checks exatos/{receipt["negative_controls"]} controles; CAS {result["wall_seconds"]/3600:.8f}h parede; sem coeficiente de anomalia. Estimativas externas explícitas US${total}, incompletas. Abertura {opening}. [{marker}]\n'.encode())
save(HERE/'CONTINUIDADE.json',dict(
    status='ACTIVE',previous_goal_turn='PROGRESS',at=now,
    completed_this_turn=['A7b minimum metric operator derivation and exact CAS input audit',
                         'Classical restriction versus quantum scalar retention distinguished'],
    next=['Fix complete temporal-products prescription before anomaly calculation',
          'Consume A7 executor results when coordinator reports completion; preserve IDs'],
    pending_orchestration='Four A7 units staged after A6 reviews; acknowledgment in orchestration/',
    remaining_full_goal=['A7.b/c/d','A8','ORDEM015 Part B','Final full requirement audit and reports'],
    quantum_anomaly_computed=False,originals_modified=False,gate_changed=False))
print(json.dumps(dict(status=receipt['status'],checks=receipt['checks'],controls=receipt['negative_controls'],
                      manifest_sha256=sha(DEST/'manifest.json')),ensure_ascii=False))
