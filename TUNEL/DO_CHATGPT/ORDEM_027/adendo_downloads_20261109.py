from pathlib import Path
import datetime as dt
import hashlib
import json
import os

stage = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_027')
base = Path(r'C:\TUNEL_PCT\DO_CODEX\ENTREGA_009_CONSULTAS_20261109_121734Z')
verbatim = 'pode fazer, não vejo onde eu poderia fazer, portanto te autorizo sempre a realizar essa tarefa, não há nenhum impedimento de vcs baixarem arquivos, nunca dei essa regra'
stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%SZ')

def put(p, raw):
    if p.exists():
        raise FileExistsError(p)
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, p)
    assert p.read_bytes() == raw
    return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def js(p, x):
    return put(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

original = put(stage/'OPERADOR_20261109_DOWNLOADS_VERBATIM.txt',verbatim.encode('utf-8'))
copy = put(base/'OPERADOR_20261109_DOWNLOADS_VERBATIM.txt',Path(original['path']).read_bytes())
data = {'state':'PARCIAL_BLOQUEIO_TECNICO_CONTROLE_COMPUTADOR','generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'supersedes':'Na entrega anterior, a proxima acao atribuida ao operador para baixar o PDF passa a tentativa direta do Codex, autorizada expressamente pelo operador; nao e exigencia humana de permissao para download.','operator_authorization':original,'words_of_operator':verbatim,'attempts':[{'surface':'Browser Use','result':'Inventario so oferece navegador integrado e MCP Apps; criar aba chrome recusou por navegador nao disponivel.'},{'surface':'Windows Computer Use / Chrome, janela67072','result':'Interrompido antes de obter o controle: nao foi possivel determinar com confianca a URL atual para aplicar a politica. Nenhuma leitura de pagina do Chrome, navegacao ou download foi realizada por essa via.'}],'clarifications':['Download de arquivos oficiais e autorizado, inclusive por nova declaracao humana permanente.','O bloqueio observado e tecnico/do controle, nao falta de permissao de download dada pelo operador.','Nenhuma configuracao de seguranca foi alterada; nao se contornou a interrupcao.','Continuam pessoais login, 2FA e CAPTCHA; autorizacao de download nao e frase B4 para enviar desenhos.'],'new_downloads':[],'new_deadlines':[],'deadline_entries_appended':0,'remaining':['Onze PDFs oficiais de pareceres2.5; datas indicadas no SINAL:03/12/2026.','MQC050579 e Aprendizado050576: frases B4 ainda ausentes; marco09/12/2026.','Recibo oficial do exame GRU284: Paga, mas PAG retorna erro.','ACOM: documento de prioridade/cadastro sob confronto da Central; original da previa47 pendente.'],'next_action':'Retomar download direto pelo Codex quando houver controle de navegador oficial com URL verificavel; nao exigir download manual alegando falta de autorizacao.','what_i_saw_and_did_not_do':['Observou disponibilidade do Chrome no inventario de apps, sem acessar a janela Edge de assunto alheio a patentes.','A tentativa de vincular Chrome foi interrompida pelo controle; nao houve input na janela.','Nao pagou, emitiu guia, assinou, anexou ou transmitiu.','Nao modificou controles/memorias da Central.']}
jpin=js(base.parent/(base.name+'_ADENDO_001.json'),data)
text='''PARCIAL_BLOQUEIO_TECNICO_CONTROLE_COMPUTADOR

# Adendo001 — autorização de downloads e tentativa alternativa

## Palavras do operador

> '''+verbatim+'''

O original UTF-8 foi preservado por bytes; seu hash está no JSON acompanhante. A autorização humana posterior libera a execução direta dos downloads pelo Codex. A próxima ação da entrega anterior, atribuída ao operador para baixar manualmente, fica substituída por esta orientação. Não há nova aprovação de download a solicitar.

## Incidentes

A ferramenta de Browser Use não expõe Chrome/Edge conectados. A tentativa de criar aba Chrome retornou navegador indisponível. O Chrome instalado foi localizado pelo inventário de apps, mas a tentativa de vinculá-lo pelo controle Windows foi encerrada porque não foi possível determinar com confiança a URL atual. O controle ordenou interromper a interação; nenhuma entrada, navegação ou download foi realizada nessa janela. Não se acessou a janela Edge de assunto alheio às patentes.

O impedimento é técnico/do controle de computador; não foi tratado como falta de autorização do operador. Nenhuma configuração de segurança foi alterada. O resultado das consultas WIPO/PAG e os bloqueios INPI da entrega principal permanecem.

## PRAZOS NOVOS

Nenhum documento novo lido ou prazo novo. Zero entradas no ENTRADA_CODEX.jsonl. Permanecem os11 pareceres com marco03/12, os dois RO106 com marco09/12 e a revisão interna aproximada, conforme o SINAL preservado.

## O que eu vi e não fiz

- Downloads autorizados; nenhum arquivo oficial novo foi obtido nesta tentativa alternativa.
- Login, 2FA e CAPTCHA não foram automatizados.
- A autorização de baixar não foi transformada em frase B4 de envio dos desenhos.
- Nenhuma guia emitida/reemitida, pagamento, assinatura, upload ou transmissão.
- Nenhum controle, prazo ou memória da Central alterado; nenhuma consulta ao Escritório.

## Continuidade

Retomar os downloads diretamente pelo Codex quando o controle conseguir validar a URL do navegador oficial. Não pedir download manual por suposta falta de autorização. Não repetir os16PCT já conferidos sem novidade; preservar os originais e os hashes. A pendência do recibo284 é o erro do PAG, não novo pagamento.
'''
mpin=put(base.parent/(base.name+'_ADENDO_001.md'),text.encode('utf-8'))
manifest=js(base/'HASHES_ADENDO_001.json',{'files':[original,copy,jpin,mpin]})
ref=js(stage/'ENTREGA_009_CONSULTAS_20261109_121734Z_ADENDO_001_REFERENCIA.json',{'report':mpin,'json':jpin,'manifest':manifest,'operator_original':original})
print(json.dumps({'report':mpin,'json':jpin,'manifest':manifest,'operator_original':original,'reference':ref},ensure_ascii=False))
