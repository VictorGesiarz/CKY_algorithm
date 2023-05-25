def read_txt():
    CNF = {}
 
    with open ('./CNF.txt') as f:
        for i in f:
            if i != '\n':
                line = i.replace('\n', '').split('->')
                left = line[0][:-1]
                right = line[1].split('|')

                for i, term in enumerate(right):
                    right[i] = ' '.join(letter for letter in term.split())

                if left in CNF:
                    CNF[left] += right
                else:
                    CNF[left] = right
    return CNF