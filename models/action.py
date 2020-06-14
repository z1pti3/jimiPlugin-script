from core.models import action

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

from core import cache
from core.models import conduct

def getConductObject(actionID,sessionData):
    return conduct._conduct().getAsClass(query={"flow.actionID" : actionID, "enabled" : True})