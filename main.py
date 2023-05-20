from collections import namedtuple

rule = namedtuple('rule', ['lhs', 'rhs'])

def CYK(I, G, _r):
    n = len(I) # Longitud de la cadena de entrada
    r = _r # Numero de reglas

    P = [[[False for _ in range(r)] for _ in range(n - i)] for i in range(n)]
    back = [[[[] for _ in range(r)] for _ in range(n- i)] for i in range(n)]

    for s in range(n):
        for lhs, rhs in G:
            if len(rhs) != 1:
                continue

            terminal = rhs[0]
            if terminal == I[s]:
                P[0][s][lhs] = True

    for l in range(1, n):  
        for s in range(n-l + 1):  
            for p in range(1, l +1): 
                if s >= n - l:
                    continue
                # print((p -1, s), (l-p, s+p))
                for lhs, rhs in G:
                    if len(rhs) != 2:
                        continue
                    a, b = rhs
                    
                    if P[p -1][s][a] and P[l-p][s+p][b]:

                        P[l][s][lhs] = True
                        back[l][s][lhs].append((p, a, b))
    print(P)
    if any(P[n- 1][0]):
        print("Input is a member of the language")
        return back
    else:
        return "Input is not a member of the language"










