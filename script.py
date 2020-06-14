from core import plugin, model

class _script(plugin._plugin):
    version = 1.1

    def install(self):
        # Register models
        model.registerModel("script","_script","_action","plugins.script.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("script","_script","_action","plugins.script.models.action")
        return True
    