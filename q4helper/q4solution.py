# Generators must be able to iterate through any kind of iterable.
# hide is present and called to ensure that your generator code works on
#   general iterable parameters (not just a string, list, etc.)
# For example, although we can call len(string) we cannot call
#   len(hide(string)), so the generator functions you write should not
#   call len on their parameters
# Leave hide in this file and add code for the other generators.

def hide(iterable):
    for v in iterable:
        yield v


# The combination of return and yield None make each of the following
#   a generator (yield None) that immediately raises the StopIteration
#   exception (return)

def sequence(*args):
    for arg in args:
        for value in arg:
            yield value


def group_when(arg_iterable, predicate):
    iter_list = []
    for value in arg_iterable:
        iter_list.append(value)
        if predicate(value):
            yield iter_list
            iter_list = []
    if len(iter_list) > 0:
        yield iter_list


def drop_last(arg_iterable, n):
    _start = iter(arg_iterable)
    iter_list = []
    try:
        for i in range(n):
            value2 = next(_start)
            iter_list.append(value2)
    except StopIteration:
        return []
    while True:
        try:
            value2 = next(_start)
            yield iter_list[0]
            iter_list = iter_list[1:]
            iter_list.append(value2)
        except StopIteration:
            break


def alternate_all(*args):
    iter_list = []
    n_count = 0
    for arg in args:
        iter_list.append(iter(arg))
        n_count = n_count + 1
    while n_count > 0:
        for i, arg in enumerate(args):
            _iter = iter_list[i]
            try:
                value = next(_iter)
                yield value
            except StopIteration:
                n_count = n_count - 1
    pass


def yield_and_skip(arg_iterable, predicate):
    _start = iter(arg_iterable)
    while True:
        try:
            value = next(_start)
            yield value
            _skip_ = predicate(value)
            for i in range(_skip_):
                value = next(_start)
        except StopIteration:
            break
    pass


def min_key_order(adict):
    # if len(adict) == 0:
    #     raise StopIteration

    key = -1
    while True:
        old_key = key
        v = None
        try:
            sorted_array = sorted(adict.items())
            for (k,v) in sorted_array:
                if k > key or key == -1:
                    key = k
                    break
            if old_key == key:
                break
            yield key, v
        except Exception:
            break
    raise StopIteration
         
if __name__ == '__main__':
    from goody import irange
    
    # Test sequence; you can add any of your own test cases
    print('Testing sequence')
    for i in sequence('abc', 'd', 'ef', 'ghi'):
        print(i,end='')
    print('\n')

    print('Testing sequence on hidden')
    for i in sequence(hide('abc'), hide('d'), hide('ef'), hide('ghi')):
        print(i,end='')
    print('\n')


    # Test group_when; you can add any of your own test cases
    print('Testing group_when')
    for i in group_when('combustibles', lambda x : x in 'aeiou'):
        print(i,end='')
    print('\n')

    print('Testing group_when on hidden')
    for i in group_when(hide('combustibles'), lambda x : x in 'aeiou'):
        print(i,end='')
    print('\n')


    # Test drop_last; you can add any of your own test cases
    print('Testing drop_last')
    for i in drop_last('combustible', 5):
        print(i,end='')
    print('\n')

    print('Testing drop_last on hidden')
    for i in drop_last(hide('combustible'), 5):
        print(i,end='')
    print('\n')


    # Test sequence; you can add any of your own test cases
    print('Testing yield_and_skip')
    for i in yield_and_skip('abbabxcabbcaccabb',lambda x : {'a':1,'b':2,'c':3}.get(x,0)):
        print(i,end='')
    print('\n')

    print('Testing yield_and_skip on hidden')
    for i in yield_and_skip(hide('abbabxcabbcaccabb'),lambda x : {'a':1,'b':2,'c':3}.get(x,0)):
        print(i,end='')
    print('\n')


    # Test alternate_all; you can add any of your own test cases
    print('Testing alternate_all')
    for i in alternate_all('abcde','fg','hijk'):
        print(i,end='')
    print('\n')
    
    print('Testing alternate_all on hidden')
    for i in alternate_all(hide('abcde'), hide('fg'),hide('hijk')):
        print(i,end='')
    print('\n\n')
       
         
    # Test min_key_order; add your own test cases
    print('\nTesting Ordered')
    d = {1:'a', 2:'x', 4:'m', 8:'d', 16:'f'}
    i = min_key_order(d)
    print(next(i))
    print(next(i))
    del d[8]
    print(next(i))
    d[32] = 'z'
    print(next(i))
    print(next(i))

    from courselib import driver
    driver.default_file_name = "bscq4F20.txt"
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()

