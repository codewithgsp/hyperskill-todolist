# The following line creates a dictionary from the input. Do not modify it, please
import json
test_dict = json.loads(input())
min_key = ''
max_key = ''
min_value = min(test for test in test_dict.values())
max_value = max(test for test in test_dict.values())
# Work with the 'test_dict'
for test in test_dict:
    if min_value == test_dict.get(test):
        min_key = test
    elif max_value == test_dict.get(test):
        max_key = test

print('min:', min_key)
print('max:', max_key)

print("min: {0}".format(min(test_dict, key=test_dict.get)))
print("max: {0}".format(max(test_dict, key=test_dict.get)))
