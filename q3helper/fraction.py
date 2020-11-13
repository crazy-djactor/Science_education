from goody import irange
from goody import type_as_str

from courselib.driver import driver


class Fraction:
    # Call as Fraction._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    @staticmethod
    def _gcd(x : int, y : int) -> int:
        assert x >= 0 and y >= 0, 'Fraction._gcd: x('+str(x)+') and y('+str(y)+') must be >= 0'
        while y != 0:
            x, y = y, x % y
        return x

    # Returns a string that is the decimal representation of a Fraction, with
    #   decimal_places digitst appearing after the decimal points.
    # For example: if x = Fraction(23,8), then x(5) returns '2.75000'
    def __call__(self, decimal_places):
        answer = ''
        num = self.num
        denom = self.denom
    
        # handle negative values
        if num < 0:
            num, answer = -num, '-'
    
        # handle integer part
        if num >= denom:
            answer += str(num//denom)
            num = num - num//denom*denom
            
        # handle decimal part
        answer += '.'+str(num*10**decimal_places//denom)
        return answer
    
    @staticmethod
    # Call as Fraction._validate_arithmetic(..); with no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Fraction or int is...
    # Fraction._validate_arithmetic(right, {Fraction,int},'+','Fraction',type_as_str(right))
    def _validate_arithmetic(v, t : set, op : str, lt : str, rt : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+lt+'\' and \''+rt+'\'')        

    @staticmethod
    # Call as Fraction._validate_relational(..); with no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v, t : set, op : str, rt : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Fraction() '+op+' '+rt+'()')        

    def __init__(self, num=0, denom=1):
        assert denom != 0 and isinstance(num, int) and isinstance(denom, int), \
            "Denominator can't be Zero and arguments should be integers"
        if num == 0:
            denom = 1
        if denom < 0:
            num *= -1
            denom *= -1
        gcd = self._gcd(abs(num), abs(denom))
        self.num = num//gcd
        self.denom = denom//gcd
        
    def __repr__(self):
        repr_str = f"Fraction({self.num},{self.denom})"
        return repr_str
    
    def __str__(self):
        _str = f"{self.num}/{self.denom}"
        return _str
   
    def __bool__(self):
        if self.num == 0:
            return False
        return True
    
    def __getitem__(self, i):
        if isinstance(i, int):
            if i == 0:
                return self.num
            elif i == 1:
                return self.denom

        elif isinstance(i, str):
            if "numerator".startswith(i):
                return self.num
            elif "denominator".startswith(i):
                return self.denom
        raise TypeError("Not supported index or key")
 
    def __pos__(self):
        x = Fraction(self.num, self.denom)
        return x
    
    def __neg__(self):
        x = Fraction((-1)*self.num, self.denom)
        return x
    
    def __abs__(self):
        x = Fraction(abs(self.num), self.denom)
        return x
    
    def __add__(self, right):
        Fraction._validate_arithmetic(right, {Fraction, int}, '+', 'Fraction', type_as_str(right))
        if type(right) is Fraction:
            x = Fraction(self.num * right.denom + self.denom*right.num, self.denom*right.denom)
        else:
            x = Fraction(self.num + right*self.denom, self.denom)
        return x

    def __radd__(self, left):
        Fraction._validate_arithmetic(left, {int}, '+', 'Fraction', type_as_str(left))
        x = Fraction(self.num + left*self.denom, self.denom)
        return x

    def __sub__(self, right):
        Fraction._validate_arithmetic(right, {Fraction, int}, '-', 'Fraction', type_as_str(right))
        if type(right) is Fraction:
            x = Fraction(self.num*right.denom - self.denom * right.num, self.denom * right.denom)
        else:
            x = Fraction(self.num - right*self.denom, self.denom)
        return x
     
    def __rsub__(self, left):
        Fraction._validate_arithmetic(left, {int}, '-', 'Fraction', type_as_str(left))
        x = Fraction(left * self.denom - self.num, self.denom)
        return x

    def __mul__(self, right):
        Fraction._validate_arithmetic(right, {Fraction, int}, '*', 'Fraction', type_as_str(right))
        if type(right) is Fraction:
            x = Fraction(self.num*right.num, self.denom*right.denom)
        else:
            x = Fraction(self.num*right, self.denom)
        return x

    def __rmul__(self, left):
        Fraction._validate_arithmetic(left, {int}, '*', 'Fraction', type_as_str(left))
        x = Fraction(self.num*left, self.denom)
        return x

    def __truediv__(self, right):
        Fraction._validate_arithmetic(right, {Fraction, int}, '/', 'Fraction', type_as_str(right))
        if type(right) is Fraction:
            x = Fraction(self.num*right.denom, self.denom*right.num)
        else:
            x = Fraction(self.num, self.denom*right)
        return x

    def __rtruediv__(self, left):
        Fraction._validate_arithmetic(left, {int}, '/', 'Fraction', type_as_str(left))
        x = Fraction(left*self.denom, self.num)
        return x

    def __pow__(self, right):
        Fraction._validate_arithmetic(right, {int}, '**', 'Fraction', type_as_str(right))
        if right > 0:
            x = Fraction(pow(self.num, right), pow(self.denom, right))
        else:
            x = Fraction(pow(self.denom, -right), pow(self.num, -right))
        return x

    def __eq__(self, right):
        Fraction._validate_relational(right, {Fraction, int}, "==", type_as_str(right))
        if type(right) is Fraction:
            if self.num*right.denom == self.denom*right.num:
                return True
        else:
            if self.num == self.denom*right:
                return True
        return False

    def __lt__(self, right):
        Fraction._validate_relational(right, {Fraction, int}, "<", type_as_str(right))
        if type(right) is Fraction:
            if self.num * right.denom < self.denom * right.num:
                return True
        else:
            if self.num < self.denom * right:
                return True
        return False
    
    def __gt__(self, right):
        Fraction._validate_relational(right, {Fraction, int}, ">", type_as_str(right))
        if type(right) is Fraction:
            if self.num * right.denom > self.denom * right.num:
                return True
        else:
            if self.num > self.denom * right:
                return True
        return False

    # Uncomment this method when you are ready to write/test it
    # If this is pass, then no attributes will be set!
    def __setattr__(self,name,value):
        if name in self.__dict__.keys():
            raise NameError("unsupported operand. can't set attributes")
        self.__dict__[name] = value

##############################


# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Fraction(1,2)
    x      = Fraction(1,2)
    for i in irange(1,n):
        big    = 2*i+1
        answer += Fraction(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer


if __name__ == '__main__':
    # Put in simple tests for Fraction before allowing driver to run
    f = Fraction(1, -2)
    print(f.num)

    driver.default_file_name = 'bscq31F20.txt'
    driver.default_show_traceback= True
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver()
