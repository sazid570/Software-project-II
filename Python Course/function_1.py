def tumi_ke(name_of_user):
    print(name_of_user+': amar nai kono nam nai')
    print('ghor bari nai')


def total_cost(price,shipping,discount):
    cost = (price+shipping)*(1-discount)
    return cost


print('imabouttocallmyfunction:')
name = 'hehe'
print(total_cost(price=50,shipping=5,discount=0.5))

tumi_ke(name)