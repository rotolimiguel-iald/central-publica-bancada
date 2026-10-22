# Parecer crítico independente — montagem e selagem E2

[REAL] **Montagem do candidato permitida como preparação; selagem/ativação não aprovadas.** Veredito: REQUEST_CHANGES_BEFORE_SEALING. Captura final 2026-09-22T21:05:36.776821+00:00. [INPUT — atualização do operador nesta rodada] O GO já existente autoriza a execução pelo principal após revisão. Não há exigência de nova confirmação humana para E2. Este parecer verifica condições técnicas desse GO; não executa produção.

[INPUT] Escopo restrito por ordem final: bloqueantes críticos de sealer/integridade; sem expansão da revisão científica E7. F1/F2 da E7 v3 estão corrigidos conforme [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V3.md>). A ressalva adicional de data futura ali documentada não reabre F1/F2 nem impede a montagem de candidato; a cronologia do recibo concreto precisa ser conferida antes de uso operacional.

[REAL] Revisão exclusivamente estática destes scripts: leitura e ast.parse, sem importar/executar assembler, selador ou ferramentas de produção; sem gerar/ler/hashear seed privada, abrir HDF/posterior/strain, executar extrator, PE ou campanha. A autorização de controles finitos E7 foi usada separadamente e descrita no parecer E7; nenhuma repetição adicional de matemática foi feita após a última instrução de escopo.

[REAL] O assembler já referencia E2_INCLUDE_FINAL_v3 nas linhas 27 e 49; o pin da guarda será atualizado na montagem após A final, conforme ordem. Não exijo pin v2 obsoleto. O selador manteve seus bytes. A guarda foi relida após atualização: acrescentou astropy/pandas à conferência de runtime, mas não um gate de recibo final/autorização. Nenhuma produção foi alterada pelo revisor.

## Quatro bloqueantes de selagem

### C1 — P1: três hashes não demonstram cobertura e conclusão das revisões

Evidência: [refeito/seal_e2_013bis.py:29](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:29>), linhas 29–32 e 44–49; [refeito/seal_e2_013bis.py:66](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:66>), linhas 66–69 e 83–85.

[REAL] A CLI exige `--finalize-reviewed-candidate`; cada revisão precisa apenas ter caminho sob bis e extensão .json/.md. O mapa deduplica caminhos, calcula SHA256 e exige `len(reviews)>=3`. Não lê o conteúdo, não identifica os papéis PE/main/E7, não verifica conclusão, pendências impeditivas, autoria independente ou candidato/árvores efetivamente revisados. Três documentos diferentes com a mesma conclusão negativa, ou três versões da revisão de um só papel, satisfazem o critério de contagem. Até o parecer E7 que pede correções pode ser contado como se fosse aprovação.

[REAL] O switch é uma intenção de quem invoca o script. O GO existente do operador já autoriza o principal após revisão; o programa não vincula essa condição ao conjunto concreto de revisões. O texto gerado diz **“A nota autoriza as execuções previstas”**. Não há entrada que ligue essa concessão ao candidato concreto e às revisões finais aceitas pelo operador. O caminho autorizado e o registro podem permanecer idênticos enquanto o conteúdo do candidato muda antes de chamar o selador.

[DERIVED] A barreira atual permite selar sem demonstrar a condição do GO: revisão pertinente do candidato com tratamento dos impedimentos. Não falta um novo GO humano, e não se pede outro. Isso não prova execução indevida já ocorrida.

Correção requerida: manifesto de revisão estrito com ao menos os três papéis exigidos, arquivos/pins, conclusões e vínculo com o candidato e dependências exatos; revisões parciais devem declarar o conjunto de pins que cobrem, e o fechamento deve conferir a união necessária. Identificação de independência continua [DECLARADO] quando não verificada fora do manifesto; hash não prova identidade humana. Registrar a referência ao GO existente e vincular sua aplicação ao hash do candidato, ao selador e ao conjunto de pareceres após conferir a condição de revisão. Isso é registro técnico pelo principal, não nova confirmação humana; a data do GO pode anteceder as revisões porque sua autorização é condicional. Preservar achados históricos, sem contar versões antigas como novos papéis.

Critério finito de fechamento: três arquivos arbitrários; três versões do mesmo papel; E7 REQUEST_CHANGES; revisão de candidato anterior; aplicação do GO a candidato diferente do revisado. Todos devem recusar antes de criar seed.

