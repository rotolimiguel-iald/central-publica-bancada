"""Append the measured desktop/cosmology delivery; byte backups on every memory."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import install_canonical
from record_universe_delivery import append

HERE = Path(__file__).resolve().parent
CANON = install_canonical.TARGET
CENTRAL = HERE.parent.parent
MARKER = 'TGL_COSMOS_DESKTOP_WEBGL2_DELIVERY_20260928'


def read_json(url):
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def main():
    source_receipts = sorted((HERE/'state').glob('validation_cosmology_*.json'))
    if len(source_receipts) != 1:
        raise ValueError('Expected one measured validation receipt; choose explicitly if multiple runs exist')
    validation_path = source_receipts[0]
    validation = json.loads(validation_path.read_text(encoding='utf8'))
    desktop_path = HERE/'state/desktop_verified_20260928.json'
    desktop = json.loads(desktop_path.read_text(encoding='utf-8-sig'))
    for shortcut in desktop:
        if hashlib.sha256(Path(shortcut['Path']).read_bytes()).hexdigest().upper() != shortcut['SHA256']:
            raise ValueError('Desktop shortcut changed after verification')
    cosmos = read_json('http://127.0.0.1:18766/api/cosmology/status')
    gw = read_json('http://127.0.0.1:18765/api/universe/status')
    assert cosmos['memory']['load_id'] == validation['overview']['memory']['load_id']
    assert gw['load_id'] == validation['gw']['load_id']
    assert cosmos['memory']['source_reads_since_load'] == 0
    gpu = read_json('http://127.0.0.1:18765/api/lab/gpu')
    files = ('cosmology_runtime.py', 'cosmology_server.py', 'launch.py',
             'static/cosmos.js', 'static/cosmos.html', 'static/cosmos.css',
             'static/universe.js', 'static/universe.html', 'create_desktop_shortcut.ps1',
             'data/cosmology/desi_gaussian_bao_ALL_GCcomb_mean.txt',
             'data/cosmology/desi_gaussian_bao_ALL_GCcomb_cov.txt')
    hashes = {}
    for name in files:
        raw = (HERE/name).read_bytes()
        assert (CANON/name).read_bytes() == raw, 'Installed file differs: '+name
        hashes[name] = hashlib.sha256(raw).hexdigest()
    output = HERE/'state/delivery_cosmology_desktop_20260928.json'
    report = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'DELIVERED_LOCAL_BAO_EXPLORER_NOT_TGL_CMB_FIT',
        'source_validation': {'path': str(validation_path), 'sha256': hashlib.sha256(validation_path.read_bytes()).hexdigest()},
        'desktop': desktop, 'installed_files': hashes, 'cosmology': cosmos,
        'gw': {key:gw[key] for key in ('status','load_id','generation','loaded_files','total_files','resident_bytes',
                                      'worker_pid','worker_rss_bytes','worker_swap_bytes','data_read_operations')},
        'gpu_telemetry': gpu,
        'tests': {'runtime':7,'http':2,'launcher':2,'total_unique':11,'result':'PASS',
                  'launcher_regression':'Cosmos failure initially hid healthy GW; fixed and rerun.'},
        'browser_checks': {
            'method':'Live CUA interaction; not a synthetic browser fixture',
            'renderer':'ANGLE (NVIDIA, NVIDIA GeForce RTX 5090 (0x00002B85) Direct3D11 vs_5_0 ps_5_0, D3D11)',
            'default_chi2_display':'28,9659','H0_73_chi2_display':'596,9249',
            'z_1_484_scale_display':'0,40258','3d_orbit_zoom_keyboard':True,
            'animation_advanced_and_stopped':True,'console_errors_observed':[],
            'navigation_gw_to_cosmology':True,'shortcut_open_invoked':True,
        },
        'limitations':['13 compressed BAO measures, not galaxy catalog or CMB maps',
                       'Flat matter+CPL background; rd independent; canonical TGL cosmology not mapped here',
                       'No fit, global significance, kernel or gate change',
                       '3D grid is a diagram; not an observed reconstruction',
                       'Public Desktop lacked write access; both user Desktop locations verified'],
    }
    if output.exists():
        raise FileExistsError('Delivery already recorded; append a new correction instead')
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    temp = output.with_suffix('.tmp')
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.stat().st_size == len(raw)
    temp.replace(output)
    installed = (*files, 'data/cosmology/ORIGINS.md', 'RENDER_E_COSMOLOGIA.md',
                 'tests/test_cosmology_runtime.py', 'tests/test_cosmology_http.py', 'tests/test_launcher.py',
                 'validate_cosmology_live.py', 'record_cosmology_delivery.py', 'install_canonical.py',
                 'state/'+output.name, 'state/'+validation_path.name, 'state/'+desktop_path.name)
    for name in installed:install_canonical.install_file(name)
    latencies = [case['http_ms'] for case in validation['calls']]
    passage = f'''## 28/09/2026 — TGL Desktop, GPU e primeiro domínio cosmológico

[INPUT] O operador pediu prosseguir, corrigir o acesso rápido TGL no Windows e avaliar renderizador/Blender.

[REAL] Atalho TGL conferido em Desktop local e OneDrive/Desktop do usuário; launcher e ícone multirresolução existem. A abertura pelo próprio atalho foi invocada e os dois serviços responderam à verificação. Não foi feita inspeção visual do desktop nativo. Tentativa de cópia pública recusada por ACL; não houve alteração de permissão. Backups preservados e ocultos para não poluir o Desktop.

[REAL] Módulo Cosmos em http://127.0.0.1:18766/cosmos, acessível pelo cartão de Cosmologia no Universo residente e pelo mesmo launcher. Renderer WebGL2 identificou RTX 5090/ANGLE D3D11 no navegador. Curvas BAO, barras de erro, resíduos, matriz de correlação, parâmetros manuais, cursor redshift/fator de escala e grade 3D com órbita/zoom/animação. Blender é ferramenta opcional de produção/exportação, não dependência do runtime. A grade é um diagrama, sem galáxias ou posições inventadas.

[REAL] Par DESI DR2 local: 13 medidas, sete redshifts, covariância 13×13 completa, 3019 bytes das duas fontes lidos uma vez. Carga {cosmos['memory']['load_id']}; consultas aquecidas sem novas leituras. A matriz possui 1352 bytes equivalentes numéricos, não RSS. Os hashes são verificados no primeiro carregamento. Fontes/copias e limitação de commit remoto estão em data/cosmology/ORIGINS.md.

[REAL] Sete testes de runtime, dois HTTP e dois launcher aprovados; onze únicos. Uma falha real foi corrigida: cosmos indisponível não deve impedir abrir GW saudável. Concorrência da interface auditada e corrigida: cancelamento ao editar, preservação do cursor na reprodução, cancelamento RAF e mensagem de erro persistente. CUA conferiu χ² 28,9659 → 596,9249 ao variar H0 de67,4 para73, cursor z1,484/a0,40258, GPU, animação e navegação. Seis cenários HTTP: {min(latencies):.2f}–{max(latencies):.2f} ms, sem significância calculada. Não é benchmark amplo.

[REAL] GW preservado: carga {gw['load_id']}, {gw['loaded_files']}/{gw['total_files']} arquivos, {gw['resident_bytes']} bytes; mesmo vetor de hashes antes/depois das consultas. Servidor GW não reiniciado. Cosmos não instancia worker GW; a separação operacional permite adicionar o domínio sem perder a RAM antiga.

[OPEN] O modelo novo é FLRW plano matéria+CPL para z≤3, sem radiação/curvatura, rd como entrada independente, estatuto EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION. É a camada interativa de dados/referência para a rota D10. Ligar a previsão cosmológica canônica da TGL e CMB/BAO com perturbações, nuisance, dados sem dupla contagem e estatística global permanece no contrato acústico já registrado. Nenhum ajuste cosmológico, 5σ novo, original científico, kernel ou gate foi alterado.

Recibo: `{CANON/'state'/output.name}`, SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}. Desenho: RENDER_E_COSMOLOGIA.md. A delegação produziu backend/testes (Fermat), HTML/CSS (Banach), auditoria/HTTP/launcher (Lagrange); integração, JS, instalação e teste real pela coordenação. Nenhuma nova chamada externa ao stack nesta rodada.
'''
    for root in (HERE,CANON):
        for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md'):
            append(root/name, passage, MARKER)
        append(root/'PLANO_UNIVERSO_RESIDENTE.md', passage, MARKER+'_PLAN')
    for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md'):
        append(CENTRAL/'memory'/name, passage, MARKER)
    print(json.dumps({'delivery':str(output),'gw_load':gw['load_id'],'cosmology_load':cosmos['memory']['load_id']}))


if __name__ == '__main__':main()
