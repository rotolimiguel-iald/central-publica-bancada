# Diagnóstico estático da falha terminal F9 ffd6

**[REAL — recibos] A unidade falhou na importação, antes de qualquer tentativa do solver.** CASE_RESULT é FAILED_LATCHED; attempted=returned=0; artifacts vazio. Há três recusas de open no journal, idênticas às três entradas do snapshot. Não existe previsão de engenharia aceita nem resultado científico desta unidade. Este diagnóstico não reabre a request ffd6ccba-cd70-4747-aceb-a10003dfb7f4.

**Errata à revisão555:** deixei passar duas lacunas concretas do inventário: a dependência transitiva instalada charset_normalizer, alcançável pela expansão dos nomes públicos de NumPy, e a sonda padrão de caminho ZIP fora das raízes admitidas. O parecer555 era estático e declarava limitações, mas sua conclusão “sem bloqueador concreto” foi insuficiente para esse runtime. As ressalvas não apagam essa omissão. A conclusão de fechamento de dependências não deve ser reutilizada para nova execução sem resolver estes pontos. O parecer anterior permanece intacto como snapshot; a correção fica aqui, ao lado.

Pedido de preparação original f07e4aba-e976-4d78-be1c-449968d4a305; autorização/consumo conduzidos por ROOT556. Consulta de mapa antes do diagnóstico retornou556. ROOT conserva a conferência externa de processos, códigos de saída e cleanup; esta análise se limita ao CASE_RESULT, journal, fontes e metadados.

## Achados acionáveis

1. **P2 — dependência transitiva omitida.** Ambos os arquivos charset_normalizer recusados existem agora por UNC, mas não têm pin nem raiz admitida no inventário consumido. A cobertura dos arquivos internos CAMB/NumPy/SciPy não equivale ao fechamento de imports que esses pacotes acionam. A revisão555 examinou imports de entrada, sysconfig e caches, mas não seguiu a expansão lazy/star de NumPy até F2PY.
2. **P2 — sonda ZIP de runtime não representada.** `/usr/lib/python312.zip` não pertence a `/usr/lib/python3.12/` nem às demais raízes admitidas e não tem pin. O guard o recusa independentemente de estar ausente. A primeira recusa já fixa o latch: mesmo que os demais imports terminassem, o checkpoint seguinte impediria o solver. Não é apenas um log benigno que possa ser ignorado na aceitação.
3. **P3 — origem profunda não conservada no traceback.** `traceback.format_exc(limit=8)[-8000:]` guarda os primeiros oito frames, depois limita caracteres. `_ufuncs.pyx` é o último frame preservado, não prova de ser o chamador direto de charset_normalizer. Para diagnóstico futuro, conservar contagem total e uma combinação limitada de início/fim da cadeia ou frames terminais, sem ampliar a saída sem limite. Não modificar o recibo consumido para preencher os frames ausentes.

## O que aconteceu, com o alcance da prova

CASE_RESULT tem 4180 bytes e SHA256 `1441687af1ccf48c723978fb909db2b08c81e8e3c093f7ce0fa3a3fde7e62a31`. As três recusas aconteceram na fase import_theory_libraries, com contadores de solver zero:

| Ordem | Alvo recusado | Evidência e interpretação |
|---|---|---|
| 1 | /usr/lib/python312.zip | Abertura tentada e bloqueada; latch persistido. O alvo está ausente na consulta atual por UNC. Não se leu conteúdo ZIP. |
| 2 | charset_normalizer/__pycache__/__init__.cpython-312.pyc | Abertura do cache existente sem pin. O loader pode absorver PermissionError porque captura OSError. |
| 3 | charset_normalizer/__init__.py | Abertura seguinte do fonte existente sem pin; PermissionError chega ao tratamento externo. |

[DERIVED — fonte CPython] `_bootstrap_external.py1086–1089` captura OSError na tentativa de ler bytecode; `1127–1128` tenta depois o fonte. Isso explica por que podem existir dois denials para uma única importação. Não foram duas execuções científicas. `-B` impede escrever bytecode; não impede lê-lo.

[REAL] O snapshot está latched=true, journal_error=null, sem checkpoints completados. O fluxo ainda estava dentro de import camb quando saiu por exceção; o guard preservou o primeiro evento e impediu promoção a sucesso. A existência de três denials não demonstra três solvers ou três novas unidades. Zero chamadas de get_background também não significa zero inicializações nativas: bibliotecas podem carregar código nativo durante importação.

## Cadeia da dependência charset_normalizer

[REAL — traceback preservado] O caminho registrado é worker.py148 import camb → camb/__init__.py16 → camb/model.py6 → camb/bbn.py10 (scipy.interpolate) → scipy/interpolate/__init__.py192 → _interpolate.py11 (scipy.special) → scipy/special/__init__.py785 → inicialização compilada scipy.special._ufuncs.

[REAL/DERIVED — fontes pinadas; não um segundo trace dinâmico] O binário `_ufuncs` contém a referência literal `scipy.linalg.cython_lapack`. O inicializador Python de scipy.linalg importa _misc; _misc.py6 importa scipy._lib._util; _util.py16 importa _array_api. Essa é uma ligação estática coerente para a continuação além do corte, mas a sequência dinâmica completa desses frames não foi conservada no recibo. Não a apresento como observada integralmente.

A partir da camada Array API, a ligação textual é explícita:

