# Memory Kings in Python 3 by G. Scary Tontini

main.py, runs the game in Pygame

memorykings0.5.py stable running all rules for Multiplayer and Solo modes on Terminal

## TODO

- Showing score on the game window
- Add Alternate Setup option

## NON STANDARD MODULES

For main: import pygame

For old_versions/memorykings0.5.py: import pyinputplus, termcolor

## KNOWN ISSUES

- During Pawns Placement: 
    In the Solo variant, player should only be able to place pawns on cards with the same Back as the Counter Pawn, and not place multiple pawns on the same card.
    In the Multiplayer game, players should only be able to place pawns on cards with White Back, and not place multiple pawns on the same card.
- Special Power of the Queen is a hot mess and needs refactoring (probably together with the rest of the program).

## LINKS

The rulebook .PDF can be downloaded in: https://www.thegamecrafter.com/games/memory-kings/download/E9768FE4-E707-11EA-AD8C-E151EE47BC41

"How to Play" video for the multiplayer game (2-4) players: https://youtu.be/snqjQtYmv_Q

More relevant links: https://linktr.ee/memorykings
