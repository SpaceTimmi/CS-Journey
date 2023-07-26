# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    else:
        first, rest = sequence[0], sequence[1::]
        permutations = get_permutations(rest)
        result = list()

        for item in permutations:
            for i in range(len(item)+1):
                combination = item[0:i] + first + item[i::]
                result.append(combination)
        return result




if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))



#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)

    example_input_two = '123'
    print('Input:', example_input_two)
    print('Expected Output:', ['123', '132', '213', '231', '312', '321'])
    print('Actual Output:', get_permutations(example_input_two))

    example_input_three = 'ab'
    print('Input:', example_input_three)
    print('Expected Output:', ['ab', 'ba'])
    print('Actual Output:', get_permutations(example_input_three))

    example_input_four = 'xyz'
    print('Input:', example_input_four)
    print('Expected Output:',  ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'])
    print('Actual Output:', get_permutations(example_input_four))



