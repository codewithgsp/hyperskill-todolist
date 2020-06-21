# put your python code here
def double_alphabet_dict():
    dict_ = {}
    for num in range(97, 97 + 26):
        dict_[chr(num)] = chr(num) * 2
    return dict_


double_alphabet = double_alphabet_dict()
