
import da
PatternExpr_455 = da.pat.TuplePattern([da.pat.ConstantPattern('result'), da.pat.FreePattern('req')])
PatternExpr_488 = da.pat.TuplePattern([da.pat.ConstantPattern('result'), da.pat.FreePattern('req')])
PatternExpr_522 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import json, sys, os, time
import request
sys.path.insert(0, '../config')
import config
import staticAnalysis
TIMEOUT = 1

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ClientReceivedEvent_0 = []
        self._ClientReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_455, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_488, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_522, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_521])])

    def setup(self, config, coord_list, counter):
        self.config = config
        self.coord_list = coord_list
        self.counter = counter
        self.req_queue = []
        self.output('Client:  Client Setup in done')
        pass

    def _da_run_internal(self):
        self.output('Client:  Client started')
        try:
            with open(self.config.conf_file, encoding='utf-8') as conf:
                conf_data = json.loads(conf.read())
                num_operations = len(conf_data['operations'])
                sta = staticAnalysis.StaticAnalysis(self.config.attr_file, self.coord_list)
                time.sleep(1)
                while (self.counter < num_operations):
                    self.output('Client: Client fetches next policy evaluation request #:', self.counter)
                    req = self.readNextOperation(conf_data)
                    self.counter = (self.counter + self.config.num_client)
                    self.output('Client: Forward policy evaluation request to First Coordinator for req id', req.id)
                    self._send(('handleReq', (req, 1)), sta.coord(sta.obj(req, 1)))
                    super()._label('_st_label_452', block=False)
                    req = None

                    def ExistentialOpExpr_453():
                        nonlocal req
                        for (_, _, (_ConstantPattern469_, req)) in self._ClientReceivedEvent_0:
                            if (_ConstantPattern469_ == 'result'):
                                if True:
                                    return True
                        return False
                    _st_label_452 = 0
                    self._timer_start()
                    while (_st_label_452 == 0):
                        _st_label_452 += 1
                        if ExistentialOpExpr_453():
                            pass
                            _st_label_452 += 1
                        elif self._timer_expired:
                            pass
                            _st_label_452 += 1
                        else:
                            super()._label('_st_label_452', block=True, timeout=(TIMEOUT * 0.1))
                            _st_label_452 -= 1
                    else:
                        if (_st_label_452 != 2):
                            continue
                    if (_st_label_452 != 2):
                        break
            while (len(self.req_queue) > 0):
                super()._label('_st_label_485', block=False)
                req = None

                def ExistentialOpExpr_486():
                    nonlocal req
                    for (_, _, (_ConstantPattern502_, req)) in self._ClientReceivedEvent_1:
                        if (_ConstantPattern502_ == 'result'):
                            if True:
                                return True
                    return False
                _st_label_485 = 0
                self._timer_start()
                while (_st_label_485 == 0):
                    _st_label_485 += 1
                    if ExistentialOpExpr_486():
                        pass
                        _st_label_485 += 1
                    elif self._timer_expired:
                        pass
                        _st_label_485 += 1
                    else:
                        super()._label('_st_label_485', block=True, timeout=(TIMEOUT * 1))
                        _st_label_485 -= 1
                else:
                    if (_st_label_485 != 2):
                        continue
                if (_st_label_485 != 2):
                    break
            self.output('Client: All Evaluation requests for this Client are over')
        except ImportError:
            self.output('Client: Error in read file', sep='|')

    def reqFactory(self, type):
        if (type == None):
            req = request.HistoryRequest()
        else:
            req = request.DrmRequest(type)
        return req

    def readNextOperation(self, conf_data):
        self.output('Client: Fetching Next Request to evaluate policy ,from Config')
        oper = conf_data['operations'][self.counter]
        req = self.reqFactory(oper['op'][2].get('type'))
        req.action = oper['op'][0].get('action')
        req.subj_id = oper['op'][1].get('sub-id')
        req.position = oper['op'][1].get('position')
        req.res_id = oper['op'][2].get('id')
        req.req_type = oper['op'][3].get('req_type')
        req.generateReqId(self.counter)
        print('req created with id', req.id)
        req.set_curr_app(self.id)
        self.req_queue.append(req.id)
        self.output('Client: A new Evaluation Request is created with req id: ', req.id)
        return req

    def handle_policy_evaluation_result(self, req):
        if (req.id in self.req_queue):
            print('Got policy evaluation result as', req.result, 'for req with req id: ', req.id)
            self.req_queue.remove(req.id)
        else:
            print('Got some random message with req_id ', req.id)

    def _Client_handler_521(self, a, b):
        self.output('Client: received policy evaluation')
        if (a == 'result'):
            self.handle_policy_evaluation_result(b)
    _Client_handler_521._labels = None
    _Client_handler_521._notlabels = None
