# PSET 1 - Part C

"""
Part C: Finding the right amount to save away
In Part B, you had a chance to explore how both the percentage of your salary that you save each month
and your annual raise affect how long it takes you to save for a down payment. This is nice, but
suppose you want to set a particular goal, e.g. to be able to afford the down payment in three years.
How much should you save each month to achieve this? In this problem, you are going to write a
program to answer that question. To simplify things, assume:
1. Your semi­annual raise is .07 (7%)
2. Your investments have an annual return of 0.04 (4%)
3. The down payment is 0.25 (25%) of the cost of the house
4. The cost of the house that you are saving for is $1M.

You are now going to try to find the best rate of savings to achieve a down payment on a $1M house in
36 months. Since hitting this exactly is a challenge, we simply want your savings to be within $100 of
the required down payment.
In​ ps1c.py​, write a program to calculate the best savings rate, as a function of your starting salary.
You should use ​bisection search​ to help you do this efficiently. You should keep track of the number of
steps it takes your bisections search to finish. You should be able to reuse some of the code you wrote
for part B in this problem.
Because we are searching for a value that is in principle a float, we are going to limit ourselves to two
decimals of accuracy (i.e., we may want to save at 7.04% ­­ or 0.0704 in decimal – but we are not
going to worry about the difference between 7.041% and 7.039%). This means we can search for an
integer​ between 0 and 10000 (using integer division), and then convert it to a decimal percentage
(using float division) to use when we are calculating the ​current_savings​ after 36 months. By using
this range, there are only a finite number of numbers that we are searching over, as opposed to the
infinite number of decimals between 0 and 1. This range will help prevent infinite loops. The reason we
use 0 to 10000 is to account for two additional decimal places in the range 0% to 100%. Your code
should print out a decimal (e.g. 0.0704 for 7.04%).
Try different inputs for your starting salary, and see how the percentage you need to save changes to
reach your desired down payment. Also keep in mind it may not be possible for to save a down
payment in a year and a half for some salaries. In this case your function should notify the user that it
is not possible to save for the down payment in 36 months with a print statement. P​ lease make your
program print results in the format shown in the test cases below.
Note: There are multiple right ways to implement bisection search/number of steps so your
results may not perfectly match those of the test case.
"""

def compute_rate(salary):
    def compute_down_payment(salary, rate):
        r_monthly = 0.04/12
        saved_monthly = (salary/12) * rate

        savings = 0
        for month in range(1, 37):
            if month % 6 == 0:
                salary += (salary * 0.07)
                saved_monthly = (salary/12) * rate
            savings += saved_monthly + (savings * r_monthly)
        return savings

    low, high = 0, 10000
    down_payment = 1000000  * 0.25
    epsilon = 100
    savings, steps = 0, 0
    while abs(down_payment - savings) > epsilon:
        rate = ((low + high)/2) / 10000
        if rate == 1.0: return (None, None)
        savings = compute_down_payment(salary, rate)
        if down_payment > savings:
            low = (low + high)/2
        else:
            high = (low + high)/2
        steps += 1
    return (rate, steps)

starting_salary = int(input("Enter the starting salary: "))
(rate, steps) = compute_rate(starting_salary)

if rate is not None:
    print(f"Best savings rate: {rate}")
    print(f"Steps in bisection search: {steps}")
else:
    print("It is not possible to pay the down payment")


