import os
import base64

from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.gp import gp_Vec, gp_Trsf
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Edge
from OCC.Extend.DataExchange import write_stl_file, read_stl_file, read_step_file, read_iges_file
from OCC.Extend.TopologyUtils import TopologyExplorer

from SceneObject import *


class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj_type: str = "None", obj_shape=None):
        new_object = SceneObject(obj_type, obj_shape)
        self.objects.append(new_object)
        return new_object.obj_id

    def add_object_from_points(self, obj_type: str, points, height):
        obj_shape = SceneObject.create_custom_shape(points, height)
        return self.add_object(obj_type, obj_shape)

    def add_bspline_from_points(self, obj_type: str, points, height, closed):
        obj_shape = SceneObject.create_custom_bspline(points, height, closed)
        return self.add_object(obj_type, obj_shape)

    def remove_object(self, obj_id: int):
        self.objects.remove(self.find_object(obj_id))

    def find_object(self, obj_id: int):
        for obj in self.objects:
            if obj.obj_id == obj_id:
                return obj
        return None

    def export_model_to_stl(self, obj_id, path: str):
        obj = self.find_object(obj_id)
        shape = obj.obj_shape
        # Zapisz do pliku STL
        write_stl_file(shape, path, mode="binary", linear_deflection=0.5, angular_deflection=0.3)

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
    
    
    def export_model_to_stl_base64(self, modelId):
        path = "assets/models/tmp.stl"

        self.export_model_to_stl(modelId, path)
        
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

    def fillet_edges(self, obj_id: int, radius: float):
        # Znajdz obiekt o podanym ID
        obj = self.find_object(obj_id)
        # Sprawdz czy istnieje
        if obj is not None:
            # Pobierz ksztalt
            shape = obj.obj_shape
            # Inicjacja narzedzia do zaokraglen
            fillet = BRepFilletAPI_MakeFillet(shape)
            # Iteracja po krawedziach
            for e in TopologyExplorer(shape).edges():
                try:
                    # Proba dodania zaokraglenia do krawedzi
                    fillet.Add(radius, e)
                except RuntimeError as e:
                    # Ostrzezenie w przypadku bledu
                    print(f"Warning: Error while adding fillet to edge: {e}. Skipping this edge.")

            try:
                # Zastosowanie zaokraglenia do obiektu
                obj.obj_shape = fillet.Shape()
            except RuntimeError as e:
                # Wyswietl blad jesli operacja sie nie powiodla
                print(f"Error: {e}")
                print(f"Fillet operation failed for object with id {obj_id}. Try reducing the fillet radius.")
        else:
            # Wyswietl komunikat jesli nie ma obiektu o takim id
            print(f"Object with id {obj_id} not found in the scene.")
