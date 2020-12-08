from predicate import is_even
from ile3helper import ints, primes, is_prime, hide, nth, nth_for_m
from collections import defaultdict


def zip_skip(predicate: callable, exception_bool, *iterables):
    args = []
    for _iterates_ in iterables:
        iter_tuple = [iter_ for iter_ in _iterates_]
        args.append(iter_tuple)

    iter_zip = zip(*args)
    for iterate in iter_zip:
        try:
            skip = False
            for x in iterate:
                if not predicate(x):
                    skip = True
                    break
            if not skip:
                yield iterate
        except Exception as e:
            if exception_bool:
                yield iterate

closet_sum_min = [[], []]

def closest_sums(ns: [int], l1: [int], l2: [int]) -> [[int], [int]]:
    l1_temp = l1.copy()
    ns_current = [i for i in ns if not i in l1_temp or l1_temp.remove(i)]
    for _ns in ns_current:
        # Calc new value
        l1_temp = l1.copy()
        l1_temp.append(_ns)
        l_temp = l1_temp.copy()
        l2_temp = [i for i in ns if not i in l_temp or l_temp.remove(i)]
        # l2_temp = ns[index + 1:]
        if sum(l1_temp) > sum(l2_temp):
            continue

        diff = sum(l2_temp) - sum(l1_temp)

        # Calc current min_value
        lmin_temp = l2.copy()
        l_temp = lmin_temp.copy()
        lmin2_temp = [i for i in ns if not i in l_temp or l_temp.remove(i)]
        diff_current = sum(lmin2_temp) - sum(lmin_temp)
        if diff < diff_current:
            l2 = l1_temp.copy()
        # ns_next = l2_temp.copy()
        l2, _ = closest_sums(ns, l1_temp, l2)

    l_temp = l2.copy()
    l_1 = [i for i in ns if not i in l_temp or l_temp.remove(i)]
    return [l2, l_1]


# class shared_dict(dict):
#     # Write __init_, __setitem, and __delitem__ below, after str/verify_shared
#
#     # Useful for debugging: see the state of all the dictionaries
#     def __str__(self):
#         return f'  # _counts     = {dict.__repr__(self._counts)}\n  # _stored_kvs = {dict.__str__(self._stored_kvs)}\n  # shared_dict = {dict.__str__(self)}'
#
#     def verify_shared(self, trace_all=False):
#         wrong = 0
#         vd = defaultdict(list)
#
#         def check(name_checking, d_checking):
#             nonlocal wrong
#             if trace_all: print(f'\nChecking {name_checking} for shared objects')
#             for k, v in d_checking.items():
#                 if trace_all: print('  ......')
#                 if trace_all: print(f'  key   {k} = {object.__repr__(k)}')
#                 vd.setdefault(k, k)
#                 if vd[k] is not k:
#                     wrong += 1
#                     print(f'  ERROR: in {name_checking} key   {k} does not refer to the correct object')
#
#                 if trace_all: print(f'  value {v} = {object.__repr__(v)}')
#                 vd.setdefault(v, v)
#                 if vd[v] is not v:
#                     wrong += 1
#                     print(f'  ERROR: in {name_checking} value {v} does not refer to the correct object')
#
#         check('_counts', self._counts)
#         check('_counts', self._stored_kvs)
#         check('shared_dict', self)
#         return wrong
#
#     def __init__(self):
#         pass
#
#     def __setitem__(self, key, value):
#         pass
#
#     def __delitem__(self, key):
#         pass


