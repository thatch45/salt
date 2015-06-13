'''
The functions that manage the eflow register
'''
# Import python libs
import fnmatch

__func_alias__ = {
    'set_': 'set',
}

# TODO: This is just a stub function to test the system, this will need
# to be replaced!
def set_(name, add, match):
    '''
    Add a value to the named set when the matched tag is found
    '''
    ret = {'name': name,
           'changes': {},
           'comment': '',
           'result': True}
    reg_key = '{0}_|-set'.format(name)
    if reg_key not in __reg__:
        __reg__[reg_key] = set()
    for event in __events__:
        if fnmatch.fnmatch(event['tag'], match):
            val = event['data'].get(add)
            if val is None:
                val = 'None'
            ret['changes'][add] = val
            __reg__[reg_key].add(val)
    return ret
