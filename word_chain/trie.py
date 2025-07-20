class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    def find_words(self, prefix):
        node = self.starts_with(prefix)
        if not node:
            return []
        result = []
        self._dfs(node, prefix, result)
        return result
    def _dfs(self, node, prefix, result):
        if node.end_of_word:
            result.append(prefix)
        for char, child in node.children.items():
            self._dfs(child, prefix + char, result)
