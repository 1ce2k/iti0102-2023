"""
Create a machine that dispenses money using 1€, 5€, 10€, 20€, 50€ and 100€ banknotes.

Given the sum, one must print out how many banknotes does it take to cover the sum. Task is to cover the sum as little
banknotes as possible.

Example
The sum is 72€
We use four banknotes to cover it. The banknotes are 20€, 50€, 1€ and 1€.
"""

amount = int(input("Enter a sum: "))
banknotes = 0
#
# Your code here
#
money = [100, 50, 20, 10, 5, 1]
for banknote in money:
    while amount >= banknote:
        amount -= banknote
        banknotes += 1

print(f"Amount of banknotes needed: {banknotes}")
