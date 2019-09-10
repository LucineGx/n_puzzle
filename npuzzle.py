import sys
from my_colors import *
sys.setrecursionlimit(10000)
# Note : c for cost, d for dictionary, f for file, i for index, l for list, s for state, t for tuple

final_s = []
size = 0

def print_puzzle(state) :
	s = ""
	i = 0

	while i < size * size :
		if (i % size == 0) :
			s += "\n"
		s += str(state[i]) + " "
		i += 1

	print(s)


# Generate the final state the puzzle should attempt

def get_final_state() :
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

	global final_s
	final_s = l

# End the program because no solution could be find

def negativ_end() :
	print("Open list is empty, no solution has been found")

# Solution found, retrace the path and end it

def positiv_end(final_elem, closed_d, step) :

	from_t = final_elem[0]
	if (from_t <> 0) :
		print_puzzle(from_t)
		if (closed_d.has_key(from_t)) :
			positiv_end(closed_d[from_t], closed_d, step + 1)
		else :
			print("Something went wrong, path is lost")
	else :
		print("Final state obtained. Function to retrace the whole path in construct..")
		print(str(step) + " moves to solve this puzzle")

# Add the element at the right place in the list, so it doesn't need to be sorted

def insert_into_open_list(open_l, new_s, new_c) :
	for i in range(0, len(open_l)) :
		if new_c > open_l[i] :
			break
	open_l.insert(i, (new_s, new_c))

# Check presence of new state in both list, then put it in the open one

def check_new_node(new_t, current_c, open_l, open_d, closed_d, from_t) :
	if closed_d.has_key(new_t) :
		return (False)

	elif open_d.has_key(new_t) :
		# Compare old recorded cost and the new one, makes the change if needed
		if open_d[new_t][1] > current_c :
			new_c = count_total_cost(new_t, current_c)
			open_d[new_t] = (from_t, current_c, new_c)

			for i, elem in enumerate(open_l) :
				if (elem[0] == new_t) :
					open_l[i] = (list(new_t), new_c)


		return(False)

	return(True)

# Calculate the heuristic cost of the state with Manhattan distance applied to

def count_total_cost(new_s, cost) :
	total = cost

	for n in range(1, size * size) :
		c_i = new_s.index(n)
		f_i = final_s.index(n)
		# Mahattan distance : |Xa - Xb| + |Ya - Yb| . X being the starting point and Y the goal
		total += abs(c_i / size - f_i / size) + abs(c_i % size - f_i % size)

	return (total)

# Get lower cost state in OpenList, put its neighbours in openList, put state in ClosedList

def treat_node(open_l, open_d, closed_d) :
	if len(open_l) == 0 :
		negativ_end()

	elif open_l[0][0] == final_s :
		print_puzzle(final_s)
		positiv_end(open_d[tuple(final_s)], closed_d, 0)

	else :
		s = open_l[0]
#		print_puzzle(s[0])
		i = s[0].index(0)
		tuple_s = tuple(s[0])
		elem = open_d[tuple_s]

		if (i >= size) :
			new_s = s[0][:]
			new_s[i] = new_s[i - size]
			new_s[i - size] = 0
			if check_new_node(tuple(new_s), elem[1] + 1, open_l, open_d, closed_d, tuple_s) :
				new_c = count_total_cost(new_s, elem[1] + 1)
				insert_into_open_list(open_l, new_s, new_c)
				open_d[tuple(new_s)] = (tuple_s, elem[1] + 1, new_c)

		if ((i + 1) % size <> 0) :
			new_s = s[0][:]
			new_s[i] = new_s[i + 1]
			new_s[i + 1] = 0
			if check_new_node(tuple(new_s), elem[1] + 1, open_l, open_d, closed_d, tuple_s) :
				new_c = count_total_cost(new_s, elem[1] + 1)
				insert_into_open_list(open_l, new_s, new_c)
				open_d[tuple(new_s)] = (tuple_s, elem[1] + 1, new_c)

		if (i/size <> size - 1) :
			new_s = s[0][:]
			new_s[i] = new_s[i + size]
			new_s[i + size] = 0
			if check_new_node(tuple(new_s), elem[1] + 1, open_l, open_d, closed_d, tuple_s) :
				new_c = count_total_cost(new_s, elem[1] + 1)
				insert_into_open_list(open_l, new_s, new_c)
				open_d[tuple(new_s)] = (tuple_s, elem[1] + 1, new_c)

		if (i%size <> 0) :
			new_s = s[0][:]
			new_s[i] = new_s[i - 1]
			new_s[i - 1] = 0
			if check_new_node(tuple(new_s), elem[1] + 1, open_l, open_d, closed_d, tuple_s) :
				new_c = count_total_cost(new_s, elem[1] + 1)
				insert_into_open_list(open_l, new_s, new_c)
				open_d[tuple(new_s)] = (tuple_s, elem[1] + 1, new_c)


		closed_d[tuple_s] = elem
		del open_l[0]
		del open_d[tuple_s]

#		print("OPEN : " + str(len(openL)) + " | CLOSED : " + str(len(closedL)))
#		if len(open_l) < 10 :
		treat_node(open_l, open_d, closed_d)

# Create our list storages, and add the initial state as a first node in the open list

def read_file(f) :
	global size
	initial_s = []
	for line in f :
		if line[0] == '#' :
			pass
		elif size == 0 :
			size = int(line)
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
	get_final_state()
	initial_c = count_total_cost(initial_s, 0)
	# add initial state to both open list forms (list and dictionnary) 
	open_l.append((initial_s, initial_c))
	open_d[tuple(initial_s)] = (0, 0, initial_c)
	treat_node(open_l, open_d, closed_d)

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