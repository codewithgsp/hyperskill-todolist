def get_bonus(salary, percentage=35):
    return int(str(salary * percentage / 100).split('.')[0])
