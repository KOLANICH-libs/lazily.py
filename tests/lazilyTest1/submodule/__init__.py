from ImportTimeline import log

log("lazilyTest1/submodule/__init__.py run")
import traceback

#traceback.print_stack()
def a():
	log("lazilyTest1.submodule.a is run")