import re, traceback, keyword


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._fields = ["x", "y"]
        self._mutable = True

    def __repr__(self):
        return f'Point(x={self.x},y={self.y})'

    def __getitem__(self, index):
        if index == 0:
            return self.get_x()
        if index == 1:
            return self.get_y()
        elif index in self._fields:
            return self.__dict__[index]
        else:
            raise IndexError('{type_name}.__getitem__: index(' + str(index) + ') is illegal')

    def _make(self, p):
        return Point(p[0], p[1])

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def _asdict(self):
        return {"x": self.x, "y": self.y}

    def __eq__(self, right):
        if type(right) is not Point:
            return False

        for i, _ in enumerate(self._fields):
            print('self[i]: ' + str(self[i]))
            print('right[i]: ' + str(right[i]))
            if self[i] != right[i]:
                return False
        return True

    def _replace(self, **kargs):
        if self._mutable:
            for f, v in kargs.items():
                self.__dict__[f] = v
            return None
        else:
            for f in self._fields:
                if f not in kargs:
                    kargs[f] = self.__dict__[f]
            return Point(**kargs)


def pnamedtuple(type_name, field_names, mutable=False, defaults={}):
    def show_listing(s):
        for line_nmber, line_txt in enumerate(s.split('\n'), 1):
            print(f' {line_nmber: >3} {line_txt.rstrip()}')

    def legal_name(name):
        return type(name) is str and name not in keyword.kwlist and re.match('[a-zA-Z]\w*', name)

    def unique(iterable, max_times=1):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i

    # Validate arguments
    if not legal_name(type_name):
        raise SyntaxError('pcollections.pnamedtuple: type_name is not legal: ' + str(type_name))

    if type(field_names) is str:
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) is not list:
        raise SyntaxError('pcollections.pnamedtuple: field_names is not legal: ' + str(field_names))

    field_names = [f for f in unique(field_names)]
    for n in field_names:
        if not legal_name(n):
            raise SyntaxError('pcollections.pnamedtuple: field name is not legal: ' + str(n))

    # Define templates to be filled in, becoming definitions
    class_template = '''\
class {type_name}:
    def __init__(self, {fields}):
        {inits}
        self._fields = [{fields_as_string}]
        self._mutable = {mutable}            # must be set last: see __setattr__
    def __repr__(self):
        return '{type_name}({repr_fmt})'.format({self_fmt})

    def __getitem__(self,index):
        if type(index) is int and 0 <= index < len(self._fields):
            return eval('self.get_'+self._fields[index]+'()')
        elif index in self._fields:
            return self.__dict__[index]
        else:
            raise IndexError('{type_name}.__getitem__: index('+str(index)+') is illegal')
    def __eq__(self,right):
        if type(right) is not {type_name}:
            return False

        for i in self._fields:
            if self[i] != right[i]:
                return False
        return True

    def _replace(self,**kargs):
        for f,v in kargs.items():
            if f not in self._fields:
                raise TypeError("Not found key in the fields")

        if self._mutable:
            for f,v in kargs.items():
                self.__dict__[f] = v
            return None
        else:
            for f in self._fields:
                if f not in kargs:
                    kargs[f] = self.__dict__[f]
            return {type_name}(**kargs)

    def _make(p):
        return {type_name}({make_params})

    def _asdict(self):
        ret_dict = {{}}
        for field_name in self._fields:
            ret_dict[field_name] = eval('self.'+field_name)
        return ret_dict

'''

    mutable_template = '''\
    def __setattr__(self,name,value):
        if ('_mutable' not in self.__dict__ or self._mutable) and name in [{fields},'_fields','_mutable']:
            self.__dict__[name] = value
        else:
            raise AttributeError("Attempted to mutate immutable {type_name} object for field named '"+name+"'")
'''

    get_template = '''\
    def get_{name}(self):
        return self.{name}

'''

    init_template = 'self.{name} = {name}'
    repr_template = '{name}'
    self_template = '{name}=self.{name}'
    fields = ""
    for field_name in field_names:
        if field_name not in defaults.keys():
            fields = fields + "," + field_name

    for field_name in field_names:
        if field_name in defaults.keys():
            fields = fields + "," + field_name + "=" + str(defaults[field_name])

    if fields[0] == ",":
        fields = fields[1:]

    make_params = ""
    for index, field_name in enumerate(field_names):
        make_params = make_params + "," + field_name + f"=p[{index}]"
    if make_params[0] == ",":
        make_params = make_params[1:]

    # Fill-in the class template
    class_definition = class_template.format(
        type_name=type_name,
        fields=fields,
        fields_as_string=','.join("'" + name + "'" for name in field_names),
        inits=('\n' + 8 * ' ').join(init_template.format(name=name) for name in field_names),
        mutable=str(mutable),
        repr_fmt=','.join(name + '=' + '{' + repr_template.format(name=name) + '}' for name in field_names),
        self_fmt=','.join(self_template.format(name=name) for name in field_names),
        make_params=make_params
    )

    get_definition = ''.join([get_template.format(name=n) for n in field_names])
    mutate_definition = mutable_template.format(fields=','.join("'" + name + "'" for name in field_names),
                                                type_name=type_name)

    class_definition += get_definition + mutate_definition

    # For initial debugging, always show the source code of the class
    # show_listing(class_definition)

    # Execute the class_definition string in a local name_space and bind the
    #   name source_code in its dictionary to the class_defintion; return the
    #   class object created; if there is a syntax error, list the class and
    #   show the error
    name_space = dict(__name__=f'pnamedtuple_{type_name}'.format(type_name=type_name))
    try:
        exec(class_definition, name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError, SyntaxError):
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    # driver tests
    from courselib import driver

    driver.default_file_name = 'bscp3F20.txt'
    #     driver.default_show_exception_message= True
    #     driver.default_show_traceback= True
    driver.driver()

    x = Point(1, 'hello')
    print(x)
    x._mutable = False
    new_x = x._replace(y=3)

