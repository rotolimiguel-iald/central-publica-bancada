import sys,importlib.util,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE));sys.path.insert(0,str(Path(__file__).resolve().parent))
import iald_orchestrator
for name in ('request_controls','coordination'):
 spec=importlib.util.spec_from_file_location('iald_orchestrator.'+name,Path(__file__).parent/'iald_orchestrator'/(name+'.py'))
 module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;setattr(iald_orchestrator,name,module);spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromNames(['test_optional_work','test_coordination','test_transport','test_request_controls'])
result=unittest.TextTestRunner(verbosity=1).run(suite)
sys.exit(not result.wasSuccessful())
