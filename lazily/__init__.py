__all__ = ("lazyImport", "Hook")
import sys
import traceback
import functools
import importlib
import importlib.abc
from importlib._bootstrap import _find_spec
from importlib._bootstrap_external import PathFinder
import inspect
import lazy_object_proxy


_lazilyGlobals = globals()



def ProxyWithWorkaround_(factory, **_delayed):
	class ProxyWithWorkaround(lazy_object_proxy.Proxy):
		"""A lazy_object_proxy class working around some `importlib._bootstrap` shit triggering importing of packages even if it was not requested"""

		def __getattr__(self, key):
			#print("__getattr__", _delayed is not None, key)
			spr = super()
			if _delayed is not None:
				if key in _delayed:
					return _delayed[key]
				else:
					s = traceback.extract_stack()[-2]
					#print(s.name, s.name=="_handle_fromlist")
					#print(s.filename, s.filename=="<frozen importlib._bootstrap>")
					
					if s.name == "_handle_fromlist":
						_bootstrapShitTriggers = (s.filename == "<frozen importlib._bootstrap>") #_bootstrap shit triggering importing of packages even if it was not requested
						try:
							# assertions are removed via optimization, this check is needed for interpreter with patched FrozedTable (useful for debugging this shit)
							assert s.filename.endswith("importlib\\_bootstrap_external.py") # Windows
							assert s.filename.endswith("importlib/_bootstrap_external.py") # Linux
						except :
							_bootstrapShitTriggers = True
						
						if _bootstrapShitTriggers : 
							return ProxyWithWorkaround_(lambda: spr.__getattr__(key))
					else:
						return lazy_object_proxy.Proxy(lambda: spr.__getattr__(key))
						#print("key", key)
						#return spr.__getattr__(key)
			else:
				return lazy_object_proxy.Proxy(lambda: spr.__getattr__(key))

		def __setattr__(self, key, value):
			if _delayed is not None:
				_delayed[key] = value
			else:
				super().__setattr__(key, value)

	@functools.wraps(factory)
	def factory1(*args, **kwargs):
		nonlocal _delayed
		#from traceback import print_stack
		#print_stack()
		res = factory(*args, **kwargs)
		#if _delayed is not None:
		#	for k, v in _delayed.items():
		#		setattr(res, k, v)
		#	_delayed = None
		return res
	res = ProxyWithWorkaround(factory1)
	return res


ProxyWithWorkaround = ProxyWithWorkaround_


class Hook:
	__slots__ = ("moduleImporter", "modulePostProcessor", "propertyPostProcessor")

	def __init__(self, moduleImporter=None, modulePostProcessor=None, propertyPostProcessor=None):
		self.moduleImporter = moduleImporter
		self.modulePostProcessor = modulePostProcessor
		self.propertyPostProcessor = propertyPostProcessor

	def __iadd__(self, other):
		for k in __class__.__slots__:
			v = getattr(other, k)
			if v:
				setattr(self, k, v)
		return self


def neutralHook(importedModule):
	return importedModule


def postProcessPandas(pandas):
	if "tqdm" in sys.modules:
		from tqdm.auto import tqdm

		tqdm.pandas()
	return pandas


hooks = {"pandas": Hook(modulePostProcessor=postProcessPandas)}


def getOuterFrame():
	frame = inspect.currentframe()
	stack = traceback.extract_stack()
	for frameSumm in reversed(stack):
		if frameSumm.filename != __file__:
			break
		frame = frame.f_back
	return (frame, frameSumm)


def genImporterFunc(name, package=None, fromlist=(), *args, **kwargs):
	h = Hook(moduleImporter=None, modulePostProcessor=neutralHook, propertyPostProcessor=neutralHook)
	if name in hooks:
		h += hooks[name]

	if not package and name[0] == ".":
		(frame, frameSumm) = getOuterFrame()
		package = frame.f_globals["__package__"]

	if h.moduleImporter is None:
		h.moduleImporter = functools.partial(importlib.import_module, name, package, *args, **kwargs)

	def readyModuleImporter():
		prepName = LazyImporter.marker + name #dot is included into marker
		#traceback.print_stack()
		#print(groups.Fore.lightgreenEx("prepName")+' "' + groups.Fore.lightcyanEx(prepName) + '"' + " in sys.modules :", prepName in sys.modules)
		#print(groups.Fore.lightgreenEx("name")+' "' + groups.Fore.lightcyanEx(name) + '"' + " in sys.modules :", name in sys.modules)

		return h.modulePostProcessor(h.moduleImporter())

	if fromlist:
		def readyPropertyImporter():
			module = readyModuleImporter()
			res = []
			for nm in fromlist:
				res.append(h.propertyPostProcessor(getattr(module, nm)))
			if len(res) == 1:
				return res[0]
			else:
				return tuple(res)
		#print("func is readyPropertyImporter", readyPropertyImporter)
		return readyPropertyImporter
	else:
		#print("func is readyModuleImporter", readyModuleImporter)
		return readyModuleImporter


