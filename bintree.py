from collections import deque

from graphviz import Digraph

import uuid
class BinTree:
    # Constructor
    def __init__(self, root=None, left=None, right=None):
        """"
        Pre: left is a BinTree, or None; right is a BinTree, or None
        Requirement: If the value v is None, so must be both children.
        """
        assert (root is not None) or (left == right == None)
        self.id = uuid.uuid4()
        self._root = root
        if root:
            left = left if left else self.get_empty()
            right = right if right else self.get_empty()
            self._left = left
            self._right = right

    # Getters
    def get_id(self):
        return self.id
    

    def get_root(self):
        """
        Pre: It is assumed that the BinTree is NOT empty
        returns the value at the root of the BinTree
        """
        return self._root

    def get_left(self):
        """
        Pre: It is assumed that the BinTree is NOT empty
        returns the left child of the BinTree
        """
        return self._left

    def get_right(self):
        """
        Pre: It is assumed that the BinTree is NOT empty
        returns the right child of the BinTree
        """
        return self._right

    def get_empty(self):
        return BinTree()
    # Setters

    def set_root(self, root):
        """
        changes the value at the root of the BinTree
        """
        assert root is not None
        if self.empty():
            self._left = self.get_empty()
            self._right = self.get_empty()
        self._root = root

    def set_left(self, left):
        """
        Pre: left is a BinTree and the BinTree is not empty
        changes the left child of the BinTree
        """
        # assert self.empty()
        # assert left is not None
        self._left = left

    def set_right(self, right):
        """
        Pre: right is a BinTree and the BinTree is not empty
        changes the right child of the BinTree
        """
        # assert self.empty()
        # assert right is not None
        self._right = right

    def empty(self):
        """
        returns True if the BinTree is empty, False in other case
        """
        return self._root is None

    def leaf(self):
        """
        returns True if the BinTree is a leaf, False if not.
        """
        return self.get_left().empty() and self.get_right().empty()

    # Traversals

    def preorder(self):
        """
        returns a list with the elements of the BinTree, ordered 
        as is specified in the definition of the pre-order traversal.
        """
        output = []
        if not self.empty():
            output += [str(self.get_root())]
            if not self.leaf():
                output += self.get_left().preorder()
                output += self.get_right().preorder()
        return output

    def postorder(self):
        """
        returns a list with the elements of the BinTree, ordered 
        as is specified in the definition of the post-order traversal.
        """
        output = []
        if self.empty():
            return []
        if not self.leaf():
            output += self.get_left().postorder()
            output += self.get_right().postorder()

        output += [str(self.get_root())]
        return output

    def inorder(self):
        """
        returns a list with the elements of the BinTree, ordered 
        as is specified in the definition of the in-order traversal.
        """
        output = []
        if self.empty():
            return []
        left = self.leaf()
        if not left:
            output += self.get_left().inorder()
        output += [str(self.get_root())]
        if not left:
            output += self.get_right().inorder()
        return output

    def levelorder(self):
        """
        returns a list with the elements of the BinTree, ordered 
        as is specified in the definition of the levels-order traversal.
        """
        output = []
        cua = deque()
        cua.append(self)
        while len(cua) > 0:
            now = cua.popleft()
            output += [str(now.get_root())]
            if not now.get_left().empty():
                cua.append(now.get_left())
            if not now.get_right().empty():
                cua.append(now.get_right())

        return output

    def visualizate_tree(self):
        dot = Digraph()
        dot.attr('node', shape='circle')

        # recursive function to traverse the tree
        def add_nodes(tree):
            if not tree.empty():
                dot.node(str(tree.get_id()), label=str(tree.get_root()))
                if not tree.get_left().empty():
                    add_nodes(tree.get_left())
                    dot.edge(str(tree.get_id()), str(tree.get_left().get_id()))
                if not tree.get_right().empty():
                    add_nodes(tree.get_right())
                    dot.edge(str(tree.get_id()), str(tree.get_right().get_id()))

        add_nodes(self)
        
        dot.view()






        