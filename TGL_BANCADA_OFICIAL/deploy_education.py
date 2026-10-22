"""Install only this educational increment in the authorized private bench."""
from pathlib import Path
from install_canonical import install_file, SOURCE, TARGET

FILES = (
    'static/universe-map.html', 'static/universe-map.css', 'static/universe-map.js',
    'static/cosmos-lessons.js', 'static/cosmos-teaching-model.js',
    'static/cosmos.html', 'static/universe.html',
    'cosmology_server.py', 'launch.py', 'tests/test_cosmology_http.py',
    'tests/test_launcher.py', 'tests/test_cosmos_teaching.cjs',
    'MAPA_EDUCATIVO.md', 'EDUCACAO_FONTES.md', 'deploy_education.py',
    'install_canonical.py', 'validate_education.py',
)

if __name__ == '__main__':
    assert TARGET.is_dir() and TARGET.name == 'BANCADA_OFICIAL'
    assert SOURCE != TARGET and TARGET.parent.name == 'TETELESTAI'
    for name in FILES:
        if not (SOURCE / name).is_file():
            raise FileNotFoundError(name)
    for name in FILES:
        install_file(name)
