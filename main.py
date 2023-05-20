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



# # Ejemplo 1

# # S --> AB | BC
# # A --> BA | a
# # B --> CC | b
# # C --> AB | a

# S = 0
# A = 1
# B = 2
# C = 3

# G = [rule(S, A, B), 
#      rule(S, B, C), 
#      rule(A, B, A), 
#      rule(A, 'a', None), 
#      rule(B, C, C), 
#      rule(B, 'b', None), 
#      rule(C, A, B), 
#      rule(C, 'a', None)]

# I = "ababa"

# result = CYK(I, G)
# print(result)



# # Ejemplo 2

# S = 0
# NP = 1
# VP = 2
# Pronoun = 3
# ProperNoun = 4
# Det = 5
# Nominal = 6
# Noun = 7
# PP = 8
# Verb = 9
# Preposition = 10
# Aux = 11

# G = [rule(S, NP, VP),
# rule(S, VP),
# rule(NP, Pronoun),
# rule(NP, ProperNoun),
# rule(NP, Det, Nominal),
# rule(Nominal, Noun),
# rule(Nominal, Nominal, Noun),
# rule(Nominal, PP),
# rule(VP, Verb),
# rule(VP, Verb, NP),
# rule(VP, Verb, PP),
# rule(VP, PP),
# rule(PP, Preposition, NP),
# rule(Det, 'that'),
# rule(Det, 'this'),
# rule(Det, 'a'),
# rule(Det, 'the'),
# rule(Noun, 'book'),
# rule(Noun, 'flight'),
# rule(Noun, 'meal'),
# rule(Noun, 'money'),
# rule(Verb, 'book'),
# rule(Verb, 'include'),
# rule(Verb, 'prefer'),
# rule(Pronoun, 'I'),
# rule(Pronoun, 'she'),
# rule(Pronoun, 'me'),
# rule(ProperNoun, 'Chicago'),
# rule(ProperNoun, 'Dallas'),
# rule(Aux, 'does'),
# rule(Preposition, 'from'),
# rule(Preposition, 'to'),
# rule(Preposition, 'on'),
# rule(Preposition, 'near'),
# rule(Preposition, 'through')]


# I = "book the flight through Chicago"
# result = CYK(I, G)
# print(result)


[[[True, False, False, False, False], 
  [False, True, False, False, False], 
  [True, False, False, False, False]], 
  [[False, False, True, False, False], 
   [False, False, False, True, False], 
   [False, False, False, False, False]], 
   [[False, False, False, False, True], 
    [False, False, False, False, False], 
    [False, False, False, False, False]]]