### C2 — P1: destinos de seed e witness não são confinados nem separados

Evidência: [refeito/seal_e2_013bis.py:50](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:50>), linhas 50–60; comparação com [bis/e2_code/registration_guard.py:26](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py:26>) e [bis/e2_code/registration_guard.py:114](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py:114>).

[REAL] O candidato, as raízes extras e os pins têm verificação de contenção. Porém `note=R/reg['witness_relative_to_Chatgpt']` e `seedpath=R/reg['blinding']['seed_relative_to_Chatgpt']` não passam por resolve/contenção, destino esperado ou teste de distinção. O budget também é aberto pelo caminho declarado sem a validação local correspondente. O preflight só verifica existência de cada destino e de .pending.

[DERIVED] Um candidato com path absoluto, `..`, alias por link/junction ou destinos coincidentes pode escrever fora da área prevista ou colocar bytes privados em área pública. Em particular, seedpath igual ao witnesspath, ambos inicialmente ausentes, passa pelo preflight: escreve a seed no destino da nota, publica o registro, e só falha quando tenta publicar a nota sobre o mesmo caminho. Não precisei ler/gerar seed para reconhecer esse fluxo.

Correção requerida: validar todos os caminhos e pais resolvidos **antes de qualquer escrita**; witness somente no destino aprovado de DO_CHATGPT, seed somente no diretório privado designado, budget no destino registrado; todos os destinos finais e temporários distintos. Recusar links/reparse points inesperados conforme a plataforma e verificar containment contra raiz resolvida. Preferir nomes fixos aprovados para estes destinos críticos.

Critério finito de fechamento: path absoluto externo, traversal, pai redirecionado, seed=witness, seed=registro/recibo/ficha e colisões envolvendo .pending. Recusa anterior a qualquer geração aleatória.

Proteção inicial da seed — parte do mesmo bloqueante C2

Evidência: [refeito/seal_e2_013bis.py:14](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:14>), linhas 14–20 e 59–62.

[REAL] A seed usa o helper genérico: abre .pending com `open('xb')`, escreve, faz fsync, publica hard link, remove .pending; **depois** aplica `chmod(seedpath,0o600)`. O script não exige ambiente POSIX, diretório privado verificado, modo de criação restritivo nem validação efetiva de ACL/permissões. O temporário e o destino podem existir antes da tentativa de restrição. Falha no chmod deixa bytes já publicados.

[OPEN] As permissões efetivas dos diretórios não foram medidas nesta revisão. Não afirmo que alguém tenha lido a seed, nem que o host esteja exposto. O ponto verificável é que a proteção não é garantida pelo fluxo de criação.

Correção requerida: primitive específica para segredo, com criação exclusiva e restrição desde o primeiro descritor; diretório privado previamente validado; proteção compatível com a plataforma autorizada, conferida antes da publicação; falha visível antes de ativação. Não enviar seed para logs nem incluir seus bytes em snapshots/revisões. Uma recusa após geração deve preservar evidência do estado parcial, sem regeneração silenciosa para “tentar de novo”.

Critério finito de fechamento, só com bytes fictícios: falha de permissão, ambiente incompatível e falha de publicação. Nenhum ensaio com seed real nesta revisão.

### C3 — P1: publicação parcial pode deixar autorização utilizável sem recibo de conclusão

Evidência: [refeito/seal_e2_013bis.py:70](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:70>), linhas 70–119; [bis/e2_code/registration_guard.py:31](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py:31>), linhas 31–67; [bis/e2_code/null_campaign.py:9](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/null_campaign.py:9>) e [bis/e2_code/run_controlled.py:39](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/run_controlled.py:39>).

[REAL] A ordem de efeitos é seed → registro com status ativo → ficha → witness → recibo. O helper protege a publicação individual, não a transação inteira. A guarda verifica o registro, witness, código, inputs, runtime e prazo, mas **não exige E2_REGISTRATION_RECEIPT.json**, nem confere seu hash de witness, nem verifica a autorização final do operador ou os arquivos de revisão. null_campaign/run_controlled começam por essa guarda.

[DERIVED] Se registro e witness já foram publicados e a escrita do recibo falha, esses dois artefatos podem passar na guarda, satisfeitas as demais condições. Também existe intervalo entre witness e recibo. O status do recibo não é, hoje, o marcador obrigatório que torna a selagem completa. Se a falha ocorrer antes do witness, a guarda recusa por ausência da nota; essa parte é fail-closed, mas deixa arquivos parciais que impedem reexecução sem tratamento explícito.

