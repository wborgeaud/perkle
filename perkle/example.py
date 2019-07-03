from Crypto.Hash import SHA3_256
from binascii import hexlify

from .utils import countries
from .merkletree import MerkleTree

def sha3(data):
    return SHA3_256.new(data).digest()

mt = MerkleTree(countries, sha3)

print(f'The root for the Merkle Tree of all countries is {hexlify(mt.root())}')

country = 'Iceland'
index, ph = mt.proof(country.encode())

print(f"The proof that {country} is in the list consists of the following {len(ph)} hashes:")
for x in ph:
    print(hexlify(x))

print(f"We only need to give these {len(ph)} hashes, along with the root, to prove that {country} is \
in the list, instead of giving {len(countries)} hashes, one for each country.")

if MerkleTree.verify(country.encode(),index,ph,mt.root(),sha3):
    print(f"{country} is in the list of countries.")
else:
    print(f"{country} is not in the list of countries.")