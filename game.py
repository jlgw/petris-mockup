import numpy as np
from fractions import gcd
import random
import time
import Tkinter

height     = 30
width      = 10
numsize    = 100
sleepytime = 200
microsleep = 0.1
easymode   = True
tutorial   = True
hardness   = 0.5 #lower is harder




def lcm(a,b):
    return (a*b)/(gcd(a,b))

def isprime(p):
    if p==1:
        return False
    ps = [2,3,5,7,11,13,17,19,23,29,31,37,41]
    if p in ps:
        return True
    for i in [2,3,5,7,11,13,17,19,23,29,31,37,41]:
        if p%i==0:
            return False
    return True

def transform(a, exp=1):
    #[0,1] => [0,1]
    #change distribution
    print a, " => ", a**(hardness*exp)
    return a**(hardness*exp)

def randnum(maxval):
    #produces a random number according to some algorithm 
    #(tests for playability) such that it is in the range 2 to the maximum
    #number
    return int(transform(random.random(), np.log(maxval))*(maxval-2)+2.5)

def divisors(n):
    #Number of divisors of the number excluding the number itself
    #Justification: Suppose m<sqrt(n) and m|n, then m'=n/m is also a 
    #divisor of  n. Further, all divisors are either on the form m<sqrt(n)
    #or m' = n/m where m|sqrt(n)
    #Multiplicity is ignored
    sq = int(n**.5)
    divs = 0
    for m in range(2, sq+1):
        if n%m==0:
            divs += 1
    return divs*2

def color(num):
    mdiv = divisors(num)
    if mdiv>8:
        mdiv=8
    st = hex(2**(8-mdiv)-1)[2:]
    while len(st)<2:
        st = '0'+st
    c = "#FFFF" + st
    return c

def cnew(num):
    if num==0:
        return ''
    #new idea
    #red channel: 2
    #green channel: 3
    #blue: divisors of number other exponents of 2 or 3
    redchan   = 0
    greenchan = 0
    bluechan  = 0
    while num%2==0 and num!=1:
        redchan += 1
        num /= 2
    while num%3==0 and num!=1:
        greenchan += 1
        num /= 3

    bluechan = divisors(num)

    if redchan>8:
        redchan = 8
    if greenchan>8:
        greenchan = 8
    if bluechan>8:
        bluechan = 8
    stred   = hex(2**(8-redchan)-1)[2:]
    stgreen = hex(2**(8-greenchan)-1)[2:]
    stblue  = hex(2**(8-bluechan)-1)[2:]
    while len(stred)<2:
        stred = '0' + stred
    while len(stgreen)<2:
        stgreen = '0' + stgreen
    while len(stblue)<2:
        stblue = '0' + stblue

    return "#" + stred + stgreen + stblue
    
shades = [cnew(n) for n in range(1000)]

def printmat(mat):
    l,m = mat.shape
    for ar in mat:
        ar2 = m*[0]
        #print ar2
        for i,a in enumerate(ar):
            if a==1:
                ar2[i] = " "
            else:
                ar2[i] = str(a)
        print '\t'.join(ar2)

   
def pilearray(ar):
    #removes 1s and stacks the other numbers at the end
    nar = len(ar)*[1]
    j = 1
    for i in range(1, len(ar)+1):
        if ar[-i] != 1:
            nar[-j] = ar[-i]
            j += 1
        
    return nar

def pile(mat):
    outmat = np.transpose([pilearray(m) for m in np.transpose(mat)])
    return outmat
    
        
def merge(inp, out=None):
    #maybe this is useless(?)
    #take array, return merged array and boolean whether affected
    #a merged array is the array with all divisors removed
    # 3 6 7 => 1 2 7
    # 3 6 2 => 1 1 1
    
    if out==None:
        outar = inp[:] #change later for reference

    for i,a in enumerate(inp):
        if i<len(inp)-1:
            #Merge these later to save a conditional
            if (inp[i]%inp[i+1])==0:
                outar[i] = inp[i]/inp[i+1]
            if (inp[i+1]%inp[i])==0:
                outar[i] = 1
        if i>0:
            #ditto
            if (inp[i]%inp[i-1])==0:
                outar[i] = inp[i]/inp[i-1]
            if (inp[i-1]%inp[i])==0:
                outar[i] = 1
    return outar

            
