import json
from botAlgorithm.create_tree import generate_children, win, counter


def print_remaining(states):
    li = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for state in states:
        if state['move'] == '':
            z = counter(state['state'])[0]
            li[z] += 1
    print(li)


def length(states):
    count = 0
    for state in states:
        if state['move'] == '':
            count += 1
    print(count)


def state_list_file_manager(func):
    # pass
    with open('states.txt', 'r') as file:
        state_list_str = file.read()

    state_list = json.loads(state_list_str)

    result = func(state_list)

    if result:
        print_remaining(result)
        # save copy
        with open('statesCopy.txt', 'w') as file:
            file.write(state_list_str)

        # save edited file
        result_str = json.dumps(result)

        with open('states.txt', 'w') as file:
            file.write(result_str)
    else:
        print('no edit')


def generate_rand_dict_row_based(children, randomness):
    index = 0
    d = {}
    for child in children:
        d[child] = randomness[index]
        index += 1
    return d


def absolute_randomness(num) -> list:
    probability = round(1/num, 2)
    randomness = [probability for _ in range(0, num)]
    return randomness


def print_state(s):
    formatted_state = f'''
         _________________
        |  {s[0]}  |  {s[1]}  |  {s[2]}  |
        |_____|_____|_____|
        |  {s[3]}  |  {s[4]}  |  {s[5]}  |
        |_____|_____|_____|
        |  {s[6]}  |  {s[7]}  |  {s[8]}  |
        |_____|_____|_____|   
            '''
    print(formatted_state)


def set_move(states):

    for state in states:

        if state['move'] == '':

            children = generate_children(state['state'])

            # if children:
            if len(children) == 7:

                while True:

                    # -----------------------
                    if len(children) % 2 == 0:
                        print('player: 2')
                    else:
                        print('player: 1')

                    print_state(state['state'])
                    # -----------------------

                    move = input('give move')

                    # if enter skip to next state
                    if move == '':
                        break

                    # set move
                    while True:
                        while move not in children and move != 'r':
                            move = input('invalid move, give again')
                        if move == 'r':
                            break
                        print_state(move)
                        confirm = input('to confirm press enter, else give new move')
                        if confirm == '':
                            break
                        move = confirm
                    state['move'] = move

                    if move == 'r':
                        move_list = []
                        for child in children:
                            print_state(child)
                            add = input('add y/n')
                            if add == 'y':
                                move_list.append(child)

                        if move_list:
                            state['move'] = generate_rand_dict_row_based(move_list, absolute_randomness(len(move_list)))


                        state['signature'] = 'set_move'

                    break



                proceed = input('to continue press enter, else exit')
                if proceed != '':
                    break

    return states


def fill_winning_moves(states):
    for state in states:
        children = generate_children(state['state'])
        for s in children:
            if win(s):
                state['move'] = s
                state['signature'] = 'fill_winning_moves'
                print(state['move'])
                break

    return states


def fill_only_one_child(states):
    for state in states:
        if state['move'] == '':
            children = generate_children(state['state'])
            if len(children) == 1:
                state['move'] = children[0]
                state['signature'] = 'fill_only_one_child'
                print(state['move'])
    return states


def fill_save_game_moves(states):
    for state in states:
        children = generate_children(state['state'])
        count = 0
        for child in children:
            child_children = generate_children(child)
            flag = False
            for s in child_children:
                if win(s):
                    count += 1
                    flag = True
                    break
            if not flag:
                safe = child

        if count == len(children) - 1:
            state['move'] = safe
            state['signature'] = 'fill_save_game_moves'
            print(state['move'])

    return states


def fill_complete_games(states: list):
    for state in states:
        if not generate_children(state['state']):
            state['move'] = 'none'
            state['signature'] = 'fill_complete_games'
            print(state['move'])
    return states


