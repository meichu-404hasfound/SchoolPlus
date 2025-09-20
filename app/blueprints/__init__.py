import pkgutil
import importlib
from pathlib import Path

def register_blueprints(app):
    package = __name__
    package_path = Path(__file__).resolve().parent

    for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
        if not is_pkg or module_name == "__init__":
            continue

        module = importlib.import_module(f"{package}.{module_name}")
        
        bp_var = f"{module_name}_bp"

        if hasattr(module, bp_var):
            app.register_blueprint(getattr(module, bp_var))