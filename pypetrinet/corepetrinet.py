import functools
import numpy as np
import builtins
import networkx as nx

#http://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html#adding-attributes-to-graphs-nodes-and-edges

class PetriMoves:
	def __init__(self, inp, out):
		self.input = inp
		self.output = out

#Базовый класс для создания сети
class PetriNetPuppet:
	def __init__(self):
		pass
	def _createMatrix(self, size):
		return np.matrix([[0 for x in range(size)] for x in range(size)])
	def add_propetry(self, *args, **kwargs):
		pass
	def connect(self, obj1, obj2):
		pass


class PetriNetBuilder:
	def __init__(self):
		pass
	def addCount(self, count):
		pass

	def construct(self):
		return BasePetriNet()

class BasePetriNet(PetriNetPuppet):
	def __init__(self):
		self.graph = nx.Graph()
		super(BasePetriNet).__init__()

	def add_Properties(self, name, prop):
		'''
			prop in dict format
		'''
		for p in prop.keys():
			N = self.graph.node
			if not (name in N):
				raise Exception("This name not in base")
			N[name].update({p: prop[p]})
	def addStates(self, states):
		self._addElement(states, 'place')
	def addMoves(self, moves):
		self._addElement(moves, 'move')

	def _addElement(self, elements, param):
		[self.graph.add_node(elem, param=param) for elem in elements]

	#Соединяем полученные метки
	#places соединяем с moves
	def connectElements(self, node, inp, otp):
		[self.graph.add_edge(node, oelem) for oelem in otp]
		[self.graph.add_edge(inp, node) for inp in inp]

	def get(self, param, value):
		'''
			filter by propetries of node
		'''
		return list(filter(
			lambda x: param in self.graph.node[x] and 
			self.graph.node[x][param] == value, self.graph.node.keys()))



#ОБлегчённый доступ к объектам PetriNet
class PetriNetProxy:
	def __init__(self, pn):
		self.pn = pn



class PetriNet:
	'''
	S - state
	T - Transactions
	F - Задаёт дуги сети
	'''
	def __init__(self, S=None, T=None):
		self.pn = BasePetriNet()
		self._hidden(S, T)
		#Сеть второго рода
		self.parts2 = False

	def _hidden(self,S,T):
		self.pn.addStates(S)
		self.pn.addMoves(T)

	#Добавить свойство к определённому ноду
	def add_property(self, name, *args, **kwargs):
		if name != None:
			self.pn.add_Properties(name, kwargs)

	def add_state(self, *args, **kwargs):
		self.pn.add_state(**kwargs)

	def add_marker(self, name, position):
		pass

	#Может принимать значения типа
	#Добавить переход
	#('t1', 's1')
	#{'t1': ['s1', 's2']}
	#{}
	#input - Входящие в оператор перехода
	#Исходящие из оператора перехода
	#Входящие и исходящие могут быть обычными значениями, а могут быть в виде 
	#списка (n, id), где n, количество связей которые соединяют/исходят
	#от текущего перехода
	def connect(self, move_id, input_arr, output_arr):
		self.pn.connectElements(move_id, input_arr, output_arr)

	#Выявление конфликтов в сети
	def check_conflict(self):
		pass

	#Определение сети второго рода
	def addParts(self, data, N):
		self.parts2 = True

	#Подготовка к графическому представлению
	def web_output(self):
		paths=[]
		move = self.getMoves()
		delay = 300
		for petri_moves in move:
			paths.append(self._construct_path(petri_moves, delay))
			delay += 50
		return paths

	#Создание стрелок для выхода в вебе
	def _construct_path(self, petri_moves, delay):
		return 'M100 {0} H200 R20'.format(delay)

	def getPlaces(self):
		return self.pn.get('param', 'place')

	def getMoves(self):
		return self.pn.get('param', 'move')

	def isMarked(self, node):
		return node in self.pn.get('type', 'marked')