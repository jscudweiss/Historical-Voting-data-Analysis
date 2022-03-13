class Tokenizer:
    def tokenize(self, token, string):
        arr_list = []
        i = -1
        n = 0
        for val in string:
            if val == token:
                match i:
                    case -1:
                        i = n
                        arr_list.append(string[:i])
                    case _:
                        arr_list.append(string[(i + 1):n])
                        i = n
            n += 1
        return arr_list


