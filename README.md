# zkSNARK-NP-Problem

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

## Prover
1. Randomly swap the symbol used to represent each variable.


