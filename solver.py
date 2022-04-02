import random
import copy
import time

goal = [["1","2","3","4"],["5","6","7","8"],["9","10","11","12"],["13","14","15","-"]]
direction = ["up", "down", "left", "right"]

class PuzzleGraph :
    puzzleCount = 0;
    def __init__(self):
        self.predNode = {}
        self.visited = []
        self.queue = []
        self.simpulDibangkitkan = 0;
        self.solutionPath = []


class Puzzle :
    # creating random puzzle
    def __init__(self):
        self.id = PuzzleGraph.puzzleCount
        self.puzzle = Puzzle.randomPuzzle()
        self.emptyTile = Puzzle.getEmptyTile(self)
        self.cost = Puzzle.costG(self)
        self.distanceFromRoot = 0
        PuzzleGraph.puzzleCount+=1

    def __init__(self, *args):
        if len(args) == 1 :
            # create puzzle from file
            file = open(args[0], 'r')
            root = []
            for line in file.readlines():
                root.append( [ str(x.rstrip('\n')) for x in line.split(' ') ] )
            file.close()
            self.id = PuzzleGraph.puzzleCount
            self.puzzle = root
            self.cost = Puzzle.costG(self)
            self.emptyTile = Puzzle.getEmptyTile(self)
            self.distanceFromRoot= 0
            PuzzleGraph.puzzleCount+=1
        elif len(args) == 2 :
            # create puzzle from puzzle
            self.id = PuzzleGraph.puzzleCount
            self.puzzle = args[0]
            self.cost = Puzzle.costG(self) + args[1]
            self.emptyTile = Puzzle.getEmptyTile(self)
            self.distanceFromRoot= args[1]
            PuzzleGraph.puzzleCount+=1

    # create random puzzle
    def randomPuzzle():
        elements = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","-"]
        puzzle = [[" " for i in range(4)] for j in range(4)]
        random.shuffle(elements)
        for i in range(4):
            for j in range(4):
                if elements[i*4+j] == "-":
                    puzzle[i][j] = "-"
                else :
                    puzzle[i][j] = elements[i*4+j]
        return puzzle

    def copyPuzzle(self):
        return copy.deepcopy(self)

    #hitung cost g
    def costG(self):
        jumlahUbinTidakTepat = 0
        for i in range(4):
            for j in range(4):
                if self.puzzle[i][j] == "-":
                    continue
                else :
                    if self.puzzle[i][j] != goal[i][j]:
                        jumlahUbinTidakTepat += 1
        return jumlahUbinTidakTepat;

    # return tile '-'
    def getEmptyTile(self):
        for i in range(0,4):
            for j in range(0,4):
                if self.puzzle[i][j] == "-":
                    return (i,j)

    # return index of tile
    def getTile(self,x):
        if x == "-":
            return self.emptyTile
        else :
            for i in range(0,4):
                for j in range(0,4):
                    if self.puzzle[i][j] == x:
                        return (i,j)

    # return index of tile dari coordinate
    def coordToIndex(x,y):
        return x*4+(y+1)

    # fungsi KURANG(i)
    def kurang(self,x):
        count = 0
        if x == 16:
            a,b = Puzzle.getTile(self,"-");
            for i in range(4):
                for j in range(4):
                    if self.puzzle[i][j] != "-"  and Puzzle.coordToIndex(i,j) > Puzzle.coordToIndex(a,b) :
                        if int(self.puzzle[i][j]) < x :
                            count+=1
        else :
            a,b = Puzzle.getTile(self,str(x))
            for i in range(4):
                for j in range(4):
                    if self.puzzle[i][j] != "-"  and Puzzle.coordToIndex(i,j) > Puzzle.coordToIndex(a,b) :
                        if int(self.puzzle[i][j]) < x :
                            count+=1
                
        print("Kurang ",x, " = ",count)
        return count
                    
    # menentukan apakah puzzle solvable
    def isSolvable(self):
        shadedTile = [2,4,5,7,10,12,13,15]
        sumKurang = 0
        
        for i in range(1,17):
            sumKurang += Puzzle.kurang(self,i)
        if Puzzle.coordToIndex(self.emptyTile[0],self.emptyTile[1]) in shadedTile:
            sumKurang += 1
        print("Total Kurang(i) + X = " ,sumKurang)
        return sumKurang%2 == 0

    def printPuzzle(self):
        for i in range(4):
            for j in range(4):
                if (len(self.puzzle[i][j]) == 1):
                    print(self.puzzle[i][j], end="  ")
                
                else:
                    print(self.puzzle[i][j], end=" ")
                
            print()
        print()

def compareMatrix(matrix1, matrix2):
    for i in range(4):
        for j in range(4):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    return True