Correção requerida: separar “registro preparado” de “ativação completa”; fazer a guarda exigir um marcador final imutável que vincule registro, witness, revisões, autorização e selador. Evitar ciclo de hashes: um manifesto final pode apontar para artefatos já congelados, e a guarda deve exigir esse manifesto. Rechecar prazo e integridade no momento de ativação. Testemunha é documento no mesmo host: hash/mtime/cronologia local não demonstram custódia humana independente.

Critério finito de fechamento: falha em cada publicação; ausência/alteração do recibo final ou witness; prazo vencido durante a montagem. Nenhum runner deve ser admitido com estado parcial. Não apagar/remendar silenciosamente uma tentativa.

### C4 — P2: hashes tardios podem atribuir bytes diferentes dos consumidos

Evidência: [refeito/assemble_e2_review_candidate_013bis.py:25](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/assemble_e2_review_candidate_013bis.py:25>), linhas 25–28 e 47–49; [refeito/seal_e2_013bis.py:35](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:35>), linhas 35 e 67–68, 110 e 117.

[REAL] Ambos carregam JSON numa leitura e calculam seu hash depois, abrindo o arquivo novamente. No selador, a proveniência, a nota e o recibo recalculam o hash do candidato em momentos diferentes. Na montagem, o mesmo padrão ocorre com draft e fragmento E7. As funções de árvore fazem parse do texto e depois hash em outra leitura. Não há confirmação final de que as fontes permaneceram iguais durante a operação.

[DERIVED] Durante trabalho concorrente — contexto efetivo desta revisão — bytes A podem ser consumidos enquanto o hash B é registrado. O registro final ainda tem seu próprio hash, mas a atribuição ao candidato aprovado fica incorreta. Um arquivo alterado entre a verificação de árvore e a publicação poderá ser recusado mais tarde pela guarda; isso não conserta a proveniência escrita.

Correção requerida: ler cada entrada uma vez em bytes, calcular SHA256 desses mesmos bytes e fazer parsing deles; capturar snapshot lógico consistente das árvores; exigir expected_candidate_sha256 da autorização e reutilizar o digest capturado em todos os artefatos. Verificar estabilidade novamente antes de ativar, sem substituir o snapshot autorizado por um novo. O mesmo vale para revisão, abertura, fragmento e manifesto.

Critério finito de fechamento: mudança entre leitura/hash ou durante composição deve recusar, nunca registrar o hash novo como se fosse o conteúdo aprovado.

Declarações de exposição/execução — parte do bloqueante de proveniência C4

Evidência: [refeito/seal_e2_013bis.py:62](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py:62>), linhas 62–69, 71–75, 83–105 e 114.

[REAL] O script atribui incondicionalmente `new_test_posterior_access_before_registration=False`, “Different builder and reviewer”, `NOT_UNBLINDED` e `E2_REGISTERED_WITNESSED_NO_SCIENCE_RUN_YET`. Não consulta uma declaração de exposição ou inventário de execução. A nota também fixa em texto “quatro” holds, “nove” exclusões, “dez” leituras, janela 16 s e verificação dos cantos dos priors; esses enunciados não são todos derivados/validados a partir do candidato e dos recibos pertinentes.

[DERIVED] O programa pode sustentar “este selador não executa campanha/PE” por seu fluxo; não consegue por isso provar “nenhuma campanha foi executada antes”, “nenhum acesso anterior aconteceu” ou “a revisão é independente”. O `False` automático pode apagar incerteza ou exposição incidental. O censo documenta exposição e ausência apenas no escopo; isso deve permanecer preservado.

Correção requerida: separar `executed_by_this_sealing_step=False` de história da campanha, que exige inventário/recibos ou fica [DECLARADO]/[OPEN]; vincular declaração humana de exposição ao hash, escopo de eventos e instante, com UNKNOWN quando não atestada. Não fazer a contagem de arquivos provar independência. Gerar contagens e parâmetros do candidato e ligar alegações de testes aos respectivos recibos; não elevar metadado a evidência de execução.