def fill_doomed(states):

    def check_doomed(l: list):
        flag = True
        for wins in l:
            if wins == 0:
                flag = False
                break

        return flag

    def get_win_count(children):
        win_count = []
        for child in children:
            count = 0
            child_children = generate_children(child)
            for s in child_children:
                if win(s):
                    count += 1
            win_count.append(count)

        return win_count

    for state in states:
        if state['move'] == '':
            children = generate_children(state['state'])
            # to be doomed it ant least 5 moves have to be played
            if len(children) < 5:

                win_count = get_win_count(children)

                if check_doomed(win_count):

                    # if more is not targeted
                    if sum(win_count) <= 6:
                        randomness = []
                        for wins in win_count:
                            if wins == 1:
                                randomness.append(0.5)
                            elif wins == 2:
                                randomness.append(0)

                    # if three possible winning moves loss is inevitable
                    else:
                        randomness = absolute_randomness(len(children))

                    state['move'] = generate_rand_dict_row_based(children, randomness)
                    state['signature'] = 'fill_doomed'
                    print(state['move'])

    return states


def fill_2_rand_moves(states):

    for state in states:
        if state['move'] == '':

            children = generate_children(state['state'])

            if len(children) == 2:

                try:
                    # index error may occur here
                    child_child_1 = generate_children(children[0])[0]
                    child_child_2 = generate_children(children[1])[0]

                    if not win(child_child_1) and not win(child_child_2) or win(child_child_1) and win(child_child_2):
                        randomness = [0.5, 0.5]
                        state['move'] = generate_rand_dict_row_based(children, randomness)
                        state['signature'] = 'fill_2_rand_moves'
                        print(state['move'])

                except IndexError:
                    pass

    return states


def fill_3_rand_moves(states):

    def get_win_count(c: list):
        wins = []
        for child in c:
            count = 0
            for s in generate_children(child):
                if win(generate_children(s)[0]):
                    count += 1
            wins.append(count)
        return wins

    for state in states:
        if state['move'] == '':
            children = generate_children(state['state'])
            if len(children) == 3:
                win_count = get_win_count(children)
                if sum(win_count) == 2:
                    randomness = []
                    for w in win_count:
                        if w == 0:
                            randomness.append(0)
                        elif w == 1:
                            randomness.append(0.5)
                    state['move'] = generate_rand_dict_row_based(children, randomness)
                    state['signature'] = 'fill_3_rand_moves'
                    print(state['move'])

                elif sum(win_count) == 0:
                    randomness = absolute_randomness(3)
                    state['move'] = generate_rand_dict_row_based(children, randomness)
                    state['signature'] = 'fill_3_rand_moves'
                    print(state['move'])

    return states


def fill_certain_win_moves(states):

    def check_certain_win(c: str):
        count = 0
        c_children = generate_children(c)
        for s in c_children:
            for s_child in generate_children(s):
                if win(s_child):
                    count += 1
                    break

        return count == len(c_children)

    for state in states:

        if state['move'] == '':
            children = generate_children(state['state'])

            if children:

                certain_wins = []
                for child in children:
                    certain_wins.append(1 if check_certain_win(child) else 0)

                p = sum(certain_wins)

                if p == 0:
                    continue
                elif p == 1:
                    for i in range(0, len(children)):
                        if certain_wins[i] == 1:
                            state['move'] = children[i]
                            state['signature'] = 'fill_certain_win_dooms'
                            print(state['move'])
                            break
                else:
                    randomness = []
                    probability = round(1/p, 2)
                    for w in certain_wins:
                        randomness.append(probability if w == 1 else 0)
                    state['move'] = generate_rand_dict_row_based(children, randomness)
                    state['signature'] = 'fill_certain_win_dooms'
                    print(state['move'])

    return states


def check_if_doomed(s):
    count = 0
    children_s = generate_children(s)
    for c in children_s:
        for d in generate_children(c):
            if win(d):
                count += 1
                break
    return count == len(children_s)


