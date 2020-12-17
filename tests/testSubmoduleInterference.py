import sys
from pathlib import Path
import unittest

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))
sys.path.insert(0, str(thisDir))

from ImportTimeline import ImportTimelineTestCase


class Tests(ImportTimelineTestCase):
	def testSimple(self):
		self.etalon = [
			"import lazily.lazilyTest1",

			("lazilyTest1", False),
			("lazilyTest1.submodule", False),
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.submodule", False),

			"lazily.lazilyTest1.initShit()", # causes initialization of lazily.lazilyTest1 with lazily
			"lazilyTest1/__init__.py run",
			"lazilyTest1.__init__.initShit is called",
			"from lazilyTest1.submodule import a",
			"lazilyTest1/submodule/__init__.py run",
			
			"a()",
			"lazilyTest1.submodule.a is run",

			("lazilyTest1", True),
			("lazilyTest1.submodule", True),
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.submodule", False),
			
			"from lazily.lazilyTest1.submodule import a",
			("lazilyTest1", True),
			("lazilyTest1.submodule", True),
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.submodule", True),
		]


		self.log("import lazily.lazilyTest1")
		import lazily.lazilyTest1

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.submodule")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.submodule")

		self.log("lazily.lazilyTest1.initShit()")
		lazily.lazilyTest1.initShit()

		self.log("from lazilyTest1.submodule import a")
		from lazilyTest1.submodule import a

		self.log("a()")
		a()

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.submodule")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.submodule")

		from lazily.lazilyTest1.submodule import a

		self.log("from lazily.lazilyTest1.submodule import a")
		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.submodule")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.submodule")


if __name__ == "__main__":
	unittest.main()