def mergemat(inpmat):
    height, width= inpmat.shape
    outmat = np.copy(inpmat)
    for j in range(height):
        for i in range(width):
            if isprime(inpmat[j,i]):
                if i>0 and i<width-1:
                    if isprime(inpmat[j,i+1]) and isprime(inpmat[j,i-1]):
                            print "three primes in a row"
                            outmat[j,i]   = 1
                            outmat[j,i-1] = 1
                            outmat[j,i+1] = 1
                if j>0 and j<height-1:
                    if isprime(inpmat[j+1,i]) and isprime(inpmat[j-1,i]):
                            print "three primes in a row"
                            outmat[j,i]   = 1
                            outmat[j-1,i] = 1
                            outmat[j+1,i] = 1
            div = 1
            if i<width-1:
                if (inpmat[j,i]%inpmat[j,i+1])==0:
                    #out = inpmat[j,i]/inpmat[j,i+1]
                    div = inpmat[j,i+1]
                if (inpmat[j,i+1]%inpmat[j,i])==0:
                    outmat[j,i] = 1
            if i>0:
                if (inpmat[j,i]%inpmat[j,i-1])==0:
                    #out = inpmat[j,i]/inpmat[j,i-1]
                    div = lcm(div, inpmat[j,i-1])
                if (inpmat[j,i-1]%inpmat[j,i])==0:
                    outmat[j,i] = 1
            
            if j<height-1:
                if (inpmat[j,i]%inpmat[j+1,i])==0:
                    div = lcm(div, inpmat[j+1,i])
                    #out = inpmat[j,i]/inpmat[j+1,i]
            if j>0:
                if (inpmat[j,i]%inpmat[j-1,i])==0:
                    div = lcm(div, inpmat[j-1,i])
                    #out = inpmat[j,i]/inpmat[j-1,i]
                if (inpmat[j-1,i]%inpmat[j,i])==0:
                    outmat[j,i] = 1
            
            if inpmat[j,i]/div < outmat[j,i]:
                outmat[j,i] = inpmat[j,i]/div
    return outmat
           
def complete_merge(mat, wait=False):
    m = np.copy(mat)
    while (m!=mergemat(m)).any():
        m = mergemat(m)
        if wait:
            update(m, buttons)
    return m
        

def test1(verbose = True):
    #test of merge function
    testarray = [2, 4, 6, 2, 8, 3, 7, 6, 3, 9, 1]
    expected  = [1, 2, 3, 1, 4, 3, 7, 2, 1, 3, 1]
    res = merge(testarray)
    if res!=expected:
        print "Fail"
        print testarray
        print res
        print expected

def test2(a=None):
    if a==None:
        testmat = np.array([[ 3,4,9,8,9,8,3,1,1,8],
                [ 6,6,3,9,9,1,3,6,8,9],
                [ 3,7,8,3,9,7,5,6,4,2],
                [ 3,9,3,5,8,8,8,6,6,4],
                [10,3,9,9,8,8,1,3,1,2],
                [ 9,8,1,2, 10,8,5,10,9,9],
                [ 9,6,5,7,6,4,8,1,1,5],
                [ 3,5,2,7,5,5,7,6,5,5],
                [ 8, 10,4,5,2,6,6,9,3,5],
                [ 4,1,5,1,1,6, 10,3,3,3],
                [ 6,8,9,6, 10,10,6,1,8,5],
                [ 9,3,9,9,6,7,4,2,9,7],
                [ 7,9,5,6,9,3,9,9,1,9],
                [ 6,8,5,10,7,4,3,2,2,2],
                [ 7,4,4,7,5,6,5,2,6,2]])
    else:   
        testmat = np.array([[random.randint(1,10) 
            for i in range(10)] for i in range(15)])
    print testmat
    #printmat(testmat)
    print
    #printmat(mergemat(testmat))
    print mergemat(testmat)

