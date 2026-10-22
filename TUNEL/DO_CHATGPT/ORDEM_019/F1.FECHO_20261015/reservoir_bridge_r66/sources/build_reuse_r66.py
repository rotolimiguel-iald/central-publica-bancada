"""Read-only source assembly for R66; no scientific imports or executions."""
from pathlib import Path
import hashlib
import json
import os
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent
ORDER = OUT.parent
REF = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')

def pin(p):
    p = Path(p); b = p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

def new(name, data):
    p = HERE/name
    if p.exists(): raise FileExistsError(p)
    b = (data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)) .encode('utf-8') + b'\n'
    t = p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes()==b
    t.rename(p)
    return pin(p)

def main():
    specs = [
        ('finite_helpers', OUT/'mission_audit_r62/finite_device_functions_r62.py', [(9,12),(18,23),(35,68)]),
        ('finite_model', ORDER/'F1.REDE/finite_device/run_finite_device.py', [(163,172),(184,191)]),
        ('frame_R57', OUT/'device_clock_r57/derive_polarization_r57.py', [(182,197),(243,249)]),
        ('R7_clock', ORDER/'F1.TEMPO.LEITURA_20261015/DISPOSITIVO_E_ESPECTRO_R7/CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt', [(22,30),(44,79),(82,107)]),
        ('output_contract', OUT/'output_field_r64/output/CONTRATO_OUTPUT_R64.md', [(9,56),(68,83)]),
        ('output_HP', OUT/'output_field_r64/output/ADENDO_DILATACAO_INICIAL_R64.md', [(3,17)]),
        ('output_runner', OUT/'output_field_r64/output/run_filtered_output_r64.py', [(34,76)]),
        ('output_literature', OUT/'output_field_r64/literature/2212.00176v2.html', [(377,392),(395,424),(475,492),(584,610)]),
        ('calibration', OUT/'calibration_r65/calibration/CONTRATO_CALIBRACAO_R65.md', [(15,60),(91,108)]),
        ('bare_frequency', OUT/'calibration_r65/BARE_FREQUENCY_COVARIANCE_R65.txt', [(1,15)]),
        ('Davies_source', Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'), [(11190,11237)]),
        ('Fock', ORDER/'F1.REDE/fock_construction/BosonicFock.lean', [(17,55)]),
        ('Fock_actions', ORDER/'F1.REDE/fock_construction/BosonicFockGroupActions.lean', [(16,23),(47,69)]),
        ('Sectors', ORDER/'F1.REDE/fock_construction/BosonicSectors.lean', [(22,34),(93,118),(154,180),(188,211)]),
        ('DirectSum', ORDER/'F1.REDE/fock_construction/SectorDirectSum.lean', [(15,18),(51,75)]),
        ('TwoParticle', ORDER/'F1.REDE/fock_construction/BosonicTwoParticle.lean', [(38,69),(85,128)]),
        ('receiver_modes', OUT/'physical_receiver_r63/receiver/DERIVACAO_RECEPTOR_R63.md', [(78,105)]),
        ('packets', OUT/'device_continuum_r57/CompactPacketRefinementR1.lean', [(19,63),(77,102),(144,189)]),
        ('complex_packets', OUT/'device_continuum_r57/ComplexPacketLimitR1.lean', [(14,44),(54,78)]),
        ('packet_residual', OUT/'device_continuum_r57/RESIDUAL_TYPED_CONTRACT_R1.txt', [(1,70)]),
        ('physical_net', OUT/'orbital_rotation/PhysicalFockNetRealizationR2.lean', [(18,49),(69,89)]),
        ('net_covariance', OUT/'orbital_rotation/PhysicalFockSpacetimeCovarianceR2.lean', [(28,87)]),
        ('Segal_transport', OUT/'maxwell_global/FockSegalUnitaryTransportR1.lean', [(19,42),(58,118)]),
        ('circular_field', OUT/'maxwell_global/CircularPhysicalFieldTransportR1.lean', [(24,32),(90,107),(110,158)]),
    ]
    sources=[]
    for ident,p,ranges in specs:
        row=pin(p);ls=p.read_bytes().decode('utf-8-sig').splitlines()
        excerpts=[]
        for a,b in ranges:
            b=min(b,len(ls));text='\n'.join(ls[a-1:b])
            excerpts.append({'line_start':a,'line_end':b,'text':text,'excerpt_utf8_lf_sha256':hashlib.sha256(text.encode()).hexdigest()})
        sources.append({'id':ident,**row,'line_count':len(ls),'ranges':ranges,'excerpts':excerpts})
    evidence_paths=[OUT/'device_continuum_r57/DELIVERY_R57.json',OUT/'continuity_r57/FINAL_CUSTODY_REVIEW_R57.json',OUT/'output_field_r64/FINAL_REVIEW_R64.json',OUT/'output_field_r64/output/RESULT_OUTPUT_R64.json',OUT/'calibration_r65/FINAL_REVIEW_R65.json',OUT/'mission_review_20261016/R50_FIELD_CORNER_REVIEW_R2.json',OUT/'reservoir_bridge_r66/HANDOFF_R66.json',OUT/'reservoir_bridge_r66/START_R4_R66_CHECK_RESULT.json',OUT/'reservoir_bridge_r66/START_R5_R66_CHECK_RESULT.json',OUT/'reservoir_bridge_r66/NOS_VIVO_R66.json']
    packet_delivery=json.loads(evidence_paths[0].read_text())
    packet_checks=[]
    for c in packet_delivery['components']:
        if c['name'] not in ['CompactPacketRefinementR1','ComplexPacketLimitR1']: continue
        checked=[]
        for key in ['source','snapshot','receipt','axioms']:
            p=c[key];a=pin(p['path'])
            assert a['sha256']==p['sha256'] and a['bytes']==p['bytes'],p
            checked.append(a)
        packet_checks.append({'component':c['name'],'existing_exit_code':c['exit_code'],'existing_trio_only':c['trio_only'],'pins_rechecked':checked,'new_build':False})
    pinfile=new('SOURCE_PINS_R66.json',{'schema':'r66-reuse-pins-v1','author':'/root/maxwell_covariance_review','source_count':len(sources),'sources':sources,'evidence':[pin(p) for p in evidence_paths],'packet_integrity':packet_checks,'scope':'Leitura focal; não é reauditoria matemática integral. Recibos anteriores referenciados, sem builds, importações científicas ou reexecuções.'})
    def a(s,x,y):return {'source_id':s,'line_start':x,'line_end':y}
    pieces=[
      {'id':'REUSE_GENERATOR','status':'EXISTE_LIGADO_FINITO','anchors':[a('finite_helpers',53,68),a('finite_model',163,191)],
       'available':'liouvillian(h,jumps) e direct_generator(h,jumps,rho), convenção vec por colunas. H completo inclui frequências, Jaynes–Cummings e Omega*(sigma_plus+sigma_minus); cinco canais são preservados.',
       'use':'Comparar o gerador construído de reservatório/colisão com esta forma sem reconstruir matriz64. A lista armazena (taxa,operador), não colapsos já ponderados.',
       'limit':'O a matricial2x2 é corte0/1, não o abaixador bosônico infinito. O novo desenvolvimento por setores de número deve usar sqrt(n) e provar compatibilidade, não identificar matrizes hardcore com operadores ordinários.'},
      {'id':'REUSE_COMMON_BATH','status':'EXISTE_CONTRATO_CONDICIONAL; COLISAO_UNITARIA_EXATA_A_CONSTRUIR','anchors':[a('output_HP',5,17),a('output_contract',11,19),a('bare_frequency',4,15),a('Davies_source',11190,11237)],
       'available':'R64 especifica5banhosproduto no vácuo, S=I e cinco colapsos. O quinto é sqrt(lambda)*(A+B), A=ao†sigma_minus, B=sigma_plus*ai. Portanto é UM canal comum às duas parcelas, embora independente dos quatro outros banhos. Custo já fornece rota espectral de Davies/KMS por correlações de banho.',
       'use':'Acoplar o mesmo ancilla/campo ao J completo preserva os termos cruzados. Para uma construção por colisões, alvo Phi_dt(rho)=Tr_aux[U_dt(rho tensor eta_aux)U_dt†], com (Phi_dt-Id)/dt convergindo ao gerador completo no domínio declarado.',
       'limit':'Nenhuma U_dt unitária exata e limite de colisões para este J foi localizada nas fontes inspecionadas. KMS/Davies secular não pode separar A,B e chamar o resultado D[J]; R65 mostra a obstrução relativa a h0 livre fora da ressonância. Não é impossibilidade geral de reservatório dirigido/não secular.'},
      {'id':'REUSE_DISCRETE_INSTRUMENT','status':'KNOWN_FONTE_CUSTODIADA; NAO_UNIDADE_MICROSCOPICA_PRONTA','anchors':[a('output_literature',377,424),a('output_literature',475,492),a('output_literature',584,610)],
       'available':'Artigo já custodiado em R64, sec2.3: M0=I−iHdt−L†Ldt/2, M1=L sqrt(dt); instrumento difusivo Mr=I−iHdt−L†Ldt/2+sqrt(eta)Lr. A média recupera a evolução não condicionada.',
       'use':'Reaproveitar a expansão de primeira ordem e convenções para o limite de um instrumento de colisões; não recalcular os correladores de R64.',
       'limit':'Os operadores truncados em dt não são, por essa fórmula sozinha, isometria/TP exata para todo dt finito; não confundir esta discretização assintótica com U_dt exata já construída. Nenhuma consulta web nova.'},
      {'id':'REUSE_DRIVE_FRAME','status':'EXISTE_LIGADO_FINITO_COM_INPUT_NOMEADO','anchors':[a('frame_R57',182,197),a('frame_R57',243,249),a('R7_clock',44,79),a('calibration',91,108)],
       'available':'R57 LAB_PHASE_LOCKED_DRIVE escreve h_lab=h0+Omega(e^{-iwdt}sigma_plus+e^{iwdt}sigma_minus), N=ni+no+ne e R=e^{iwdtN}; demonstra h_rot e transporte dos canais. R7 distingue micro-ondas Omega*sigma_x de injeção óptica/EOM. R65 registra que input coerente contínuo requer deslocamento e Hamiltoniano óptico correspondente.',
       'use':'O drive OH limitado pode ser reinserido na extensão bosônica, com sua normalização Omega (sem1/2). Transporte LO de R64 theta_rot=theta_lab+wd*t. Conservar o sistema completo na comparação.',
       'limit':'O deslocamento de campo que deriva um drive óptico do reservatório coerente não foi implementado nessas peças; não confundir esse drive com micro-ondas. Fórmulas R57 são verificadas no corte; extensão e controle de domínio do gerador infinito são nova obrigação.'},
      {'id':'REUSE_TEMPORAL_READOUT','status':'EXISTE_LIGADO_CONDICIONAL','anchors':[a('output_contract',21,56),a('output_HP',5,17),a('output_runner',46,76),a('calibration',40,58)],
       'available':'dBout=dBin+Ldt, M_theta, ordem temporal, ruído delta/2, ODEs para rho,u,v e decoder de modos filtrados já construídos. R65 transporta tempo, taxas, colapsos sqrt(t0), filtros e LO.',
       'use':'Uma dilatação nova que descarregue as hipóteses de R64 pode consumir diretamente esse instrumento e seus controles anteriores.',
       'limit':'O modo temporal B_f contém campo incidente e integral de a(t); não é a_out num instante, nem vetor de H1 espacial identificado por nome. A correspondência instrumental permanece condicional à mesma porta e estado de entrada.'},
      {'id':'REUSE_FOCK_MODE_EMBEDDING','status':'EXISTE_CINEMATICA; FATORIZACAO_COMPLETA_NAO_LOCALIZADA_NO_RECORTE','anchors':[a('Fock',17,55),a('Sectors',22,34),a('Sectors',93,118),a('DirectSum',51,75),a('TwoParticle',38,69),a('receiver_modes',78,90)],
       'available':'F1.REDE constrói F=lp(Sector n)2; setores simétricos são fechos de spans das potências tensoriais. Há sectorEmbedding, oneParticle, vácuo e ortogonalidade. R63 escreve inclusão V0/1 para fi,fo ortonormais:Omega,fi,fo,(fi tensor fo+fo tensor fi)/sqrt2, estendida por identidadeOH.',
       'use':'Para a família totalN≤m, reutilizar esses setores e construir os vetores de ocupação normalizados de fi/fo em cada setor. Os dados fi,fo continuam INPUT até ligação aos modos físicos.',
       'limit':'V0/1 é derivação cinemática escrita, não theorem Lean de fatorização F≅F(span{fi,fo})tensorF(perp). Não localizei tal fatorização completa nos10módulos de F1.REDE/fock_construction consultados. BosonicTwoParticle usa seu setor fixo por flip; BosonicSectors usa fecho de spans diagonais: comparar as interfaces antes de tratá-las como definicionalmente idênticas.'},
      {'id':'REUSE_SPATIAL_PACKETS','status':'EXISTE_COMPILADO_REUTILIZAVEL','anchors':[a('packets',19,61),a('packets',77,101),a('packets',144,189),a('complex_packets',14,44),a('complex_packets',54,78)],
       'available':'CompactPacket, packetSpace, inclusões literais isométricas e compatibilidade; packet_union_closure=compactLocalized. complexPacket_union_dense fornece densidade no mesmo H1. Translação/Lorentz levam pacotes às imagens; incluem FutureLorentz e boost=B0.',
       'use':'Escolher perfis de campo derivados do acoplamento físico dentro desses geradores e usar os refinamentos/densidade já prontos. Não exigir que cada pacote finito seja invariante pelo grupo.',
       'limit':'Não fornece ainda a igualdade de Gram/covariância dos modos do reservatório com circularSmear, ação microscópica ou limite dinâmico. Não reabrir a obstrução da torre produto como proibição de estados correlacionados.'},
      {'id':'REUSE_NET_ACTION_FIELDS','status':'EXISTE_NA_MESMA_REDE_CANONICA','anchors':[a('Fock_actions',16,23),a('Fock_actions',47,69),a('physical_net',18,49),a('net_covariance',28,87),a('Segal_transport',58,118),a('circular_field',24,32),a('circular_field',90,158)],
       'available':'gamma(u) segunda quantização no mesmo H1, UF/VF e covariância; rede FieldWeyl.R(compactLocalized), covariância translacional e FutureLorentz; circularSmearCLM e transporte Segal/campo normalizado com amplitude fixa sqrt((2pi)^−3).',
       'use':'Após construir o mapa de modos e sua compatibilidade espacial, consumir esses entrelaçamentos e a covariância pronta. gamma aqui recebe u:H1≃liH1; a interface não é uma segunda quantização genérica de qualquer inclusão entre Hilberts distintos.',
       'limit':'Não inferir Fock temporal HP=Fock Maxwell por isomorfismo abstrato. A igualdade de produto interno, suporte/localização, representação e o transporte do gerador no domínio devem vir do mapa físico.'},
    ]
    next_steps=[
      'Banho/colisão: construir unidade por passo para J inteiro e canais convencionais, provar expansão e limite; conservar H e termo OH. Não trocar D[A+B] por soma independente.',
      'Bosônico: usar setores por totalN e abaixadores sqrt(n); provar compatibilidade de cortes, extensão conservativa em classe-traço e controle de domínio. Reintroduzir driveOH limitado requer teorema de perturbação/produto adequado, não só finitude de matrizes.',
      'Rede: construir perfis de teste F_j(f) a partir da porta/acoplamento, com K(f)=circularSmear(F_j(f)); provar igualdade de Gram (ou limite controlado), suporte e covariância. Depois usar pacotes densos e gamma/campo existentes.',
      'Instrumento: transportar o mesmo estado, porta, campo incidente, LO/filtro e escala ao contrato R64; somente então declarar que as hipóteses dessa realização foram descarregadas.',
    ]
    report={'schema':'r66-focused-reuse-v1','created_utc':datetime.now(timezone.utc).isoformat(),'author':'/root/maxwell_covariance_review','status':'DECLARADO_CANDIDATE_SOURCE_REUSE','mission_reference':str(REF),'source_pins':pinfile,'reference_project':pin(HERE/'PROJECT_START_R66.json'),'requirement_satisfied':False,'source_count':len(sources),'pieces':pieces,'shortest_construction':next_steps,'coverage':{'text_search':'12 fontes já pinadas de R65/R64; padrões e linhas em FOCAL_SEARCH_R66.json. Kraus/Krauss/colisão lexical filtrados semanticamente.','formal_lookup':'10módulos diretos F1.REDE/fock_construction; fornecedores específicos R57,PhysicalFockNet/Spacetime e transporte de campo. Sem varredura de caches/attempts para descoberta.','absence_scope':'Nenhuma afirmação de ausência universal. Fatorização completa/colisão exata não localizadas somente no recorte consultado.','activities':'Zero simulações, builds, importações científicas, provedores, dados observados, alterações de memória/cânone/gate ou transições por este agente.'}}
    r=new('REUSE_R66.json',report)
    text=['R66 — reaproveitamento focal; candidato documental','Referência: '+str(REF),'Fonte/pinos: SOURCE_PINS_R66.json;12fontes na busca lexical e fornecedores diretos identificados abaixo.','']
    for p in pieces:
        text += [p['id']+' — '+p['status'],p['available'],'Uso: '+p['use'],'Limite: '+p['limit'],'Âncoras: '+ '; '.join(x['source_id']+':'+str(x['line_start'])+'–'+str(x['line_end']) for x in p['anchors']),'']
    text += ['Próxima composição (não executada nesta revisão):']+next_steps+['','Caminhos e hashes completos:']+[s['id']+' | '+s['path']+' | '+s['sha256'] for s in sources]
    t=new('REUSE_R66.txt','\n'.join(text))
    print(json.dumps({'report':r,'note':t,'pins':pinfile,'sources':len(sources),'pieces':len(pieces)},ensure_ascii=False))

if __name__=='__main__':main()
