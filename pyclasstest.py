class club():
	def __init__(self,a):
		self.age=a
		print(self.age)
	def expected_points(self, gf, ga, m):
		p = m*3*(float(gf-ga)/float(ga+gf))
		return p
