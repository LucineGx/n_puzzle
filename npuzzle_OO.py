import sys
from my_colors import *
class NPuzzleGame :
    """The n-puzzle game rules the interaction between the states of the tiles"""

    def __init__(self, input_file):
        self.size = 0
        self.final_s = []
        self.total_s = 0
        self.max_s = 0

        self.open_l = []
        self.open_d = {}
        self.closed_d = {}

        if self.ReadFile(input_file) :
            self.GetFinalState()
            pass
        else :
            print(RED + "This puzzle can not be solved" + RESET)

    def full_size(self) :
        return (self.size**2)

    def ReadFile(self, f) :
        initial_s = []
        for line in f :
            if line[0] == '#' :
                pass
            elif self.size == 0 :
                self.size = int(line)
            else :
     #remove \n + split the line in a tab which is combined to the initial state list
                initial_s.extend(line.replace('\n','').split(' '))
        #remove empty elements that the split function could have created
        initial_s = filter(None, initial_s)
        #convert str values into ints
        initial_s = map(int, initial_s)
        return (self.SolutionExists(initial_s))

    def SolutionExists(self, s) :
        #first count how many inversion there is, compare to an usual n-puzzle solution
        inversion = 0
        for i in range(0, self.full_size()) :
            if (s[i] <> 0) :
                for j in range(0, i) :
                    if s[j] > s[i] :
                        inversion += 1
	    # if the size is odd, the number of inversion must be odd too
        if self.size % 2 and inversion % 2 == 0 :
            return False
        
        elif not self.size % 2 :
            null_rindex = 0
            # with an even size, the 0 index comes as a condition that must be checked
            for i in range(self.full_size() - 1, -1, -1) :
                null_rindex += 1
                if s[i] == 0 :
                    break
            if self.size % 4 :
                if null_rindex % 2 == inversion % 2 :
                    return False
            else :
                if null_rindex % 2 <> inversion % 2 :
                    return False
        print(GREEN + "This puzzle can be solved..." + RESET)
        return True
    
    def GetFinalState(self) :
        l = self.full_size() * [0]
        x = 0
        y = 0
        o = "right"

        for n in range(1, self.full_size()) :
		l[self.size * x + y] = n

		if o == "right":
			if y == self.size - 1 or l[self.size * x + y + 1] <> 0 :
				o = "down"
				x += 1
			else :
				y += 1

		elif o == "down" :
			if x == self.size - 1 or l[self.size * (x + 1) + y] <> 0 :
				o = "left"
				y -= 1
			else :
				x += 1

		elif o == "left" :
			if y == 0 or l[self.size * x + y - 1] <> 0 :
				o = "up"
				x -= 1
			else :
				y -= 1

		elif o == "up" :
			if l[self.size * (x - 1) + y] <> 0 :
				o = "right"
				y += 1
			else :
				x -= 1
        
        self.final_s = l


class TilesState :
    """Keep a state of tiles, and define how to manipulate them"""

    def __init__(self, l, game, c) :
        self.l = l
        self.c = c
        self.total_c = c
        self.game = game

        self.GetHeuristic()
    
    def PrintState(self) :
        s = ""
        for i in range(0, self.game.full_size()) :
            if i % self.game.size == 0 :
                s += "\n"
            s += str(self.l[i]) + " "
            if (self.l[i] < 10) :
                s += " "
        print(s)
    
    def GetHeuristic(self) :
        size = self.game.size
        for n in range(1, self.game.full_size) :
            new_i = self.l.index(n)
            goal_i = self.game.final_s.index(n)
            self.total_c += abs(new_i/size - goal_i/size) + abs(new_i%size - goal_i%size)

    def AddToOpenList(self) :
        self.game.open_l.append((initial))

if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        try :
            f = open(sys.argv[1])

        except IOError as e :
            print(RED + "'" + sys.argv[1] + "' : " + e.args[1] + RESET)
            print("To create a puzzle, you may use the generator")
        
        except Exception as e :
            sys.stdout.write(RED)
            print("Something went wrong : " + e.args[1])
        
        else :
            game = NPuzzleGame(f)
    
    else :
        print("usage : python npuzzle.py [file]")