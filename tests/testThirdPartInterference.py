import sys
from pathlib import Path
import unittest
import os

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))
sys.path.insert(0, str(thisDir))

class Tests(unittest.TestCase):
	def testThirdPartyInterference(self):
		self.etalon = [
		]

		from lazily.functools import partial
		import csv
		os.stat(csv.__file__)


if __name__ == "__main__":
	unittest.main()
