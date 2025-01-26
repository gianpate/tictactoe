import json


def load_state_file(f):
    # load the state list
    with open(f'state_files/{f}.txt', 'r') as file:
        state_list_str = file.read()

    return json.loads(state_list_str)


def open_f():

    with open('tree.txt', 'r') as file:
        tree_str = file.read()
        tree = json.loads(tree_str)
    return tree


def copy():
    tree = open_f()

    tree_str = json.dumps(tree)
    with open('tree_copy.txt', 'w') as f:
        f.write(tree_str)

    with open('tree_copy.json', 'w') as file:
        json.dump(tree, file, indent=4)


def locate_state(state, states):
    for s in states:
        if state == s['state']:
            # print(s)
            return s


def node_move(s):
    """
    :param s: move of state from the state list
    :return: move in list form
    """
    # print(type(s))
    if type(s) == str:
        return [s]
    elif type(s) == dict:
        rand_moves = []
        for m in s:
            if s[m] != 0:
                rand_moves.append(m)
        return rand_moves


def fill_8(states, tree):
    for node in tree[1]:
        obj = locate_state(node[0], states)
        node[2] = node_move(obj['move'])
    return tree


def fill_7(states, i8, tree):
    for node in tree[1][i8][1]:
        # print(node)
        obj = locate_state(node[0], states)
        node[2] = node_move(obj['move'])
    return tree


def fill_6(states, i8, tree):
    for subtree in tree[1][i8][1]:
        for node in subtree[1]:
            obj = locate_state(node[0], states)
            node[2] = node_move(obj['move'])
    return tree


def fill_5(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for node in subtree6[1]:
                obj = locate_state(node[0], states)
                node[2] = node_move(obj['move'])
    return tree


def fill_4(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for subtree5 in subtree6[1]:
                for node in subtree5[1]:
                    obj = locate_state(node[0], states)
                    node[2] = node_move(obj['move'])
    return tree


def fill_3(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for subtree5 in subtree6[1]:
                for subtree4 in subtree5[1]:
                    for node in subtree4[1]:
                        obj = locate_state(node[0], states)
                        node[2] = node_move(obj['move'])
    return tree


def fill_2(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for subtree5 in subtree6[1]:
                for subtree4 in subtree5[1]:
                    for subtree3 in subtree4[1]:
                        for node in subtree3[1]:
                            obj = locate_state(node[0], states)
                            node[2] = node_move(obj['move'])
    return tree


def fill_1(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for subtree5 in subtree6[1]:
                for subtree4 in subtree5[1]:
                    for subtree3 in subtree4[1]:
                        for subtree2 in subtree3[1]:
                            for node in subtree2[1]:
                                obj = locate_state(node[0], states)
                                node[2] = node_move(obj['move'])
    return tree

def fill_0(states, i8, tree):
    for subtree7 in tree[1][i8][1]:
        for subtree6 in subtree7[1]:
            for subtree5 in subtree6[1]:
                for subtree4 in subtree5[1]:
                    for subtree3 in subtree4[1]:
                        for subtree2 in subtree3[1]:
                            for subtree1 in subtree2[1]:
                                for node in subtree1[1]:
                                    node[2] = "none"
    return tree



def close(tree):
    result_json = json.dumps(tree)
    with open('tree.txt', 'w') as file:
        print('txt')
        file.write(result_json)

    with open('tree.json', 'w') as file:
        print('json')
        # print(tree)
        json.dump(tree, file, indent=4)


# all purpose tests
def check():
    tree = open_f()
    flag = True
    for child in tree[1]:
        for s in child[1]:
            for c in s[1]:
                if not c[2]:
                    flag = False
    print(flag)


def main():
    # chane file code accordingly
    states = load_state_file('4_children')
    tree = open_f()

    # result = fill_8(states, tree)


    # for i in range(0, 9):
    #     tree = fill_7(states, i, tree)


    # for i in range(0, 9):
    #     tree = fill_6(states, i, tree)
    #     print(i, 'complete')


    # for i in range(0, 9):
    #     tree = fill_5(states, i, tree)
    #     print(i, 'complete')


    # for i in range(0, 9):
    #     tree = fill_4(states, i, tree)
    #     print(i, 'complete')

    # for i in range(0, 9):
    #     tree = fill_3(states, i, tree)
    #     print(i, 'complete')


    # for i in range(0, 9):
    #     tree = fill_2(states, i, tree)
    #     print(i, 'complete')


    # for i in range(0, 9):
    #     tree = fill_1(states, i, tree)
    #     print(i, 'complete')

    # for i in range(0, 9):
    #     fill_0(states, i, tree)
    #     print(i, 'complete')

    if tree:
        print('y')
        close(tree)


main()
# check()



# copy()


