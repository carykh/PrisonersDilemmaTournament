encoding = {
    'd': 0,
    'c': 1
}
inv_encoding = {
    0: 'd',
    1: 'c'
}


def decode(choice, history):
    choice = encoding.get(choice.lower())
    if choice is None:
        return 1 if history.shape[1] == 0 else history[1, -1]
    return choice

def code(response):
    return ''.join(inv_encoding.get(digit, '*') for digit in response)


#### STATES ###

def counter_alld(response):
    if 'c' in response:
        return 'ccc', recover_phase_a
    return '***', counter_alld

def counter_random(response):
    if 'c' not in response:
        return 'ccc', recover_phase_a
    return 'ddd', counter_random

def recover_phase_b(response):
    if 'd' in response:
        return 'ddd', counter_random
    return 'c', wait_for_defect

def recover_phase_a(response):
    if response in ('ccd', 'cdc', 'dcc'):
        return 'ccc', recover_phase_b
    if response == 'ccc':
        return 'c', wait_for_defect
    if response == 'ddd':
        return 'd**', counter_alld
    return 'ddd', counter_random

def wait_for_defect(response):
    if response == 'd':
        return 'dcc', recover_phase_a
    return 'c', wait_for_defect

def wait_for_coop(response):
    if response == 'c':
        return 'ccc', recover_phase_a
    return 'd', wait_for_coop

def strategy(history, memory):
    if memory is None:
        state, schedule, count = wait_for_defect, list('c'), 0
    else:
        state, schedule, count = memory

    if len(schedule) == 0:
        response = code(history[1, -count:])
        schedule, state = state(response)
        schedule = list(schedule)
        count = 0
    choice = decode(schedule.pop(0), history)
    count += 1
    return choice, (state, schedule, count)
