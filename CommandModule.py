import SceneModule as scene
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.DataExchange import write_stl_file, read_stl_file
from OCC.Display.SimpleGui import init_display

class Command:
    def __init__(self, commandName, jsonParams):
        self.commandName = commandName
        self.jsonParams = jsonParams      
        
        
class CommandExecutor:
    def __init__(self, sceneObject):
        self.sceneObject = sceneObject
        self.executedCommandHistory = []

    
    def execute(self, commandObject):
        #Zapis wykonanego polecenia
        self.executedCommandHistory.append(commandObject)
        
        #Wykonywanie
        if commandObject.commandName == "AddNewLayer":
            return self.__addNewLayerHandler(commandObject.jsonParams)
        elif commandObject.commandName == "SelectObject":
            return self.__selectObjectHandler(commandObject.jsonParams)
        elif commandObject.commandName == "ModifyLayerProperties":
            return self.__modifyLayerHandler(commandObject.jsonParams)
        
        
            
    def __addNewLayerHandler(self, requestData):
        #TODO: tutaj drodzy backendwcy możecie sobie wyciągnąć dane z request data i zastosować je do sceny
        #Przykład
        print("Creating new layer of type: " + requestData['type'])
        
        if requestData['type'] == "box":
            box = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
            self.sceneObject.add_object(box)
        elif requestData['type'] == "torus":
            my_torus = BRepPrimAPI_MakeTorus(20.0, 10.0).Shape()
            self.sceneObject.add_object(my_torus)
        return
            
    def __selectObjectHandler(self, requestData):
        selectedOnFronendObjectId = requestData['objectId']
        
        #TODO: Do implementacji wybieranie obiektu
        #implementacja
        
        #Tutaj zwracam na sztywno prtzykładową strukture, ale po wybraniu obiektu będzią zwracane jego właciwoci, czyli co to jest warstwa czy ozdoba oraz jej parameytry
        return {"objectType": "layer", "objectProperties":{"type":"box", "position":{"x":0, "y":0, "z":0}}}
    
    def __modifyLayerHandler(self, requestData):
        #TODO: Do implementacji
        print("Api executed modify layer command succesfully! But there is no implementation YET!")

        return 
    