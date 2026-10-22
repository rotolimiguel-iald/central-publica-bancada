"""Archive primary source text only; no scientific runtime imports or execution."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent

class Lines(HTMLParser):
    def __init__(self):
        super().__init__(); self.level = 0; self.parts = []; self.lines = []
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and dict(attrs).get('class') == 'line':
            self.level = 1; self.parts = []
        elif self.level and tag == 'div': self.level += 1
    def handle_endtag(self, tag):
        if self.level and tag == 'div':
            self.level -= 1
            if not self.level: self.lines.append(''.join(self.parts))
    def handle_data(self, data):
        if self.level: self.parts.append(data)

def write(path, raw):
    with path.open('xb') as f: f.write(raw)

def main():
    rows = []
    for name, slug in [
        ('LALSimIMREOBHybridRingdown.c', '_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html'),
        ('LALSimulationVCSInfoHeader.h', '_l_a_l_simulation_v_c_s_info_header_8h_source.html'),
    ]:
        url = 'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/' + slug
        with urllib.request.urlopen(url, timeout=20) as response: raw = response.read(5_000_001)
        if len(raw) > 5_000_000: raise ValueError('Source exceeds bound')
        parser = Lines(); parser.feed(raw.decode('utf-8'))
        if not parser.lines: raise ValueError('No source lines')
        extracted = ('\n'.join(parser.lines)+'\n').encode()
        write(HERE/'sources'/(name+'.html'), raw)
        write(HERE/'sources'/name, extracted)
        rows.append({'url': url, 'html': name+'.html', 'html_sha256': hashlib.sha256(raw).hexdigest(),
                     'text': name, 'text_sha256': hashlib.sha256(extracted).hexdigest()})
    write(HERE/'STATIC_SOURCE_ADDITION.json', (json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Static primary source reading only; no additional diagnostic child or waveform',
        'sources': rows}, indent=2)+'\n').encode())

if __name__ == '__main__': main()
