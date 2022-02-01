# turdle
Aid for solving Wordle

### How to Solve Wordle
Given a list of words, L, a guess, G, subdivides the words into sets based on the possible results of the guess.
Each guess results in a row of five squares, each grey (no match), yellow (match in another position) or green (match in the guessed position).
Therefore there are 3^5 = 243 groups of words for each guess.  The goal is to select a guess, G, such that the expected size
is minimized.   If the total number of words is n and the size of each group, g, is g(i), i=1->243, then the quantity to minimize
is f(G) = Sum-i(g(i)/n * g(i)) = Sum-i(g^2(i))/n.  So the brute force solution is to compute f(G) for each word in the list of possible
words.  Note that the best guess, G, might not be one of the words in L!  


