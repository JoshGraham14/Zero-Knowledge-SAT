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

from typing import List, Tuple
# from random import shuffle
import Crypto.Random.random as crypto_random
from copy import deepcopy


def swap_var_names(cnf: List[List[str]], 
                    vars: List[str]) -> Tuple[List[List[str]], List[str]]:
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
    return new_vars, new_cnf



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

    print('Original cnf:')
    print_nice(problem)


    #new_vars, new_cnf = swap_var_names(problem, vars)
    #new_cnf = permute_vars(new_cnf)
    new_cnf, var_perm_mapping = permute_vars(problem)
    print_nice(new_cnf)
    print(var_perm_mapping)


if __name__ == '__main__':
    main()
