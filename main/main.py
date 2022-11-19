'''
Implementation of a zkSNARK for the 3-SAT problem.

Example 3-SAT problem/solution

Problem:
(a | b | ~c) & (~a | ~b | d) & (~a | b | ~d) & (b | ~c | d)

solution:
a: True
b: False
c: False
d: False
'''

from typing import List, Tuple, Dict
# from random import shuffle
import Crypto.Random.random as crypto_random
from copy import deepcopy


def swap_var_names(cnf: List[List[str]], 
                    vars: List[str]) -> Tuple[List[List[str]], Dict[str, str]]:
    '''
    Randomly swaps the variable names in a CNF formula.
    @param cnf: Formula in CNF
    @param vars: List of the variables used in the CNF

    @returns A tuple containing the CNF with swapped vars and the mapping 
             for the new variable names
    '''
    new_vars = vars.copy()
    new_cnf = deepcopy(cnf)
    crypto_random.shuffle(new_vars)

    for i, clause in enumerate(cnf):
        for k, atom in enumerate(clause):
            for j, var in enumerate(vars):
                if len(atom) == 2:
                    if atom[1] == var:
                        new_cnf[i][k] = '~' + new_vars[j]
                elif atom == var:
                    new_cnf[i][k] = new_vars[j]

    var_swap_mapping = {new_vars[i]: vars[i] for i in range(len(vars))}
    return new_cnf, var_swap_mapping



def permute_vars(cnf: List[List[str]]) \
                -> Tuple[List[List[str]], List[List[int]]]:
    '''
    Permutes the variables in each clause of the CNF formula. The new permuted
    CNF is returned along with a mapping for how each variable was permuted.
    Here is how the mapping is read:\n
    Given the clause [a, b, c] and mapping [2, 0, 1], the clause becomes
    [c, a, b]. Each number in the mapping list is the original index
    of the element that now exists in that position. So for the given
    example, mapping[0] = 2, which means clause[2] is now in position
    0 of the new permuted clause. 
    @param cnf: Formula in CNF
    @returns A 2-tuple whose first element is the new cnf formula with
             permuted variables and second element is the list mapping
             how the variables were permuted.
    '''
    var_perm_mapping = []
    for clause in cnf:
        indices = [0, 1, 2]
        crypto_random.shuffle(indices)
        old_clause = clause.copy()
        for i in range(3):
            clause[i] = old_clause[indices[i]]
        var_perm_mapping.append(indices)

    return cnf, var_perm_mapping


def permute_clauses(cnf: List[List[str]]) \
                -> Tuple[List[List[str]], List[List[int]]]:
    '''
    Permutes the clauses in a cnf formula randomly. The new permuted cnf is
    returned along with a mapping for how the clauses were permuted. A mapping
    can be read as follows:
    mapping [2, 3, 1, 0] means orig_cnf[2] = permuted_cnf[0],
    orig_cnf[3] = permuted_cnf[1], orig_cnf[1] = permuted_cnf[2], and
    orig_cnf[0] = permuted_cnf[0].
    @param cnf: Formula in CNF
    @returns A 2-tuple whose first element is the new cnf formula with
             permuted clauses and second element is the list mapping
             how the clauses were permuted.
    '''
    indices = [i for i in range(len(cnf))]
    crypto_random.shuffle(indices)
    old_cnf = deepcopy(cnf)
    for i in range(len(cnf)):
        cnf[i] = old_cnf[indices[i]]
    return cnf, indices


