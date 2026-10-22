"""Documentary source/pin audit. Candidate and stdlib sources are text only."""
from pathlib import Path
import json,hashlib,ast,os
from datetime import datetime,timezone
BASE=Path(__file__).parent
SRC=BASE.parent/'guard_wsl_path_repair_preparation'
CONSUMED=BASE.parent/'guard_wsl_integration_preparation_v2'
checks=[]
def pin(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def check(name,ok,detail=None):
 checks.append(dict(name=name,ok=bool(ok),detail=detail))
 if not ok:raise RuntimeError(name)
def load(p):return json.loads(p.read_bytes())
def pinmatch(p,q):
 a=pin(p);return all(a[k]==q[k] for k in ('bytes','sha256'))
manifest=load(SRC/'MANIFESTO_PREPARACAO_CAMINHOS.json')
contract=load(SRC/'CONTRATO_INTERFACE_CAMINHOS.json')
inventory=load(SRC/'INVENTARIO_TOKENS.json')
examples=load(SRC/'EXEMPLOS_ESPERADOS_DADOS.json')
for q in manifest['artifacts']:check('manifestpin:'+Path(q['path']).name,pinmatch(Path(q['path']),q))
for row in inventory['sources']:
 q=row['source'];path=Path(q['path']);check('inventoriedsourcepin:'+path.name,pinmatch(path,q));lines=path.read_text(encoding='utf-8-sig').splitlines()
 for excerpt in row['relevant_lines']:check('inventoryline:'+path.name+':'+str(excerpt['line']),lines[excerpt['line']-1]==excerpt['text'])
 check('rootflagabsent:'+path.name,'--root' not in path.read_text(encoding='utf-8-sig'))
for row in inventory['observed']:
 q=row['source'];check('observedpin:'+Path(q['path']).name,pinmatch(Path(q['path']),q));data=load(Path(q['path']));check('observedargv_exact',row['argv']==data['argv']);check('observedbroken_index10',row['broken_script_token']==data['argv'][10])
old=(CONSUMED/'common.py').read_text(encoding='utf-8-sig')
new=(SRC/'common.py.candidate.txt').read_text(encoding='utf-8-sig');tree=ast.parse(new);check('candidate_AST_only',True)
assign={x.targets[0].id:x.value for x in tree.body if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name)}
root=assign['LINUX_ARGV_ROOT'];check('root_is_explicit_PurePosixPath',isinstance(root,ast.Call) and isinstance(root.func,ast.Name) and root.func.id=='PurePosixPath')
root_literal=root.args[0].value
check('literal_destination',root_literal==contract['interface']['destination_root'])
check('literal_restricted_POSIX_space',root_literal.startswith('/mnt/c/') and '\\' not in root_literal and 'Central de Patentes' in root_literal and '"' not in root_literal and "'" not in root_literal)
check('LINUX_concrete_io','LINUX = Path(LINUX_ARGV_ROOT.as_posix())' in new)
check('BASE_host_selected','BASE = WIN if os.name == "nt" else LINUX' in new)
check('script_token_pure_expression','(LINUX_ARGV_ROOT/script).as_posix()' in new and 'str(LINUX/script)' not in new)
check('rest_common_unchanged',new.replace('from pathlib import Path, PurePosixPath','from pathlib import Path').replace("LINUX_ARGV_ROOT = PurePosixPath("+repr(root_literal)+")\n# POSIX representation for transported tokens; concrete Path is only for host IO.\nLINUX = Path(LINUX_ARGV_ROOT.as_posix())",'LINUX = Path("'+root_literal+'")').replace('(LINUX_ARGV_ROOT/script).as_posix()','str(LINUX/script)')==old)
check('no_candidate_split_shell',all(x not in new for x in ['shell=True','shlex.split','urllib.parse','list2cmdline']))
roles={'--supervisor':'linux_control.py','--cleanup':'linux_control.py','--child':'worker.py'}
check('role_contract',contract['interface']['scripts']==roles)
for row in examples['examples']:
 if 'role' not in row:continue
 argv=row['expected_linux_argv'];role=row['role']
 check('examplepositions:'+role,len(argv)==10 and argv[:6]==['/opt/lal_env/bin/python','-I','-S','-B','-X','utf8'] and argv[7]==role and row['script_token_index']==6)
 check('exampletext:'+role,argv[6]==root_literal+'/'+roles[role],'Text comparison of frozen expectations; no constructor evaluation')
 check('future_placeholders:'+role,argv[8]=='<REQUEST_FUTURA_NAO_CRIADA>' and argv[9]=='<NONCE_FUTURO_NAO_CRIADO>')
 check('examples_not_launch:'+role,row['not_a_launch_command'] is True)
