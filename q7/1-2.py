'''
1.
'''
def Never_1(N):
    if N < 0 or N > 100:
        return 0
    s = 0
    for i in range(0, 200):
        for j in range(N):
            s = s + j
    return s


def Never_2(N):
    if N < 0 or N > 100:
        return 0
    s = 0
    for i in range(N - 1):
        for j in range(i, N):
            s = s + j
    return s


def Always_1(N):
    if N < 1:
        return 0
    s = 0
    for i in range(N - 1):
        s = s + i
    return s


def Always_2(N):
    if N < 1:
        return 0
    s = 0
    for i in range(N - 1):
        for j in range(i, N):
            s = s + j
    return s


def Sometimes_1(N):
    if N < 0:
        return 0
    s = 0
    for i in range(N):
        s = s + i
    return s


def Sometimes_2(N):
    if N < 0:
        return 0
    s = 0
    for i in range(N - 1):
        for j in range(i, N):
            s = s + j
    return s

'''
2. 
(a) : O(N log N^2) = O(N * 2 * log N) = O(N log N)
    So simply the time complexity of Fast Sort algorithm will be equivalent to this.
(b) : 
    sorted(set(1)) <=> set(sorted(1))
    The time complexity of set algorithm is O(N log N) and one of sorted is O(N).
        
    The key of difference is the result of set(1) and sorted(1).
    set(1) can reduce the size of element, but sorted can't.
    This means if list contains same values, it can be removed in sort function and this can reduce the calculate time.
    For example:
    - set(sorted(1))
        A = [1,3,2,3,1,2,3,2,3,1,2,3]
        >>> A = sorted(A)
        [1,1,1,2,2,2,2,3,3,3,3,3]
        >>> set(A)
        {1, 2, 3}
    - sorted(set(1))
        A = [1,3,2,3,1,2,3,2,3,1,2,3]
        >>> A = set(A)
        {1, 3, 2}
        >>> A = sorted(A)
        {1, 2, 3}
    
    SO sorted(set(1)) CAN BE FASTER THAN set(sorted(1)).
    
    worst-case:
         Above example says if the list contains 1 value repeatedly, sorted(set(1)) is much faster than set(sorted(1)).         
'''
'''
3,
a1) About how long does it take the 8008 to sort 1,000 values?
    10/200,000 * 1000 Log 1000 = 1/20 * 9.97 = 0.4985
a2) About how long does it take the Core 2 to sort 1,000 values?
    2/3,000,000,000 * 1000 * 1000 = 0,00066
b1) About how long does it take the 8008 to sort 1,000,000 values?
    10/200,000 * 1000,000 Log 1000,000 = 50 * 19.93 = 996.5
b2) About how long does it take the Core 2 to sort 1,000,000 values?
    2/3,000,000,000 * 1000,000 * 1000,000 = 667
c1) For what problem sizes N is it faster to use the 8008 for sorting?
    For greater values 8008 is faster than Core2.
    10/200,000 * N Log N = 2/3,000,000,000 * N * N
    10/200 * LogN = 2/3,000,000 * N
    75,000 * LogN = N
    N ~ 1541707
    For problem size more than 1541707, 8008 is faster.
    
c2)  For what problem sizes N is it faster to use the Core2 for sorting?
    For problem size less than 1541707, Core2 is faster.

if __name__ == '__main__':
    import math
    for N in range(800000, 2000000):
        if (N / math.log(N, 2)) > 75000:
            break
        print(f"{N} {N / math.log(N, 2)}")    
'''
'''
Tn(N) = c * N * (Log N)^3  
'''
import math

c = 80 / (1000000 * math.log(1000000, 2) * math.log(1000000, 2) * math.log(1000000, 2))
# c = 1.0103353601462652e-08
def Tn(N):
    time = c * N * math.log(N, 2) * math.log(N, 2) * math.log(N, 2)
    return time

# def calc():
#     for N in range(3500000, 6000000):
#         value = 2*math.pow(10, 6)*math.log(math.pow(10, 6), 2)*2
#         if N * math.log(N, 2) > value:
#             break
#         print(N, N * math.log(N, 2), value)

if __name__ == '__main__':
    print(f"{c}")
    print(Tn(1000000000))
