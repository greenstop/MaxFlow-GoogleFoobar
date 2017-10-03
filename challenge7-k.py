from copy import deepcopy
from math import sqrt;
from time import time;
runs = 0
nruns = 0
tRuns = 0
iters = 0;
eRuns = 0;
tVisited = 0;
solutionHits = 0
#credit ford-fulkerson algorithm,Neelam Yadav from geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
def answer(entrances,exits,path):
    #
    entranceTotal = sum([ sum(path[row]) for row in entrances]);

    #
    P = Problem(entrances,exits,path)
    total = P.solve();

    return total;

def search(problem,root):
    global runs,nruns;
    #print("Breadth search iterations %d"%runs, "="*60);

    queue = [];
    visited = [False for j in range(problem.N)];

    queue.append(root)
    visited[root] = True;
    #print("queue",queue);
    #print("visited",visited);

    while len(queue)>0:
        runs+=1;
        #print("Breadth search %d"%runs, "="*50);
        node = queue.pop(0);
        visited[node]=True;
        #print("  Searching Node:",node,"="*48);
        #print("  Searching queue so far:", queue[:10] if queue else " empty"); 
        #print("  visited", visited); 

        if problem.solution(node):
            #print("  Solution %d "%runs,);
            #print("    Node:",node);
            return True;

        #print("  Pushing into queue:",); 
        for adjacent in problem.nextnodes(node):
            nruns+=1;
            if visited[adjacent]: continue;
            queue.append(adjacent);
            problem.parents[adjacent]= node;
        #print("  After Pushing into queue: ",queue); 

    return False;

class Problem:
    def __init__(self,entrances,exits,path):
        self.exits = exits;
        self.path = path;
        self.entrances = entrances;
        self.N = len(path);
        self.parents = [];
        self.currentSource = None;
        self.total = 0;
        
        for row in exits:
            self.path[row][row] = float("inf"); 
        self.index = getMatrixIndex(exits,self.path);
        self.T = transpose(self.path);

    def nextnodes(self,node):
        if node not in self.index: return [];
        return self.index[node]

    def updateTransition(self,node):

        #print("Updating transition matrix"); p(self.T);
        #print("  The entry vector is %d "%(self.currentSource),);
        #print("  The termninal vector is %d"%(node),);
        minValue = float("inf");
        child = node;
        while self.currentSource != child:
            parent = self.parents[child]
            minValue = min(self.T[child][parent],minValue);
            child = parent;

        #print("  The overall minimum of the path is %.0f"%(minValue),);
        #print("Adding min value of %.0f totals"%(minValue), self.total);
        #print("  total to add %.0f"%minValue,);
        self.total += minValue;
        #print("  updated", self.total);

        child = node;
        while self.currentSource != child:
            parent = self.parents[child]
            #print("  Starting walk up path at penultimate node %s,%.0f"%((child,parent),self.T[child][parent]),);
            #print("      in node %s, changing value %.0f to minus min value %.0f "%((child,parent),self.T[child][parent],minValue),);
            #print("      node %s is set to %d"%((child,parent),self.T[child][parent]-minValue),);
            self.T[child][parent] -= minValue;
            # remove from possible next node in index if exhausted
            if self.T[child][parent] == 0:
                #print("      Removing from index %s from vector %d"%((child,parent),parent),);
                #print("      ",self.index);
                self.index[parent].pop(self.index[parent].index(child));
                #print("        removed",);
                #print("       dict", self.index);
            # add as a possible next node in index if not previously
            if self.T[parent][child] == 0 and minValue > 0:
                #print("      Add new possible node to index %s from vector %d"%((parent,child),child),);
                #print("      ",self.index);
                self.index[child].append(parent);
                #print("        added",);
                #print("       dict", self.index);
            #print("      Adding the fordfulkerson reverse edge node %s=%.0f to %.0f"%((parent,child),self.T[parent][child],self.T[parent][child]+minValue),);
            self.T[parent][child] += minValue;
            #
            child = parent;
        #print("Updated transition matrix"); p(self.T);


    def solve(self):
        #
        global runs, nruns;
        global tRuns;
        runs = 0
        tRuns = 0

        #print("  T"); p(self.T);

        #
        while self.entrances:
            self.parents = {};
            #print("X"*100);
            #print("X"*100);
            #print("X"*100);
            root = self.entrances.pop(0);
            self.currentSource = root;
            #print("Starting with node %s"%root, );
            #print("Entry nodes are", self.entrances);
            #print("  T"); p(self.T);
            #print("  index"); print(self.index);
            #self.stabilize();
            hasPath = True;
            while hasPath:
                hasPath = search(self,root);
            #print("Total so far ", self.total);

        #print("Runs ", runs);
        #print("next state runs ", nruns);

        return int(self.total);

    def solution(self,node):
        if node in self.exits:
            self.updateTransition(node);
            return True;
        else:
            return False;

def transpose(M):
    m=len(M)
    n=len(M[0]);
    A = [ [ 0 for i in range(m) ] for j in range(n) ];
    for i in range(n):
        for j in range(m):
            A[i][j] = M[j][i];
    return A;

def getMatrixIndex(exits,M):
    #print("Generating Matrix index",); p(M);
    index = {};
    for i in this(M):
        row=[];
        for j,r in enumerate(M[i]):
            #print("  %d,%d row %6.0f %40s"%(i,j,r,M[i]),);
            if (r != 0 and j != i ) or (j in exits and j==i and r!=0):
                row.append(j);
                #print("    First j:%d r:%.0f"%(j,r),);
                #print("    row %40s"%(row),);
        if len(row) > 0:
            index[i]=row;
            #print("    Index %40s"%(index),);

    #print("  Matrix index",);
    for k in index:
        #print("  Vector column %d "%k," row: ", index[k]);
        pass;
    return index;

zeroes = lambda n: [ [ 0 for i in range(n)] for i in range(n) ]
this = lambda l,a=0,b=0: range(a,len(l)+b);

def p(m):
    for r in m: print( "".join([ ("%5.0f]"%float(i) if (i>=1 or i <=-1) and i != float(" inf") and i != float("-inf") else "%5.2f]" %float(i)) if i != 0 and i != float(" inf") and i != float("-inf") else "     ]" if i != float(" inf") and i != float("-inf") else " inf ]" if i != float("-inf") else "-inf ]" for i in r]) );

import sys
w = sys.stdout.write
def pS(m,node=None):
    for i in this(m,b=1):
        for j in this(m,b=1):
            if i==0 and j==0: w(" "*6);
            elif i == 0 and j > 0:
                w("%6d"%(j-1));
            elif j==0 :
                w("%6d"%(i-1));
            elif (j>0 and j<len(m)+1) and (i>0 and i<len(m)+1) and node is None:
                w("[ %s  ]"%("X" if m[i-1][j-1] else " ")); 
            elif (j>0 and j<len(m)+1) and (i>0 and i<len(m)+1) and node is not None and node[0] == i-1 and node[1] == j-1:
                w("[ %s  ]"%("O"));
            else:
                w("[ %s  ]"%("X" if m[i-1][j-1] else " ")); 
            if j==len(m):
                w("\n");

