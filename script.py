from core import plugin, model

class _script(plugin._plugin):
    version = 3.0

    def install(self):
        # Register models
        model.registerModel("script","_script","_action","plugins.script.models.action")
        model.registerModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("script","_script","_action","plugins.script.models.action")
        model.deregisterModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
        return True
    
    def upgrade(self,LatestPluginVersion):
        if self.version < 1.2:
            model.registerModel("scriptBlock","_scriptBlock","_action","plugins.script.models.action")
