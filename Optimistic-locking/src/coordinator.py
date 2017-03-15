
import da
PatternExpr_1187 = da.pat.TuplePattern([da.pat.ConstantPattern('req_app'), da.pat.FreePattern('msg')])
PatternExpr_1211 = da.pat.TuplePattern([da.pat.ConstantPattern('req_sub'), da.pat.FreePattern('msg')])
PatternExpr_1234 = da.pat.TuplePattern([da.pat.ConstantPattern('reply_work'), da.pat.FreePattern('msg')])
PatternExpr_1257 = da.pat.TuplePattern([da.pat.ConstantPattern('reply_res'), da.pat.FreePattern('msg')])
PatternExpr_1280 = da.pat.TuplePattern([da.pat.ConstantPattern('req_sub_conflict_check'), da.pat.FreePattern('msg')])
PatternExpr_1307 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import config
import random, time
TIMEOUT = 1
MAXDBLatency = 0.1
MINDBLatency = 0.01
w = da.import_da('worker')
from message import Message

class Coordinator(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._CoordinatorReceivedEvent_0 = []
        self._CoordinatorReceivedEvent_1 = []
        self._CoordinatorReceivedEvent_2 = []
        self._CoordinatorReceivedEvent_3 = []
        self._CoordinatorReceivedEvent_4 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_0', PatternExpr_1187, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_1', PatternExpr_1211, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_2', PatternExpr_1234, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_3', PatternExpr_1257, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_4', PatternExpr_1280, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_5', PatternExpr_1307, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Coordinator_handler_1306])])

    def setup(self, config, coord_list, worker_count, data, work_list):
        self.config = config
        self.coord_list = coord_list
        self.worker_count = worker_count
        self.data = data
        self.work_list = work_list
        self.subj_attr_dict = {}
        self.res_attr_dict = {}
        self.tentative_dict = {}
        work = da.new(w.Worker, num=self.config.num_workers)
        self.work_list = list(work)
        da.setup(work, (self.coord_list, self.config.policy_file, self.data))
        da.start(work)

    def _da_run_internal(self):
        self.output('Coordinator started')
        while True:
            super()._label('_st_label_1184', block=False)
            msg = None

            def ExistentialOpExpr_1185():
                nonlocal msg
                for (_, _, (_ConstantPattern1202_, msg)) in self._CoordinatorReceivedEvent_0:
                    if (_ConstantPattern1202_ == 'req_app'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_1209():
                nonlocal msg
                for (_, _, (_ConstantPattern1225_, msg)) in self._CoordinatorReceivedEvent_1:
                    if (_ConstantPattern1225_ == 'req_sub'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_1232():
                nonlocal msg
                for (_, _, (_ConstantPattern1248_, msg)) in self._CoordinatorReceivedEvent_2:
                    if (_ConstantPattern1248_ == 'reply_work'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_1255():
                nonlocal msg
                for (_, _, (_ConstantPattern1271_, msg)) in self._CoordinatorReceivedEvent_3:
                    if (_ConstantPattern1271_ == 'reply_res'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_1278():
                nonlocal msg
                for (_, _, (_ConstantPattern1294_, msg)) in self._CoordinatorReceivedEvent_4:
                    if (_ConstantPattern1294_ == 'req_sub_conflict_check'):
                        if True:
                            return True
                return False
            _st_label_1184 = 0
            self._timer_start()
            while (_st_label_1184 == 0):
                _st_label_1184 += 1
                if ExistentialOpExpr_1185():
                    pass
                    _st_label_1184 += 1
                elif ExistentialOpExpr_1209():
                    pass
                    _st_label_1184 += 1
                elif ExistentialOpExpr_1232():
                    pass
                    _st_label_1184 += 1
                elif ExistentialOpExpr_1255():
                    pass
                    _st_label_1184 += 1
                elif ExistentialOpExpr_1278():
                    pass
                    _st_label_1184 += 1
                elif self._timer_expired:
                    pass
                    _st_label_1184 += 1
                else:
                    super()._label('_st_label_1184', block=True, timeout=(TIMEOUT * 10))
                    _st_label_1184 -= 1
            else:
                if (_st_label_1184 != 2):
                    continue
            if (_st_label_1184 != 2):
                break

    def caluculateHash(self, sub_id):
        count = 0
        for i in sub_id:
            count += ord(i)
        return count

    def sendPolicyResultToApp(self, msg):
        self.output('Coordinator: Policy result is received ,sending to App')
        self._send(('result_sub', msg), msg.get_curr_app())

    def send_query_to_resource_coordinator_for_verification(self, msg):
        self.output('Coordinator: Check with Resource Coordinator for conflict')
        self._send(('req_sub_conflict_check', msg), self.coord_list[(self.caluculateHash(msg.res_id) % len(self.coord_list))])

    def send_response_to_subject_coordinator_after_verification(self, msg):
        self.output('send cached updates and verified resource attributes')
        self._send(('reply_res', msg), self.coord_list[(self.caluculateHash(msg.subj_id) % len(self.coord_list))])

    def populate_tentative_subj_updates_in_msg(self, msg):
        if (msg.subj_id in self.subj_attr_dict):
            msg.tent_attr.set_sub_attr(self.subj_attr_dict[msg.subj_id])
        if ((msg.subj_id in self.tentative_dict) and (len(self.tentative_dict[msg.subj_id]) > 0)):
            self.tentative_dict[msg.subj_id][(- 1)][1].append(msg.subj_id)

    def populate_tentative_res_updates_in_msg(self, msg):
        self.output('Coordinator: in populate_tentative_res_updates_in_msg self.res_attr_dict,', self.res_attr_dict, self)
        if (msg.subj_id in self.res_attr_dict):
            msg.tent_attr.set_res_attr(self.res_attr_dict[msg.res_id])

    def restart_policy_evauation_request(self, msg):
        self.output('Coordinator: restarting conflicting request for msg id::', msg.MsgId)
        msg.generateTimeStamp()
        msg.reset_attr_objects()
        self._send(('req_app', msg), self.coord_list[(self.caluculateHash(msg.subj_id) % len(self.coord_list))])

    def check_conflicts_on_subject_coordinator(self, msg):
        self.output('Coordinator: check_conflicts_on_subject_coordinator')
        if (msg.subj_id in self.subj_attr_dict):
            tentative_attr_list = self.subj_attr_dict[msg.subj_id]
            for (k, v) in msg.worker_attr.get_read_attr_sub().items():
                print('check_conflicts_on_subject_coordinator', k, v, msg.timeStamp)
                if ((k in tentative_attr_list) and (tentative_attr_list[k][1] > msg.timeStamp)):
                    print('Conflict detected at subject coordinator for msg id::', msg.MsgId)
                    self.restart_policy_evauation_request(msg)
                    return True
        return False

    def check_conflicts_on_resource_coordinator(self, msg):
        self.output('Coordinator: check_conflicts_on_resource_coordinator')
        if (msg.res_id in self.res_attr_dict):
            tentative_attr_list = self.res_attr_dict[msg.res_id]
            for (k, v) in msg.worker_attr.get_read_attr_res().items():
                print('check_conflicts_on_resource_coordinator', k, v, msg.timeStamp)
                if ((k in tentative_attr_list) and (tentative_attr_list[k][1] > msg.timeStamp)):
                    print('Conflict detected at resource for msg id::', msg.MsgId)
                    self.restart_policy_evauation_request(msg)
                    return True
        return False

    def update_attribute_on_resource_coordinator(self, msg):
        self.output('update_attribute_on_resource_coordinator entry', msg.worker_attr.get_updated_attr_res())
        if (not (msg.res_id in self.res_attr_dict)):
            self.res_attr_dict[msg.res_id] = dict()
        for (k, v) in msg.worker_attr.get_updated_attr_res().items():
            clk = time.time()
            self.res_attr_dict[msg.res_id][k] = (v, clk)
        print('update_attribute_on_resource_coordinator exit', self.res_attr_dict)

    def check_conflict_and_restart_request(self, msg, tentative_attr_list):
        self.output('Coordinator: check_conflict_and_restart_request')
        tentative_attr = msg.worker_attr.get_read_attr_sub()
        for attr in tentative_attr_list:
            if (attr in tentative_attr):
                print('Msg id', msg.MsgId, 'got the conflict')
                self.restart_policy_evauation_request(msg)
                break

    def removeTentativeAttributes(self, msg, tentative_attr_list):
        self.output('Coordinator: removeTentativeAttributes')
        for attr in tentative_attr_list:
            if (attr in self.subj_attr_dict):
                del self.subj_attr_dict[attr]

    def removeEntryFromTentativeList(self, msg, is_conflicted):
        self.output('Coordinator: removeEntryFromTentativeList')
        i = 0
        j = 0
        print('tentative_dict is:', self.tentative_dict)
        if (msg.subj_id in self.tentative_dict):
            tentative_list = self.tentative_dict[msg.subj_id]
            while (i < len(tentative_list)):
                if ((len(tentative_list[i]) > 0) and (tentative_list[i][1][0] == msg.MsgId)):
                    print('Found msg with ', msg.MsgId, 'as creator of tentative updates')
                    self.removeTentativeAttributes(msg, tentative_list[i][0][0])
                    self.tentative_dict[msg.subj_id][i][1].pop(0)
                    if is_conflicted:
                        self.restart_policy_evauation_request(msg)
                        self.tentative_dict[msg.subj_id][i][0][1] = False
                    return
                i = (i + 1)
            i = 0
            while (i < len(tentative_list)):
                while ((len(tentative_list[i]) > 0) and (j < len(tentative_list[i][1]))):
                    if (tentative_list[i][1][j] == msg.MsgId):
                        if is_conflicted:
                            self.restart_policy_evauation_request(msg)
                        elif (tentative_list[i][0][1] == False):
                            self.check_conflict_and_restart_request(msg, tentative_list[i][0][0])
                        self.tentative_dict[msg.subj_id][i][1].pop(j)
                        if (len(self.tentative_dict[msg.subj_id][i][1]) == 0):
                            self.tentative_dict[msg.subj_id].pop(i)
                        return
                    j = (j + 1)
                i = (i + 1)

    def populate_subject_tentative_updates_in_coordinator(self, msg):
        self.output('Coordinator: populate_subject_tentative_updates_in_coordinator')
        updated_attr_sub = msg.worker_attr.get_updated_attr_sub()
        print('updated_attr_sub', updated_attr_sub)
        if (len(updated_attr_sub) > 0):
            attr = list()
            req = list()
            req.append(msg.MsgId)
            if (not (msg.subj_id in self.subj_attr_dict)):
                self.subj_attr_dict[msg.subj_id] = dict()
            if (not (msg.subj_id in self.tentative_dict)):
                self.tentative_dict[msg.subj_id] = list()
            for (k, v) in msg.worker_attr.get_updated_attr_sub().items():
                clk = time.time()
                self.subj_attr_dict[msg.subj_id][k] = (v, clk)
                attr.append(k)
            t1 = (attr, True)
            t2 = (t1, req)
            self.tentative_dict[msg.subj_id].append(t2)

    def handleSubjectRequest(self, msg):
        self.output('Coordinator: handleSubjectRequest: piggyback tentative updates to msg')
        self.populate_tentative_subj_updates_in_msg(msg)
        self._send(('req_sub', msg), self.coord_list[(self.caluculateHash(msg.res_id) % len(self.coord_list))])

    def handleResourceRequest(self, msg):
        self.output('Coordinator: handleResourceRequest')
        self.populate_tentative_res_updates_in_msg(msg)
        msg.curr_worker = self.work_list[(self.worker_count % self.config.num_workers)]
        self._send(('req_res', msg), msg.curr_worker)
        self.worker_count += 1
        print('Work sent to worker')

    def handleResourceResponse(self, msg):
        self.output('Coordinator: handleResourceResponse')
        if (msg.get_result() == False):
            x = random.uniform(MINDBLatency, MAXDBLatency)
            time.sleep(x)
            self._send(('req_db_write', msg), self.data)
            msg.set_result(True)
            self.sendPolicyResultToApp(msg)
            self.removeEntryFromTentativeList(msg, False)
        else:
            print('restarting conflicting request for msg id::', msg.MsgId)
            self.removeEntryFromTentativeList(msg, True)

    def handleWorkerResponse(self, msg):
        self.output('Coordinator: handleWorkerResponse')
        if (msg.result == False):
            self.sendPolicyResultToApp(msg)
        elif (self.check_conflicts_on_subject_coordinator(msg) == False):
            self.output('Coordinator: store tentative updates to tentative list ')
            self.populate_subject_tentative_updates_in_coordinator(msg)
            self.send_query_to_resource_coordinator_for_verification(msg)

    def handleConflictCheckOnResource(self, msg):
        self.output('Coordinator: handleConflictCheckOnResource')
        result = self.check_conflicts_on_resource_coordinator(msg)
        if (result == False):
            self.update_attribute_on_resource_coordinator(msg)
        msg.set_result(result)
        self.send_response_to_subject_coordinator_after_verification(msg)

    def _Coordinator_handler_1306(self, a, b):
        if (a == 'req_app'):
            self.handleSubjectRequest(b)
        elif (a == 'req_sub'):
            self.handleResourceRequest(b)
        elif (a == 'reply_work'):
            self.handleWorkerResponse(b)
        elif (a == 'reply_res'):
            self.handleResourceResponse(b)
        elif (a == 'req_sub_conflict_check'):
            self.handleConflictCheckOnResource(b)
    _Coordinator_handler_1306._labels = None
    _Coordinator_handler_1306._notlabels = None
