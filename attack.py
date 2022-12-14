from functools import reduce
from itertools import product
from tqdm import tqdm

# Extend the given list to include inverses
def extend(lst) -> list:
    lst_e = lst.copy()
    for x in lst_e:
        xi = x.inverse()
        if (xi not in lst_e):
            lst_e.append(xi)

    return lst_e

# Solve the Simultaneous Conjugacy Search Problem by brute force
# The progress bar refelcts percent of key space searched, not percent to completion
def solve_SCSP(xbar_e, n, ybar, XiYX):
    for x in tqdm( product(xbar_e, repeat=n), desc="Solving SCSP", total=(len(xbar_e)**n)):
        g = reduce(lambda a, b: a * b, x)
        conj = True
        for i in range(len(ybar)):
            if (g.inverse() * ybar[i] * g != XiYX[i]):
                conj = False
                break
        if conj:
            return g

    # error: no g was found
    return 0

# O(2(b^n * b))
# b is the size of the public sets, extended to include the inverses of the present elements
# n is the number of multiplers to the private key
def bruteforce(abar, bbar, n, AiBA, BiAB):

    # Calculate A
    abar_e = extend(abar)
    A = solve_SCSP(abar_e, n, bbar, AiBA)

    # Calculate B
    bbar_e = extend(bbar)
    B = solve_SCSP(bbar_e, n, abar, BiAB)

    K = A.inverse() * B.inverse() * A * B

    return K
