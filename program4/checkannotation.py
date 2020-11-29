from goody import type_as_str
import inspect


class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """

    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_All_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        for annot in self._annotations:
            check(param, annot, value,
                  check_history + 'Check_All_OK check: ' + str(annot) + ' while trying: ' + str(self) + '\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """

    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_Any_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations:
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param) + ' failed annotation check(Check_Any_OK): value = ' + repr(value) + \
                          '\n  tried ' + str(self) + '\n' + check_history


class Check_Annotation:
    # Start off binding the class attribute to True allowing checking to occur
    #   (but iff the function's self._checking_on is likewise bound to True)
    checking_on = True

    # To check the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.
    def check(self, param, annot, value, check_history=''):
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        def check_list_tuple(_param, _annot, _value, _check_history):
            history = _check_history
            if type(_annot) != type(_value):
                assert False, f"{repr(_param)} failed annotation check(wrong type) : \n " \
                              f"value = {_value} \n was type {type_as_str(_value)} should be type {type_as_str(_annot)}"
            if type(_annot) is list:
                _type = "list"
            else:
                _type = "tuple"

            if len(_annot) == 1:
                for i in range(len(_value)):
                    self.check(_param, _annot[0], _value[i], history)
                    history = history + f"{_type} [{i}] check: {str(annot[0])} \n"
                return True
            if not len(_annot) == len(_value):
                assert False, f"{repr(_param)} failed annotation check(wrong number of elements) : \n " \
                              f"value = [{str(len(_value))}] \n annotation had {str(len(_annot))} " \
                              f"elements {str(_annot)} \n {history}"
            for i in range(len(_value)):
                self.check(_param, _annot[i], _value[i], history)
                history = history + _type + " check: " + str(_annot[i]) + "\n"
            return True

        def check_dict(_param, _annot, _value, _check_history):
            history = _check_history
            if not isinstance(_value, dict):
                assert False, f"{repr(_param)} failed annotation check(wrong type): value = " \
                              f"{repr(_value)}\n  was type {type(_value)} ...should be type dict\n {history}"
            if len(_annot) != 1:
                assert False, f"{repr(_param)} annotation inconsistency: dict should have 1 item but had {str(len(_annot))} " \
                              f"\n  annotation = {str(_annot)} \n {history}"

            # annot_key_type = [k for k in _annot.keys()][0]
            # annot_value_type = [_annot[k] for k in _annot.keys()][0]
            annot_key_type = annot_value_type = ""
            for k in _annot.keys():
                annot_key_type = k
                annot_value_type = _annot[k]
                break

            for value_k, value_v in _value.items():
                self.check(_param, annot_key_type, value_k, history)
                history = history + f"dict key check: {str(annot_key_type)} \n"
                self.check(_param, annot_value_type, value_v, history)
                history = history + f"dict value check: {str(annot_value_type)} + '\n"
            return True

        def check_set_frozen(_param, _annot, _value, _check_history):
            history = _check_history
            if type(_annot) != type(_value):
                assert False, f"{repr(_param)} failed annotation check(wrong type) : \n " \
                              f"value = {_value} \n was type {type_as_str(_value)} should be type {type_as_str(_annot)}"
            if isinstance(_annot, set):
                _type = "set"
            else:
                _type = "frozenset"
            if len(_annot) != 1:
                assert False, f"{repr(_param)}  annotation inconsistency: {type} should have 1 value but had " \
                              f"{str(len(_annot))} \n  annotation = {str(_annot)} \n {history}"
            set_annot = next(iter(_annot))
            for _v in _value:
                self.check(_param, set_annot, _v, history)
                history = history + f"set value check: {str(set_annot)} \n"
            return True

        def check_lambda(_param, _annot, _value, _check_history):
            history = _check_history
            if not len(_annot.__code__.co_varnames) == 1:
                assert False, f"{repr(_param)} annotation inconsistency: predicate should have 1 parameter but had " \
                              f"{str(len(_annot.__code__.co_varnames))} \n  annotation = {str(_annot)} \n {history}"
            try:
                 if not _annot(value):
                     assert False, f"{repr(_param)} failed annotation check value = {value}"
            except:
                assert False, f"{repr(_param)} annotation predicate ( {str(_annot)} ) raised exception "

        def check_str(_param, _annot, _value, _check_history):
            history = _check_history
            try:
                returned = eval(_annot, _value)
                if not returned:
                    assert False, f"{repr(_param)} failed annotation check(str predicate {_annot}) \n " \
                                  f" args for evaluation: {_value}"
            except:
                assert False, f"{repr(_param)} failed annotation check(str predicate {_annot}) \n " \
                              f" args for evaluation: {_value}"

        # Start off by matching check's function annotation with its arguments
        # Return result of calling decorated function call, checking present
        if annot is None:
            return True
        if type(annot) is type:
            if not isinstance(value, annot):
                msg = f"{repr(param)} failed annotation check(wrong type) : value = " \
                              f"{repr(value)} \n  was type {type(value)} shuold be type {str(annot)} \n"
                assert False, msg
            return f"{repr(param)} succeed annotation check : value = {repr(value)}\n  is type {type(value)} \n"
        elif isinstance(annot, list) or isinstance(annot, tuple):
            check_list_tuple(param, annot, value, check_history)
        elif isinstance(annot, dict):
            check_dict(param, annot, value, check_history)
        elif isinstance(annot, set) or isinstance(annot, frozenset):
            check_set_frozen(param, annot, value, check_history)
        elif inspect.isfunction(annot):
            check_lambda(param, annot, value, check_history)
        elif type(annot) is str:
            check_str(param, annot, value, check_history)
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except:
                msg = f"{repr(param)} failed annotation exception occured \n"
                assert False, msg

    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):

        # Return the parameter/argument bindings via an ordereddict (a special
        #   kind of dict): it binds the function header's parameters in order
        def param_arg_bindings():
            f_signature = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args, **kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not self._checking_on or not Check_Annotation.checking_on:
            return self._f(*args, *kargs)

        f_args = param_arg_bindings()
        print(f_args)
        try:
            # For each annotation found, check if the parameter satisfies it
            print(self._f.__annotations__)
            for annotation in self._f.__annotations__.keys():
                if annotation not in f_args.keys():
                    continue
                if type(self._f.__annotations__[annotation]) == str:
                    self.check(annotation,
                               self._f.__annotations__[annotation],
                               f_args)
                else:
                    self.check(annotation,
                               self._f.__annotations__[annotation],
                               f_args[annotation])
            # Compute/remember the value of the decorated function
            return_result = self._f(*args, *kargs)
            # If 'return' is in the annotation, check it
            if 'return' in self._f.__annotations__:
                self.check("return",
                           self._f.__annotations__["return"],
                           return_result)
            # Return the decorated answer
            return return_result

        # On first AssertionError, print the source lines of the function and reraise
        except AssertionError:
            # print(80 * '-')
            # for l in inspect.getsourcelines(self._f)[0]:  # ignore starting line #
            #     print(l.rstrip())
            # print(80 * '-')
            raise


if __name__ == '__main__':
    # an example of testing a simple annotation
    # driver tests
    import driver

    def f(x: None) -> int: return x
    f = Check_Annotation(f)
    f(3)

    driver.default_file_name = 'bscp4F20.txt'
    #     driver.default_show_exception= True
    #     driver.default_show_exception_message= True
    #     driver.default_show_traceback= True
    driver.driver()
