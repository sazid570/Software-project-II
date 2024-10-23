weight=float(input("Input your weight:"))
unit = input("(l)bs or (k)gs:")
unit = unit.lower()

if unit == 'l':
    converted = weight * 0.45
    print("You are " +str(converted)+ " kilos")
elif unit == 'k':
    converted = weight / 0.45
    print("You are " +str(converted)+ " pounds")
else:
    print("Invalid input")


