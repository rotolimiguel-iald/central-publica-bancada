"""Append the bounded ORDEM018 record with byte backups and optimistic checks."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from audit_inputs import ROOT, safe_write, save_json, file_info


def main():
    marker = '<!-- ORDEM018_CONSOLIDACAO_F0_F2_20261005 -->'
    central = ROOT.parents[3]
    assert central == Path(r'C:\IALD\Central de Patentes')
    a = json.loads((ROOT/'CURRENT_ANCHOR.json').read_bytes())
    assert a['program']['sha256'] == a['seal_fields']['sha256']['um.py']
    now = datetime.now(timezone(timedelta(hours=-3))).isoformat()
    delivered = [ROOT/f for f in ['ENTREGA_018_F0_RANKING.md','ENTREGA_018_F1_HUBBLE.md','ENTREGA_018_F2_DERIVACOES.md','ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md','MANIFESTO_CONSOLIDACAO_PARCIAL.json']]
    refs = '\n'.join(f'- `{p}` — SHA256 `{file_info(p)["sha256"]}`.' for p in delivered)
    block = f'''

{marker}
## {now} — ORDEM 018 do TÚNEL: F0/F2 entregues; F1/F3 em andamento

[INPUT] Meta vigente do operador: usar a estrutura de IAs e a Bancada para localizar um dado discriminante da TGL, conforme ORDEM_018_o_discriminante.md de 05/10. Esta série é distinta da ORDEM_018_TESTE_SENSIBILIDADE de setembro. A abertura de composto para veredito permanece decisão do operador após V1 por hash; preparação e controles locais já autorizados continuam.

[REAL — âncora consultada] Programa {a['seal_fields']['um_version']}, selo `{a['seal_fields']['timestamp']}`. Bytes do programa: {a['program']['bytes']}; SHA256 `{a['program']['sha256']}`, igual à entrada um.py do selo. Selo SHA256 `{a['source']['sha256']}`; result_hash nele registrado `{a['seal_fields']['result_hash']}`. Recibo CURRENT_ANCHOR.json registra horário, fontes e hashes. Leitura de bytes/metadados, sem execução do programa nem nova compilação. Nenhum novo selo científico foi produzido.

[REAL / DERIVED condicional — F0] Treze rotas inventariadas. Hubble é a primeira candidata a completar o contrato, não uma detecção anunciada. Sigma H0DN publicada 0,81 dá separação gaussiana esperada 6,01756 e potência idealizada de 84,56% no desenho Hfid70, fundo sigma0,5 e K fixo em runtime. Não inclui incerteza de K, covariância cruzada ou nuisance das cinco hipóteses. Não usar valores centrais para esse ranking; H0DN/SH0ES/CCHP e variantes da rede não são dados independentes. O resultado não substitui ajuste/evidência com covariância real.

[REAL — F1 parcial] Reproduzida por implementação independente a validação SN-only histórica da Fase5: 1657 linhas, 77 calibradores, 37 hospedeiras; H0=73,53291178±1,01700384, Omega_m=0,33168044, chi2=1452,01710591. Tabela e STAT+SYS públicas coincidem byte a byte com o residente; Cholesky e quadratura independentes conferem. Não é o R22 baseline nem o novo composto Fase9. Reprodução conjunta Fase4/5, cinco evidências e V1 unificado permanecem pendentes.

[REAL documental — novidade de uso] Dezoito fontes de proveniência foram rastreadas, incluindo CRUZ e Evento2 alpha-livre, com trechos e hashes. Foi preservado o resultado discordante do ajuste alpha2 em dezembro, separado do ramo teórico fixo; não se inferiu que esse best-fit substituiu beta fixo. A existência de dados anteriores não deprecia uma retrodição sem ajuste. A forma efetiva do mapa, o fluxo INPUT e a cronologia de cada expressão permanecem distintos; primeira publicação imutável e primeira ocorrência literal de K ainda não foram certificadas por esta revisão.

[REAL documental / DERIVED — H0DN, seq399] A revisão da gerência pinou 24 arquivos públicos e localizou estrutura de rede, covariâncias compartilhadas e uso de pseudoinversa. A matriz 277×277 fornecida é SN, não a C global. Vieses diferenciais Cefeidas atuam nos módulos escolhidos; um zero-point comum a host/âncora pode cancelar. Uma C singular exige suporte N^T r=0 além de r^T C^+ r; a pseudoinversa sozinha não pune violações determinísticas. Deslocamento universal com H0 livre é degenerado; o teste requer fundo independente. Isso qualifica a nota SPD anterior sem alegar defeito no resultado publicado.

[DERIVED condicional / OPEN — F2] Distância acumulada/sombra usa Q=(integral k/E)/(integral1/E), não k no endpoint. No mapa implementado BAO continua nu; planejamento por covariância e nuisance dá D=0,164 no conjunto SN+BAO. Revisão independente GLS concorda em 5,8e-9. Dualidade depende de fL/fA. Temperatura padrão requer dephasing na base do mesmo H, redshift usual e adiabaticidade; a identidade de traço sozinha não fixa T(z). Lentes: fphi=DeltaPhi_fit/DeltaPhi_true, Hfit/Hbg=fphi/(ft FD), errata393 ao lado. S8 +0,599766% é aritmética com sigma8 fixo, não dinâmica de shear. Relógios não ganham nova tau* pela expressão duas leituras. Neutrino m2 é condicional a sin45° POSTULATE e 1eV NORM; soma aposentada por D2 preservada. Pontes faltantes foram localizadas, não declaradas impossíveis.

[REAL documental / OPEN — R-I] O piso limita densidade TOTAL média no núcleo xc=0,25, não perfil radial, saturação ou distribuição populacional. HSW/clipping e lognormal encontrados são templates externos/auxiliares. Nenhum novo estatístico de perfil foi proposto sem F_beta ou Pi_beta e operador observacional. Errata documental395 qualifica nota Neff incongruente do índice seq158 sem transferir conclusão científica aos vazios; resultados396–397 não repetem V11.

[REAL preparação / DERIVED condicional — F3] Rascunho primordial D1–D11 escrito, sem ratificação. Sob proxy S uniforme, DeltaYp=0,00140708 e Delta log10(D/H)=0,00657979; separações apenas por sigmas 1,082/1,265 antes de teoria/nuisance. S(T) e priors externos são necessários; duas abundâncias com dois nuisance livres não identificam o contraste sozinhas. Não se demonstrou poder 5sigma deste instrumento; disso não decorre uma impossibilidade eterna da BBN. ACT DR6 combinações sobrepostas: sigma0,13/0,12/0,11, último com D/He observados. Relação de consistência BBN é hipótese teórica distinta de reutilizar dados de abundância.

[KNOWN — fontes atuais / DERIVED cenário] Simons enhanced sigmaNeff0,045 é forecast estatístico com Planck para levantamento inteiro2025–2034, D2,655 condicional; não é previsão2030. CMB-S4 teve apoio DOE/NSF retirado09/07/2025 e entrou em encerramento ordenado conforme site oficial. Seu cenário antigo0,03 pressupõe consistência BBN (0,09 com Yp livre na referência da F3); não transportá-lo a BBN modificada sem tratamento consistente. Não há calendário numérico ratificado2027/2030 para o estimador completo das13rotas.

[REAL preparação — ringdown D] GPS14/14 localizados em catálogo pinado; 28HDF5+28NPZ existem, tamanhos/janelas/URLs conferidos por stat. Hashes das séries declarados no manifesto, não recomputados sem leitura. Quatro holds e V1 preservados; PSD não identificado nos insumos nomeados. Nenhum posterior/strainD aberto, PE realizada ou hold removido. A31 somente sigmas/spins conhecidos: Dbruto11,383 cai0,742 ao projetar c0+kc sigma livres, verificação independente; não é poder/vereditoD. Cópia sintética IMR só-DTau220, com outros três zeros fixos, está em preparação para qualificar controles sem dadosD. Custo histórico é proxy, não novo piloto medido. F3 continua parcial.

[REAL — coordenação] Subtarefas locais de proveniência, derivações e pré-registros, com revisão cruzada. Zero chamadas novas de executores remotos; Work não usado. Unidade MiMo a4534bcd-8058-48a7-b5fa-34bc046dc46e não submetida: integridade da âncora local bloqueia a prévia, não é diagnóstico de cota da API. Pedido Claude antigo mantém geração pinada divergente, sem repin/repetição. Slots verificados: 1coordenação não terminal,0execuções; limites5/3/1. Solicitação à gerente já respondida; nenhuma cobrança duplicada.

[MAPA / ENTREGA] Consolidação seq400–403; demais seq por rota nos relatórios. Memórias Central atualizadas com backup byte a byte e escrita temporária verificada. Nenhuma versão selada nem mudança de caminho crítico canônico: Nós/linhagem/desenho continuam somente leitura desta frente; a gerência recebe os achados para incorporação própria. NOT_FALSIFIED não vira CONFIRMED. Kernel, gate, originais e pré-registros congelados preservados. Meta ativa, F4 final não emitida.

{refs}
'''
    receipt = {'at':now, 'anchor':file_info(ROOT/'CURRENT_ANCHOR.json'), 'surfaces':[]}
    for filename in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md']:
        path=central/'memory'/filename
        old=path.read_bytes()
        if marker.encode() in old:
            receipt['surfaces'].append({'file':str(path),'status':'marker_already_present'})
            continue
        new=old+block.encode('utf-8')
        if filename=='TGL_ATLAS.md':
            header_marker='<!-- ORDEM018_ANCHOR_20261005 -->'
            first_end=old.index(b'\n')+1
            header=f'\n{header_marker}\n> **Reâncora de consulta ORDEM018, {now}:** {a["seal_fields"]["um_version"]}, selo {a["seal_fields"]["timestamp"]}; um.py `{a["program"]["sha256"]}`; result_hash do selo `{a["seal_fields"]["result_hash"]}`. Bytes e selo conferidos em CURRENT_ANCHOR.json; sem nova execução/compilação. As âncoras anteriores permanecem como linhagem.\n'
            new=old[:first_end]+header.encode()+old[first_end:]+block.encode()
        # Preserve the exact version being touched, and fail visibly on concurrent edits.
        assert path.read_bytes()==old, 'Concurrent memory update before backup'
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup=path.with_name(path.name+'.bak_'+stamp)
        backup.write_bytes(old)
        assert backup.read_bytes()==old
        temp=path.with_name(path.name+'.tmp_ordem018_'+str(os.getpid()))
        temp.write_bytes(new)
        assert temp.read_bytes()==new and len(new)>len(old)
        assert path.read_bytes()==old, 'Concurrent memory update before replacement'
        os.replace(temp,path)
        assert path.read_bytes()==new
        receipt['surfaces'].append({'before':{'bytes':len(old),'sha256':hashlib.sha256(old).hexdigest()},'backup':file_info(backup),'after':file_info(path),'prefix_preserved':filename!='TGL_ATLAS.md','atlas_old_bytes_preserved_except_additive_header':filename=='TGL_ATLAS.md'})
    save_json(ROOT/'RECIBO_MEMORIA_CONSOLIDACAO.json',receipt)
    print(json.dumps({'updated_surfaces':len(receipt['surfaces']),'receipt':file_info(ROOT/'RECIBO_MEMORIA_CONSOLIDACAO.json')},ensure_ascii=False))


if __name__=='__main__':
    main()
