import math #used for cos, sin

class Vector3:
    def __init__(self, x=0.0,y=0.0,z=0.0):
        self.x, self.y, self.z = map(float, (x,y,z))
        
    def __str__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)
        
    def __repr__(self):
        return self.__str__()
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        
    @staticmethod
    def fromPoints(src, dest):
        return Vector3(dest[0]-src[0], dest[1]-src[1], dest[2]-src[2])
    
    def len(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
        
    def normalize(self):
        length = self.len()
        if length > 0:
            return Vector3(self.x / length, self.y / length, self.z / length)
        else:
            return Vector3()
    
    def inormalize(self): #in-place normalization
        length = self.len()
        if length > 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self
        
    def irotate(self, a=None):
        """In-place versio of rotate."""
        if a==None: self.x*=-1; self.y*=-1; return
        x = (self.x * math.cos(a)) - (self.y * math.sin(a))
        y = (self.x * math.sin(a)) + (self.y * math.cos(a))
        self.x = x
        self.y = y
        return self
        
    def rotate(self, a=None):
        """Returns a vector rotatet with an angle of a around the z axis
        Use irotate to rotate in-place
        Not sending any argument will rotate by pi,
          eg. v.rotate() == -v"""
        if a == None: return self * (-1)
        x = (self.x * math.cos(a)) - (self.y * math.sin(a))
        y = (self.x * math.sin(a)) + (self.y * math.cos(a))
        
        return Vector3(x,y,self.z)
        
    def __iadd__(self, rhs):
        if not isinstance(rhs, Vector3):
            rhs = Vector3(rhs, rhs, rhs)
        self.x += rhs.x
        self.y += rhs.y
        self.z += rhs.z
        return self
        
    def __add__(self, rhs):
        if not isinstance(rhs, Vector3):
            rhs = Vector3(rhs, rhs, rhs)
        return Vector3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
    
    def __isub__(self, rhs):
        if not isinstance(rhs, Vector3):
            rhs = Vector3(rhs, rhs, rhs)
        self.x -= rhs.x
        self.y -= rhs.y
        self.z -= rhs.z
        return self
        
    def __sub__(self, rhs):
        if not isinstance(rhs, Vector3):
            rhs = Vector3(rhs, rhs, rhs)
        return Vector3(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
        
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
        
    def __imul__(self, scalar):
        scalar = float(scalar)
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self
        
    def __mul__(self, scalar):
        """Multiplies by scalar or with another vector (dot product)"""
        if isinstance(scalar, Vector3):
            return self.x*scalar.x + self.y*scalar.y + self.z*scalar.z
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
        
    def __idiv__(self, scalar):
        scalar = float(scalar)
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self
        
    def __div__(self, scalar):
        scalar = float(scalar)
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
        
    def tuple(self):
        return (self.x, self.y, self.z)
        
    def dot(self, rhs):
        """Returns the dot product of this vector with another vector"""
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z
        
    def angleTo(self, rhs):
        return math.acos(self.dot(rhs) / (self.len() * rhs.len()))
        
    def __pow__(self, rhs): #** operator is the same as cross product
        return self.cross(rhs)
    
    def cross(self, rhs):
        """Calculates the cross product of self and the rhs vector"""
        newX = self.y*rhs.z - self.z*rhs.y
        newY = self.z*rhs.x - self.x*rhs.z
        newZ = self.x*rhs.y - self.y*rhs.x
        
        return Vector3(newX, newY, newZ)
        
V3 = Vector3
e_x = V3(1,0,0)
e_y = V3(0,1,0)
e_z = V3(0,0,1)
norm = lambda *args: V3(*args).normalize()

ex, ey, ez = e_x, e_y, e_z

vsum = lambda seq: reduce(lambda a,b: a + b, seq)
        
if __name__ == "__main__":
    v = V3(-1,-1,0).normalize() * (1/math.sqrt(2))
    v += V3(1,1,0)
    v *= 2
    v /= 4
    v.irotate(math.pi)
    v2 = v.rotate(-math.pi/2)
    print v
    print v.dot(v2)
    print v.angleTo(v2)