[REAL] Há salvaguardas textuais corretas a manter: cabeçalho NÃO-CEGO; campanhas/teste físico NÃO PAGOS; ausência documental não universal; exposição incidental preservada; sem custodiante humano independente; alvos E0 não garantem poder depois de nuisance; sem significância física com gate vermelho. A nota não relata campanha como executada. O defeito é a combinação de ressalvas corretas com campos históricos absolutos não verificados.


## Limite do parecer e condição de fechamento

[REAL] As recusas por arquivo existente, AST inválida, pin/árvore divergente e status diferente de draft são salvaguardas existentes. A publicação individual usa temporário, fsync, verificação de tamanho e hard link exclusivo. O defeito C3 é a conclusão da transação como um todo. O budget é pinado pelo builder; não alego ausência total desse pin. Nenhuma alegação de execução indevida já ocorrida é feita.

[OPEN] Para selar: vínculo verificável das três revisões mínimas com o candidato e aplicação documentada do GO existente; destinos e criação privada da seed validados antes de escrever; marcador final obrigatório pela guarda; proveniência baseada nos bytes consumidos, com exposições/campanhas tipadas como evidência ou declaração. A revisão não concede autorização para corrigir/escrever produção. Correções cabem ao responsável; o fechamento posterior deve ser focado nestes pontos, sem refazer matemática já aprovada.

[INPUT] Preservar NÃO-CEGO no desenho, cegueira procedural no mesmo host e exposição incidental do censo. Preparação não é campanha executada. NOT_FALSIFIED nunca CONFIRMED. Forecast e fórmulas não mudam estatuto ou gate por este parecer.

## Pins medidos

[REAL] Sete fontes analisadas sintaticamente a partir dos mesmos bytes cujo SHA256 foi calculado. Parse não equivale a teste funcional. Os hashes delimitam esta revisão, não versões futuras.

| Fonte relativa a ORDEM_013_RINGDOWN | Bytes | SHA256 |
|---|---:|---|
| `refeito/seal_e2_013bis.py` | 9655 | `381cf5905081aec32cd75d2ebc1ce851d90c907adaa19bceee137c1bbd5dcf5a` |
| `refeito/assemble_e2_review_candidate_013bis.py` | 3654 | `aaa28ee73591aa6a7168ff4e9e301dbea51f404bab5d25e88add541445121b73` |
| `refeito/prepare_e2_design_013bis.py` | 14750 | `a39c8e6a33bbe0431b23eeae2e62eb40b31f6b80c734ed403dca4245c1a78321` |
| `bis/e2_code/registration_guard.py` | 12537 | `9576db51615627c1264ef51ba228c47a12f162c6c62f68b939306135e1ae3743` |
| `bis/e2_code/blinding.py` | 3121 | `7d4407fde07c66929651b017501873ecd4bd69ca80fd3e6cd03eaf8e653c6bc5` |
| `bis/e2_code/null_campaign.py` | 3269 | `9fa748e79ba55312543220542f4e470b8759360cd30040ae7fc1f35bf7859785` |
| `bis/e2_code/run_controlled.py` | 5991 | `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d` |

## Apêndice — texto das fontes-alvo capturadas

[REAL] Hashes referem-se aos bytes originais, não à representação Markdown. Não há seed nem amostras neste apêndice.

### seal_e2_013bis.py

