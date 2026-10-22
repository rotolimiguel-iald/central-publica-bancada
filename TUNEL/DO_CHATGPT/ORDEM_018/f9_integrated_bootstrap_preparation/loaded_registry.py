"""Trusted, byte-pinned source loader and cooperative live-object registry.

Only invoked by a future reviewed bootstrap after original ROOT admission.
Captures actual objects immediately after executing exact source bytes. This is
not universal protection against a hostile native library or same-uid process.
"""
import ast
import importlib
import os
from pathlib import Path
import sys
import types
from posix_protocol import canonical, document, need, pinned, read_bytes, sha

class LoadedRegistry:
    def __init__(self, package, package_pins, runtime, policy, runtime_sha256):
        self.base=Path(package);self.pins=package_pins;self.runtime=runtime;self.policy=policy;self.runtime_sha256=runtime_sha256
        self.modules={};self.objects={};self.sources={}

    def load(self, role, filename, alias):
        need(alias not in sys.modules,'MODULE_ALIAS_ALREADY_PRESENT:'+alias)
        raw=pinned(str(self.base/filename),self.pins[filename],self.pins[filename]['bytes'])
        module=types.ModuleType(alias);module.__file__=str(self.base/filename)
        module.__package__='';module.__spec__=importlib.machinery.ModuleSpec(alias,loader=None,origin=module.__file__)
        sys.modules[alias]=module
        # compile receives exactly the bytes verified above, not a filename lookup.
        exec(compile(raw,module.__file__,'exec',dont_inherit=True),module.__dict__)
        self.modules[role]=module;self.sources[role]={'file':module.__file__,'sha256':sha(raw)}
        self._capture(role,module)
        return module

    def primitive(self, filename):
        # Exact AST node from the existing primitive; no historical main or data imports.
        raw=pinned(str(self.base/filename),self.pins[filename],self.pins[filename]['bytes'])
        tree=ast.parse(raw,filename=str(self.base/filename))
        node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='block_correlation')
        module=types.ModuleType('f9_integrated_stellar_primitive');module.__file__=str(self.base/filename)
        module.np=sys.modules['numpy'];sys.modules[module.__name__]=module
        code=compile(ast.Module(body=[node],type_ignores=[]),module.__file__,'exec',dont_inherit=True)
        exec(code,module.__dict__)
        self.modules['primitive']=module;self.sources['primitive']={'file':module.__file__,'sha256':sha(raw),'scope':'exact block_correlation AST only'}
        self._capture('primitive',module)
        return module.block_correlation

    def native_module(self, role, module):
        path=str(Path(module.__file__).absolute());pin=self.policy.read_pins[path]
        pinned(path,pin,max(1,pin['bytes']))
        self.modules[role]=module;self.sources[role]={'file':path,'sha256':pin['sha256']}
        # Native modules remain trusted/pinned; this records actual module identity.
        # The supplier and supervisor jointly check the temporary CAMB wrapper.
        self.objects[role]=[]

    def _capture(self, role, module):
        rows=[]
        for name,value in module.__dict__.copy().items():
            if isinstance(value,types.FunctionType) and value.__module__==module.__name__:
                rows.append((module,name,value,value.__code__))
            elif isinstance(value,type) and value.__module__==module.__name__:
                rows.append((module,name,value,None))
                for method,fn in value.__dict__.copy().items():
                    if isinstance(fn,(staticmethod,classmethod)):fn=fn.__func__
                    if isinstance(fn,types.FunctionType):rows.append((value,method,fn,fn.__code__))
        self.objects[role]=rows

    def check(self, deep=False):
        self.policy.checkpoint('LOADED_OBJECTS')
        for role,module in self.modules.items():
            need(sys.modules.get(module.__name__) is module,'LOADED_MODULE_REPLACED:'+role)
            for owner,name,expected,code in self.objects[role]:
                current=owner.__dict__[name]
                if isinstance(current,(staticmethod,classmethod)):current=current.__func__
                need(current is expected and (code is None or current.__code__ is code),'LOADED_OBJECT_REPLACED:'+role+'.'+name)
            if deep:
                raw=read_bytes(module.__file__,self.policy.read_pins[module.__file__]['bytes'])
                need(sha(raw)==self.sources[role]['sha256'],'LOADED_SOURCE_CHANGED:'+role)
        if deep:self.policy.verify_runtime_modules_and_maps()

    def receipt(self):
        self.check(deep=True)
        return canonical({'schema':'F9_ACTUAL_LOADED_OBJECTS_SCOPED_RECEIPT_V1',
            'source_loader':'compile exact verified bytes; retained live object/code identity',
            'modules':self.sources,'object_counts':{k:len(v) for k,v in self.objects.items()},
            'runtime_sha256':self.runtime_sha256,'evidence_scope':'TRUSTED_PYTHON_LOADER_AND_SAMPLED_NATIVE_MAPS',
            'native_syscall_interception':False,'native_file_operations':None,'native_network_operations':None})
