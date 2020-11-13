import collections
import re

db = {
    's1': {
        (11, 6): [('Amy',10,2000), ('Bob',8,1500), ('Bob',7,1500)], # Bob rents twice
        (11, 7): [('Cam',12, 800)]
    },
    's2': {
        (10, 31): [('Cam',12, 800), ('Ida',30,8000)],
        (11, 6): [('Gil',20, 400), ('Dan',17,3500), ('Eva',15,1800)],
    }
}

#1a
def rentals (db : {str:{(int,int): [(str,int,int)]}}, date : (int,int)) -> int:
    total_count = 0
    for record_scooter in db.values():
        for date_key in record_scooter.keys():
            if date_key[0] == date[0] and date_key[1] == date[1]:
                total_count = total_count + 1
    return total_count

#1b
def by_month (db : {str:{(int,int): [(str,int,int)]}}) -> {int:int}:
    total_feets = {}
    for record_scooter in db.values():
        for date_key in record_scooter.keys():
            month = date_key[0]
            feet_in_month = 0
            for entry in record_scooter[date_key]:
                feet_in_month = feet_in_month + entry[2]
            if month in total_feets.keys():
                total_feets[month] = total_feets[month] + feet_in_month
            else:
                total_feets[month] = feet_in_month
    return total_feets


#1c
def by_name (db : {str:{(int,int): [(str,int,int)]}}) -> [str]:
    rent_by_name = {}
    for record_scooter in db.values():
        for date_key in record_scooter.keys():
            for entry in record_scooter[date_key]:
                if entry[0] in rent_by_name.keys():
                    data = rent_by_name[entry[0]]
                    rent_by_name[entry[0]] = (data[0] + 1, data[1] + entry[2])
                else:
                    rent_by_name[entry[0]] = (1, entry[2])
    sorted_ = collections.OrderedDict(sorted(rent_by_name.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True))
    return list(sorted_.keys())

#2a
def reg_match():
    pattern = "^x([ab]?c)*(x+)$"
    m = re.match(pattern, "xxx")
    print("xxx", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "xccccx")
    print("xccccx", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "xacbcxx")
    print("xacbcxx", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "xaacxx")
    print("xaacxx", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "x")
    print("x", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "xaax")
    print("xaax", 'Matched' if m != None else "Not matched")
    m = re.match(pattern, "xcacbcxx")
    print("xcacbcxx", 'Matched' if m != None else "Not matched")

#3

class Measurement:
    def __init__(self,low,high):
        assert low<=high, f'Measurement.__init__: low({low})>high({high})'
        self.low = low
        self.high = high

    # a) overload the method called by repr
    def __repr__(self):
        return f"{self.low} <= {self.high}"

    # b) overload the method called by < assuming both objects are Measurements
    def __lt__(self, other):
        return self.low < other.low

    # c) overload + allowing Measurement + Measurement, Measurement + int or float, and
    # int or float + Measurement; addition fails for any other combinations
    def __add__(self, other):
        if type(other) is Measurement:
            return Measurement(self.low + other.low, self.high + other.high)
        elif type(other) is int or type(other) is float:
            return Measurement(self.low + other, self.high + other)

    def __radd__(self, other):
        if other is type(int) or other is type(float):
            return Measurement(self.low + other, self.high + other)
        assert f'Measurement.add type error'

#4
class Scooter_DB:
    def __init__(self,rentals):
        self.rentals = rentals

    def __contains__(self, item):
        if item[1] in self.rentals.keys():
            scooter_record = self.rentals[item[1]]
            for date_record in scooter_record.values():
                for value in date_record:
                    if item[0] in value:
                        return True
        return False

    def __getitem__(self, item):
        item_list = []
        for scooter_record in self.rentals.values():
            if item in scooter_record.keys():
                item_list = item_list + scooter_record[item]
        return item_list

    def __delitem__(self, key):
        b_remove = False
        for s_key in self.rentals.keys():
            scooter_record = self.rentals[s_key]
            if key in scooter_record.keys():
                self.rentals[s_key].pop(key, None)
                b_remove = True
        if not b_remove:
            raise KeyError('Cannot find key')

if __name__ == '__main__':
    print (rentals(db, (11, 6)))
    print(by_month(db))
    print(by_name(db))
    reg_match()
    a = Measurement(2, 5)
    print(a)
    b = Measurement(3, 6)
    c = a + b
    print(c)
    s = Scooter_DB(db)
    print(('Alex','s1') in s)
    print(s[(11,6)])
    del s[(11,6)]
    print(s[(11, 6)])
    del s[(11, 6)]
