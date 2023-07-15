# Loops and Iteration

"""
5.2 Write a program that repeatedly prompts a user for integer numbers until the user enters 'done'. Once 'done' is entered, print out the largest and smallest of the numbers. If the user enters anything other than a valid number catch it with a try/except and put out an appropriate message and ignore the number. Enter 7, 2, bob, 10, and 4 and match the output below.
"""
largest = None
smallest = None
firstLoop = True

while True:
    num = input("Enter a number: ")
    if num == "done":
        break
    try:
        int(num)
    except:
        print("Invalid input")
    else:
        num = int(num)
        if (firstLoop is True):
            largest = num
            smallest = num
            firstLoop = False
        else:
            if (num > largest):
                largest = num
            if (num < smallest):
                smallest = num

print("Maximum is", largest)
print("Minimum is", smallest)

