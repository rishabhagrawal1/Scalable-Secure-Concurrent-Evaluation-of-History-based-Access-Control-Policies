
import da
PatternExpr_435 = da.pat.TuplePattern([da.pat.ConstantPattern('result_sub'), da.pat.FreePattern('msg')])
PatternExpr_469 = da.pat.TuplePattern([da.pat.ConstantPattern('result_sub'), da.pat.FreePattern('msg')])
PatternExpr_503 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import json
import message
import time
TIMEOUT = 1

class Application(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ApplicationReceivedEvent_0 = []
        self._ApplicationReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ApplicationReceivedEvent_0', PatternExpr_435, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ApplicationReceivedEvent_1', PatternExpr_469, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ApplicationReceivedEvent_2', PatternExpr_503, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Application_handler_502])])

    def setup(self, coord_list, conf_file, num_applications, counter):
        self.coord_list = coord_list
        self.conf_file = conf_file
        self.num_applications = num_applications
        self.counter = counter
        self.msg_queue = []
        self.output('Application:  Application Setup in done')
        pass

    def _da_run_internal(self):
        self.output('Application:  Application started')
        try:
            with open(self.conf_file, encoding='utf-8') as conf:
                conf_data = json.loads(conf.read())
                num_operations = len(conf_data['operations'])
                time.sleep(1)
                while (self.counter < num_operations):
                    self.output('Application: Application fetches next policy evaluation request #:', self.counter)
                    msg = self.readNextOperation(conf_data)
                    self.counter = (self.counter + self.num_applications)
                    self.output('Application coord list is this', type(msg))
                    self._send(('req_app', msg), self.coord_list[(self.caluculateHash(msg.subj_id) % len(self.coord_list))])
                    self.output('Application: Application: Forward policy evaluation request to Subject Co ordinator')
                    super()._label('handle_policy_evaluation_results', block=False)
                    msg = None

                    def ExistentialOpExpr_433():
                        nonlocal msg
                        for (_, _, (_ConstantPattern449_, msg)) in self._ApplicationReceivedEvent_0:
                            if (_ConstantPattern449_ == 'result_sub'):
                                if True:
                                    return True
                        return False
                    _st_label_432 = 0
                    self._timer_start()
                    while (_st_label_432 == 0):
                        _st_label_432 += 1
                        if ExistentialOpExpr_433():
                            self.output('Application: Application: Application: Policy Evaluation result received')
                            _st_label_432 += 1
                        elif self._timer_expired:
                            pass
                            _st_label_432 += 1
                        else:
                            super()._label('handle_policy_evaluation_results', block=True, timeout=(TIMEOUT * 0.1))
                            _st_label_432 -= 1
                    else:
                        if (_st_label_432 != 2):
                            continue
                    if (_st_label_432 != 2):
                        break
            while (len(self.msg_queue) > 0):
                super()._label('_st_label_466', block=False)
                msg = None

                def ExistentialOpExpr_467():
                    nonlocal msg
                    for (_, _, (_ConstantPattern483_, msg)) in self._ApplicationReceivedEvent_1:
                        if (_ConstantPattern483_ == 'result_sub'):
                            if True:
                                return True
                    return False
                _st_label_466 = 0
                self._timer_start()
                while (_st_label_466 == 0):
                    _st_label_466 += 1
                    if ExistentialOpExpr_467():
                        pass
                        _st_label_466 += 1
                    elif self._timer_expired:
                        pass
                        _st_label_466 += 1
                    else:
                        super()._label('_st_label_466', block=True, timeout=(TIMEOUT * 1))
                        _st_label_466 -= 1
                else:
                    if (_st_label_466 != 2):
                        continue
                if (_st_label_466 != 2):
                    break
            self.output('Application: All Evaluation requests for this Application are over')
        except ImportError:
            self.output('Application: Error in read file', sep='|')

    def caluculateHash(self, subj_id):
        count = 0
        for i in subj_id:
            count += ord(i)
        return count

    def msgFactory(self, type):
        if (type == None):
            msg = message.HistoryMessage()
        else:
            msg = message.DrmMessage(type)
        return msg

    def readNextOperation(self, conf_data):
        self.output('Application: Fetching Next Request to evaluate policy ,from Config')
        oper = conf_data['operations'][self.counter]
        msg = self.msgFactory(oper['op'][2].get('type'))
        msg.action = oper['op'][0].get('action')
        msg.subj_id = oper['op'][1].get('sub-id')
        msg.position = oper['op'][1].get('position')
        msg.res_id = oper['op'][2].get('id')
        msg.generateMsgId(self.counter)
        msg.set_curr_app(self.id)
        self.msg_queue.append(msg.MsgId)
        self.output('Application: A new Evaluation Request is created with msgId: ', msg.MsgId)
        return msg

    def handle_policy_evaluation_result(self, msg):
        if (msg.MsgId in self.msg_queue):
            print('Got policy evaluation result for msg with msg id: ', msg.MsgId)
            print('evaluation result is: ', msg.result)
            self.msg_queue.remove(msg.MsgId)
        else:
            print('Got some random message')

    def _Application_handler_502(self, a, b):
        if (a == 'result_sub'):
            self.handle_policy_evaluation_result(b)
    _Application_handler_502._labels = None
    _Application_handler_502._notlabels = None
