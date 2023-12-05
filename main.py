import os
import SceneModule as scene
import CommandModule as command
import tornado.ioloop
import tornado.web

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.DataExchange import write_stl_file, read_stl_file
from OCC.Display.SimpleGui import init_display

# Funkcja do wyswietlania pozycji kursora i wyswietlania nazwy zaznaczonego ksztaltu
def print_xy_click(shp, *kwargs):
    for shape in shp:
        print("Shape selected: ", shape)
    print(kwargs)

# Inicjalizacja wyświetlania
#display, start_display, add_menu, add_function_to_menu = init_display()

# Tworzenie obiektów
#box = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
#my_torus = BRepPrimAPI_MakeTorus(20.0, 10.0).Shape()

# Tworzenie sceny
scene = scene.Scene()
commandExecutor = command.CommandExecutor(scene)


# Dodanie obiektow do sceny
#scene.add_object(box)
#scene.add_object(my_torus)

# Usun box z sceny
# scene.remove_object(box)

# Przesun obiekt
#scene.translate_object(box, 100, 20, 35)
#scene.translate_object(my_torus, -100, 20, 35)

# Wczytaj model
#scene.import_model("assets/models/cake.iges","iges",0,50,100)

# sciezka do pliku sceny
stl_output = "assets/models/scene.stl"

# Zapisanie sceny do pliku
scene.export_to_stl(stl_output)

# Wczytanie sceny
stl_scene = read_stl_file(stl_output)


class SelectObjectRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def options(self, *args):
        self.set_status(204)
        self.finish()
        
    def post(self):
        requestData = tornado.escape.json_decode(self.request.body)
        
        requestCommand = command.Command("SelectObject", requestData)
        response = commandExecutor.execute(requestCommand)
        
        print("Request " + requestCommand.commandName + "executed succesfully!")
        self.write(response)
        
class ModifyLayerPropertiesRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def options(self, *args):
        self.set_status(204)
        self.finish()
        
    def post(self):
        requestData = tornado.escape.json_decode(self.request.body)
        
        requestCommand = command.Command("ModifyLayerProperties", requestData)
        response = commandExecutor.execute(requestCommand)
        
        print("Request " + requestCommand.commandName + "executed succesfully!")
        self.write(response)
        
        
        
class AddLayerRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def options(self, *args):
        self.set_status(204)
        self.finish()
        
    def post(self):
        requestData = tornado.escape.json_decode(self.request.body)
        
        requestCommand = command.Command("AddNewLayer", requestData)
        commandExecutor.execute(requestCommand)
    
        encodedModel = scene.export_to_stl_base64()
        response = {"sceneModel": encodedModel}
        
        print("Request " + requestCommand.commandName + "executed succesfully!")
        self.write(response)
        
        
        
        
def make_app():
    return tornado.web.Application([
        (r"/select", SelectObjectRequestHandler),
        (r"/modify/layer", ModifyLayerPropertiesRequestHandler),
        (r"/add/layer", AddLayerRequestHandler),
    ])
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()