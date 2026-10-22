"""Keep the operational memory tied to measured conditional-model results."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from record_universe_delivery import append, HERE, CANON, CENTRAL


def main():
    receipt = Path(sys.argv[1]).resolve()
    assert receipt.parent == (HERE/'state').resolve()
    result = json.loads(receipt.read_text(encoding='utf-8'))
    assert result['status'] == 'PASS' and result['gw_unchanged']
    for name, sha in result['installed_sha256'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == sha
        assert hashlib.sha256((CANON/name).read_bytes()).hexdigest() == sha
    cases = result['cases']
    ref = cases['mass_clock_reference']['prediction']
    high = cases['mass_clock_high_spin']['prediction']
    freq = cases['mass_clock_high_frequency']['prediction']
    pin = result['installed_sha256']['static/universe-map.js']
    marker = 'TGL_EXTREME_REGIMES_' + pin[:16]
    text = f'''## {datetime.now():%d/%m/%Y %H:%M} — Regimes extremos visíveis e métricas condicionais

[INPUT] Operador: “Inclusive eu preciso ver os locais de regime extremo com maior facilidade, porque é lá onde a TGL vai se manifestar em maior evidência”. Implementada navegação por ambientes, eventos e cenários, preservando como hipótese investigativa a relação entre regime extremo e maior evidência. Não há ranking de sigma sem medida de sensibilidade.

[REAL — interface] Seção destacada `/explore#extreme-regimes`, com seis rotas: Universo jovem/acústica (prioridade D10), horizontes/ringdown (GW250114), spin elevado, modos de maior frequência, vazios/contrastes e partículas/coerência. Cada seleção mostra o que variar, efeito a comparar, estado da sensibilidade e acesso disponível. CMB alto-z permanece didático; BAO abre o V3 existente z≤3. Vazios/partículas identificados como integração pendente. Sem coordenadas celestes inventadas.

[REAL — cenários] Links allowlist `?regime=high-spin#ringdown` e `?regime=high-frequency#ringdown` preparam apenas controles `model-*`, nunca o evento. Cenário spin: massa fonte65, spin0,95, z0,1, duração0,12s; frequência: massa fonte20, spin0,7, mesmo z/duração. Não selecionam relógio; leitura exigida do usuário. Banner deixa explícito cenário exploratório, não ajuste ao evento. Valores desconhecidos/duplicados de regime não aplicam preset.

[REAL / CONDICIONAL] UI lê do executor Γ, x=Γτ_GR, delta_tau_ensemble_exact, modo e método QNM; nenhuma fórmula física nova no navegador. Dados ausentes são indisponíveis; números minúsculos usam notação científica; R-GLOBAL exibe zero real. Seis controles HTTP medidos no executor existente: R-B referência x={ref['x']}, delta_tau={ref['delta_tau_ensemble_exact']}; spin0,95 x={high['x']}, delta_tau={high['delta_tau_ensemble_exact']}. Massa20: frequência {freq['f_gr_hz']}Hz, Γ={freq['gamma_per_s']}s^-1, x={freq['x']} igual à referência dentro da precisão. R-A conserva efeito muito pequeno e a escala inversa com massa; R-GLOBAL zero. São previsões de ensemble sob hipóteses explícitas, sem fit, curva de sensibilidade ou sigma.

[REAL — verificação] Navegador conferiu seis cartões, deep link spin com campos corretos, relógio vazio e botão de cálculo desabilitado, seleção R-B e valores do executor, R-A não arredondado a zero, R-GLOBAL com zero, método/mode retornados, sem erros JS ou overflow horizontal. Revisão física independente examinou escalas da fonte e limites. Nenhum novo serviço nem reinício: preservada carga GW {result['gw']['loaded_files']}/{result['gw']['total_files']}, {result['gw']['resident_bytes']}bytes, load_id {result['gw']['load_id']} e hashes. Alteração somente da bancada local; web pública/iOS/Android não afetados. Nenhum original científico ou gate alterado.

Guia: `{CANON/'REGIMES_EXTREMOS.md'}`. Recibo: `{CANON/'state'/receipt.name}`, SHA256 {hashlib.sha256(receipt.read_bytes()).hexdigest()}. Memórias com backup imediato de bytes e append atômico. Sensibilidade global, mapas CMB/estrutura, vazios e partículas seguem nas pendências explicitadas.
'''
    for root in (HERE, CANON):
        for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PLANO_UNIVERSO_RESIDENTE.md','DESENHO_DO_COCKPIT.md'):
            append(root/name, text, marker)
    for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md'):
        append(CENTRAL/'memory'/name, text, marker)
    print(marker)


if __name__ == '__main__':
    main()