```python
"""Finalize the reviewed E2 candidate and its tunnel witness; never overwrite."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,ast

B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def create(p,value):
    raw=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if p.exists():raise FileExistsError(p)
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Incomplete bytes retained')
    os.link(tmp,p);tmp.unlink()

def code_tree(root):
    found={}
    for p in root.rglob('*.py'):
        ast.parse(p.read_text(encoding='utf-8-sig'));found[p.relative_to(root).as_posix()]=sha(p)
    return found

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True)
    ap.add_argument('--independent-review',action='append',required=True)
    ap.add_argument('--finalize-reviewed-candidate',action='store_true');args=ap.parse_args()
    if not args.finalize_reviewed_candidate:raise ValueError('Explicit finalization required')
    candidate=(B/'bis'/args.candidate).resolve()
    if not candidate.is_relative_to(B/'bis'):raise ValueError('Candidate outside bis')
    reg=json.loads(candidate.read_bytes())
    if reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Not a draft')
    if reg['own_code_tree_sha256']!=code_tree(B/'bis/e2_code'):raise ValueError('Own code changed after review candidate')
    for entry in reg['extra_code_roots']:
        p=(R/entry['relative_to_Chatgpt']).resolve()
        if not p.is_relative_to(R) or code_tree(p)!=entry['files_sha256']:raise ValueError('Extra code changed')
    for name,pin in reg['input_pins_relative_to_Chatgpt'].items():
        p=(R/name).resolve()
        if not p.is_relative_to(R) or sha(p)!=pin:raise ValueError('Input changed '+name)
    reviews={}
    for name in args.independent_review:
        p=(B/name).resolve()
        if not p.is_relative_to(B/'bis') or p.suffix not in ('.json','.md'):raise ValueError('Invalid review path')
        reviews[p.relative_to(B).as_posix()]=sha(p)
    if len(reviews)<3:raise ValueError('PE, main modules, and E7 independent reviews required')
    budget=json.loads((R/reg['budget_relative_to_Chatgpt']).read_bytes())
    now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(budget['hard_deadline_utc']):raise TimeoutError('Budget expired')
    opening=D/'ENTREGA_013BIS_ABERTURA_operador.md'
    final=B/'RINGDOWN_5SIGMA_V1.json';note=R/reg['witness_relative_to_Chatgpt']
    seedpath=R/reg['blinding']['seed_relative_to_Chatgpt'];fiche=B/'REAPROVEITAMENTO_AMPLIACAO_E2.md'
    receipt=B/'bis/E2_REGISTRATION_RECEIPT.json'
    for p in (final,note,seedpath,fiche,receipt):
        if p.exists() or p.with_name(p.name+'.pending').exists():raise FileExistsError(p)
    # Seed bytes remain local and never enter a printed result or tunnel note.
    create(seedpath,os.urandom(32));os.chmod(seedpath,0o600)
    reg['blinding']['seed_commitment_sha256']=sha(seedpath)
    reg['blinding']['status']='PROCEDURAL_SAME_HOST_SEED_COMMITTED_NOT_UNBLINDED'
    reg['status']='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST'
    reg['registered_utc']=now.isoformat()
    reg['e7']['guard_pin_status']='PINNED_AT_FINAL_E2_REGISTRATION'
    reg['independent_review_files_sha256']=reviews
    reg['registration_provenance']={'candidate_sha256':sha(candidate),'sealer_sha256':sha(Path(__file__)),
      'opening_sha256':sha(opening),'not_blind_design':True,'new_test_posterior_access_before_registration':False,
      'independence_scope':'Different builder and reviewer; procedural same-host custody, no independent human seed custodian'}
    create(final,reg);digest=sha(final)
    create(fiche,('[REAL — reaproveitamento E2; desenho NÃO-CEGO, dados novos de teste ainda não lidos]\n\n'
      'Reutilizados E0/E1, metadados públicos, strain arquivado da calibração GW250114, priors e código de runtime instalados; pins integrais no registro. '
      'Preparados código e controles finitos independentes; nenhum posterior novo, PE, waveform física ou nulo de campanha executado nesta selagem. '
      'Os testes de adaptador e conversão são sintéticos e não demonstram viabilidade de PE.\n\n'
      'PAGO: registro, seleção documental, guardas e compromisso de cegueira procedural. NÃO PAGO: campanha nula, piloto, calibração física, seleção normalizada, PE cega, teste e E7 extração. '
      'N/A — sem Lean; nenhum gate formal alterado.\n\n'
      f'Abertura `{sha(opening)}`. Registro `{digest}`.\n').encode())
    lines=['[NÃO-CEGO — E2 registrado; campanhas e teste físico ainda NÃO PAGOS]', '',
      '# E2 — registro testemunhado antes dos dados novos', '',
      f'registro_sha256: {digest}',f'registered_utc: {datetime.now(timezone.utc).isoformat()}', '',
      f'Abertura vinculante `{opening.name}` — SHA256 `{sha(opening)}`.',
      f'Ficha `{fiche.name}` — SHA256 `{sha(fiche)}`.', '',
      'PAGO: desenho, código integral pinado, critérios pré-análise, leituras paralelas, protocolo de cegueira e controles finitos. '
      'NÃO PAGO nesta nota: nulos de campanha, Kerr/piloto IMR, calibração de duas famílias, PE cega, normalização hierárquica e teste físico. '
      'A nota autoriza as execuções previstas; não relata seu resultado.', '',
      f"O censo contém {len(reg['calibration_event_ids'])} identidades de calibração/exclusão de cegueira. "
      f"{sum(x['eligible'] is True and x['published_deformation_at_registration'] is False for x in reg['test_candidates'].values())} eventos elegíveis não foram localizados no escopo documental congelado; quatro têm pendência de qualidade. "
      'Ausência no escopo não é ausência universal de publicação. Nova conferência documental precede cada admissão. '
      'Os nove publicados fora do antigo corpus permanecem excluídos da rota cega; a exposição incidental descrita no censo fica preservada.', '',
      'Os alvos E0 não garantem 90% de poder após incorporar nuisance. A matriz E1 entra apenas como INPUT sintético. '
      'O registro conserva as dez leituras, nenhuma escolhida, e proíbe offset fixo em zero como estatística de teste. '
      'Com gate sistemático vermelho não se declara significância física nem se combina eventos para uma descoberta.', '',
      f"Nulos: {len(reg['nulls']['cells'])} células pré-fixadas, {sum(x['draws'] for x in reg['nulls']['cells'].values()):,} desenhos sintéticos no total. "
      'Gaussianos e cauda t5 de medida com nuisance gaussiano têm interpretações distintas; os limites empíricos de resolução são reportados. '
      'Não equivalem a calibração física da pipeline.', '',
      'Piloto GW250114: janela 16 s, fonte IMR e quatro deformações livres, priors INPUT; Kerr220/10M precede a execução IMR. '
      'A família alinhada pSEOBNRv4HM_PA difere do produto publicado precessante v5PHM. '
      'O limite temporal foi verificado nos cantos dos priors; o interior não é certificado por esse teste. '
      'Remanescente usa fit GR nomeado e redshift usa Planck18 externo INPUT; não são observáveis independentes.', '',
      'Cegueira procedural no mesmo computador: somente o compromisso SHA256 da seed fica no registro; logs e intermediários sem deslocamento permanecem privados. '
      'Não há custódia humana independente. Descegamento exige informação suficiente, gate sistemático verde e revisão vinculada ao conjunto.', '',
      f"Prazo rígido contínuo: `{budget['hard_deadline_utc']}`. E3.2 fixará alocação adicional com custo medido do piloto e testemunha própria antes de novos jobs. "
      'Nenhuma autorização para ultrapassar 40 h. Catálogos futuros: AWAITING_DATA.', '',
      'Tentativas e correções anteriores permanecem nas revisões: adaptador inicialmente rejeitado, janela de 8 s insuficiente, guardas de downloads, publicação, qualidade e payload reforçadas. '
      'Nenhuma dessas correções é resultado físico. N/A — sem Lean.', '',
      'Comandos previstos (WSL /opt/lal_env, dentro do prazo): `python -B bis/e2_code/null_campaign.py`; '
      '`python -B -O bis/e4_e5_prepare/deterministic_e4_e5.py --execute --authorization <ativação pinada>`; '
      '`python -B bis/e2_code/run_controlled.py --job GW250114_PILOT` somente após E3.1/Kerr e encerramento F0. '
      'Saídas existentes são recusadas. Reprodução exige destino isolado e novo registro explícito, não sobrescrita.', '',
      '## Revisões e código', '',f'- Registro — `{digest}`.',f'- Candidato — `{sha(candidate)}`.']
    lines.extend(f'- `{n}` — `{pin}`.' for n,pin in reviews.items())
    lines.extend(f'- `bis/e2_code/{n}` — `{pin}`.' for n,pin in reg['own_code_tree_sha256'].items())
    create(note,('\n'.join(lines)+'\n').encode())
    value={'status':'E2_REGISTERED_WITNESSED_NO_SCIENCE_RUN_YET','registration_sha256':digest,
      'witness_sha256':sha(note),'opening_sha256':sha(opening),'fiche_sha256':sha(fiche),
      'seed_commitment_sha256':reg['blinding']['seed_commitment_sha256'],
      'candidate_sha256':sha(candidate),'sealer_sha256':sha(Path(__file__)),
      'finished_utc':datetime.now(timezone.utc).isoformat()}
    create(receipt,value);print(json.dumps(value))

if __name__=='__main__':main()
```

