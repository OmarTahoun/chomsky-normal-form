from CNF import *

def main():
    rules = {}
    voc = []
    # This list's going to be our "letters pool" for naming new states
    let = list(letters[26:]) + list(letters[:25])

    let.remove('e')

    # Number of grammar rules
    while True:
        userInput = raw_input('Give number of rules: ')
        try:
            # check if N is integer >=2
            N = int(userInput)
            if N <=2: print 'N must be a number >=2!'
            else: break
        except ValueError:
            print "Must be an Integer"

    # Initial state
    while True:
        S = raw_input('Give initial state: ')
        if not re.match("[a-zA-Z]*$", S): print 'Initial state must be a single character!'
        else:break

    print '+------------------------------------------------------+'
    print '|Give rules in the form A B (space-delimited), for A->B|'
    print '|or A BCD, if more than one states in the right part   |'
    print '|(without spaces between right part members).          |'
    print '+------------------------------------------------------+'

    for i in range(N):
        # A rule is actually in the form fr->to. However, user gives fr to.
        fr, to = map(str,raw_input('Rule #' + str(i + 1)+': ').split())
        # Remove given letters from "letters pool"
        for l in fr:
            if l!='e' and l not in voc: voc.append(l)
            if l in let: let.remove(l)
        for l in to:
            if l!='e' and l not in voc: voc.append(l)
            if l in let: let.remove(l)
        # Insert rule to dictionary
        rules.setdefault(fr, []).append(to)

    # remove large rules and print new rules
    print '\nRules after large rules removal: '
    rules,let,voc = remove_large(rules,let,voc)
    print_rules(rules)
    #print voc

    # remove empty rules and print new rules
    print '\nRules after empty rules removal: '
    rules,voc = remove_epsilon(rules,voc)
    print_rules(rules)
    #print voc

    print '\nRules after short rules removal: '
    rules,D = remove_short(rules,voc)
    print_rules(rules)

    print '\nFinal rules'
    rules = final_rules(rules,D,S)
    print_rules(rules)

if __name__ == '__main__':
    main()
