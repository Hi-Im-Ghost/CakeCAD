import os
import base64

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape
from OCC.Core.gp import gp_Vec, gp_Trsf
from OCC.Extend.DataExchange import write_stl_file, read_stl_file, read_step_file, read_iges_file

from SceneObject import *

class Scene:

    def __init__(self):
        self.objects = []

    def add_object(self, obj_type: str, obj_shape):
        new_object = SceneObject(obj_type, obj_shape)
        self.objects.append(new_object)
        return new_object.obj_id

    def remove_object(self, obj_id: int):
        self.objects.remove(self.find_object(obj_id))

    def find_object(self, obj_id: int):
        for object in self.objects:
            if object.obj_id == obj_id:
                return object
        return None

    def export_model_to_stl(self, obj, path: str):
        # Zapisz do pliku STL
        write_stl_file(obj, path, mode="binary", linear_deflection=0.5, angular_deflection=0.3)
    def export_scene_to_stl(self, path: str):
        # deklaracja pustego obiektu
        compound = TopoDS_Compound()
        BRep_Builder().MakeCompound(compound)

        # dodaj wszystkie obiekty na scenie
        for obj in self.objects:
            BRep_Builder().Add(compound, obj.obj_shape)

        # Zapisz do pliku STL
        write_stl_file(compound, path, mode="binary", linear_deflection=0.5, angular_deflection=0.3)

    def export_to_stl_base64(self):
        path = "assets/models/tmp.stl"
        compound = TopoDS_Compound()
        BRep_Builder().MakeCompound(compound)

        # dodaj wszystkie obiekty na scenie
        for obj in self.objects:
            BRep_Builder().Add(compound, obj.obj_shape)

        # Zapisz do pliku STL
        write_stl_file(compound, path, mode="binary", linear_deflection=0.5, angular_deflection=0.3)

        file_text = open(path, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read).decode('ascii')
        return file_encode

    def import_model(self, obj_type: str, file_path: str, file_format: str, x=0, y=0, z=0):
        if file_format.lower() == "stl":
            shape = read_stl_file(file_path)
        elif file_format.lower() == "step":
            shape = read_step_file(file_path)
        elif file_format.lower() == "iges":
            shape = read_iges_file(file_path)
        else:
            raise ValueError("Unsupported file format")

        self.translate_object(self.add_object(obj_type, shape), x, y, z)

    def translate_object(self, obj_id: int, x, y, z):
        translation_vector = gp_Vec(x, y, z)
        trsf = gp_Trsf()
        trsf.SetTranslation(translation_vector)
        location = TopLoc_Location(trsf)
        obj = self.find_object(obj_id)
        if obj is not None:
            shape = obj.obj_shape
            shape.Move(location)
        else:
            print(f"Object with id {obj_id} not found in the scene.")