class myclass:
   def __init__(self,one,two,three):
       self.one = one
       self.two = two
       self.three = three



my = myclass(two=2,three=3,one=None)

print(my.two)
print(my.three)
