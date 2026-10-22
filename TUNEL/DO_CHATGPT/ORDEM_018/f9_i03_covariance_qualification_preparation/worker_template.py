"""Source template inserted into the supervised driver; not executed here."""
def worker(args):
    import ast
    contract,lineage,runtime,msha,dsha=validate(args.decision_sha256)
    out=ROOT/'execution_once';claim,_=read(ROOT/'RUN_CLAIM.json')
    need(claim['nonce']==args.nonce and claim['supervisor_pid']==os.getppid() and claim['request_id']==RID,'WORKER_PARENT_CLAIM')
    need(claim['manifest_sha256']==msha and claim['decision_sha256']==dsha,'WORKER_CLAIM_PINS')
    exclusive(out/'WORKER_STARTED.json',{'request_id':RID,'pid':os.getpid(),'ppid':os.getppid(),'nonce':args.nonce})
    start=time.monotonic();deadline=start+contract['budgets']['worker_cooperative_seconds']
    need(not any(n=='numpy' or n.startswith('numpy.') for n in sys.modules),'EARLY_NUMPY_IMPORT')
    sys.path.append(runtime['site'])
    dll_handle=os.add_dll_directory(str(Path(runtime['site'])/'numpy.libs'))
    attestation={}
    try:
        import numpy as np
        need(np.__version__==runtime['numpy_version_metadata'],'NUMPY_VERSION')
        need(Path(np.__file__).resolve()==Path(runtime['site'])/'numpy/__init__.py','NUMPY_LOCATION')
        sources=contract['sources']
        support=load_module('singular_gaussian_v2',sources['support'],attestation)
        linear=load_module('linear_gaussian',sources['backend'],attestation)
        consumer=load_module('f9_i03_consumer',sources['consumer'],attestation)
        builder=load_module('f9_i03_builder',sources['builder'],attestation)
        helpers=load_module('f9_i03_fixture_helpers',sources['helpers'],attestation)
        # Reuse the exact original callable body without importing its old main
        # module, sys.path side effect, audit_inputs or historical error inputs.
        prim=types.ModuleType('f9_stellar_primitive');prim.__file__=sources['primitive']['path'];prim.np=np
        sys.modules[prim.__name__]=prim
        tree=ast.parse(checked(sources['primitive']),filename=prim.__file__)
        definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='block_correlation']
        need(len(definitions)==1 and not definitions[0].decorator_list,'PRIMITIVE_AST_SELECTION')
        projection=ast.Module(body=definitions,type_ignores=[])
        exec(compile(projection,prim.__file__,'exec',dont_inherit=True,optimize=0),prim.__dict__)
        need(prim.block_correlation.__globals__['np'] is np and linear.np is np and support.np is np
             and linear.SupportGaussian is support.SupportGaussian,'INJECTED_RUNTIME_BINDINGS')
        attestation[prim.__name__]={'source':sources['primitive'],'loader':'AST projection of original block_correlation only; original line numbers retained',
              'first_line':definitions[0].lineno,'last_line':definitions[0].end_lineno,
              'original_top_level_executed':False,'original_main_executed':False,'numpy_global_identity':True}
        manifest,_=read(ROOT/'MANIFESTO_PREPARACAO.json')
        case_pin=next(r for r in manifest['members'] if Path(r['path']).name=='cases.py')
        cases=load_module('f9_i03_cases',case_pin,attestation)
        need(builder.REQUEST_ID=='f200dee1-0ecf-4a51-9b38-4c32d7eb0696'
             and consumer.REQUEST_ID=='a9874f79-9d71-48f5-824c-d51d6d819534','CANDIDATE_IDENTITIES')
        need(builder.METADATA_SHA256==sources['metadata']['sha256'],'BUILDER_METADATA_IDENTITY')
        meta=json.loads(checked(sources['metadata']));layout=json.loads(checked(sources['layout']));design=json.loads(checked(sources['design']))
        new_json(out/'LOADED_SOURCE_ATTESTATION.json',{'request_id':RID,'python_version':sys.version,
             'sources':attestation,'runtime_inventory_sha256':contract['runtime']['sha256'],
             'numpy_import':audit_loaded(runtime),'cross_process_marshal_identity_claimed':False,
             'helper_scope':['structure_from_documents','make_packet','serialization helpers'],'old_run_called':False})
        def emit(name,record):
            need(time.monotonic()<deadline,'COOPERATIVE_DEADLINE')
            need(name in {c+s for c in contract['case_order'] for s in ('_STARTED','_RESULT')},'OUTPUT_NAME')
            return new_json(out/(name+'.json'),record)
        result=cases.run(np,builder,prim.block_correlation,consumer,linear.FlatNuisanceGaussian,helpers,
            contract,meta,layout,design,{'artifact_sha256':contract['runtime']['sha256'],
            'clause':RID+'/runtime-bytes-rechecked','status':'SYNTHETIC_FIXTURE'},emit,deadline)
        need(result['status']=='PASS' and len(result['cases'])==6,'CASE_COMPLETENESS')
        for rec in list(contract['sources'].values())+lineage['inherited']:checked(rec)
        new_json(out/'LOADED_ORIGINS_AFTER.json',audit_loaded(runtime))
        result.update(manifest_sha256=msha,decision_sha256=dsha,worker_seconds=time.monotonic()-start)
        need(time.monotonic()<deadline,'WORKER_DEADLINE_AT_COMMIT')
        new_json(out/'RESULT.json',result)
    finally:dll_handle.close()
