numbers = [1,2,2,3,4,5,7,7,5,4,5,5,4]
numbers.sort()
for i in numbers:
    next_number=numbers[numbers.index(i)+1]
    if next_number == i:
        numbers.remove(i)
print(numbers)