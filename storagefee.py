import math

COST = []
lo = []
def computeCost(m,A,S,C,F):
    global COST, lo
    COST = [None]*m
    lo = [None]*m
    
    if A[0] == 0:
        COST[0] = 0
        lo[0] = None
    else:
        COST[0] = F
        lo[0] = 0

    i=1
    while i < m: 
        if lo[i-1] == None:
            if A[i] == 0:
                COST[i] = 0
                lo[i] = None
                print("none for month", i)
            else:
                COST[i] = F
                lo[i] = i
                #print("cost:", COST[i], "last order:", lo[i], "for month", i)
        else:
            # set the potential optimal plan to place a new order, is one to beat
            COST[i] = F + COST[i-1]
            lo[i] = i
            j = lo[i-1]
            while(j<i):
                # compute potential new cost if we place a new order in month j, j from lo[i-1] to i
                # if placing orders in month j would break inventory, break
                sum=0
                k=j+1
                while(k<=i):
                    sum += A[k]
                    k+=1

                if sum>S:
                    break

                newcost=0
                #storage fee from month lo[i-1]+1 to month j-1
                k=lo[i-1]+1
                while(k<j):
                    newcost += C*A[k]*(k-lo[i-1])
                    k+=1
                #storage fee from month j+1 to month i
                k=j+1
                while(k<=i):
                    newcost += C*A[k]*(k-j)
                    k+=1

                #saved storage fee from moving orders for month j to month i-1, from month lo[i-1] to month j
                k=j
                while(k<i):
                    newcost -= C*A[k]*(j-lo[i-1])
                    k+=1

                if j==lo[i-1]:
                    newcost -= F

                if COST[i-1]+newcost+F < COST[i]:
                    COST[i] = COST[i-1]+newcost+F
                    #update last order date for month j to i
                    k=j
                    while (k<=i):
                        lo[k]=j
                        k+=1
                j+=1

        i+=1

    return COST

def planPurchases(A):
    global COST, lo
    m = len(A)
    plan = [0]*m
    i = m-1
    next = lo[i]
    while i >= 0:
        if next==None:
            return plan
        plan[next] += A[i]
        i-=1
        if (lo[i] != lo[next]):
            next = lo[i]
    print(lo)
    return plan
 
#def planPurchases(A):
#    global COST, lo
#    k = len(A)
#    plan = [0]*k
#    l = lo[k]
#    while l!=0:
#        plan[l]=0
#        i=l
#        while i<=k:
#            plan[l] += A[i]
#            i+=1
#        k=l-1
#        l=lo[k]
#        if l==None:
#            return plan
#    plan[0] = 0
#    i=1
#    while i<=k:
#        plan[0] += A[i]
#    return plan

A = [0,0]
print("0", computeCost(2, A, 4, 3, 7), "plan: ", planPurchases(A))

A = [6,2]
print("13", computeCost(2, A, 4, 3, 7), "plan: ", planPurchases(A))

A = [3,5,4]
print("16", computeCost(3, A, 10, 1, 6), "plan: ", planPurchases(A))

A = [8,6,3,1]
print("26", computeCost(4, A, 5, 2, 8), "plan: ", planPurchases(A))

A = [8,0,6,0,3,1]
# 8+8+8+8+2 > 8+8+8+2
print("?", computeCost(6, A, 5, 2, 8), "plan: ", planPurchases(A))

A = [8,0,6,0,3,1]
# 80+80+8+8+2
print("?", computeCost(6, A, 5, 2, 80), "plan: ", planPurchases(A))
