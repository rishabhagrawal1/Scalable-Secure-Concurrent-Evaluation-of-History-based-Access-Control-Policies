
import da
PatternExpr_936 = da.pat.TuplePattern([da.pat.ConstantPattern('req_cord'), da.pat.FreePattern('req')])
PatternExpr_964 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import sys
import xml.etree.ElementTree as ET
sys.path.insert(0, '../config')
import config
import staticAnalysis
d = da.import_da('database')
co = da.import_da('coordinator')
TIMEOUT = 1

class Worker(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._WorkerReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_0', PatternExpr_936, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_1', PatternExpr_964, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Worker_handler_963])])

    def setup(self, coord_list, config):
        self.coord_list = coord_list
        self.config = config
        pass

    def _da_run_internal(self):
        while True:
            super()._label('_st_label_933', block=False)
            req = None

            def ExistentialOpExpr_934():
                nonlocal req
                for (_, _, (_ConstantPattern951_, req)) in self._WorkerReceivedEvent_0:
                    if (_ConstantPattern951_ == 'req_cord'):
                        if True:
                            return True
                return False
            _st_label_933 = 0
            self._timer_start()
            while (_st_label_933 == 0):
                _st_label_933 += 1
                if ExistentialOpExpr_934():
                    pass
                    _st_label_933 += 1
                elif self._timer_expired:
                    pass
                    _st_label_933 += 1
                else:
                    super()._label('_st_label_933', block=True, timeout=(TIMEOUT * 10))
                    _st_label_933 -= 1
            else:
                if (_st_label_933 != 2):
                    continue
            if (_st_label_933 != 2):
                break

    def return_result_to_client(self, req, result):
        self.output('Worker: Policy Evaluation complete sending result ', result, ' of read only request with id ', req.id, ' to client')
        self._send(('result', req), req.curr_app)

    def handle_evaluation_result(self, req, result):
        sta = staticAnalysis.StaticAnalysis(self.config.attr_file, self.coord_list)
        req.set_result(result)
        if ((len(req.worker_attr.updated_attr_sub) >= 1) and (sta.obj(req, 1).type == 'sub')):
            req.updatedObj = 1
            req.rdonlyObj = 2
        elif ((len(req.worker_attr.updated_attr_sub) >= 1) and (sta.obj(req, 2).type == 'sub')):
            req.updatedObj = 2
            req.rdonlyObj = 1
        elif ((len(req.worker_attr.updated_attr_res) >= 1) and (sta.obj(req, 1).type == 'res')):
            req.updatedObj = 1
            req.rdonlyObj = 2
        elif ((len(req.worker_attr.updated_attr_res) >= 1) and (sta.obj(req, 2).type == 'sub')):
            req.updatedObj = 2
            req.rdonlyObj = 1
        print('handle_evaluation_result req id is', req.id, 'updated obj is', req.updatedObj)
        if (req.updatedObj == (- 1)):
            self.return_result_to_client(req, result)
            for i in range(1, 3):
                self._send(('readAttr', (req, i)), sta.coord(sta.obj(req, i)))
        else:
            self._send(('result', req), sta.coord(sta.obj(req, req.updatedObj)))

    def check_attribute(self, curr_value, policy_value):
        idx = policy_value.find('>')
        if (not (idx == (- 1))):
            value = policy_value[(idx + 1):]
            if (value.isnumeric() and ((int(curr_value) - 1) > int(value))):
                return True
        idx = policy_value.find('<')
        if (not (idx == (- 1))):
            value = policy_value[(idx + 1):]
            if (value.isnumeric() and ((int(curr_value) + 1) < int(value))):
                return True
        if ((policy_value == 'empty') or (policy_value == '')):
            plist = []
        else:
            plist = policy_value.split(',')
        if ((curr_value == 'empty') or (curr_value == '')):
            dlist = []
        else:
            dlist = curr_value.split(',')
        if (not (len(dlist) == len(plist))):
            return False
        else:
            for item in dlist:
                if (not (item in plist)):
                    return False
            return True
        return False

    def update_attributes(self, update_attr, curr_attr, req, type):
        self.output('Worker: update_attributes : find attributes to be updated in DB for ', type)
        if (not (update_attr == None)):
            for (k, v) in update_attr.attrib.items():
                if (k in curr_attr):
                    if ((v == '++') and curr_attr[k].isnumeric()):
                        value = str((int(curr_attr[k]) + 1))
                    elif ((v == '--') and curr_attr[k].isnumeric()):
                        value = str((int(curr_attr[k]) - 1))
                    elif (not curr_attr[k].isnumeric()):
                        if ((curr_attr[k] == '') or (curr_attr[k] == 'empty')):
                            value = v
                        else:
                            value = ((curr_attr[k] + ',') + v)
                    else:
                        value = curr_attr[k]
                    if (type == 'sub'):
                        req.worker_attr.get_updated_attr_sub()[k] = value
                    elif (type == 'res'):
                        req.worker_attr.get_updated_attr_res()[k] = value
        self.output('Worker: update_attributes : Attributes collected, will be sent to co ordinator to write on DB for', type)

    def evaluate_rule(self, sc, rc, act, su, ru, req, sub_attr, res_attr):
        if (sc.attrib.get('position') == req.position):
            if ((rc.attrib.get('id') == req.res_id) or (('type' in dir(req)) and (rc.attrib.get('type') == req.type))):
                if (act.attrib.get('name') == req.action):
                    for (k, v) in sc.attrib.items():
                        if ((not (k in sub_attr)) or (self.check_attribute(sub_attr[k], v) == False)):
                            return False
                        else:
                            req.worker_attr.get_read_attr_sub()[k] = v
                    for (k, v) in rc.attrib.items():
                        if ((not (k in res_attr)) or (self.check_attribute(res_attr[k], v) == False)):
                            return False
                        else:
                            req.worker_attr.get_read_attr_res()[k] = v
                    print('in evaluate_rule reaching to update ')
                    self.update_attributes(su, sub_attr, req, 'sub')
                    self.update_attributes(ru, res_attr, req, 'res')
                    return True
        return False

    def evaluate_policy(self, req):
        print('Worker: evaluate policy Entry for req id', req.id)
        tree = ET.parse(self.config.policy_file)
        root = tree.getroot()
        print('Entry Evaluate policy')
        sub_attr = req.catched_attr.get_sub_attr()
        res_attr = req.catched_attr.get_res_attr()
        for rule in root.iter('rule'):
            sc = rule.find('subjectCondition')
            rc = rule.find('resourceCondition')
            act = rule.find('action')
            su = rule.find('subjectUpdate')
            ru = rule.find('resourceUpdate')
            req.worker_attr.set_read_attr_sub({})
            req.worker_attr.set_read_attr_res({})
            if (self.evaluate_rule(sc, rc, act, su, ru, req, sub_attr, res_attr) == True):
                self.handle_evaluation_result(req, True)
                return
        self.handle_evaluation_result(req, False)

    def _Worker_handler_963(self, a, b):
        self.output('received req with id ', b.id, b.req_type, 'in worker to evaluate from local co-ordinator: ', a)
        if (a == 'req_cord'):
            self.evaluate_policy(b)
    _Worker_handler_963._labels = None
    _Worker_handler_963._notlabels = None
