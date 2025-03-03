class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def print_trie(self, node=None, word=''):
        if node is None:
            node = self.root
        if node.is_end_of_word:
            print(word)
        for char, child_node in node.children.items():
            self.print_trie(child_node, word + char)

trie_base = Trie()
solved= dict()
with open('Lista 1\\words_for_ai1.txt', 'r', encoding='utf-8-sig') as file:
    for line in file:
        word = line.strip()
        trie_base.insert(word)


def solve(word,trie, word_length, acc_word):
    if not word:
        solved[word] = (0, '')
        return (0, '')

    if len(word) <= word_length:
        #print(f'{word} is not valid')
        return ('INF', word)

    char = word[word_length]

    if char not in trie.children:
        #print(f'{word} is not valid')
        return ('INF', word)

    trie = trie.children[char]
    acc_word += char
    if trie.is_end_of_word:
        if(len(word)-1 == word_length):
            return (word_length**2, f'{acc_word}')
        result2 = solve(word, trie, word_length+1, acc_word)
        result = solve(word[word_length+1:], trie_base.root, 0, '')
        solved[word[word_length+1:]] = result
        if result[0] == 'INF' and result2[0] == 'INF':
            #print(f'{word[word_length:]} is not valid because {result[1]} is not a valid word and {result2[1]} is not a valid word')
            return ('INF', word)
        elif(result[0] == 'INF'):
            #print(f'{word[word_length:]} is valid because {result2[1]} is a valid word')
            return (result2[0], f'{result2[1]}')
        elif(result2[0] == 'INF'):
            #print(f'{word[word_length:]} is valid because {result[1]} is a valid word')
            return (result[0]+word_length**2, f'{acc_word} {result[1]}')
        else:
            if result2[0] >= result[0]+word_length**2:
                #print(f'{word[word_length:]} is valid because {result2[1]} is a valid word')
                return (result2[0], f'{result2[1]}')
            else:
                #print(f'{word[word_length:]} is valid because {result[1]} is a valid word')
                return (result[0]+word_length**2, f'{acc_word} {result[1]}')

    else:
        return solve(word, trie, word_length + 1, acc_word)
        
                    
with open('Lista 1\\pan_tadeusz_bez_sapcji.txt', 'r', encoding='utf-8-sig') as file:
    for line in file:
        word = line.strip()
        result = solve(word, trie_base.root, 0, '')
        print(f'{result[1]}')
