import time
from pathlib import Path
from core.models import action, webui, conduct
from core import cache, helpers

class _script(action._action):
    scriptName = str()

    def __init__(self):
        cache.globalCache.newCache("actionConductCache")

    def run(self,data,persistentData,actionResult):
        mod = __import__("plugins.script.scripts.{0}".format(self.scriptName), fromlist=["run"])
        actionResult["result"], actionResult["rc"], data = mod.run(data)
        # Support for increasing event to events
        if "events" in data:
            for event in data["events"]:
                tempData = { "event" : event, "var" : data["var"], "action" : data["action"] }
                foundConducts = cache.globalCache.get("actionConductCache",self._id,getConductObject)
                if foundConducts:
                    for foundConduct in foundConducts:
                        foundConduct.triggerHandler(self._id,tempData,True)
            del data["events"]
        return actionResult

# Planned to replace script in the near future
class _scriptBlock(action._action):
    class _properties(webui._properties):
       def generate(self,classObject):
           formData = []
           formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
           formData.append({"type" : "script", "schemaitem" : "scriptBlock", "textbox" : classObject.scriptBlock})
           return formData

    scriptBlock = str()

    def __init__(self):
        self.scriptBlock = "def run(data):\n\t# Insert Code\n\treturn (True,0,data)"

    def run(self,data,persistentData,actionResult):
        scriptBlock = helpers.evalString(self.scriptBlock,{"data" : data}).replace("def run(data):","def {0}(data):".format(self.name.replace(" ","")))
        exec(scriptBlock)
        actionResult["result"], actionResult["rc"], data = locals()[self.name.replace(" ","")](data)

        # Support for increasing event to events
        if "events" in data:
            for event in data["events"]:
                tempData = { "event" : event, "var" : data["var"], "action" : data["action"] }
                foundConducts = cache.globalCache.get("actionConductCache",self._id,getConductObject)
                if foundConducts:
                    for foundConduct in foundConducts:
                        foundConduct.triggerHandler(self._id,tempData,True)
            del data["events"]
        return actionResult

def getConductObject(actionID,sessionData):
    return conduct._conduct().getAsClass(query={"flow.actionID" : actionID, "enabled" : True})