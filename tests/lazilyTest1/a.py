from ImportTimeline import log

log("lazilyTest1/a.py run")
import traceback

#traceback.print_stack()


def b():
	log("lazilyTest1.a.b called")

def getSourceFile():
	log("lazilyTest1.a.getSourceFile called")
	from inspect import currentframe, getsourcefile
	print("lazilyTest1.a.getFrameInfo called: "+str(getsourcefile(currentframe().f_back)))