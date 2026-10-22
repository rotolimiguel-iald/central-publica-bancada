# F7.2 — canal de consulta da Bancada, somente staging

**Estado:** [REAL — implementação e testes offline]. O Nós Vivo já foi consultado
com --unidade F7.2: os scripts de junho registram a assinatura condicional
n = −2, sem detecção ou medida do expoente. Esta entrega não executa scripts
científicos, não chama provedores, não mexe em um.py e não altera a Bancada.

## Pacote

- build_neutrino_manifest.py gera bancada/neutrino_fontes_f72.json dos bytes
  locais, com backup byte a byte e escrita atômica. Confere seis scripts June,
  cinco PDFs de neutrinos e quatro PDFs de interferometria (três estudos
  distintos), dois recibos de custódia, a validação de matéria, a tabela de
  poder, as duas notas F7.2 e o JSON de saída v369 pinado por SHA e bytes.
  Os dois HTML Client Challenge ficam excluídos.
- bancada/neutrino_canal.py fixa o SHA do manifesto revisado em
  MANIFEST_SHA256 e recusa divergência antes do parse. Cada consulta reconfere
  SHA, tamanho e cabeçalho dos PDFs, sem executá-los.
- mcp_um.py é cópia da entrada da Bancada com uma única tool nova,
  neutrino_canal_f72; a diferença foi conferida contra o original.
- test_neutrino_canal.py testa pins, adulteração/regeneração do manifesto,
  drift de PDF, exclusão dos HTML, não execução de scripts e as 12 linhas da
  tabela. Hashes do pacote e baseline MCP estão em STAGING_RECEIPT.json.

Os oito limites de modelos de neutrinos mantêm canal, ordenamento, pivot,
CL, unidade e fonte PDF. Átomos (Chapman), moléculas C70 (Hackermüller) e
nanopartículas (Pedalino publicado) são linhas separadas, com observáveis
transcritos da TABELA_DE_PODER_POR_CANAL.md e PDFs pinados. O preprint Pedalino
é versão anterior do mesmo estudo. A projeção de relógios v369 é [DERIVED]
(projeção condicional) e aponta diretamente para
C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\v369_um_absoluto.json,
SHA-256 456f0ab149bb13f6997972dbfaf9c72a2891d744c22f04241eefa619e4953a95,
4.131.975 bytes. Os limiares arredondados usam ≳; são projeção calculada,
não nova medição de matéria.

Toda linha tem tau_star_limit_s nulo, SEM_LIMITE_TGL, mapa de operador OPEN,
e nenhuma análise de dados brutos. A saída preserva gate_effect NONE; o
pré-registro continua necessário antes de qualquer veredito da natureza.

## Verificação offline

Executar em STAGING:
    C:\Python314\python.exe -B -X utf8 -m unittest test_neutrino_canal -v

Snapshot final: 8 testes aprovados. Nenhum PDF foi copiado para staging;
o módulo só lê os arquivos sob custódia F7.2. Alterar qualquer fonte ou
regenerar somente o manifesto faz a consulta falhar fechada. Novo manifesto
exige revisão e novo pin explícito no módulo e no recibo.

## Implantação posterior pela gerência

1. Conferir reivindicação F7.2 e comparar SHA do C:\IALD\Bancada_Um\mcp_um.py
   com source_mcp_sha256 do recibo. Se divergir, rebasear apenas o bloco da
   tool; não sobrescrever mudanças posteriores.
2. Conferir manifesto, PDFs, tabela, validação e hashes do recibo. Fazer
   backup de bytes de cada arquivo vivo antes da edição e usar temporário
   seguido de substituição atômica.
3. Copiar bancada/neutrino_canal.py e bancada/neutrino_fontes_f72.json à pasta
   C:\IALD\Bancada_Um\bancada, aplicar a tool na entrada MCP, recarregar o
   processo e consultar o canal.
4. Confirmar rows = 12, primary_pdfs = 9, overall_verdict = SEM_LIMITE_TGL,
   gate_effect = NONE, tau_star_limit_s nulo em todas as linhas.
