from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon, \
    BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Vec


class SceneObject:
    _id_counter = 1000

    def __init__(self, obj_type: str = "None", obj_shape=None):
        self._obj_id = SceneObject._id_counter
        SceneObject._id_counter += 1
        self._obj_type = obj_type
        self._obj_shape = obj_shape

    def __str__(self):
        return f"Object ID: {self._obj_id}, Type: {self._obj_type}"

    @property
    def obj_id(self):
        return self._obj_id

    @property
    def obj_type(self):
        return self._obj_type

    @property
    def obj_shape(self):
        return self._obj_shape

    @obj_id.setter
    def obj_id(self, value_id: int):
        self._obj_id = value_id

    @obj_type.setter
    def obj_type(self, type_name: str):
        self._obj_type = type_name

    @obj_shape.setter
    def obj_shape(self, new_shape):
        self._obj_shape = new_shape

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

    @staticmethod
    def create_custom_bspline(points, height, closed=False):

        # Jeśli ma być zamknięty, dodaj punkt końcowy identyczny z punktem początkowym
        if closed:
            points.append(points[0])

        # Tablica punktów dla BSpline
        points_array = TColgp_Array1OfPnt(1, len(points))
        for i, point in enumerate(points):
            points_array.SetValue(i + 1, gp_Pnt(*point))

        # Tworzenie krzywej BSpline
        bspline_curve = GeomAPI_PointsToBSpline(points_array).Curve()

        # Tworzenie krawędzi na podstawie krzywej BSpline
        bspline_edge = BRepBuilderAPI_MakeEdge(bspline_curve).Edge()

        # Wyciaganie
        vec = gp_Vec(0, 0, height)
        prism = BRepPrimAPI_MakePrism(bspline_edge, vec).Shape()

        return prism
