import vecs


# Stores attributes of the camera
class Camera:
    def __init__(self, offset=vecs.Vec3(), rotation=vecs.Vec3(), zoom=0.4):
        self.offset = offset
        self.rotation = rotation
        self.zoom = zoom