def swapPuzzle(puzzle, direction):
    if direction == "up":
        copypuzzle = puzzle.copyPuzzle()
        a,b = copypuzzle.getTile("-")
        if a-1 >= 0:
            copypuzzle.puzzle[a][b],copypuzzle.puzzle[a-1][b] = copypuzzle.puzzle[a-1][b],copypuzzle.puzzle[a][b]
            copypuzzle.emptyTile = (a-1,b)
        
    elif direction == "down":
        copypuzzle = puzzle.copyPuzzle()
        a,b = copypuzzle.getTile("-")
        if a+1 <= 3:
            copypuzzle.puzzle[a][b],copypuzzle.puzzle[a+1][b] = copypuzzle.puzzle[a+1][b],copypuzzle.puzzle[a][b]
            copypuzzle.emptyTile = (a+1,b)
    
    elif direction == "left":
        copypuzzle = puzzle.copyPuzzle()
        a,b = copypuzzle.getTile("-")
        if b-1 >= 0:
            copypuzzle.puzzle[a][b],copypuzzle.puzzle[a][b-1] = copypuzzle.puzzle[a][b-1],copypuzzle.puzzle[a][b]
            copypuzzle.emptyTile = (a,b-1)
    
    elif direction == "right":
        copypuzzle = puzzle.copyPuzzle()
        a,b = copypuzzle.getTile("-")
        if b+1 <= 3:
            copypuzzle.puzzle[a][b],copypuzzle.puzzle[a][b+1] = copypuzzle.puzzle[a][b+1],copypuzzle.puzzle[a][b]
            copypuzzle.emptyTile = (a,b+1)
    
    return copypuzzle

# ambil puzzle dengan cost terkecil
def getMinCost(queue):
    minCost = queue[0].cost
    minIndex = 0
    for i in range(len(queue)):
        if queue[i].cost < minCost:
            minCost = queue[i].cost
            minIndex = i
    return queue[minIndex]

# algortima branch and bound
def branchAndBound(graph, root):

    # cek jika simpul akar adalah simpul solusi
    graph.queue.append(root)
    graph.visited.append(root.puzzle)
    graph.predNode[root] = None
    hitGoal = False
    
    while len(graph.queue) > 0 and hitGoal == False:
        # enquque puzzle dengan cost terkecil
        node = getMinCost(graph.queue)
        graph.queue.remove(node)

        # cek jika node adalah solusi
        if compareMatrix(node.puzzle, goal):
            hitGoal = True
            graph.solutionPath = []
            graph.solutionPath.append(node)
            while graph.predNode[node] != None:
                graph.solutionPath.append(graph.predNode[node])
                node = graph.predNode[node]
            graph.solutionPath.reverse()
            print("Solusi ditemukan")

        # bangkitkan node yang valid
        for i in range(len(direction)):
            child = Puzzle(swapPuzzle(node, direction[i]).puzzle, node.distanceFromRoot+1) 
            if child.puzzle not in graph.visited and child != node:
                graph.queue.append(child)
                graph.simpulDibangkitkan += 1
                graph.predNode[child] = node

                
    return graph.solutionPath           

# main function
puzzlegraph = PuzzleGraph();
print("Welcome to 15PuzzleSolver by Aloysius Gilang")
print("Choose your puzzle : ")
print("1. Random puzzle")
print("2. Puzzle from file")
print("3. Exit")

option = input();
if option == "1":
    puzzle = Puzzle()
    print("Your puzzle : ")
    print(puzzle.printPuzzle())
    solvable = puzzle.isSolvable()
    print("Solvable : ", solvable)
    if solvable:
        start = time.time()
        solution = branchAndBound(puzzlegraph,puzzle)
        end = time.time()
        for i in range(len(solution)):
            print("Step ",i+1," : ")
            solution[i].printPuzzle()
        print("Jumlah simpul dibangkitkan : ",puzzlegraph.simpulDibangkitkan)
        print("Waktu eksekusi : ",end-start)
    else:
        print("Puzzle tidak solvable")

elif option == "2":
    print("Enter the file name : ")
    fileName = input()
    puzzle = Puzzle(fileName)
    print("Your puzzle : ")
    puzzle.printPuzzle()
    solvable = puzzle.isSolvable()
    print("Solvable : ", solvable)
    if solvable:
        start = time.time()
        solution = branchAndBound(puzzlegraph,puzzle)
        end = time.time()
        for i in range(len(solution)):
            print("Step ",i+1," : ")
            solution[i].printPuzzle()
        print("Jumlah simpul dibangkitkan : ",puzzlegraph.simpulDibangkitkan)
        print("Waktu eksekusi : ",end-start)
    else :
        print("Puzzle tidak solvable")
elif option == "3":
    exit()
else:
    print("Invalid option")
    exit()
