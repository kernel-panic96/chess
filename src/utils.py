import functools

def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    return wrapper
