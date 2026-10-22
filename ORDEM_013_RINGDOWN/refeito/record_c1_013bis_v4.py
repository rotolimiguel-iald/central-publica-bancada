"""Create corrected C1 artifacts beside immutable v1, with measured controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from c1_evidence_guards_v2 import validate_evidence, require

ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,text):
    if p.exists(): raise FileExistsError(p)
    raw=text.encode('utf-8'); tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f: f.write(raw)
    require(tmp.read_bytes()==raw,'Output bytes differ')
    tmp.replace(p)

def main():
    original=ROOT/'C1_LEITURAS.json'; before=original.read_bytes()
    data=json.loads(before)
    numpath=ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json'; measured=json.loads(numpath.read_bytes())
    refs_path=ROOT/'bis/C1_PRIMARY_RETRIEVALS.json'; refs=json.loads(refs_path.read_bytes())
    core=json.loads((ROOT/'cache/casa/um_absoluto.json').read_bytes())['core']['clock_test_result_v369']
    validated=validate_evidence(ROOT,measured,core)
    for row in refs:
        if row.get('sha256'):
            require(sha(ROOT/row['path'])==row['sha256'],'Primary source changed')
    stamp=datetime.now(timezone.utc).isoformat()
    data.update(status='C1_CORRECTED_CONDITIONAL_READINGS__PRIMARY_KERR_TEXTS_NOT_FULLY_ACCESSED',
                supersedes='C1_LEITURAS_v3.json',supersedes_sha256=sha(ROOT/'C1_LEITURAS_v3.json'),updated_utc=stamp,
                origin_generator_sha256=data.pop('generator_sha256'),
                v4_generator=dict(path=str(Path(__file__)),sha256=sha(Path(__file__))),
                evidence_validator=dict(path='refeito/c1_evidence_guards_v2.py',sha256=sha(ROOT/'refeito/c1_evidence_guards_v2.py')),
                numerical_controls=dict(path=str(numpath),sha256=sha(numpath)),
                primary_retrievals=dict(path=str(refs_path),sha256=sha(refs_path)))
    for row in data['rows']:
        if row['reading'] in ('R-A','R-RAIZ-EP4'):
            row.update(excluded_if_universal=None,
                excluded_if_universal_P1_matter=validated['clock']['P1_excluded'],
                excluded_if_universal_P2_independent_arm_light_modes=validated['clock']['P2_excluded'],
                P2_tau_star_bound_in_tP=measured['P2_tau_star_bound_tP'],
                exclusion_scope='P1 matter not excluded; P2 local independent optical arm modes excluded. These are separate physical partitions, not a universal verdict on the theory.')
        if row['reading']=='R-MOD':
            row.update(excluded_if_universal=validated['clock']['unruh_g_excluded'],
                exclusion_scope='If the same local KMS horizon period governs laboratory clocks (terrestrial Unruh-g), v369 excludes that extension. A non-universality rule is required to avoid it; the operator specifies the physical partition.',
                physical_statute='CONJECTURE — management hypothesis, not TGL canon',
                step5='Numerical coincidence near spin 0.68, not identity with R-RAIZ-0.',
                spin_discriminant=measured['spin_comparison'],
                exact_QNM_provenance='qnm '+measured['qnm_version']+'; fresh mode evaluation in numerical controls; old catalog values preserved')
        row['units_derived_SI_mass_length_time']=measured['dimensions'][row['reading']]
    data['limits']=[x for x in data['limits'] if 'Null universal flag' not in x]
    data['limits']+=['Partition-specific fields govern R-A and R-RAIZ-EP4; a null aggregate is not a favorable verdict.',
        'Kay-Wald full text access failed (403); Sewell DOI returned a redirect, not the article. No claim of reading either full article.',
        'Bisognano-Wichmann 1975/1976 complete PDFs archived; relevant introduction, modular and theorem sections read, not every proof.',
        'Numerical controls re-evaluate all 264 CSV rows, including the requested 99 R-A/R-RAIZ-EP4/R-RAIZ-REST rows. The 132 sub-resolution count also includes 33 exactly zero R-GLOBAL rows.']
    target=ROOT/'C1_LEITURAS_v4.json'
    write_new(target,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=[f'[DERIVED condicional; CONJECTURE na ponte Kerr–KMS] {stamp}; adendo a C1_LEITURAS.json, SHA256 {sha(original)}.',
      '', '# C1 — correções medidas e limites da leitura modular', '',
      'Nenhuma leitura foi selecionada. O ensaio é NÃO-CEGO quanto aos dados já publicados. A coluna das falas do operador permanece vazia.',
      '', 'As bandeiras de R-A e R-RAIZ-EP4 agora separam P1 (matéria, não excluída) de P2 (modos ópticos independentes por braço, excluída nessa partição). A cota P2 lida do núcleo é τ★/tP ≤ '+format(measured['P2_tau_star_bound_tP'],'.12g')+'. Cota da série mediana, com margem de calibração; sem nível de confiança atribuído.',
      'R-MOD recebe excluded_if_universal=true apenas para a extensão do período KMS local aos relógios terrestres (Unruh-g). Sua sobrevivência requer regra explícita de não universalidade, parte da partição física a cargo do operador.',
      '', '## Passo 5: coincidência numérica, não identidade', '',
      '| spin | δτ R-MOD, QNM exato | δτ R-RAIZ-0, QNM exato | R-MOD, controle BCW |',
      '|---:|---:|---:|---:|']
    for row in measured['spin_comparison']:
        lines.append('| {spin:g} | {delta_mod:.9g} | {delta_root_zero:.9g} | {delta_mod_bcw_control:.9g} |'.format(**row))
    lines += ['', 'As duas expressões têm dependências distintas em spin. A proximidade perto de 0,68 não fornece uma identidade de operadores nem escolhe uma leitura. O controle BCW é impresso como aproximação; o ramo corrotante usa QNM exato.',
      '', '## Passo 1: fontes e três rotas para spin não nulo', '',
      '[KNOWN — seções do integral consultadas] Bisognano–Wichmann 1975: introdução, Teoremas 1–2 e discussão de Tomita–Takesaki (pp. 993, 997–998). O enunciado usa cunhas de Minkowski, vácuo, covariância e hipóteses sobre campos/álgebras. Não estabelece um estado térmico global em Kerr. Em 1976, introdução e Teorema 1 estendem o quadro a campos com spin e explicam a dualidade modificada na presença de férmions; tampouco identificam QNM com oscilador fechado.',
      '[OPEN — integral não lido] Kay–Wald 1991: tentativas na editora e repositório autoral retornaram HTTP 403. Sewell 1982: o DOI forneceu apenas uma página de redirecionamento; a página recebida não contém o artigo. A referência bibliográfica não paga uma leitura integral. O passo fecha como parede de acesso documentada, não como teorema importado verificado nesta rodada.',
      '[CONJECTURE — hipóteses da construção, não cânone] As alternativas são:',
      '1. Restringir a região dentro da superfície em que o gerador corrotante se torna nulo e selecionar modos com ν=ω_R−mΩH>0. No oscilador efetivo escolhido, Z=Σ exp[−(2π/κ)νn] converge. Perde-se a identificação com todo o exterior assintoticamente plano; condições de contorno e existência do estado regional continuam exigências independentes. A positividade de um modo não prova a existência do estado completo.',
      '2. Incluir um modo bosônico com ν<0 mantendo esse mesmo ansatz de Gibbs: os termos da soma geométrica crescem, logo Z diverge; em ν=0 também diverge. Não há estado normalizado desse oscilador. Uma truncagem finita esconderia a obstrução; não a remove no limite. Isso refuta o ansatz, não todos os estados de Kerr.',
      '3. Usar um estado de Unruh para o problema de emissão/colapso. Nessa rota não se pressupõe equilíbrio KMS global do exterior. Perde-se a passagem automática K=(2π/κ)νN+log Z, ds/dt=κ/(2π) para toda a dinâmica; Γ da R-MOD não decorre apenas do nome Unruh. A lei de ruído/readout ainda exige derivação.',
      '', '## Passos restantes e unidades', '',
      'κ=√(1−χ²)/[2t_M(1+√(1−χ²))] e ν=ω_R−mΩH têm unidade s⁻¹; −Im ω determina τ_GR separadamente. Passo 2 [DERIVED condicional]: assumindo o oscilador positivo, K=(2π/κ)νN+log Z e ds/dt=κ/(2π), a coerência adjacente do duplo comutador dá Γ=πβν²/κ. Passo 3: o domínio ν>0 é exigido, e o ramo fora dele é recusado. Passo 4: a extensão universal laboratorial foi corrigida acima. Passo 6: estatutos permanecem separados. Nenhuma dessas contas prova a identificação do estado físico do horizonte.',
      'As dimensões foram reconstruídas a partir de G, c, ħ, massa, frequência e energia, com expoentes racionais SI; uma soma de taxa com tempo é recusada como controle negativo. R-PROP é um expoente adimensional de propagação. R-GLOBAL tem taxa relacional nula por hipótese.',
      '', '## C3.1 — constantes e regressão', '',
      'LEGACY_V346 preserva G=6,674×10⁻¹¹ e M☉=1,98892×10³⁰ kg: não é o perfil CODATA2018/IAU2015. Comparação abaixo em z=0, para não misturar a diferença de constantes com a convenção de relógio fonte/detector:',
      '', '| leitura | Γ_legado/Γ_moderno−1 | δτ_legado/δτ_moderno−1 |','|---|---:|---:|']
    for row in measured['profile_comparison']:
        lines.append('| {reading} | {gamma_legacy_over_modern_minus_one:.9g} | {delta_legacy_over_modern_minus_one:.9g} |'.format(**row))
    lines += ['', f"Recalculadas {validated['checked']}/{validated['checked']} linhas do CSV, inclusive as {validated['small']} linhas pequenas solicitadas. O contador de {validated['sub_resolution']} inclui também as {validated['zero']} linhas R-GLOBAL de efeito exatamente nulo. Todas as diferenças relativas nas três colunas ficaram abaixo de 10⁻¹²; este é controle de reprodução do módulo, não uma segunda derivação independente de todas as leis.",
      'A regressão v346 compara delta_tau_linear; a expressão de ensemble exata é −x/(1+x). O modo realization continua sem previsão universal: NÃO PAGO como distribuição calibrada de uma pipeline física; requer desenrolamento, estimador, janela e ruído nomeados. Os ensaios condicionais de C2 são separados.',
      '', '## Evidência e reprodução', '',
      f'- C1_LEITURAS_v4.json: {sha(target)}', f'- C1_NUMERICAL_CONTROLS_v2.json: {sha(numpath)}', f'- C1_PRIMARY_RETRIEVALS.json: {sha(refs_path)}']
    for row in refs:
        if row.get('sha256'):
            lines.append('- '+row['name']+': '+row['sha256']+'; '+row['url'])
    lines += ['', 'Comando do cálculo: `/opt/lal_env/bin/python -B refeito/measure_c1_013bis_v2.py` a partir da bancada WSL. O script recusa sobrescrever resultado existente; para nova auditoria, executar uma cópia numa pasta própria com seus insumos.',
      'Axiomas: N/A — sem Lean. A fonte canônica não foi executada nem editada. Não foram feitas PE, calibração pesada ou seleção de partição. A falha inicial de token da guarda P2 permanece em bis/C1_FAILED_P2_TOKEN_PREFIX.txt e no código .failed_P2_TOKEN_PREFIX.',
      'Abertura do operador: SHA256 '+sha(ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md')+'.']
    write_new(ROOT/'C1_ADENDO_CORRECOES_013BIS_v3.md','\n'.join(lines)+'\n')
    fiche=['[REAL — reaproveitamento C1; sem seleção física]', '',
      'Existia: tgl_ringdown_prediction.py:16 (β em runtime), :48 (BCW), :73 (prediction), :109 (R-MOD); C1_LEITURAS.json; QNM_GRID.json; C4_CATALOG_220.json; C7_INDEPENDENT/tables/event_reading_predictions.csv.',
      'Reusado: as funções de predição e os insumos congelados; a biblioteca qnm 0.4.4 já disponível. Novo: controles em spin, dimensões derivadas, reprodução CSV, perfis de constantes, bandeiras separadas P1/P2 e adendo de limites bibliográficos.',
      'Motivo: atender as correções medidas de F1 sem apagar a v1 nem transformar hipótese modular em identificação física.',
      'Não pago: identificação física do estado Kerr; leitura integral de Kay–Wald/Sewell; calibração da transferência realização→posterior.',
      'Axiomas: N/A — sem Lean.', '']
    for p in [original,target,numpath,ROOT/'C1_ADENDO_CORRECOES_013BIS_v3.md',ROOT/'tgl_ringdown_prediction.py']:
        fiche.append(str(p)+' — SHA256 '+sha(p))
    write_new(ROOT/'REAPROVEITAMENTO_C1_v3.md','\n'.join(fiche)+'\n')
    require(original.read_bytes()==before,'Historical v1 changed')
    print(json.dumps(dict(original_unchanged=True,v2_sha256=sha(target),adendo_sha256=sha(ROOT/'C1_ADENDO_CORRECOES_013BIS_v3.md')),indent=2))

if __name__=='__main__': main()
