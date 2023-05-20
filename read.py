
def read_txt():
    CNF = {}
    CNFs = []

    with open ('./CNF.txt') as f:
        for i in f:
            if i != '\n':
                line = i.replace('\n', '').replace(' ', '').split('->')
                left = line[0]
                right = line[1].split('|')
                CNF[left] = right
            else:
                CNFs.append(CNF)
                CNF = {}

    return CNFs