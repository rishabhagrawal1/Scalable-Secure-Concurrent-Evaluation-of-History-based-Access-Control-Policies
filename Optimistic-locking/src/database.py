
import da
PatternExpr_363 = da.pat.TuplePattern([da.pat.ConstantPattern('req_db_read'), da.pat.FreePattern('msg')])
PatternExpr_387 = da.pat.TuplePattern([da.pat.ConstantPattern('req_db_write'), da.pat.FreePattern('msg')])
PatternExpr_414 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import sys, os, json
TIMEOUT = 1

class Database(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._DatabaseReceivedEvent_0 = []
        self._DatabaseReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_0', PatternExpr_363, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_1', PatternExpr_387, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_2', PatternExpr_414, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Database_handler_413])])

    def setup(self, data_file):
        self.data_file = data_file
        self.attributeStore = dict()
        self.attributeStore['resources'] = dict()
        self.attributeStore['subjects'] = dict()
        if (self.loadConfig() == False):
            sys.exit((- 1))

    def _da_run_internal(self):
        while True:
            super()._label('_st_label_360', block=False)
            msg = None

            def ExistentialOpExpr_361():
                nonlocal msg
                for (_, _, (_ConstantPattern378_, msg)) in self._DatabaseReceivedEvent_0:
                    if (_ConstantPattern378_ == 'req_db_read'):
                        if True:
                            return True
                return False
            msg = None

            def ExistentialOpExpr_385():
                nonlocal msg
                for (_, _, (_ConstantPattern401_, msg)) in self._DatabaseReceivedEvent_1:
                    if (_ConstantPattern401_ == 'req_db_write'):
                        if True:
                            return True
                return False
            _st_label_360 = 0
            self._timer_start()
            while (_st_label_360 == 0):
                _st_label_360 += 1
                if ExistentialOpExpr_361():
                    pass
                    _st_label_360 += 1
                elif ExistentialOpExpr_385():
                    pass
                    _st_label_360 += 1
                elif self._timer_expired:
                    pass
                    _st_label_360 += 1
                else:
                    super()._label('_st_label_360', block=True, timeout=(TIMEOUT * 10))
                    _st_label_360 -= 1
            else:
                if (_st_label_360 != 2):
                    continue
            if (_st_label_360 != 2):
                break

    def handleupdate(self, msg):
        self.output('Database: Database received write request to update attributes for Id:', msg.subj_id)
        for (k, v) in msg.worker_attr.updated_attr_sub.items():
            print('k and v are available')
            if (k in self.attributeStore['subjects'].get(msg.subj_id)):
                self.attributeStore['subjects'].get(msg.subj_id)[k] = v
        for (k, v) in msg.worker_attr.updated_attr_res.items():
            if (k in self.attributeStore['resources'].get(msg.res_id)):
                self.attributeStore['resources'].get(msg.res_id)[k] = v
        self.output('Database: Database write request completed for Id:', msg.subj_id)

    def handleQuery(self, msg):
        self.output('Database: Received a query for :', msg.subj_id)
        item = self.attributeStore['subjects'].get(msg.subj_id)
        self.output('item in database is ', item)
        if (not (item == None)):
            msg.db_attr.set_sub_attr(item)
        item = self.attributeStore['resources'].get(msg.res_id)
        if (not (item == None)):
            msg.db_attr.set_res_attr(item)
        self.output('item in database is ', item)
        self._send(('reply_db_read', msg), msg.curr_worker)
        self.output('Database : Message sent to worker back after database fetch')

    def loadConfig(self):
        if (not os.path.exists(self.data_file)):
            self.output(('Database: preInit Config file %s not found' % self.data_file))
            return (- 1)
        try:
            preConfigData = json.loads(open(self.data_file).read())
            self.output('Database: Loading entries in JSon file to local memory to simulate DB')
            for subjects in preConfigData.get('subjects'):
                item = subjects.get('id')
                self.attributeStore['subjects'][item] = dict()
                for (k, v) in subjects.items():
                    if (not (k == 'id')):
                        self.attributeStore['subjects'][item][k] = v
            for resources in preConfigData.get('resources'):
                item = resources.get('id')
                self.attributeStore['resources'][item] = dict()
                for (k, v) in resources.items():
                    if (not (k == 'id')):
                        self.attributeStore['resources'][item][k] = v
            self.output('Loading Datasbe entries in JSon file complete, DB Simulator Ready')
            return True
        except:
            self.output('Database: Json file not in correct syntax')
            return False

    def _Database_handler_413(self, a, b):
        if (a == 'req_db_read'):
            self.handleQuery(b)
        elif (a == 'req_db_write'):
            self.handleupdate(b)
    _Database_handler_413._labels = None
    _Database_handler_413._notlabels = None
