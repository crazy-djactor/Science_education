# p is a predicate: it returns True/False when called on one argument

def separate(p: callable, l: [object]) -> ([object], [object]):
    if len(l) <= 0:
        return [], []
    a, *b = l
    t, f = separate(p, b)
    if p(a):
        return [a] + t, f
    return t, [a] + f


def is_sorted(l: [object]) -> bool:
    if len(l) == 0 or len(l) == 1:
        return True
    if l[0] <= l[1]:
        return is_sorted(l[1:])
    return False


def sort(l: [object]) -> [object]:
    if not l:
        return []
    a, *b = l
    lower, greater = separate((lambda x: x <= a), b)
    new_sorted = sort(lower) + [a] + sort(greater)
    return new_sorted


def merge_chars(a: str, b: str) -> str:
    if not a and not b:
        return ''

    if a and (not b or a[0] <= b[0]):
        return a[0] + merge_chars(a[1:], b)
    else:
        return b[0] + merge_chars(a, b[1:])


def nested_count(l: 'any nested list of int', a: int) -> int:
    if not l:
        return 0
    if l[0] == a:
        return 1 + nested_count(l[1:], a)
    if type(l[0]) == type(a):
        return nested_count(l[1:], a)
    elif type(l[0]) == list:
        return nested_count(l[0], a) + nested_count(l[1:], a)
    return 0


if __name__ == "__main__":
    from courselib import driver, predicate
    import random
    from courselib.goody import irange

    z, d = separate((lambda x: x >= 0), [1, -3])

    print(separate((lambda x: x >= 0), [1, -3, -2, 4, 0, -1, 8]))

    print('Testing separate')
    print(separate(predicate.is_positive,[]))
    print(separate(predicate.is_positive,[1, -3, -2, 4, 0, -1, 8]))
    print(separate(predicate.is_prime,[i for i in irange(2,20)]))
    print(separate(lambda x : len(x) <= 3,'to be or not to be that is the question'.split(' ')))
    print(separate(lambda x : x <= 'm','to be or not to be that is the question'.split(' ')))

    print('\nTesting is_sorted')
    print(is_sorted([]))
    print(is_sorted([0]))
    print(is_sorted([-5,-4]))
    print(is_sorted([1, 2, 3, 4, 5, 6, 7]))
    print(is_sorted([1, 2, 3, 7, 4, 5, 6]))
    print(is_sorted([1, 2, 3, 4, 5, 6, 5]))
    print(is_sorted([7, 6, 5, 4, 3, 2, 1]))
#
    print('\nTesting sort')
    print(sort([4, 5, 3, 1]))
    print(sort([1,2,3,4,5,6,7]))
    print(sort([7,6,5,4,3,2,1]))
    print(sort([4,5,3,1,2,7,6]))
    print(sort([1,7,2,6,3,5,4]))
    l = [i+1 for i in range(30)]
    random.shuffle(l)
    print(l)
    print(sort(l))

    print('\nTesting merge_chars')
    print(merge_chars('',''))
    print(merge_chars('','abc'))
    print(merge_chars('abc',''))
    print(merge_chars('ace','bdf'))
    print(merge_chars('abc','xyz'))
    print(merge_chars('abxy','lmzzz'))
    print(merge_chars('acdeghilmnosu','bfjkpqrtvwxyz'))
    print(merge_chars('bcgprvyz','adefhijklmnoqstuwx'))
    print(merge_chars('cdefghijklmnpqrstuvw','aboxyz'))

    print('\nTesting nested_count')
    print(nested_count([1,2,4,1,8,1,3,2,1,1],1))
    print(nested_count([[1,2,4,1,8],[1,3,2],1,1],1))
    print(nested_count([[1,2,[4,[1],8],[1,3,2]],[1,1]],1))

    driver.default_file_name = "bscq5F20.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
