from core import plugin, model

class _script(plugin._plugin):
    version = 3.11

    def install(self):
        # Register models
        model.registerModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True
    
    def upgrade(self,LatestPluginVersion):
        pass
