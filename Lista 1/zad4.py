
input = input()
ciag,dlugoscbloku = input.split()

#ciag = list(ciag)


def opt_dist(lst, D):
    lst=list(lst)
    n = len(lst)
    min_changes = float('inf')
    
    for start in range(n - D + 1):
        changes = sum(1 for i in range(n) if (start <= i < start + D) != (lst[i] == '1'))
        min_changes = min(min_changes, changes)
    
    if D == 0:
        return lst.count(1)
    
    return min_changes

print(opt_dist(ciag, int(dlugoscbloku)))

'''
print(opt_dist("0010001000", 5))
print(opt_dist("0010001000", 4))
print(opt_dist("0010001000", 3))
print(opt_dist("0010001000", 2))
print(opt_dist("0010001000", 1))
print(opt_dist("0010001000", 0))
print(opt_dist("0000000001", 1))
print(opt_dist("0000000010", 1))
print(opt_dist("1000000000", 1))
print(opt_dist("0100000000", 1))


print(opt_dist("0010101000", 5))
print(opt_dist("0010101000", 4))
print(opt_dist("0010101000", 3))
print(opt_dist("0010101000", 2))
print(opt_dist("0010101000", 1))
print(opt_dist("0010101000", 0))
'''