- scipy/_lib/_array_api.py24–42 importa scipy._external.array_api_compat.numpy.
- Esse __init__.py9 executa `clone_module("numpy", globals())`.
- array_api_compat/_internal.py60–68 importa o módulo e executa `from numpy import *`, seguido de acesso aos nomes públicos.
- NumPy/__init__.py626–630 inclui f2py em __numpy_submodules__;674–692 incorpora esse conjunto em __all__;734–736 implementa o carregamento lazy de numpy.f2py.
- numpy/f2py/__init__.py19 importa f2py2e; f2py2e.py21–30 importa crackfortran.
- crackfortran.py152–155 tenta `import charset_normalizer` e captura somente ImportError. Uma PermissionError da política de leitura não equivale a dependência opcional ausente e não cai nesse fallback.

[REAL] O __init__ instalado de charset_normalizer mede1582bytes e foi lido/hashado somente para este diagnóstico. Ele importa api, legacy, models, utils e version do próprio pacote. Portanto, liberar somente os dois alvos que apareceram no journal não demonstraria fechamento do restante dessa dependência. Isso não autoriza importá-la, habilitá-la ou alterar o inventário nesta unidade.

## Alcance da sonda ZIP

[REAL] O evento registra alvo e fase, mas não stack do próprio open. O caminho está fora das raízes do inventário. A exceção de worker.py para ABSENT_RUNTIME_PROBE_NO_CONTENT só alcança caminhos ausentes dentro dessas raízes; logo não alcança esse ZIP. A consulta atual encontrou o ZIP ausente, enquanto os dois arquivos charset existem. Ausência atual não prova, sozinha, o estado do filesystem no instante passado do evento.

[DERIVED — mecanismo concreto disponível] `importlib.metadata` usa sys.path como padrão de busca; FastPath.children678–683 tenta listdir e, sob suppress(Exception), zip_children. Este cria zipfile.Path(self.root), que abre o caminho como arquivo ZIP. Assim, sondar um caminho ZIP ausente pode causar tentativa de open e ter a PermissionError absorvida pelo mecanismo de busca, enquanto o audit latch continua ligado. O comportamento é compatível com a primeira recusa seguida das outras duas. O zipimport clássico, por sua vez, faz stat antes da leitura; não se deve atribuir automaticamente este evento a ele.

[OPEN] O recibo não preserva o chamador exato do primeiro open nem sys.path completo naquele instante. Não afirmo que importlib.metadata foi, comprovadamente, o chamador único; tampouco que houve arquivo ZIP lido, exfiltração, leitura observacional ou falha física. A causa de recusa é demonstrável sem resolver essa atribuição: o alvo não é pinado nem está nas raízes de sondagem ausente.

## Proposta documental mínima para decisão futura

Estas são alternativas delimitadas, não uma correção aplicada e não autorização de nova execução:

- **Dependência instalada:** preparar um inventário explícito de charset_normalizer e somente de sua cadeia efetivamente necessária, incluindo fontes/cache e eventual componente binário com identidade real. A entrada do pacote mostra que dois arquivos isolados não bastam. Preservar a recusa a qualquer arquivo existente fora da lista; não liberar site-packages inteiro nem substituir o erro por sucesso.
- **Sonda ZIP:** escolher no próximo contrato entre representar esse único caminho como sonda permitida apenas sob ausência verificada ou retirar explicitamente de sys.path o caminho ausente antes da busca de bibliotecas/metadados. A primeira alternativa conserva o caminho padrão e exige distinguir ausência de permissão de leitura de conteúdo; a segunda evita a sonda, mas altera explicitamente a configuração de busca. Se o ZIP existir, seria necessário um pin próprio ou falha visível. Nenhuma alternativa justifica abrir toda a árvore /usr/lib ou absorver genericamente recusas do guard. As limitações cooperativas/stat–open continuam declaradas.
- **Diagnóstico:** manter no futuro a identificação de evento/módulo/caminho/fase e reservar frames de cauda limitados. Isso melhora a evidência de falha sem pretender garantir que a lista estática preveja todo import nativo possível.

Não proponho uma campanha adicional nem executar agora um teste de importação. Cabe à gerente/ROOT decidir se e como preparar uma versão nova que resolva esses pontos; esta request permanece consumida e terminal. Eventual validação futura requer artefatos e identidade próprios, sem edição dos arquivos consumidos ou reaproveitamento da autorização anterior.

## Custódia e ações desta análise

EVIDENCIA_ESTATICA_FFD6.json reúne23 fontes de runtime, seus trechos e hashes calculados;22 têm pins correspondentes no inventário e conferiram, e a entrada charset_normalizer é identificada como fora dele. Há também pins dos recibos consumidos e do parecer555 preservado. A busca dirigida inicial leu803 fontes.py não-testes já inventariados de CAMB/NumPy/SciPy para localizar menções a charset_normalizer/requests; a ocorrência relevante foi crackfortran.py. Isso foi leitura de código, não execução dos pacotes.

O script próprio collect_static_diagnostic.py só faz leitura, hashes, extração de trechos/strings e escrita atômica de evidência nesta pasta. Zero imports candidatos, zero WSL/Linux iniciado, zero solver/controle, zero mudanças na allowlist, AUTORIZAÇÃO, CLAIM, RUN, pacote consumido, memórias compartilhadas ou ledger. Não foi feito novo ajuste, leitura de centros observados ou inferência científica. As leituras UNC dirigidas foram autorizadas como somente leitura.
