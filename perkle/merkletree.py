from Crypto.Random import get_random_bytes
from math import log2, ceil

from .utils import is_power2

class MerkleTree:
    def __init__(self, data_list, hashalg, random_padding=True, padding_byte=None):
        self.data_list = data_list
        self.hashdata = [hashalg(x) for x in data_list]
        self.hashalg = hashalg
        self.depth = ceil(log2(len(data_list))) if len(data_list) else 0
        self.random_padding = random_padding
        self.padding_byte = padding_byte
        if random_padding:
            self.padding = (2**self.depth - len(self.data_list))*[hashalg(get_random_bytes(16))]
        else:
            self.padding = (2**self.depth - len(self.data_list))*[hashalg(padding_byte)]
        self.tree = {}
        self.create_tree()
    
    def create_tree(self):
        self.tree[self.depth] = self.hashdata + self.padding
        for i in range(self.depth-1,-1,-1):
            level = self.tree[i+1]
            self.tree[i] = []
            for j in range(0,len(level),2):
                left = level[j]
                right = level[j+1]
                self.tree[i].append(self.hashalg(left + right))

    def root(self):
        return self.tree[0][0] 
    
    def update(self, index, data):
        self.data_list[index] = data
        self.hashdata[index] = self.hashalg(data)
        self._update_tree(index)

    
    def _update_tree(self, index):
        self.tree[self.depth][index] = self.hashdata[index]
        for i in range(self.depth-1,-1,-1):
            if index%2:
                self.tree[i][index//2] = self.hashalg(
                    self.tree[i+1][index-1] + self.tree[i+1][index]
                )
            else:
                self.tree[i][index//2] = self.hashalg(
                    self.tree[i+1][index] + self.tree[i+1][index+1]
                )
            index //= 2

    
    def insert(self, data):
        if not is_power2(len(self.data_list)):    
            index = len(self.data_list)
            self.data_list.append(data)
            self.hashdata.append(self.hashalg(data))
            self.padding = self.padding[1:]

            self._update_tree(index)
        else:
            self.depth += 1
            index = len(self.data_list)
            self.data_list.append(data)
            self.hashdata.append(self.hashalg(data))
            if self.random_padding:
                self.padding = (2**self.depth - len(self.data_list))*[self.hashalg(get_random_bytes(16))]
            else:
                self.padding = (2**self.depth - len(self.data_list))*[self.hashalg(self.padding_byte)]
            
            self.create_tree()

    def proof(self, data):
        original_index = index = self.data_list.index(data)
        proof_hashes = []
        for i in range(self.depth,0,-1):
            complementary_index = index-1 if index%2 else index+1
            proof_hashes.append(
                self.tree[i][complementary_index]
            )
            index //= 2
        
        return original_index, proof_hashes
    
    @staticmethod
    def verify(data, index, proof_hashes, root, hashalg):
        h = hashalg(data)
        for x in proof_hashes:
            if index%2:
                h = hashalg(x + h)
            else:
                h = hashalg(h + x)
            index //= 2
        
        return h == root