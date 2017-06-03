# Battlefield
This is a utility package that contains game and robot engines to help developers create games or robots.

## Installation
just install it with pip
```
$ pip install battlefield
```

## Usage
Here's a basic example of using the library.

> **Note**: the library is under heavy development and it may change a lot

### Create a game
```python
import random

from battlefield.engine import TurnEngine


class Math(TurnEngine):
    def step(self, robot):
        a = random.randint(1,100)
        b = random.randint(1,100)
        op = random.choice(['+', '-', '*', '/'])
        if op == '+':
            self.answer = a + b
        elif op == '-':
            self.answer = a - b
        elif op == '*':
            self.answer = a * b
        elif op == '/':
            self.answer = a / b
        resp = yield ' '.join([a, op, b])
        if int(resp) == self.answer:
            robot.score += 1

    def end(self):
        if self.robots[0].score == self.robots[1].score:
            return 'DRAW'
        elif self.robots[0].score > self.robots[1].score:
            return 'FIRST'
        else:
            return 'SECOND'
```
This engines generate a simple math question and asks the robots to answer.
 
### Create a robot
```python
from battlefield.robot import Robot


class MathSolver(Robot):
    def step(self, data):
        a, op, b = data.split()
        a, b = int(a), int(b)
        if op == '+':
            return str(a + b)
        elif op == '-':
            return str(a - b)
        elif op == '*':
            return str(a * b)
        elif op == '/':
            return str(a / b)
```
This robot receive a question from the engine above in each step and respond to it.
