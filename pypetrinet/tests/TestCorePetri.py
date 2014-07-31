import sys
sys.path.append("../")
import unittest
from corepetrinet import PetriNet

class TestCorePetri(unittest.TestCase):
	"""docstring for TestCorePetri"""
	def setUp(self):
		self.petri = PetriNet(['s1', 's2', 's3', 's4'], ['t1', 't2', 't3'])
	def test_add_node(self):
		self.assertSequenceEqual (self.petri.getPlaces(), ['s4', 's3', 's2', 's1'] )

	def test_makred_node(self):
		self.petri.add_property('s1', type='marked')
		self.assertTrue(self.petri.isMarked('s1'))


if __name__ == '__main__':
	unittest.main()
