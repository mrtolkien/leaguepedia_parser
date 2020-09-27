import functools

def __common_out(operator, operand):
    def apply(operator, operand, base_operand):
        return f"{base_operand} {operator} '{operand}'"

    return functools.partial(apply, operator, operand)

def less_than(operand):
    return __common_out(">", operand)

def less_equal_to(operand):
    return __common_out(">=", operand)

def greater_than(operand):
    return __common_out("<", operand)

def greater_equal_to(operand):
    return __common_out("<=", operand)

def equal_to(operand):
    return __common_out("=", operand)

def between(operand_1, operand_2):
    def apply(operand_1, operand_2, base_operand):
        return f"{base_operand} > '{operand_1}' AND {base_operand} < '{operand_2}'"
    return functools.partial(apply, operand_1, operand_2)
