from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, uuid

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'acceleration_20260924'
DEST.mkdir(exist_ok=True)
stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')

def save(path, obj):
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as out: out.write(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as out: out.write(data)
    assert temp.read_bytes() == data and data
    temp.replace(path)

def excerpt(name):
    path = HERE / name
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    return '\nSOURCE ' + name + '\nsha256=' + hashlib.sha256(raw).hexdigest() + '\n' + '\n'.join(f'{i}: {s}' for i, s in enumerate(lines, 1))

units = [
    ('kimi_energy_skeptic', 'kimi', 'skeptic', 'A-3.b.2',
     'Audite adversarialmente a cadeia de energia positiva analítica já compilada, SEM refazê-la. A pergunta única: a conclusão para todo vetor L2 e todo a no cone futuro realmente segue sem hipótese oculta de primeiro momento finito? Confira sinal (+---), limite na borda, majorante da derivada, medida de densidade e ligação ao coeficiente matricial. Entregue somente falhas concretas com linhas ou parecer de escopo sustentado. Fontes compiladas rc0 com axiomas auditados pelo compilador local; você não tem ferramentas nem pode alegar nova compilação. Não inferir rede AQFT/BW deste resultado.',
     ['PositiveEnergyIntegral_v4.lean', 'OrbitalPositiveEnergy_v3.lean', 'OrbitalStateAnalytic.lean', 'OrbitalPositiveEnergyContract.lean']),
    ('kimi_helicity_construction', 'kimi', 'draft', 'A-3.c.4',
     'Construa a ponte explícita que falta no subalvo de ausência de autovetores para helicidades +1 e -1. Pergunta única: como realizar o cociclo unitário mensurável do boost de cunha no cone sem massa de modo que a ação seja C_s(q,xi) f(q,xi-s), satisfazendo composição e identificada com a representação de helicidade, e não apenas duas cópias escalares? Use a carta p=(r cosh xi,r sinh xi,q0,q1), r=norm q, com d3p/|p|=d2q dxi fora de q=0 nulo. O lema normativo abaixo JÁ está compilado; não o rederive. Entregue seção/trivialização, fórmula ou construção exata, verificação de isometria, mensurabilidade e composição, e separe precisamente o que exige demonstração adicional. Não substitua J modular por conjugação informal, não escolha partição física e não construa Fock (fora da ordem). Não alegue consulta externa/compilação não feita.',
     ['IsometricCocycleSpectrum_v2.lean']),
    ('mimo_null_ergodicity', 'mimo', 'draft', 'A-3.b.5',
     'Resolva a precisão lógica do subalvo de vácuo de uma partícula. Pergunta única: no L2 da órbita positiva de massa m>=0, com U(a)f(p)=exp(i a.p)f(p), o subespaço fixo por U(l n), n=(1,1,0,0), é zero e torna a cláusula isolada null_ergodic vacuamente satisfeita? Separe a inexistência de vácuo normalizado fixo pelos boosts (já compilada abaixo) da implicação forall psi, (forall l,U(l n)psi=psi)->psi pertence a span_C(vac). Derive por frequências contáveis, suporte e conjuntos nulos, incluindo m=0, onde p0-p1=0 apenas no raio de medida nula; não use interseção não enumerável de conjuntos quase certos. Entregue prova exata e roteiro Lean mínimo reutilizando multiplicadores/L2. Não invente vácuo, não acrescente Fock e não afirme compilação própria.',
     ['OrbitalBoostContinuity_v2.lean'])
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
save(DEST / 'runtime_status.json', runtime.status())
summary = []
for slug, provider, role, branch, question, sources in units:
    path = DEST / (slug + '_submit.json')
    if path.exists():
        payload = json.loads(path.read_text(encoding='utf-8'))
    else:
        prompt = ('ORDEM_016. Unidade nova independente; não repete os dois pedidos anteriores em autorização pendente. '
                  'Pedido atual do operador: distribuir mais tarefas, principalmente Kimi. '
                  'Estatutos explícitos; saída é contribuição a conferir localmente, não prova nem alteração de gate. '
                  'Memória científica canônica comum pelo transporte; nenhuma fonte jurídica ou segredo.\n' + question
                  + ''.join(excerpt(name) for name in sources))
        assert len(prompt) < 24000
        constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=slug,
                           role=role, required_provider=provider, max_calls=1)
        if provider == 'mimo': constraints.update(max_cost_usd=None, max_output_tokens=131072)
        payload = dict(operation='submit', request_id=str(uuid.uuid4()), prompt=prompt,
                       execution_constraints=constraints)
        save(path, payload)
        receipt = dict(request_id=payload['request_id'], origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
                       origin_directory=str(HERE), created_at=datetime.now(timezone.utc).isoformat(),
                       provider=provider, branch=branch, status='prepared_not_submitted',
                       prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), sources=sources)
        save(DEST / (slug + '_receipt.json'), receipt)
    preview = runtime.preview(payload['prompt'], payload['execution_constraints'])
    save(DEST / (slug + '_preview.json'), preview)
    assert preview.get('selected') == provider, 'ROTA_NAO_DISPONIVEL: ' + slug
    summary.append(dict(slug=slug, provider=provider, request_id=payload['request_id'],
                        selected=preview.get('selected'), prompt_chars=len(payload['prompt'])))
save(DEST / 'prepared_units.json', summary)
print(json.dumps(summary, ensure_ascii=False))
