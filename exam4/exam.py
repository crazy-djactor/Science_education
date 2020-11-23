from goody import type_as_str  # Useful in some exceptions
import prompt                  # Use functions here if needed


class DictList:
    def __init__(self, *args):
        if len(args) == 0:
            raise AssertionError("Type is not supported")
        self.dl = []
        for arg in args:
            if type(arg) is not dict:
                raise AssertionError("Type is not supported")
            self.dl.append(arg.copy())

    def __len__(self):
        key_list = []
        total_len = 0
        for dict_ in self.dl:
            new_count = len(dict_.keys())
            for key in dict_.keys():
                if key in key_list:
                    new_count = new_count - 1
                else:
                    key_list.append(key)
            total_len = total_len + new_count
        return total_len

    def __repr__(self):
        ret_str = ""
        for dict_ in self.dl:
            ret_str = ret_str + "," + str(dict_)
        return "DictList(" + ret_str[1:] + ")"

    def __contains__(self, item):
        for dict_ in self.dl:
            if item in dict_.keys():
                return True
        return False

    def __getitem__(self, item):
        for dict_ in reversed(self.dl):
            if item in dict_.keys():
                return dict_[item]
        raise KeyError("Type is not supported")

    def __setitem__(self, key, value):
        for dict_ in reversed(self.dl):
            if key in dict_.keys():
                dict_[key] = value
                return
        new_item = {key: value}
        self.dl.append(new_item)

    def __call__(self, *args, **kwargs):
        k = args[0]
        ret_val = []
        for index, dict_ in enumerate(self.dl):
            if k in dict_.keys():
                ret_val.append((index, dict_[k]))
        return ret_val

    def __iter__(self):
        key_list = []
        for dict_ in reversed(self.dl):
            sorted_dict = sorted(dict_)
            for k in sorted_dict:
                if k in key_list:
                    continue
                key_list.append(k)
                yield k, dict_[k]

    def __eq__(self, other):
        if type(other) is not DictList and type(other) is not dict:
            raise TypeError("Type is not supported")
        for k, v in self.__iter__():
            try:
                if other[k] != v:
                    return False
            except:
                return False

        if type(other) is DictList:
            for k, v in other:
                try:
                    if self.__getitem__(k) != v:
                        return False
                except:
                    return False
        else:
            for k in other.keys():
                try:
                    if self.__getitem__(k) != other[k]:
                        return False
                except:
                    return False

        return True

    def __add__(self, other):
        if type(other) is not dict and type(other) is not DictList:
            raise TypeError("Type is not supported")

        if type(other) is DictList:
            self_result = {}
            for dict_ in self.dl:
                for k in dict_.keys():
                    self_result[k] = dict_[k]

            dict_result = {}
            for dict_ in other.dl:
                for k in dict_.keys():
                    dict_result[k] = dict_[k]
            return DictList(self_result, dict_result)

        ret_list = self.dl.copy()
        ret_list.append(other)
        return DictList(*ret_list.copy())

    def __radd__(self, other):
        if type(other) is not dict:
            raise TypeError("Type is not supported")
        ret_list = self.dl.copy()
        ret_list.insert(0, other)
        return DictList(*ret_list.copy())

if __name__=='__main__':  
    #Put code here to test DictList before doing bsc test
    # d0 = dict(a=1, b=2, c=3)
    # d = DictList(d0)
    # len1 = len(d)
    #driver tests
    import driver
    driver.default_file_name = 'bscile2F20.txt'  
    #Uncomment the following lines to see MORE details on exceptions  
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
