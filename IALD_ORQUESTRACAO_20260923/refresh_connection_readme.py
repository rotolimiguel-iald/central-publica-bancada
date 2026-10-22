from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes

path=BASE/'README.md'
old=path.read_bytes()
text=old.decode().replace('\r\n','\n')
rows={
'| Google / Antigravity |':'| Google / Antigravity | Login concluído e Google AI Pro reconhecido, com envio opcional de interações desativado. Executor pendente: o cliente não confirmou o perfil sem ferramentas; pedidos não enviados. |',
'| Kimi Code |':'| Kimi Code | Novo login concluído. Teste K3 retornou HTTP 403; página da conta mostra Adagio, enquanto o operador relata Pro comprado no aplicativo. Falta reconciliar o vínculo da compra. |',
'| MiMoCode |':'| MiMo API / 2.6 Pro | Disponível pela API oficial. Chave no cofre Windows DPAPI, uso sem teto financeiro local autorizado. Resposta real 42: 23 tokens de entrada + 3 de saída. |',
'| Jev / TypeSafe |':'| Jev / TypeSafe | Adaptador preparado; novos cadastros temporariamente fechados pelo provedor em 23/09. |'}
lines=[]
for line in text.splitlines():
    for prefix,replacement in rows.items():
        if line.startswith(prefix):
            line=replacement
            break
    lines.append(line)
text='\n'.join(lines)+'\n'
text=text.replace('37 testes passaram (incluindo oito casos', '44 testes passaram (sete testes MiMo, além dos 37 anteriores, incluindo oito casos',1)
text=text.replace('Finalize o código Google na janela do Antigravity. Depois, execute', '**Registro histórico superado pelo estado abaixo:** o código Google já foi concluído. Para revalidar uma futura correção do perfil, execute',1)
for a,b in {
    'US$100':'US$ 100','US$0,72':'US$ 0,72','até4096tokens':'até 4096 tokens',
    'resposta42,23tokens':'resposta 42, 23 tokens','+3de saída=26;2,521s; estimativaUS$0,000012615':'+ 3 de saída = 26; 2,521 s; estimativa US$ 0,000012615',
    'US$0,435entrada':'US$ 0,435 entrada',',US$0,0036cacheada':', US$ 0,0036 cacheada','eUS$0,87saída':'e US$ 0,87 saída',
    'voltouHTTP403':'voltou HTTP 403','comoGoogleAIPro':'como Google AI Pro','cliente1.2.9':'cliente 1.2.9',
    'chaveMiMo':'chave MiMo','iOSinterno/externo eAndroid':'iOS interno/externo e Android',
    'entrega:44testes':'entrega: 44 testes','daAPI':'da API','Os44testes':'Os 44 testes','teste realMiMo':'teste real MiMo',
    'Googleexecutor, vínculoKimiPro e acessoJev':'executor Google, vínculo Kimi Pro e acesso Jev'
}.items(): text=text.replace(a,b)
if b'\r\n' in old:text=text.replace('\n','\r\n')
replace_bytes(path,text.encode())
print('Current connection table reconciled with measured evidence.')