def lazyImport(name, package=None, fromlist=(), *args, **kwargs):
	"""Imports lazily"""
	return ProxyWithWorkaround(genImporterFunc(name, package, fromlist, *args, **kwargs))

#from RichConsole import groups

class LazyImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
	__slots__ = ("failImmediately",)
	marker = __name__ + "."

	def __init__(self, *args, failImmediately=False, **kwargs):
		super().__init__(*args, **kwargs)
		self.failImmediately = failImmediately

	def find_spec(self, fullName, path, target=None, *args, **kwargs):
		#print(groups.Fore.lightredEx("find_spec")+" "+groups.Fore.lightcyanEx(fullName), path, target, args, kwargs)
		if not fullName.startswith(__class__.marker):
			#import traceback
			#traceback.print_stack()
			return None
		else:
			trueName = fullName[len(__class__.marker):]
			#print("trueName", trueName)
			trueNameComponents = trueName.split(".")
			#print(trueNameComponents)
			
			try:
				if len(trueNameComponents) == 1:
					origSpec = importlib.util.find_spec(trueName)
				else:
					origSpec = _find_spec(trueName, sys.modules[__class__.marker+".".join(trueNameComponents[:-1])].__path__) # should not trigger loading, since worked aroung. Workaround is needed not only here, so we cannot remove it
					#origSpec = None # if it is a submodule we don't search for a spec, it triggers executing
			except:
				if not self.failImmediately:
					origSpec = None
				else:
					raise
			
			if origSpec:
				spec = importlib.machinery.ModuleSpec(
					name=fullName,
					loader=self,
					origin=origSpec.origin,
					loader_state=None,
				)
				spec.submodule_search_locations=origSpec.submodule_search_locations
			else:
				if self.failImmediately:
					raise ImportError("Could not import `"+trueName+"`: `origSpec` is None, which may mean there is no such a module")
				else:
					spec = importlib.machinery.ModuleSpec(
						name=fullName,
						loader=self,
					)
			
			spec.has_location = False
			spec.trueName = trueName
			return spec

	def create_module(self, spec, *args, **kwargs):
		#print(groups.Fore.lightredEx("create_module") + ' "' + groups.Fore.lightcyanEx(spec.name) + '"' + " in sys.modules :", spec.name in sys.modules)
		return None

	def exec_module(self, module, *args, **kwargs):
		trueName = module.__spec__.name[len(__class__.marker):]
		#print(groups.Fore.lightredEx("exec_module")+' "' +groups.Fore.lightcyanEx(module.__spec__.name) + '"' + " in sys.modules :", module.__spec__.name in sys.modules, '"' + groups.Fore.lightcyanEx(trueName) + '"' + " in sys.modules :", trueName in sys.modules)
		#print("module.__spec__.origin", module.__spec__.submodule_search_locations)
		mod = ProxyWithWorkaround(genImporterFunc(trueName), __spec__=module.__spec__, __file__=None, __path__=module.__spec__.submodule_search_locations)
		#mod = ProxyWithWorkaround(genImporterFunc(trueName), __spec__=module.__spec__, __file__=module.__spec__.submodule_search_locations)
		#mod = __import__(trueName)
		#print("exec_module", trueName, "mod", "(", mod, ")")
		sys.modules[module.__spec__.name] = mod
		return mod


def findPathFinderIndex():
	for i, v in enumerate(sys.meta_path):
		if v is PathFinder:
			return i

_importer = LazyImporter()
sys.meta_path.insert(findPathFinderIndex(), _importer)