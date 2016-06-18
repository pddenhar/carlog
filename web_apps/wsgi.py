# Import flask and template operators
from flask import Flask, render_template, g
import jinja2
import pkgutil
import importlib
import os

class WebApp(Flask):
    def __init__(self, implementation):
        Flask.__init__(self, __name__, static_url_path="/common_static")

        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter = ".")
        ])
        sidebar_links = []

        #Custom module importing
        #Import all controller modules in mod_* packages
        #if the define a "mod" attribute
        def import_dir(path, prefix):
            for _, package, _ in pkgutil.walk_packages([path]):
                if package[:4] == "mod_" or package == implementation:
                    for _, module, _ in pkgutil.iter_modules([path + package]):
                        if module == "controller":
                            controller = importlib.import_module(prefix + "." + package + "." + module)
                            if hasattr(controller, "mod"):
                                self.register_blueprint(controller.mod)
                                print "Registering:", prefix + "." + package + "." + module


        path = os.path.dirname(__file__) + "/"
        import_dir(path, "web_apps")
        import_dir(path + implementation + "/", "web_apps." + implementation)

        # HTTP error handling
        @self.errorhandler(404)
        def not_found(error):
          return render_template('404.html'), 404

        # Make sure that the database is closed
        @self.teardown_appcontext
        def close_db(error):
          """Closes the database again at the end of the request."""
          if hasattr(g, 'cursor'):
            g.cursor.close()
          if hasattr(g, 'database'):
            g.database.close()
          if hasattr(g, 'clientsDB'):
            g.clientsDB.close()

            """ End Init """

    def create_global_jinja_loader(self):
        return self.jinja_loader
    
    def register_blueprint(self, bp):
        Flask.register_blueprint(self, bp)
        self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader