#All you need should be in this library, do not use another one
import numpy


def class Solver(object):

	#x : your symbol, either "1" or "2"
	#g : game engine
	def __init__(self,x,g):
		self.x = x
		self.g = g

	#m : a 2D integer numpy matrix which each cell is either 0,1 or 2
	#return the next move in a tuple (a,b) for which your own symbol 'x' will be placed, i.e. after this function call, m[a-1,b-1] = x if m[a-1,b-1] is valid and was = 0 before
	#(otherwise your turn will be skipped, beware !) 
	def solve(m):
		#Your magic code here
		return (1,1)

