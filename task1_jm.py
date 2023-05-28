"""Program prints an integer or a string in the range <n; m>
 according to the given conditions."""

def num_text_printing(n, m):
    """Printing an integer or a string according to the task conditions."""

    # Conditions check.
    if n < 1 or n > 10000 or n >= m or m > 10000:
        print("Numbers do not meet the conditions.")
    else:
        print("Input values:" + "\n" + str(n) + "\n" + str(m))

        # Program prints number from n to m (inclusive) but
        # for multiples of three, print Fizz (instead of the number)
        # for multiples of five, print Buzz (instead of the number)
        # for multiples of both three and five, print FizzBuzz (instead of the number).

        numbers = [i for i in range(n, m + 1)]
        print(numbers)

        print("Output values: ")
        for number in numbers:
            if number % 3 == 0 and number % 5 == 0:
                print("FizzBuzz")
            elif number % 3 == 0:
                print("Fizz")
            elif number % 5 == 0:
                print("Buzz")
            else:
                print(number)

# User provides two numbers.
n = input("Provide number n from range 1 <= n <= 10000: ")
m = input("Provide number m from range n < m <= 10000: ")

# Provided values are numbers - check.
if not (n.isnumeric() and m.isnumeric()):
    print("Input values are not numbers. Please provide numbers.")
else:
    n, m = int(n), int(m)
    printing = num_text_printing(n, m)