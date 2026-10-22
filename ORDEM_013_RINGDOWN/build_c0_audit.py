"""Line-complete claim audit; source hashes are computed, never transcribed."""
from pathlib import Path
import hashlib
import json
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent
INPUT=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_013_INSUMOS/TEXTO_CONFRONTACAO_OPERADOR_21SET_VERBATIM.md'
rows=[]

def add(lines, verdict, right, corrected, *evidence):
    rows.append(dict(lines=lines,verdict=verdict,what_the_text_gets_right=right,
                     corrected_public_sentence=corrected,evidence=list(evidence)))

def main():
    lines=INPUT.read_text(encoding='utf-8').splitlines()
    add([1,9,11,17,19,25,27,31,47,49,51,58],'NÃO_APLICÁVEL','São títulos ou transições.','Organização textual, sem afirmação científica adicional.','input')
    add([3,5],'PARCIAL','Existe no programa uma realização finita com L=sqrt(beta)sqrt(K).',
        'A v369 constrói um salto hermitiano em um proxy positivo 4x4; a fórmula não identifica por si a dinâmica de um horizonte tipo III1.','verb','gksl')
    add([5],'CANÔNICO','O coeficiente beta é alpha_CODATA2018*sqrt(e).',
        'Beta é calculado em runtime a partir de alpha e sqrt(e); seu valor sozinho não determina um tempo físico.','verb','checks')
    add([7],'PARCIAL','A taxa é proporcional a beta mantendo os demais dados fixados.',
        'Na lei quadrática, tau_deph=2/(beta*tau_star*omega²); uma previsão de detectabilidade em O5 exige relógio, SNR e parâmetros de perturbação.','clock','fisher')
    add([13,60],'CERTO_NO_ESSENCIAL','É necessário mapear o gerador e seu relógio aos observáveis.',
        'O ramo B fornece Gamma=beta*w(chi)²/(2*t_M) sob o relógio INPUT t_M; a distância afeta amplitude/redshift, não necessariamente a taxa local. A escolha física do ramo permanece aberta.','old_prediction','clock','mapping')
    add([14,63],'CERTO_NO_ESSENCIAL','Uma previsão de strain deve ser executável e reproduzível.',
        'Há agora um template condicional de ensemble e um desenrolamento de fase explícito; distinguir ambos e calibrar recuperação é necessário antes do confronto de strain.','template','mapping')
    add([15,62],'CERTO_NO_ESSENCIAL','A viabilidade requer previsão quantitativa de evidência.',
        'O fator de Bayes é aleatório e depende de SNR, PSD e priors. O forecast pontual local tem média +/-z²/2 e dispersão z; não é um ln B observado.','fisher','registration')
    add([20],'CONTRADITO_PELO_CANON','A identificação GKSL-horizonte-strain ainda pede hipóteses explícitas.',
        'A forma funcional e o rito V346 já existem; a rodada V2 foi inconclusiva por sistemáticas e baixa sensibilidade. Não se deve dizer que nunca foi testado.','old_prediction','v2','plan')
    add([21,55],'PARCIAL','Não observação sem confirmação é uma distinção correta.',
        'Os ensaios de ecos da casa não estabeleceram detecção; seus controles de sensibilidade e sistemáticas impedem usar ausência de pico como exclusão geral. Não se reabre esse canal nesta ordem.','echo','plan')
    add([22],'PARCIAL','Resultados publicados são compatíveis com Kerr no estudo consultado.',
        'A precisão depende do modo, observável e modelo. Um limite sobre amortecimento efetivo não é automaticamente um limite sobre decoerência quântica de propagação.','lvk','mapping')
    add([23],'PARCIAL','A inferência GW conferida não mede beta de forma independente.',
        'Na lei quadrática, um relógio livre mede o produto beta*tau_star. Para medir beta é preciso fixar ou identificar o relógio e a partição por informação independente.','clock','plan')
    add([29],'PARCIAL','K=-log Delta é uma convenção de gerador modular.',
        'A identificação modular é dependente da álgebra e do estado; o K bilateral tem simetria de sinal. Não se pode tomar sqrt(K) positiva sem especificar outra construção.','finite_J','gksl')
    add([29],'PARCIAL','O tipo III1 envolve espectro modular amplo, não um corte finito de autovalores.',
        'Espectro como conjunto contínuo não significa ausência de espectro pontual: estados quase periódicos do fator III1 injetivo fornecem uma ressalva explícita. KΩ=0 já é um autovetor modular.','finite_J','almost_periodic')
    add([33],'CANÔNICO','A expressão é o dissipador GKSL formal.',
        'A fórmula é válida para operadores limitados na regularização finita; operadores não limitados exigem domínios e existência do semigrupo. O termo Hamiltoniano foi omitido nesse trecho.','gksl','verb')
    add([35,37],'CONTRADITO_PELO_CANON','Tr(L†L rho)=beta<K> é uma taxa de saltos na representação escolhida.',
        'A taxa de coerência é beta*(sqrt(k_i)-sqrt(k_j))²/2. A média beta<K> não é essa taxa e muda sob L+cI sem mudar o dissipador.','crossover','checks','gksl')
    add([39],'DIMENSIONALMENTE_INCONSISTENTE','A massa fornece uma escala gravitacional natural.',
        'Em hbar=c=1, M/m_P²=GM é tempo. Não é um gerador modular adimensional nem uma taxa sem fatores adicionais e uma identificação física.','checks')
    add([41],'DIMENSIONALMENTE_INCONSISTENTE','A expressão tenta relacionar a taxa a uma escala do remanescente.',
        'Beta*GM/c³ tem unidade de tempo. A lei do ramo B contém ainda omega²/2, tornando Gamma uma taxa.','checks','old_prediction')
    add([43],'DIMENSIONALMENTE_INCONSISTENTE','Uma taxa muito maior que a frequência precisaria ser confrontada com coerência observada.',
        'Para 60 massas solares t_M é cerca de 2.96e-4 s, ou 5.48e39 tempos de Planck. O número 1e76 não é essa taxa; (M_solar/m_P)² é apenas uma hipótese de origem da confusão.','checks')
    add([45],'CONTRADITO_PELO_CANON','Uma leitura física com excesso de perda de coerência pode ser refutada.',
        'A alegada falsificação por 1e76 não decorre das equações apresentadas. Existem leituras fortemente suprimidas e outras testáveis; cada uma exige confronto com seu observável, sem declarar falsificação global a partir de unidades inconsistentes.','checks','clock','registration')
    add([53],'PARCIAL','A frequência fundamental recebeu limites percentuais fortes.',
        'No GW250114 consultado, o ajuste IMR limita df220 em escala percentual e dtau220 em aproximadamente dez por cento (90%); não se generaliza a todos os testes nem ao ringdown isolado.','lvk')
    add([54],'PARCIAL','O estudo consultado encontra consistência com Kerr.',
        'GW250114 fornece limites fortes e dependentes do modelo; consistência não é prova definitiva de Kerr ou confirmação da TGL.','lvk')
    add([56],'DECLARADO','As ondas detectadas permitem estimar coerência e modos sob modelos de sinal.',
        'O texto não fornece um limite numérico de decoerência de propagação. Coerência de strain, matriz densidade e ruído óptico do interferômetro são observáveis diferentes.','mapping','plan')
    add([61],'CERTO_NO_ESSENCIAL','Gamma/omega quantifica um regime perturbativo.',
        'Reportar Gamma/omega é necessário, mas detectabilidade é controlada pela correção em tau comparada à incerteza, depois de eliminar degenerescências e sistemáticas.','fisher','mapping')
    add([65],'PARCIAL','Taxa, template e previsão de evidência tornam o teste operacional.',
        'A precisão final depende da informação dos dados e da calibração. As próximas etapas são posteriores, injeções e strain registrado; fórmulas e software não garantem poder de decisão.','plan','registration')
    refs={
       'input':dict(path=str(INPUT),locator='linhas 1-65'),
       'verb':dict(path='cache/casa/um.py',locator='2311-2332: _verb_L'),
       'crossover':dict(path='cache/casa/um.py',locator='2831-2875: prove_dephasing_crossover, errata v369'),
       'clock':dict(path='cache/casa/um.py',locator='190961-191018: lei e partition_declared'),
       'finite_J':dict(path='cache/casa/ContinuousModularZero.lean',locator='80-94: modularGen_omega_zero, J_modularGen_J; FACE FINITA, não recompilada nesta ordem'),
       'old_prediction':dict(path='cache/casa/ringdown_dephasing_v2.py',locator='139-141'),
       'v2':dict(path='cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json',locator='resultado congelado e per_series[2]'),
       'echo':dict(path='cache/casa/ECHO_PE_V2_RESULT.json',locator='resultado antigo; não reexecutado'),
       'plan':dict(path='cache/casa/PLANO_EXPERIMENTAL_5SIGMA.md',locator='seções 2-4'),
       'checks':dict(path='C0_C3_checks.json',locator='units, jump_rate, signed_modular_extensions, legacy_regression'),
       'gksl':dict(path='verify_c0_c3.py',locator='dissipator e diagonalização independente'),
       'template':dict(path='tgl_ringdown_template.py',locator='ringdown, convenção e recusa de desenrolamento indevido'),
       'mapping':dict(path='C2_MAPEAMENTO_ANALITICO.md',locator='seções 1-6'),
       'fisher':dict(path='C5_FISHER.json',locator='records, mass_spin_free; previsão condicional, não dados'),
       'registration':dict(path='REGISTRO_C4.json',locator='registro anterior à inspeção local, NÃO-CEGO'),
       'lvk':dict(url='https://arxiv.org/html/2509.08099v1',locator='eqs. (1),(2), parágrafos do ajuste pSEOBNR e SNR; texto principal consultado, arquivo primário local ainda pendente'),
       'almost_periodic':dict(url='https://arxiv.org/abs/2406.00874',locator='abstract consultado: estados quase periódicos e espectro pontual em R_infinito')}
    for entry in refs.values():
        if 'path' in entry:
            p=Path(entry['path'])
            if not p.is_absolute():p=ROOT/p
            entry['path']=str(p)
            entry['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    covered=set()
    for n,row in enumerate(rows,1):
        row['id']=f'T{n:02d}'
        row['verbatim']=[dict(line=i,text=lines[i-1]) for i in row['lines']]
        covered.update(row['lines'])
        assert all(ref in refs for ref in row['evidence'])
    required={i for i in range(3,66) if lines[i-1].strip()}
    missing=sorted(required-covered)
    assert not missing,missing
    out=dict(status='CLAIM_COVERAGE_AND_NUMERICAL_ORACLES_COMPLETE__PRIMARY_SOURCE_ARCHIVING_PENDING',
             input_sha256=hashlib.sha256(INPUT.read_bytes()).hexdigest(),claims=rows,references=refs,
             coverage=dict(required_nonempty_lines=sorted(required),covered=sorted(covered),missing=missing),
             remaining=['Archive primary literature with hashes','Full state/domain analysis beyond finite proxy',
                        'Confront current posterior samples; C0 does not replace C4-C6'])
    atomic_json(ROOT/'C0_AUDITORIA.json',out)
    text=['[REAL — auditoria de cobertura e oráculos; arquivo primário local da literatura pendente]',
          '', '# C0 — Auditoria do texto de confrontação', '',
          f'{len(rows)} itens; {len(required)} linhas não vazias exigidas; zero linha descoberta.',
          'A auditoria não declara o objetivo integral encerrado. Referências/hash completos no JSON.','']
    for row in rows:
        text += [f"## {row['id']} — linhas {', '.join(map(str,row['lines']))}",
                 '',f"**{row['verdict']}**",'',
                 'Texto: '+' / '.join(v['text'] for v in row['verbatim']), '',
                 '**O que acerta:** '+row['what_the_text_gets_right'],'',
                 '**Frase corrigida:** '+row['corrected_public_sentence'],'',
                 'Evidências: '+', '.join(row['evidence']), '']
    text += ['## Referências','']+[f'- **{key}**: {ref}' for key,ref in refs.items()]
    target=ROOT/'C0_AUDITORIA.md'
    if target.exists():raise FileExistsError('Preserve previous audit; make a dated amendment')
    temp=target.with_suffix('.tmp'); raw='\n'.join(text).encode('utf-8');temp.write_bytes(raw)
    assert temp.stat().st_size==len(raw);temp.replace(target)
    print(json.dumps({'claims':len(rows),'required_lines':len(required),'missing':missing}))

if __name__=='__main__':main()
