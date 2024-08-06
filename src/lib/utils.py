import sys


def debug(ev, filt):
    for k in dir(ev):
        if filt in k: print(f"{k}: {getattr(ev, k)}")

def stacktrace(func):
    def wrapper(*a, **kw):
        try:
            func(*a, **kw)
        except Exception as e:
            sys.print_exception(e)
    return wrapper

def reload(mod):
    import sys
    mod_name = mod.__name__
    del sys.modules[mod_name]
    exec("import {}".format(mod_name))
