from FSM import FSM, concat, add, iteration, intersect, shortest_word, SIGMA, dfsm, EPSILON


def fsm_from_expression(expression):
    fsm_stack = []
    for char in expression:
        if char in SIGMA or char == EPSILON:
            fsm = FSM()
            fsm_stack.append(fsm.create(char))
        elif char == '.':
            second_fsm = fsm_stack.pop()
            first_fsm = fsm_stack.pop()
            fsm_stack.append(concat(first_fsm, second_fsm))

        elif char == '+':
            first_fsm = fsm_stack.pop()
            second_fsm = fsm_stack.pop()
            fsm_stack.append(add(first_fsm, second_fsm))

        elif char == '*':
            fsm = fsm_stack.pop()
            fsm_stack.append(iteration(fsm))

    if len(fsm_stack) != 1:
        raise IndexError
    return fsm_stack[0]


def natural_notation(reg_expr):
    reg_expr_list = list(reg_expr)
    res = []
    for char in reg_expr_list:
        if char in SIGMA or char == EPSILON:
            res.append(char)
        elif char == '.':
            expr1 = res.pop()
            expr2 = res.pop()
            res.append(expr2 + '.' + expr1)
        elif char == '+':
            expr1 = res.pop()
            expr2 = res.pop()
            res.append('('+expr2+'+'+expr1+')')
        elif char == '*':
            expr = res.pop()
            if len(expr) > 1:
                res.append('('+expr+')*')
            else:
                res.append(expr+'*')
        else:
            raise IndexError
    if len(res) > 1:
        print res
        raise IndexError
    return res[0]


def reverse_polish_notation(reg_exp):
    res = ''
    stack = []
    for char in reg_exp:
        if char in SIGMA or char == EPSILON or char == '*':
            res += char
        elif char == ')':
            while stack[-1] != '(':
                res += stack.pop()
            stack.pop()
        elif char == '+':
            while len(stack) > 0 and stack[-1] == '.':
                res += stack.pop()
            stack.append(char)
        elif char == '.' or char == '(':
            stack.append(char)
        else:
            raise IndexError
    while len(stack) != 0:
        if stack != '(':
            res += stack.pop()
        else:
            raise IndexError
    return res


if __name__ == "__main__":
    try:
        print 'Enter reg expr:'
        reg_expr = raw_input()
        nfsm = fsm_from_expression(reverse_polish_notation(reg_expr))
        print '======================================================'
        print 'NFSM:'
        print nfsm
        print '======================================================'
        print 'DFSM:'
        print dfsm(nfsm)
    except IndexError:
        print 'wrong reg expr'

