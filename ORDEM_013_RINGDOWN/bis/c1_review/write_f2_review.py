"""Write the compact F2 review from independent audit receipts."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_bytes())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
p=R/'bis/F2_DENSITY_CLOCK_REVIEW.md';need(not p.exists(),'Output exists')
r=load('bis/c1_review/f2_light_results.json');s=load('bis/c1_review/f2_support_results.json')
for n,h in r['input_hashes'].items():need(sha(R/n)==h,'Input changed: '+n)
need(sha(R/'bis/F2_FREE_CLOCK_EXTENDED.json')==s['curve_sha256'],'Curve changed')
gtable='\n'.join(f"| {v['reading']} | {v['lnB']:.12g} |" for v in r['gaussian'])
ctable=[]
for cross in r['crossings']:
    bw=cross['bandwidth'];point=next(v for v in r['sparse_KDE_controls'] if v['bandwidth']==bw and v['q']==cross['q'])
    qp=next(v for v in s['support'] if v['bandwidth']==bw and v['is_q95_L20'])
    integral=next(v for v in r['integrals'] if v['bandwidth']==bw and v['ceiling']==20)
    ctable.append(f"| {bw} | {cross['q']:.9f} | {point['ESS_shifted']:.6f} | {integral['q95']:.9f} | {qp['ESS_shifted']:.6f} | {integral['lnB']:.9f} |")
ctable='\n'.join(ctable)
paths=['bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json','bis/F2_FREE_CLOCK_EXTENDED.json','refeito/measure_f2_density_clock_013bis.py','bis/REGISTRO_C4_EMENDA_013BIS.json','C4_EMENDA_TECNICA_013BIS.md','bis/c1_review/f2_light_checks.py','bis/c1_review/f2_light_results.json','bis/c1_review/f2_support_probe.py','bis/c1_review/f2_support_results.json','bis/c1_review/write_f2_review.py']
hashes='\n'.join(f'| `{n}` | `{sha(R/n)}` |' for n in paths)
text=f'''[REAL — controles de aproximação NÃO-CEGOS; OPEN — suporte de densidade na cauda; sem exclusão física]

# Revisão compacta F2: densidade e relógio

Data UTC: {datetime.now(timezone.utc).isoformat()}. Caminhos relativos a `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`.

**Estimador gaussiano aprovado no escopo solicitado; fórmula e aritmética do relógio estendido corroboradas. Um achado de suporte permanece aberto:** os três cruzamentos de −ln(100) têm ESS local abaixo de 100, mínimo declarado na emenda. Não aprovo esses cruzamentos como cortes sustentados pelo dado. Os números continuam válidos como avaliações da aproximação KDE arquivada; o artefato já evita exclusão física, mas falta transportar o diagnóstico de suporte para os resultados.

F4-R1/R2 foram encerrados antes desta revisão, separadamente em `bis/F4_CLOSING_REVIEW.md`. Não se reabre esse fechamento. Esta revisão não certifica toda F2, catálogos, calibração ou PE.

## Independência, fórmula e controles

[REAL] O novo estimador ajusta **uma gaussiana bivariada de covariância amostral completa** aos dados cisalhados `(df, dtau−g(spin))`. Não usa banda de KDE. Portanto é uma aproximação de densidade de fato distinta, conforme a opção expressa na ordem; compartilha amostras e curva física, logo não é evidência estatisticamente independente. A comparação interna com scipy valida a fórmula, não a adequação gaussiana. Caudas/assimetria permanecem uma limitação explícita.

Reabri os 40.776 posteriores existentes, sem importar o builder ou módulos de produção. Recalculei os quatro deslocamentos por fórmulas adimensionais independentes: x_B=β·omega_R·Q, x_raiz=βQ, x_lin=2βQ; para R-MOD, x=βπ(omega_R−chi/(1+sqrt(1−chi²)))²/(kappa_adimensional·|omega_I|), com interpolação B-spline da grade QNM arquivada. β foi calculado de alpha CODATA2018×sqrt(e), sem literal beta. R-MOD mantém seu caráter de hipótese física condicional; esta conta não demonstra KMS global em Kerr.

Usei médias/somas compensadas e a inversa/determinante explícitos da matriz 2×2, sem chamar a função gaussiana do builder. Maior diferença absoluta de lnB: {max(v['absolute_error'] for v in r['gaussian']):.6g}.

| Leitura | lnB gaussiano independente |
|---|---:|
{gtable}

R-B gaussiano −0,03717 versus KDE central +0,02903 reforça a interpretação já exigida: |lnB| pequeno, sinal dependente do estimador. Não se escolhe o sinal conveniente.

[DERIVED, condicional] O cisalhamento completo tem jacobiano um. Com priors uniformes reais de df220/dtau220 em [−0,8;2] e priors nuisance idênticos, cancela a densidade do prior entre as restrições. A razão é entre densidades marginais no ponto zero após integrar nuisance; não é média de razões condicionais. Os textos dos priors foram lidos no HDF5, inclusive os dois priors livres do 440. As amostras liberadas não têm campo de pesos; equal-weight continua a interpretação declarada da origem, não uma nova prova de independência das amostras.

Para o relógio, q=tau_source/tM_source e g_i(q)=−q x_B,i/(1+q x_B,i). A transformação de fonte para detector cancela o redshift nessa razão. Para teto L, o prior uniforme em tau_source **condicional à massa** transforma-se em aproximadamente 1/L em q; a forma exata é 1/(L−q_min,i), com q_min,i=tP/tM_source,i. O máximo recalculado é {r['max_q_lower']:.12g}; trocar essa borda por zero é numericamente desprezível aqui, e foi declarado.

Se ell(q) é o log da razão de densidades, a evidência livre é `log[integral_0^L exp(ell(q)) dq / L]`; os quantis usam a integral acumulada normalizada sem o fator 1/L. O código implementa ambas. Não confunde uniforme em q condicionado à massa com relógio universal compartilhado ou prior uniforme em segundos com teto fixo para todas as massas.

[REAL] Conferi os 801 nós de cada uma das três grades e refiz as nove integrais/quantis e seus controles de passo 0,05/0,10 a partir dos números arquivados. Todos conferem. Controle independente de densidade com `scipy.stats.gaussian_kde`: q=0,1,10,20,40 para as três bandas, além dos cruzamentos; maior diferença nos nós {max(v['absolute_error'] for v in r['sparse_KDE_controls'] if v['q'] in [0.,1.,10.,20.,40.]):.6g}. Não refiz a grade completa. Por exemplo, banda 1 e q=10: lnB=−5,105451965291; com L=20, q95=6,686242026877 e lnB integrado=−1,528667125036. O corte relativo central é q=9,657703642054, um objeto diferente do quantil.

Os dois priors originais e seus controles foram preservados exatamente no novo JSON. Os tetos 10/20/40, a escolha de banda e o uso NÃO-CEGO são explícitos. Estabilidade numérica do q95 ao mudar o teto não elimina a dependência da evidência em 1/L nem constitui limite posterior independente de prior.

## Achado F2-R1: suporte de cauda omitido

**P2 — bloqueia apresentar o cruzamento como corte apoiado pelo dado ou declarar o diagnóstico de suporte pago.** A emenda, campo ESS, estabelece mínimo 100 para o ponto restrito e o ponto GR. O builder (`measure_f2_density_clock_013bis.py:29`, `:76` e `:82`) retorna densidade, convergência de grade e cruzamento, mas não calcula/transporta ESS. Medi `ESS=(sum w_i)^2/sum(w_i²)` com os mesmos kernels; o ponto GR passa em todas as bandas (564,25; 1154,34; 2230,34), porém:

| Banda | q no cruzamento | ESS restrito no cruzamento | q95, teto 20 | ESS no q95 | lnB integrado, teto 20 |
|---|---:|---:|---:|---:|---:|
{ctable}

Em q=20 e 40, o ESS restrito fica próximo de 1: os grandes lnB negativos dependem essencialmente da cauda de um kernel. Em q=8, banda 1, ESS≈83,54; em q=5, ESS≈392,11. Isso localiza a perda de suporte sem negar a região central. O q95 da banda 0,7 também falha no mínimo declarado; os q95 das bandas 1/1,4 passam localmente, mas suas normalizações ainda integram a cauda pouco sustentada. ESS é diagnóstico de suporte de kernels, não tamanho efetivo de cadeia MCMC nem erro estatístico universal.

**Correção exata, em versão ao lado:** manter curvas, integrais e cruzamentos brutos; acrescentar ESS_GR/ESS_restricted e limiar aos pontos reportados, cruzamentos e quantis, com `INCONCLUSIVE_DENSITY_SUPPORT` onde min(ESS)<100. Separar `quadrature_converged=true` de suporte estatístico, incluindo a ressalva na interpretação dos posteriores. Marcar os três cruzamentos como `raw_KDE_diagnostic`, com `data_supported_cut=null` enquanto falham no critério. Não apagar a cauda, não substituir sua densidade por zero e não reduzir silenciosamente o teto: isso alteraria o prior. Para um limite validado, permanece aberta a avaliação do efeito dessa cauda/robustez da densidade; nenhum desses reparos exige nova PE para documentar a lacuna atual.

A advertência existente “not a posterior bound / not physical exclusion” é correta e permanece. O defeito aqui é a ausência do diagnóstico quantitativo declarado, não uma alegação de confirmação já feita pelo JSON.

## Proveniência e reprodução

[REAL] Conferem SHA do posterior, schema, cinco dependências, builder, emenda, registro original, abertura e testemunho textual. O code_sha256 da emenda identifica seu registrador; o dos resultados identifica o medidor, corretamente distintos. A emenda declara conhecimento prévio, teto escolhido após o diagnóstico e ESS criado depois do registro original. Os hashes autenticam os bytes vinculados; não constituem, sozinhos, prova externa da sequência temporal “antes das contas”. Nenhum estatuto cego foi aceito.

Controles executados em WSL: `/opt/lal_env/bin/python -B <caminho>/bis/c1_review/f2_light_checks.py` e `f2_support_probe.py`. Escrita final pelo Python bundled, sem importação de produção. Scripts recusam sobrescrita; reprodução em cópia isolada preservando os caminhos relativos. Evidências por ponto nos JSON abaixo. Insumos novamente conferidos antes desta escrita, intactos. Sem PE, injeções, builder inteiro, um.py, memória ou canônico. Axiomas: N/A — sem Lean.

| Arquivo | SHA256 lido |
|---|---|
{hashes}
'''
raw=text.encode();tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
need(tmp.read_bytes()==raw and len(raw)>0,'Write differs');need(not p.exists(),'Output appeared');tmp.rename(p)
print(json.dumps(dict(report=str(p),sha256=sha(p),bytes=len(raw))))
