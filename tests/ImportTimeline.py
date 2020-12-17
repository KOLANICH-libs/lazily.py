__all__ = ("log",)

import sys
from unittest import TestCase

from sideBySideDiff import sideBySideDiff

timeline = []

#from RichConsole import groups


def log(msg: str, testInitiated: bool=False):
	#print((groups.Fore.lightcyanEx if testInitiated else groups.Fore.lightgreenEx)(msg))
	timeline.append(msg)


class ImportTimelineTestCase(TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.etalon = None

	def log(self, msg):
		log(msg, True)
		self.assertTimeline()

	def assertTimeline(self):
		if timeline != self.etalon[: len(timeline)]:
			for l in sideBySideDiff(self.etalon[: len(timeline)], timeline, names=("Etalon", "Real")):
				print(l)
		self.assertEqual(timeline, self.etalon[: len(timeline)])

	def assertInModulesStatus(self, moduleName):
		self.log((moduleName, moduleName in sys.modules))