### assemble_e2_review_candidate_013bis.py

```python
"""Merge reviewed packages into a candidate; no seed or registration created."""
from pathlib import Path
import argparse,json,hashlib,ast
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1];R=B.parent

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()
def read(p):return json.loads(p.read_bytes())
def tree(root):
    result={}
    for p in sorted(root.rglob('*.py')):
        ast.parse(p.read_text(encoding='utf-8-sig'));result[p.relative_to(root).as_posix()]=sha(p)
    if not result:raise ValueError('Empty code tree')
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',required=True);parser.add_argument('--tag',required=True);args=parser.parse_args()
    if not args.tag.isalnum():raise ValueError('Alphanumeric tag')
    draft=(B/'bis'/args.draft).resolve()
    if not draft.is_relative_to(B/'bis'):raise ValueError('Invalid draft path')
    reg=read(draft)
    if reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Not a draft')
    fragment=read(B/'bis/e7_prepare/E2_INCLUDE_FINAL_v3.json')
    reg['e7']=fragment['e7'];reg['e7']['guard_sha256']=sha(B/'bis/e2_code/registration_guard.py')
    reg['e7']['guard_pin_status']='READ_FROM_CURRENT_REVIEW_CANDIDATE__NOT_YET_REGISTERED'
    for n,pin in fragment['input_pins_relative_to_Chatgpt'].items():
        if sha(R/n)!=pin:raise ValueError('E7 input changed '+n)
        if n in reg['input_pins_relative_to_Chatgpt'] and reg['input_pins_relative_to_Chatgpt'][n]!=pin:raise ValueError('Conflicting input pin')
        reg['input_pins_relative_to_Chatgpt'][n]=pin
    reg.pop('extra_code_trees',None)
    reg['own_code_tree_sha256']=tree(B/'bis/e2_code')
    roots=['ORDEM_013_RINGDOWN/bis/e7_prepare/producer','ORDEM_013_RINGDOWN/bis/e4_e5_prepare']
    reg['extra_code_roots']=[{'relative_to_Chatgpt':root,'files_sha256':tree(R/root)} for root in roots]
    e4=B/'bis/e4_e5_prepare'
    package={n:sha(e4/n) for n in ['PLAN.json','INPUT_MANIFEST.json','SCHEMA.json','deterministic_e4_e5.py']}
    reg['e4_e5_preparation_pins']=package
    for n in package:reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/bis/e4_e5_prepare/'+n]=package[n]
    for item in read(e4/'INPUT_MANIFEST.json')['files']:
        p=(B/item['path']).resolve()
        if not p.is_relative_to(R) or sha(p)!=item['sha256']:raise ValueError('E4 input changed')
        n=p.relative_to(R).as_posix();reg['input_pins_relative_to_Chatgpt'][n]=item['sha256']
    reg['registration_id']='RINGDOWN_5SIGMA_V1_013BIS'
    reg['review_candidate_provenance']={'draft':draft.relative_to(B).as_posix(),'draft_sha256':sha(draft),
      'assembled_utc':datetime.now(timezone.utc).isoformat(),'assembler_sha256':sha(Path(__file__)),
      'E7_fragment_sha256':sha(B/'bis/e7_prepare/E2_INCLUDE_FINAL_v3.json'),
      'scope':'Code/input snapshot only; no E2 witness, no seed, no execution yet'}
    out=B/'bis'/('E2_REVIEW_CANDIDATE_'+args.tag+'.json')
    with out.open('x',encoding='utf-8') as f:json.dump(reg,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps({'candidate':out.name,'sha256':sha(out),'own_code_files':len(reg['own_code_tree_sha256']),
      'extra_code_files':sum(len(r['files_sha256']) for r in reg['extra_code_roots']),
      'calibration_identities':len(reg['calibration_event_ids']),
      'eligible_absent_in_scoped_census':sum(x['eligible'] is True and x['published_deformation_at_registration'] is False for x in reg['test_candidates'].values())}))

if __name__=='__main__':main()
```

## Atualização de escopo — GO existente e E7 v4

[INPUT] O operador esclareceu que o GO existente autoriza execução pelo principal após revisão, sem nova confirmação para E2. As exigências anteriores de obter nova autorização ficam expressamente superadas; exige-se conferir a condição técnica de revisão, não renovar consentimento. Os quatro pontos críticos acima permanecem avaliações de implementação. [OPEN] Wegener prepara v4 para F3; o próximo fechamento E7 será só da mudança de cronologia e seus pins, preservando a v3 e sem repetir a matemática já aprovada.

