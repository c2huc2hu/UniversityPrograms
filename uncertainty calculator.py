############################# UNCERTAINTY CALCULATOR ############################
# The Measurement class holds the value and uncertainty of objects allowing
# for error calculations. It supports all of the arithmetic operations that
# made sense. Note that this version of error calculation is not the real one,
# but rather it follows the rule "pick the larger error" as directed in the
# document "Simplified Uncertainty Analysis in PHY180".
#
# author: Christopher Chu
# last modified: 2014-09-07 20:48
#
# Possible improvements:
# - add support for units.
# - if I use this heavily, create __iadd__, __isub__ etc. to be more efficient. 
#################################################################################


########################### INSTRUCTIONS #####################################
# Run this file in IDLE which can be found at (for windows): C:/Python33/Lib/idlelib/idle.bat
# Press F5 to run the calculator. 
#
# To create a value with an uncertainty (e.g. 5.2±0.3, use: 
# >>> a = Measurement(5.2, 0.3)
# or (M is short for Measurement)-
# >>> a = M(5.2, 0.3)
#
# To do arithmetic, add variables or measurements. +, -, *, / and ** (for integer powers) are defined 
# >>> b = M(5.26, 0.05)
# >>> a + b
# >>> (a + b) * M(6.245, 0.004)
#
# The underscore is helpful. It refers to the output of the last line.
# The following is equivalent to the above. 
# >>> a + b
# >>> _ * M(6.245, 0.004) 

import numbers

class Measurement (numbers.Real):
    def __init__ (self, value, uncertainty):
        self.value = value
        self.uncertainty = abs(uncertainty)

    def _operator_fallbacks(base_operator):
        """
        Returns both the function and its right inverse.
        Interpreted from https://docs.python.org/3.3/library/numbers.html
        """
        def forward (a, b):
            if isinstance (b, Measurement):
                return base_operator (a, b)
            elif isinstance (b, numbers.Real):
                return base_operator (a, Measurement (b, 0))
            
            else:   
                return NotImplemented
        def reverse (b, a):
            if isinstance (a, Measurement):
                return base_operator (a, b)
            elif isinstance (b, numbers.Real):
                return base_operator (Measurement (a, 0), b)
            else:
                return NotImplemented
        forward.__doc__ = base_operator.__doc__
        reverse.__doc__ = base_operator.__doc__
        
        return forward, reverse

    ### MATH OPERATORS ###
    def _add (self, other):
        """Add the measurements"""
        return Measurement (self.value + other.value, max (self.uncertainty, other.uncertainty))
    def _sub (self, other):
        return Measurement (self.value - other.value, max (self.uncertainty, other.uncertainty))
    def _mul (self, other):
        if abs(self.uncertainty / self.value) > abs(other.uncertainty / other.value):
            return Measurement (self.value * other.value, abs(other.value * self.uncertainty)) #self.value * other.value * self.uncertainty / self.value
        else:
            return Measurement (self.value * other.value, abs(self.value * other.uncertainty)) #self.value * other.value * other.uncertainty / other.value
    def _truediv (self, other):
        if abs(self.uncertainty / self.value) > abs(other.uncertainty / other.value):
            return Measurement (self.value / other.value, abs(self.uncertainty / other.value)) #self.value / other.value * self.uncertainty / self.value
        else:
            return Measurement (self.value / other.value, abs(self.value / other.value * other.uncertainty / other.value)) #self.value / other.value * other.uncertainty / other.value
    def __pow__ (self, other):
        "Raise to a power. Only defined on integral powers"
        if isinstance (other, numbers.Integral):
            return Measurement (self.value ** other, self.value ** (other - 1) * self.uncertainty)
        else:
            return NotImplemented
        
    __add__, __radd__ = _operator_fallbacks (_add)
    __sub__, __rsub__ = _operator_fallbacks (_sub)
    __mul__, __rmul__ = _operator_fallbacks (_mul)
    __truediv__, __rtruediv__ = _operator_fallbacks (_truediv)


    ### COMPARISON OPERATORS ###
    def __gt__ (self, other):
        if self.value - self.uncertainty - other.uncertainty > other.value:
            return True
        else:
            return False
    __ge__ = __gt__
    def __lt__ (self, other):
        if self.value + self.uncertainty + other.uncertainty < other.value:
            return True
        else:
            return False
    __le__ = __lt__
    
    ### MISCELLANEOUS OPERATORS ###
    def __abs__ (self):
        "Makes the value non-negative"
        return Measurement (abs (self.value), self.uncertainty)
    def __float__ (self):
        "Returns the value ignoring the uncertainty"
        return self.value
    def __neg__ (self):
        "Negates the value"
        return Measurement (-self.value, self.uncertainty)
    def __pos__ (self):
        "Does nothing"
        return Measurement (self.value, self.uncertainty)
    def __round__ (self, other):
        if isinstance (other, numbers.Integral):
            return Measurement (round (self.value, other), round (self.value, other))
        else:
            return NotImplemented
    def __repr__ (self):
        import math
        uncert_precision = -math.floor (math.log10 (abs (self.uncertainty))) #TODO: fix this
        #the error only has one decimal place and it doesn't make sense to return the value more precisely than that (for PHY180 at least)
        return "{}±{}".format (round (self.value, uncert_precision), round (self.uncertainty, uncert_precision))
    def __trunc__ (self):
        import math
        return Measurement (math.trunc (self.value), math.trunc (self.uncertainty))

    __ceil__ = __eq__ = __floor__ = __floordiv__ = __mod__ = __ne__ = __rfloordiv__= __rmod__= __rpow__= __trunc__ = lambda self: NotImplemented


if __name__ == "__main__":
    #These tests are not comprehensive, and I haven't done very many of them.
    #I don't guarantee that this code works. 
    M = Measurement

    d = M(2.8480, 0.0005)
    t = M(0.755, 0.005)

    print (d + t)
    print (-d)
    e = M(-5.25, 1)
    print (e, e + d, e * d)
    print ("d * 4 = ", d * 4)
    print ("4 * d = ", 4 * d)
    print (d * 4.53, 4.15 * d)
