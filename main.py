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
from typing import List
from prover import util as prover


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

    print('Original CNF:')
    print_nice(problem)

    new_cnf, neg_map, new_solution = prover.negate_vars_randomly(problem, vars, solution)
    new_cnf, new_vars = prover.swap_var_names(problem, vars)
    new_cnf, clause_perm_mapping = prover.permute_clauses(new_cnf)
    new_cnf, var_perm_mapping = prover.permute_vars(new_cnf)
    new_solution = prover.get_new_solution(new_solution, vars, new_vars)
    
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