def test3():
    testarray = [7, 2, 3, 1, 4, 3, 7, 2, 1, 3, 7]
    print testarray
    print pilearray(testarray)

def test4():
    testmat = np.array([[1, 4, 3, 8, 1, 8, 1, 1, 1, 8],
            [1, 1, 1, 1, 1, 1, 1, 1, 2, 9],
            [1, 7, 8, 1, 1, 7, 5, 1, 1, 1],
            [1, 3, 1, 5, 1, 1, 1, 1, 1, 2],
            [10, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 8, 1, 1, 5, 1, 1, 2, 1, 1],
            [1, 6, 5, 1, 6, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 7, 6, 1, 1],
            [2, 2, 2, 5, 1, 1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1, 1, 10, 1, 1, 1],
            [6, 8, 1, 6, 1, 1, 6, 1, 8, 5],
            [3, 1, 1, 1, 6, 7, 2, 1, 9, 7],
            [7, 3, 1, 6, 3, 1, 1, 1, 1, 9],
            [6, 2, 1, 2, 7, 4, 1, 1, 1, 1],
            [7, 1, 1, 7, 5, 6, 5, 1, 3, 1]])


    print testmat
    print 
    print pile(testmat)
    

def update(mat,entries):
    global oldmat, easymode, num
    height,width = mat.shape
    for i in range(height):
        for j in range(width):
            if mat[i,j]!=oldmat[i,j]:
                if mat[i,j]==1:
                    entries[i][j].configure(text="       ", 
                            bg=root.cget('bg'))
                else:
                    if easymode:
                        if tutorial:
                            if (num%mat[i,j]==0 or mat[i,j]%num==0) and not(i==row
                                    and j==col):
                                entries[i][j].configure(text=str(int(mat[i,j])), 
                                        bg="grey")
                            else:
                                entries[i][j].configure(text=str(int(mat[i,j])), 
                                        bg=shades[int(mat[i,j])])
                        else:
                            entries[i][j].configure(text=str(int(mat[i,j])), 
                                    bg=shades[int(mat[i,j])])
                    else:
                        entries[i][j].configure(text=str(int(mat[i,j])), 
                                bg="blue")
    oldmat = np.copy(mat) 
                    
'''testmat = np.array([[ 3,4,9,8,9,8,3,1,1,8],
            [ 6,6,3,9,9,1,3,-,8,9],
            [ 3,7,8,3,9,7,5,6,4,2],
            [ 3,9,3,5,8,8,8,6,6,4],
            [10,3,9,9,8,8,1,3,1,2],
            [ 9,8,1,2, 10,8,5,10,9,9],
            [ 9,6,5,7,6,4,8,1,1,5],
            [ 3,5,2,7,5,5,7,6,5,5],
            [ 8, 10,4,5,2,6,6,9,3,5],
            [ 4,1,5,1,1,6, 10,3,3,3],
            [ 6,8,9,6, 10,10,6,1,8,5],
            [ 9,3,9,9,6,7,4,2,9,7],
            [ 7,9,5,6,9,3,9,9,1,9],
            [ 6,8,5,10,7,4,3,2,2,2],
            [ 7,4,4,7,5,6,5,2,6,2]])'''

testmat = np.array([[random.randint(2,40) 
    for i in range(width)] for i in range(height)])
#testmat = np.ones([height,width])
oldmat = np.zeros([height,width])
root = Tkinter.Tk()
root.geometry("400x800")
root.grid_propagate(1)
N,E,W,S = Tkinter.N,Tkinter.E,Tkinter.W,Tkinter.S
buttons = [[0 for i in range(width)] for j in range(height)]
col = 0
row = 0
#num = random.randint(2,numsize)
num = randnum(numsize)
shade = cnew(num)
#numnext = random.randint(2,numsize)
numnext = randnum(numsize)

def spawnshow(event):
    s = random.randint(0,numsize)
    print s

def mergeall(event=None):
    global testmat
    c = -1
    while ((testmat!=complete_merge(dp(testmat))).any()):
        c += 1
        testmat = complete_merge(dp(testmat), True)
        update(testmat, buttons)
    if c>1:
        print c, "x Combo!"
    update(testmat, buttons)

