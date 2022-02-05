# turdle
Aid for solving Wordle

### How to Solve Wordle

W is the set of words that could be the hidden answer.

G is the set of words you can guess. (G might include words not in W.)

h(g, w) is the hint that Wordle returns when you guess g but the answer is really w.  

A partition of a set is a collection of disjoint subsets of the set, where every element
of the original set is in one of he subsets.  

The partition p(g, W)={p1,p2,..} is a partition of W in which all words in a subset, pi, have the same hint
when g is guessed and no words in different subsets have the same hint, i.e.:
for all wj,wk in pi, h(g,wj)=h(g,wk).  Further if wj is in pi and wk is not in pi then
h(g,wj)!=h(g,wk).

If the set of possible words is W, the hidden word is w, and the guess is g, then the 
hint returned when g is guessed reduces the set of possible words to pw, where pw is 
the subset in the partition p(g,W) which contains w.

Clearly it's good for pw to be as small as possible. Turdle's strategy is to pick a guess
g such that the "expected value" of pw, `E[pw]` is as small as possible.  Given a guess g, the expected
value of pw is:

	E[pw] = Sumi (|pi|*P(pi,g))
I.e., the expected size of pw is the sum, over all subsets pi of the partition p generated 
for guess g, of the size of pi (|pi|) times the probability that pi is the subset indicated 
by the returned hint.

Note that P(pi,g) is simply the probability that the hidden word, w, is in pi and that, in turn,
is determined by its size, i.e.:

	P(pi,g) = |pi|/W
So

	E[pw] = Sumi (|pi|*|pi|/W)
or

	E[pw] = Sumi (|pi|^2) / W
The best guess, g, then is the guess whose value for E[pw] is the minimum. 

Note that optimal guesses most evenly partition a set of possible words into even sized subsets. For example say |W| is 9 and one guess separates into three groups of size:

	1, 1, 7
while another guess evenly divides the list into three equally sized groups:

	3, 3, 3
	
The value of E[pw] for the first guess is (1+1+49)/9 = 5.7

The value of E[pw] for the second guess is (9+9+9)/9 = 3

  

Note that the best guess, g, might not be one of the words in L!  If W = {'shard','shark','sharp'} then g='adept' will tell you immediately which of the three words is correct, while guessing any of the words in W will most likely reduce the list of possibilities to two.


