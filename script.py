from core import plugin, model

import jimi

class _script(plugin._plugin):
    version = 4.0

    def install(self):
        # Register models
        model.registerModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True
    
    def upgrade(self,LatestPluginVersion):
        if self.version < 4.0:
            from plugins.script.models import action
            classes = jimi.db.getClassByName("_scriptBlock",None)
            if len(classes) == 1:
                scriptBlocks = action._scriptBlock().getAsClass(query={ "classID" : classes[0]["_id"] })
                for scriptBlock in scriptBlocks:
                    scriptBlock.scriptBlock = scriptBlock.scriptBlock.replace("def run(data):\r\n","def run(data):\r\n\tdata = data[\"flowData\"]\r\n").replace("def run(data):\n","def run(data):\n\tdata = data[\"flowData\"]\n")
                    scriptBlock.update(["scriptBlock"])
                
