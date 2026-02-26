#We want to write a program that prompts the user to enter a number
#It should find the products of the factors of the number
#It does it by making a function prodf(n) and the number should be declared as x
#return prod

def prodf(n):
    prod = 1
    for i in range(1, n + 1):
        if n % i == 0:
            prod *= i
    return prod
while True:
    try:
        x = int(input("Enter a number: "))
        result = prodf(x)
        print(f"The product of the factors of {x} is: {result}")
        break
    except ValueError:
        print("Please enter a valid integer.")
