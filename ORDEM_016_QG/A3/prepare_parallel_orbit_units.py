from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, uuid

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / 'IALD_ORQUESTRACAO_20260923'
STAMP = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')

def save(path, data):
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes() == old
    tmp = path.with_name(path.name + '.tmp_' + STAMP)
    with tmp.open('xb') as f: f.write(raw)
    assert tmp.read_bytes() == raw and len(raw) > 0
    tmp.replace(path)

def source(name):
    p = HERE / name
    raw = p.read_bytes()
    lines = raw.decode('utf-8').splitlines()
    info = dict(path=str(p), sha256=hashlib.sha256(raw).hexdigest(), first_line=1, last_line=len(lines))
    return info, f'FONTE {p.name}; SHA256 {info["sha256"]}; linhas 1-{len(lines)}\n' + '\n'.join(f'{i}: {s}' for i, s in enumerate(lines, 1))

common = '''ORDEM_016, casa Central de Patentes, bancada científica A3. O operador pediu expressamente nesta sessão: "distribua mais tarefas para o Kimi e para o Mimo". Esta é uma unidade NOVA delimitada, não reenvio das unidades A3.d terminadas nem do DeepSeek cancelado. Usar memória científica comum pelo transporte máximo. Uma chamada por unidade; sem fallback ou repetição incerta. Fontes abaixo são arquivos científicos da própria bancada, com hashes calculados agora. Não enviar/solicitar credenciais, acervo jurídico ou outros confidenciais. Não acessar caminhos: os conteúdos necessários estão transcritos.
A sessão Codex escreve/compila localmente; você fornece derivação ou rascunho e declara não ter executado Lean. Não crie outra arquitetura, não renomeie postulados como provas, não mova gate, não escolha horizonte nem massa para o operador. Reaproveite o material. Estatutos DERIVED/OPEN/DECLARADO e hipóteses explícitas. Uma pergunta técnica por unidade.
'''

tasks = [
    ('mimo', 'A3.4', 'product_norm_cocycle_no_eigen', 'draft',
     '''PERGUNTA ÚNICA: qual é a menor extensão demonstrável do argumento já compilado rapidityShift_no_eigen para f em L²(Q×R, ν⊗dξ;E), quando (U_s f)(q,ξ)=C_s(q,ξ)f(q,ξ-s), com C_s isométrico na fibra, e U_s f=c_s f com |c_s|=1, que prova f=0 SEM postular gauge que torne C_s=1?
Entregue prova completa por integrais de norma sobre ladrilhos ou Fubini, cuidando dos quantificadores quase em toda parte (somente s inteiros devem bastar; não interseção não enumerável), mensurabilidade e finitude. Ofereça um rascunho Lean mínimo reutilizando o argumento anexado; API não documentada deve ficar marcada como nome a localizar, nunca fingir que compilou. Não resolva a mudança de medida orbital: ela é unidade local distinta. Nesta tarefa Q=R², ν=Lebesgue; se generalizar, declare sigma-finitude/hipóteses realmente usadas. Para E=C² a norma é a Hilbertiana; não confunda produto com norma sup padrão. Nenhuma construção física de C_s foi fornecida: separar prova normativa condicional de representação de helicidade construída.
Evidência da bancada: VectorRapiditySpectrum.lean, rc0, dois #print axioms no trio padrão. A sua tarefa é a extensão ao produto com cociclo, não refazer o lema de deslocamento puro.
''', ['VectorRapiditySpectrum.lean']),
    ('kimi', 'A3.1', 'skeptic_operator_faithfulness_from_orbit', 'skeptic',
     '''PERGUNTA ÚNICA: as sete declarações anexadas de fidelidade pontual bastam, e sob quais pontes mínimas verificáveis, para provar fidelidade de U(a)f(p)=exp(i<a,p>)f(p) em L² da órbita futura, isto é U(a)=I implica a=0, nos casos m>0, m=0 helicidade0 e m=0 helicidades+1⊕−1?
Faça uma revisão cética da inferência, não repita a prova algébrica já compilada. O problema exato é que os momentos sobre eixos usados na prova têm medida zero: igualdade a.e. do multiplicador não pode ser avaliada neles sem argumento de suporte pleno/continuidade. Construa essa ponte ou dê contraexemplo à formulação insuficiente. Medida pretendida d³p/p0, parametrização p0=sqrt(m²+|p|²), vértice excluído para m=0; norma Hilbertiana no setor duplo. Explique como identidade do operador implica multiplicador=1 a.e. com testes L² de suporte finito e depois igualdade em todo ponto da órbita; explicite sigma-finitude, positividade da densidade e continuidade. Entregue uma sequência mínima de lemas com hipóteses, distinguindo os que já estão anexados dos novos. Não postule a própria fidelidade, nem deduza representação de Lorentz/energia positiva/KMS desse resultado. Não pesquise teorias diferentes. Nomes Mathlib não fornecidos são sugestões não verificadas.
Evidência local: OrbitTranslationFaithfulness_v2.lean compilou rc0 com sete declarações auditadas; o arquivo deliberadamente prova somente fidelidade pontual. A ponte de operador permanece a examinar. Você não executou a compilação.
''', ['OrbitTranslationFaithfulness_v2.lean'])
]

sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
status = runtime.status()
save(HERE / 'parallel_orbit_status.json', status)

for provider, branch, lemma, role, question, names in tasks:
    receipt_path = HERE / f'{provider}_parallel_orbit_receipt.json'
    assert not receipt_path.exists(), 'Existing request: recover rather than duplicate'
    pairs = [source(n) for n in names]
    prompt = common + question + '\n\n' + '\n\n'.join(p[1] for p in pairs)
    assert len(prompt) <= 20000
    rid = str(uuid.uuid4())
    constraints = dict(mission_id='ORDEM_016', branch_id=branch, lemma_id=lemma, role=role, required_provider=provider, max_calls=1)
    if provider == 'mimo': constraints.update(max_cost_usd=None, max_output_tokens=131072)
    receipt = dict(request_id=rid, job_id=None, status='prepared', created_at=datetime.now(timezone.utc).isoformat(), origin_thread='01a070fc-9484-7e13-a654-c6b5f61093a4', origin_house='Central de Patentes', origin_folder=str(HERE.parent), sources=[p[0] for p in pairs], prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), execution_constraints=constraints)
    save(receipt_path, receipt)
    save(BASE / 'state/session_requests' / (rid + '.json'), receipt)
    save(HERE / f'{provider}_parallel_orbit_submit.json', dict(operation='submit', request_id=rid, prompt=prompt, execution_constraints=constraints))
    preview = runtime.preview(prompt, constraints)
    save(HERE / f'{provider}_parallel_orbit_preview.json', preview)
    assert preview.get('selected') == provider, (provider, preview.get('status'))
    print(json.dumps(dict(provider=provider, request_id=rid, selected=preview['selected'], status=preview['status'], prompt_chars=len(prompt)), ensure_ascii=False))
