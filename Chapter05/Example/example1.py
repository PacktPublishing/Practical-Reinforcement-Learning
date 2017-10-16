#We will import all the scientific libraries using _numPy package
import numpy as _numP

# Trowing a _varDice_rand for N intervals and evaluating the anticipation

_varDice_rand = _numP.random.randint(low=1, high=7, size=3)
print("Anticipation (throughing 3 intervals): " + 
  str(_numP.mean(_varDice_rand)))

_varDice_rand = _numP.random.randint(low=1, high=7, size=10)
print("Anticipation (throughing 10 intervals): " +
  str(_numP.mean(_varDice_rand)))

_varDice_rand = _numP.random.randint(low=1, high=7, size=100)
print("Anticipation (throughing 100 intervals): " +
  str(_numP.mean(_varDice_rand)))

_varDice_rand = _numP.random.randint(low=1, high=7, size=1000)
print("Anticipation (throughing 1000 intervals): " +
  str(_numP.mean(_varDice_rand)))

_varDice_rand = _numP.random.randint(low=1, high=7, size=100000)
print("Anticipation (throughing 100000 intervals): " +
  str(_numP.mean(_varDice_rand)))