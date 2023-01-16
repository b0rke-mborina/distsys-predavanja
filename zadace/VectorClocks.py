from collections import defaultdict
import json


class VectorClock:
	@classmethod
	def parse(class_, obj):
		retval = VectorClock(obj["node_label"])
		for k, v in obj["state"].items():
			retval.state[k] = v

		return retval

	def __init__(self, node_label):
		self.state = defaultdict(int)
		self.node_label = node_label

	def clone(self):
		retval = VectorClock(self.node_label)
		for k, v in self.state.items():
			retval.state[k] = v

		return retval

	def increment(self):
		self.state[self.node_label] += 1

	def set(self, node, value):
		if value > self.state[node]:
			self.state[node] = value

	def __repr__(self):
		return str(sorted(list(self.state.items()), key=lambda x: x[0]))

	def __add__(a, b):
		result = VectorClock(a.node_label)
		for node, counter in a.state.items():
			result.set(node, counter)
		for node, counter in b.state.items():
			result.set(node, counter)
		return result

	def __eq__(a, b):
		return a.state == b.state

	def __neq__(a, b):
		return not a == b

	def __le__(a, b):
		keys = set(a.state.keys()).union(set(b.state.keys()))
		return all(a.state[k] <= b.state[k] for k in keys)

	def __lt__(a, b):
		return a <= b and a != b

	def __floordiv__(a, b):
		return not a <= b


if __name__ == "__main__":

	v1 = VectorClock("A")
	v1.increment()
	v1.increment()

	v2 = VectorClock("B")
	v2.increment()
	v2.set("B", 2)

	print(v1, v2)

	v3 = v1 + v2
	print(v3)

	print("Equal:       v1 == v1 \t", v1 == v1)  # True
	print("Not equal:   v1 != v2 \t", v1 != v2)  # True
	print("Before:      v1 < v2 \t", v1 < v2)  # False
	print("Concurrent:  v1 // v2 \t", v1 // v2)  # True