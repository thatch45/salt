'''
Manage the eflow system
'''
# Import salt libs
import salt.eflow


def start():
    '''
    Execute the eflow runtime
    '''
    state = salt.eflow.EFlowState(__opts__)
    state.start_runtime()