def negate_vars_randomly(cnf: List[List[str]], vars: List[str], 
                value_mapping: Dict[str, bool]) \
                -> Tuple[List[List[str]], List[bool], Dict[str, bool]]:
    '''
    Randomly negates all instances of roughly 50% of the variables, as well as
    the value mapped to that variable to preserve satisfiability.
    @param cnf: Formula in CNF
    @param vars: List of the variables used in the CNF
    @param value_mapping: Dictionary assigning True/False values to each 
                          variable

    @returns A tuple containing the CNF with the negated vars, a list 
             describing which vars were changed, and the new mapping for the 
             variables values
    '''
    # generate True/False values to associate with each variable
    # if True, that variable will be negated
    neg_map: List[bool] = [crypto_random.randint(0,1) == 1 for i in range(len(vars))]

    for clause in cnf:
        for i, symbol in enumerate(clause):
            for j, var in enumerate(vars):
                if neg_map[j]:
                    if var == symbol:
                        clause[i] = '~' + clause[i]
                    elif len(symbol) == 2 and var == symbol[1]:
                        clause[i] = clause[i][1]
    # fix variable mapping for negated variables
    for i, val in enumerate(neg_map):
        if val:
            value_mapping[vars[i]] = not value_mapping[vars[i]]

    return cnf, neg_map, value_mapping


def get_new_solution(old_solution: Dict[str, bool], vars: List[str],
                new_var_names: Dict[str, str]) -> Dict[str, bool]:
    '''
    Obtain the solution to the modified CNF formula after variables have been
    negated and have new names.

    @param old_solution: The old variable-value mappings
    @param vars: List of the variables used in the CNF
    @param new_var_names: A dictionary containing where each key is the new
                          name of a variable and the value is the old name
    
    @returns A dictionary containing a key for each variable where the value
             is the new True/False value for that variable
    '''
    new_solution = {}
    
    for i, var in enumerate(vars):
        new_name = new_var_names[var]
        val = old_solution[var]
        #print(f'{var} has been changed to {new_name}, with a value of {val}')
        new_solution[new_name] = val

    return new_solution


def print_nice(cnf: List[List[str]], separate_lines: int=0) -> None:
    '''
    Prints a CNF formula in a readable format with unicode symbols for 
    disjunction, conjunction, and negation.
    @param cnf: Formula in CNF
    @param separate_lines: optional keyword argument to restrict how many 
                           clauses should be printed per line. (Default is 0,
                           meaning no restriction to number of clauses per
                           line)
    '''
    num_clauses = len(cnf)
    print('(', end='')
    for i, clause in enumerate(cnf):
        for j, var in enumerate(clause):
            # if the var has been negated
            if len(var) == 2:
                print(f'¬{var[1]}', end='')
            else:
                print(f'{var}', end='')
            # if it is not the last element in the clause
            if j != 2:
                print(' ∨ ', end='')
        # if the user wants to separate the output on multiple lines
        if separate_lines != 0:
            # if max number of clauses are on line, go to a new line
            if (i + 1) % separate_lines == 0 and i != num_clauses - 1:
                print(') ∧\n(', end='')
            # if it isn't the last clause and not max number per line
            elif i < num_clauses - 1:
                print(') ∧ (', end='')
            else:
                print(')')
        # if it isn't the last clause
        elif i < num_clauses - 1:
            print(') ∧ (', end='')
        # elif i == num_clauses - 1:
        else:
            print(')')


def main() -> None:
    problem: List[List[str]] = [['a', 'b', '~c'], ['~a', '~b', 'd'],
                                ['~a', 'b', '~d'], ['b', '~c', 'd']]
    solution: dict[str, bool] = {'a': True, 'b': False, 'c': False, 'd': False}
    vars = ['a', 'b', 'c', 'd']

    # print('Original CNF:')
    # print_nice(problem)

    new_cnf, neg_map, new_solution = negate_vars_randomly(problem, vars, solution)
    new_cnf, new_vars = swap_var_names(problem, vars)
    new_cnf, clause_perm_mapping = permute_clauses(new_cnf)
    new_cnf, var_perm_mapping = permute_vars(new_cnf)
    new_solution = get_new_solution(new_solution, vars, new_vars)
    
    print('New CNF:')
    print_nice(new_cnf)
    print(f'New solution: {new_solution}')
    print(f'Variable permutation mapping: {var_perm_mapping}')
    print(f'Clause permutation mapping: {clause_perm_mapping}')
    print(f'Variable swap mapping: {new_vars}')
    print(f'Variable negation mapping: {neg_map}')
    print(f'The variables are: {vars}')


if __name__ == '__main__':
    main()
