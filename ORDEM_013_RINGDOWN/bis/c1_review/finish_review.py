"""Supplemental scalar checks and Portuguese review; writes authorized paths only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
from independent_checks import ROOT, HERE, quantities, error, ALPHA_FINE_CODATA_2018


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_new(path, text):
    if path.exists():
        raise FileExistsError(path)
    raw=text.encode('utf-8'); temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw and raw
    if path.exists():raise FileExistsError(path)
    temp.rename(path)


def main():
    numeric=json.loads((HERE/'independent_results.json').read_bytes())
    guards=json.loads((HERE/'guard_probe_results.json').read_bytes())
    c1=json.loads((ROOT/'C1_TABLES.json').read_bytes())
    beta=float(ALPHA_FINE_CODATA_2018)*math.sqrt(math.e)
    extra=[]
    for row in c1['rows']:
        inp,p=row['inputs'],row['prediction']; reading=p['reading']
        if reading=='R-RAIZ-COHERENT':
            base=quantities(inp['mass'],inp['spin'],inp['redshift'],'R-GLOBAL')
            fresh={'gamma_per_s':beta*base['omega']/(8*1e78),'gamma_over_omega':beta/(8*1e78)}
            assert p['delta_tau'] is None
        else:
            mode=[p['omega_mass'],-p['t_mass_s']/p['tau_gr_s']] if reading=='R-MOD' else None
            values=quantities(inp['mass'],inp['spin'],inp['redshift'],reading,mode=mode)
            fresh={'gamma_per_s':values['Gamma_per_second'],'gamma_over_omega':values['Gamma_over_omega'],'delta_tau':values['delta_tau']}
        extra.append({'event':row['event'],'reading':reading,'relative_errors':{k:error(value,p[k]) for k,value in fresh.items()}})
    inp=next(r['inputs'] for r in c1['rows'] if r['event']=='GW250114_public_posterior_medians')
    local=quantities(inp['mass'],inp['spin'],inp['redshift'],'R-A')
    prop=c1['propagation_example']; zmax=prop['z_max']; h0=prop['H0_km_s_Mpc']*1000/3.085677581491367e22
    def xi(n):
        dz=zmax/n
        f=lambda j:(1+j*dz)/(h0*math.sqrt(.3*(1+j*dz)**3+.7))
        integral=dz/3*(f(0)+f(n)+4*math.fsum(f(j) for j in range(1,n,2))+2*math.fsum(f(j) for j in range(2,n,2)))
        return beta*local['t_planck']*local['omega']**2*integral/2
    supplement={'utc':datetime.now(timezone.utc).isoformat(),'script_sha256':sha(Path(__file__)),
                'source_hashes':{p:sha(ROOT/p) for p in ('C1_TABLES.json','build_c1_tables.py')},
                'rows':extra,'max_relative_error':max(max(r['relative_errors'].values()) for r in extra),
                'propagation':{'stored_trapezoid_4096':prop['Xi'],'independent_simpson_512':xi(512),
                               'independent_simpson_1024':xi(1024),'relative_difference':error(xi(1024),prop['Xi']),
                               'scope':'INPUT_FLRW_ILLUSTRATION__NOT_A_RINGDOWN_RATE'},
                'final_input_hashes':{name:sha(ROOT/name) for name in numeric['inputs_before']}}
    supplement['all_original_inputs_still_unchanged']=supplement['final_input_hashes']==numeric['inputs_before']
    assert supplement['all_original_inputs_still_unchanged']
    assert supplement['max_relative_error']<1e-12
    write_new(HERE/'supplementary_results.json',json.dumps(supplement,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    files=['C1_LEITURAS_v2.json','C1_ADENDO_CORRECOES_013BIS.md','REAPROVEITAMENTO_C1.md',
           'refeito/measure_c1_013bis.py','refeito/record_c1_013bis.py',
           'bis/C1_NUMERICAL_CONTROLS.json','bis/C1_PRIMARY_RETRIEVALS.json',
           'C1_LEITURAS.json','cache/casa/um_absoluto.json',
           'bis/c1_review/independent_checks.py','bis/c1_review/independent_results.json',
           'bis/c1_review/guard_probes.py','bis/c1_review/guard_probe_results.json',
           'bis/c1_review/finish_review.py','bis/c1_review/supplementary_results.json']
    manifest='\n'.join(f'| `{name}` | `{sha(ROOT/name)}` |' for name in files)
    runtime=r'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    spin_table='\n'.join(f"| {r['spin']:g} | {r['delta_mod']:.12g} | {r['delta_root_zero']:.12g} | {r['delta_mod_bcw_control']:.12g} | {100*r['mod_bcw_relative_error']:.6g}% |" for r in numeric['spin'])
    profile_table='\n'.join(f"| {r['reading']} | {r['gamma_legacy_over_modern_minus_one']:.12g} | {r['delta_legacy_over_modern_minus_one']:.12g} |" for r in numeric['profiles'])
    report=f'''[REAL — auditoria independente dos bytes e cálculos C1/F1; CONJECTURE preservada na ponte QNM–KMS; sem alteração de gate]

# Parecer adversarial C1 — ORDEM 013-bis

Data UTC: {datetime.now(timezone.utc).isoformat()}. Casa: `C:\\IALD\\Central de Patentes`. Raiz dos caminhos relativos deste parecer: `{ROOT}`.

**Conclusão: números e bandeiras do rascunho aprovados no escopo conferido; scripts de certificação aprováveis somente após as correções B1/B2 abaixo.** Não encontrei bloqueante científico ou aritmético nos valores atuais. Há defeitos reproduzidos de validação que bloqueiam qualificar o procedimento automático como fail-closed. Isso não transforma os dados atuais em incorretos: a conferência independente, com guardas adicionais, passou.

O parecer não é entrega M1 nem aprovação de F1 inteiro. Não cobra do rascunho uma entrega formal que ele não anuncia. C0/C2/C5-Fisher, F0/F2/F7, PE e demais frentes não foram duplicados. O `record_c1_013bis.py` auditado está efetivamente em `refeito/`.

## 1. Achados e correções exatas

### B1 — Bloqueante para a garantia fail-closed do medidor: duplicatas e NaN passam

**[REAL; prioridade P2]** `refeito/measure_c1_013bis.py:76–91` transforma diretamente o CSV em dicionário e usa `max(errors.values()) < 1e-12`. A sonda independente em memória demonstrou:

- 265 linhas, incluindo duplicata, tornam-se as mesmas 264 entradas; uma duplicata conflitante anterior com `delta_tau=12345` também desaparece.
- Com erros na ordem efetiva do código, `max([0.0, 0.0, NaN])` devolve `0.0`; portanto um `NaN` no último campo passa na guarda. O NaN pode vir do baseline CSV, sem alterar a fórmula.
- O código não verifica igualdade exata dos conjuntos de chaves catálogo/CSV, unicidade nem cardinalidade esperada. O `PASS` pode certificar somente um subconjunto se os insumos forem reduzidos juntos.

**Correção:** materializar as linhas brutas; rejeitar duplicatas antes de construir o dicionário; validar `math.isfinite` em cada entrada, previsão e erro; exigir igualdade exata entre os conjuntos de `(evento, leitura)`; conferir 33 eventos × 8 leituras = 264 chaves neste insumo congelado e os grupos 99 + 33. Usar `ValueError`/`RuntimeError` explícitos para guardas contratuais, para que `python -O` não as remova. Preservar o ensaio negativo com duplicata conflitante e NaN. Não é necessário recalcular PE.

**Efeito nesta rodada:** nenhum valor atual está não finito; as 264 chaves são únicas e a cobertura é exata. Evidência: `bis/c1_review/guard_probe_results.json` e `independent_results.json`. As variantes foram criadas só em memória; o CSV original não foi editado.

### B2 — Bloqueante para certificação automática pelo registrador: afirmações fixas sem validar a evidência

**[REAL por inspeção estática; prioridade P2]** `refeito/record_c1_013bis.py:18–44` lê os controles e imediatamente prepara o status corrigido e as bandeiras. O texto emitido contém contagens fixas “264/264”, “99”, “132” e erro inferior a 10⁻¹² sem verificar `status`, `checked`, conteúdo de `csv_checks`, dependências ou P1. O medidor valida P2/Unruh-g, mas não P1; o registrador grava P1=false como literal. Estes campos coincidem com o cache atual, porém a rotina não recusa uma evidência parcial ou desatualizada.

**Correção:** antes de gravar qualquer artefato, cruzar os hashes de `measured.dependencies` com os bytes atuais; conferir status esperado, cobertura, finitude e limiar de cada erro; conferir P1/P2/Unruh-g e a cota diretamente no snapshot identificado de `um_absoluto.json`. Gerar as contagens do texto a partir dos dados validados. Na divergência, interromper antes de criar v2/adendo/ficha. Isso é uma correção da cadeia de certificação, não mudança da partição física.

### C1 — Proveniência da v2 ambígua

**[REAL; correção de custódia]** `C1_LEITURAS_v2.json:814` conserva `generator_sha256` do `complete_c1_contract.py`, que gerou a v1. O hash confere com esse arquivo, mas não identifica o registrador da v2. Não há hash falso: falta distinguir as duas gerações.

**Correção:** preservar esse hash com papel explícito de gerador de origem e acrescentar `v2_generator={{path,sha256}}` para `refeito/record_c1_013bis.py`, além das dependências medidas. Incluir os dois scripts na futura ficha de reprodução. O script de registro ainda contém referências antigas de linhas do módulo (:18/:47/:64/:108), enquanto a ficha existente já usa :16/:48/:73/:109; alinhar a geração com a ficha ou usar nomes de funções e hashes.

### C2 — Precisões editoriais, sem bloqueio numérico

- Acrescentar à cota P2: **“cota da série mediana, com margem de calibração; sem nível de confiança atribuído”**. É a qualificação presente em `core.clock_test_result_v369.P2.gamma_upper_bound_note`. O adendo não a chama de 95%, mas deve carregar o escopo junto com o número.
- Na fórmula modular, escrever `ν=ω_R−mΩ_H` e `κ=√(1−χ²)/[2t_M(1+√(1−χ²))]`, em s⁻¹. O código usa a parte real do QNM; `−Im ω` entra separadamente em τ_GR. Evita ler uma frequência complexa como energia autoadjunta do oscilador.
- O registro de Sewell comprova HTML de redirecionamento, não artigo. A frase de falha adicional “pela ferramenta web” no adendo não tem log próprio entre os artefatos auditados: retirar essa oração ou marcá-la `[DECLARADO]` e anexar a evidência antes de promovê-la a verificação documental. Os dois 403 de Kay–Wald estão registrados como resultados das tentativas; não foram repetidos nesta auditoria.

## 2. Critérios C1/F1 conferidos

| Critério | Resultado desta revisão |
|---|---|
| R-A e R-RAIZ-EP4: P1=false, P2=true | PAGO — iguais ao sentido dos resultados do cache, com partições separadas. |
| Cota P2 | PAGO numericamente — {numeric['flags']['P2_bound_stored']:.17g} tP; também refeita por `gamma_upper_bound_s_median_with_cal/gamma_s`. Qualificação editorial em C2. |
| R-MOD=true somente na extensão terrestre Unruh-g | PAGO — o cache tem `unruh_g_excluded=true`; sem exclusão irrestrita da leitura BH. |
| Passo 5: spin e BCW × QNM | PAGO — sete spins conferidos independentemente; coincidência perto de 0,68 não é identidade. |
| Passo 1: BW e três rotas | PAGO como discussão condicional e parede documental permitida; não como identificação física completa. |
| Kay–Wald/Sewell integrais | NÃO PAGO como leitura; parede declarada admitida pela ordem. Não é bloqueante artificial desta F1. |
| Dimensões | PAGO — taxas em s⁻¹; Ξ adimensional; reescala independente de M,L,T passou. O zero relacional recebe a unidade de taxa por tipagem. |
| 99 linhas pequenas e 264 CSV | PAGO para os bytes atuais; defeitos gerais do validador em B1/B2. |
| Perfis e regressão | PAGO para as diferenças impressas em z=0; a chave histórica é `delta_tau_linear`. Não foi reexecutado o rito v346. |
| Escolha física/falas do operador | PAGO — nenhuma leitura selecionada; dez campos `physical_selection` e dez `relation_to_operator_16Sep` permanecem null. |
| Integridade dos insumos | PAGO — hashes declarados conferidos, inclusive dependências e remissões de fonte/linha. v1 e demais insumos permaneceram idênticos. |

## 3. Cálculos independentes

Não importei `tgl_ringdown_prediction`, `qnm`, scripts da bancada ou `um.py`. Usei Python bundled/NumPy e fórmulas novas em Decimal com 120 dígitos. Nos offsets, calculei diretamente a diferença das raízes nessa precisão, em vez de reutilizar a racionalização do módulo. β foi sempre construído em runtime como `ALPHA_FINE_CODATA_2018 × √e`.

**CSV:** 33 eventos distintos, oito leituras por evento, 264 chaves distintas. Conferidos Γ, Γ/ω e δτ em todas as linhas: erro relativo máximo **{numeric['csv']['max_relative_error']:.6g}**, abaixo de 10⁻¹². Para zeros, foi usada diferença absoluta e verificada igualdade exata. O erro zero do relatório original é reprodução do mesmo módulo; o erro independente acima tem outra implementação.

| Grupo | Linhas |
|---|---:|
| R-A | 33 |
| R-RAIZ-EP4 | 33 |
| R-RAIZ-REST | 33 |
| Pequenas não nulas solicitadas | **99** |
| R-GLOBAL exatamente nula | **33** |
| Total pelo predicado `abs(delta_tau)<1e-6` | **132** |

Esse predicado é uma classificação numérica do script, não resolução estatística calibrada de detector. Restam 132 linhas das quatro leituras de maior efeito. Portanto, o “165 verificadas + 99 não refeitas” da ordem é compatível com incluir as 33 R-GLOBAL entre as 165 já conferidas; chamá-las todas de “resolvidas” é nomenclatura imprecisa, não uma quinta leitura de efeito resolvido.

**QNM:** os sete pares novos foram submetidos à equação angular por matriz espectral (truncagens l=16/24) e à recorrência radial de Leaver (profundidades 400/800), sem ajustar a frequência fornecida. Resíduo radial absoluto máximo **{max(r['radial_abs_depth800'] for r in numeric['spin']):.6g}**. Perturbar a frequência em 10⁻⁴ eleva o resíduo à ordem 10⁻³; o controle tem sensibilidade. Nos 33 pares arquivados do catálogo, o máximo foi **{max(r['radial_abs_depth800'] for r in numeric['catalog_mode_residuals']):.6g}**, compatível com sua origem interpolada. Isso é consistência numérica das equações, não prova rigorosa de erro nem quantização do QNM.

A matriz angular e a recorrência padrão foram cruzadas com a documentação primária do pacote: [qnm.angular](https://qnm.readthedocs.io/en/latest/_modules/qnm/angular.html) e [qnm.radial](https://qnm.readthedocs.io/en/latest/_modules/qnm/radial.html). A recorrência física não é uma descoberta desta revisão; a avaliação foi nova, em código separado, sem executar o solver arquivado.

| χ | δτ R-MOD (QNM) | δτ R-RAIZ-0 (QNM) | δτ R-MOD (BCW) | BCW/QNM−1 |
|---:|---:|---:|---:|---:|
{spin_table}

Em χ=0,6785 o desvio BCW é cerca de +3,18%; em 0,9, −22,82%; em 0,95, −50,71%. A tabela do adendo é correta. O uso de BCW no controle está explicitamente rotulado e não substitui o ramo QNM.

**Perfis em z=0:** G legado=6,674×10⁻¹¹, massa solar legada=1,98892×10³⁰ kg, ħ legado=1,054571817×10⁻³⁴ J·s. Perfil moderno usa G=6,67430×10⁻¹¹, GM☉ nominal=1,3271244×10²⁰ m³/s² e ħ=h/(2π). Portanto, as diferenças impressas são do perfil completo, não somente de G. A comparação em z=0 separa constantes da convenção de relógio/redshift.

| Leitura | Γ_legado/Γ_moderno−1 | δτ_legado/δτ_moderno−1 |
|---|---:|---:|
{profile_table}

Em R-B, `x=β w(χ)²/(2q)` com `q=−Im(Mω)` não depende da escala de massa; por isso δτ não muda com o perfil, embora Γ mude. O zero impresso é consistente, não perda da correção. R-LIN tem o mesmo cancelamento da escala.

**Demais exemplos da v2:** as 18 entradas herdadas de C1_TABLES também conferiram, erro relativo máximo {supplement['max_relative_error']:.6g}. A taxa coerente corresponde somente à inclinação inicial do cenário N=10⁷⁸; δτ continua null. Para R-PROP, Simpson independente deu Ξ={xi(1024):.12g}, contra {prop['Xi']:.12g} pelo trapézio arquivado; diferença relativa {error(xi(1024),prop['Xi']):.6g}, compatível com a discretização. Não é uma taxa extra de ringdown.

## 4. Estatutos e honestidade das fontes

**[KNOWN no alcance lido]** Conferi os TXT locais de BW1975: introdução, enunciados dos Teoremas 1–2 e discussão de Tomita nas pp. 993 e 997–998; BW1976: introdução e Teorema 1 (p. 310). O texto efetivamente trata de cunhas, vácuo, condições sobre campos/álgebras e a modificação para férmions. O adendo não extrapola isso a um equilíbrio global de Kerr. **Não li cada prova nem afirmo leitura integral dos PDFs.** Os hashes/tamanhos dos PDFs arquivados conferem com o registro de recuperação; isso comprova identidade dos bytes, não leitura integral.

Kay–Wald: o JSON registra falha 403 nas duas tentativas; não há texto integral lido nesta rodada. Sewell: o HTML tem título `Redirecting` e redirecionamento, sem conteúdo do artigo. “RETRIEVED” nesse registro significa bytes recebidos, conforme seu `reading_scope=RETRIEVAL_ONLY`; não significa obra lida. É recomendável acrescentar `content_class=REDIRECT_ONLY` em futura evidência, preservando o registro original.

**[DERIVED condicional]** Para ν>0 no oscilador escolhido, `Z=1/(1−exp(−2πν/κ))` é finito; em ν=0 a soma diverge e em ν<0 seus termos crescem. Isso rejeita esse ansatz bosônico irrestrito, não todos os estados possíveis em Kerr. As condições regionais/de contorno e a existência do estado físico não decorrem da positividade de um único modo.

Com `K=(2πν/κ)N+log Z`, `dρ/ds=−(β/2)[K,[K,ρ]]` e `ds/dt=κ/(2π)`, a coerência adjacente fornece Γ=πβν²/κ; uma matriz finita independente confirmou o coeficiente. K e s são adimensionais; κ e ν têm s⁻¹. Esta é a álgebra do modelo efetivo. Identificar esse oscilador, seu K e seu relógio com o sistema físico de Kerr permanece **[CONJECTURE]**. O QNM dissipativo não vira, pela conta, oscilador fechado autoadjunto.

A rota de Unruh preserva uma descrição de emissão/colapso, mas não paga automaticamente o ansatz KMS nem a lei de ruído/readout; o adendo diz isso. A regra de não universalidade de R-MOD permanece pendência física do operador. A restrição ν>0 é visível no código; não foi mascarada por quadrar uma frequência negativa.

`realization` está declarada NÃO PAGA como distribuição calibrada; não há promoção a medição de um único evento. Não se encontrou escolha física, confirmação da natureza, compilação Lean alegada nesta rodada ou movimentação de gate. Axiomas: **N/A — sem Lean**.

## 5. Reprodução e custódia

Artefatos de revisão ficam exclusivamente em `bis/c1_review/` e neste parecer. Os scripts usam saídas exclusivas e recusam sobrescrita. Para reproduzir de novo, copiar **os scripts da revisão e os insumos para uma bancada isolada**, preservando a estrutura relativa; não executar os scripts de produção sobre esta pasta. A recusa diante de resultado existente é intencional. Os comandos executados, a partir de `{ROOT.parent.parent}`, foram:

```powershell
& '{runtime}' -B 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/independent_checks.py'
& '{runtime}' -B 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/guard_probes.py'
& '{runtime}' -B 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/finish_review.py'
```

Não foi necessário WSL/escalonamento. Não executei/importei `um.py`, medidor/registrador originais, PE ou injeções; não alterei memórias, canônico, v1 ou resultados existentes. Falhas de acesso amplas na busca inicial e ausência de `C:\\IALD\\AGENTS.md` não foram tratadas como sucesso; as instruções fornecidas, skill e protocolo específico foram lidos. Os TXT/PDF só foram consultados/hasheados, sem regravação. As checagens de integridade ao início/fim confirmaram que os insumos auditados permaneceram idênticos.

| Arquivo | SHA256 lido por script |
|---|---|
{manifest}

**Encaminhamento C1/F1:** corrigir B1/B2 antes de certificar o procedimento como fail-closed; ajustar a proveniência e qualificações C1/C2. Preservar os números aprovados, a v1, a parede Kay–Wald/Sewell e todos os estatutos condicionais. A aceitação global da ordem permanece fora deste parecer.
'''
    write_new(ROOT/'bis/C1_ADVERSARIAL_REVIEW.md',report)
    print(json.dumps({'review_path':str(ROOT/'bis/C1_ADVERSARIAL_REVIEW.md'),
                      'review_sha256':sha(ROOT/'bis/C1_ADVERSARIAL_REVIEW.md'),
                      'supplementary_sha256':sha(HERE/'supplementary_results.json'),
                      'all_original_inputs_still_unchanged':True,
                      'propagation':supplement['propagation']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
