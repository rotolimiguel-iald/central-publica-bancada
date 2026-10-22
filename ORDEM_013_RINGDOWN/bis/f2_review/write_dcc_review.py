"""Document text-only DCC applicability, with binary posterior content unread."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(path,text):
    if path.exists():raise FileExistsError(path)
    raw=text.encode();tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw
    tmp.replace(path)
def link(name,rel,line):return '['+name+'](<'+(ROOT/rel).as_posix()+':'+str(line)+'>)'

def main():
    inventory=OUT/'dcc_text_inventory.json';d=json.loads(inventory.read_bytes())
    archive=ROOT/d['archive']['path'].replace('\\','/')
    assert sha(archive)==d['archive']['sha256']
    p='bis/f2_review/dcc_text/pSEOB/'
    sources=[dict(path=r['path'],sha256=r['sha256'],member=r['member']) for r in d['text_sources']]
    sources += [dict(path=r['source_only_path'],sha256=r['source_only_sha256']) for r in d['text_sources'] if 'source_only_path' in r]
    for r in sources:assert sha(ROOT/r['path'].replace('\\','/'))==r['sha256']
    for rel in ['cache/public/DCC_P2600130_v1/release.html','bis/F2_GWTC4_RELEASE_SEARCH.json','bis/f2_review/dcc_text_inventory.json']:
        sources.append(dict(path=rel,sha256=sha(ROOT/rel)))
    report=dict(status='RELEASE_LOCATED__SAME_SPIN_DEPENDENT_LNB_NOT_SUPPORTED_BY_TEXT_INSPECTED_PACKAGE',
        release_located=True,correction='Replace not located by DCC P2600130-v1 located; usability separately unverified',
        archive=d['archive'],run_same_lnB=False,lnB=None,joint_df_dtau_spin_per_event_verified=False,
        binary_posterior_values_read=False,pickles_deserialized=False,archive_code_executed=False,
        sources=sources,
        exact_external_route=dict(filename_template='pSEOB_{event_map[event]}_Prod0.h5',
            group_referenced='pSEOBNRv5PHM-reweighted',fields_referenced=['domega220','dtau220'],
            file_location='Associated Zenodo release named by README, not identified or downloaded in this task',
            remnant_spin_mass_fields='Not established by these notebook excerpts',
            prior_bounds_notebook=dict(default=[-.8,2.],exceptions={'S191109d':[-.8,4.],'S200208q':[-.8,4.]}),
            prior_density_and_joint_contract_verified=False),
        distinctions=['joint directory is combined-catalog material, not a per-event posterior with remnant spin',
            'Notebook pairs the separate df and dtau combined columns in a 2D plot; independent marginals must not be presumed',
            'hierarchical NPZ keys describe population means, widths, correlation or population draws, not event spin',
            'Pickle properties and scalar total-mass summaries are not verified joint posterior draws'],
        no_claim=['Does not establish that usable posteriors do not exist elsewhere',
            'HTTP Last-Modified is not certified publication time',
            'No contents of NPZ, PKL or DAT.GZ were inspected'],
        written_files=['bis/f2_review/inspect_dcc_text.py','bis/f2_review/dcc_text_inventory.json',
            'bis/f2_review/write_dcc_review.py','bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.json',
            'bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md']+[r['path'] for r in sources if '/dcc_text/' in r['path'].replace('\\','/')])
    jp=OUT/'GWTC4_DCC_APPLICABILITY_REVIEW.json';new(jp,json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    text='''[REAL — release e textos primários localizados/lidos; DERIVED — aplicabilidade limitada; 22/09/2026] **Corrigir “não localizado”: o release DCC P2600130-v1 existe e foi arquivado. O pacote pSEOBNR examinado não demonstra disponibilidade do posterior conjunto por evento (df220, dtau220, spin) necessário para reutilizar diretamente o mesmo ln B dependente do spin.** Nenhum ln B foi calculado. Ausência de comprovação neste pacote não é inexistência de um release utilizável em outro local.

Esta revisão complementa `bis/F2_RD_APPLICABILITY_REVIEW.md/json`; o RD já foi concluído separadamente. Não foi duplicado trabalho gaussianindependent/freeclock.

## Fonte e cobertura

'''
    text+='A '+link('página DCC arquivada:71','cache/public/DCC_P2600130_v1/release.html',71)+' identifica GWTC-4.0 TGR III. A linha 116 liga o tar pSEOBNR; as linhas 115–119 mostram outros pacotes do release, que **não foram auditados aqui**. URL primária: [DCC P2600130-v1](https://dcc.ligo.org/LIGO-P2600130/public). A licença CC-BY-4.0 é declarada na página:105.\n\n'
    text+='Conferi o SHA-256 do tar de **14.923.249 bytes**, o inventário completo de **49 membros** contra o recibo e extraí somente textos em `bis/f2_review/dcc_text/`. Recusei nomes absolutos, `..` e links; verifiquei confinamento e tamanho. Os três notebooks foram analisados como JSON/texto; suas células fonte foram numeradas em arquivos `.cells.txt`. Nenhuma célula foi executada e seus outputs não foram usados como prova. O utilitário Python foi apenas lido como texto. Não foi feito `pickle.load`, import de código do tar, `np.load` ou leitura de valores `.dat.gz`.\n\n'
    text+='O header HTTP arquivado traz `Last-Modified: Wed, 18 Mar 2026 15:17:05 GMT`. Isso não certifica a data de publicação nem prova retroativamente em que dia o produto ficou disponível. A correção de localização é atual e documental.\n\n'
    text+='## O que dizem README e notebooks\n\n'
    text+='1. '+link('README:3–5',p+'README.md',3)+' caracteriza o material como dados auxiliares/notebooks de figuras e manda obter as amostras individuais no release Zenodo associado. Não fornece nessa linha um identificador Zenodo; esta revisão não o adivinha.\n'
    text+='2. '+link('Notebook principal, células 5–6, linhas 117–135',p+'pSEOBNR_main_figure.cells.txt',117)+' tenta ler `pSEOB_{event_map[event]}_Prod0.h5`, com `pesummary.io.read`, e depois `samples_dict["pSEOBNRv5PHM-reweighted"][param]` para `domega220` e `dtau220`. Esses HDF5 não constam dos 49 membros. O caminho de computador do autor não é um arquivo disponível localmente.\n'
    text+='3. '+link('Linhas 76–92',p+'pSEOBNR_main_figure.cells.txt',76)+' declaram limites [−0,8;2] para ambos os desvios, estendidos a [−0,8;4] em S191109d e S200208q. São limites descritos no notebook, não priors analíticos lidos dos HDF5 nem comprovação de independência dos priors/nuisance. O notebook não identifica campos de spin/massa do remanescente para a curva.\n'
    text+='4. '+link('Linhas 147–158',p+'pSEOBNR_main_figure.cells.txt',147)+' carregam produtos combinados `joint/` e `hierarchical/`. As '+link('linhas 220–249',p+'pSEOBNR_main_figure.cells.txt',220)+' passam as duas colunas combinadas a uma KDE/contorno 2D. Portanto, **não é correto declarar apenas pelo nome dos arquivos que sejam marginais independentes**. O código sugere uso pareado de um produto combinado 2D; o pareamento dos valores não foi conferido. Mesmo se confirmado, falta a dimensão de spin e a correspondência por evento para a curva g(chi).\n'
    text+='5. '+link('Notebook hierárquico:18–31',p+'hierarchical_2D_figure.cells.txt',18)+' referencia `mu_domega_220`, `mu_dtau_220`, `sigma_domega_220`, `sigma_dtau_220`, `rho`; o principal referencia `pop_domega_220` e `pop_dtau_220`. São parâmetros/amostras populacionais segundo o uso documentado, não o spin do remanescente de cada evento. Os campos foram identificados no texto, não verificados dentro dos NPZ.\n'
    text+='6. '+link('Notebook mock:45–55',p+'mock_catalog_figure.cells.txt',45)+' também exige dados externos do Zenodo: Q0 e resultados de 1000 catálogos simulados. Não roda nem fornece a ponte entre os produtos resumidos e os draws conjuntos reais por evento.\n'
    text+='7. '+link('utils_o3b.py:169–203',p+'aux_data/utils_o3b.py',169)+' lê pickles como propriedades auxiliares de catálogos e mapeia nomes como `CHIF→final_spin`. A existência dessa string **não é evidência de posterior conjunto**: os pickles ficaram opacos. O '+link('dict_det_masses.json:1',p+'aux_data/dict_det_masses.json',1)+' guarda números escalares de massa total para cores, conforme o notebook:61–67; não são draws de massa final/spin correlacionados com deformações.\n\n'
    text+='## Matriz de aplicabilidade\n\n| Produto | Evidência textual | Serve ao mesmo ln B por curva em spin? |\n|---|---|---|\n| HDF5 individuais pSEOB_*_Prod0.h5 | Referenciados; ausentes deste tar | Potencial rota futura, não verificada: faltam arquivos, esquema conjunto e priors completos. |\n| joint/*/domega_220_comb.dat.gz e dtau_220_comb.dat.gz | Produtos combinados; notebook usa pares em 2D | Não sustentam a integração por evento com spin. Não separar ou fabricar pareamento. |\n| hierarchical/*/pseob_hier*.npz | Hiperparâmetros/população no texto | Não substituem o posterior por evento da curva determinística. |\n| aux_data/*.pkl | Propriedades auxiliares; conteúdo não lido | Não certificado; não desserializado. |\n| aux_data/dict_det_masses.json | Massas totais escalares para cores | Não contém a distribuição conjunta necessária. |\n| Mock catalogs | Dados externos referenciados | Simulações e resumos não são novos eventos nem ln B dos dados reais. |\n\n'
    text+='O mesmo estimador em `posterior_220_readout.py:3–7,25–53` exige o posterior conjunto livre e correlação com g(chi), além do contrato de priors. Agregar eventos antes da avaliação da curva geralmente perde a informação de qual spin está associado a qual deformação; um resumo 2D não a recria. Não usar uma mediana de spin, a massa escalar de cores ou propriedades pickle não lidas para preencher a lacuna. A inexistência de HDF5 por si só não seria impedimento — outro formato seguro poderia conter os mesmos draws —, mas este README e os fluxos de leitura deixam a dependência externa explícita.\n\n'
    text+='**Disposição F2:** localização PAGA; disponibilidade direta neste pacote do joint df/dtau/spin por evento NÃO DEMONSTRADA; ln B NÃO CALCULADO (`null`). É necessário localizar o Zenodo associado e inspecionar seus dados/priors em tarefa autorizada antes de mudar essa conclusão. Este parecer não afirma que essa rota esteja bloqueada para sempre, nem que o restante do release DCC seja inutilizável.\n\n'
    text+='## Hashes e arquivos escritos\n\n| Fonte | SHA-256 |\n|---|---|\n'
    text+='| pSEOBNR.tar.gz | `'+d['archive']['sha256']+'` |\n'
    for r in sources:text+='| '+r['path']+' | `'+r['sha256']+'` |\n'
    text+='| Parecer JSON | `'+sha(jp)+'` |\n\n'
    text+='Escritos apenas os seguintes arquivos deste complemento:\n\n'
    text+='\n'.join('- `'+r+'`' for r in report['written_files'])
    text+='\n\nRaiz B: `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`. Dados de origem, notebooks no tar e produção permaneceram intactos. Todos os nomes de fields de NPZ citados são referências textuais, não resultados de abertura dos bins. Nenhuma conclusão física, publicação, comunicação externa ou alteração de gate.\n'
    new(OUT/'GWTC4_DCC_APPLICABILITY_REVIEW.md',text)
    print(json.dumps(dict(status=report['status'],json_sha256=sha(jp),md_sha256=sha(OUT/'GWTC4_DCC_APPLICABILITY_REVIEW.md')),indent=2))

if __name__=='__main__':main()