def fill_save_doomed_4_6(states):

    for state in states:

        if state['move'] == '':

            children = generate_children(state['state'])

            if len(children) == 4:

                # omit the doomed moves by marking them with 0
                doom = []
                for child in children:
                    d = 1
                    for s in generate_children(child):
                        if check_if_doomed(s):
                            d = 0
                            break
                    doom.append(d)

                # if there is at least one doom:
                if sum(doom) != len(children):

                    # check if opponent can force a doom
                    for i in range(0, len(children)):
                        if doom[i] == 0:
                            i_children = generate_children(children[i])
                            for child in i_children:
                                count = 0
                                for s in generate_children(child):
                                    flag = False
                                    for c in generate_children(s):
                                        if win(c):
                                            count += 1
                                            flag = True
                                            break
                                    if not flag:
                                        safe = s

                                if count == len(i_children) - 1:
                                    for s in generate_children(safe):
                                        if check_if_doomed(s):
                                            doom[i] = 0

                    # maximize winning chance
                    for i in range(0, len(children)):
                        if doom[i] != 0:
                            i_children = generate_children(children[i])
                            flag = False
                            for child in i_children:
                                for s in generate_children(child):
                                    if win(s):
                                        flag = True
                                        break
                                if flag:
                                    doom[i] = 2
                                    break

                    # if there are 2s format the doom list: replace 1s with 0 and 2s with 1s
                    if 2 in doom:
                        doom = list(map(
                            (lambda x: 0 if x == 0 else 1 if x == 2 else x),
                            doom
                        ))
                    print(doom)
                    # set move
                    p = sum(doom)
                    if p == 1:
                        for i in range(0, len(doom)):
                            if doom[i] == 1:
                                state['move'] = children[i]
                                state['signature'] = 'fill_save_doomed'
                                print(state['move'])
                                break
                    elif p != 0:
                        randomness = []
                        probability = round(1/p, 2)
                        for d in doom:
                            randomness.append(probability if d == 1 else 0)
                        state['move'] = generate_rand_dict_row_based(children, randomness)
                        state['signature'] = 'fill_save_doomed_4_6'
                        print(state['move'])
    return states


def fill_second_move(states):

    for state in states:
        if counter(state['state'])[0] == 8:

            # middle
            if state['state'] == '000010000':
                state['move'] = {
                    '200010000': 0.25,
                    '002010000': 0.25,
                    '000010200': 0.25,
                    '000010002': 0.25
                }

            # corners
            elif state['state'] in ['100000000', '001000000', '000000100', '000000001']:
                move = state['state'][0:4] + '2' + state['state'][5:9]
                state['move'] = move

            # sides
            else:
                if state['state'] == '000001000':
                    state['move'] = {'002001000': 0.33, '000021000': 0.33, '000001002': 0.33}
                elif state['state'] == '010000000':
                    state['move'] = {'210000000': 0.33, '012000000': 0.33, '010020000': 0.33}
                elif state['state'] == '000000010':
                    state['move'] = {'000020010': 0.33, '000000210': 0.33, '000000012': 0.33}
                else:
                    state['move'] = {'200100000': 0.33, '000120000': 0.33, '000100200': 0.33}

            state['signature'] = 'fill_second_move'
            print(state['move'])

    return states


def fill_cause_doom_moves(states):

    def locate_safe(c):
        """
        :param c: child
        :return: safe state or ''
        """
        c_children = generate_children(c)
        count = 0
        for s in c_children:
            flag = False
            for o in generate_children(s):
                if win(o):
                    count += 1
                    flag = True
                    break

            if not flag:
                safe = s

        if count == len(c_children) - 1:
            return safe
        else:
            return ''

    for state in states:

        if state['move'] == '':
            children = generate_children(state['state'])

            winning = []

            for child in children:
                safe = locate_safe(child)

                if safe:
                    flag = False
                    for s in generate_children(safe):
                        if check_if_doomed(s):
                            flag = True
                            break

                    winning.append(1 if flag else 0)

                else:
                    winning.append(0)

            p = sum(winning)
            if p == 1:
                for i in range(0, len(winning)):
                    if winning[i] == 1:
                        state['move'] = children[i]
                        state['signature'] = 'fill_cause_doom_moves'
                        print(state['move'])
                        break
            elif p != 0:
                randomness = []
                probability = round(1 / p, 2)
                for d in winning:
                    randomness.append(probability if d == 1 else 0)
                state['move'] = generate_rand_dict_row_based(children, randomness)
                state['signature'] = 'fill_cause_doom_moves'
                print(state['move'])

    return states


