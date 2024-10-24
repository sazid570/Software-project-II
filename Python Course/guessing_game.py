secret_number = 7
guess_count = 0
guess_limit = 3

flag = 0

while guess_count < guess_limit:
    guess=input("Guess: ")
    guess_count+=1

    if guess == secret_number:
        print("You won!")
        flag =1
        break
    else:
        print("Try again!")

if flag != 1:
    
   print("better luck next time")


