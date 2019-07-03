# Perkle: A simple Python 3 implementation of Merkle Trees
Perkle provides a simple, all python, implementation of Merkle Trees. 

## Installation
The package can be installed via pip:
```bash
pip install perkle
```
or by cloning this repository.

The package `pycryptodome` is in the requirements. Make sure that this will not conflict with an installation of the (deprecated) package `pycrypto`.

## Example
Here is how to create a Merkle Tree of numbers from 0 to 9:
```python
from Crypto.Hash import SHA256
from perkle import MerkleTree
from binascii import hexlify
data_list = [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9']
sha256 = lambda x : SHA256.new(x).digest() 
mt = MerkleTree(data_list, sha256, random_padding=False, padding_byte=b'0')
print(hexlify(mt.root()))
#70cc27c03c0444d1dfc63f58e373a2882a7b9f4f7f6ed1a4dfc1a94a5ac5875c
```
By default, we add a random padding to the data to have a power of two leaves. You can make the padding non-random with the `random_padding` parameter to make the results consistent.

New data can be inserted in the Merkle Tree:
```python
data = b'10'
mt.insert(data)
print(hexlify(mt.root()))
#3e32b51c76de4b124f1fedfbb4d5a30d117274bf04b538ca7f10434e2f8a35b9
```

And existing data can be updated:
```python
new_data = b'zero'
mt.update(0,new_data)
print(hexlify(mt.root()))
#d485ca0c92d339d2e8495216cdb420f0e215003fffdb62d09da56d8739c94a11
```

Proofs can be easily generated:
```python
index, proof_hashes = mt.proof(b'7')
```
and verified:
```python
print(MerkleTree.verify(b'7',index,proof_hashes,mt.root(),sha256))
#True
```