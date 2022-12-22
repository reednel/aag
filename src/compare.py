from src.aag import AAGExchangeObject
from src.attack import bruteforce
import csv
import time
from tqdm import tqdm

def timing(group_type, group_object, pk_length, sk_length):
    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    startExchangeTime = time.time_ns()

    # Choose random subset of bg to be publicKey
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)

    # Choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)

    # Derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    endExchangeTime = time.time_ns()
    exchangeTime = (endExchangeTime - startExchangeTime) / 1000000 # to ms

    # Execute bruteforce attack
    atb = alice.transition(bob)
    bta = bob.transition(alice)
    startAttackTime = time.time_ns()
    bfSharedKey, guesses = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)
    endAttackTime = time.time_ns()
    attackTime = (endAttackTime - startAttackTime) / 1000000 # to ms

    # Check correctness
    if (not (aliceSharedKey == bobSharedKey == bfSharedKey)):
        print("RUNTIME ERROR")
        print("\tAlice's K:", aliceSharedKey)
        print("\tBob's K  :", bobSharedKey)
        print("\tEve's K  :", bfSharedKey)

    return exchangeTime, attackTime, guesses

def generate(file_name, group_type, group, group_name, number_of_points, public_sizes, private_sizes):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["group", "pk", "sk", "exchange", "attack", "guesses", "cardinality"])
        for pub in tqdm(public_sizes, desc='Public',leave=False, position=1):
            for priv in tqdm(private_sizes, desc='Private', leave=False, position=2):
                for _ in tqdm(range(number_of_points), leave=False, desc='Points', position=3):
                    exchangeTime, attackTime, guesses = timing(group_type, group, pub, priv)
                    writer.writerow([group_name, pub, priv, exchangeTime, attackTime, guesses, group.cardinality()])
                    f.flush()
