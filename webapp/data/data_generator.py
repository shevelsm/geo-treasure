import json
from random import randrange

# values for future using in source data
RANK_RANGE = (0, 6)
SOURCE_RANGE = (0, 3)


# simple description for every marker
DESCRIPTION = 'some html description here'


# square area for marker generation in 4 digits, where xxxx = XX.XX0000 degree
X_RANGE = (3850, 4100)
Y_RANGE = (4330, 4550)


# collect arguments from user
while True:
    data_type = input('Enter type of data ("s" - source or "r" - ready): ')
    if data_type not in ('s', 'r'):
        print('Valid input is "r" or "s"!')
        continue
    try:
        number_of_dots = int(input('Enter number of dots to generate: '))
    except ValueError:
        print('Please, enter digits number of dots!')
        continue
    file_name = input('Enter file name for json data file: ')
    if not file_name.isalnum():
        print('Enter valid file name with only text and digit symbols!')
        continue
    break


# generate python data
data = []
for dot in range(number_of_dots):
    current_dot = {}
    current_dot['x'] = randrange(X_RANGE[0] * 10**4, X_RANGE[1] * 10**4) / 10**6
    current_dot['y'] = randrange(Y_RANGE[0] * 10**4, Y_RANGE[1] * 10**4) / 10**6
    current_dot['description'] = DESCRIPTION
    if data_type == 's':
        current_dot['source_id'] = randrange(*SOURCE_RANGE)
        current_dot['rank'] = randrange(*RANK_RANGE)
    data.append(current_dot)


# write python data to json file
json_data = json.dumps(data, indent=4)
with open(file_name + '.json', 'w', encoding='utf-8') as file:
    file.write(json_data)
