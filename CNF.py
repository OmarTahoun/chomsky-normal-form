from string import letters
import copy
import re

# *******HEADER*******
# This File contains the functions that construct the chomsky normal form

# CNF is divided intwo 3 main steps which are:

# 1) Removing the long rules (e.g. A->BCD will become  A -> ED where E -> BC)

# 2) Removing the Epsilon Rules (e.g. A -> aaA | e Will become A -> aaA, A -> aa)

# 3) Removing the short/useless rules (e.g. A -> B, B -> C will become A -> C)



# 1) Removing the long rules (e.g. A->BCD will become  A -> ED where E -> BC)
def remove_large(rules,let,voc):
    """
        A -> BCD gives
          1) A-> BE (if E is the first "free" letter from letters pool) and
          2) E-> CD
    """

    new_dict = copy.deepcopy(rules)         # Make a hard copy of the dictionary (as its size is changing over the process)
    for key in new_dict:                 # For all the keys (non-terminal charachters)
        values = new_dict[key]
        for i in range(len(values)):    # Check the production rule of this key
            if len(values[i]) > 2:      # Check if we have a rule violation (the length is more than 2)
                for j in range(len(values[i]) - 2):
                    # replace first rule
                    if j==0:
                        rules[key][i] = rules[key][i][0] + let[0]

                    # add new rules
                    else:
                        rules.setdefault(new_key, []).append(values[i][j] + let[0])
                    voc.append(let[0])
                    # save letter, as it'll be used in next rule
                    new_key = copy.deepcopy(let[0])
                    # remove letter from free letters list
                    let.remove(let[0])
                # last 2 letters remain always the same
                rules.setdefault(new_key, []).append(values[i][-2:])

    return rules,let,voc


# 2) Removing the Epsilon Rules (e.g. A -> aaA | e Will become A -> aaA, A -> aa)
def remove_epsilon(rules,voc):
    e_list = []                         # list with keys of empty rules
    new_dict = copy.deepcopy(rules)     # find  non-terminal rules and add them in list

    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if values[i] == 'e' and key not in e_list:  # if key gives an empty state and is not in list, add it
                e_list.append(key)
                rules[key].remove(values[i])    # remove empty state

        if len(rules[key]) == 0:    # if key doesn't contain any values, remove it from dictionary
            if key not in rules:
                voc.remove(key)
            rules.pop(key, None)


    # delete empty rules
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):

            # check for rules in the form A->BC or A->CB, where B is in e_list
            # and C in vocabulary
            if len(values[i]) == 2:
                # check for rule in the form A->BC, excluding the case that
                # gives A->A as a result)
                if values[i][0] in e_list and key!=values[i][1]:
                    rules.setdefault(key, []).append(values[i][1])

                # check for rule in the form A->CB, excluding the case that
                # gives A->A as a result)
                if values[i][1] in e_list and key!=values[i][0]:
                    if values[i][0]!=values[i][1]:
                        rules.setdefault(key, []).append(values[i][0])

    return rules,voc

# 3) Removing the short/useless rules (e.g. A -> B, B -> C will become A -> C)
def remove_short(rules,voc):

    # create a dictionary in the form letter:letter (at the beginning D(A) = {A})
    D = dict(zip(voc, voc))

    # just transform value from string to list, to be able to insert more values
    for key in D:
        D[key] = list(D[key])

    # for every letter A of the vocabulary, if B->C, B in D(A) and C not in D(A)
    # add C in D(A)
    for letter in voc:
        for key in rules:
            if key in D[letter]:
                values = rules[key]
                for i in range(len(values)):
                    if len(values[i]) == 1 and values[i] not in D[letter]:
                        D.setdefault(letter, []).append(values[i])

    rules,D = remove_shorter(rules,D)
    return rules,D


# Helper function for the remove_short function
def remove_shorter(rules,D):
    # remove short rules (with length in right side = 1)
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) == 1:
                rules[key].remove(values[i])
        if len(rules[key]) == 0: rules.pop(key, None)

    # replace each rule A->BC with A->B'C', where B' in D(B) and C' in D(C)
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            # search all possible B' in D(B)
            for j in D[values[i][0]]:
                # search all possible C' in D(C)
                for k in D[values[i][1]]:
                    # concatenate B' and C' and insert a new rule
                    if j+k not in values:
                        rules.setdefault(key, []).append(j + k)

    return rules,D


# Insert rules S->BC for every A->BC where A in D(S)-{S}
# Finalize the vocabulary
def final_rules(rules,D,S):
    for let in D[S]:
        # check if a key has no values
        if not rules[S] and not rules[let]:
            for v in rules[let]:
                if v not in rules[S]:
                    rules.setdefault(S, []).append(v)
    return rules

# Print rules
def print_rules(rules):
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            print key + '->' + values[i]
    return 1
