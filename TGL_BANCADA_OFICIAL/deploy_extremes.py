"""Deploy navigation/readouts only. Both resident services stay running."""
from install_canonical import install_file

FILES = (
    'static/universe-map.html', 'static/universe-map.css', 'static/universe-map.js',
    'static/universe.html', 'static/universe.js', 'static/universe.css',
    'REGIMES_EXTREMOS.md', 'validate_extreme_regimes.py', 'deploy_extremes.py',
)

if __name__ == '__main__':
    for name in FILES:
        install_file(name)
