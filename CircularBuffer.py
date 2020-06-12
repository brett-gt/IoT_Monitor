class CircularBuffer(object):

	def __init__(self, size, data=[]):
		self.index = 0
		self.size = size
		self.data = list(data)[-size:]

	def append(self, value):
		if(len(self.data) == self.size):
			self.data[self.index] = value
		else:
			self.data.append(value)
		self.index = (self.index + 1) % self.size

	def get_oldest(self):
		if(len(self.data) == self.size):
			return (self.data[self.index % self.size])
		else:
			return (self.data[0])

	def __getitem__(self, key):
		if(len(self.data) == self.size):
			return (self.data[(key + self.index) % self.size])
		else:
			return (self.data[key])

	def __repr__(self):
		return self.data.__repr__() + ' (' + str(len(self.data)) + ' items)'
