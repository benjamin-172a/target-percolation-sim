import numpy as np
import time
from matplotlib import pyplot as plt
import sys

qs = []
probabilities = []

"""
TAKING INPUT DATA
Allows the user to input the following information.
- q precision level. E.g. if the precision is 0.01, then evaluate at q = 0.01, 0.02, ..., 0.99.
- Which grid structure to use. W for the wedge (half of a grid - see README) or the full 2D grid.

Only certain inputs are valid.
- q should be a positive number, and the program only accepts a value 0.05 or less.
(If q is too large, the results are less informative.)
- The grid structure has to be one of the two valid options, W or Z (the program accepts either lower or upper case).
"""
valid = 0
while valid == 0:
    prec = input("What level of precision to use? (Distance between values of q.)")
    try:
        prec = float(prec)
        if prec > 0 and prec <= 0.05:
            valid = 1
        else:
            print("You should choose a positive precision, and it should be 0.05 or less.")
    except ValueError:
        print("Invalid input, try again.")

valid = 0
while valid == 0:
    struc = input("What lattice structure to use? Input W for the wedge Z_2 (x>=y) or Z for the complete grid Z_2.")
    if struc.upper() == "W" or struc.upper() == "Z":
        valid = 1
    else:
        print("Invalid input, try again.")
    
for q in np.arange(prec, 1, prec): # Find player 1's winning probability for q=prec,2*prec,...,1.
    MaxK = int(50*(1/q)) # This program uses a finite sum approximation of an infinite sum. This line ensures that enough terms are evaluated for a good approximation.
    #start_time = time.time() # Optional - track how long the program takes.

    ### Calculate the values of P(k).
    P = [0]
    for k in range(MaxK):
        P.append( P[k] + q * (1 - P[k]) * (1-q)**k )

    ### Calculate the probability that player 1 wins.
    Sum = 0
    for i in range(1,MaxK+1):
        if struc.upper() == "W":
            Sum = Sum + P[i] * q * (1-q)**(i-1)   ### Z_2 (x >= y) wedge
        else:
            Sum = Sum + (1 - (1 - P[i])**2) * q * (1-q)**(i-1)    ### Z_2

    # Adds a pair of matched values, q to qs and Sum to probabilities, a matching pair (q,Sum) of the winning probability for player 1 at value q.
    qs.append(q)
    probabilities.append(Sum)

# Optional - print result lists and/or time taken. Printing result lists not recommended for a small value of q.
#print(qs)
#print(probabilities)
#end_time = time.time()
#print("The time taken was",end_time-start_time)

# Plot player 1's winning probability (list probabilities) against q.
plt.plot(qs, probabilities)
plt.xlabel("q")
plt.ylabel("Probability of win for player 1")
if struc.upper() == "W":
    plt.title("Winning probability for player 1 against q in Z_2 wedge game")
else:
    plt.title("Winning probability for player 1 against q in Z_2 grid game")

# Optional - save the plot.
plt.savefig("percolation_game_data.pdf")

plt.show()

"""
Set up our variables for polynomial fitting. We are estimating how the input variable x (q values)
relates to the outcome variable y (winning probabilities).
"""
x = qs
y = probabilities

"""
POLYNOMIAL FITTING
Here, the user has the option to plot a polynomial fit of the results and see the coefficients of the polynomial.
"""
# User chooses a positive integer polynomial degree.
valid = 0
while valid == 0:
    deg_in = input("What degree for the polynomial fit? If you do not want to try a fit, enter 0.")
    try:
        deg = int(deg_in)
        deg_in = float(deg_in)
        if deg - deg_in == 0 and deg >= 0: # Check that the user inputted a non-negative integer.
            valid = 1
        else:
            print("You should choose a positive integer.")
    except ValueError:
        print("Invalid input, try again.")

# If the user chose not to use a polynomial fit, quit the program.
if deg == 0:
    sys.exit()

# Fit polynomial using numpy polyfit.
coeffs = np.polyfit(x, y, deg)
polynomial = np.poly1d(coeffs)

# Print polynomial equation so the user can see the estimated co-efficients.
print("Polynomial function:")
print(polynomial)

# Use x values from qs for plotting polynomial
y_p = polynomial(qs)

# Plot the original data and fitted polynomial
plt.plot(x, y, label="Winning probability data")
plt.plot(qs, y_p, label=f"Degree {deg} polynomial Fit")
plt.xlabel("q")
plt.ylabel("Probability of win for player 1")
plt.legend()

# Optional - save the plot.
plt.savefig("percolation_polyfit.pdf")

plt.show()

sys.exit()

