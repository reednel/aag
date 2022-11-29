# AAG

import random

A_public_size = 10
B_public_size = 10
A_private_size = 8
B_private_size = 8

G = groups.matrix.Heisenberg(n=1, R=13)

# Get A's public set
A_public = []
for i in range(A_public_size / 2):
    g = G.random_element()
    if (g not in A_public):
        A_public.append(g)
        A_public.append(g.inverse())
    else:
        i -= 1
print("A's public set:", A_public) # DEBUG

# Get B's public set
B_public = []
for i in range(B_public_size):
    g = G.random_element()
    if (g not in B_public and g.inverse() not in B_public):
        B_public.append(g)
        B_public.append(g.inverse())
    else:
        i -= 1
print("B's public set:", B_public) # DEBUG

# Get A's private tuple
A_private = []
for i in range(A_private_size):
    g = random.choice(A_public)
    if (g not in A_private):
        A_private.append(g)
    else:
        i -= 1
print("A's private tuple:", A_private) # DEBUG

# Get B's private tuple
B_private = []
for i in range(B_private_size):
    g = random.choice(B_public)
    if (g not in B_private):
        B_private.append(g)
    else:
        i -= 1
print("B's private tuple:", B_private) # DEBUG

# Compute A^-1 b_i A for all b_i in B's private tuple


def conj(G, h):
    GIhG = 1
    for g in G:
        GIhG = GIhG * g.inverse() * h * g
    
