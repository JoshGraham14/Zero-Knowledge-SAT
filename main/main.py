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


def main() -> None:
    problem: List[List[str]] = [['a', 'b', '~c'], ['~a', '~b', 'd'],
                                ['~a', 'b', '~d'], ['b', '~c', 'd']]
    solution: dict[str, bool] = {'a': True, 'b': False, 'c': False, 'd': False}


if __name__ == '__main__':
    main()
