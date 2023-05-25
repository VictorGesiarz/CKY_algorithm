import itertools
from cyk import *

# Función auxiliar que se usa a la hora de eliminar producciones vacias 
# Con esta función calculamos todas las posibilidades que se generan cuando 
# eliminamos una epsilon del estilo A -> A | 3 (representamos las epsilon con 3)
def get_combinations(letters, non_terminal):
    c_indices = [i for i, letter in enumerate(letters) if letter == non_terminal]
    other_indices = [i for i, letter in enumerate(letters) if letter != non_terminal]

    c_combinations = []
    for r in range(len(c_indices) + 1):                                 # Con los indices de la regla a la que le eliminamos epsilon,
        c_combinations.extend(itertools.combinations(c_indices, r))     # buscamos las posibles formas de combinarlo

    combinations = []
    for c_comb in c_combinations:
        indices = list(c_comb) + other_indices
        indices.sort()
        combination = [letters[i] for i in indices]                     # Nos guardamos cada posible combinación

        if combination not in combinations:
            combinations.append(combination)
    return combinations[:-1]


# Clase con la cual representamos la gramática.
class Grammar:
    
    def __init__(self):
        self.non_terminals = set()  # Aquí guardamos todos los símbolos no terminales (A | VB | N ...)
        self.terminals = set()      # Aquí guardamos todos los síbmolos terminales (a | b | coche ...)
        self.productions = dict()   # Aquí guardamos la gramática en forma de diccionario (A: a | b, B: A | B a ...)


    def __repr__(self) -> str:      # Esta función nos sirve para dibujar de forma bonita la gramática en la terminal.
        print('Non terminals:', end=' ')
        for i in self.non_terminals: print(i, end=' ')
        print()

        print('Terminals:', end=' ')
        for i in self.terminals: print(i, end=' ')
        print()

        print('Productions:')
        for key, item in self.productions.items(): 
            for production in item:
                print(f'    {key} -> {production}', end='')
                print()
        return ''
    
    
    def is_grammar_correct(self):   # Esta función sirve para comprobar que la gramática sea correcta, es decir,
                                    # que por cada parte derecha de las reglas que apunte a un no terminal, 
                                    # exista ese no terminal en la gramática.
        non_terminals = set()
        for left, right in self.productions.items():
            for term in right:
                for symbol in term.split():
                    if symbol.isupper():
                        non_terminals.add(symbol)

        if any(non_terminal not in self.non_terminals for non_terminal in non_terminals):
            return False
        return True
    

    def add_production(self, lhs, rhs):     # Con esta función podemos definir la gramática regla por regla. 
        self.productions.setdefault(lhs, []).append(rhs)    # Añadimos la producción
        
        self.non_terminals.add(lhs)         # Añadimos el no terminal a su lista
        for symbol in rhs.split():
            if not symbol.isupper():
                self.terminals.add(symbol)  # Añadimos el terminal a su list


    def __remove_epsilon_productions(self):     # Primer paso en la conversión a Chomsky Normal Form. 
        
        # Tenemos dos posibles casos de epsilon, que un no terminal solo lleve a epsilon: A -> 3
        # O que un no terminal produzca epsilon entre otras cosas: A -> a | 3 ...
        # En el primer caso simplemente eliminamos la regla y todas las apariciones de la regla en la gramática.
        # En el segundo caso tenemos que calcular las combinaciones resultantes de cualquier regla que llame a A.
        # Si B -> A b A, al eliminar la epsilon de A, B quedaría como: B -> A b A | A b | b A | b
        
        remove_empty = []
        combine_empty = []

        # Encontrar los casos que tienen epsilon
        for left, right in self.productions.items():    # Esta misma estructura de bucle la repeteriemos constantemente
            for i, term in enumerate(right):            # por que hay que seguir los pasos uno detrás de otro. Recorremos cada producción de cada regla.
                if term == '3':
                    if len(right) > 1:                  # Segundo caso
                        combine_empty.append(left)
                    else:                               # Primer caso
                        remove_empty.append(left)
                        self.non_terminals.remove(left)
                    right.remove(term)                  # Eliminamos la epsilon

        # Eliminar los que sean del primer caso
        for non_terminal in remove_empty:
            for left, right in self.productions.items():
                for i, term in enumerate(right):
                    if term == non_terminal:            # Si la producción es directamente el símbolo correspondiente
                        right.remove(term)
                    elif non_terminal in term:          # Si la producción tiene varios símbolos 
                                                        # (al tenerlo guardado como strings hay que hacerlo de la siguiente manera)
                        right[i] = ' '.join(letter for letter in term.split() if letter != non_terminal)

        # Eliminar los que sean del segundo caso
        new_productions = {}
        for non_terminal in combine_empty:
            for left, right in self.productions.items():
                for i, term in enumerate(right):
                    if len(term) > 1 and non_terminal in term:  # Si el termino contiene la regla de la cual eliminamos la epsilon
                        letters = term.split()
                        letter = non_terminal
                        combinations = get_combinations(letters, letter)    # Obtenemos las combinaciones con la función
                        
                        for combination in combinations:    # Creamos las nuevas producciones que se generan
                            new_productions.setdefault(left, []).append(' '.join(letter for letter in combination))

        # Añadir las nuevas reglas creadas
        for left, right in new_productions.items():
            for term in right:
                self.add_production(left, term)
        
        # Eliminar epsilon de la lista de terminales
        if '3' in self.terminals:
            self.terminals.remove('3')


    def __remove_unit_productions(self):         # Segundo paso en la conversión a Chomsky Normal Form. 
        
        # Ahora toca eliminar las reglas que produzcan un único símbolo no terminal
        # Aqúi también tenemos dos opciones, que la regla produzca solo un no terminal: C -> B
        # O que la regla produzca varias opciones: A -> B | C D | a ...
        # En el primer caso tendriamos que eliminar la regla y sustituir todas sus apariciones y en el segundo caso
        # simplemente reemplazar el no terminal por la regla que produzca dicho símbolo.
        
        substitute = {}
        remove_non_terminal = {}
    
        # Identificamos el primer caso
        for left, right in self.productions.items():
            for term in right:
                if len(right) == 1 and len(term) == 1 and term in self.non_terminals:
                    remove_non_terminal[left] = right           # Si la regla solo tiene una producción y dicha 
                    self.productions[left] = []                 # producción es un no terminal, lo eliminamos y lo añadimos a la lista
                    self.non_terminals.remove(left)

        # Eliminamos las reglas que se hayan correspondido con el primer caso
        for remove, subst in remove_non_terminal.items():
            for left, right in self.productions.items():
                for i, term in enumerate(right):
                    if remove in term:                          # Añadimos la producción de la regla que vamos a eliminar
                        right[i] = term.replace(remove, ' '.join(letter for letter in subst))   # Eliminamos dicha regla de el término en el que estamos

        # Ahora identificamos el segundo caso
        for left, right in self.productions.items():
            for term in right:
                if len(right) > 1 and len(term) == 1 and term in self.non_terminals:    
                    if term not in substitute:                      # Si la regla tiene varias producciones y una de ellas
                        substitute[term] = self.productions[term]   # es un no terminal, lo añadimos a la lista para sustituirlo.

        # Este caso es por si se da, por ejemplo: B -> A B | B | c ..., 
        # para que no empiece a sustituir la B a si misma en bucle
        for remove, subst in substitute.items():
            for term in subst:
                if term == remove:
                    subst.remove(term)

        # Sustituimos los terminos que se correspondan con el segundo caso.
        for remove, subst in substitute.items():
            for left, right in self.productions.items():
                for i, term in enumerate(right):
                    if left not in remove_non_terminal and term == remove:  # Si el término de la regla es igual al que queremos sustituir
                        if term != left:
                            right += subst                                          # Sustituimos y
                        self.productions[left] = [i for i in right if i != term]    # Eliminamos el término

        # Actualizamos el diccionario de producciones
        new_productions = {}
        for left, right in self.productions.items():
            if len(right) >= 1:
                new_productions[left] = list(set(right))
        self.productions = new_productions
            

    def __conver_long_productions(self):    # Tercer paso en la conversión a Chomsky Normal Form. 
        
        # En este paso eliminamos frases muy largas, por ejemplo: A -> A c B D
        # En CNF solo pueden ser de máximo 2 de largo.
        
        new_productions = {}
        
        for left, right in self.productions.items():
            num_variable = 1
            for i, term in enumerate(right):
                characters = term.split()

                while len(characters) > 2:                          # Si el término de la regla tiene más de 2 símbolos.
                    new_variable = left + str(num_variable)         # Creamos una nueva regla añadiendole un número a la que ya estamos
                    new_production = characters[0:2]                # Cogemos esos símbolos y los guardamos
                    characters[0:2] = [new_variable]                # Sustituimos los 2 símbolos del término por la nueva variable
                    new_productions.setdefault(new_variable, []).append(' '.join(letter for letter in new_production))
                    num_variable += 1
                
                right[i] = ' '.join(letter for letter in characters)    # Actualizamos la regla ya existente para que coincida
            
        # Actualizamos nuestro diccionario
        for left, right in new_productions.items():
            self.productions[left] = right
            self.non_terminals.add(left)


    def __convert_non_terminal_with_terminal(self):     # Cuarto paso en la conversión a Chomsky Normal Form. 
        
        # Este es el último paso y se asegura de que todas las normas se cumplan.
        # Lo único que queda es que un un terminal solo puede producir exactamente un terminal o exactamente dos no terminales.
        # En este paso solo nos queda cambiar los casos del estilo: A -> B a.
        
        new_productions = {}
        
        for left, right in self.productions.items():
            num_variable = 1
            for i, term in enumerate(right):
                characters = term.split()
                if len(characters) == 2 and any(char in self.terminals for char in characters):  # Comprobamos que estemos en un caso que tengamos que arreglar
                    index = 0 if characters[0] in self.terminals else 1
                    terminal = characters[index]
                    
                    new_variable = left + '.' + str(num_variable)   # Creamos el nombre de la nueva variable añadiendo un punto y un número
                    num_variable += 1  
                    for left1, right1 in new_productions.items():   # Si ya existe una nueva regla que lleve al mismo terminal, no creamos una nueva variable
                        if right1[0] == terminal:
                            new_variable = left1
                            num_variable -= 1
                            break  
                    
                    new_production = [characters[index - 1]] + [new_variable]
                    right[i] = ' '.join(letter for letter in new_production)    # Actualizamos el término para que coincida
                    new_productions[new_variable] = [terminal]                  # Añadimos la regla

        # Actualizamos nuestro diccionario
        for left, right in new_productions.items():
            self.productions[left] = right
            self.non_terminals.add(left)


    def convert_to_cnf(self):   # Combinar todos los pasos para que se hagan seguidamente. 

        assert self.is_grammar_correct(), "The grammar is not correct"

        print("Converting from Context-Free-Grammar to Chomsky-Normal-Form\n")

        print("- - Removing empty productions")
        self.__remove_epsilon_productions()
        print(self)

        print("- - Removing unit productions")
        self.__remove_unit_productions()
        print(self)

        print("- - Convert long productions")
        self.__conver_long_productions()
        print(self)
        
        print("- - Convert productions with terminals and non-terminals")
        self.__convert_non_terminal_with_terminal()
        print(self)

        print("- - Finished - -")
        

    def is_phrase_in_grammar(self, phrase):
        pass


# Example usage
G = Grammar()
G.add_production('A', 'B D a')
G.add_production('A', 'D')
G.add_production('B', 'C b C')
G.add_production('C', '3')
G.add_production('C', 'A')
G.add_production('D', 'B')


print(G)

G.convert_to_cnf()
