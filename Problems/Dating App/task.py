def select_dates(potential_dates):
    to_print = [potential_date.get('name') for potential_date in potential_dates if potential_date.get('age') > 30 and 'art' in potential_date.get('hobbies') and potential_date.get('city') == 'Berlin']
    return ', '.join(to_print)
