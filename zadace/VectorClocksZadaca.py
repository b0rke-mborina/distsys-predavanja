class VectorClock:
	def __init__(self):
		self._data = []

	def __iter__(self):
		for elem in self._data:
			yield elem

	def __repr__(self):
		return self._data

	def __str__(self):
		return str(self._data)

	def __add__(self, other):
		helperDict = {"A": 0, "B": 0, "C": 0}
		for item in self._data:
			helperDict[item[0]] += item[1]
		for item in other:
			if item[1] > helperDict[item[0]]:
				helperDict[item[0]] = item[1]
		return [(item, helperDict[item]) for item in helperDict if helperDict[item] != 0]
	
	def __lt__(self, other):
		helperDict = {"A": [], "B": [], "C": []}
		for key in helperDict.keys():
			for item in self._data:
				if item[0] == key: helperDict[key].append(item[1])
			for item in other:
				if item[0] == key:
					if len(helperDict[key]) < 1: helperDict[key].append(0)
					helperDict[key].append(item[1])
			if len(helperDict[key]) < 2: helperDict[key].append(0)
		return all(True if helperDict[key][0] < helperDict[key][1] else False for key in helperDict.keys())
	
	def __floordiv__(self, other):
		helperDict = {"A": [], "B": [], "C": []}
		for key in helperDict.keys():
			for item in self._data:
				if item[0] == key: helperDict[key].append(item[1])
			for item in other:
				if item[0] == key:
					if len(helperDict[key]) < 1: helperDict[key].append(0)
					helperDict[key].append(item[1])
			if len(helperDict[key]) < 2: helperDict[key].append(0)
		oneLower = any(True if helperDict[key][0] <= helperDict[key][1] else False for key in helperDict)
		oneHigher = any(True if helperDict[key][0] >= helperDict[key][1] else False for key in helperDict)
		return oneLower and oneHigher

	def increment(self, nodeName):
		if not any(True if item[0] == nodeName else False for item in self._data):
			self._data.append((nodeName, 1))
		else:
			index = [name for name, timestamp in self._data].index(nodeName)
			lst = list(self._data[index])
			lst[1] += 1
			self._data[index] = tuple(lst)
		pass

	def set(self, nodeName, timestampValue):
		if not any(True if item[0] == nodeName else False for item in self._data):
			self._data.append((nodeName, timestampValue))
		else:
			self._data = [(item[0], timestampValue) if item[0] == nodeName else item for item in self._data]
		pass

if __name__ == "__main__":

	v1 = VectorClock()
	v1.increment("A")  # uvećaj timestamp za node "A"
	v1.increment("B")  # uvećaj timestamp za node "B"

	v2 = VectorClock()
	v2.increment("C")
	v2.set("B", 2)  # postavi timestamp za node "B" na dvojku

	print(v1, v2)  # [('A', 1), ('B', 1)] [('C', 1), ('B', 2)]

	v3 = v1 + v2
	print(v3)  # [('A', 1), ('B', 2), ('C', 1)]

	print("Equal:       v1 == v1 \t", v1 == v1)  # True
	print("Not equal:   v1 != v2 \t", v1 != v2)  # True
	print("Before:      v1 < v2 \t", v1 < v2)    # False
	print("Concurrent:  v1 // v2 \t", v1 // v2)  # True
