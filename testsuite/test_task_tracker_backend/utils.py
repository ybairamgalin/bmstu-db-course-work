def gen_query(handler, params):
    if not params:
        return handler
    return handler + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
