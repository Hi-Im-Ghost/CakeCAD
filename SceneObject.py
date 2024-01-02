from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon, \
    BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Vec

class SceneObject:
    _id_counter = 1000

    def __init__(self, obj_type: str = "None", obj_shape=None):
        self.obj_id = SceneObject._id_counter
        SceneObject._id_counter += 1
        self.obj_type = obj_type
        self.obj_shape = obj_shape

    def __str__(self):
            return f"Object ID: {self.obj_id}, Type: {self.obj_type}"

    @staticmethod
    def create_custom_shape(points, height):
        # Tworzenie linii na podstawie punktow (ostatnia krawedz laczy ostatni punkt z pierwszym)
        wire_builder = BRepBuilderAPI_MakeWire()
        for i, point in enumerate(points):
            if i == len(points) - 1:
                edge = BRepBuilderAPI_MakeEdge(gp_Pnt(*point), gp_Pnt(*points[0])).Edge()
            else:
                edge = BRepBuilderAPI_MakeEdge(gp_Pnt(*point), gp_Pnt(*points[i + 1])).Edge()
            wire_builder.Add(edge)

        # Tworzenie powierzchni na podstawie linii
        wire = wire_builder.Wire()
        face_builder = BRepBuilderAPI_MakeFace(wire)
        face = face_builder.Face()
        # Wyciaganie w gore o zadana wysokosc
        vec = gp_Vec(0, 0, height)
        prism = BRepPrimAPI_MakePrism(face, vec).Shape()

        return prism