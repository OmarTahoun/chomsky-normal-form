from CNF import *



def main():
    """
    This is the driver function:
    It starts by asking the user to enter the number of rules.
    next The user enters the Initial State character
    Then the user enter the rules one after another

    The Rules are entered in this format:
        A -> B is Entered as  A B (space seperated)

        A -> B | C is Entered as 2 sperate rules like this:
            A B
            A C

        A -> aaA | null is Entered as 2 sperate rules like this:
            A aaA
            A e
        (e is used for the epsilon/null operation)
    """


    rules = {} # We start by creating an empty dictionary for the rules
    voc = []

    # This list's going to be our "letters pool" for naming new states
    let = list(letters[26:]) + list(letters[:25])
    let.remove('e')

    # Taking user input for number of rules
    while True:
        userInput = raw_input('Give number of rules: ')

        # check if N is integer >=2
        try:
            N = int(userInput)
            if N <=2: print 'N must be a number >=2!'
            else: break
        except ValueError:
            print "Must be an Integer"

    # Taking user input for the initial state
    while True:
        S = raw_input('Give initial state: ')
        if not re.match("[a-zA-Z]*$", S): print 'Initial state must be a single character!'
        else:break


    print '+------------------------------------------------------+'
    print '|Give rules in the form A B (space-delimited), for A->B|'
    print '|or A BCD, if more than one states in the right part   |'
    print '|(without spaces between right part members).          |'
    print '+------------------------------------------------------+'


    # Taking in the rules and adding them to the vocabulary list
    for i in range(N):
        fr, to = map(str,raw_input('Rule #' + str(i + 1)+': ').split()) # A rule is actually in the form fr->to. However, user gives fr to.

        # Remove given letters from "letters pool"
        for l in fr:
            if l!='e' and l not in voc: voc.append(l)
            if l in let: let.remove(l)

        for l in to:
            if l!='e' and l not in voc: voc.append(l)
            if l in let: let.remove(l)

        # Insert rule to dictionary
        rules.setdefault(fr, []).append(to)


    # 1) STEP 1 Removing Long rules

    print '\nRules after large rules removal: '
    rules,let,voc = remove_large(rules,let,voc)
    print_rules(rules)  # Print Updated rules

    # 2) STEP 2  Removing NULL/epsilon rules
    print '\nRules after empty rules removal: '
    rules,voc = remove_epsilon(rules,voc)
    print_rules(rules)  # Print Updated rules

    # 3) STEP 3  Removing short/useless rules
    print '\nRules after short rules removal: '
    rules,D = remove_short(rules,voc)
    print_rules(rules)  # Print Updated rules


    # 4) STEP 4 Constructing the final grammar
    print '\nFinal rules'
    rules = final_rules(rules,D,S)
    print_rules(rules)  # Print final grammar


if __name__ == '__main__':
    main()
