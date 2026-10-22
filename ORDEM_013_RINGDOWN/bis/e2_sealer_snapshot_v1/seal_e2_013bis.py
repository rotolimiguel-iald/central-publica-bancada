"""Finalize the reviewed E2 candidate and its tunnel witness; never overwrite."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,ast

B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'

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
        ast.parse(p.read_text(encoding='utf-8-sig'));found[p.relative_to(root).as_posix()]=sha(p)
    return found

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True)
    ap.add_argument('--independent-review',action='append',required=True)
    ap.add_argument('--finalize-reviewed-candidate',action='store_true');args=ap.parse_args()
    if not args.finalize_reviewed_candidate:raise ValueError('Explicit finalization required')
    candidate=(B/'bis'/args.candidate).resolve()
    if not candidate.is_relative_to(B/'bis'):raise ValueError('Candidate outside bis')
    reg=json.loads(candidate.read_bytes())
    if reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Not a draft')
    if reg['own_code_tree_sha256']!=code_tree(B/'bis/e2_code'):raise ValueError('Own code changed after review candidate')
    for entry in reg['extra_code_roots']:
        p=(R/entry['relative_to_Chatgpt']).resolve()
        if not p.is_relative_to(R) or code_tree(p)!=entry['files_sha256']:raise ValueError('Extra code changed')
    for name,pin in reg['input_pins_relative_to_Chatgpt'].items():
        p=(R/name).resolve()
        if not p.is_relative_to(R) or sha(p)!=pin:raise ValueError('Input changed '+name)
    reviews={}
    for name in args.independent_review:
        p=(B/name).resolve()
        if not p.is_relative_to(B/'bis') or p.suffix not in ('.json','.md'):raise ValueError('Invalid review path')
        reviews[p.relative_to(B).as_posix()]=sha(p)
    if len(reviews)<3:raise ValueError('PE, main modules, and E7 independent reviews required')
    budget=json.loads((R/reg['budget_relative_to_Chatgpt']).read_bytes())
    now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(budget['hard_deadline_utc']):raise TimeoutError('Budget expired')
    opening=D/'ENTREGA_013BIS_ABERTURA_operador.md'
    final=B/'RINGDOWN_5SIGMA_V1.json';note=R/reg['witness_relative_to_Chatgpt']
    seedpath=R/reg['blinding']['seed_relative_to_Chatgpt'];fiche=B/'REAPROVEITAMENTO_AMPLIACAO_E2.md'
    receipt=B/'bis/E2_REGISTRATION_RECEIPT.json'
    for p in (final,note,seedpath,fiche,receipt):
        if p.exists() or p.with_name(p.name+'.pending').exists():raise FileExistsError(p)
    # Seed bytes remain local and never enter a printed result or tunnel note.
    create(seedpath,os.urandom(32));os.chmod(seedpath,0o600)
    reg['blinding']['seed_commitment_sha256']=sha(seedpath)
    reg['blinding']['status']='PROCEDURAL_SAME_HOST_SEED_COMMITTED_NOT_UNBLINDED'
    reg['status']='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST'
    reg['registered_utc']=now.isoformat()
    reg['e7']['guard_pin_status']='PINNED_AT_FINAL_E2_REGISTRATION'
    reg['independent_review_files_sha256']=reviews
    reg['registration_provenance']={'candidate_sha256':sha(candidate),'sealer_sha256':sha(Path(__file__)),
      'opening_sha256':sha(opening),'not_blind_design':True,'new_test_posterior_access_before_registration':False,
      'independence_scope':'Different builder and reviewer; procedural same-host custody, no independent human seed custodian'}
    create(final,reg);digest=sha(final)
    create(fiche,('[REAL — reaproveitamento E2; desenho NÃO-CEGO, dados novos de teste ainda não lidos]\n\n'
      'Reutilizados E0/E1, metadados públicos, strain arquivado da calibração GW250114, priors e código de runtime instalados; pins integrais no registro. '
      'Preparados código e controles finitos independentes; nenhum posterior novo, PE, waveform física ou nulo de campanha executado nesta selagem. '
      'Os testes de adaptador e conversão são sintéticos e não demonstram viabilidade de PE.\n\n'
      'PAGO: registro, seleção documental, guardas e compromisso de cegueira procedural. NÃO PAGO: campanha nula, piloto, calibração física, seleção normalizada, PE cega, teste e E7 extração. '
      'N/A — sem Lean; nenhum gate formal alterado.\n\n'
      f'Abertura `{sha(opening)}`. Registro `{digest}`.\n').encode())
    lines=['[NÃO-CEGO — E2 registrado; campanhas e teste físico ainda NÃO PAGOS]', '',
      '# E2 — registro testemunhado antes dos dados novos', '',
      f'registro_sha256: {digest}',f'registered_utc: {datetime.now(timezone.utc).isoformat()}', '',
      f'Abertura vinculante `{opening.name}` — SHA256 `{sha(opening)}`.',
      f'Ficha `{fiche.name}` — SHA256 `{sha(fiche)}`.', '',
      'PAGO: desenho, código integral pinado, critérios pré-análise, leituras paralelas, protocolo de cegueira e controles finitos. '
      'NÃO PAGO nesta nota: nulos de campanha, Kerr/piloto IMR, calibração de duas famílias, PE cega, normalização hierárquica e teste físico. '
      'A nota autoriza as execuções previstas; não relata seu resultado.', '',
      f"O censo contém {len(reg['calibration_event_ids'])} identidades de calibração/exclusão de cegueira. "
      f"{sum(x['eligible'] is True and x['published_deformation_at_registration'] is False for x in reg['test_candidates'].values())} eventos elegíveis não foram localizados no escopo documental congelado; quatro têm pendência de qualidade. "
      'Ausência no escopo não é ausência universal de publicação. Nova conferência documental precede cada admissão. '
      'Os nove publicados fora do antigo corpus permanecem excluídos da rota cega; a exposição incidental descrita no censo fica preservada.', '',
      'Os alvos E0 não garantem 90% de poder após incorporar nuisance. A matriz E1 entra apenas como INPUT sintético. '
      'O registro conserva as dez leituras, nenhuma escolhida, e proíbe offset fixo em zero como estatística de teste. '
      'Com gate sistemático vermelho não se declara significância física nem se combina eventos para uma descoberta.', '',
      f"Nulos: {len(reg['nulls']['cells'])} células pré-fixadas, {sum(x['draws'] for x in reg['nulls']['cells'].values()):,} desenhos sintéticos no total. "
      'Gaussianos e cauda t5 de medida com nuisance gaussiano têm interpretações distintas; os limites empíricos de resolução são reportados. '
      'Não equivalem a calibração física da pipeline.', '',
      'Piloto GW250114: janela 16 s, fonte IMR e quatro deformações livres, priors INPUT; Kerr220/10M precede a execução IMR. '
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
      '## Revisões e código', '',f'- Registro — `{digest}`.',f'- Candidato — `{sha(candidate)}`.']
    lines.extend(f'- `{n}` — `{pin}`.' for n,pin in reviews.items())
    lines.extend(f'- `bis/e2_code/{n}` — `{pin}`.' for n,pin in reg['own_code_tree_sha256'].items())
    create(note,('\n'.join(lines)+'\n').encode())
    value={'status':'E2_REGISTERED_WITNESSED_NO_SCIENCE_RUN_YET','registration_sha256':digest,
      'witness_sha256':sha(note),'opening_sha256':sha(opening),'fiche_sha256':sha(fiche),
      'seed_commitment_sha256':reg['blinding']['seed_commitment_sha256'],
      'candidate_sha256':sha(candidate),'sealer_sha256':sha(Path(__file__)),
      'finished_utc':datetime.now(timezone.utc).isoformat()}
    create(receipt,value);print(json.dumps(value))

if __name__=='__main__':main()
