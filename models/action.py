import time
from pathlib import Path
from core.models import action, webui, conduct
from core import cache, helpers

class _scriptBlock(action._action):
    scriptBlock = str()

    def __init__(self):
        self.scriptBlock = "def run(data):\n\t# Insert Code\n\treturn (True,0,data)"

    def doAction(self,data):
        scriptBlock = helpers.evalString(self.scriptBlock,{"data" : data}).replace("def run(data):","def scriptBlock{0}(data):".format(self._id.replace("-","")))
        exec(scriptBlock)
        result, rc, data = locals()["scriptBlock{0}".format(self._id.replace("-",""))](data)

        # Support for increasing event to events
        if "events" in data:
            for event in data["events"]:
                tempData = { "event" : event, "var" : data["var"], "action" : data["action"] }
                foundConducts = cache.globalCache.get("actionConductCache",self._id,getConductObject)
                if foundConducts:
                    for foundConduct in foundConducts:
                        foundConduct.triggerHandler(self._id,tempData,True)
            del data["events"]
        return {"result" : result, "rc" : rc, "msg" : "Script executed successful" }

def getConductObject(actionID,sessionData):
    return conduct._conduct().getAsClass(query={"flow.actionID" : actionID, "enabled" : True})
