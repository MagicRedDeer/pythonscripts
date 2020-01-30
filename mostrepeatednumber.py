def k():
    print 'determine most repeated number'

    print 'Enter numbers and press q to exit'
    numbers = []
    while True:
        input = raw_input('Enter number:')
        if not input:
            continue
        elif input == 'q':
            break
        numbers.append(int(input))


    number_count = {}
    for num in numbers:
        if number_count.has_key(num):
            number_count[num] = number_count[num] + 1
        else:
            number_count[num] = 1

    max_count = 0
    max_number = None

    for num in numbers:
        count = number_count[num]
        if count > max_count:
            max_count = count
            max_number = num

    print 'the numbers are ', numbers
    print 'the number with maximum occurences %d is %d' % (max_count, max_number)
