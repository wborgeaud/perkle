import unittest
from Crypto.Hash import SHA256, SHA3_256
from Crypto.Random import get_random_bytes

from .merkletree import MerkleTree

def sha256(data):
    return SHA256.new(data).digest()

def sha3(data):
    return SHA3_256.new(data).digest()

def create_tree(n, hashalg):
    data_list = [get_random_bytes(16) for _ in range(n)]
    mt = MerkleTree(data_list, hashalg)
    mt.create_tree()
    return mt

class BasicTests(unittest.TestCase):
    
    def test_different_data_different_root(self):
        mt1 = create_tree(1000, sha256)
        mt2 = create_tree(1000, sha256)
        self.assertNotEqual(mt1.root(), mt2.root())
    
    def test_different_hash_different_root(self):
        mt1 = create_tree(1000, sha256)
        mt2 = create_tree(1000, sha3)
        self.assertNotEqual(mt1.root(), mt2.root())
    
    def test_proofs_work_all_leaves(self):
        mt = create_tree(1000, sha256)
        result = []
        for x in mt.data_list:
            index, ph = mt.proof(x)
            result.append(MerkleTree.verify(x,index,ph,mt.root(),sha256))
        self.assertTrue(all(result))

class InsertUpdateTests(unittest.TestCase):

    def test_insertion_works(self):
        data_list = [b'lol',b'bam',b'boom',b'bim']
        mt1 = MerkleTree(data_list, sha256)
        mt2 = MerkleTree(data_list[:-1], sha256)
        mt2.insert(b'bim')
        self.assertEqual(mt1.tree, mt2.tree)
    
    def test_create_tree_by_insertions(self):
        data_list = [get_random_bytes(16) for _ in range(100)]
        mt1 = MerkleTree(data_list,sha256,random_padding=False,padding_byte=b'0')
        mt2 = MerkleTree([],sha256,random_padding=False,padding_byte=b'0')
        for x in data_list:
            mt2.insert(x)
        self.assertEqual(mt1.tree, mt2.tree)

    def test_update_works(self):
        data_list1 = [get_random_bytes(16) for _ in range(100)]
        for i in range(len(data_list1)):
            mt1 = MerkleTree(data_list1,sha256,random_padding=False,padding_byte=b'0')
            data_list2 = data_list1[:i] + [b'foo'] + data_list1[i+1:]
            mt2 = MerkleTree(data_list2,sha256,random_padding=False,padding_byte=b'0')
            mt1.update(i, b'foo')
            with self.subTest(i=i):
                self.assertEqual(mt1.tree, mt2.tree)
    
    def test_create_tree_by_updates(self):
        data_list = [get_random_bytes(16) for _ in range(100)]
        mt1 = MerkleTree(data_list,sha256,random_padding=False,padding_byte=b'0')
        mt2 = MerkleTree([get_random_bytes(16) for _ in range(100)],sha256,random_padding=False,padding_byte=b'0')
        for i, x in enumerate(data_list):
            mt2.update(i,x)
        self.assertEqual(mt1.tree, mt2.tree)

if __name__ == '__main__':
    unittest.main()