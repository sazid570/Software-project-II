number={
    '0':'zero',
    '1':'one',
    '2':'two',
    '3':'three',
    '4':'four'
}

phone = input("please input your phone no: ")
for i in phone:
    print(number.get(i),end=" ")