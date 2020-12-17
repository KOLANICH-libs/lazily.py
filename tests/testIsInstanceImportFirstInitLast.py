import sys
from pathlib import Path
import unittest

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))
sys.path.insert(0, str(thisDir))

from ImportTimeline import ImportTimelineTestCase


class Tests(ImportTimelineTestCase):
	def testIsInstanceImportFirstInitLast(self):
		self.etalon = [
			"from lazily.lazilyTest1 import Abracadabra",

			"from lazilyTest1 import Abracadabra as AbracadabraTrue",
			"lazilyTest1/__init__.py run",
			"objectOfInitialClass = AbracadabraTrue()",
			"Abracadabra",
			"objectOfLazyClass = Abracadabra()",
			"Abracadabra",
		]

		self.log("from lazily.lazilyTest1 import Abracadabra")
		from lazily.lazilyTest1 import Abracadabra

		self.log("from lazilyTest1 import Abracadabra as AbracadabraTrue")
		from lazilyTest1 import Abracadabra as AbracadabraTrue

		self.log("objectOfInitialClass = AbracadabraTrue()")
		objectOfInitialClass = AbracadabraTrue()

		self.log("objectOfLazyClass = Abracadabra()")
		objectOfLazyClass = Abracadabra()

		self.assertIsInstance(objectOfLazyClass, AbracadabraTrue)
		self.assertIsInstance(objectOfInitialClass, Abracadabra)


if __name__ == "__main__":
	unittest.main()
