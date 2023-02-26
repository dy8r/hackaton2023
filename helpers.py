from datetime import datetime


def val_from_query(query):
    index = query.index('VALUES')
    new_query = query[:index] + 'VALUES ('
    # breakpoint()
    params = query[index+7:].replace(')', '').replace('(', '')
    val = tuple(params.split(','))
    param_num = len(val)
    param_st = ''
    for i in range(param_num):
        param_st += '%s,'
    param_st = param_st[:-1]
    query = new_query + param_st + ')'
    return query, val