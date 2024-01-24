import SceneModule as scene
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeCylinder

class Command:
    def __init__(self, commandName, jsonParams):
        self.commandName = commandName
        self.jsonParams = jsonParams      
    
    def asJson(self):
        return {"commandName": self.commandName, "params": self.jsonParams }
        
        
class CommandExecutor:
    def __init__(self, sceneObject):
        self.sceneObject = sceneObject
        self.executedCommandHistory = []

    
    def execute(self, commandObject):
        #Zapis wykonanego polecenia
        self.executedCommandHistory.append(commandObject)
        print ("Executing command " + commandObject.commandName)
        
        #Wykonywanie 
        if commandObject.commandName == "AddNewLayer":
            return self.__addNewLayerHandler(commandObject.jsonParams)
        elif commandObject.commandName == "SelectObject":
            return self.__selectObjectHandler(commandObject.jsonParams)
        elif commandObject.commandName == "ModifyLayerProperties":
            return self.__modifyLayerHandler(commandObject.jsonParams)
        elif commandObject.commandName == "RoundLayerCommand":
            return self.__roundLayerHandler(commandObject.jsonParams)
        elif commandObject.commandName == "CreateFromPointsCommand":
            return self.__createFromPointsHandler(commandObject.jsonParams)
        
        
    def __createFromPointsHandler(self, requestData):
        
        
        points = []
        height = 10
        
        for point in requestData['points']:
            splited = point.replace(" ", "").split(",")
            x = float(splited[0])
            y = float(splited[1])
            z = float(splited[2])
            points.append((x,y,z))
            

        
        id = self.sceneObject.add_object_from_points("Custom", points, height )

        return id
    
    def __roundLayerHandler(self, requestData):
        self.sceneObject.fillet_edges(requestData['id'], 0.9)
            
        return requestData['id']
            
    def __addNewLayerHandler(self, requestData):
        #TODO: tutaj drodzy backendwcy możecie sobie wyciągnąć dane z request data i zastosować je do sceny
        #Przykład
        print("Creating new layer of type: " + requestData['type'])
        id = -1
        if requestData['type'] == "box":
            box = BRepPrimAPI_MakeBox(10, 10, 5).Shape()
            id = self.sceneObject.add_object(requestData['type'], box)
            
        elif requestData['type'] == "torus":
            my_torus = BRepPrimAPI_MakeTorus(20.0, 5.0).Shape()
            id = self.sceneObject.add_object(requestData['type'], my_torus)
            
        elif requestData['type'] == "cylinder":
            my_cyulinder = BRepPrimAPI_MakeCylinder(10.0, 5.0).Shape()
            id = self.sceneObject.add_object(requestData['type'], my_cyulinder)
            
        return id
            
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
    
    def SaveProject(self):
        jsonCommandList =  []
        for command in self.executedCommandHistory:
            jsonCommandList.append(command.asJson())
        
        return {"commands": jsonCommandList}
    