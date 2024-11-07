
def process(feas, slot_id, op_func, **args):
    feas[slot_id] = op_func(**args)
