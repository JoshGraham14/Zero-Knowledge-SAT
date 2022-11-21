from typing import List, Tuple, Dict
import Crypto.Random.random as crypto_random


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



if __name__ == '__main__':
    clause = ['~a', 'b', '~c']
    clause_solution = {'d': False, 'b': False, 'c': False, 'a': True}
    print(verify_clause(clause, clause_solution))
