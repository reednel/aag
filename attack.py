from sage.all import *
from sage.groups.group import Group

from datetime import timedelta
from functools import reduce
from itertools import product
import time

def getKey(g, BiAB):
    kb = g * BiAB
    k = kb.inverse()
    return k

# Return true if the given g is Alice's private A, false otherwise
def isA(g, AiBA, BiAB) -> bool:
    B = g * AiBA * g.inverse()
    BigB = B.inverse * g * B
    if (BigB == BiAB):
        return True
    else:
        return False

# O((2|abar|)^n)
# CRITICAL ERROR: I forgot AiBA and BiAB are lists not elements...must rethink attack
def bruteforce(abar, n, AiBA, BiAB):
    startTime = time.time()

    # Extend abar for inverses
    for a in abar:
        ai = a.inverse()
        if (ai not in abar):
            abar.append(ai)

    for i in product(abar, repeat=n):
        g = reduce(lambda x, y: x * y, i)
        print("GTYPE:", type(AiBA))
        if (isA(g, AiBA, BiAB)):
            break

    endTime = time.time()
    elapsed = str(timedelta(seconds=((endTime - startTime))))
    print("Bruteforced in:", elapsed)

    return getKey(g, BiAB)
