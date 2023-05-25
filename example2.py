from grammar import *
from read import *

# Example usage
G = Grammar()
G.set_grammar(read_txt())
print(G.productions)

G.convert_to_cnf()

G.convert_to_namedtuples()

phrase = 'ababab'
result = G.is_phrase_in_grammar(phrase)
print(phrase)

if result:
    print(result[0])

    G.trace(result[1], phrase)
else:
    print(result)