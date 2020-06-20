def get_percentage(num, round_digits=None):
    return str(round(num * 100, ndigits=round_digits)) + '%'


print(get_percentage(0.0123))      # 1%
print(get_percentage(0.0123, 0))   # 1.0%
print(get_percentage(0.0123, 1))   # 1.2%
print(get_percentage(0.0123, 10))  # 1.23%
