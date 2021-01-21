class Rectangle:
    def __init__(self,w,h):
        self.w=w
        self.h=h

    def area(self):
        return self.w*self.h

    def __mul__(self, rect2):
        return Rectangle(self.w*rect2.w,self.h*rect2.h)

    def __str__(self):
        return "I am a rectangle."

rex=Rectangle(3,4)
print(rex)
print(rex.area())
print(rex(3,4))