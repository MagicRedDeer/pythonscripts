from __future__ import print_function

class adder(float):
    def __call__(self, num, mult=1):
        return adder( self + num * mult )

print (adder(10)(2)(3)(4)(5)(6)(6))
