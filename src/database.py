
import da
PatternExpr_686 = da.pat.TuplePattern([da.pat.ConstantPattern('req_db_read'), da.pat.FreePattern('req')])
PatternExpr_710 = da.pat.TuplePattern([da.pat.ConstantPattern('req_db_write'), da.pat.FreePattern('req')])
PatternExpr_737 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import sys, os, json
TIMEOUT = 1

class Database(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._DatabaseReceivedEvent_0 = []
        self._DatabaseReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_0', PatternExpr_686, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_1', PatternExpr_710, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_2', PatternExpr_737, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Database_handler_736])])

    def setup(self, data_file):
        self.data_file = data_file
        self.attributeStore = dict()
        self.attributeStore['resources'] = dict()
        self.attributeStore['subjects'] = dict()
        if (self.getDataFromFile() == False):
            sys.exit((- 1))

    def _da_run_internal(self):
        while True:
            super()._label('_st_label_683', block=False)
            req = None

            def ExistentialOpExpr_684():
                nonlocal req
                for (_, _, (_ConstantPattern701_, req)) in self._DatabaseReceivedEvent_0:
                    if (_ConstantPattern701_ == 'req_db_read'):
                        if True:
                            return True
                return False
            req = None

            def ExistentialOpExpr_708():
                nonlocal req
                for (_, _, (_ConstantPattern724_, req)) in self._DatabaseReceivedEvent_1:
                    if (_ConstantPattern724_ == 'req_db_write'):
                        if True:
                            return True
                return False
            _st_label_683 = 0
            self._timer_start()
            while (_st_label_683 == 0):
                _st_label_683 += 1
                if ExistentialOpExpr_684():
                    pass
                    _st_label_683 += 1
                elif ExistentialOpExpr_708():
                    pass
                    _st_label_683 += 1
                elif self._timer_expired:
                    pass
                    _st_label_683 += 1
                else:
                    super()._label('_st_label_683', block=True, timeout=(TIMEOUT * 10))
                    _st_label_683 -= 1
            else:
                if (_st_label_683 != 2):
                    continue
            if (_st_label_683 != 2):
                break

    def create_new_version(self, req):
        v = dict()
        v['v_ts'] = req.ts
        if (not (req.worker_attr.get_updated_attr_sub() == None)):
            for (k, val) in req.worker_attr.read_attr_sub.items():
                v[k] = val
            for (k, val) in req.worker_attr.updated_attr_sub.items():
                v[k] = val
        else:
            for (k, val) in req.worker_attr.read_attr_res.items():
                v[k] = val
            for (k, val) in req.worker_attr.updated_attr_res.items():
                v[k] = val
        return v

    def handleupdate(self, req):
        self.output('Database: Database received write request to update attributes for Id:', req.subj_id)
        v = self.create_new_version(req)
        if (not (req.worker_attr.get_updated_attr_sub() == None)):
            if (self.attributeStore['subjects'].get(req.subj_id) is None):
                self.attributeStore['subjects'][req.subj_id] = []
            self.attributeStore['subjects'].get(req.subj_id).append(v)
            self.output('Database: Database write request completed for sub Id:', req.subj_id)
        else:
            if (self.attributeStore['resources'].get(req.res_id) is None):
                self.attributeStore['resources'][req.subj_id] = []
            self.attributeStore['resources'].get(req.sub_id).append(v)
            self.output('Database: Database write request completed for res Id:', req.res_id)

    def handleQuery(self, req):
        self.output('Database: Received a query for with ts :', req.subj_id, req.ts)
        version_list = self.attributeStore['subjects'][req.subj_id]
        self.output('version_list subj in database is ', version_list)
        index = (- 1)
        for i in range(0, len(version_list)):
            ts = version_list[i].get('v_ts')
            if (float(ts) < float(req.ts)):
                index = i
                break
        if (not (index == (- 1))):
            subj_attribs = dict()
            for (k, v) in version_list[i].items():
                if (not (k == 'v_ts')):
                    subj_attribs[k] = v
        req.db_attr.set_sub_attr(subj_attribs)
        version_list = self.attributeStore['resources'][req.res_id]
        self.output('version_list res in database is ', version_list)
        index = (- 1)
        for i in range(0, len(version_list)):
            ts = version_list[i].get('v_ts')
            if (float(ts) < float(req.ts)):
                index = i
                break
        if (not (index == (- 1))):
            res_attribs = dict()
            res_attribs['id'] = req.res_id
            for (k, v) in version_list[i].items():
                if (not (k == 'v_ts')):
                    res_attribs[k] = v
        req.db_attr.set_res_attr(res_attribs)
        self._send(('reply_db_read', req), req.curr_coordinator)
        self.output('Database : Message sent to curr_coordinator back after database fetch')

    def getDataFromFile(self):
        if (not os.path.exists(self.data_file)):
            self.output(('Database: preInit Config file %s not found' % self.data_file))
            return (- 1)
        try:
            fileData = json.loads(open(self.data_file).read())
            self.output('Database: Loading entries from JSon file to local memory to simulate DB')
            for subjects in fileData.get('subjects'):
                item = subjects.get('sub-id')
                version = subjects.get('version')
                self.attributeStore['subjects'][item] = version
            for resources in fileData.get('resources'):
                item = resources.get('id')
                version = resources.get('version')
                self.attributeStore['resources'][item] = version
            self.output('Loading Datasbe entries in JSon file complete, DB Simulator Ready')
            return True
        except:
            self.output('Database: Json file not in correct syntax')
            return False

    def _Database_handler_736(self, a, b):
        self.output('received req in Database: ', a)
        if (a == 'req_db_read'):
            self.handleQuery(b)
        elif (a == 'req_db_write'):
            self.handleupdate(b)
    _Database_handler_736._labels = None
    _Database_handler_736._notlabels = None
