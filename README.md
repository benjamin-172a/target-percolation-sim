# Percolation games with targets
This project computes results for the percolation game of Holroyd, Marcovici and Martin [[1]](#1) in the case with targets. The paper focuses largely on the regime with only traps, and this project is meant as a first step towards finding results with targets.

## Description of the game
The game is played on a network, but it can be thought of as being played on a checkerboard. A marker starts in the bottom-left corner of the board, which extends east and north infinitely. There is a parameter q between 0 and 1, and when the game initialises, each space on the board (except for the starting space) is designated as a target with probability q, independently for each space. The locations of the targets are known to the players. The two players take turns to move the marker either one space east or one space north (it is mandatory to move). The first player to move the marker on to a target wins.

Our question: as q varies, what is the probability that the first player wins, assuming perfect play from both players after the targets are generated? Holroyd, Marcovici and Martin addressed this question for a game with 'traps' that cause players to lose instead of targets, but were not able to address the case with targets.

You may consider that a situation may emerge where neither player has a winning strategy, and the game continues forever with neither player reaching a target. Holroyd, Marcovici and Martin proved that as long as q > 0, the probability that this occurs is actually zero, so we don't need to worry about this possibility.

## My solution
Consider the following strategy for player 2. Look down the main diagonal from the starting position until you see a target. Then, on each turn, if player 1 moves east, you move north, and vice versa, if player 1 moves north, you move east. Then, you will eventually hit this target!

Except, maybe there is a target near the main diagonal on the way.

<figure>
  <img src="https://github.com/user-attachments/assets/c7c67e7c-081e-4e4f-830d-cc01f62b67d0" width="400" height="400">
  <figcaption>Figure 1</figcaption>
</figure>



If there is another target at any of the pink spots, then player 1 can move to be diagonally away from it on their first move, and now they are on track to win first by using the same idea. However, this can happen multiple times. Imagine that player 1 does have a target on a pink spot, for example:

<figure>
  <img src="https://github.com/user-attachments/assets/154541ff-90ed-4468-8a74-76e3d21c9c60" width="400" height="400">
  <figcaption>Figure 2</figcaption>
</figure>

If the target shown on the pink square is the nearest such target to the start among pink squares, and player 1 moves north with the idea to eventually move on to the target, now player 2 can regain a good position if there are any targets on the orange squares, by moving to that diagonal. (We know that the squares east of the pink squares are not targets, as we assumed that the original target in the top right of the diagram was the first on the main diagonal, so we do not have the same effect there.)

This switching of control between the players can occur many times, but describes in full the behaviour of the game. We can set up an infinite series to find player 1's probability of winning. We will solve the game both on a complete 2D "lattice" (grid) and on the half-lattice "wedge" shown below, only containing the squares where x ≥ y.

<figure>
  <img src="https://github.com/user-attachments/assets/f16106a0-1c57-4ebb-a308-0d01ee8f1a11" width="400" height="400">
  <figcaption>Figure 3</figcaption>
</figure>

## Formula for player 1's winning probability

<b>This section is more mathematically intensive - feel free to skip, this just explains how the program derives the probability.</b>

Consider the situation in Figure 2 for the player facing the situation with the four orange squares, needing one of them to be a target. We will consider in general the 'active player' to be the one needing one of a certain number of squares (in this example, four) to be a target. And here, we are only considering wins and losses as they would happen if the game proceeded on this side of the main diagonal - we will need to consider each side of the main diagonal separately. There are various possibilities:

<ol>
  <li>The first square (counting from the south-west) is a target. The active player wins.</li>
  <li>The first square is not a target, but the second square is. Then the other player becomes the active player, with only one opportunity to find a target.</li>
  <li>The first two squares are not targets, but the third square is. Then the other player becomes the active player, with two opportunities to find a target.</li>
  <li>The first three squares are not targets, but the fourth square is. Then the other player becomes the active player, with three opportunities to find a target.</li>
  <li>None of the four squares are targets. The active player loses.</li>
</ol>

In general, we will write $P(k)$ for the probability that the active player wins facing $k$ squares. For example, with one square, they only win if it is a target (probability q), so $P(1) = q.$ With two squares, they also win if the first is a target (probability q), or they can win if the first is not a target (probability 1-q) and the second is, but then the other player will become the active player facing one square. So, $P(2) = q + (1-q)q(1 - P(1)).$

Continuing the same reasoning will show that, for example, $P(3) = q + (1-q)q(1 - P(1)) + (1-q)^2q(1 - P(2)),$ and, in general,

$$P(k) = \sum_{i=0}^{k-1} (1-q)^k q (1 - P(i)).$$

Since only one term is added each time, we can write $P(k+1)$ in terms of $P(k),$ plus one more term, for more efficient computation:

$$P(k+1) = P(k) + (1-q)^{k} q (1 - P(k)).$$

To calculate the winning probability for player 1, we have to consider that the first target on the main diagonal can appear at any space on that diagonal; its probability to appear $i$ squares diagonally away from the start is $(1-q)^{i-1}q,$ since each of the first $i-1$ squares need to not be targets and then the next one needs to be one. Then, we multiply this probability by player 1's winning probability if that is where the first target on the diagonal spawns, and sum to infinity (sum over all possible spaces that could be the first target on the diagonal).

In the wedge case, there is only one side of the diagonal for player 1 to use to try to win, and so his winning probability if the first target on the diagonal is on its $i$-th square is simply $P(i).$ Therefore,

$$P(\textrm{Player 1 wins on the wedge}) = \sum_{i=1}^{\infty} (1-q)^{i-1}qP(i).$$

In the full lattice case, there are two sides of the diagonal, and if either of them are favourable for player 1, he can use that one. He therefore will have two opportunities to win, with probability $P(i)$ each time; he will therefore win with probability $1 - (1 - P(i))^2$ (he only loses if an event with probability $1 - P(i)$ happens twice). Therefore,

$$P(\textrm{Player 1 wins on the full lattice}) = \sum_{i=1}^{\infty} (1-q)^{i-1}q(1 - (1 - P(i))^2).$$

It is these quantities that we will be interested in computing.

## Results

The program, percolation_targets_sim.py, is included as part of this repository.

Here, you can see the results!

<figure>
  <img src="https://github.com/user-attachments/assets/122be7a5-7ed4-4db5-9b0b-25060c9ff2c7">
  <figcaption>Figure 4: Player 1's probability of winning plotted against q in the wedge game.</figcaption>
</figure>

<figure>
  <img src="https://github.com/user-attachments/assets/8373de50-f138-47b2-b2fd-213e8cfd3150">
  <figcaption>Figure 5: Player 1's probability of winning plotted against q in the full grid game.</figcaption>
</figure>

The program also allows you to perform a polynomial fit for the results using Numpy, for a specified degree polynomial.
<figure>
  <img src="https://github.com/user-attachments/assets/90f85e09-700d-4256-a70f-18e533bae837">
  <figcaption>Figure 6: Degree 2 polynomial fit for the wedge case.</figcaption>
</figure>

The program also outputs its parameter estimates. In this case, the estimated polynomial is $y = 0.4367q^2 + 0.1904q + 0.3744.$

## References
<a id="1">[1]</a> 
Holroyd, A. E., Marcovici, I. and Martin, J.
Percolation games, probabilistic cellular automata, and the hard-core model.
Probability Theory and Related Fields, vol. 174, nos. 3-4, pp. 1187-1217 (2019).
