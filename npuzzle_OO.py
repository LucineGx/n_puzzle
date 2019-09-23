import sys
from my_colors import *
class Game :
    """The n-puzzle game rules the interaction between the states of the tiles"""
    size = 0
    final_s = []
    total_s = 0
    max_s = 0

    open_l = []
    open_d = {}
    closed_d = {}

    def __init__(self, input_file = False, l = [], c = 0):
        self.l = l
        self.c = c
        self.total_c = c

        if input_file :
            if self.ReadFile(input_file) :
                self.GetFinalState()
                self.GetHeuristic()
                self.AddToOpenList()
            else :
                print(RED + "This puzzle can not be solved" + RESET)
        else :
            #self.GetHeuristic()
        

    def full_size(self) :
        return (Game.size**2)
    
    def PrintState(self) :
        s = ""
        for i in range(0, self.full_size()) :
            if i % Game.size == 0 :
                s += "\n"
            s += str(self.l[i]) + " "
            if (self.l[i] < 10) :
                s += " "
        print(s)

    def ResetGame(self) :
        Game.size = 0
        Game.final_s = []
        Game.total_s = 0
        Game.max_s = 0
        Game.open_l = []
        Game.open_d = {}
        Game.closed_d = {}

    def ReadFile(self, f) :
        for line in f :
            if line[0] == '#' :
                pass
            elif Game.size == 0 :
                Game.size = int(line)
            else :
     #remove \n + split the line in a tab which is combined to the initial state list
                self.l.extend(line.replace('\n','').split(' '))
        #remove empty elements that the split function could have created
        self.l = filter(None, self.l)
        #convert str values into ints
        self.l = map(int, self.l)
        return (self.SolutionExists())

    def SolutionExists(self) :
        #first count how many inversion there is, compare to an usual n-puzzle solution
        inversion = 0
        for i in range(0, self.full_size()) :
            if (self.l[i] <> 0) :
                for j in range(0, i) :
                    if self.l[j] > self.l[i] :
                        inversion += 1
	    # if the size is odd, the number of inversion must be odd too
        if Game.size % 2 and inversion % 2 == 0 :
            return False
        
        elif not Game.size % 2 :
            null_rindex = 0
            # with an even size, the 0 index comes as a condition that must be checked
            for i in range(self.full_size() - 1, -1, -1) :
                null_rindex += 1
                if self.l[i] == 0 :
                    break
            if Game.size % 4 :
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
		l[Game.size * x + y] = n

		if o == "right":
			if y == Game.size - 1 or l[Game.size * x + y + 1] <> 0 :
				o = "down"
				x += 1
			else :
				y += 1

		elif o == "down" :
			if x == Game.size - 1 or l[Game.size * (x + 1) + y] <> 0 :
				o = "left"
				y -= 1
			else :
				x += 1

		elif o == "left" :
			if y == 0 or l[Game.size * x + y - 1] <> 0 :
				o = "up"
				x -= 1
			else :
				y -= 1

		elif o == "up" :
			if l[Game.size * (x - 1) + y] <> 0 :
				o = "right"
				y += 1
			else :
				x -= 1
        
        Game.final_s = l
    
    def GetHeuristic(self) :
        size = Game.size
        for n in range(1, self.full_size) :
            new_i = self.l.index(n)
            goal_i = Game.final_s.index(n)
            self.total_c += abs(new_i/size - goal_i/size) + abs(new_i%size - goal_i%size)

    def AddToOpenList(self) :

        Game.open_l.append((self.l, self.c))
        Game.open_d[tuple(self.l)] = (0, 0, self.c)
        Game.total_s += 1

    def TreatNode(self) :


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
            start = Game(f)
            while (len(open_l))

    
    else :
        print("usage : python npuzzle.py [file]")