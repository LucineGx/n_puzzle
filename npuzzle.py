import sys
from my_colors import *

# Generate the final state the puzzle should attempt

def get_final_state(size) :
	l = (size * size) * [0]
	x = 0
	y = 0
	d = "right"

	for n in range(1, size * size) :
		l[size * x + y] = n

		if d == "right":
			if y == size - 1 or l[size * x + y + 1] <> 0 :
				d = "down"
				x += 1
			else :
				y += 1

		elif d == "down" :
			if x == size - 1 or l[size * (x + 1) + y] <> 0 :
				d = "left"
				y -= 1
			else :
				x += 1

		elif d == "left" :
			if y == 0 or l[size * x + y - 1] <> 0 :
				d = "up"
				x -= 1
			else :
				y -= 1

		elif d == "up" :
			if l[size * (x - 1) + y] <> 0 :
				d = "right"
				y += 1
			else :
				x -= 1
	return (l)

# Calculate the heuristic cost of the state with extended Manhattan distance

def count_heuristic(size, state, cost, goal) :
	heuristic = 0

	for n in range(1, size * size) :
		i = state.index(n)
		ig = goal.index(n)
		heuristic += abs(i / size - ig / size) + abs(i % size - ig % size)

	return (heuristic)

# Get lower cost state in OpenList, put its neighbours in openList, put state in ClosedList

def treat_state(openl, fs) :
	print("ok")

# Read the file and create the Open list wih the initial state

def read_file(f) :
	size = 0
	state = []
	openl = []

	for line in f :
		if line[0] == '#' :
			pass
		elif size == 0 :
			size = int(line)
		else :
			state.extend(line.replace('\n', '').split(' '))

	state = filter(None, state)
	state = map(int, state)
	fs = get_final_state(size)
	openl.append((state, 0, count_heuristic(size, state, 0, fs)))
	treat_state(openl, fs)

# Checks input and calls reading function

if __name__ == '__main__' :
	if len (sys.argv) == 2 :
		try :
			f = open(sys.argv[1])
			read_file(f)

		except IOError as e :
			sys.stdout.write(RED)
			print("'" + sys.argv[1] + "' : " + e.args[1])
			sys.stdout.write(RESET)
			print("To create a puzzle, you may use the generator")

#		except Exception as e :
#			sys.stdout.write(RED)
#			print("Something went wrong : " + e.args[1])

	else :
		print("usage : python npuzzle.py [file]")