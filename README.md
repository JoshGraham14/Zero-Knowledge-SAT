# zkSNARK-NP-Problem

## Setup:

1. If you don't already have the venv folder, create the environment by running `python3 -m venv venv`
2. To activate the environment, run `venv\Scripts\activate.bat` if on Windows, `source venv/bin/activate` if on MacOS/Linux
3. pip install -r requirements.txt to install any packages needed for the backend
4. In the `main` function of the `main.py` file, enter your CNF formula for the variable `problem` (a default problem is provided)
5. In the `main` function of the `main.py` file, enter your solution for the CNF problem for the variable `solution` (a default solution is provided)
6. In the `main` function of the `main.py` file, enter the variable names used in your cnf in the list `vars` (a default list of vars is provided)

# How to run
From the base directory, run `python3 main.py` if on MacOS/Linux or `python main.py` if on Windows

This is my course project for CISC 468 (Cryptography), it is a Python implementation of a zkSNARK (**Z**ero-**K**nowledge **S**uccinct **N**on-interactive **AR**guments of **K**nowledge) to prove/verify the solution of an NP-class problem.

I would eventually like for this implementation to be able to prove/verify the solution to any NP-class problem. However, to make this possible I have chosen to create a zkSNARK for the 3-SAT problem. 3-SAT is a subset of the Boolean Satisfiability problem where each clause in the CNF (Conjuctive Normal Form) formula contains 3 variables. Every SAT problem can be reduced to 3-SAT, furthermore, every NP-class problem can be reduced to SAT. Therefore, a zkSNARK for the 3-SAT problem can techincally be used to prove/verify any problem in the class NP.

Before continuing, I would like to clarify some terminology.

**CNF** = Conjunctive Normal Form   
Example of a CNF formula `(a ∨ b ∨ ¬c) ∧ (¬a ∨ ¬b ∨ d)`

**∨** = Disjunction (logical OR)   
**∧** = Conjunction (logical AND)   
**¬** = Negation (logical NOT)   

**Variable** = A symbol used to represent a true or false value  
Example: in the CNF formula above, the variables are `a`, `b`, `c`, and `d`.

**Clause** = A collection of three variables, separated by disjunctions, surrounded by brackets. Each clause is connected by a conjunction.  
Example: in the CNF formula above, the clauses are `(a ∨ b ∨ ¬c)` and `(¬a ∨ ¬b ∨ d)`

**Value** = A mapping of `True` or `False` assigned to each variable.

**Satisfiability** = an instance of 3-SAT is satisfiable if there exists a mapping of values for each variable that causes the entire CNF formula to evaluate to true.   
Example: A satisfying mapping for the above CNF formula would be `{a: True, b: False, c: False, d: False}`

# Process for zero-knowledge proof of 3-SAT
Given a situation where there is a prover and a verifier, the verifier has a 3-SAT problem in CNF and wants to verify that the prover knows a correct mapping to satisfy the fomula. Here is the process each person must take:

## Prover
1. Randomly swap the symbols used to represent each variable.
2. Randomly permute the clauses in the CNF formula.
3. Randomly permute the variables in each of the clauses.
4. Swap the value of approximately 1/2 of the variables and subsequently negate those variables in the CNF formula.

## Verifier
For each round of the verification (it will take many rounds for the verifier to have a high level of confidence that the prover has a satisfying solution), the verifier has two choices:

1. Choose to view the new CNF formula after all permutations, swaps, and negations have been performed, along with the mappings for how the variables and clauses were permutated, swapped, and negated; without seeing the values assigned to each variable.

2. Choose to view one random clause from the new CNF formula, with the associated values of the variables.

If choice 1 is selected, the verifier can reverse the negations, permutations, and swaps to confirm that the formula they were sent is in fact equivalent to the original formula.

If choice 2 is selected, the verifier can confirm that the clause evaluates to true with the provided variable-value mappings.




