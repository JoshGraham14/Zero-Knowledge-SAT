# Problems

-   Actually implementing a solution to the SAT problem would be very difficult
    -   Involves implementing or using an external propositional logic library
    -   Would need to write the algorithm, which due to being in the class NP, would have time complexity worse than polynomial

# Potential Solutions

-   Program doesn't actually solve the SAT problem, just provides a zkSNARK if it has a solution
-   This means for demonstration purposes, a predetermined problem/solution can be hardcoded
    -   Then as long as the zero-knowldge proof aspect is not hardcoded, this could technically work for any SAT solution
    -   Meaning that if there was a SAT-solver implemented, it could use this system

# Ideas

-   Focus on 3-SAT, the uniformity of the clauses will provide better structure to provide a zero-knowledge proof
-   Any general SAT problem can be reduced to 3-SAT, so this still works for any SAT problem

From https://cs.stackexchange.com/questions/135457/is-there-a-zero-knowledge-proof-for-sat#:~:text=3%2DSAT%20is%20used%20so,proof%20for%20SAT%20as%20well.

For each round the prover should:

-   Permute the variable labels randomly.
-   Permute the clause order in the formula randomly.
-   Permute the variable order in each clause randomly.
-   Invert the parity of each variable's literals randomly with probability one-half.
-   Commit to this new formula, but in a way that is hidden from the verifier.
-   Commit to a satisfying assignment of this new formula, but in a way that is hidden from the verifier.

After this is done, the verifier can ask the prover for either:

-   The new formula and the permutation mappings so that he can verify that the new formula is the same as the original formula, or
-   One clause of the new formula and the variable assignments for the variables in that clause, taken from the satisfying assignment previously committed to.
