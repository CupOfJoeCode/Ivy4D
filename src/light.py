import vecs


class Light:
    def __init__(self, color=vecs.Vec3(1., 1., 1.), ambient=vecs.Vec3(0., 0., 0.)):
        self.color = color
        self.ambient = ambient
