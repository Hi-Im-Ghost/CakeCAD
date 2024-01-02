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


# Inicjalizacja projektu
scene = scene.Scene()
commandExecutor = command.CommandExecutor(scene)

#Inicjalizacja endpointów

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
        
        commandExecutor.execute(requestCommand)
        
        encodedModel = scene.export_to_stl_base64()
        response = {"sceneModel": encodedModel}
        
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
        
class SaveProjectRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def options(self, *args):
        self.set_status(204)
        self.finish()
        
    def post(self):
        response = commandExecutor.SaveProject()
        self.write(response)
        
    
class LoadProjectRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def options(self, *args):
        self.set_status(204)
        self.finish()
        
    def post(self):
        requestData = tornado.escape.json_decode(self.request.body)
       
        #TODO: do implementacji 
        #Należy tu zresetować projekt, a nastpenie wykonać wszystkie polecenia które przyszły w requestData
        
        
        self.write(response)
        
class HelloWorldHandler(tornado.web.RequestHandler):
        
    def get(self):
        
        print("Request hello worldexecuted succesfully!")
        self.write("Hello world")
        
        
def make_app():
    return tornado.web.Application([
        (r"/select", SelectObjectRequestHandler),
        (r"/hello", HelloWorldHandler),
        (r"/project/save", SaveProjectRequestHandler),
        (r"/project/load", LoadProjectRequestHandler),
        (r"/modify/layer", ModifyLayerPropertiesRequestHandler),
        (r"/add/layer", AddLayerRequestHandler),
    ])
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Backend server started!")
    tornado.ioloop.IOLoop.current().start()
    print("Backend server closed!")