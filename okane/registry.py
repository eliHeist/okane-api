import importlib
import pkgutil
from django.urls import path

class URLRegistry:
    def __init__(self):
        self.patterns = []

    def route(self, url_string, name=None):
        def decorator(view_func):
            actual_view = view_func
            
            # Handle class-based views
            if hasattr(view_func, 'as_view'):
                actual_view = view_func.as_view()
            # Async function-based views and async CBVs are registered as-is
            # (Django's path() handles them correctly)
            
            self.patterns.append(
                path(url_string, actual_view, name=name or view_func.__name__)
            )
            return view_func
        return decorator
    
    def discover(self, package_name):
        """
        Dynamically imports all modules in a package using the dotted path.
        """
        package = importlib.import_module(package_name)
        # pkgutil.walk_packages is Docker-friendly as it uses Python's import system
        for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_module_name = f"{package_name}.{module_name}"
            importlib.import_module(full_module_name)

# Initialize the registry instance
app_urls = URLRegistry()