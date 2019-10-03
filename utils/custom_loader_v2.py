from __future__ import print_function

import __builtin__
import imp
import sys

from constants.hooks import USER_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback
from utils.instrumentation import instrument


# Replacement for __import__()
def import_hook(name, globals=None, locals=None, fromlist=None):
    parent = determine_parent(globals)
    q, tail = find_head_package(parent, name)
    m = load_tail(q, tail)
    if not fromlist:
        return q
    if hasattr(m, "__path__"):
        ensure_fromlist(m, fromlist)
    return m


def determine_parent(globals):
    if not globals or  not globals.has_key("__name__"):
        return None
    pname = globals['__name__']
    if globals.has_key("__path__"):
        parent = sys.modules[pname]
        assert globals is parent.__dict__
        return parent
    if '.' in pname:
        i = pname.rfind('.')
        pname = pname[:i]
        parent = sys.modules[pname]
        assert parent.__name__ == pname
        return parent
    return None


def find_head_package(parent, name):
    if '.' in name:
        i = name.find('.')
        head = name[:i]
        tail = name[i+1:]
    else:
        head = name
        tail = ""
    if parent:
        qname = "%s.%s" % (parent.__name__, head)
    else:
        qname = head
    q = import_module(head, qname, parent)
    if q: return q, tail
    if parent:
        qname = head
        parent = None
        q = import_module(head, qname, parent)
        if q: return q, tail
    raise ImportError("No module named " + qname)


def load_tail(q, tail):
    m = q
    while tail:
        i = tail.find('.')
        if i < 0: i = len(tail)
        head, tail = tail[:i], tail[i+1:]
        mname = "%s.%s" % (m.__name__, head)
        m = import_module(head, mname, m)
        if not m:
            raise ImportError("No module named " + mname)
    return m


def ensure_fromlist(m, fromlist, recursive=0):
    for sub in fromlist:
        if sub == "*":
            if not recursive:
                try:
                    all = m.__all__
                except AttributeError:
                    pass
                else:
                    ensure_fromlist(m, all, 1)
            continue
        if sub != "*" and not hasattr(m, sub):
            subname = "%s.%s" % (m.__name__, sub)
            submod = import_module(sub, subname, m)
            if not submod:
                raise ImportError("No module named " + subname)


def import_module(partname, fqname, parent):
    try:
        return sys.modules[fqname]
    except KeyError:
        pass
    try:
        fp, pathname, stuff = imp.find_module(partname,
                                              parent and parent.__path__)
    except ImportError:
        return None
    try:
        module = imp.load_module(fqname, fp, pathname, stuff)
        # Invoking hooking logic at time of module loading
        try:
            if module.__name__ in list(USER_CALLABLES_TO_HOOK.keys()):
                for func_string in USER_CALLABLES_TO_HOOK[module.__name__]:
                    cls = None
                    func_str = func_string
                    if func_str.find(".") != -1:
                        class_str, func_str = func_str.split(".")
                        cls = getattr(module, class_str)
                    if cls is not None:
                        func = getattr(cls, func_str)
                        setattr(cls, func_str,
                                instrument(func, start_callback, end_callback, error_callback, isMethod=True))
                    else:
                        func = getattr(module, func_str)
                        setattr(module, func_str,
                                instrument(func, start_callback, end_callback, error_callback))
        except:
            print("Error caught : {}".format(sys.exc_info()))

    finally:
        if fp: fp.close()
    if parent:
        setattr(parent, partname, module)
    return module


# Replacement for reload()
def reload_hook(module):
    name = module.__name__
    if '.' not in name:
        return import_module(name, name, None)
    i = name.rfind('.')
    pname = name[:i]
    parent = sys.modules[pname]
    return import_module(name[i+1:], name, parent)


# Save the original hooks
original_import = __builtin__.__import__
original_reload = __builtin__.reload

def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    __builtin__.__import__ = import_hook
    __builtin__.reload = reload_hook


def disable_module_hook_on_load():
    """Counter function of enable_module_hook_on_load"""
    __builtin__.__import__ = original_import
    __builtin__.reload = original_reload
