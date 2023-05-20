from main import CYK, rule


def example1():
    I = "aba"
    # A --> a
    # B --> b
    # C --> AB
    # D --> BA
    # E --> CD

    A = 0
    B = 1
    C = 2
    D = 3
    E = 4

    G = [rule(A, ('a')),
        rule(B, ('b')),
        rule(C, (A, B)),
        rule(D, (B, A)),
        rule(E, (C, A))]
    
    result = CYK(I, G, 5)
    print(result)
    


def example2():
    I = "baaba"

    # S --> AB | BC
    # A --> BA | a
    # B --> CC | b
    # C --> AB | a

    S = 0
    A = 1   
    B = 2
    C = 3

    G = [rule(S, (A, B)),
        rule(S, (B, C)),
        rule(A, (B, A)),
        rule(A, ('a')),
        rule(B, (C, C)),
        rule(B, ('b')),
        rule(C, (A, B)),
        rule(C, ('a'))]
    
    result = CYK(I, G, 4)
    print(result)


example1()