# Read the actual consumers: map all call sites rather than assuming AST equality is semantic evidence.
texts={name:(CONSUMED/name).read_text(encoding='utf-8-sig') for name in ['common.py','launch_windows.py','linux_control.py','worker.py']}
check('windows_outer_list','argv=[WSL,"--distribution","Ubuntu-24.04","--exec",*g.argv_for(mode,nonce)]' in texts['launch_windows.py'])
check('primary_cleanup_both_builder','launch(g,"--supervisor",nonce)' in texts['launch_windows.py'] and 'launch(g,"--cleanup",nonce)' in texts['launch_windows.py'])
check('Linuxchild_same_builder','argv=g.argv_for("--child",nonce)' in texts['linux_control.py'])
check('parent_identity_same_builder','g.matches(parent,g.argv_for("--supervisor",nonce))' in texts['worker.py'])
check('scoped_identity_same_builder','targets=[argv_for("--supervisor",nonce),argv_for("--child",nonce)]' in new)
check('fixed_PY_literal',assign['PY'].value=='/opt/lal_env/bin/python')
check('historical_request_not_new',assign['REQUEST'].value==contract['source_terminal_request_id'])
check('no_execution_contract',contract['new_execution_request_id'] is None and contract['new_authorization'] is False and contract['new_claim'] is False and contract['new_launcher'] is False)
for n in ['AUTORIZACAO_ROOT.json','CLAIM.json','RUN','RESULT.json','launch_windows.py','common.py']:check('candidate_package_absent:'+n,not (SRC/n).exists())
stdlib_paths={
 'Windows_pathlib':Path(r'C:\Python314\Lib\pathlib\__init__.py'),
 'Windows_posixpath':Path(r'C:\Python314\Lib\posixpath.py'),
 'Windows_subprocess':Path(r'C:\Python314\Lib\subprocess.py'),
 'Linux_pathlib':Path(r'\\wsl.localhost\Ubuntu-24.04\usr\lib\python3.12\pathlib.py'),
 'Linux_subprocess':Path(r'\\wsl.localhost\Ubuntu-24.04\usr\lib\python3.12\subprocess.py')}
std={name:path.read_text(encoding='utf-8-sig') for name,path in stdlib_paths.items()}
check('Windows_explicit_POSIX_parser','class PurePosixPath(PurePath):' in std['Windows_pathlib'] and 'parser = posixpath' in std['Windows_pathlib'])
check('Linux_explicit_POSIX_flavour','class PurePosixPath(PurePath):' in std['Linux_pathlib'] and '_flavour = posixpath' in std['Linux_pathlib'])
for tag in ['Windows_pathlib','Linux_pathlib']:
 check(tag+'_with_segments_keeps_class','return type(self)(*pathsegments)' in std[tag])
 check(tag+'_Path_host_dispatch',"cls = WindowsPath if os.name == 'nt' else PosixPath" in std[tag])
 check(tag+'_PurePath_only_abstract_dispatch',"if cls is PurePath:" in std[tag])
check('Windows_as_posix','return str(self).replace(self.parser.sep, \'/\')' in std['Windows_pathlib'])
check('Linux_as_posix',"return str(self).replace(f.sep, '/')" in std['Linux_pathlib'])
check('Windows_quotes_spaces', 'needquote = (" " in arg) or ("\\t" in arg) or not arg' in std['Windows_subprocess'])
check('Windows_Popen_list2cmdline','args = list2cmdline(args)' in std['Windows_subprocess'])
check('Linux_Popen_list','args = list(args)' in std['Linux_subprocess'] and 'self.pid = _fork_exec(' in std['Linux_subprocess'])
check('POSIX_join_separator','path += sep + b' in std['Windows_posixpath'])
# Freeze documentary evidence, including consumed results; no process inspection or launch.
evidence=[pin(path) for path in stdlib_paths.values()]+[pin(SRC/n) for n in ['MANIFESTO_PREPARACAO_CAMINHOS.json','CONTRATO_INTERFACE_CAMINHOS.json','common.py.candidate.txt','INVENTARIO_TOKENS.json','EXEMPLOS_ESPERADOS_DADOS.json']]+[pin(CONSUMED/n) for n in ['CLAIM.json','RESULT.json','EXEC_RESULT_OFFICIAL_TOOL.json','RUN/WSL_PROCESS.json','RUN/CLEANUP_WSL_PROCESS.json']]
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'STATIC_PATH_CANDIDATE_ACCEPTED_WITHOUT_DYNAMIC_VALIDATION','map_before_seq':533,'terminal_request_reference':contract['source_terminal_request_id'],'new_request_created':False,'source_manifest':pin(SRC/'MANIFESTO_PREPARACAO_CAMINHOS.json'),'check_count':len(checks),'checks':checks,'evidence_pins':evidence,'candidate_imports':0,'candidate_executions':0,'WSL_invocations':0,'path_constructor_evaluations_for_target':0,'hooks_or_controls':0,'authorizations_or_claims_created':0,'source_edits':0,'source_access_note':'Windows stdlib read locally; Linux pathlib/subprocess read only via two exact UNC files with restricted escalation after default denial. No WSL executable or Linux Python started.','limits':'Derived fixed literal/role semantics only. Actual wsl.exe destination argv and executable opening not measured; generic Windows/UNC conversion not claimed.'}
p=BASE/'RECIBO_REVISAO_CAMINHOS.json';assert not p.exists();raw=(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode();tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,p)
print(json.dumps({'check_count':len(checks),'receipt':pin(p),'source_manifest':pin(SRC/'MANIFESTO_PREPARACAO_CAMINHOS.json')},ensure_ascii=False))
