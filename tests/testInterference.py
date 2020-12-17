import sys
from pathlib import Path
import unittest

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))
sys.path.insert(0, str(thisDir))

from ImportTimeline import ImportTimelineTestCase


class Tests(ImportTimelineTestCase):
	def testInterference(self):
		self.etalon = [
			"from lazilyTest2 import b",
			"lazilyTest2/__init__.py run",
			"lazilyTest2/b.py run",
			("lazilyTest1", False),
			("lazilyTest1.a", False),
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.a", True),
			("lazily.lazilyTest1.b", False),

			"from lazily.lazilyTest1 import a",
			("lazilyTest1", False),
			("lazilyTest1.a", False),
			("lazily.lazilyTest1", True),
			("lazily.lazilyTest1.a", True),
			("lazily.lazilyTest1.b", False)
		]

		self.log("from lazilyTest2 import b")
		from lazilyTest2 import b

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1.b")
		self.log("from lazily.lazilyTest1 import a")

		from lazily.lazilyTest1 import a

		self.assertInModulesStatus("lazilyTest1")
		self.assertInModulesStatus("lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1")
		self.assertInModulesStatus("lazily.lazilyTest1.a")
		self.assertInModulesStatus("lazily.lazilyTest1.b")


if __name__ == "__main__":
	unittest.main()
