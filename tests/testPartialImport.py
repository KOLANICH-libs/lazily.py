import sys
from pathlib import Path
import unittest

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))
sys.path.insert(0, str(thisDir))

from ImportTimeline import ImportTimelineTestCase


class Tests(ImportTimelineTestCase):
	def testPartialImport(self):
		self.etalon = [
			"from lazily.lazilyTest1.a import b",

			("lazilyTest1", False),
			("lazilyTest1.a", False),
			("lazilyTest1.a.b", False), # b is not a module
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.a", True),
			("lazily.lazilyTest1.a.b", False), # b is not a module

			"b()",
			"lazilyTest1/__init__.py run",
			"lazilyTest1/a.py run",
			"lazilyTest1.a.b called",

			("lazilyTest1", True),
			("lazilyTest1.a", True),
			("lazilyTest1.a.b", False), # b is not a module
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.a", True),
			("lazily.lazilyTest1.a.b", False), # b is not a module

		]

		self.log("from lazily.lazilyTest1.a import b")
		from lazily.lazilyTest1.a import b

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.a")
		self.assertInModulesStatus("lazilyTest1.a.b")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1.a.b")

		self.log("b()")
		b()

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.a")
		self.assertInModulesStatus("lazilyTest1.a.b")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1.a.b")


if __name__ == "__main__":
	unittest.main()
