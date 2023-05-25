from probabilistic_cyk import probabilistic_cyk, rule


def example1():
    I = "abaa"
    # A --> a
    # B --> b
    # C --> AB
    # D --> BA
    # E --> CA

    A = 0
    B = 1
    C = 2
    E = 3

    convert = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'E'
    }

    G = [rule(A, 'a', None, 0.3),
        rule(B, 'b', None, 0.5),
        rule(C, A, B, 0.1),
        rule(E, C, A, 0.2),
        rule(A, B, A, 0.1),
        rule(B, B, A, 0.2)]
    
    result, back = probabilistic_cyk(I, G, 4)
    
    if result:
        print("Input is a member of the language with a probability of: ", result)
    else:
        print("Input is not a member of the language")

example1()