##
def test0():
    print("="*100);
    print(" == overlapping 2 ==");
    M = zeroes(7)
    M[0][2]=55 
    M[0][5]=70 
    M[1][5]=9 
    M[2][4]=51
    M[2][5]=3 
    M[3][6]=79 
    M[4][0]=45
    M[4][6]=36 
    M[5][3]=78
    M[5][6]=87 
    M[6][4]=91 
    M[1][1]=1  
    M[2][2]=1  
    print("Matrix");
    p(M)
    entrances=[0,3]
    exits=[1,2]
    r = answer(entrances,exits,M);
    print("answer", r);
    assert r == 55;

    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=6
    M[3][5]=6
    print("answer: M");
    p(M)
    entrances=[0,1]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 16;

    print("="*100);
    print("answer overlapping");
    M = zeroes(6)
    M[0][1]=2
    M[0][3]=3
    M[1][2]=5
    M[1][3]=1
    M[2][4]=2
    M[2][1]=4
    M[3][4]=8
    M[3][5]=6
    print("answer: M");
    p(M)
    entrances=[0,1,2]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 16;

    print("="*100);
    print("answer");
    M = zeroes(4)
    M[0][1]=7
    M[1][2]=6
    M[2][3]=8
    M[3][0]=9
    print("answer: M");
    p(M)
    entrances=[0]
    exits=[3]
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 16;

    print("="*100);
    print("answer zeroes");
    M = zeroes(6)
    print("answer: M");
    p(M)
    entrances=[0,1]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 0;

    print("="*100);
    print("answer backwards 0");
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=6
    M[3][5]=6
    print("answer: M");
    p(M)
    entrances=[0,1]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 20;
    # correct 20, returned 19

    print("="*100);
    print("answer backwards 1");
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=7
    M[3][5]=7
    print("answer: M");
    p(M)
    entrances=[0,1]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 22;
    # correct 22, returned  21

    print("="*100);
    print("answer backwards XXX");
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=8
    M[3][5]=8
    print("answer: M");
    p(M)
    entrances=[0,1]
    exits=[4,5]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 23;
    # correct 23, returned  23

