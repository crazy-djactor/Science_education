

if __name__ == '__main__':
    for i in sequence("abc", "d", "ef", "ghi"):
        print(i, end="")
    print("\n")

    for i in group_when("combustibles", lambda x: x in "aeiou"):
        print(i, end="")
    print("\n")

    for i in drop_last("combustibles", 5):
        print(i, end="")

    print("\n")
    for i in yield_and_skip("abbabxcabbcaccabb", lambda x: {"a": 1, "b": 2, "c": 3}.get(x, 0)):
        print(i, end="")

    print("\n")
    for i in alternate_all("abcde", "fg", "hijk"):
        print(i, end="")

    print("\n")
    d = ({1:"a", 2:"x", 4:"m", 8:"d"})
    i = min_key_order(d)
    print(next(i))
    print(next(i))
    del d[8]
    print(next(i))
    d[16] = "f"
    d[32] = "z"
    print(next(i))
    print(next(i))