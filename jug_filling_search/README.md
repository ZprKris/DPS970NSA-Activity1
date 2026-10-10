# Three-Jug Water-Measuring Problem

## Problem

There are three jugs with capacities of 12, 8, and 3 gallons. Jugs can be filled from a water faucet, empitied onto the ground, and poured into each other until the source is empty or the destination is full. The goal is to fill one jug with exactly one gallon. 

## State-space representation

A state is a tuple `(A, B, C)`, where A is 12-gallon jug, B is 8-gallon jug, C is 3-gallon jug.

## Breadth-first search

`jug_fill.py` uses breadth-first search (BFS) to search this state space. It
keeps a FIFO frontier using `collections.deque` and a set of explored states
to avoid visiting a state more than once. Each frontier entry contains a state
and the path of actions used to reach it.

The search removes the oldest entry from the frontier, checks whether it meets
the goal, then adds each unexplored successor to the end of the frontier. Since
each action has equal cost, BFS finds a solution using the fewest actions. It
returns the sequence of actions and resulting states, or `None` if no solution
is found.

## Run

From this directory, run:

```bash
python jug_fill.py
```