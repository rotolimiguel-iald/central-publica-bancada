"""Assemble the independent RD applicability report from the completed audit."""
from pathlib import Path
from collections import Counter
import ast
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[2]
PREFIX='cache/public/21454847/controls_extracted/'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def new(path, content):
    if path.exists():raise FileExistsError(path)
    raw=content.encode('utf-8');temporary=path.with_name(path.name+'.tmp')
    with temporary.open('xb') as f:f.write(raw)
    assert temporary.read_bytes()==raw
    temporary.replace(path)

def canonical(model):
    result={}
    for key,value in model.items():
        try:result[key]=ast.literal_eval(value)
        except (SyntaxError,ValueError):result[key]=value
    return result

def link(label,rel,line=None):
    suffix=':'+str(line) if line else ''
    return '['+label+'](<'+(ROOT/rel).as_posix()+suffix+'>)'

def main():
    inventory_path=ROOT/'bis/f2_review/rd_inventory.json'
    inventory=json.loads(inventory_path.read_bytes())
    assert not any(inventory[k] for k in ('read_errors','hash_mismatches','missing_on_disk','extra_on_disk'))
    files=inventory['files'];by_path={r['path'].replace('\\','/'):r for r in files}
    nc=[r for r in files if r['type']=='netcdf'];configs=[r for r in files if r['type']=='config']
    changing=[r for r in nc if 'posterior/df' in r['deviations']]
    for r in nc:
        assert r['mode_labels'][0]=='1,-2,2,2,0'
        assert all(ast.literal_eval(a)==ast.literal_eval(b) for a,b in r['embedded_vs_sidecar_model_differences'].values())
    for r in changing:
        for name in ('df','dg'):
            s=r['deviations']['posterior/'+name]
            assert s['finite'] and s['min_by_last_axis'][0]==s['max_by_last_axis'][0]==0 and s['nonzero_by_last_axis'][0]==0
    for r in configs:
        m=canonical(r['sections']['model'])
        assert tuple(m['modes'][0])==(1,-2,2,2,0)
        if 'df_min' in m:
            assert all(m[k][0]==0 for k in ('df_min','df_max','dg_min','dg_max'))
    families=[]
    for family in inventory['families']:
        models=[canonical(m) for m in family['models']]
        assert all(m==models[0] for m in models)
        model=models[0];name=family['family'];parts=name.split('/')
        regime='NOISE_'+parts[parts.index('noisy_data')+1] if 'noisy_data' in parts else ('ZERO_NOISE_INJECTION' if name.endswith('_INJ') else 'OBSERVED_EVENT')
        config_path=PREFIX+name+'/config.ini'
        assert config_path in by_path
        results=[by_path[p.replace('\\','/')] for p in family['results']]
        example=results[0]
        stats={}
        if 'df_min' in model:
            for variable in ('df','dg'):
                stats[variable]=dict(mode220_min=0.,mode220_max=0.,mode220_nonzero=0,
                    mode221_min=min(r['deviations']['posterior/'+variable]['min_by_last_axis'][1] for r in results),
                    mode221_max=max(r['deviations']['posterior/'+variable]['max_by_last_axis'][1] for r in results))
        families.append(dict(family=name,event=parts[1],regime=regime,
            model_short=parts[-1].split('_start')[0],model_config=model,
            config_path=config_path,config_sha256=by_path[config_path]['sha256'],
            result_paths=family['results'],result_count=len(results),config_count=len(family['configs']),
            example_result=dict(path=example['path'],sha256=example['sha256'],mode_labels=example['mode_labels'],
                posterior_fields=example['posterior_names'],deviation_stats=example['deviations']),
            physical_free_modes=['221'] if 'df_min' in model else [],
            free_220=False,deviation_summary=stats,same_lnB_applicable=False))
    code_paths=['catalog_220_readout.py','posterior_220_readout.py']
    paper_rel='../TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt'
    order_rel='../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
    source_paths=['bis/F2_CONTROL_EXTRACTION.json','bis/F2_CONTROL_SCHEMAS.json',paper_rel,order_rel,*code_paths,
        'bis/f2_review/inspect_rd.py','bis/f2_review/rd_inventory.json','bis/f2_review/write_review.py']
    sources=[dict(path=rel,bytes=(ROOT/rel).stat().st_size,sha256=digest(ROOT/rel)) for rel in source_paths]
    primary=next(r for r in families if 'broaddfdg' in r['family'])
    injection=next(r for r in families if r['model_short']=='220+delta221' and r['regime']=='ZERO_NOISE_INJECTION')
    counts=dict(configs=len(configs),netcdf=len(nc),readme=1,hashed_extracted_files=len(files),
        kerr_results=len(nc)-len(changing),free_221_results=len(changing),free_220_results=0,
        model_time_scan_families=len(families),events=len({r['event'] for r in families}),
        schema_fingerprints=len({r['schema_sha256'] for r in nc}),
        samples_per_netcdf=4000,
        fixed_zero_values_per_physical_deviation=sum(math.prod(r['deviations']['posterior/df']['shape'][:-1]) for r in changing),
        observed_event_results=sum(r['result_count'] for r in families if r['regime']=='OBSERVED_EVENT'),
        injection_control_results=sum(r['result_count'] for r in families if r['regime']!='OBSERVED_EVENT'),
        omitted_regular_members=len(inventory['omitted_regular_members']))
    output=dict(status='NOT_APPLICABLE_DIRECT_SAME_LNB_220__DOCUMENTED_F2_JUSTIFICATION',
        epistemic_status='REAL for inspected files and fixed coordinates; DERIVED for applicability decision',
        scope='RD.tar.gz from release 21454847 only; no new PE, density estimation, free-clock or Gaussian-independent work',
        run_same_lnB_permitted=False,lnB=None,usable_free220_posteriors=[],
        reason='All RD posteriors fix physical 220 deviations to Kerr. The only free deviations are log-frequency/log-damping-rate coordinates of 221.',
        F2_disposition='Justification alternative documented; same-lnB RD robustness not computed and not a measured success',
        counts=counts,archive={k:v for k,v in inventory['archive'].items() if k!='members'},
        sources=sources,extracted_sources=[{k:r[k] for k in ('path','member','bytes','sha256')} for r in files],
        all_sources_match_receipt=True,all_nc_read=True,sidecar_and_embedded_models_equal_after_literal_normalization=True,
        omitted_regular_members=inventory['omitted_regular_members'],model_table=families,
        prerequisites_for_other_release=['Joint physical free df220 and dtau220 posterior with remnant parameters',
            'Prior densities and support at GR and the deformation curve, including Jacobian if coordinates change',
            'Same nuisance priors/likelihood treatment within the two hypotheses and explicit higher-mode scope',
            'A documented start-time choice, sampling/weight conventions and no double-counting with pSEOB'],
        not_done=['No code from tar executed; no pickle deserialized; no strain values read',
            'No lnB, Gaussian-independent or free-clock calculation',
            'No external library defaults or spin prior endpoints inferred',
            'No new posterior or nontrivial reparameterization of the 221 model',
            'Not an audit of full F2 or C2 v2'],
        files_written=['bis/f2_review/inspect_rd.py','bis/f2_review/rd_inventory.json','bis/f2_review/write_review.py',
            'bis/F2_RD_APPLICABILITY_REVIEW.json','bis/F2_RD_APPLICABILITY_REVIEW.md'])
    json_path=ROOT/'bis/F2_RD_APPLICABILITY_REVIEW.json'
    new(json_path,json.dumps(output,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    t=[]
    t.append('[REAL — inspeção independente completa dos produtos RD; DERIVED — decisão de aplicabilidade; 22/09/2026] **NÃO É APLICÁVEL RODAR DIRETAMENTE O MESMO ln B DE DEFORMAÇÃO LIVRE DO 220 CONTRA GR NESTES RD.** Não foi encontrado posterior físico livre do 220. O valor de ln B permanece NÃO CALCULADO (`null`), não zero, −∞ ou exclusão. A alternativa de F2 “ou justificar por escrito” recebe esta justificativa documental; o controle numérico RD não foi realizado nem simulado como sucesso.\n')
    t.append('O resultado vale para o RD.tar.gz identificado abaixo. Não afirma inexistência de outro produto público ou impossibilidade de uma análise reformulada. A correção C2 v2 informada pelo operador não foi reaberta nesta tarefa. Nenhum trabalho gaussianindependent/freeclock foi duplicado.\n')
    t.append('## Cobertura integral, não inferência pelos seis primeiros arquivos\n')
    t.append(f"Foram lidos **{counts['configs']} configs**, **{counts['netcdf']} esquemas NetCDF** e o README: **{counts['hashed_extracted_files']}/{counts['hashed_extracted_files']} hashes extraídos conferem**, sem arquivo ausente, extra ou falha de leitura. A hash do próprio tar também confere. Há **31 famílias de modelo/varredura**, cinco supereventos e 14 esquemas distintos. Cada família tem 12 configs (um mestre e 11 locais) e 11 posteriores, cada um com 4 cadeias × 1000 draws. Os seis NC do recibo amostral eram uma amostra de Kerr220+330; não fundamentaram sozinhos a conclusão.\n")
    t.append('Classificação: **297 posteriores Kerr**, **44 com desvios livres somente do 221**, **zero com 220 livre**. São 209 resultados sobre eventos observados e 132 controles de injeção; janelas e modelos do mesmo evento não são evidências independentes. Os diretórios `noise0`/`noise6` são controles, não eventos adicionais.\n')
    t.append('O inventário do tar foi percorrido integralmente, sem extração ou execução adicional. Além dos 714 arquivos auditados, há somente 10 arquivos regulares: cinco scripts de figuras, pyproject.toml, uv.lock e três PDFs de figuras. Não há outro posterior NetCDF/HDF5 nem pickle no inventário deste tar. Os corpos desses dez arquivos não foram lidos; seus nomes e tamanhos estão no inventário. Não foi seguido link HDF5 externo ou simbólico (nenhum encontrado).\n')
    t.append('## Evidência decisiva: qual modo é livre\n')
    t.append('No caso com maior suporte de desvios, '+link('config do evento S240621dy, linhas 1–10',primary['config_path'],1)+', a ordem dos modos é `(1,-2,2,2,0)` e `(1,-2,2,2,1)`, isto é, **220 primeiro, 221 segundo**. Os limites são:\n\n```text\ndf_min = [0., -0.8]    df_max = [0., 1.1]\ndg_min = [0., -2]      dg_max = [0., 0.8]\n```\n')
    example=primary['example_result']
    t.append('No '+link('NetCDF correspondente',example['path'])+', os localizadores são `posterior/mode`, `posterior/df` e `posterior/dg`. Os dois últimos têm forma `(4,1000,2)`; o eixo final segue os rótulos de `posterior/mode`. Em **todos os 44 arquivos com desvios**, os 176.000 valores de `df[...,0]` e os 176.000 valores de `dg[...,0]` são exatamente zero. Min=max=0, contagem não zero=0. A segunda coluna varia. O JSON do parecer contém caminhos exatos, hashes e min/max por família; o inventário contém o esquema de cada arquivo.\n')
    t.append('**Armadilha adicional verificada:** `posterior/df_unit` e `posterior/dg_unit` têm amostras variáveis inclusive no primeiro modo. São coordenadas auxiliares; não são os desvios físicos. Com limites inferior e superior iguais a zero, uma coordenada unitária variável não abre suporte em df220/dg220. Trocar os campos físicos pelos auxiliares fabricaria uma distribuição de deformação.\n')
    t.append('Nos 297 produtos Kerr não há `posterior/df`/`posterior/dg` físicos livres. Há `posterior/m`, `posterior/chi`, `posterior/f` e `posterior/g`: frequência e taxa variam com massa/spin, não com um parâmetro 220 independente. Não se pode converter essa variação em df220 pela comparação com Kerr em parâmetros arbitrariamente fixos. Os configs de cada NC e seus atributos `config` coincidem semanticamente; as diferenças textuais encontradas eram somente formatação de arrays numéricos. Todos declaram a versão `ringdown 1.0.1.dev312+gdee4418`.\n')
    t.append('## Fonte primária e priors: logaritmo não é desvio fracionário\n')
    t.append('A seção 7.1 do '+link('artigo GWTC-5.0 local, linhas 3648–3662',paper_rel,3648)+' explica que as frequências e taxas Kerr são funções da massa final no referencial do detector e do spin; o 220 ancora esses parâmetros, enquanto o modo subdominante pode se desviar. A Eq. (16) usa `f=f_Kerr exp(df)` e `gamma=gamma_Kerr exp(dg)`. As '+link('linhas 3726–3728',paper_rel,3726)+' declaram priors planos U(−0,8;0,8), estendidos quando necessário. As '+link('linhas 3938–3944',paper_rel,3938)+' identificam explicitamente o teste de desvios do **221**. Texto primário efetivamente lido nessas passagens; não alego leitura integral do artigo. Numeração por quebras LF, não por form feeds de página.\n')
    t.append('Os priors de deformação efetivamente configurados são:\n\n| Produtos | df220 / dg220 físicos | df221 logarítmico | dg221 logarítmico |\n|---|---|---|---|\n| Kerr, 297 NC | fixos em 0; coordenadas de desvio ausentes | fixo/ausente | fixo/ausente |\n| S240621dy, evento, broaddfdg, 11 NC | ambos fixos em 0 | U(−0,8;1,1) | U(−2;0,8) |\n| S240621dy, injeção zero, 11 NC | ambos fixos em 0 | U(−0,8;0,8) | U(−0,8;0,8) |\n| S240621dy, noise0 e noise6, 22 NC | ambos fixos em 0 | U(−0,8;0,8) | U(−0,8;0,8) |\n')
    t.append('A forma plana vem da declaração do artigo; os limites acima vêm dos configs lidos. Para a injeção: '+link('config:7–10',injection['config_path'],7)+'. Massa é declarada plana no artigo e seus limites por evento estão na tabela de modelos JSON. Os configs não explicitam os limites numéricos do prior de spin; não os inferi de defaults de biblioteca nem certifiquei um contrato completo de priors de nuisance. Esse desconhecimento é secundário à ausência comprovada de suporte livre no 220.\n')
    t.append('[DERIVED] Converter os parâmetros logarítmicos em desvios fracionários daria `delta_f=exp(df)−1` e `delta_tau=exp(−dg)−1`, não `delta_tau=dg` nem `−dg` exatamente. Um prior uniforme em df,dg induz densidade proporcional a `1/[(1+delta_f)(1+delta_tau)]` no suporte transformado; não vira automaticamente o prior uniforme fracionário usado no código C4. Isso diz respeito ao **221 disponível**, não cria um 220 livre.\n')
    t.append('## Por que a rotina existente não pode receber esses RD\n')
    t.append('A rotina '+link('posterior_220_readout.py:3–7',code_paths[1],3)+' define a razão de densidades `p(df220,dtau220−g(chi)|d)(0,0) / p(df220,dtau220|d)(0,0)`, sob priors de deformação uniformes independentes e compatibilidade dos priors restantes. A função '+link('uniform_prior:25–44',code_paths[1],25)+' exige esse contrato; '+link('catalog_220_readout.py:57–75',code_paths[0],57)+' lê `domega220`, `dtau220` e parâmetros conjuntos do remanescente. A transformação cisalhante tem Jacobiano um nesse espaço, mas isso pressupõe que tal posterior livre exista. Esses fontes foram lidos, não importados ou executados.\n')
    t.append('O RD fornece um posterior restrito ao 220 Kerr e, em 44 casos, uma extensão em **outras coordenadas modais**. Uma KDE sobre zeros físicos teria covariância singular; adicionar jitter ou aproveitar `*_unit` criaria suporte artificial. Avaliar a curva sobre o posterior Kerr de massa/spin tampouco recupera a verossimilhança fora da superfície Kerr. Não há argumento para atribuir ln B=0 ou −∞ aos ramos de efeito não nulo com esses produtos.\n')
    t.append('“Priors comuns” significa priors compatíveis entre as duas hipóteses comparadas no mesmo modelo amplo; não exige que todo método público tenha priors numericamente idênticos aos do pSEOB. Um outro posterior poderia permitir correção explícita de priors/Jacobianos. Aqui essa correção não resolve a direção 220 que não foi amostrada. Uma reparametrização não trivial que reancorasse massa/spin em outro modo exigiria nova demonstração de bijeção, suporte, priors induzidos e hipóteses de modos superiores; não foi construída nem autorizada como reutilização direta do MESMO estimador.\n')
    t.append('Para um produto futuro ser diretamente utilizável, seriam necessários draws conjuntos de desvios **físicos** livres do 220 e parâmetros do remanescente; significado, suporte e densidade dos priors; compatibilidade de nuisance/modos superiores entre curva e GR; convenções de pesos e início de janela. Nenhum caminho/field/prior desse tipo foi encontrado neste RD. **Lista de posteriores livre220 utilizáveis: vazia.**\n')
    t.append('## Tabela completa de modelos e regimes\n\nCada linha representa uma família com 11 NC e 12 configs, cobrindo a varredura de início registrada. O link aponta ao config mestre lido, linha 1. Todos mantêm o 220 Kerr. “Evento” é o identificador do pacote, sem inventar novas observações para cada janela.\n\n| Evento | Regime | Modelo/config | NC | Desvios livres físicos |\n|---|---|---|---:|---|')
    for r in families:
        regime={'OBSERVED_EVENT':'evento','ZERO_NOISE_INJECTION':'injeção zero','NOISE_noise0':'injeção noise0','NOISE_noise6':'injeção noise6'}[r['regime']]
        t.append('| '+r['event']+' | '+regime+' | '+link(r['model_short'],r['config_path'],1)+' | '+str(r['result_count'])+' | '+('221' if r['physical_free_modes'] else 'nenhum')+' |')
    t.append('\n## Custódia e alcance da decisão F2\n')
    t.append('A '+link('ORDEM_013BIS:85',order_rel,85)+' pede o mesmo ln B no RD **ou justificativa por escrito**, sem multiplicá-lo ao pSEOB. A ausência de posterior livre220 é uma justificativa concreta de não execução direta. O pedido de inspeção/aplicabilidade está cumprido; o resultado científico de robustez não foi produzido. Não substitui a conclusão dos outros itens F2, o marco formal de entrega ou a decisão da gerência.\n')
    t.append('| Fonte/recibo | SHA-256 calculado |\n|---|---|')
    t.append('| RD.tar.gz, '+str(inventory['archive']['bytes'])+' bytes | `'+inventory['archive']['sha256']+'` |')
    for r in sources:
        if r['path'].endswith('write_review.py'):continue
        t.append('| '+r['path']+' | `'+r['sha256']+'` |')
    t.append('| NC exemplar com desvios 221 | `'+example['sha256']+'` |')
    t.append('| Parecer JSON completo | `'+digest(json_path)+'` |')
    t.append('\nOs hashes de todos os 714 produtos estão no JSON e no inventário; o JSON inclui todos os caminhos de resultados, campos e limites por modelo. Os insumos com barras Windows foram normalizados para leitura no WSL, com verificação de confinamento na raiz autorizada. Leitura de HDF5 em modo `r`, sem interpretação de pickle. Nenhum código do tar foi executado e nenhum script de produção alterado. A varredura de metadados e hashes levou aproximadamente 217,53 s; não foi inferência ou grande rerun.\n')
    t.append('Não lidos: valores dos datasets de strain, posteriores primários pSEOB para refazer análises, corpos dos scripts/lock/figuras omitidos da extração, defaults internos do pacote ringdown ou artigo completo. Os valores numéricos lidos dos NC foram somente coordenadas de modos e campos de desvios/auxiliares relevantes; os demais datasets foram inspecionados por nome, forma e dtype. O HDF5 de injeção do outro tar (17018009) não foi usado para alegar disponibilidade em RD. Sem consulta web: a fonte primária local bastou para identificar as convenções.\n')
    t.append('Reprodução da inspeção (recusa sobrescrever o inventário já existente):\n\n```powershell\nwsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/inspect_rd.py"\n```\n')
    t.append('Arquivos escritos nesta revisão, somente estes:\n')
    t.extend(str(i)+'. `'+p+'`' for i,p in enumerate(output['files_written'],1))
    t.append('\nRaiz B: `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`. Temporários exclusivos foram substituídos por seus destinos; nenhuma escrita em dados, código de produção, C2, memória ou canônico. Axiomas N/A; nenhum gate ou veredito físico alterado.\n')
    new(ROOT/'bis/F2_RD_APPLICABILITY_REVIEW.md','\n'.join(t))
    print(json.dumps(dict(status=output['status'],counts=counts,json_sha256=digest(json_path),
        markdown_sha256=digest(ROOT/'bis/F2_RD_APPLICABILITY_REVIEW.md')),indent=2))

if __name__=='__main__':main()
