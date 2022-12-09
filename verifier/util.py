from typing import List, Tuple, Dict
import Crypto.Random.random as crypto_random

from main import print_nice
import copy


def verify_clause(clause: List[str], solution: Dict[str, bool]) -> bool:
    '''
    Verifies whether a given clause is satisfied by a given solution.

    @param clause: a single clause of a CNF formula.
    @param solution: A dictionary containing the variable-value mappings to
                     satisfy the CNF formula
    
    @returns True if the clause is satisfiable, False otherwise
    '''
    for var in clause:
        if len(var) == 2:
            if not solution[var[1]]:
                return True
        else:
            if solution[var]:
                return True
    
    return False


def choose_clause(num_clauses: int) -> int:
    '''Chooses a random clause number of the CNF formula.'''
    return crypto_random.randint(0, num_clauses - 1)


def permute_vars(cnf: List[List[str]], 
        var_perm_mapping: List[List[int]]) -> List[List[str]]:
    '''Undo the permutation of the variables.'''
    new_cnf = copy.deepcopy(cnf)

    for i, clause in enumerate(cnf):
        old_clause = clause.copy()
        for j in range(3):
            new_cnf[i][var_perm_mapping[i][j]] = clause[j]
    return new_cnf


def permute_clauses(cnf: List[List[str]], 
        clause_perm_mapping: List[List[int]]) -> List[List[str]]:
    '''Undo the permutation applied to the clauses.'''
    new_cnf = copy.deepcopy(cnf)
    for i, clause in enumerate(cnf):
        new_cnf[clause_perm_mapping[i]] = clause

    return new_cnf


def swap_var_names(cnf: List[List[str]], 
        var_mapping: Dict[str, str], vars: List[str]) -> List[List[str]]:
    '''Swaps the variable names back to what they originally were.'''

    new_cnf = copy.deepcopy(cnf)

    for i in range(len(vars)):
        for j, clause in enumerate(cnf):
            for k, var in enumerate(clause):
                if len(var) == 2:
                    new_cnf[j][k] = '~' + var_mapping[var[1]]
                else:
                    new_cnf[j][k] = var_mapping[var]

    return new_cnf


def negate_vars(cnf: List[List[str]], neg_map: List[bool]) -> List[List[str]]:
    '''(Un)negate the vars that were negated by the prover.'''
    new_cnf = copy.deepcopy(cnf)

    for j, clause in enumerate(cnf):
        for k, var in enumerate(clause):
            if len(var) == 2:
                if neg_map[var[1]]:
                    new_cnf[j][k] = var[1]
            else:
                if neg_map[var]:
                    new_cnf[j][k] = '~' + var

    return new_cnf

if __name__ == '__main__':
    problem: List[List[str]] = [['a', 'b', '~c'], ['~a', '~b', 'd'],
                                ['~a', 'b', '~d'], ['b', '~c', 'd']]
    vars = ['a', 'b', 'c', 'd']
    clause = ['~a', 'b', '~c']
    clause_solution = {'d': False, 'b': False, 'c': False, 'a': True}
    print(verify_clause(clause, clause_solution))
    print_nice(problem)