if __name__ == '__main__':
    print('\n\nTesting zip_skip')
    lst = list(zip_skip((lambda x: is_even(x)), False, hide([0, 0, 1, 1, 0]), hide([0, 1, 0, 1, 'X'])))

    print("for i in zip_skip( (lambda x : x%2 == 0), False )\n  ... should produce nothing")
    for i in zip_skip((lambda x: is_even(x)), False):
        print(' ', i)

    print(
        "\nzip_skip( (lambda x : is_even(x)), False, hide([0, 0, 1, 1, 0]), hide([0, 1, 0, 1, 'X']))\n  ... should produce (0, 0)")
    for i in zip_skip((lambda x: is_even(x)), False, hide([0, 0, 1, 1, 0]), hide([0, 1, 0, 1, 'X'])):
        print(' ', i)

    print(
        "\nzip_skip( (lambda x : is_even(x)), True, hide([0, 0, 1, 1, 0]), hide([0, 1, 0, 1, 'X']))\n   ... should produce (0, 1) and (0, 'X')")
    for i in zip_skip((lambda x: is_even(x)), True, hide([0, 0, 1, 1, 0]), hide([0, 1, 0, 1, 'X'])):
        print(' ', i)
    #
    # print("\nnth_for_m(primes(),10,3))\n...should produce\n[29, 31, 37]")
    # print(nth_for_m(primes(), 10, 3))
    #
    # print(
    #     "\nnth_for_m(zip_skip( (lambda x : x%10 == 7), True, ints(), primes()),50,10)\n...should produce\n[(1777, 15227), (1797, 15377), (1807, 15467), (1877, 16127), (1927, 16657), (1967, 17047), (1977, 17167), (1997, 17377), (2027, 17627), (2037, 17747)]")
    # print(nth_for_m(zip_skip((lambda x: x % 10 == 7), True, ints(), primes()), 50, 10))
    #
    # print('\n\nTesting closest_sums. Feel free to test other cases: e.g, base cases you choose')

    # print('  closest_sums([],[],[])      = ', closest_sums([], [], []),
    #       '     ...should be [[],[]]     with allowed permutations')
    # print('  closest_sums([8],[],[])     = ', closest_sums([8], [], []),
    #       '    ...should be [[8],[]]    with allowed permutations')
    # print('  closest_sums([5,8],[],[])   = ', closest_sums([5, 8], [], []),
    #       '   ...should be [[5],[8]]   with allowed permutations')
    print('  closest_sums([2,5,8],[],[]) = ', closest_sums([2, 5, 8], [], []),
          '...should be [[2,5],[8]] with allowed permutations')
    print('  closest_sums([1,10,8,11,1,9,10],[],[]) = ', closest_sums([1, 10, 8, 11, 1, 9, 10], [], []),
          '...should be [[1, 10, 11, 1],[8,9,10]] with allowed permutations')
    #
    # print('\n\nTesting shared_dict. Feel free to test other cases')
    # print('__setitem__ test: see specifications')
    # sd = shared_dict()
    #
    # print('sd = shared_dict()\n', sd, sep='')
    # sd['a'] = tuple([1, 2, 3])
    # print("\nsd['a'] = tuple([1,2,3])\n", sd, sep='')
    #
    # sd['b'] = tuple([1, 2, 3])
    # print("\nsd['b'] = tuple([1,2,3])\n", sd, sep='')
    #
    # print("\nprint(sd['a'] is sd['b'])\n", "  ", sd['a'] is sd['b'], sep='')
    #
    # sd['c'] = 'c'
    # print("\nsd['c'] = 'c'\n", sd, sep='')
    #
    # sd[tuple([1, 2, 3])] = 'd'
    # print("\nsd[tuple([1,2,3])] = 'd'\n", sd, sep='')
    #
    # print('\nverifying all equal (==) objects are shared; set trace_all = True for more details')
    # if (wrong = sd.verify_shared(trace_all=False)) != 0:
    #     print(f'---found {wrong} objects not shared correctly')
    # else:
    #     print('---All are correctly shared')
    #
    # print('\n\n__delitem__ test: see specifications')
    # del sd['a']
    # print("\ndel sd['a']\n", sd, sep='')
    # del sd['b']
    # print("\ndel sd['b']\n", sd, sep='')
    # del sd['c']
    # print("\ndel sd['c']\n", sd, sep='')
    # del sd[tuple([1, 2, 3])]
    # print("\ndel sd[tuple([1,2,3])]\n", sd, sep='')
    #
    # print('\n\n__setitem__ EXTRA CREDIT test: see specifications')
    # sd = shared_dict()
    # print('sd = shared_dict()\n', sd, sep='')
    # sd['a'] = tuple([1, 2, 3])
    # print("\nsd['a'] = tuple([1,2,3])\n", sd, sep='')
    # sd['a'] = frozenset([1, 2])
    # print("\nsd['a'] = frozenset([1,2])\n", sd, sep='')
    #
    # print()
    import driver
    #
    # # Uncomment the following lines to see MORE details on exceptions
    driver.default_file_name = 'bscile3F20.txt'
    # But better to debug putting testing code above
    #     driver.default_show_exception=True
    #     driver.default_show_exception_message=True
    driver.driver()
