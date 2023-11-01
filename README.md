## Goal

The objective is to determine whether the player who takes the first turn or the one who goes second is guaranteed to win or achieve a tie in the game, assuming both players make optimal moves at every step.

## Introduction to the game

* Name: Gobblet Gobblers (奇雞連連)

* Rules:

    **【Equipment】**

    * 12 playing pieces called Gobblers, with 6 in red and 6 in blue.

    * A 3x3 chess board

    **【Playing】**

    Each player selects a color.

    In their turn, players can choose to:

    1. Place a new Gobbler on the board in an empty space or on top of a smaller Gobbler.

    2. Move one of their Gobblers already on the board to an empty space or on top of a smaller Gobbler.

    **【Winning】**

    If you are the first player to get 3 pieces in a row, you win!

* Play the game online at:
https://gobblet-gobblers.netlify.app/

## Achieving the Goal: The Algorithm

The algorithm same as https://github.com/patrick-csliu/Tic-Tac-Toe-Prove/blob/version3/README.md

## Issues

order by severity
1. The tree is too deep, which leads to a stack overflow when using recursion.

1. The number of possible "board positions" is on the order of magnitude of $10^9$.

    Approximation: $\frac{all possible in a layer^{three layer of gobbler}}{symmetry} = \frac{2117^3}{8} = 1.118 \times 10^9$
