import sys
from my_colors import *

# !! Verifie le parsing de securite à appliquer sur le fichier entrant

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

# End the program because no solution could be find

def negativ_end() :
	print("Open list is empty, no solution has been found")

# Solution found, retrace the path and end it

def positiv_end() :
	print("Final state obtained. Still need a function to retrace the whole path")

# Check presence of new state in both list, then put it in the open one

def check_new(new, openL, closedL, cost) :
	for elem in closedL :
		if elem[0] == new :
			if elem[1] <= cost + 1 :
				return(False)
			else :
				closedL.remove(elem)
				break
	for elem in openL :
		if elem[0] == new :
			if elem[1] <= cost + 1 :
				return(False)
			else :
				openL.remove(elem)
				break
	return(True)

# Calculate the heuristic cost of the state with extended Manhattan distance

def count_total_cost(current_s, final_s, size, cost) :
	total = cost

	for n in range(1, size * size) :
		c_i = current_s.index(n)
		f_i = final_s.index(n)
		# heuristic depends on Mahattan distance : |Xa - Xb| + |Ya - Yb| 
		total += abs(c_i / size - f_i / size) + abs(c_i % size - f_i % size)

	return (total)

# Get lower cost state in OpenList, put its neighbours in openList, put state in ClosedList

def treat_node(open_l, open_d, closed_d, final_s, size) :
	if len(openL) == 0 :
		negativ_end()
	openL.sort(key = lambda x : x[1])

	s = openL[0]
	if s[0] == fs :
		positiv_end()

	else :
		i = s[0].index(0)
		if (i >= size) :
			new = s[0][:]
			new[i] = new[i - size]
			new[i - size] = 0
			if check_new(new, openL, closedL, s[1]) :
				openL.append((new, s[1] + 1, count_heuristic(size, new, s[1] + 1, fs)))

		if ((i + 1) % size <> 0) :
			new = s[0][:]
			new[i] = new[i + 1]
			new[i + 1] = 0
			if check_new(new, openL, closedL, s[1]) :
				openL.append((new, s[1] + 1, count_heuristic(size, new, s[1] + 1, fs)))

		if (i/size <> size - 1) :
			new = s[0][:]
			new[i] = new[i + size]
			new[i + size] = 0
			if check_new(new, openL, closedL, s[1]) :
				openL.append((new, s[1] + 1, count_heuristic(size, new, s[1] + 1, fs)))

		if (i%size <> 0) :
			new = s[0][:]
			new[i] = new[i - 1]
			new[i - 1] = 0
			if check_new(new, openL, closedL, s[1]) :
				openL.append((new, s[1] + 1, count_heuristic(size, new, s[1] + 1, fs)))

		closedL.append(s)
		del openL[0]
		print("OPEN : " + str(len(openL)) + " | CLOSED : " + str(len(closedL)))
		if len(closedL) < 995 :
			treat_state(size, openL, fs, closedL)

# Create our list storages, and add the initial state as a first node in the open list

def read_file(f) :
	size = 0
	initial_s = []
	for line in f :
		if line[0] == '#' :
			pass
		elif size == 0 :
			size == int(line)
		else :
			# remove \n in line then split it into numbers and add them on the initial state list
			initial_s.extend(line.replace('\n', '').split(' '))
	# the split function may create empty elements in the list, let's remove them
	initial_s = filter(None, initial_s)
	# just need to convert all those values into int type
	initial_s = map(int, initial_s)

	open_l = []
	open_d = {}
	closed_d = {}
	final_s = get_final_state(size)
	initial_c = count_total_cost(initial_s, final_s, size, 0)
	# add initial state to both open list forms (list and dictionnary) 
	open_l.append((initial_s, initial_c))
	open_d[tuple(initial_s)] = (0, 0, initial_c)
	treat_node(open_l, open_d, closed_d, final_s, size)

# Checks input and calls reading function

if __name__ == '__main__' :
	if len (sys.argv) == 2 :
		try :
			f = open(sys.argv[1])

		except IOError as e :
			sys.stdout.write(RED)
			print("'" + sys.argv[1] + "' : " + e.args[1])
			sys.stdout.write(RESET)
			print("To create a puzzle, you may use the generator")

		except Exception as e :
			sys.stdout.write(RED)
			print("Something went wrong : " + e.args[1])

		else :
			read_file(f)

	else :
		print("usage : python npuzzle.py [file]")