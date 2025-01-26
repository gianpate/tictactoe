import json
from botAlgorithm.create_tree import counter


# load the state list
with open('states.txt', 'r') as file:
    state_list_str = file.read()

state_list = json.loads(state_list_str)


c8, c7, c6, c5, c4, c3, c2, c1 = [], [], [], [], [], [], [], []


for state in state_list:
    z, o, t = counter(state['state'])
    if z == 1:
        c1.append(state)
    elif z == 2:
        c2.append(state)
    elif z == 3:
        c3.append(state)
    elif z == 4:
        c4.append(state)
    elif z == 5:
        c5.append(state)
    elif z == 6:
        c6.append(state)
    elif z == 7:
        c7.append(state)
    elif z == 8:
        c8.append(state)


l = [c1, c2, c3, c4, c5, c6, c7, c8]


def fill_file(l):
    for i in range(0, 8):
        file = f'state_files/{i+1}_children.txt'
        content = json.dumps(l[i])
        with open(file, 'w') as f:
            f.write(content)


# fill_file(l)