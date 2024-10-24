user_input = " "


while user_input != "quit":
    user_input =input(">")

    if user_input == "help":
        print(">Type start to \'start\' the car \n>Type \'stop\' to stop the car\n>Type \'quit\' to quit the game")
    if user_input == 'start':
        print("Car has started...")
    
    if user_input == 'stop':
        print('car has stopped.')
    
    else:
        print("Unrecognized input, type help for details")
