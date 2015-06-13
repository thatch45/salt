'''
The eflow system allows for advanced event tracking and reactions
'''
# Needed:
# Use a top file to load sls files locally
# use the existing state system to compile a low state
# Create a new state runtime to run the low state flow programming style
# Create the eflow plugin system

# Import python libs
import time
import logging
import traceback

# Import Salt libs
import salt.state
from salt.exceptions import SaltRenderError

log = logging.getLogger(__name__)


class EFlowState(salt.state.HighState):
    '''
    Compile the eflow state and manage it in the eflow runtime
    '''
    def __init__(self, opts):
        opts['file_roots'] = opts['eflow_roots']
        self.opts = opts
        salt.state.HighState.__init__(self, self.opts, loader='eflow')
        self.state.inject_globals = {'__reg__': {}}
        self.event = salt.utils.event.get_master_event(
                self.opts,
                self.opts['sock_dir'])

    def start_runtime(self):
        '''
        Start the system!
        '''
        chunks = self.get_chunks()
        while True:
            try:
                print('call the runtime')
                self.call_runtime(chunks)
            except Exception:
                time.sleep(self.opts['eflow_interval'])


    def get_chunks(self, exclude=None, whitelist=None):
        '''
        Compile the top file and enter the eflow runtime!
        '''
        ret = {}
        err = []
        try:
            top = self.get_top()
        except SaltRenderError as err:
            return ret
        except Exception:
            trb = traceback.format_exc()
            err.append(trb)
            return err
        err += self.verify_tops(top)
        matches = self.top_matches(top)
        if not matches:
            msg = 'No Top file found!'
            raise SaltRenderError(msg)
        matches = self.matches_whitelist(matches, whitelist)
        high, errors = self.render_highstate(matches)
        if exclude:
            if isinstance(exclude, str):
                exclude = exclude.split(',')
            if '__exclude__' in high:
                high['__exclude__'].extend(exclude)
            else:
                high['__exclude__'] = exclude
            err += errors
        high, ext_errors = self.state.reconcile_extend(high)
        err += ext_errors
        err += self.state.verify_high(high)
        if err:
            raise SaltRenderError(err)
        return self.state.compile_high_data(high)

    def get_events(self):
        '''
        iterate over the available events and return a list of events
        '''
        ret = []
        while True:
            event = self.event.get_event(wait=1)
            if event is None:
                return ret
            ret.append(event)

    def call_runtime(self, chunks):
        '''
        Execute the runtime
        '''
        interval = self.opts['eflow_interval']
        while True:
            print('get events')
            events = self.get_events()
            print(events)
            if not events:
                time.sleep(interval)
            self.state.inject_globals['__events__'] = events
            start = time.time()
            running = self.state.call_chunks(chunks)
            print(running)
            elapsed = time.time() - start
            left = interval - elapsed
            if left > 0:
                time.sleep(left)
            self.state.reset_run_num()
