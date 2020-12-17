from ImportTimeline import log

log("lazilyTest1/__init__.py run")
import traceback

#traceback.print_stack()


def initShit():
	log("lazilyTest1.__init__.initShit is called")


class Abracadabra:
	__slots__ = ("a",)

	def __init__(self):
		self.a = 1
		log(self.__class__.__name__, "constructed")