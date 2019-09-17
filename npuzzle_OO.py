import sys
from my_colors import *

class NPuzzle_Game :
    def __init__(self, input_file):
        self.size = 0 
        self.final_s = []
        self.total_s = 0
        self.max_s = 0

    def read_file(f) :


if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        try :
            f = open(sys.argv[1])

        except IOERROR as e :
            sys.stdout.write(RED)
            print("'" + sys.argv[1] + "' : " + e.args[1])
            sys.stdout.write(RESET)
            print("To create a puzzle, you may use the generator")
        
        except Exception as e :
            sys.stdout.write(RED)
            print("Something went wrong : " + e.args[1])
        
        else :
            print("Do your thing")
            game = NPuzzle_Game(read_file(f))
    
    else :
        print("usage : python npuzzle.py [file]")