def new_num(event=None):
    global col, row, num, numnext, numsize, sleepytime, shade, oldmat
    numsize += 1
    mergeall(testmat)
    update(testmat, buttons)
    col = width/2
    row = 0
    #num = random.randint(2,numsize)
    num = numnext
    shade = cnew(num)
    print shade
    testmat[row,col] = num
    oldmat = np.zeros((height,width))
    update(testmat, buttons)
    #numnext = random.randint(2,numsize)
    numnext = randnum(numsize)
    print "Next number is: ", numnext, " (", numsize, ")"
    root.after(sleepytime, ml)

def ml(event=None):
    global col, row, num, numsize, sleepytime
    if row<height-1:
        if testmat[row+1,col] != 1:
            new_num()
            #numsize += 1
            #mergeall(testmat)
            #update(testmat, buttons)
            #col = width/2
            #row = 0
            #num = random.randint(2,numsize)
            #root.after(sleepytime, ml)
        else:
            row += 1
            testmat[row, col] = num
            testmat[row-1, col] = 1
            update(testmat, buttons)
            root.after(sleepytime, ml)
    else:
        new_num()
        #numsize += 1
        #mergeall(testmat)
        #update(testmat, buttons)
        #col = width/2
        #row = 0
        #num = random.randint(2,numsize)
        #root.after(sleepytime, ml)

def tickonce(event=None):
    global row, changed
    testmat[row, col] = num
    testmat[row-1, col] = 1
    update(testmat, buttons)
    row += 1
    changed = True
    
def tickdown(event=None, disp=True):
    global col, row, num, changed, testmat
    if row<height-1:
        if testmat[row+1,col] != 1:
            return True
        row += 1
        testmat[row, col] = num
        testmat[row-1, col] = 1
        update(testmat, buttons)
    else:
        return True
    

def spawnloop():
    
    sleepytime = 0.1
    time.sleep(sleepytime)
    
def spawn(j, num = [1]):
    global testmat
    if num==[]:
        num[0] = random.randint(1,numsize)
    testmat[0,j] = num[0]
    mergeall()
    num[0] = random.randint(1,numsize)
    print num[0]
    update(testmat,buttons)

def down_press(event=None):
    global testmat
    testmat = pile(testmat)
    update(testmat, buttons)

def dp(event=None):
    global testmat
    tp = pile(testmat)
    return tp

def merge_press(event=None):
    global testmat 
    #testmat = mergemat(testmat)
    testmat = complete_merge(testmat)
    update(testmat, buttons)

def left(event=None):
    global row, col, num, testmat
    if col>0:
        if testmat[row, col-1] ==1:
            col -= 1
            testmat[row, col]   = num
            testmat[row, col+1] = 1
            update(testmat, buttons)

def right(event=None):
    global row, col, num, testmat
    if col<width-1:
        if testmat[row, col+1] ==1:
            col += 1
            testmat[row, col]   = num
            testmat[row, col-1] = 1
            update(testmat, buttons)

def down(event=None):
    global row, col, num, testmat
    rold = row
    while row<height-2 and testmat[row+2,col] == 1:
        row += 1
    testmat[rold, col] = 1
    testmat[row,col] = num

for i in range(height):
    for j in range(width):
        buttons[i][j] = Tkinter.Button(text=' ', command=lambda j=j: spawn(j))

        buttons[i][j].grid(row=i, column=j, sticky=(N,E,W,S))
                
update(testmat, buttons)
for i in range(height):
    root.grid_rowconfigure(i,weight=1)

for i in range(width):
    root.grid_columnconfigure(i,weight=1)
#update(mat,buttons)
root.grid_propagate(0)
#update(mat,buttons)
root.bind("<Left>",left)
root.bind("<Right>",right)
#root.bind("<Up>",up)
#root.bind("<Down>",down_press)
root.bind("<Down>", down)
root.bind("m",merge_press)
#tickdown()
root.after(100, ml)
root.mainloop()




#test1()
#test2()
#test3()
#test4()
#test5()
