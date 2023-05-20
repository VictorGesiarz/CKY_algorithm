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




def example3():

    S = 0
    NP = 1
    VP = 2
    Pronoun = 3
    ProperNoun = 4
    Det = 5
    Nominal = 6
    Noun = 7
    PP = 8
    Verb = 9
    Preposition = 10
    Aux = 11
    G = [rule(S, NP, VP),
    rule(S, VP),
    rule(NP, Pronoun),
    rule(NP, ProperNoun),
    rule(NP, Det, Nominal),
    rule(Nominal, Noun),
    rule(Nominal, Nominal, Noun),
    rule(Nominal, PP),
    rule(VP, Verb),
    rule(VP, Verb, NP),
    rule(VP, Verb, PP),
    rule(VP, PP),
    rule(PP, Preposition, NP),
    rule(Det, 'that'),
    rule(Det, 'this'),
    rule(Det, 'a'),
    rule(Det, 'the'),
    rule(Noun, 'book'),
    rule(Noun, 'flight'),
    rule(Noun, 'meal'),
    rule(Noun, 'money'),
    rule(Verb, 'book'),
    rule(Verb, 'include'),
    rule(Verb, 'prefer'),
    rule(Pronoun, 'I'),
    rule(Pronoun, 'she'),
    rule(Pronoun, 'me'),
    rule(ProperNoun, 'Chicago'),
    rule(ProperNoun, 'Dallas'),
    rule(Aux, 'does'),
    rule(Preposition, 'from'),
    rule(Preposition, 'to'),
    rule(Preposition, 'on'),
    rule(Preposition, 'near'),
    rule(Preposition, 'through')]


    I = "book the flight through Chicago"
    result = CYK(I, G)
    print(result)