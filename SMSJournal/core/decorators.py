from functools import wraps
from rest_framework.permissions import IsAuthenticated


#Decorator stolen from GrammieGram/grams/decorators.py
def define_usage(params=None, returns=None):
    def decorator(function):
        cls = function.view_class
        methods = cls.http_method_names
        perms = cls.permission_classes
        header = None
        # Is authentication required to access this view?
        if any(IsAuthenticated for cls in perms):
            header = {"Authorization": "Token String"}
        # Build a list of the valid methods, but take out "OPTIONS"
        temp = []
        for method in methods:
            if method != "options":
                temp.append(method.upper())
        methods = temp
        # Build response dictionary
        usage = {"Request Types": methods, "Headers": header, "Body": params, "Returns": returns}
        # Prevent side effects

        @wraps(function)
        def _wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        _wrapper.usage = usage
        return _wrapper
    return decorator
