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
import Crypto.Random.random as crypto_random
import copy
from prover import util as prover
from verifier import util as verifier


def get_clause(cnf: List[List[str]], solution: Dict[str, bool], 
            clause_num: int) -> Tuple[List[str], Dict[str, bool]]:
    '''
    Returns a clause from the modified CNF formula along with the variable
    values that satisfy the clause.

    @param cnf: Formula in CNF
    @param solution: A dictionary containing the variable-value mappings to
                     satisfy the CNF formula
    @param clause_num: Indicates which clause should be returned (0-indexing)

    @returns a tuple containing a single clause from the CNF formula along
             with the variable-value mapping that satisfies the clause
    '''
    if clause_num > len(cnf) - 1:
        raise ValueError(f'There are not {clause_num} clauses \
                            in the CNF formula')

    return cnf[clause_num], solution    


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
    # necessary if a single clause is given as a 1D list
    if not isinstance(cnf[0], list):
        cnf = [cnf]

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


def simulate(problem: List[List[str]], solution: Dict[str, bool], vars: List[str]) -> bool:
    '''
    Simulate a zero-knowledge proof protocol between a prover and a verifier. Returns True
    if the prover can successfully prove their knowledge for n^2 rounds, where n represents
    the number of conjunctions in the given problem. Returns False otherwise.
    '''
    orig_cnf = copy.deepcopy(problem)

    for i in range((len(orig_cnf) - 1)**2):
        print(f'\n========================================= Round {i} ==========================================\n')
        # Prover
        new_cnf, neg_map, new_solution = prover.negate_vars_randomly(problem, vars, solution)
        new_cnf, new_vars = prover.swap_var_names(new_cnf, vars)
        new_cnf, clause_perm_mapping = prover.permute_clauses(new_cnf)
        new_solution = prover.get_new_solution(new_solution, vars, new_vars)
        new_cnf, var_perm_mapping = prover.permute_vars(new_cnf)
        
        # Verifier
        option: int = crypto_random.randint(0, 1)

        # Verify jumbled cnf formula
        if option == 0:
            ver_cnf = verifier.permute_vars(new_cnf, var_perm_mapping)
            ver_cnf = verifier.permute_clauses(ver_cnf, clause_perm_mapping)
            ver_cnf = verifier.swap_var_names(ver_cnf, new_vars, vars)
            ver_cnf = verifier.negate_vars(ver_cnf, neg_map)
            if ver_cnf == orig_cnf:
                print('Confidence gained from verifying jumbled solution')
            else:
                print('Verification of jumbled formula went wrong, prover can\'t be trusted')
                return False
        # Verify single clause
        else:
            clause_num: int = verifier.choose_clause(len(problem))
            # The prover then calls this function to get the clause
            # for the verifier
            ver_clause, ver_solution = prover.get_one_clause(new_cnf, 
                                            clause_num, new_solution)
            if verifier.verify_clause(ver_clause, ver_solution):
                print('Confidence gained from verifying clause')
            else:
                print('Verification of clause went wrong, prover can\'t be trusted')
                print(f'{ver_clause = }')
                print(f'{ver_solution = }')
                return False

    return True



def main() -> None:
    problem: List[List[str]] = [['a', 'b', '~c'], ['~a', '~b', 'd'],
                                ['~a', 'b', '~d'], ['b', '~c', 'd']]
    solution: dict[str, bool] = {'a': True, 'b': False, 'c': False, 'd': False}
    vars: List[str] = ['a', 'b', 'c', 'd']

    print('Original CNF:')
    print_nice(problem)

    if simulate(problem, solution, vars):
        print('The prover can be trusted!')
    else:
        print('The prover cannot be trusted!')


if __name__ == '__main__':
    main()
