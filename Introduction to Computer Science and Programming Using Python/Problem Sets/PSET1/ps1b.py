# PSET 1 - Part B

"""
Part B: Saving, with a raise
Background
In Part A, we unrealistically assumed that your salary didn’t change. But you are an MIT graduate, and
clearly you are going to be worth more to your company over time! So we are going to build on your
solution to Part A by factoring in a raise every six months.
In ​ps1b.py​, copy your solution to Part A (as we are going to reuse much of that machinery). Modify
your program to include the following
1.
Have the user input a semi-annual salary raise ​semi_annual_raise​ (as a decimal percentage)
2.
After the 6​th​ month, increase your salary by that percentage. Do the same after the 12
th​th month, the 18​​ month, and so on.
Write a program to calculate how many months it will take you save up enough money for a down
payment. LIke before, assume that your investments earn a return of ​r​ = 0.04 (or 4%) and the
required down payment percentage is 0.25 (or 25%). Have the user enter the following variables:
1. The starting annual salary (annual_salary)
2. The percentage of salary to be saved (portion_saved)
3. The cost of your dream home (total_cost)
4. The semi­annual salary raise (semi_annual_raise)
"""

def compute_down_payment(annual_salary, portion_down_payment, total_cost, semi_annual_raise):
    """
    Computes how many months it will take to save up for a down-payment of a house based on pset1.
    """
    months, current_savings = 0, 0
    monthly_savings = (annual_salary / 12) * portion_down_payment
    monthly_returns = 0.04 / 12
    down_payment = total_cost * 0.25

    while down_payment > current_savings:
        print(current_savings, annual_salary)
        months += 1
        if (months % 6 == 0):
            annual_salary += annual_salary * semi_annual_raise
            monthly_savings = (annual_salary / 12) * portion_down_payment
        additional = current_savings + (current_savings * monthly_returns)
        current_savings = monthly_savings + additional
    return months


annual_salary = int(input("Enter your annual salary: "))
portion_down_payment = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = int(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

months = compute_down_payment(annual_salary, portion_down_payment, total_cost, semi_annual_raise)


print(f"Number of months: {months}")


