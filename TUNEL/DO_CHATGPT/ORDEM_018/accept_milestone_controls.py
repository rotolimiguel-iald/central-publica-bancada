"""Incorporate reviewed, bounded results without rerunning scientific jobs."""
from datetime import datetime, timezone
from pathlib import Path
import json
from audit_inputs import ROOT, file_info, safe_write, save_json


def append_once(name, marker, body):
    path = ROOT / name
    old = path.read_bytes()
    if marker.encode() not in old:
        safe_write(path, old + ('\n\n' + marker + '\n' + body + '\n').encode())


def main():
    checks = []
    sources = [
        ('preregistros/conjunto_d/piloto_sintetico/MANIFESTO_PILOTO_SINTETICO.json', 'files'),
        ('proveniencia/REVISAO_PILOTO_SINTETICO_F3_ENCERRAMENTO.json', 'artifacts'),
        ('reproducao_fase45_conjunta/T4_MANIFESTO.json', 'artifacts'),
    ]
    for rel, key in sources:
        manifest = json.loads((ROOT / rel).read_bytes())
        for item in manifest[key]:
            actual = file_info(Path(item['path']))
            assert actual['bytes'] == item['bytes'] and actual['sha256'] == item['sha256'], item['path']
            checks.append(actual)
    review = json.loads((ROOT / sources[1][0]).read_bytes())
    assert review['open_findings'] == 0 and not review['D_opened'] and review['PE'] == 0
    append_once('ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md', '<!-- F3_P0_P2_ACCEPTED_411_412 -->', '''## Atualização: P0–P2 qualificados e revistos independentemente

[REAL — 05/10 local, 06/10 UTC] A preparação descrita acima avançou: P0–P2 foram concluídos e a revisão independente não deixou achado bloqueante no recorte pinado. A rodada final aprovou38 controles; duas revisões somaram12 gerações nativas, seis construções de injeção de três cenários repetidos, e zero PE/EDOM. Não são38 realizações estatísticas independentes. GR→RB→GR retornou bit a bit. Outros três parâmetros de deformação permaneceram zero; demais harmônicos GR da família IMR permanecem.

O revisor realizou212 conferências em44 arquivos e releu165 hashes de runtime. Reconstruiu exatamente os12 hashes de strain sintético como noise+signal e verificou SNR ótimo de rede20, PSD, grades, ruído e unidades. Não gerou novas waveforms. A errata da frase de allowlist do contrato02 foi resolvida ao lado, sem repinar ou repetir a rodada. O hook Python não é uma auditoria universal de syscalls; os registros em memória qualificam o fluxo exercitado.

Custo medido das duas revisões:2,493175s CPU dos filhos e7,511290s wall dos launchers;0,677694s nas chamadas nativas. Isso mede construção/controle da fonte, não custo ou convergência de PE. Cobertura, viés, poder D e recuperação seguem OPEN. O próximo passo é um contrato limitado a dois jobs de recuperação sintética, revisto antes da execução; nenhuma série/posterior D foi aberta, nenhum hold/V1 alterado.

Evidências: [nota do autor](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/NOTA_QUALIFICACAO_P0_P2.md>), [manifesto](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/MANIFESTO_PILOTO_SINTETICO.json>) e [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/REVISAO_PILOTO_SINTETICO_F3.md>). Mapa411–412. A F3 permanece parcial.''')
    append_once('ENTREGA_018_F1_HUBBLE.md', '<!-- F1_T4_REPRODUCTION_ACCEPTED_409_410 -->', '''## Atualização: reprodução histórica T/F4 D1b

[REAL — reprodução determinística] A família T, Planck comprimido+DESI DR2+32 cronômetros diagonais, foi reproduzida independentemente. Não inclui escada. Os mínimos chi2 LCDM/TGL fixa/beta livre são29,0166786272 /39,4097976997 /28,9459763407; diferenças dos números arquivados até3,12e-8. Beta livre0,000947055731 e sigma0,003551165741 reproduzem o diagnóstico histórico, sem redefinir a teoria. Conservou-se o resultado discordante deste ramo.

As covariâncias Planck3×3 e DESI13×13 foram mantidas; CC é diagonal histórica, não a sistemática F7. A fatorização entre blocos é INPUT arquivado. A tabela CAMB pinada foi reutilizada; não se alegou independência de sua geração. Código próprio, quadratura GL64/128,400 pontos de controle CAMB e três ajustes convergentes. Wall1,503660s, CPU0,796875s, pico75,65MiB. Sem nova evidência ou composto F9.

Protocolo e código foram congelados localmente antes da execução. O registro adicional no MCP pré-run falhou por status inválido; a recusa foi preservada e o registro final409–410 não foi retrodatado. O motor histórico completo não tinha hash no resultado antigo: acordo numérico não inventa identidade binária desse processo. [Nota e artefatos](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/reproducao_fase45_conjunta/T4_NOTA_REPRODUCAO.md>). A unidade T está encerrada e não será repetida; demais famílias/evidências seguem etapas próprias.''')
    append_once('ENTREGA_018_F1_HUBBLE.md', '<!-- F1_H0DN_SUPPORT_AMENDMENT_20261006 -->', '''## Proposta ao contrato H0DN

[DERIVED / proposta não ratificada] O [adendo](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/H0DN_ADENDO_CONTRATO.md>) fixa a distinção entre a coluna h da rede, viés diferencial de módulos Cefeidas e zero-point comum de âncoras/hosts. H0DN baseline exclui JAGB: esse baseline sozinho não atende o item TRGB/JAGB da F1. Extensão requer seleção e covariância compartilhada próprias.

O protótipo de suporte singular passou18 controles analíticos sintéticos, sem dados reais: a pseudoinversa sozinha ignora resíduos no núcleo, enquanto a guarda de suporte os recusa. Normalização e dimensão da medida importam. O protótipo aguarda revisão independente; tolerâncias dimensionless não foram transportadas ao H0DN. A transformação de prior s→delta_C foi escrita como exemplo restrito de escada puramente Cefeida, não aplicada à rede mista. [Protótipo](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/covariance_support/NOTA_SUPORTE_SINGULAR.md>). Nenhum novo fit, prior ratificado ou V1 congelado foi produzido por esse adendo.''')
    p = ROOT / 'CONTINUIDADE.json'
    state = json.loads(p.read_bytes())
    state['updated_at'] = datetime.now(timezone.utc).isoformat()
    state['phases']['F1'] = 'PARTIAL_CHRONOLOGY_SN_ONLY_T4_REPRODUCED; P4_P5_DETERMINISTIC_FINISHING; FIVE_EVIDENCES_AND_UNIFIED_V1_PENDING'
    state['phases']['F3'] = 'PARTIAL_PRIMORDIAL_DRAFT_D_METADATA_AND_P0_P2_INDEPENDENTLY_REVIEWED; P3_SYNTHETIC_CONTRACT_IN_PREPARATION; NO_D_PE'
    state['milestone_sequences'] = [404, 405, 406, 407, 408, 409, 410, 411, 412]
    save_json(p, state)
    receipt = {'at': state['updated_at'], 'scope': 'coordinator byte acceptance and incorporation; no reexecution',
               'verified_files': checks, 'count': len(checks),
               'manifests': [file_info(ROOT / rel) for rel, _ in sources],
               'updated_deliverables': [file_info(ROOT / name) for name in ['ENTREGA_018_F1_HUBBLE.md', 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md', 'CONTINUIDADE.json']]}
    save_json(ROOT / 'RECIBO_ACEITE_P0_P2_T4.json', receipt)
    print(json.dumps({'checked':len(checks), 'receipt':file_info(ROOT/'RECIBO_ACEITE_P0_P2_T4.json')}))


if __name__ == '__main__':
    main()
