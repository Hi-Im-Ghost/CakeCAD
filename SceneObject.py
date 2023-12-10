class SceneObject:
    _id_counter = 1000

    def __init__(self, obj_type: str, obj_shape):
        self.obj_id = SceneObject._id_counter
        SceneObject._id_counter += 1
        self.obj_type = obj_type
        self.obj_shape = obj_shape

        def __str__(self):
            return f"Object ID: {self.obj_id}, Type: {self.obj_type}"