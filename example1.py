from grammar import *
from read import *

# Example usage
G = Grammar()
G.add_production('A', 'a')
G.add_production('B', 'b')
G.add_production('C', 'A B C')
G.add_production('C', '3')
print(G)

G.convert_to_cnf()

phrase = 'ababab'
result = G.is_phrase_in_grammar(phrase)
print(result[0])

G.trace(result[1], phrase)
