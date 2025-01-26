from collections import Counter
import json


def counter(x):
    """
    count values of a state
    returns in a list orders: [num of zeros, num of ones, num of twos]
    """
    count = Counter(x)
    return count.get('0', 0), count.get('1', 0), count.get('2', 0)


def get_0_positions(state):
    """
    get a list of positions of a state where value=0
    """
    positions = []
    for i in range(9):
        if state[i] == '0':
            positions.append(i)
    return positions


def win(state):
    col1 = state[0] == state[3] and state[3] == state[6] and state[6] != '0'
    if col1:
        return True
    col2 = state[1] == state[4] and state[4] == state[7] and state[7] != '0'
    if col2:
        return True
    col3 = state[2] == state[5] and state[5] == state[8] and state[8] != '0'
    if col3:
        return True
    row1 = state[0] == state[1] and state[1] == state[2] and state[2] != '0'
    if row1:
        return True
    row2 = state[3] == state[4] and state[4] == state[5] and state[5] != '0'
    if row2:
        return True
    row3 = state[6] == state[7] and state[7] == state[8] and state[8] != '0'
    if row3:
        return True
    main_diagonal = state[0] == state[4] and state[4] == state[8] and state[8] != '0'
    if main_diagonal:
        return True
    second_diagonal = state[2] == state[4] and state[4] == state[6] and state[6] != '0'
    if second_diagonal:
        return True
    return False


def generate_children(parent):
    """
    produces a list of all children states of the given state (parent-state)
    """
    z, o, t = counter(parent)
    if o == t:
        player = '1'
    elif o == t + 1:
        player = '2'
    else:
        return Exception('Input Error')
    if win(parent):
        return []
    else:
        children = []
        positions = get_0_positions(parent)
        if 0 in positions:
            children.append(player + parent[1:9])
            positions.remove(0)
        if 8 in positions:
            children.append(parent[0:8] + player)
            positions.remove(8)
        for i in positions:
            children.append(parent[0:i] + player + parent[i+1:9])
        return children

#
# print('011020202 -------------',generate_children('121212121'))
# print('-----------------------------------------------------')
# print('011020200 -------------',generate_children('011020200'))
# print('-----------------------------------------------------')
# print('121212100 -------------',generate_children('121212100'))
# print('-----------------------------------------------------')
# print('000000000 --------------',generate_children('000000000'))
#


def create_tree(initial):
    """
    produce a tree of parent-children state relations

    the tree is formatted with nested lists.
    each list has the current state/value on position 0,
    the list of children in position 1 (which is a list of lists),
    and at position 2 the next move

    :param initial: the initial state we want to generate a tree for
    :return: the tree of the given state
    """
    children = generate_children(initial)
    tree = [initial, [], '']
    for child in children:
        tree[1].append(create_tree(child))

    return tree


# ---------- create tree -------------
# tree = create_tree("000000000")
# with open('tree.txt', 'w') as file:
#     string_tree = json.dumps(tree)
#     file.write(string_tree)




def state_list_generate(tree):
    # initialize list

    state_list = []

    def add_state(state):
        nonlocal state_list
        # check if already in list
        for state_dict in state_list:
            if state_dict['state'] == state:
                return None
        # if not add to list
        state_list.append({"state": state, "move": ''})

    def tree_iterator(sub_tree: list):
        for state in sub_tree[1]:
            add_state(state[0])
            tree_iterator(state)

    tree_iterator(tree)

    return state_list

# ----------- create states list --------------
# with open('tree.txt', 'r') as file:
#     tree_str = file.read()
#
# tree = json.loads(tree_str)
# result = state_list_generate(tree)
# result_json = json.dumps(result)
#
# with open('states.txt', 'w') as file:
#     file.write(result_json)


# ---------- copy tree to json file -----------------
# with open('tree.txt', 'r') as file:
#     tree_str = file.read()
#     tree_states = json.loads(tree_str)
#
# with open('tree.json', 'w') as file:
#     json.dump(tree_states, file, indent=4)















