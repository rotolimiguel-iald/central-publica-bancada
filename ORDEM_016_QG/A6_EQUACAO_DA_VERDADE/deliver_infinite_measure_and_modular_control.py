from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
B=HERE/'B_fechamentos'
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode('utf-8') if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
spec=importlib.util.spec_from_file_location('audit',ROOT/'A0/auditar_axiomas.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
finals=[]
for branch,file,label in [('B1d_control','InfiniteLimitUniformControl_v2.lean','infinite_uniform_control_02'),
                         ('B8','ModularGeneratorControl.lean','modular_generator_01')]:
    p=B/file;log=B/(label+'.log');receipt=json.loads((B/(label+'.json')).read_bytes())
    assert receipt['rc']==0 and sha(p)==receipt['source_sha256'] and sha(log)==receipt['log_sha256']
    a=audit.audita(str(p),str(log));assert a['auditoria']=='PASSA'
    save(B/(label+'_audit.json'),a)
    finals.append(dict(branch=branch,source=str(p),source_sha256=sha(p),receipt=receipt,audit=a))
cfc=KERNEL/'.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Continuity.lean'
lines=cfc.read_text(encoding='utf-8').splitlines()
start=next(i for i,l in enumerate(lines,1) if l.startswith('theorem tendsto_cfc_fun '))
assert 'TendstoUniformlyOn' in '\n'.join(lines[start-1:start+5])
equi=KERNEL/'.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Equicontinuity.lean'
el=equi.read_text(encoding='utf-8').splitlines()
estart=next(i for i,l in enumerate(el,1) if l.startswith('theorem EquicontinuousAt.tendsto_of_mem_closure '))
attempts=[json.loads((B/(l+'.json')).read_bytes()) for l in
          ['infinite_uniform_control_01','infinite_uniform_control_02','modular_generator_01']]
opening_sha=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
now=datetime.now(timezone.utc)
m=dict(status='B1d_MEDIDA_B8_PAGO',at=now.isoformat(),opening_sha256=opening_sha,
       finals=finals,attempts=attempts,
       cfc_api=dict(path=str(cfc),sha256=sha(cfc),first_line=start,last_line=start+5,
                    excerpt='\n'.join(lines[start-1:start+5])),
       dense_api=dict(path=str(equi),sha256=sha(equi),first_line=estart,last_line=estart+5,
                      excerpt='\n'.join(el[estart-1:estart+5])),
       wall_seconds=sum(r['wall_seconds'] for r in attempts),
       cpu_seconds=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts),
       gap_statement='bounded_positive_strong_limit: for every bounded self-adjoint nonnegative H on a complete Hilbert space, FlowTendsToFamily (fun s x => T H s x) (reading H)',
       strong_limit_proved=False,uniform_route_refuted_on_interval=True,
       actual_l2_diagonal_operator_constructed=False,
       kernel_written=False,gate_changed=False)
