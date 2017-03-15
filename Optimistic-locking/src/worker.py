
import da
PatternExpr_1088 = da.pat.TuplePattern([da.pat.ConstantPattern('req_res'), da.pat.FreePattern('msg')])
PatternExpr_1112 = da.pat.TuplePattern([da.pat.ConstantPattern('reply_db_read'), da.pat.FreePattern('msg')])
PatternExpr_1139 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import sys
import xml.etree.ElementTree as ET
TIMEOUT = 1
d = da.import_da('database')

class Worker(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._WorkerReceivedEvent_0 = []
        self._WorkerReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_0', PatternExpr_1088, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_1', PatternExpr_1112, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_2', PatternExpr_1139, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Worker_handler_1138])])

    def setup(self, coord_list, policy_file, data):
        self.coord_list = coord_list
        self.policy_file = policy_file
        self.data = data
        self.output('Worker: Steup Done')
        pass

    def _da_run_internal(self):
        self.output(' Worker Thread start ')
        while True:
            super()._label('_st_label_1085', block=False)
            msg = None

            def ExistentialOpExpr_1086():
                nonlocal msg
                for (_, _, (_ConstantPattern1103_, msg)) in self._WorkerReceivedEvent_0:
                    if (_ConstantPattern1103_ == 'req_res'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_1110():
                nonlocal msg
                for (_, _, (_ConstantPattern1126_, msg)) in self._WorkerReceivedEvent_1:
                    if (_ConstantPattern1126_ == 'reply_db_read'):
                        if True:
                            return True
                return False
            _st_label_1085 = 0
            self._timer_start()
            while (_st_label_1085 == 0):
                _st_label_1085 += 1
                if ExistentialOpExpr_1086():
                    pass
                    _st_label_1085 += 1
                elif ExistentialOpExpr_1110():
                    pass
                    _st_label_1085 += 1
                elif self._timer_expired:
                    pass
                    _st_label_1085 += 1
                else:
                    super()._label('_st_label_1085', block=True, timeout=(TIMEOUT * 10))
                    _st_label_1085 -= 1
            else:
                if (_st_label_1085 != 2):
                    continue
            if (_st_label_1085 != 2):
                break

    def send_attr_request(self, msg):
        self.output('Worker: sending attribute read request to DB')
        self._send(('req_db_read', msg), self.data)

    def caluculateHash(self, sub_id):
        count = 0
        for i in sub_id:
            count += ord(i)
        return count

    def return_result_to_sub_id(self, msg, result):
        self.output('Worker: Policy Evaluation complete sending to Subject Coordinator', result)
        msg.set_result(result)
        self._send(('reply_work', msg), self.coord_list[(self.caluculateHash(msg.subj_id) % len(self.coord_list))])

    def update_db_result_with_tentative(self, msg):
        self.output('Worker: extract tentative and database fetched attributes for use by evaluator')
        tent_sub_attr = msg.tent_attr.get_sub_attr()
        tent_res_attr = msg.tent_attr.get_res_attr()
        db_sub_attr = msg.db_attr.get_sub_attr()
        db_res_attr = msg.db_attr.get_res_attr()
        if (len(tent_sub_attr) > 0):
            for (k, v) in tent_sub_attr.items():
                if (k in db_sub_attr):
                    msg.db_attr.get_sub_attr()[k] = v[0]
        if (len(tent_res_attr) > 0):
            for (k, v) in tent_res_attr.items():
                if (k in db_res_attr):
                    msg.db_attr.get_res_attr()[k] = v[0]
        self.output('Worker:Attribute set ready for evaluation')

    def parse_policy(self, msg):
        self.output('Worker: parse policy file to identify the relevant policy')
        tree = ET.parse(self.policy_file)
        root = tree.getroot()
        self.output('Worker: Parse tree created')
        for rule in root.iter('rule'):
            print('rule', rule.attrib['name'])
            sc = rule.find('subjectCondition')
            for neighbor in sc.iter():
                print(neighbor.attrib)
            rc = rule.find('resourceCondition')
            for neighbor in rc.iter():
                print(neighbor.attrib)
            act = rule.find('action')
            for neighbor in act.iter():
                print(neighbor.attrib)
            su = rule.find('subjectUpdate')
            if (not (su == None)):
                for neighbor in su.iter():
                    print(neighbor.attrib)
            ru = rule.find('resourceUpdate')
            if (not (ru == None)):
                for neighbor in ru.iter():
                    print(neighbor.attrib)
        self.output('Worker: Rule found')

    def check_attribute(self, db_value, policy_value):
        idx = policy_value.find('>')
        if (not (idx == (- 1))):
            value = policy_value[(idx + 1):]
            if (value.isnumeric() and ((int(db_value) - 1) > int(value))):
                return True
        idx = policy_value.find('<')
        if (not (idx == (- 1))):
            value = policy_value[(idx + 1):]
            if (value.isnumeric() and ((int(db_value) + 1) < int(value))):
                print('check_attribute, policy value ', value, 'db_value ', db_value)
                return True
        if ((policy_value == 'empty') or (policy_value == '')):
            plist = []
        else:
            plist = policy_value.split(',')
        if ((db_value == 'empty') or (db_value == '')):
            dlist = []
        else:
            print('type of db_value', type(db_value))
            dlist = db_value.split(',')
        if (not (len(dlist) == len(plist))):
            return False
        else:
            for item in dlist:
                if (not (item in plist)):
                    return False
            return True
        return False

    def update_attributes(self, update_attr, db_attr, msg, type):
        self.output('Worker: update_attributes : find attributes to be updated in DB')
        if (not (update_attr == None)):
            for (k, v) in update_attr.attrib.items():
                if (k in db_attr):
                    if ((v == '++') and db_attr[k].isnumeric()):
                        value = str((int(db_attr[k]) + 1))
                    elif ((v == '--') and db_attr[k].isnumeric()):
                        value = str((int(db_attr[k]) - 1))
                    elif (not db_attr[k].isnumeric()):
                        if ((db_attr[k] == '') or (db_attr[k] == 'empty')):
                            value = v
                        else:
                            value = ((db_attr[k] + ',') + v)
                    else:
                        value = db_attr[k]
                    if (type == 'sub'):
                        msg.worker_attr.get_updated_attr_sub()[k] = value
                    elif (type == 'res'):
                        msg.worker_attr.get_updated_attr_res()[k] = value
        self.output('Worker: update_attributes : Attributes collected, will be sent to subject co ordinator to write on DB')

    def evaluate_rule(self, sc, rc, act, su, ru, msg, db_sub_attr, db_res_attr):
        if (sc.attrib.get('position') == msg.position):
            if ((rc.attrib.get('id') == msg.res_id) or (('type' in dir(msg)) and (rc.attrib.get('type') == msg.type))):
                if (act.attrib.get('name') == msg.action):
                    print('matched')
                    for (k, v) in sc.attrib.items():
                        if (k in db_sub_attr):
                            print('sc.attrib.items', db_sub_attr[k], v)
                            print(self.check_attribute(db_sub_attr[k], v))
                        if (k == 'position'):
                            continue
                        elif ((not (k in db_sub_attr)) or (self.check_attribute(db_sub_attr[k], v) == False)):
                            return False
                        else:
                            print('sub k and v is: ', k, v)
                            msg.worker_attr.get_read_attr_sub()[k] = v
                    for (k, v) in rc.attrib.items():
                        if (k in db_res_attr):
                            print(db_res_attr[k], v)
                        if ((k == 'id') or (k == 'type')):
                            continue
                        elif ((not (k in db_res_attr)) or (self.check_attribute(db_res_attr[k], v) == False)):
                            return False
                        else:
                            msg.worker_attr.get_read_attr_res()[k] = v
                    print('in evaluate_rule reaching to update ')
                    self.update_attributes(su, db_sub_attr, msg, 'sub')
                    self.update_attributes(ru, db_res_attr, msg, 'res')
                    return True
        return False

    def evaluate_policy(self, msg):
        self.output('Worker: evaluate policy Entry')
        tree = ET.parse(self.policy_file)
        root = tree.getroot()
        print('Entry Evaluate policy')
        db_sub_attr = msg.db_attr.get_sub_attr()
        db_res_attr = msg.db_attr.get_res_attr()
        for rule in root.iter('rule'):
            sc = rule.find('subjectCondition')
            rc = rule.find('resourceCondition')
            act = rule.find('action')
            su = rule.find('subjectUpdate')
            ru = rule.find('resourceUpdate')
            msg.worker_attr.set_read_attr_sub({})
            msg.worker_attr.set_read_attr_res({})
            if (self.evaluate_rule(sc, rc, act, su, ru, msg, db_sub_attr, db_res_attr) == True):
                return self.return_result_to_sub_id(msg, True)
        self.return_result_to_sub_id(msg, False)

    def _Worker_handler_1138(self, a, b):
        self.output('received message in worker to evaluate: ', a)
        if (a == 'req_res'):
            print('recived message from resource co-ordinator')
            self.send_attr_request(b)
        if (a == 'reply_db_read'):
            print('recived reply from database')
            self.update_db_result_with_tentative(b)
            self.evaluate_policy(b)
    _Worker_handler_1138._labels = None
    _Worker_handler_1138._notlabels = None