def testwrongallconnect():
    print("="*100);
    print(" == All connected ==");
    print("Matrix");
    M1=[[    5,    6,    6,    3,    2,    5,    7,    4,    5,   13,    9,    5,    1,    1,    9,    3,   13,    1,    4,   11,    7,    5,    3,    1,    7,    5,   13,   13,    1,    8,   13,   11,   12,    9,    7,    7,   12,    2,    6,    6,   13,    7,   11,   11,   13,   12,    7,   11,   11,    7],
    [   10,    6,    9,   11,   11,   10,    6,   13,   10,   13,    8,    1,    6,    2,    8,    4,    1,    6,   12,   12,   13,   12,   11,    3,   11,   13,   11,   12,    5,    2,    3,    9,   13,   10,    2,    7,   13,    1,   11,    8,    9,    8,   12,    5,    1,   13,    8,    8,    4,    6],
    [    3,    2,   12,    6,    7,   10,    2,    9,    1,    9,    6,   11,   10,    1,    8,   10,    6,    7,    1,    9,   12,    6,    6,    4,   13,    2,    4,   10,   12,   10,    7,    6,   13,    6,    6,   13,    2,   13,    5,   13,    9,    8,    8,   12,    2,    9,    6,    8,   11,    9],
    [   10,   13,    6,   11,    4,   10,    8,    7,    4,   10,   10,   11,    7,    7,    5,   11,    5,   12,   12,   11,    1,    8,    6,    3,   13,    8,   10,    2,   13,    2,   13,    6,   11,    4,   11,    6,    8,   12,    9,    7,    1,    7,    2,    2,    4,    3,    4,    6,    1,   12],
    [    8,   11,    2,    5,   11,    8,    5,   13,    5,   10,    4,   10,    8,    1,    8,    1,    1,    1,    4,   12,    1,   12,   10,   10,    6,    9,   13,    7,    9,    8,   13,    7,    8,   13,   11,    5,    7,    5,    3,    8,    7,    4,    3,   13,    5,    5,    6,    7,    4,   10],
    [   10,    2,    8,   11,    6,    3,    1,   13,   13,   13,    5,    5,    2,   13,    5,    7,    8,   13,    2,   10,    8,    4,    7,    7,    3,    2,    8,    1,   12,    8,   11,    2,    5,    3,   11,    2,    7,    2,   12,    9,   13,   11,    5,    7,    8,    3,    7,    8,   13,   13],
    [    6,   11,    9,    3,   11,    9,    5,    7,    7,   11,   12,   11,    1,    9,   13,    9,    1,    7,    3,    1,   13,    1,    8,    2,    5,   13,   10,    8,    4,    5,   12,    5,    7,    8,   11,   12,    7,    4,    4,    8,   13,    9,    9,    2,   12,    2,    8,   13,    2,   13],
    [   11,   12,    4,    3,   13,    6,    5,   13,    9,    6,    8,   11,    1,    3,    2,   12,   10,    3,    2,   12,    5,    7,    1,    1,    1,   11,    4,    9,    8,   10,   10,    1,    9,   13,    7,    5,    6,    9,   10,   11,    8,    9,   12,    1,   12,    4,    5,    9,    6,   12],
    [   13,    3,   12,    2,    6,    5,   13,    2,    2,   11,    3,    1,    8,   12,    9,    6,   12,    4,    8,    6,    3,    6,    3,   12,    6,    9,    7,    1,    9,    6,    5,    5,    7,    1,    8,    1,    3,   10,    2,    9,   11,    6,   11,    7,    6,   12,    5,    2,    2,    2],
    [    9,    7,   13,    7,    7,   13,    1,    4,   11,   10,    6,   10,   13,    5,   12,    2,    2,    9,    9,    2,    9,    1,    7,   11,    5,   11,    5,   12,    5,   10,   10,    7,    9,   10,   13,    1,   11,    4,    5,    3,    5,   11,   11,    3,    5,    4,    2,   12,   10,    4],
    [    2,    8,    1,    6,   10,    7,    2,    9,    2,    3,    8,   13,    6,    4,    8,    5,   12,    3,    1,    7,   10,   13,    1,    8,   10,    4,   13,   11,    6,   11,   13,   10,   10,    1,    2,    4,    8,    4,    7,    7,    3,    3,    9,   10,    2,    6,    9,    9,    4,    5],
    [   12,   11,    4,    1,    1,    8,   10,   13,    9,    4,   12,   12,    3,   11,    2,    5,    4,   12,   12,    4,    9,    9,    8,    4,    3,    4,    3,    3,   12,    1,   12,   11,    7,    6,   13,    8,    8,    8,    4,    3,   11,    4,   10,    7,   10,    7,    7,   10,    4,   11],
    [  100,    0,    0,    0,    0,  100,    0,  100,    0,    0,    0,  100,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  100,    0,    0,    0,    0,    0,    0,    0,    0,  100,    0,  100,    0,  100,  100,    0,  100,  100,    0,    0,    0,    0,    0,  100,    0,  100,  100,    0],
    [    8,    2,    7,   11,    5,    9,    5,    6,    4,    3,    1,    9,    7,   10,    8,   11,   13,   12,    3,   10,   10,    2,    5,   11,    8,   12,    9,   13,   12,    1,    5,    1,    6,    9,   11,    4,    3,   12,    9,   12,   12,    5,   11,    8,   12,   13,    1,   10,    8,    6],
    [    6,   13,    9,    6,   13,    8,   13,    7,   11,   10,   11,    3,    5,    2,   12,    1,    7,    2,    6,   11,   11,   12,    6,   11,    8,    2,   13,    8,   13,    8,    4,    3,    9,    9,    1,    3,   13,    7,   13,    2,    5,    5,    3,    9,    5,   10,    8,    3,    8,   12],
    [   11,   13,   13,    2,   12,    1,    5,   13,   12,    4,    6,    1,    4,    3,    7,    2,    5,   12,   11,    7,   11,    2,    9,   13,   10,    1,    6,    4,   13,    4,    3,    8,    1,    5,    2,   12,    8,   10,    1,    1,    9,    4,    1,   11,    6,   10,    2,   12,   10,   10],
    [    1,    5,    3,    5,   11,    7,    3,    2,    7,    9,    7,    3,   10,   11,    9,    7,    7,   12,    2,    1,   11,    2,    4,    1,    9,    6,    5,    1,   10,    4,    4,   12,    7,    8,    4,   10,   13,   10,   11,    4,    4,    6,    4,    8,    8,   12,    1,    7,    2,    5],
    [    3,    4,    6,    4,    3,    2,   11,    7,   11,   10,   13,    8,    1,   10,    5,    9,   12,    7,    8,   13,    8,    1,    4,   11,   10,   10,    4,    1,    7,    5,    1,    4,    4,    5,    7,   11,    4,    5,    1,   13,   10,   13,    5,    8,    8,   13,   12,    2,    4,    3],
    [   13,    8,    2,    7,    6,    8,    5,    1,    7,    2,   10,    6,    9,   13,   12,    6,    4,    3,   11,   13,   10,    2,    7,    3,    1,   11,   12,    5,    7,    6,   13,    4,   12,    5,    3,    2,    7,    7,   11,   13,    5,    8,    1,    3,    7,    4,   11,    9,    8,    9],
    [    7,    9,   10,   10,   11,    4,    6,    3,   13,    2,   11,    6,   10,    9,    8,    4,    8,    3,   12,    9,    5,    9,    2,    4,   11,   12,    4,   13,    3,    5,   13,   12,    3,    4,   13,    6,    9,   12,    5,    1,    7,   11,   11,    1,   10,   10,   12,    8,    8,    9],
    [    3,    2,   13,   13,    5,   11,    5,    6,   11,   11,   12,    1,    5,    6,   13,    7,    2,    2,    9,    7,    8,   13,    9,    9,    7,    9,   13,    3,    3,    4,    9,   12,   13,    5,    7,    1,    2,   10,    5,   10,    7,    9,    4,    2,    2,    9,    1,   12,   12,    7],
    [    7,    8,   11,    2,   11,   12,    2,   12,   12,    7,    1,   10,   13,    7,   12,    5,    8,    8,    7,    6,    7,   12,    3,   13,   12,   11,    5,    3,    7,    5,    5,   12,    4,   11,    9,    8,    6,    8,    3,    9,   10,   11,    5,    4,    9,   10,   13,   10,    1,   12],
    [   11,    9,    2,    4,    5,   13,    2,   11,   10,    4,    3,   13,    7,    8,    7,    5,    3,   12,    2,    1,   11,    7,    7,   12,    1,   10,    3,   12,    1,    9,    9,    9,    3,   10,    9,    7,    3,    1,    6,    4,   12,    3,    6,   12,   10,   13,    4,   11,   10,    7],
    [    0,    0,  100,    0,    0,    0,    0,    0,  100,    0,  100,    0,    0,  100,    0,    0,    0,    0,    0,  100,    0,    0,    0,    0,    0,    0,    0,  100,    0,    0,    0,    0,    0,    0,  100,  100,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
    [    8,    7,    3,    7,   10,   10,    8,    4,    6,    6,   13,    6,    3,   11,   12,   10,   10,    7,    2,   12,    1,    8,   12,    5,    8,    1,    6,    9,    9,   11,   13,   11,   10,   11,   10,    5,   13,    6,    5,   13,   12,    3,   12,    8,   11,    9,    6,    5,   13,    7],
    [    5,    9,    2,    5,   13,    8,    8,   10,   11,   13,    3,    3,   11,    2,    4,    6,    7,    7,    7,    4,    2,    8,    1,   13,   12,   11,    8,    8,   10,    3,    2,    6,   10,    7,   11,    7,    2,    2,    3,    6,    4,    5,   13,   11,   10,    7,    4,    3,    1,    2],
    [    3,    3,   10,   10,    5,    3,    4,   13,   11,   12,   13,   13,    4,    5,   13,    3,   11,    9,    5,    3,    6,    9,   11,    2,    5,    5,    9,    3,   11,    7,    4,    6,    9,    4,    3,    6,    3,    6,    8,   11,    1,    5,    6,    9,   13,   10,    7,    1,    3,   11],
    [    8,    8,    9,   11,    9,    8,    1,    1,    3,    8,   13,   13,    8,   12,    9,    2,    5,    5,   10,    5,    6,   10,    8,    8,   11,    8,   13,    8,   10,   12,    8,   13,    8,    9,   13,    8,    9,    1,    2,    7,    9,    1,    3,    4,    4,    4,   12,    1,    5,    1],
    [    3,   11,   13,    5,    4,   10,    5,    5,   11,    6,    5,   11,    5,    7,    8,    4,    7,    2,    4,    2,    6,   11,   10,    5,    5,    8,    7,   11,    8,    2,    3,    6,    7,   11,    4,    3,    7,   10,    2,    7,   13,   13,    6,    5,    6,    1,    4,    4,   13,    6],
    [    7,    4,    3,    7,    6,    2,    2,   12,   13,    4,   12,   12,   10,    4,    6,    1,    7,    2,    9,    3,   11,    3,    8,    4,   13,    1,   11,   12,   11,    5,   10,    5,    3,    5,    6,   12,    5,    1,   11,    7,    8,    5,    7,    1,    8,    7,   10,    6,    2,   10],
    [    7,    6,    9,   12,   13,    4,    5,    7,   12,   12,   10,    4,    6,   12,    8,    5,    1,    5,    7,   10,    7,   11,    1,    7,    1,   12,   12,    2,   10,   11,    6,   10,    2,    1,    2,    2,    6,    6,    5,    2,   12,    7,    6,    1,    5,    1,   11,    3,    3,    1],
    [    0,  100,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  100,  100,    0,  100,    0,  100,    0,    0,    0,    0,  100,    0,    0,    0,    0,  100,    0,    0,    0,    0,    0,    0,    0,  100,  100,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  100,    0],
    [   10,   11,    2,    5,    9,    8,    7,    2,    6,    4,    7,   12,   12,   10,    1,    4,    3,    5,    2,   10,   11,   10,    7,    8,    8,    5,   10,    2,    8,    8,    3,    1,    2,    5,    6,    8,   12,   10,    2,   13,   12,    5,   10,    3,   12,   12,    8,    1,    7,   11],
    [    3,    4,    3,   10,    3,    2,    5,   11,    8,    8,    7,   13,    8,   11,    6,    1,    3,   10,    7,   13,   10,   10,    5,    2,    5,    5,   12,    3,    1,    2,   10,    7,   13,    1,    5,    1,    2,    9,    3,   12,    7,   13,   11,   13,   10,    6,   10,   11,   10,    6],
    [   13,    8,    5,    4,   12,    8,   12,   13,   11,    5,    6,   12,    9,   10,    2,    5,    4,    3,   13,    6,    7,    6,    3,    8,    4,    7,    3,   10,    2,   10,    9,   10,    4,    3,   13,   12,    7,    5,    9,    7,    1,    8,   10,   11,    9,    6,    7,    8,    7,   10],
    [   10,    7,    5,    2,    4,    6,   10,    6,    8,    3,    1,   10,    3,   10,    6,    3,    3,    5,    8,    2,    4,    2,    6,    5,    7,    9,    8,   10,   12,    3,   13,    6,    5,    1,    1,   13,   13,   10,    8,    2,    4,   10,   10,    9,    3,    6,    7,   13,    6,   10],
    [    5,   13,    9,   11,    6,    2,   12,    6,    2,    7,   10,    8,    7,   12,    6,    3,    1,   10,    8,    1,    8,    9,   12,    6,    7,    9,    3,   11,    9,    7,    4,    7,   13,   13,   10,    3,    9,    2,   10,    8,    6,    2,    7,    7,    8,   11,   11,    3,    7,   12],
    [   10,    6,    2,    8,    9,    7,   13,    4,   10,    3,    1,    3,   11,    2,    3,    5,    7,    1,    5,   13,   13,    5,   11,    5,    3,   13,   10,   10,    8,    3,    9,   12,   12,   12,   13,    5,    5,    1,   12,    1,    3,    8,    5,    2,   10,   11,    8,    7,    4,   13],
    [   12,    1,    6,   10,    6,   12,   12,    1,    7,   11,    9,    6,   12,    9,    5,   13,    4,    9,   13,    7,    1,    6,    2,    5,   11,    5,    4,    4,    5,    1,   11,    2,    2,   10,    9,   13,    2,   10,    6,    3,    3,   13,   11,    3,    3,    8,    4,    8,    4,   13],
    [    9,    2,    2,    6,    8,    2,    9,   13,   12,   11,    2,    7,    2,    8,    8,    8,    1,    7,   11,    8,    7,    4,   13,    5,    7,    8,    4,    4,    2,    3,    8,    9,    4,   10,   13,   12,    7,   12,    7,    5,    8,   13,    4,    5,   11,    9,    7,    5,    4,    8],
    [   10,   13,    4,   10,    3,    7,   10,   11,   13,    7,    8,    9,    4,    7,    9,    4,    8,   13,    4,    1,   13,    4,    7,    5,    4,    1,    6,    5,    7,    1,   13,    9,   12,    8,   11,    6,    5,   10,    2,    8,    3,   10,    8,   12,    8,   10,    1,   12,    1,   10],
    [    6,   13,    9,    4,    6,    4,    2,    7,    9,    5,    8,    7,   11,    5,    5,    3,   10,    7,    8,   11,    6,   13,    1,    6,    1,    3,    3,   11,   10,    9,    6,    3,   10,    9,    1,    4,   12,    6,    1,    1,    6,    9,    5,    8,    1,    3,    8,   12,   11,    7],
    [    9,   11,    7,    7,    3,    2,   11,    7,    8,   11,    8,   11,    8,    6,    1,    8,   11,    5,    8,    3,    4,    9,    8,    8,    9,    9,    6,    1,    6,    5,    2,   13,    5,    1,   10,    5,    8,    3,    3,    7,   10,    2,    6,   11,   11,    1,    3,    3,    3,   11],
    [   10,    9,   10,    3,   13,    8,    6,    1,   13,   12,    7,   12,   11,    7,    5,   10,    4,   11,   13,    9,    2,    5,    7,    1,    2,    2,   12,    3,    6,    7,    6,    2,   12,    3,    1,   11,   12,    5,    9,    5,    3,    1,    9,    6,    1,    6,    6,   12,   12,    4],
    [    1,   12,    1,    6,    5,    7,    8,   13,    3,   13,    6,    1,    2,   12,    8,    5,   13,    4,    9,    4,    8,    6,    2,    4,    5,   10,    8,    8,   10,    7,    6,    8,   10,   12,    2,    2,    5,    6,    9,   11,    6,    8,    8,    6,   13,    3,    7,    6,    6,    1],
    [    2,    5,   12,    6,    9,   11,    9,   10,   12,    5,    1,    1,    9,    7,    5,    4,    7,    7,   11,   11,    3,    5,    8,   13,    1,    8,    7,    4,   12,    9,   13,    4,    6,    1,    1,    6,    4,   10,   11,   11,    3,   12,   11,   10,    5,    9,    5,    3,    5,    2],
    [   11,    3,    8,    8,    4,    7,    6,    7,    6,    1,    2,    3,   10,    8,   13,   11,    2,    2,    2,    6,   11,   13,    5,    5,    4,   12,    1,    2,    6,    7,   13,    3,    8,    4,    2,    6,    7,    5,   12,    9,    6,    2,    3,   11,   13,   12,    1,    2,    8,    6],
    [    5,    9,   12,   10,    7,    2,    9,    5,    1,    2,   11,   12,    4,   11,    9,    2,   12,    7,    3,    4,    6,    6,    3,    9,    6,    7,    3,   11,    9,    5,    9,   13,    8,   12,    8,   13,    6,    7,   13,    2,   13,    6,    9,    6,   12,    3,    9,    3,    6,    9],
    [   12,    9,    4,    4,   13,   11,    2,   13,    7,   13,    8,    6,    1,    8,   10,    7,    2,    9,   12,   10,   10,    6,    4,   12,    9,    8,    7,    2,   13,    5,    7,    8,    7,    3,    9,   13,    6,   10,    8,    6,    6,    6,   10,   11,    3,   13,    8,    1,    6,    5],
    [    4,    7,   13,    7,   13,    5,   12,    7,    9,   11,   11,    9,    6,    2,   11,    7,    6,   11,    8,    8,   13,   11,    8,    6,    1,    7,    5,    3,    8,   11,   13,   10,    3,    3,    1,    9,   13,    7,    8,   11,    1,    8,   12,    7,    3,    8,    2,   11,    2,    5]];
    entrances=[31, 12, 23];
    exits=[27, 19, 10, 11, 45];
    #('answer: entrance', [31, 12, 23])
    #('answer: exit', [27, 19, 10, 11, 45])
    #('Matrix is all connected total is', 2022)
    #2021
    #M2
    M2=[[    9,    5,   12,    3,   12,    7,    7,    9,    7,    1], 
    [    5,    9,    9,    8,    4,    8,   13,   12,   12,   13],
    [    8,    7,   10,    3,    3,   10,    6,   11,    4,    9],
    [   12,   10,   12,    4,    9,    8,    9,    5,    6,    1],
    [   13,    3,    2,    5,    7,   11,   13,    1,    1,   12],
    [    4,   11,    3,   10,    8,    3,    3,   11,   11,    4],
    [   13,   13,   13,   11,    5,    8,    8,    2,    1,    1],
    [    8,   11,    3,   11,    5,   10,    5,    6,    2,    4],
    [    0,    0,    0,    0,    0,    0,    0,    0,  100,  100],
    [    2,    7,   10,    6,    3,    8,   13,    4,    2,    5]];
    #entrances=[8];
    #exits=[7];
    #('answer: entrance', [8])
    #('answer: exit', [7])
    #('Matrix is all connected total is', 55)
    #53

    M3=[[   10,    5,    1,   11,    9,    5], 
    [    5,    8,    2,    4,   12,    6],
    [    9,   10,    6,    3,    6,   13],
    [    4,    1,   12,   10,    9,   12],
    [  100,    0,    0,  100,    0,    0],
    [   10,    1,    2,   13,    5,    5]]
    #entrances=[4];
    #exits=[3];

    #   10]    5]    1]   11]    9]    5]
    #    5]    8]    2]    4]   12]    6]
    #    9]   10]    6]    3]    6]   13]
    #    4]    1]   12]   10]    9]   12]
    #  100]     ]     ]  100]     ]     ]
    #   10]    1]    2]   13]    5]    5]
    #('answer: entrance', [4])
    #('answer: exit', [3])
    #('Matrix is all connected total is', 131)
    #122

    M4=[[    4,    6,    6,    4,    9,    1], 
    [    4,    5,    6,    7,   11,    3],
    [    3,    8,   13,    9,   12,    7],
    [    2,    9,    9,    9,    4,    6],
    [    8,   13,   12,    9,    9,    2],
    [    0,  100,    0,  100,    0,    0]]
    #entrances=[5];
    #exits=[4];
    
    #    4]    6]    6]    4]    9]    1]
    #    4]    5]    6]    7]   11]    3]
    #    3]    8]   13]    9]   12]    7]
    #    2]    9]    9]    9]    4]    6]
    #    8]   13]   12]    9]    9]    2]
    #     ]  100]     ]  100]     ]     ]
    #('answer: entrance', [5])
    #('answer: exit', [4])
    #('Matrix is all connected total is', 36)
    #(52, [1, 3], 36, 200, 0)
    #34

    M=M1;
    p(M);
    r = answer(entrances,exits,M);
    print("answer", r);
    #assert r == 55;

def testAllones():
    from random import randint 
    R = lambda b,a=1: randint(a,int(b));
    P = lambda p=.25: R(100) <= 100*p
    
    print("="*100);
    print("answer");
    N= 50
    m = R(N,N-5);
    m=50
    M = [ [ 1 if P(1) else 0 for i in range(m) ] for j in range(m) ];
    #M = [ [ P(R(200000),.7) if R(100) < 50 else P(R(100),.7) for i in range(m) ] for j in range(m) ];
    #M = [ [ 200000 for i in range(m) ] for j in range(m) ];
    print("answer: M %dx%d"%(len(M),len(M[0])));
    
    #exits={ R(m)-1 for i in range(R(m*.1))}
    #entrances={ R(m)-1 for i in range(R(m*.1))}
    #entrances={R(m-1)};
    #exits={R(m-1)};
    entrances={0}; exits={m-1};
    print("answer: entrance", entrances);
    print("answer: exit", exits);
    entrances -= exits;
    entrances = list(entrances);
    exits = list(exits);

    l = len(entrances+exits);
    lin = len(entrances);
    lou = len(exits);
    for i in range(m):
        for j in entrances:
            M[j][i]=100 if P(.5) else 0;
    
    p(M)
    print("M", M);

    print("answer: entrance", entrances);
    print("answer: exit", exits);
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 23;

def testAlls():
    from random import randint 
    R = lambda b,a=1: randint(a,int(b));
    P = lambda p=.25: R(100) <= 100*p
    
    print("="*100);
    print("answer");
    N= 50
    m = R(N,N-5);
    m=N=50
    M = [ [ R(2) for i in range(m) ] for j in range(m) ];
    #M = [ [ P(R(200000),.7) if R(100) < 50 else P(R(100),.7) for i in range(m) ] for j in range(m) ];
    #M = [ [ 200000 for i in range(m) ] for j in range(m) ];
    print("answer: M %dx%d"%(len(M),len(M[0])));
    
    #exits={ R(m)-1 for i in range(R(m*.1))}
    #entrances={ R(m)-1 for i in range(R(m*.1))}
    entrances={R(m-1)};
    exits={R(m-1)};
    #entrances={0}; exits={m-1};
    print("answer: entrance", entrances);
    print("answer: exit", exits);
    entrances -= exits;
    entrances = list(entrances);
    exits = list(exits);
    path=M;

    l = len(entrances+exits);
    lin = len(entrances);
    lou = len(exits);
    for i in range(m):
        for j in entrances:
            M[j][i]=1000 if P(1) and j not in exits else 1;

    allone = lambda : sum(sum([ r for i,r in enumerate(path) if i not in entrances+exits],[])) == N*(N-len(entrances+exits))
    alls = lambda : sum(sum([[1 for i in range(N) if M[i][j] !=0 and i not in entrances+exits] for j in range(N) ],[])) == N*(N-len(entrances+exits))
    allMul = lambda : sum(sum([ r for i,r in enumerate(path) if i not in entrances+exits],[])) % N*(N-len(entrances+exits)) == 0

    #if not allone(): assert not allMul();
    b = sum([ path[entry][exit] for exit in exits for entry in entrances]);
    total_in = sum([ path[entry][i] for entry in entrances for i in range(N) if i not in entrances+exits]);
    path = sum([path[i][j] for i in range(N) if i not in entrances+exits for j in exits]);
    #print("resultXX"*10,b+min(path,total_in));
    #print("pathXX"*10,path);
    #print("total inXX"*10,total_in);
    #print("b XX"*10,b);

    
    p(M)

    print("answer: entrance", entrances);
    print("answer: exit", exits);
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 23;

def testRand():
    from random import randint 
    R = lambda b,a=1: randint(a,b);
    P = lambda p: R(100) <= 100*p;
    
    print("="*100);
    print("answer");
    N= 50
    m = R(N,N-5);
    M = [ [ R(200000) if P(.8) else 0 for i in range(m) ] for j in range(m) ];
    #M = [ [ P(R(200000),.7) if R(100) < 50 else P(R(100),.7) for i in range(m) ] for j in range(m) ];
    #M = [ [ 200000 for i in range(m) ] for j in range(m) ];
    print("answer: M %dx%d"%(len(M),len(M[0])));
    p(M)
    entrances={ R(m)-1 if P(.1) else 0 for i in range(m)}
    exits={ R(m)-1 if P(.1) else 0 for i in range(m)}
    entrances={R(m-1)};
    exits={R(m-1)};
    print("answer: entrance", entrances);
    print("answer: exit", exits);
    entrances -= exits;
    entrances = list(entrances);
    exits = list(exits);
    print("answer: entrance", entrances);
    print("answer: exit", exits);
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 23;

def testOrdering():
    M = zeroes(12)
    M[0][2]=3
    M[2][3]=7
    M[3][2]=1
    M[2][4]=7
    M[4][2]=1
    M[2][5]=7
    M[5][2]=7
    M[2][6]=7
    M[6][11]=13
    print("answer: M");
    p(transpose(M))
    entrances=[0]
    exits=[11]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 3;

def testUnOptimal():
    M = zeroes(12)
    M[0][2]=3
    M[2][3]=7
    M[3][2]=1
    M[2][4]=7
    M[4][2]=1
    M[2][5]=7
    M[5][2]=7
    M[2][6]=7
    M[6][11]=13
    print("answer: M");
    p(transpose(M))
    entrances=[0]
    exits=[11]
    print("normal");
    p(M)
    r = answer(entrances,exits,M);
    print(r);
    assert r == 3;
    
    M = zeroes(12)
    M[0][2]=3
    M[2][3]=7
    M[3][2]=1
    M[2][4]=7
    M[4][2]=1
    M[2][5]=7
    M[5][2]=7
    M[2][6]=7
    M[6][11]=5
    print("answer: M");
    p(transpose(M))
    entrances=[0]
    exits=[11]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 3;

    print("Better to go around");
    M = zeroes(12)
    M[0][2]=3
    M[2][3]=7
    M[3][2]=1
    M[2][4]=7
    M[4][2]=1
    M[2][5]=7
    M[5][11]=99
    M[5][2]=7
    M[2][6]=7
    M[6][11]=5
    print("answer: M");
    p(transpose(M))
    entrances=[0]
    exits=[11]
    r = answer(entrances,exits,M);
    print(r); assert r == 3;

def testlarge():
    print("answer 46x46");

    M=[[0, 0, 0, 1446, 17007, 2610, 1931, 0, 8517, 0, 10000, 0, 0, 0, 2778, 0, 16632, 0, 14730, 0, 1667, 13412, 17280, 19103, 5110, 19721, 8586, 13754, 6149, 4667, 0, 16681, 95, 19197, 0, 0, 0, 5586, 0, 8121, 19740, 8821, 0, 0, 0, 5533],
    [458, 0, 5135, 1393, 5614, 4056, 5504, 9809, 5906, 11131, 0, 17194, 5440, 0, 1304, 16240, 0, 0, 0, 7237, 16253, 12269, 6268, 12051, 0, 7251, 12994, 12024, 7058, 4611, 13637, 1815, 0, 0, 14134, 19520, 573, 3061, 18756, 7132, 16360, 5751, 13668, 5505, 0, 7916],
    [0, 0, 0, 7164, 16645, 9757, 0, 0, 5261, 0, 0, 12545, 16573, 13549, 5825, 0, 4046, 4961, 1814, 10562, 0, 16703, 6236, 6253, 0, 2260, 0, 0, 0, 6168, 13750, 12013, 0, 0, 0, 6145, 0, 7979, 563, 19297, 5924, 13838, 0, 13380, 19775, 1649],
    [6288, 11948, 10857, 12464, 0, 5383, 6867, 0, 15743, 0, 14563, 0, 19612, 0, 0, 0, 11303, 0, 19121, 0, 0, 0, 8907, 14476, 5280, 0, 0, 6234, 0, 0, 12437, 0, 18104, 9979, 0, 0, 19701, 0, 2176, 0, 4955, 13397, 13804, 5462, 6748, 4203],
    [0, 0, 0, 0, 7399, 0, 13432, 0, 0, 0, 17759, 0, 5587, 0, 8152, 5104, 0, 16232, 13439, 0, 12689, 10538, 8165, 2167, 12961, 3914, 13533, 10746, 0, 9762, 0, 0, 11950, 18954, 12757, 10036, 3723, 0, 4014, 15796, 0, 0, 745, 13387, 0, 12967],
    [14262, 15444, 877, 14604, 19957, 9037, 2533, 2357, 12240, 9693, 216, 7444, 0, 0, 9877, 19628, 3286, 0, 17200, 17640, 5911, 0, 0, 10138, 6010, 6664, 17959, 9017, 19422, 8764, 16761, 13277, 9658, 0, 16274, 15201, 222, 0, 4906, 12406, 1477, 4869, 15539, 10490, 5265, 6411],
    [16545, 10973, 4534, 9341, 16473, 0, 3073, 4833, 0, 0, 3160, 0, 9660, 0, 0, 0, 19710, 14630, 16012, 3677, 10894, 13533, 0, 0, 3353, 8886, 18485, 4557, 17733, 6421, 0, 0, 13536, 0, 16192, 0, 18016, 15202, 0, 11860, 13319, 1589, 9217, 17217, 15396, 0],
    [12828, 9781, 0, 13634, 10371, 5412, 0, 11066, 16610, 4342, 16915, 15119, 0, 0, 0, 11795, 6023, 12396, 7329, 5202, 17697, 15678, 9985, 8770, 2105, 13341, 0, 0, 0, 15555, 17574, 0, 4881, 0, 6649, 0, 17093, 14633, 6262, 12743, 0, 4072, 0, 5876, 7000, 1546],
    [5717, 19110, 0, 4516, 0, 6278, 5791, 5919, 7210, 9987, 14905, 0, 11425, 0, 17905, 4577, 18827, 8944, 0, 1816, 12343, 13783, 6425, 0, 16785, 2643, 5055, 3769, 17949, 18492, 9840, 18354, 5274, 0, 5803, 15435, 0, 13242, 963, 9817, 19822, 19828, 0, 0, 0, 0],
    [18014, 18745, 4851, 1086, 3719, 3907, 13297, 0, 0, 19975, 0, 0, 0, 0, 11635, 17929, 3586, 7691, 13071, 3402, 0, 0, 2769, 1579, 12116, 16062, 0, 0, 15820, 0, 0, 13875, 0, 18053, 0, 11323, 0, 11500, 5412, 0, 6532, 11507, 16851, 2550, 0, 0],
    [0, 0, 0, 0, 0, 19188, 10644, 3378, 0, 8572, 0, 1874, 11688, 0, 0, 9844, 0, 3462, 0, 18245, 10474, 6667, 0, 15242, 8193, 6155, 18889, 12261, 0, 0, 11356, 0, 14091, 5246, 15315, 11692, 13747, 19252, 19926, 18824, 0, 16192, 15908, 0, 8356, 13894],
    [5968, 5421, 16827, 17526, 0, 6674, 2185, 13133, 12688, 17774, 16923, 17415, 0, 9296, 17570, 313, 17728, 0, 5101, 13939, 7871, 0, 0, 0, 5651, 981, 0, 2810, 12462, 6393, 12759, 3454, 6445, 0, 19678, 1968, 8112, 0, 15327, 10025, 6902, 10407, 0, 5121, 0, 18853],
    [8420, 16229, 0, 4386, 0, 19231, 1489, 19903, 17301, 3452, 17446, 13876, 0, 0, 13504, 7588, 0, 0, 14255, 8920, 3582, 12507, 7824, 2864, 6294, 0, 0, 2701, 0, 11300, 12752, 13351, 8408, 13404, 17888, 16239, 0, 410, 9470, 17456, 7630, 0, 12755, 0, 9198, 0],
    [15516, 0, 0, 7675, 0, 0, 4169, 0, 9718, 0, 9241, 2223, 408, 1271, 0, 0, 17270, 3722, 16174, 12362, 1178, 14011, 2385, 12325, 0, 15315, 19432, 3935, 0, 1020, 15968, 7617, 11078, 19898, 0, 18780, 18321, 787, 1690, 0, 2065, 2943, 16550, 2408, 0, 13180],
    [0, 5478, 0, 8831, 6926, 4303, 0, 11927, 12577, 2072, 17293, 694, 0, 0, 2976, 1244, 0, 14276, 0, 6795, 7045, 18305, 16939, 0, 6273, 1779, 1343, 0, 1860, 15078, 10321, 3204, 0, 3546, 0, 0, 1347, 14387, 11972, 7427, 14968, 0, 19957, 0, 8850, 18982],
    [0, 11034, 0, 0, 0, 0, 0, 7445, 1725, 19916, 0, 2770, 9427, 0, 16182, 0, 6888, 3939, 18656, 17017, 16586, 5040, 0, 0, 0, 0, 0, 13706, 1178, 2930, 5683, 15552, 5437, 5210, 698, 3459, 0, 2263, 14196, 3795, 3395, 17908, 0, 0, 11755, 926],
    [15217, 10550, 0, 9946, 3442, 6508, 1384, 19171, 14530, 0, 3122, 4289, 0, 8614, 13903, 0, 1214, 0, 8555, 0, 17080, 19795, 19768, 6422, 976, 0, 6072, 15190, 8793, 0, 12736, 10846, 14236, 5453, 12953, 16431, 0, 0, 13355, 0, 1515, 12058, 10639, 0, 0, 0],
    [17787, 1052, 17231, 0, 0, 16254, 4445, 15435, 19658, 1541, 13950, 16925, 15959, 0, 0, 3411, 12731, 19493, 0, 0, 0, 17478, 14746, 9269, 0, 18974, 18377, 13399, 0, 2616, 13080, 2773, 19489, 1721, 0, 12433, 14587, 13969, 0, 10354, 0, 0, 18440, 0, 9525, 18277],
    [0, 0, 0, 0, 11196, 4092, 0, 0, 7355, 13153, 1383, 11626, 61, 14047, 7879, 1680, 3431, 461, 11379, 4241, 6126, 17700, 8258, 16748, 2258, 6065, 0, 0, 0, 591, 19666, 0, 8515, 18123, 0, 0, 8408, 9878, 6074, 10455, 14834, 17421, 0, 11181, 15534, 643],
    [0, 1281, 9505, 11111, 14990, 12341, 4762, 0, 13906, 0, 0, 6007, 0, 10043, 7795, 11242, 1518, 0, 15270, 19601, 19299, 5909, 2490, 0, 9727, 0, 0, 14539, 1325, 0, 2039, 7465, 15406, 3560, 15705, 0, 10488, 9977, 1195, 0, 0, 9564, 16298, 14560, 19455, 11480],
    [17979, 18418, 11741, 12292, 12897, 10257, 7929, 10921, 0, 9479, 6404, 0, 0, 16175, 5905, 19604, 15916, 0, 7754, 0, 18068, 10534, 18177, 15337, 0, 5402, 7642, 12717, 2265, 0, 1948, 17836, 552, 4454, 15374, 9485, 7394, 0, 0, 13976, 0, 8725, 5484, 0, 12292, 3337],
    [0, 0, 0, 2336, 0, 6283, 697, 3104, 3103, 0, 6435, 17118, 2080, 4557, 3675, 10030, 13903, 7668, 12556, 14166, 10298, 0, 5025, 15071, 14971, 0, 3118, 0, 11576, 1306, 0, 17136, 11661, 1436, 0, 0, 7045, 17465, 13623, 0, 12621, 0, 0, 11655, 5184, 2010],
    [0, 10681, 0, 18906, 16347, 3766, 16971, 0, 9773, 18403, 19218, 88, 19205, 5840, 17266, 14012, 12504, 0, 0, 19736, 0, 0, 15349, 4590, 5722, 9978, 826, 0, 4852, 2733, 0, 14707, 1276, 13432, 1211, 17141, 7837, 17734, 0, 0, 0, 6780, 4052, 0, 0, 12906],
    [14403, 8661, 10835, 8597, 7250, 0, 0, 12309, 10617, 13493, 17072, 0, 15264, 11374, 0, 15340, 1974, 14583, 18449, 16158, 14324, 4134, 0, 3422, 9075, 18607, 4068, 18603, 16173, 0, 12178, 19809, 0, 11074, 9922, 7547, 4681, 263, 10179, 16990, 3246, 8674, 19123, 14329, 0, 901],
    [4579, 0, 2715, 8372, 0, 14429, 6134, 0, 4956, 6109, 1105, 16141, 13295, 13252, 0, 0, 14764, 285, 0, 0, 0, 16615, 9478, 0, 8032, 6341, 14700, 6958, 3677, 0, 4046, 16543, 0, 9793, 0, 958, 7822, 4996, 12150, 870, 16120, 0, 4923, 0, 0, 17016],
    [0, 0, 13801, 19761, 1150, 12163, 161, 0, 12750, 8685, 3520, 14670, 0, 4201, 7345, 7348, 670, 0, 15468, 4999, 11244, 18131, 12558, 0, 0, 8114, 34, 17438, 0, 6746, 0, 0, 0, 13170, 5791, 0, 2003, 3171, 0, 7598, 12706, 6234, 0, 18017, 0, 7558],
    [0, 12007, 4663, 0, 15559, 12939, 5006, 0, 2220, 3434, 11670, 16425, 14986, 15162, 19575, 10934, 15321, 9369, 2540, 15350, 4610, 15243, 0, 11194, 471, 0, 16318, 0, 10106, 18438, 3867, 0, 16906, 18468, 16371, 7811, 1168, 12720, 19474, 17951, 10169, 7765, 13403, 11487, 0, 0],
    [0, 4128, 3860, 12332, 13904, 0, 288, 9295, 2379, 10904, 10126, 9176, 18123, 0, 3116, 5190, 13896, 2078, 4772, 12944, 9118, 0, 4708, 0, 5306, 17026, 17073, 9412, 14002, 0, 9373, 9342, 0, 6818, 14625, 10276, 15104, 12602, 0, 8024, 9385, 2381, 14994, 0, 0, 9951],
    [7098, 16184, 10638, 0, 13371, 3822, 0, 0, 5322, 1714, 0, 19521, 0, 12094, 1536, 2911, 6226, 13465, 0, 12725, 14566, 6341, 7439, 0, 8380, 1996, 12069, 0, 0, 0, 2098, 6778, 0, 0, 14842, 3195, 17329, 0, 11955, 17198, 2697, 18482, 4562, 0, 2528, 0],
    [0, 16614, 13282, 0, 780, 9955, 0, 2025, 0, 0, 0, 0, 11988, 0, 0, 0, 0, 16347, 16020, 532, 0, 8139, 190, 0, 6311, 19047, 0, 0, 6141, 0, 8916, 3393, 0, 7029, 0, 1189, 0, 6443, 0, 17013, 26, 0, 9049, 0, 3920, 18821],
    [0, 3022, 19154, 3427, 13348, 10253, 1527, 12916, 19105, 0, 10906, 9152, 5800, 374, 1099, 0, 2652, 0, 18011, 8962, 4418, 7882, 15799, 7198, 0, 2656, 15692, 10578, 1876, 19923, 2113, 8565, 0, 10691, 15978, 11886, 2427, 19974, 0, 9518, 0, 3521, 0, 0, 16382, 18690],
    [8143, 0, 16061, 16339, 3542, 0, 0, 4721, 17696, 2961, 0, 17915, 0, 13672, 8240, 0, 0, 14533, 19889, 16019, 13913, 9790, 10964, 0, 254, 0, 16605, 0, 3943, 0, 0, 2506, 16376, 13871, 15651, 92, 11834, 13023, 0, 0, 12952, 14516, 0, 10219, 4635, 2345],
    [0, 17793, 1916, 0, 11816, 1643, 0, 0, 0, 8005, 0, 18892, 1146, 2742, 3921, 11519, 7483, 885, 13837, 16693, 6954, 1563, 7279, 8363, 3882, 0, 1788, 3249, 8610, 0, 2429, 8123, 16336, 19033, 13550, 6741, 0, 5743, 10458, 6386, 1678, 0, 0, 8976, 0, 3509],
    [0, 0, 4401, 1373, 0, 0, 5188, 6613, 0, 0, 4397, 16667, 13596, 19451, 0, 16369, 263, 13170, 14609, 13408, 8963, 0, 0, 0, 0, 16436, 3954, 9151, 13342, 0, 2234, 18006, 19457, 5495, 0, 16259, 11158, 13023, 5494, 0, 3563, 16551, 10634, 660, 0, 10095],
    [16458, 12799, 7648, 0, 0, 7402, 0, 7975, 2179, 1412, 9619, 0, 4170, 0, 9863, 4827, 3685, 12287, 11692, 18180, 0, 5614, 4375, 15721, 0, 11892, 6362, 3178, 19213, 8821, 18089, 6403, 9679, 0, 0, 9458, 0, 18796, 0, 7433, 12090, 658, 0, 5849, 0, 0],
    [0, 0, 12487, 15654, 0, 8458, 18117, 0, 13039, 16359, 13470, 0, 0, 17023, 2477, 12027, 9536, 7629, 19818, 8817, 14925, 3123, 17329, 10477, 10752, 8221, 13289, 13399, 0, 783, 7931, 19526, 254, 19948, 3211, 3192, 365, 3963, 16516, 5927, 0, 0, 0, 8067, 10549, 0],
    [4008, 6274, 10006, 7827, 18847, 435, 19093, 18511, 1802, 3286, 10148, 4296, 3937, 2089, 0, 18190, 18980, 5998, 0, 12436, 14327, 4590, 11774, 0, 13942, 16166, 9200, 17799, 0, 5821, 14799, 17443, 2618, 2715, 3218, 18664, 17592, 0, 0, 0, 15867, 0, 0, 3755, 0, 15125],
    [5179, 11919, 0, 1849, 0, 15489, 1522, 0, 6840, 0, 0, 0, 0, 16061, 0, 13881, 8630, 7935, 11650, 2248, 14594, 1232, 16059, 4196, 10206, 6897, 10723, 2902, 9180, 0, 18796, 0, 9162, 18384, 0, 18964, 17470, 6790, 443, 0, 299, 0, 16701, 15067, 17259, 8427],
    [165, 0, 4488, 6883, 10604, 13873, 0, 10179, 18476, 14478, 13535, 0, 15754, 1315, 15950, 15340, 7308, 14216, 0, 0, 8763, 14490, 487, 6564, 14454, 12073, 19443, 0, 77, 18099, 12917, 9796, 0, 5110, 14074, 16241, 13514, 0, 2636, 15974, 59, 10807, 0, 10765, 12344, 0],
    [17677, 0, 9726, 14141, 0, 0, 0, 0, 0, 0, 0, 17166, 9072, 0, 0, 6887, 410, 3990, 726, 11689, 1321, 0, 0, 2781, 0, 15602, 0, 0, 12544, 5605, 0, 10093, 17639, 8898, 3729, 4855, 7008, 15677, 13685, 4319, 2034, 1735, 0, 3332, 0, 6176],
    [0, 0, 0, 1954, 0, 0, 18272, 0, 0, 12010, 0, 916, 0, 4096, 7707, 0, 10569, 0, 11644, 15756, 1124, 7798, 15084, 17648, 16157, 15489, 1149, 18355, 0, 926, 0, 0, 15832, 0, 16793, 9859, 0, 7890, 1725, 0, 862, 15722, 0, 8730, 5317, 0],
    [17882, 10337, 2618, 0, 3143, 5867, 1640, 4769, 3895, 7678, 9480, 12819, 0, 18832, 0, 16210, 1000, 17366, 0, 3339, 0, 4756, 0, 17697, 6343, 15042, 0, 9690, 9410, 0, 2540, 17003, 1268, 0, 6650, 0, 18292, 11818, 18623, 18455, 4669, 4666, 4990, 6470, 15622, 876],
    [19583, 0, 5656, 7283, 2748, 3720, 7978, 4218, 0, 4864, 0, 15567, 10224, 5686, 0, 4189, 14730, 0, 0, 0, 1203, 0, 13899, 0, 0, 14719, 16504, 18878, 1631, 0, 19730, 7318, 0, 0, 27, 0, 0, 11036, 0, 12416, 5193, 0, 10998, 11344, 0, 16935],
    [4755, 4917, 0, 9011, 0, 18108, 13983, 1190, 17603, 12335, 15291, 17112, 17914, 11046, 1115, 0, 11534, 12998, 0, 513, 0, 0, 0, 15549, 3033, 0, 19471, 6269, 16198, 12185, 6188, 0, 18669, 0, 0, 14382, 16240, 0, 0, 14399, 2575, 10011, 16772, 5859, 2224, 15639],
    [2384, 4549, 14758, 13614, 0, 2009, 13819, 19728, 19904, 0, 17137, 0, 18239, 15149, 778, 12568, 0, 4344, 6086, 0, 0, 14992, 12726, 0, 1734, 15114, 11952, 16350, 5733, 7461, 18091, 0, 18507, 0, 0, 0, 4589, 0, 4061, 0, 5344, 10240, 10280, 16007, 13987, 0],
    [6672, 14630, 0, 0, 8479, 0, 14389, 6364, 264, 13691, 8803, 1772, 12603, 2306, 10190, 18293, 6463, 15340, 19270, 10711, 2529, 19969, 19807, 0, 3917, 11076, 16277, 3625, 4502, 8531, 10255, 5679, 5966, 0, 5861, 7015, 9671, 0, 11535, 774, 11515, 15275, 0, 19983, 14564, 8754]]
    print("answer: M");
    p(M)
    entrances= [0, 6, 40, 10, 11, 17, 20, 22, 23, 31]
    exits=[33, 4, 5, 9, 12, 45, 14, 21]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 2067146;
    #2065600
    #1856199.0539289627
    #1856199.0539289627
    #2067146
    #2067146

def testProblem():
    #M1
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=6
    M[3][5]=6
    entrances=[0,1]
    exits=[4,5]
    M1 = M

    #M2
    M = zeroes(12)
    M[0][2]=3
    M[2][3]=7
    M[3][2]=1
    M[2][4]=7
    M[4][2]=1
    M[2][5]=7
    M[5][11]=99
    M[5][2]=7
    M[2][6]=7
    M[6][11]=5
    entrances=[0]
    exits=[11]
    M2 = M

    #M3
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=7
    M[3][5]=7
    entrances=[0,1]
    exits=[4,5]
    M3 = M;

    #M4
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=6
    M[3][5]=6
    entrances=[0,1]
    exits=[4,5]
    M4 = M;

    #M5
    M = zeroes(6)
    M[0][2]=4
    M[0][3]=6
    M[1][2]=5
    M[1][3]=8
    M[2][3]=2
    M[2][4]=4
    M[2][5]=4
    M[3][4]=6
    M[3][5]=6
    M[1][3]=2000000
    M[3][2]=2000000-1
    M[2][4]=2000000-2
    entrances=[0,1]
    exits=[4,5]
    M5 = M;

    #M6
    N=50
    M=[ [ 1 for i in range(N)] for j in range(N) ];
    for i in range(N): M[0][i]=40000;
    #entrances=[0]
    #exits=[]
    M6 = M;

    M = M4;
    print("Test Problem");
    p(M);

    #
    #M=stabilizeT(entrances,exits,deepcopy(M));

    P = Problem(entrances,exits,deepcopy(M))
    print("  M");
    p(P.M);
    print("  T");
    p(P.T);
    #print("  Stabilized");
    #P.stabilize();

    if M==M1: assert (2,0) in P.initials;
    print(P.initials);
    print(" children");
    if M==M1: n = P.initials[0]; 
    if M==M1: assert  n == (2,0);
    if M==M1: print( P.nextnodes(n));
    if M==M1: assert P.nextnodes(n)[0] == 4;

    print(" terminus");
    print(P.terminus); 
    if M==M1: assert (4,4) in P.terminus;

    r = answer(entrances,exits,M);
    print(r);
    if M==M1: assert r == 16;
    if M==M2: assert r == 3;
    if M==M3: assert r == 22;
    if M==M4: assert r == 20;

def testinfinity():
    print("="*100);
    print("answer backwards XXX");
    M = zeroes(6)
    #M[0][2]=float("inf");
    #M[0][3]=6
    #M[1][2]=5
    #M[1][3]=8
    #M[2][3]=0
    #M[2][4]=4
    #M[2][5]=4
    #M[3][4]=8
    #for i in (1,2,3,4): M[i][5]=float("inf");
    print("answer: M");
    p(M)
    entrances=[0]
    exits=[5]
    r = answer(entrances,exits,M);
    print(r);
    #assert r == 23;

def testBackwards():
    print("Better to go around");
    M = zeroes(4)
    M[0][1]=2
    M[0][2]=3
    M[1][3]=3
    M[2][1]=5
    M[2][3]=2
    print("answer: M");
    p(transpose(M))
    entrances=[0]
    exits=[3]
    r = answer(entrances,exits,M);
    print(r);
    assert r == 5;

if __name__ == "__main__":
    print("starting");
    testBackwards();
    #testinfinity();
    #testProblem();
    test0();
    testUnOptimal();
    testOrdering();
    #testRand();
    #testwrongallconnect();
    testAllones();
    testlarge();
    testAlls();
