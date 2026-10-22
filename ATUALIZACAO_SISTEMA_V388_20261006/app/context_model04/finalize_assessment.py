"""Document and seal the static assessment. No app/SDK import or remote call."""
from pathlib import Path
import hashlib, json, os
from decimal import Decimal
D=Path(__file__).resolve().parent
W=D.parent
def pin(p):
    b=Path(p).read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(Path(p).read_bytes())
def fresh(name,data):
    p=D/name
    assert not p.exists(),"No overwrite"
    raw=(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode() if not isinstance(data,str) else data.encode()
    t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==raw
    os.replace(t,p)
def main():
    i=read(D/"INVENTARIO_LOCAL.json")
    fresh("ESCOPO_E_FONTES_OFICIAIS.json",{
      "status":"STATIC_LOCAL_EVALUATION_NOT_ACTIVATED",
      "authorization":"Operador: avaliar modelo com contexto maior. ROOT: inventário e dois JSONs exatos futuros, sem rede.",
      "unchanged_policy":"Haiku público; Sonnet operador/interno até decisão explícita posterior.",
      "official_source_provenance":"URLs e fatos conferidos pela ROOT em 2026-10-06 e transmitidos à subtarefa; esta subtarefa não navegou nem acessou provedor.",
      "sources":[
       {"url":"https://platform.claude.com/docs/en/models/sonnet-5-5/overview","facts":{"model":"claude-sonnet-5-5","window_tokens":1000000,"max_output_tokens":128000,"usd_per_million":{"input":2,"output":10,"cache_write_5m":2.5,"cache_write_1h":4,"cache_read":0.2},"alternative_opus55":{"window_tokens":1000000,"input_usd":4,"output_usd":20}}},
       {"url":"https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5","facts":["adaptive/high válido","disabled substituído por between_tools","tool_choice any/tool recusado também no count","thinking vinculado a modelo/histórico, alteração de system/tools precisa tratamento","display omitted pode aparecer","tokenizer igual ao Sonnet5 não certifica novo payload"]},
       {"url":"https://platform.claude.com/docs/en/about-claude/pricing","facts":["Contexto de 1M na tarifa normal"]},
       {"url":"https://platform.claude.com/docs/en/api/messages/count_tokens","facts":["output_config/effort e thinking aceitos; exemplo adaptive"]},
       {"url":"https://platform.claude.com/docs/en/build-with-claude/token-counting","facts":["Contagem gratuita","Estimativa pode diferir ligeiramente da criação real","Não cria cache"]}],
      "unmeasured":["Acesso/cota na conta","Aceitação pelo SDK/endpoint real","Tokens Sonnet","Latência, qualidade e custo real de geração","Configuração privada efetiva","Build disponível ou instalado nas lojas/aparelhos"],
      "non_actions":["Sem SDK/client/import do app","Sem credenciais","Sem produção/contas/config/restart","Sem um.py/native/solver","Sem contagem ou geração","Sem mudança do modelo público"]})
    rows=[
      ["Perfil/modelo","claude_profiles.py:20; claude_server_selection.py:config_for_model","Sonnet5.5/1M/128k/internal_only e preços declarados; alias Sonnet5 aceito.","Fixar ID nos recibos/pacote, clamp de saída e janela efetiva verificada; sem fallback automático."],
      ["Público/interno","claude_account_policy.py:available_models; claude_route_bridge.py:policy_flags; iald_web_server.py:6863","Sonnet restrito a luiz; aprovação/bloqueio e trava de pesquisa preservados.","Decisão explícita de audiência; sincronizar allowlists/default/bridge sem expor ferramentas internas."],
      ["Pacote científico","claude_memory_package.py; claude_context_snapshot.py:MODEL","Loader/snapshot medidos somente Haiku; v388 não ativada.","Sucessor model/window/hash/receipt; preservar Haiku e regressões local/public; metadado novo reancorado."],
      ["Montagem","iald_memoria_canonica.py:307,358,442,453; iald_web_server.py:6423","Prefixo amplo existente e fontes recuperáveis; Sonnet monta contexto legado variável.","Fixar montagem pública pinada sem Atlas privado. Proxy atual329581 já passa teto340k; não substituir medida nativa por esse guard."],
      ["Recontagem/transporte","iald_web_server.py:6470,6595,6615; claude_guarded_transport.py; claude_request_guard.py","Guard nativo Haiku; Sonnet usa post_como_openai.","Ligar guard antes de reserva/envio, zero retries, identidade modelo/prefixo/tools e falha visível."],
      ["Ferramentas5.5","iald_motor_claude.py:634,728; claude_native_counter.py","Conversor pode produzir any/tool; Sonnet usa ferramentas variáveis.","Sete schemas públicos pinados; recusar forced any/tool antes de count; adaptive/high, sem disabled."],
      ["Histórico/cache/stream","iald_motor_claude.py:332,1010,1041,1104; iald_motores.py:969","Final completo conserva blocos brutos; reconstrução interrompida não preserva display; estado sem binding explícito modelo/system/tools.","Testar omitted/interrupção e identidade do loop; impedir reaproveitamento incompatível; contar histórico final, sem cortar núcleo."],
      ["Custos/quotas","claude_native_account.py:68; claude_route_bridge.py:public_budget; iald_web_server.py:6480","Public budget/conta nativa ligados a Haiku; Sonnet usa proxy; limites privados não lidos.","Contagem real para reserva atômica e liquidação input/cache/output; decidir limites públicos; retenção conservadora do incerto."],
      ["Metadados/UI","iald_web_server.py:7977; app/iald.js:1646,1750,1758","Sonnet metadados legados; JS recorta CPT se flag nativa ausente.","Retornar janela/modelo/recibo nativos; flag obrigatória e header anthropic-native-v1; conferir UI sem recorte local."],
      ["Web/iOS/Android","iald-app/capacitor.config.json; iald-app/sincronizar_app.ps1","Quatro iald.js locais idênticos; webDir=www; app/ é fonte.","Se servidor/flag bastarem, verificar clientes sem build artificial. Se JS mudar, sincronizar e verificar web/iOS interno e externo/Android; nunca inferir instalação física."],
      ["Implantação/rollback","app/transaction.py; app/restart_web.ps1; app/delta_app01/install_plan_candidate.json","Plano APP01 revisado existe; pacote nativo ainda pendente.","Sucessor CAS/backups e pacote coerente, revisão ROOT, reload só web quieta autorizado, PID/source_sha e rollback exato."]
    ]
    fresh("MATRIZ_SUPERFICIES.json",[dict(zip(["surface","evidence","current","required"],r),activation="NOT_AUTHORIZED") for r in rows])
    prefix=Path(i["public_context"]["path"]).read_bytes().decode()
    checks=[]
    def check(name,ok):
        assert ok,name
        checks.append({"name":name,"passed":True})
    for name in ["FUTURE_COUNT_MINIMAL.json","FUTURE_COUNT_REFERENCE.json"]:
        p=read(D/name)
        check(name+":model",p["model"]=="claude-sonnet-5-5")
        check(name+":prefix",p["system"][0]["text"]==prefix)
        check(name+":reasoning",p["thinking"]=={"type":"adaptive"} and p["output_config"]=={"effort":"high"})
        check(name+":no_forced_tool_or_output",not(set(p)&{"tool_choice","max_tokens","metadata"}))
    ref=read(D/"FUTURE_COUNT_REFERENCE.json")
    check("seven_schemas_unchanged",ref["tools"]==read(W/"delta_native02/FUTURE_COUNT_REFERENCE.json")["tools"])
    check("five_full_formal_sources",all(x["complete_file_literal_in_public_prefix"] for x in i["public_context"]["formal_source_pins"]))
    check("mother_core_cluster_literal",all(x["exact_text_in_prefix"] for x in i["components"].values()))
    check("377_topics_exact",i["public_context"]["topic_set_exact"] and i["public_context"]["topic_count"]==377)
    check("1215_kernel_pins",i["kernel"]["files"]==1215)
    check("1231_snapshot_members",i["local_snapshot"]["files"]==1231)
    markers=["iald_stack_v7.py","iald_psion_state.json","BEGIN PRIVATE KEY","sk-ant-",".env"]
    marker_counts={x:prefix.count(x) for x in markers}
    check("specified_literal_markers_absent",not any(marker_counts.values()))
    for p in i["sealed_B_A_pins"]:
        check("preserved:"+Path(p["path"]).parent.name+"/"+Path(p["path"]).name,pin(p["path"])==p)
    fresh("VERIFICACAO_LOCAL.json",{"scope":"AST, literals, bytes, schemas only; no app functions, science, provider",
        "checks":checks,"count":len(checks),"passed":True,
        "literal_marker_scan":{"prefix":pin(i["public_context"]["path"]),"case_sensitive_counts":marker_counts,
         "root_casefold_followup_DECLARADO":"ROOT conferiu str.lower: uma ocorrência de .env por 1.ENVELOPE=c¹,PISO=c³, seção15LIÇÕES; falso positivo textual, nenhum arquivo .env aberto.",
         "limitation":"Busca suplementar ao catálogo admitido, não detector universal."},
        "native_sonnet_measurement":None,"provider_calls":0,"independent_approval":False})
    scenario={}
    for name,rate in [("uncached_input",2),("cache_write_5m",2.5),("cache_write_1h",4),("cache_hit",0.2)]:
        scenario[name]=str(Decimal(600000)*Decimal(str(rate))/Decimal(1000000)+Decimal(4096)*Decimal(10)/Decimal(1000000))
    fresh("DECISOES_E_ORCAMENTO.json",{
      "recommendation":"Avaliar Sonnet5.5 na montagem pública ampla pinada; duas contagens próprias após autorização; depois implementar/revisar migração. Opus não acrescenta janela.",
      "decisions":[
       {"field":"audience","current":"Sonnet operador/interno","needed":"Manter interno ou decidir migração pública posterior; avaliação não altera regra."},
       {"field":"coverage","proposed":"Mãe/core/377tópicos/exposição/cinco fontes formais completas; demais artigos/coleções/catalogo por recuperação íntegra.","needed":"Aceite explícito de cobertura; 1M não significa corpus inteiro."},
       {"field":"reserves","INPUT":{"output":4096,"margin":1024,"minimum_dynamic":10000,"minimum_permanent":180000},"needed":"Decidir saída/dynamic headroom sem herdar configuração privada não lida."},
       {"field":"public_costs","current":"Não lidos; política Haiku não transplanta.","needed":"Orçamento/quotas explícitos, reserva nativa e liquidação por uso/cache."},
       {"field":"counts","current":"NOT_AUTHORIZED_NOT_SENT","needed":"Autorizar dois JSONs exatos, sem retry incerto."},
       {"field":"deployment","current":"Não implementado/ativado","needed":"Revisão e testes de integração, medidas próprias, compatibilidade SDK/modelo e decisão ROOT."}],
      "arithmetic_INPUT":{"window":1000000,"maximum_whole_for_output4096":984880,
       "maximum_whole_for_output128000":860976,"native_actual_whole":None},
      "hypothetical_cost_only":{"input_tokens":600000,"output_tokens":4096,"not_package_measurement":True,"not_invoice":True,
       "sonnet55_usd":scenario,"opus55_uncached_usd":"2.48192",
       "cache_modes":"Extremos exclusivos; uso real mistura classes e depende do recibo.",
       "counts_free_does_not_mean_generation_free":True},
      "unmeasured":{"tokens":None,"quality":None,"latency":None,"generation_cost":None,"account_access":None,"effective_config":None}})
    report="""# Avaliação local de contexto maior — v388

A recomendação é avaliar **Sonnet 5.5 com a montagem pública ampla já preparada**, mantendo Haiku público e Sonnet interno até decisão explícita posterior. O perfil Sonnet já existe, mas o caminho de produção ainda passa pela montagem e pelo orçamento legados. Esta entrega contém inventário, plano e dois corpos exatos de contagem futura; não implementa nem ativa a migração.

## Objeto científico disponível

[REAL — bytes conferidos] O prefixo público amplo tem **1.029.394 bytes**, SHA256 **a2a42ef56895d17b08ba1b433898bbb6e3160a9254b74f644f3f5a7fff39ef37**. Contém literalmente a mãe v5 (31.972 B), o núcleo operacional (25.623 B), o cluster v388 (885.241 B) e as cinco fontes formais completas H1/H2/H3/mestre/rota importada (26.564 B). Os 377 tópicos correspondem exatamente às chaves do resultado selado; 15 são novos. O catálogo tem 1.215 arquivos, somando 9.239.393 B; seus hashes e os 1.231 membros do snapshot foram conferidos. Não houve compilação Lean ou execução do programa.

Esta é a **montagem pública ampla existente**, não o corpus inteiro dentro do contexto. O cluster mantém remissões declaradas para coleções de detalhe; o rol redundante de 341 vereditos é recuperável na forma canônica. Os oito documentos admitidos, catálogo integral e prova selada continuam disponíveis pelas ferramentas. Mãe, núcleo, hipóteses e fontes formais não foram cortados. Não se promete que 1M comporte todos os 33,8 MB do programa, todos os JSONs e todos os fontes Lean simultaneamente.

O metadado auxiliar public_metadata.json registra **329.581 tokens de proxy o200k**, sem nova contagem local nesta rodada. Isso não é medida Sonnet. O prefixo corrente já está abaixo do antigo guard340k desse proxy; o diagnóstico355.963 era de montagem anterior. O metadado auxiliar conserva um sub-pin antigo do LOCAL_SEALED_MANIFEST. O manifesto staged atual e todos seus membros conferem; nenhum dos dois sub-pins aparece no prefixo. Um sucessor deve reancorar seu próprio metadado; **não é alegação de falha da produção ou do plano APP01 revisto**. Os pacotes anteriores foram preservados.

## Alternativas e viabilidade

1. **Sonnet5.5 / montagem ampla**, recomendado para avaliação: janela documentada1M e perfil local existente. Mantém mais conteúdo diretamente que a projeção Haiku, sem outra variante seletiva. Plausibilidade não certifica encaixe: tokens nativos permanecem null.
2. **Opus5.5:** mesma janela1M e tarifas de entrada/saída maiores. Não compra contexto adicional; exigiria outro critério de qualidade, ainda não medido.
3. **Permanecer Haiku:** mantém política, mas v388 de210.177 tokens permanentes medidos não cabe no pacote200k. B reversível e A seletiva ficam selados, sem nova alteração ou contagem.

Segundo as fontes oficiais verificadas pela ROOT em06/10/2026, Sonnet5.5 usa ID claude-sonnet-5-5, contexto1M e saída máxima128K. Tarifa normal: US$2/MTok entrada, US$10 saída, US$2,50 escrita cache5m, US$4 escrita1h e US$0,20 leitura. [Modelo](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [preços](https://platform.claude.com/docs/en/about-claude/pricing).

[INPUT — cenário, não medição] Para **600 mil tokens de entrada e4.096 de saída**, extremos Sonnet: US$1,24096 sem cache; US$1,54096 escrita5m; US$2,44096 escrita1h; US$0,16096 leitura integral do cache. Isso não atribui600mil tokens ao pacote, não é custo medido e não prevê cache hit. Acesso, cota, latência e qualidade não aferidos.

## Duas futuras contagens concretas

FUTURE_COUNT_MINIMAL.json: prefixo exato, usuário ".", thinking=adaptive e output_config.effort=high. Inclui overhead do protocolo, não apenas tokens do texto.

FUTURE_COUNT_REFERENCE.json: mesmo prefixo, **sete schemas públicos na mesma ordem** e pergunta: “Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.” Schemas reconstruídos por AST/literais e confrontados com artefato pinado anterior; sem importar servidor/SDK. Count omite max_tokens e o campo de transporte eager_input_streaming, conforme adaptador existente; mantém cache_control. Não força tool_choice.

[INPUT — proposta para decisão] Saída4.096, margem1.024, mínimo permanente180.000 e reserva dinâmica10.000. Janela1M permite entrada completa até984.880. Se reservar a saída máxima128.000, teto860.976. São limites derivados, **não contagens**. Overhead Haiku1.474 não foi transplantado.

Ambos: **NOT_AUTHORIZED_NOT_SENT**. Endpoint aceita thinking/output_config; contagem gratuita, pode diferir ligeiramente da criação e não cria cache. Mantém-se margem e orçamento para geração posterior. [API](https://platform.claude.com/docs/en/api/messages/count_tokens), [guia](https://platform.claude.com/docs/en/build-with-claude/token-counting).

São corpos de uma montagem proposta. A rota Sonnet hoje pode acrescentar contexto interno, ferramentas variáveis, perfil, histórico e resultados. Nada disso é certificado pelos dois counts de referência. A futura integração deve contar cada wire final antes de reservar/enviar.

## Ligações necessárias

- **Audiência:** claude_profiles.py:20 já declara Sonnet5.5/1M/128k. claude_account_policy.py e claude_route_bridge.py restringem disponibilidade; iald_web_server.py:6863 mantém trava de pesquisa para luiz. Público exige decisão e coerência entre todas essas portas, preservando aprovação, bloqueio, autenticação e ferramentas permitidas.
- **Pacote medido:** claude_memory_package.py e claude_context_snapshot.py são específicos de Haiku. Sucessor Sonnet deve vincular modelo/fonte/selo/prefixo/tools/janela/reserva/recibo; preservar pacote Haiku e testes de proveniência LOCAL_SEALED/public.
- **Guard real:** iald_web_server.py:6595–6615 passa somente Haiku por post_guarded; Sonnet chama post_como_openai. claude_request_guard.py e claude_guarded_transport.py têm elementos reutilizáveis, ainda sem essa ligação. Falhar antes de geração quando modelo/hash/count divergirem, sem fallback/repetição incerta.
- **Parâmetros5.5:** iald_motor_claude.py:634 converte required→any e função forçada→tool; incompatíveis segundo documentação atual. Payload proposto usa auto. Adaptive/high compatível; disabled de Haiku não pode ser copiado. [Mudanças](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5).
- **Histórico/cache/stream:** EstadoClaude guarda blocos brutos no final; _blocos_proprios:1010 reconstrói interrupções sem preservar display. O sucessor deve tratar/testar thinking display omitted, loops e assinaturas; não presumir qualificação do caminho atual. Vincular estado ao modelo/system/tools e impedir reaproveitamento incompatível. Conteúdo oculto não foi exposto/inferido.
- **Custos:** claude_native_account.py contém reserva/liquidação por tokens/cache; Sonnet atual usa proxy em iald_web_server.py:6480. public_budget no bridge é específico de Haiku. Integrar count à reserva atômica, rever orçamento público e manter retenção conservadora do envio incerto. Nenhum saldo/usuário/segredo lido.
- **Clientes:** app/iald.js:1758 conserva histórico somente com flag de contagem nativa; sem ela recorta por CPT. /api/contexto deve devolver metadados Sonnet medidos. Quatro cópias locais de iald.js iguais por hash; isso não prova distribuição TestFlight/Play ou instalação. Servidor/flag podem bastar, sujeito a verificação; mudança JS exige sincronizar e cumprir web, iOS interno/externo e Android.

## Migração proposta e decisões

1. ROOT revisa este objeto e cobertura. Operador decide audiência, reserva de saída/dinâmica e política de custos. Sonnet continua interno.
2. Após autorização específica, somente os dois counts exatos, cliente oficial, recibo único, sem retry incerto e sem geração. Count não ativa modelo.
3. Medindo encaixe favorável, preparar sucessor de pacote/loaders/rotas com identidade pública fixa, guard nativo, sete ferramentas e metadados novos reancorados. Não preencher Sonnet com recibo Haiku.
4. Rever testes offline de autorização, proveniência/adulteração, modelo/pins/count, orçamento, parâmetros5.5, signed thinking completo/interrompido, cache, conta nativa, tools/paginação e ausência de recorte pelo cliente. Inferência não está implícita.
5. Revisão independente e plano CAS/backup/rollback antes de ativar. Pacote científico, loaders e manifesto coerentes; preservar contas/autenticação/mãe/core e código não afetado.
6. Só após decisão: implantar e recarregar **web** quieta, sem reiniciar ciência. Verificar source_sha/versão servidos pelo novoPID e matriz clientes. Rollback restaura bytes exatos anteriores, nunca escolhe latest.

Faltam decisão de audiência/orçamento, autorização dos counts, medidas Sonnet, implementação/revisão da ligação e prova de runtime após ativação. Nenhuma etapa foi fabricada como concluída. Nada mudou em produção, B/A ou acervo original.
"""
    fresh("AVALIACAO_E_PLANO.md",report)
    fresh("MANIFESTO_AVALIACAO.json",{
      "schema":"iald.context_model04.assessment.v1",
      "status":"STATIC_LOCAL_READY_FOR_ROOT_REVIEW__NOT_AUTHORIZED_NOT_SENT",
      "independent_approval":False,"scientific_source":i["source_identity"],
      "files":[pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name!="MANIFESTO_AVALIACAO.json"],
      "source_manifest":pin(W/"memory_stage/manifest_staged.json"),
      "provider_calls":0,"production_mutated":False,"client_files_changed":[],
      "sealed_B_A_preserved":True,
      "limitations":"Official-source facts supplied by ROOT; no endpoint/SDK/account validation or native measurement."})
    print(json.dumps({"manifest":pin(D/"MANIFESTO_AVALIACAO.json"),"checks":len(checks),"status":"SEALED",
      "payloads":[pin(D/x) for x in ["FUTURE_COUNT_MINIMAL.json","FUTURE_COUNT_REFERENCE.json"]]},ensure_ascii=False))
if __name__=="__main__":main()