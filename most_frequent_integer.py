def most_frequent_integer(array):
    most_frequent = max_frequency = -1
    frequencies = {}

    for num in array:                   # n
        num = int(num)
        freq = frequencies.get(num, 0)  # 1
        freq += 1
        frequencies[num] = freq
        if freq > max_frequency:
            most_frequent, max_frequency = num, freq

    if max_frequency == -1:
        raise ValueError("no values found in input array")

    return most_frequent


def pairs_to_number_n2(array, num): 
    for idx, num1 in enumerate(array):
        for num2 in (array[:idx] + array[idx+1:]):
            if num == num1 + num2:
                return num1, num2


def pairs_to_number(array, num):
    for number in array:
        assert isinstance(number, int)
    array.sort()
    index1, index2 = 0, len(array)-1
    while index1 < index2:
        num1 = int(array[index1])
        num2 = int(array[index2])
        added = num1 + num2
        if added == num:
            return array[index1], array[index2]
        elif added > num:
            index2 -= 1
        else:
            index1 += 1


def return_non_pair(array):
    non_pair = set()
    for num in array:
        if num in non_pair:
            non_pair.remove(num)
        else:
            non_pair.add(num)
    return non_pair


def part1():
    print("Most frequent integer:")

    inputs = [[1, 2, 3, 3],
              [1, 2, 3],
              [3, 1, 4, 57, 4]]
    for inp in inputs:
        print(inp, most_frequent_integer(inp))


def part2():
    print("Pairs that add up to a given integer:")
    inputs = [
            ([1, 2, 9, 12], 10),
            ([1, 9, 1, 9], 10),
            ([1, 9, 1], 10),
            ([1, 5, 2], 10)]
    for inp in inputs:
        print(inp, pairs_to_number(*inp))


def part3():
    print("Get non pairs")
    inputs = [
            [1, 1, 9, 5, 9],
            [4, 5, 5, 6, 4, 9, 1],
            [22, 22, 44, 55, 44, 99]]
    for inp in inputs:
        print(inp, return_non_pair(inp))


def main():
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
