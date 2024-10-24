number=[1,2,3,5,6,7,9]

max = number[1]

for i in number:
    if max<i:
        max=i

print(f"the maximum number is:{max}")