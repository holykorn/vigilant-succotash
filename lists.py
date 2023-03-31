# 3.2
list_1 = ['Hi', 'ananas', 2, None, 75, 'pizza', 36, 100]
int_list = filter(lambda x: type(x) is int, list_1)
print(sum(int_list))