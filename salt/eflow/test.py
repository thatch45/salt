'''
A simple test module, write things to disk to verify activity
'''
# Import python libs
import os
import yaml

# Import salt libs
import salt.utils


def save(name):
    '''
    Save the named register to /tmp/<name>
    '''
    ret = {'name': name,
           'changes': {},
           'comment': '',
           'result': True}
    fn_ = os.path.join('/tmp', name)
    with salt.utils.fopen(fn_, 'w+') as fp_:
        fp_.write(yaml.dump(__reg__))
    return ret
