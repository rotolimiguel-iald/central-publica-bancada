"""Finalize the reviewed E2 candidate and its tunnel witness; never overwrite."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,ast,stat,subprocess

B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
SNAPSHOTS={}

def snapshot(p):
    p=Path(p).resolve();raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if p in SNAPSHOTS and SNAPSHOTS[p]!=digest:raise ValueError('Input changed during snapshot: '+str(p))
    SNAPSHOTS[p]=digest
    return raw,digest

def stable():
    for p,pin in SNAPSHOTS.items():
        if sha(p)!=pin:raise ValueError('Captured input changed: '+str(p))

def unredirected(p):
    p=Path(p).absolute()
    for part in (p,*p.parents):
        if part.exists():
            info=part.lstat()
            if part.is_symlink() or getattr(info,'st_file_attributes',0)&getattr(stat,'FILE_ATTRIBUTE_REPARSE_POINT',1024):
                raise ValueError('Redirected path refused: '+str(part))
    return p.resolve()

def fixed_path(value,expected):
    if value!=expected:raise ValueError('Critical path differs from fixed contract')
    p=unredirected(R/expected)
    if not p.is_relative_to(R.resolve()):raise ValueError('Critical path outside root')
    return p

def private_directory(action):
    if os.name!='nt':raise RuntimeError('This sealer requires the reviewed Windows ACL primitive')
    command=['powershell.exe','-NoProfile','-File',str(B/'refeito/e2_private_directory.ps1'),'-Action',action]
    result=subprocess.run(command,capture_output=True,text=True,check=True,timeout=30)
    value=json.loads(result.stdout)
    if value['status']!='CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED':raise ValueError('Private ACL not verified')
    return value

def create_seed(p):
    acl=private_directory('Prepare')
    private_directory('Verify')
    temporary=p.with_name(p.name+'.pending')
    # The directory DACL is already exclusive before this first descriptor.
    fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_BINARY',0),0o600)
    with os.fdopen(fd,'wb') as f:f.write(os.urandom(32));f.flush();os.fsync(f.fileno())
    if temporary.stat().st_size!=32:raise OSError('Incomplete private seed retained')
    private_directory('VerifySeed');os.link(temporary,p);temporary.unlink()
    return acl

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def create(p,value):
    raw=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if p.exists():raise FileExistsError(p)
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Incomplete bytes retained')
    os.link(tmp,p);tmp.unlink()

def code_tree(root):
    found={}
    for p in root.rglob('*.py'):
        raw,pin=snapshot(p);ast.parse(raw.decode('utf-8-sig'));found[p.relative_to(root).as_posix()]=pin
    return found

def check_review_application(application,reg,candidate_pin,sealer_pin):
    if application['status']!='APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE':raise ValueError('Missing application of existing GO')
    if application['candidate_sha256']!=candidate_pin or application['sealer_sha256']!=sealer_pin:raise ValueError('GO/review applies to other bytes')
    issued=datetime.fromisoformat(application['created_utc'])
    if issued.tzinfo is None or issued>datetime.now(timezone.utc):raise ValueError('Review application chronology invalid')
    if set(application['reviews'])!={'PE','MAIN','E7','ACTIVATION'}:raise ValueError('Four distinct review roles required')
    required={'bis/e2_code/'+k:v for k,v in reg['own_code_tree_sha256'].items()}
    required.update({'bis/e7_prepare/producer/'+k:v for k,v in reg['e7']['producer_tree_sha256'].items()})
    covered={};review_pins={}
    for role,review in application['reviews'].items():
        if review['status']!='BLOCKERS_CLOSED' or review['blocking_findings']!=[]:raise ValueError('Unclosed review '+role)
        if not review['reviewer_agent_id'] or review['reviewer_agent_id']==review['builder_identity']:raise ValueError('Distinct reviewer declaration required')
        texts=[]
        if not review['files']:raise ValueError('Review evidence missing')
        for name,pin in review['files'].items():
            p=unredirected(B/name)
            if not p.is_relative_to(B/'bis'):raise ValueError('Review outside bis')
            raw,actual=snapshot(p)
            if actual!=pin:raise ValueError('Review evidence changed')
            texts.append(raw.decode('utf-8-sig'));review_pins[name]=pin
        for name,pin in review['covered_source_sha256'].items():
            if name not in required or pin!=required[name] or not any(pin in t for t in texts):raise ValueError('Review coverage does not match source '+name)
            covered[name]=pin
        if role=='ACTIVATION':
            helper='ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1'
            expected={helper:reg['input_pins_relative_to_Chatgpt'][helper]}
            if review.get('covered_security_input_sha256')!=expected or not any(expected[helper] in t for t in texts):
                raise ValueError('Private ACL helper review/pin missing')
    if covered!=required:raise ValueError('Incomplete current-source review coverage')
    go=application['existing_go'];p=unredirected(R/go['relative_to_Chatgpt'])
    if not p.is_relative_to(R/'TUNEL/PARA_CHATGPT') or snapshot(p)[1]!=go['sha256']:raise ValueError('Existing GO source differs')
    if application['exposure_declaration']['statute']!='DECLARADO_PRINCIPAL_WITH_SCOPED_CENSUS':raise ValueError('Exposure history must remain a declaration')
    return review_pins

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True)
    ap.add_argument('--expected-candidate-sha256',required=True)
    ap.add_argument('--review-application-sha256',required=True)
    ap.add_argument('--finalize-reviewed-candidate',action='store_true');args=ap.parse_args()
    if not args.finalize_reviewed_candidate:raise ValueError('Explicit finalization required')
    candidate=(B/'bis'/args.candidate).resolve()
    if not candidate.is_relative_to(B/'bis'):raise ValueError('Candidate outside bis')
    candidate_raw,candidate_pin=snapshot(candidate);reg=json.loads(candidate_raw)
    if candidate_pin!=args.expected_candidate_sha256:raise ValueError('Candidate differs from explicitly approved bytes')
    _,sealer_pin=snapshot(Path(__file__))
    _,helper_pin=snapshot(B/'refeito/e2_private_directory.ps1')
    if reg['input_pins_relative_to_Chatgpt'].get('ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1')!=helper_pin:
        raise ValueError('Private ACL helper differs from approved candidate')
    if reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Not a draft')
    if reg['own_code_tree_sha256']!=code_tree(B/'bis/e2_code'):raise ValueError('Own code changed after review candidate')
    for entry in reg['extra_code_roots']:
        p=(R/entry['relative_to_Chatgpt']).resolve()
        if not p.is_relative_to(R) or code_tree(p)!=entry['files_sha256']:raise ValueError('Extra code changed')
    for name,pin in reg['input_pins_relative_to_Chatgpt'].items():
        p=(R/name).resolve()
        if not p.is_relative_to(R) or sha(p)!=pin:raise ValueError('Input changed '+name)
        SNAPSHOTS[p]=pin
    apppath=B/'bis/E2_REVIEW_APPLICATION_V1.json';appraw,apppin=snapshot(apppath)
    if apppin!=args.review_application_sha256:raise ValueError('Review application changed')
    application=json.loads(appraw);reviews=check_review_application(application,reg,candidate_pin,sealer_pin)
    budgetpath=fixed_path(reg['budget_relative_to_Chatgpt'],'ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json')
    budgetraw,budgetpin=snapshot(budgetpath)
    if budgetpin!=reg['budget_sha256']:raise ValueError('Budget pin differs')
    budget=json.loads(budgetraw)
    now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(budget['hard_deadline_utc']):raise TimeoutError('Budget expired')
    opening=unredirected(D/'ENTREGA_013BIS_ABERTURA_operador.md');_,opening_pin=snapshot(opening)
    if application['opening_sha256']!=opening_pin:raise ValueError('Opening GO application changed')
    final=unredirected(B/'RINGDOWN_5SIGMA_V1.json')
    note=fixed_path(reg['witness_relative_to_Chatgpt'],'TUNEL/DO_CHATGPT/ENTREGA_013BIS_E2_REGISTRO_V1.md')
    seedpath=fixed_path(reg['blinding']['seed_relative_to_Chatgpt'],'ORDEM_013_RINGDOWN/cache/E2_PRIVATE/BLIND_SEED_V1.bin')
    fiche=unredirected(B/'REAPROVEITAMENTO_AMPLIACAO_E2.md');receipt=unredirected(B/'bis/E2_REGISTRATION_RECEIPT.json')
    destinations=[p for dest in (final,note,seedpath,fiche,receipt) for p in (dest,dest.with_name(dest.name+'.pending'))]
    if len(set(destinations))!=len(destinations):raise ValueError('Output/temporary collision')
    for p in (final,note,seedpath,fiche,receipt):
        if p.exists() or p.with_name(p.name+'.pending').exists():raise FileExistsError(p)
    # Seed bytes remain local and never enter a printed result or tunnel note.
    if seedpath.parent.exists():raise FileExistsError('Prior private-directory attempt; explicit audit required')
    stable();acl_receipt=create_seed(seedpath)
    reg['blinding']['seed_commitment_sha256']=sha(seedpath)
    reg['blinding']['status']='PROCEDURAL_SAME_HOST_SEED_COMMITTED_NOT_UNBLINDED'
    reg['status']='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST'
    reg['registered_utc']=now.isoformat()
    reg['e7']['guard_pin_status']='PINNED_AT_FINAL_E2_REGISTRATION'
    reg['independent_review_files_sha256']=reviews
    reg['activation']={'receipt_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json',
      'review_application_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V1.json',
      'review_application_sha256':apppin,'sealer_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py',
      'sealer_sha256':sealer_pin}
    reg['registration_provenance']={'candidate_sha256':candidate_pin,'sealer_sha256':sealer_pin,
      'opening_sha256':opening_pin,'not_blind_design':True,'executed_science_by_this_sealing_step':False,
      'exposure_history':application['exposure_declaration'],
      'independence_scope':'Declared distinct builder/reviewer roles recorded in application; procedural same-host custody, no independent human custodian'}
    stable()
    create(final,reg);digest=sha(final)
    create(fiche,('[REAL — reaproveitamento E2; desenho NÃO-CEGO; exposição conforme declaração vinculada]\n\n'
      'Reutilizados E0/E1, metadados públicos, strain arquivado da calibração GW250114, priors e código de runtime instalados; pins integrais no registro. '
      'Preparados código e controles finitos independentes; nenhum posterior novo, PE, waveform física ou nulo de campanha executado por este selador. Histórico de exposição é declaração do principal vinculada ao censo, não prova de ausência global. '
      'Os testes de adaptador e conversão são sintéticos e não demonstram viabilidade de PE.\n\n'
      'PAGO: registro, seleção documental, guardas e compromisso de cegueira procedural. NÃO PAGO: campanha nula, piloto, calibração física, seleção normalizada, PE cega, teste e E7 extração. '
      'N/A — sem Lean; nenhum gate formal alterado.\n\n'
      f'Abertura `{opening_pin}`. Registro `{digest}`.\n').encode())
    lines=['[NÃO-CEGO — E2 registrado; campanhas e teste físico ainda NÃO PAGOS]', '',
      '# E2 — registro testemunhado antes dos dados novos', '',
      f'registro_sha256: {digest}',f'registered_utc: {datetime.now(timezone.utc).isoformat()}', '',
      f'Abertura vinculante `{opening.name}` — SHA256 `{opening_pin}`.',
      f'Ficha `{fiche.name}` — SHA256 `{sha(fiche)}`.', '',
      'PAGO: desenho, código integral pinado, critérios pré-análise, leituras paralelas, protocolo de cegueira e controles finitos. '
      'NÃO PAGO nesta nota: nulos de campanha, Kerr/piloto IMR, calibração de duas famílias, PE cega, normalização hierárquica e teste físico. '
      'A aplicação do GO existente está vinculada às revisões; só o recibo final E2_ACTIVATION_COMPLETE permite execução. Esta nota isolada não ativa o registro nem relata resultado científico.', '',
      f"O censo contém {len(reg['calibration_event_ids'])} identidades de calibração/exclusão de cegueira. "
      f"{sum(x['eligible'] is True and x['published_deformation_at_registration'] is False for x in reg['test_candidates'].values())} eventos elegíveis não foram localizados no escopo documental congelado; {sum(x['eligible'] is True and x['published_deformation_at_registration'] is False and x['data_quality_hold'] for x in reg['test_candidates'].values())} têm pendência de qualidade. "
      'Ausência no escopo não é ausência universal de publicação. Nova conferência documental precede cada admissão. '
      f"Os {len(reg['publication_census']['additional_published_exclusions'])} publicados fora do antigo corpus permanecem excluídos da rota cega; a exposição incidental descrita no censo fica preservada.", '',
      'Os alvos E0 não garantem 90% de poder após incorporar nuisance. A matriz E1 entra apenas como INPUT sintético. '
      f"O registro conserva {len(reg['readings'])} leituras, nenhuma escolhida, e proíbe offset fixo em zero como estatística de teste. "
      'Com gate sistemático vermelho não se declara significância física nem se combina eventos para uma descoberta.', '',
      f"Nulos: {len(reg['nulls']['cells'])} células pré-fixadas, {sum(x['draws'] for x in reg['nulls']['cells'].values()):,} desenhos sintéticos no total. "
      'Gaussianos e cauda t5 de medida com nuisance gaussiano têm interpretações distintas; os limites empíricos de resolução são reportados. '
      'Não equivalem a calibração física da pipeline.', '',
      f"Piloto GW250114: janela {reg['pe_jobs']['GW250114_PILOT']['duration_s']} s, fonte IMR e quatro deformações livres, priors INPUT; Kerr220/10M precede a execução IMR. "
      'A família alinhada pSEOBNRv4HM_PA difere do produto publicado precessante v5PHM. '
      'O limite temporal foi verificado nos cantos dos priors; o interior não é certificado por esse teste. '
      'Remanescente usa fit GR nomeado e redshift usa Planck18 externo INPUT; não são observáveis independentes.', '',
      'Cegueira procedural no mesmo computador: somente o compromisso SHA256 da seed fica no registro; logs e intermediários sem deslocamento permanecem privados. '
      'Não há custódia humana independente. Descegamento exige informação suficiente, gate sistemático verde e revisão vinculada ao conjunto.', '',
      f"Prazo rígido contínuo: `{budget['hard_deadline_utc']}`. E3.2 fixará alocação adicional com custo medido do piloto e testemunha própria antes de novos jobs. "
      'Nenhuma autorização para ultrapassar 40 h. Catálogos futuros: AWAITING_DATA.', '',
      'Tentativas e correções anteriores permanecem nas revisões: adaptador inicialmente rejeitado, janela de 8 s insuficiente, guardas de downloads, publicação, qualidade e payload reforçadas. '
      'Nenhuma dessas correções é resultado físico. N/A — sem Lean.', '',
      'Comandos previstos (WSL /opt/lal_env, dentro do prazo): `python -B bis/e2_code/null_campaign.py`; '
      '`python -B -O bis/e4_e5_prepare/deterministic_e4_e5.py --execute --authorization <ativação pinada>`; '
      '`python -B bis/e2_code/run_controlled.py --job GW250114_PILOT` somente após E3.1/Kerr e encerramento F0. '
      'Saídas existentes são recusadas. Reprodução exige destino isolado e novo registro explícito, não sobrescrita.', '',
      '## Revisões e código', '',f'- Registro — `{digest}`.',f'- Candidato — `{candidate_pin}`.',f'- Aplicação técnica do GO — `{apppin}`.']
    lines.extend(f'- `{n}` — `{pin}`.' for n,pin in reviews.items())
    lines.extend(f'- `bis/e2_code/{n}` — `{pin}`.' for n,pin in reg['own_code_tree_sha256'].items())
    create(note,('\n'.join(lines)+'\n').encode())
    stable()
    if datetime.now(timezone.utc)>=datetime.fromisoformat(budget['hard_deadline_utc']):raise TimeoutError('Deadline reached before activation; partial files retained')
    value={'status':'E2_ACTIVATION_COMPLETE','registration_sha256':digest,
      'witness_sha256':sha(note),'opening_sha256':opening_pin,'fiche_sha256':sha(fiche),
      'seed_commitment_sha256':reg['blinding']['seed_commitment_sha256'],
      'candidate_sha256':candidate_pin,'sealer_sha256':sealer_pin,'review_application_sha256':apppin,
      'executed_science_by_this_sealing_step':False,'seed_private_directory':acl_receipt,
      'finished_utc':datetime.now(timezone.utc).isoformat()}
    create(receipt,value);print(json.dumps(value))

if __name__=='__main__':main()
