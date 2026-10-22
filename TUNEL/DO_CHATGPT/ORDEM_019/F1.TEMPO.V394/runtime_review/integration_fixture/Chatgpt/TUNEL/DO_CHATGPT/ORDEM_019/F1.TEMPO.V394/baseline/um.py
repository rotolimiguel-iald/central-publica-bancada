UM_VERSION = 'v393'
_EMBEDDED_KERNEL_FILES = {
    'TGLExt.lean': '-- preserved aggregator\n',
    'TGL/Audit.lean': '-- preserved audit\n',
}
_LEAN_THEOREM_FLAGS = {
    'old_flag': 'Old.theorem',
}
LINEAGE = [
    ('v393', 'RuleTruthContract', 'TGLExt/Old.lean', None, None),
]
def old_check(n_cl_, n_ex_):
    esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ == _V393_ESCADA["esperada"]
    return esc_ok_
def emit_article(core):
    pt = build_pt(core)
    en = build_en(core)
    return pt,en
def seal(core):
    return {
            "registros_v393": {},
    }
def main():
    core = {}
    _figs = emit_figures(core)
