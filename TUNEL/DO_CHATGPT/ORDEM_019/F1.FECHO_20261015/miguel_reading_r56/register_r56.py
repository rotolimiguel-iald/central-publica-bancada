"""Append reviewed R56 custody to the existing route and unit."""
from support_r56 import *

route='formal.f1_rede.concrete_bosonic_kinematics'
artifacts=[str(ROOT/n) for n in ['DELIVERY_R56.json','MEMORY_COMPLETION_R56.json',
           'REVIEW_R56.json','REVIEW_R56_SCOPE_ADDENDUM.json','RELATORIO_R56.txt']]
items=[dict(tipo='ERRATA',rota_id=route,corrige=1184,estatuto='DERIVED',
    titulo='R56: correcao da exigencia de escolha exclusiva do dispositivo',
    resultado='Em nome de codex-gerente-tgl: era prematuro exigir escolha exclusiva MQC/Supercondutor/Psi-NET. O contrato R1 atribui papeis complementares de celula/dinamica/protocolo. A ambiguidade do aparelho singular permanece, mas nao impede investigar a composicao. Critérios R4/R5 mantidos literalmente; nenhum aceite de realizacao fisica inferido.',
    artefatos=artifacts,olhou_dados=False),
 dict(tipo='RESULTADO',rota_id=route,dominio='FORMAL',
    titulo='R56: leitura do angulo de Miguel reutilizada, memoria e frequencia parametrizada',
    pergunta='Como preservar a referencia humana e reutilizar a reconstrucao matricial existente, delimitando o transporte ao relogio do dispositivo?',
    dados=['Fontes Lean locais do kernel consultado','Cinco falas integrais do operador','Patente cientifica do Supercondutor e contratos R1/R55'],
    metodo='Reaproveitamento por import, composicao Lean em sandbox, hashes e bytes, revisao independente. Nenhum dado observado.',
    resultado='Oito superficies de memoria receberam verbatim e alcance com backups de bytes. R2 compilou EXIT0 em 51,422s: oito declaracoes impressas apenas no trio, zero sorry. Leitura/reconstrucao/releitura e fase relativa exp(i Omega*t) provadas para S(thetaMiguel(beta)+Omega*t). Controle: selecao nao injetiva no ambiente matricial inteiro. A orbita varia os pesos e nao e dinamica demonstrada de refletividade beta constante. O sinal atenuado exige preservar amplitude e fase; identificacao com observavel fisico segue aberta. R1 interrompida por recursos, recibos preservados.',
    veredito='COMPONENT_VERIFIED_WITH_SCOPE',estatuto='REAL',status='EM_CURSO',
    olhou_dados=False,
    defeito='R4/R5: realizacao fisica do sinal/gerador e refinamentos da rede. Omega ainda parametro; fase nao fixa voltas nem tempo global. R3/R10: rito integral e revisao final. A presente composicao nao fornece H3 universal.',
    nao_refazer='Reutilizar miguel_boundary_reconstructed_from_its_selected_face, observing_adds_nothing e os aceites R6/Fock, R7/Takesaki, R8/Maxwell. Nao pedir escolha exclusiva dos tres projetos sem alternativas fisicas realmente incompatíveis.',
    proximo_passo='Ligar o sinal complexo, com amplitude preservada, ao setor e gerador ja escritos do Supercondutor; distinguir omegaOH, OmegaRabi, V0/hbar e taxa de coerencia 2Omega. Construir transporte dos refinamentos em R5 a partir da rede existente. R4/R5 em needs_revalidation sem enfraquecimento dos criterios; manter referencia exata/preflight e aceites anteriores.',
    onde=str(ROOT),artefatos=artifacts,
    nota='F1.FECHO_20261015, claim933. Escopo matematico delimitado e memoria; aceite tecnico distinto da ratificacao c1. Sem alteracao de um.py, kernel original, Bancada, dado observado ou gate.')]
entry=new('MAP_ENTRY_R56.json',items)

def run(args,name):
    p=subprocess.run([sys.executable,'-B','-X','utf8',*args],capture_output=True,text=True,encoding='utf-8')
    out=new(name,dict(command=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
    if p.returncode:raise RuntimeError(str(out))
    return out,p.stdout

out,stdout=run([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']], 'MAP_REGISTERED_R56.json')
print(stdout)
out,stdout=run([r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015',
 '--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',*artifacts,
 '--nota','R56: memoria persistida e composicao angular verificada; R4/R5 fisicos e rito/revisao final permanecem. O componente nao fecha a unidade inteira.'],
 'BOARD_REGISTERED_R56.json')
print(stdout)
