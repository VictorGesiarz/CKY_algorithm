from collections import namedtuple
from math import log, exp
rule = namedtuple('rule', ['lhs', 'rhs1', "rhs2", "prob"])


def probabilistic_cyk(I, G, _r):
    n = len(I) # Longitud de la cadena de entrada
    r = _r # Nº de elementos no terminales (no reglas) (ej: A, B, C, D, E)

    G_T  = []
    G_NT = []

    for rule in G:
        if rule.rhs2 is None:
            G_T.append(rule)
        else:
            G_NT.append(rule)

    # Crear la matriz de programación dinámica
    P = [[[0 for _ in range(r)] for _ in range(n - i)] for i in range(n)]

    back = [[[[] for _ in range(r)] for _ in range(n - i)] for i in range(n)]


    for s in range(n):

        for lhs, rhs1, rhs2, prob  in G_T:
            terminal = rhs1
            if terminal == I[s]:
                P[0][s][lhs] = log(prob)

    print(P[0])
    for l in range(1, n):           
        for s in range(n-l + 1):    
            for p in range(1, l +1):
                if s >= n - l:                
                    continue

                last_prob = None
                for lhs, rhs1, rhs2, rule_prob in G_NT:
                    if P[p - 1][s][rhs1] and P[l-p][s+p][rhs2]:

                        prob = P[p - 1][s][rhs1] + P[l-p][s+p][rhs2] + log(rule_prob)
                        if last_prob  is not None:

                            if last_prob >= prob:
                                continue
                        
                        last_prob = prob

                        
                if last_prob is None:
                    continue

                
                P[l][s][lhs] = last_prob
                back[l][s][lhs].append((p, s, l, lhs, rhs1, rhs2))

    for prob in P[n-1][0]:
        if prob:
            return exp(prob), back
    return False, back


from bintree import BinTree


def read_back(back, convert, I):

    def trace(elements):
        if not elements:
            return 

        p, s, l, lhs, rhs1, rhs2 = elements[0]

        output = convert[lhs] + " --> " + convert[rhs1] + " " + convert[rhs2] + " ||"

        child1 = trace(back[p-1][s][rhs1])

        child2 = trace(back[l-p][s+p][rhs2])
        child1 = child1 if child1 else I[s]
        child2 = child2 if child2 else I[s+p]
        return output + " " + child1 + " " + child2
    
            

    last = back[-1][-1]
    non_null = [(i, element) for i, element in enumerate(last) if element]
    
    i, elements = non_null[0]

    output = trace(elements)
    print(output)


# Creamos un árbol binario a partir de la matriz de backtracking
# Para ello, recorremos la matriz de backtracking desde la última posición
# y vamos reconstruyendo el árbol de derivación
# Para ello, en cada posición de la matriz de backtracking, guardamos
# la posición de la partición, la posición de la subcadena, la longitud de la subcadena
# y los símbolos de la regla que se cumple en esa posición
# Con estos datos, podemos reconstruir el árbol de derivación
# Para ello, creamos un árbol binario con el símbolo de la regla que se cumple en esa posición
# y llamamos recursivamente a la función con los símbolos de la regla que se cumplen en las posiciones
# de la partición y de la subcadena
# Si no se cumple ninguna regla en esa posición, devolvemos None, este es nuestro caso base

# Después de crear el árbol binario, lo visualizamos usando graphviz
def trace_to_bintree(back, convert, I):
    def trace(elements):
        if not elements:
            return 
        p, s, l, lhs, rhs1, rhs2 = elements[0]

        root = convert[lhs]
        
        child1 = trace(back[p-1][s][rhs1])

        child2 = trace(back[l-p][s+p][rhs2])

        child1 = child1 if child1 else BinTree(I[s])
        child2 = child2 if child2 else BinTree(I[s+p])

        return BinTree(root, child1, child2)

    
            

    last = back[-1][-1]
    non_null = [(i, element) for i, element in enumerate(last) if element]
    
    i, elements = non_null[0]

    tree = trace(elements)

    tree.visualizate_tree()









