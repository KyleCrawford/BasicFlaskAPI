def list_of_dict_issorted_by_key(dict, key):
    return all(dict[i][key] <= dict[i+1][key] for i in range(len(dict) - 1))

def list_of_dict_issorted_by_key_reverse(dict, key):
    return all(dict[i][key] >= dict[i+1][key] for i in range(len(dict) - 1))