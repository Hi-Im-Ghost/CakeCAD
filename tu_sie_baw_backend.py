import os

from OCC.Core.TopoDS import TopoDS_Shape

import SceneModule as scene
import CommandModule as command
import tornado.ioloop
import tornado.web

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
from OCC.Extend.DataExchange import write_stl_file, read_stl_file
from OCC.Display.SimpleGui import init_display

from SceneObject import *

# Funkcja do wyswietlania pozycji kursora i wyswietlania nazwy zaznaczonego ksztaltu
def print_xy_click(shp, *kwargs):
    for shape in shp:
        if isinstance(shape, TopoDS_Shape):
            for obj in scene.objects:
                if obj.obj_shape.IsEqual(shape):
                    print("Object Class: ", obj.__class__.__name__)
                    print("Object ID: ", obj.obj_id)
                    print("Object Type: ", obj.obj_type)
                    print("Object Shape: ", obj.obj_shape)
                    break
        else:
            print("Not a valid shape.")

    print(kwargs)


# Inicjalizacja wyświetlania
display, start_display, add_menu, add_function_to_menu = init_display()

# Tworzenie obiektów
#box = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
#my_torus = BRepPrimAPI_MakeTorus(20.0, 10.0).Shape()

# Tworzenie sceny
scene = scene.Scene()
commandExecutor = command.CommandExecutor(scene)

# Dodanie obiektow do sceny
#scene.add_object("box", box)
#scene.add_object("torus", my_torus)
# Przykład użycia funkcji create_shape_from_points
points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
height = 4.0
scene.add_object_from_points("Custom", points, height)

print("Objects before removal:")
for obj in scene.objects:
    print(obj.obj_id)

# Usun box z sceny
#scene.remove_object(1000)



# Przesun obiekt
# scene.translate_object(1000, 100, 20, 35)
#scene.translate_object(1001, -100, 20, 35)

# Wczytaj model
#scene.import_model("cake", "assets/models/cake.iges", "iges", 0, 50, 100)

# sciezka do pliku sceny
stl_output = "assets/models/scene.stl"

# Zapisanie sceny do pliku
#scene.export_scene_to_stl(stl_output)

# Wczytanie sceny (nie dziala poprawnie poniewaz potrzebuje funkcji importu sceny)
#stl_scene = read_stl_file(stl_output)

# Wyświetlenie obiektow z listy sceny
print("Objects:")
for obj in scene.objects:
    print(obj.obj_id)
    display.DisplayShape(obj.obj_shape, update=True)

# Callback do wyświetlania pozycji kursora i wyswietlania nazwy kliknietego obiektu
display.register_select_callback(print_xy_click)

# Uruchomienie interaktywnego widoku
start_display()