save(B/'infinite_measure_and_modular_manifest.json',m)
text=f'''[REAL — controle de uniformidade provado; OPEN — limite forte geral ainda não formalizado]

# A6.B1d — MEDIDA da rota por cálculo funcional

Abertura do operador, SHA256: `{opening_sha}`.

A API `tendsto_cfc_fun`, em `{cfc.name}`:{start}, exige **TendstoUniformlyOn** no espectro; não recebe convergência pontual. A leitura do enunciado e a hipótese estão transcritas e custodiadas no manifesto.

Compilados e auditados três teoremas: para λ≥0, exp(−sλ) converge pontualmente ao indicador de λ=0; para cada s≥0, λ=1/(s+1) pertence a (0,1] e o erro é maior que exp(−1); logo a tolerância uniforme exp(−1) não pode ser atingida nesse intervalo. O primeiro probe falhou por composição de filtros e orientação de uma identidade de fração; a segunda versão compilou rc0, somente trio. Fontes/logs das duas tentativas preservados.

**Alcance:** isso impede a aplicação geral direta daquela API ao limite espectral descontínuo. Não refuta a convergência forte e não constrói o operador diagonal em ℓ²; o controle formal atual é escalar. A propriedade operatorial exigida continua NÃO PAGA nesta rodada:

`bounded_positive_strong_limit`: H limitado, auto-adjunto e não negativo em Hilbert completo ⇒ T_s x→P_ker(H)x para cada x, sem hipótese de dimensão finita ou gap.

Rota analítica alternativa identificada: construir estimativa para exp(−sH)H, contração uniforme e densidade de ker(H)+ran(H), e usar `EquicontinuousAt.tendsto_of_mem_closure` ({equi.name}:{estart}). Outra rota é representar a norma residual por uma medida espectral e aplicar convergência dominada. Esses passos não foram compilados aqui. Não substituí a conclusão por um novo axioma; a recíproca infinita existente continua condicionada a `FlowTendsToFamily`, como prevê a receita. Ausência de gap não autoriza limite em norma.

MEDIDA delimita a formalização atual, sem declarar parede física. O controle da API foi pago; a passagem forte geral permanece aberta. Revisão Kimi B1d já estava preparada, sem nova chamada. Próximo ramo da árvore: B8 e controles C. Teto de duas horas não foi esgotado; não se alega que seja impossível completar a formalização.

Manifesto: `{B/'infinite_measure_and_modular_manifest.json'}`. Duas compilações B1d, tempo de máquina {sum(r['wall_seconds'] for r in attempts[:2]):.6f}s; comandos, rc, hashes e avisos no manifesto. Não move gate.
'''
save(OUT/'ENTREGA_016_MEDIDA_A6_B1d_limite_forte.md',text)
text=f'''[REAL — seis teoremas compilados e auditados sobre o gerador modular finito]

# A6.B8 — modo zero não é operador zero

Abertura do operador, SHA256: `{opening_sha}`.

PAGO no escopo finito: para ρ positiva definida, `modularGen ρ y=0 ↔ Commute ρ y`. A direção de ida reutiliza `exp_logRho`, já canônico: comutar com logρ implica comutar com exp(logρ)=ρ. A volta usa o cálculo funcional já existente.

O exemplo construído é ρ=diag(1/3,2/3): positividade definida e traço 1 foram provados. A unidade matricial E₀₁ não comuta com ρ, portanto o gerador não é nulo nela nem como função. No controle complementar, ρ=cI tem gerador nulo em todo argumento. Não houve necessidade de introduzir um novo cálculo matricial explícito do logaritmo.

Seis theorem/lemma novos, todos impressos e auditados no trio; primeira compilação rc0. Tempo de máquina {attempts[2]['wall_seconds']:.6f}s. Dois avisos de argumentos simp redundantes; sem erro e sem escrita no kernel. Não identificar o aniquilamento de Ω pelo gerador com a nulidade do operador inteiro. A semântica física de ψ permanece no escopo da ordem; este é um controle matemático.

Fonte: `{B/'ModularGeneratorControl.lean'}`.
Manifesto: `{B/'infinite_measure_and_modular_manifest.json'}`.
Próximo: C1/C2. Monólito ainda pendente; nenhum um.py ou gate alterado.
'''
save(OUT/'ENTREGA_016_A6_B8_gerador_modular.md',text)
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();marker='A6_B1D_MEASURE_B8_CONTROL_20260924'
if marker.encode() not in old:
    e=dict(event=marker,at=now.isoformat(),opening_sha256=opening_sha,
       manifest=str(B/'infinite_measure_and_modular_manifest.json'),
       manifest_sha256=sha(B/'infinite_measure_and_modular_manifest.json'),
       wall_seconds=m['wall_seconds'],cpu_seconds=m['cpu_seconds'],external_execution=False)
    save(ledger,old+json.dumps(e,ensure_ascii=False).encode()+b'\n')
progress=OUT/'ENTREGA_016_PROGRESSO.md';old=progress.read_bytes()
if marker.encode() not in old:
    line=(f'\n- {now.isoformat()} — A6.B1d MEDIDA (forte geral OPEN; 3 controles escalares auditados); '
       f'B8 PAGO,6 teoremas sobre modularGen. Máquina {m["wall_seconds"]/3600:.6f}h parede/'
       f'{m["cpu_seconds"]/3600:.6f}h CPU; bancada não exclusiva. Abertura {opening_sha}. '
       f'Nenhuma chamada externa nova; próximo C1/C2. Não move gate. [{marker}]\n')
    save(progress,old+line.encode())
print(json.dumps(dict(status=m['status'],new_theorems=9,wall_seconds=m['wall_seconds'],audit='PASSA')))
