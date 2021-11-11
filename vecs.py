class Vec3():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return (self.x * self.x + self.y * self.y + self.z * self.z)**0.5

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __gt__(self, other):
        return self.length() > other.length()

    def __lt__(self, other):
        return self.length() < other.length()

    def normalized(self):
        if self.length() == 0:
            return Vec3(0, 0, 0)
        return self / toVec3(self.length())


def toVec2(x):
    return Vec3(x, x, 0)


def toVec3(x):
    return Vec3(x, x, x)
