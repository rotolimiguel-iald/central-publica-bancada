"""Write explicit physical scope of R-MOD/R-PROP; no new physical identification."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    if p.exists():raise FileExistsError(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Write mismatch')
    t.replace(p)
old=ROOT/'C2_MAPEAMENTO_ANALITICO.md';c1=ROOT/'C1_ADENDO_CORRECOES_013BIS_v3.md'
reading=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_013_INSUMOS/LEITURA_03_NUMEROS.md'
opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
doc='''[DERIVED condicional; CONJECTURE na identificação física] {utc}; adendo a C2_MAPEAMENTO_ANALITICO.md, SHA256 `{old}`.

# C3.2, R-MOD e R-PROP: derivação condicional e paredes

## R-MOD — seis passos com estatuto

1. **[KNOWN / OPEN] Região e estado.** A leitura de Bisognano–Wichmann está limitada às seções e hipóteses registradas no adendo C1: cunha de Minkowski e vácuo não constituem Kerr térmico global. Kay–Wald/Sewell não tiveram integrais obtidos; os HTTP 403/redirecionamentos são paredes de acesso. Para spin não nulo, a região corrotante restrita perde a descrição de todo o exterior; o ansatz de Gibbs com ν≤0 perde normalização; Unruh perde o KMS global usado na conversão. PAGO como identificação das alternativas/parede; NÃO PAGO como construção de um estado físico global.

2. **[DERIVED sob CONJECTURE] Tempo.** Para um oscilador corrotante escolhido, ν=ω_R−mΩ_H>0, K=(2π/κ)νN+log Z e s=κt/(2π). Se, adicionalmente, o gerador em s for o duplo comutador −β[K,[K,ρ]]/2, a coerência adjacente tem taxa em segundos Γ=(κ/2π)(β/2)(2πν/κ)²=πβν²/κ. κ e ν estão em s⁻¹; Γ também. A constante log Z cancela nesse duplo comutador. **Esse é o modelo quadrático assumido pela R-MOD; não é derivação da lei L=√β√K por mera troca de nomes.** Para o salto raiz, o gap de raízes seria diferente e dependeria dos níveis/fundo. O K deste oscilador térmico não se identifica automaticamente com o superoperador bilateral −logΔ do kernel. PAGO como álgebra condicional; NÃO PAGO como identificação microscópica do horizonte/QNM ou escolha de relógio.

3. **[DERIVED] Domínio.** O requisito ν>0 permite normalizar a soma bosônica Σ exp[−(2π/κ)νn]. Para ν=0 os termos são constantes; para ν<0 crescem. O ramo numérico recusa esse domínio. Não inferir existência de estado regional completo a partir da positividade de um único modo. PAGO como domínio do ansatz, NÃO PAGO como teorema global de Kerr.

4. **[INPUT / OPEN] Não universalidade.** O mesmo período KMS aplicado a laboratório leva à alternativa Unruh-g excluída pela v369 no escopo testado. A regra que separaria laboratório e horizonte depende da partição física. A bancada não preencheu a fala do operador. PAGO como parede condicional; NÃO PAGO como regra derivada de não universalidade.

5. **[REAL numérico] Coincidência e discriminante.** A tabela independente de sete spins no C1 mostra que R-MOD e R-RAIZ-0 coincidem aproximadamente perto de 0,68, mas divergem em spin. A coluna BCW mede o erro da aproximação; o ramo corrotante usa QNM exato. PAGO como controle numérico; nenhuma identidade estrutural entre as leituras.

6. **[KNOWN / DERIVED / CONJECTURE / OPEN] Proveniência.** As seções BW foram consultadas; Kay–Wald/Sewell permanecem com acesso incompleto. A álgebra dimensional foi conferida. Estado físico, subsistema, tempo modular/Killing e duplo comutador aplicado ao QNM são hipóteses explícitas. R-MOD é **CONJECTURE — management hypothesis, not TGL canon**. PAGO como discriminação de estatutos; fechamento físico NÃO PAGO.

## R-PROP — confronto explícito com LEITURA_03

LEITURA_03_NUMEROS.md, SHA256 `{reading}`, chama a aplicação do relógio GM_f/c³ à viagem de “erro de tipo”, porque M_f pertence à fonte. C2 §5 discordou sem apontar a passagem; esta nota explicita a diferença.

**[DERIVED] Não existe erro dimensional:** GM_f/c³ é tempo, Γ=βτ★ω²/2 é taxa, ΓD/c é adimensional, mesmo quando τ★ depende de M_f. Uma lei de propagação pode ser postulada com parâmetros da fonte; isso não é proibido pela álgebra. **[OPEN / CONJECTURE] Existe uma passagem física não justificada:** o ramo B registrado era dinâmica local do remanescente, não uma memória do emissor carregada por toda a propagação. Reutilizar seu τ★ ao longo do caminho sem declarar esse novo mecanismo seria erro de escopo/identificação. O grande expoente obtido assim não falsifica o ramo B local. A crítica da LEITURA_03 é aceita nesse sentido físico restrito, não como impossibilidade matemática universal. Nenhum dos textos fornece a ponte não local.

**[DERIVED condicional]** Para um relógio universal local constante na fonte e ω(z)=ω_obs(1+z), dt=−dz/[(1+z)H(z)], a integral da taxa é Ξ=(βτ★ω_obs²/2)∫₀ᶻ(1+z′)/H(z′)dz′. H(z) deve ser declarado; D_L/c não é o tempo de voo cosmológico exato. A expansão aqui usa a cosmologia indicada no módulo, não uma medição de Ξ. O expoente atenua coerência espectral de ensemble sob a hipótese de ruído local independente; ele não é automaticamente um novo amortecimento no intervalo temporal do ringdown. Amplitude livre absorve atenuação constante; dependência espectral, correlações espaciais, detector/referência e realização exigem uma função de transferência própria. PAGO como conta dimensional/integral e comparação de escopos; NÃO PAGO como observável estocástico calibrado de propagação. A linha numérica sub-resolução não resolve essa ponte.

## Template e evidências já existentes

tgl_ringdown_template.py documenta h₊∝cos(ω(t−t_start)+φ) e h×∝sin(ω(t−t_start)+φ), com fatores de inclinação 220; h₊−ih× tem fase exp(−iωt) face-on. A fase é do modo, não orbital. As saídas plus/cross são compatíveis como arrays com interface temporal Bilby; isso não demonstra equivalência com sua likelihood. PyCBC requer TimeSeries com delta_t/epoch. O template não é modificação completa de IMR nem substituto de pyRing. Modos superiores exigem fatores angulares explícitos. C3_README_013BIS.md e bis/C3_C6_TIMING_013BIS.json dão a origem GPS e os cortes realizados, sem reler strain. C2_ADENDO_OBSERVAVEL_v2.md contém os controles de trajetórias condicionais; não transforma realization em previsão universal do módulo.

Nenhuma nova PE, execução Lean ou escolha física. Reprodução documental: python -B refeito/record_c3_physical_walls_013bis.py numa cópia isolada (recusa sobrescrita). Axiomas: N/A — sem Lean. Abertura SHA256 `{opening}`. C1 adendo SHA256 `{c1}`. Os hashes das demais evidências estão em bis/C3_PHYSICAL_WALLS_SOURCES.json.
'''.format(utc=datetime.now(timezone.utc).isoformat(),old=sha(old),reading=sha(reading),opening=sha(opening),c1=sha(c1))
names=['tgl_ringdown_template.py','tgl_ringdown_prediction.py','C2_MAPEAMENTO_ANALITICO.md','C1_ADENDO_CORRECOES_013BIS_v3.md','C3_README_013BIS.md','bis/C3_C6_TIMING_013BIS.json','C2_ADENDO_OBSERVAVEL_v2.md','bis/C1_CLOSING_REVIEW.md','bis/C2_ADVERSARIAL_REVIEW.md']
new(ROOT/'bis/C3_PHYSICAL_WALLS_SOURCES.json',(json.dumps(dict(code_sha256=sha(Path(__file__)),sources={n:sha(ROOT/n) for n in names},reading03_sha256=sha(reading),opening_sha256=sha(opening)),indent=2)+'\n').encode())
new(ROOT/'C3_ADENDO_RMOD_RPROP_013BIS.md',doc.encode())
print(sha(ROOT/'C3_ADENDO_RMOD_RPROP_013BIS.md'))