def fill_save_doomed_7(states):

    for state in states:

        if state['move'] == '':

            children = generate_children(state['state'])

            if len(children) == 7:

                # omit the doomed moves by marking them with 0
                doom = []
                for child in children:
                    d = 1
                    for s in generate_children(child):
                        if check_if_doomed(s):
                            d = 0
                            break
                    doom.append(d)

                if sum(doom) != len(children):

                    # check if opponent can force a doom
                    for i in range(0, len(children)):
                        if doom[i] != 0:
                            i_children = generate_children(children[i])
                            for child in i_children:
                                count = 0
                                for s in generate_children(child):
                                    flag = False
                                    for c in generate_children(s):
                                        if win(c):
                                            count += 1
                                            flag = True
                                            break
                                    if not flag:
                                        safe = s

                                if count == len(i_children) - 1:
                                    for s in generate_children(safe):
                                        if check_if_doomed(s):
                                            doom[i] = 0

                    # maximize winning chance
                    for i in range(0, len(children)):
                        if doom[i] != 0:
                            i_children = generate_children(children[i])
                            flag = False
                            for child in i_children:
                                for s in generate_children(child):
                                    if win(s):
                                        flag = True
                                        break
                                if flag:
                                    doom[i] = 2
                                    break

                    # if there are 2s format the doom list: replace 1s with 0 and 2s with 1s
                    if 2 in doom:
                        doom = list(map(
                            (lambda x: 0 if x == 0 else 1 if x == 2 else x),
                            doom
                        ))

                    # set move
                    p = sum(doom)
                    if p == 1:
                        for i in range(0, len(doom)):
                            if doom[i] == 1:
                                state['move'] = children[i]
                                state['signature'] = 'fill_save_doomed'
                                print(state['move'])
                                break
                    elif p != 0:
                        randomness = []
                        probability = round(1/p, 2)
                        for d in doom:
                            randomness.append(probability if d == 1 else 0)
                        state['move'] = generate_rand_dict_row_based(children, randomness)
                        state['signature'] = 'fill_save_doomed_7'
                        print(state['move'])

    return states


def fill_4_5_max_win_in_ties(states):

    for state in states:

        if state['move'] == '':

            children = generate_children(state['state'])
            if len(children) in [4, 5]:

                winning = []


                for child in children:

                    flag = False
                    for s in generate_children(child):

                        for c in generate_children(s):
                            if win(c):
                                flag = True
                                break

                        if flag:
                            winning.append(child)
                            break

                if winning:
                    state['move'] = generate_rand_dict_row_based(winning, absolute_randomness(len(winning)))

    return states


# !!!!!!!!!!! fill_save_doomed_7 and fill_save_doomed_4_6 are the same but target different states



print('--------------------before-----------------------')
state_list_file_manager(print_remaining)
state_list_file_manager(length)
print('--------------------before-----------------------')

# state_list_file_manager(set_move)


state_list_file_manager(fill_complete_games)
state_list_file_manager(fill_only_one_child)
state_list_file_manager(fill_winning_moves)
state_list_file_manager(fill_save_game_moves)
state_list_file_manager(fill_second_move)
state_list_file_manager(fill_doomed)
state_list_file_manager(fill_2_rand_moves)
state_list_file_manager(fill_3_rand_moves)
state_list_file_manager(fill_certain_win_moves)
state_list_file_manager(fill_save_doomed_4_6)
state_list_file_manager(fill_cause_doom_moves)
state_list_file_manager(fill_save_doomed_7)
state_list_file_manager(fill_4_5_max_win_in_ties)
# remaining 24 sevens filled manually with set_move()


print('---------------------after-----------------------')
state_list_file_manager(print_remaining)
state_list_file_manager(length)
print('--------------------after------------------------')


# caution
# there are moves with probability set to zero. take care!
