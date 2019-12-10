import json
from random import randrange

# values for future using in source data
RANK_RANGE = (0, 6)
SOURCE_RANGE = (0, 3)

# simple description for every marker
DESCRIPTION = 'some html description here'

# square area for marker generation in 4 digits, where xxxx = XX.XX0000 degree
X_RANGE = (3900, 4100)
Y_RANGE = (4400, 4500)


# collect arguments from user
while True:
    data_type = input('Enter type of data ("s" - source or "r" - ready): ')
    if data_type not in ('s', 'r'):
        print('Valid input is "r" or "s"!')
        continue
    try:
        number_of_dots = int(input('Enter number of dots to generate: '))
    except TypeError:
        print('Please, enter digits number of dots!')
        continue
    file_name = input('Enter file name for json data file: ')
    if not file_name.isalpha():
        print('Enter valid file name with only text symbols!')
        continue
    break


# generate json data file
data = []
for dot in range(number_of_dots):
    current_dot = {}
    current_dot['x'] = randrange(*X_RANGE)
    current_dot['y'] = randrange(*Y_RANGE)
    print(current_dot)



# with open(file_name + '.json', 'w', encoding='utf-8') as file:
