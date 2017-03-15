
import da
PatternExpr_818 = da.pat.TuplePattern([da.pat.ConstantPattern('reply_db_read'), da.pat.FreePattern('req1')])
PatternExpr_1764 = da.pat.TuplePattern([da.pat.ConstantPattern('handleReq'), da.pat.TuplePattern([da.pat.FreePattern('req'), da.pat.FreePattern('i')])])
PatternExpr_1793 = da.pat.TuplePattern([da.pat.ConstantPattern('readAttr'), da.pat.TuplePattern([da.pat.FreePattern('req'), da.pat.FreePattern('i')])])
PatternExpr_1820 = da.pat.TuplePattern([da.pat.ConstantPattern('result'), da.pat.FreePattern('req')])
PatternExpr_1843 = da.pat.TuplePattern([da.pat.ConstantPattern('restart'), da.pat.FreePattern('req')])
PatternExpr_1866 = da.pat.TuplePattern([da.pat.ConstantPattern('reply_db_read'), da.pat.FreePattern('req')])
PatternExpr_1894 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import random, time, sys
import version
import staticAnalysis
sys.path.insert(0, '../config')
import config
w = da.import_da('worker')
from request import Request
MAXDBLatency = 0.1
MINDBLatency = 0.01
TIMEOUT = 1

class Coordinator(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._CoordinatorReceivedEvent_0 = []
        self._CoordinatorReceivedEvent_1 = []
        self._CoordinatorReceivedEvent_2 = []
        self._CoordinatorReceivedEvent_3 = []
        self._CoordinatorReceivedEvent_4 = []
        self._CoordinatorReceivedEvent_5 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_0', PatternExpr_818, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_1', PatternExpr_1764, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_2', PatternExpr_1793, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_3', PatternExpr_1820, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_4', PatternExpr_1843, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_5', PatternExpr_1866, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_6', PatternExpr_1894, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Coordinator_handler_1893])])

    def setup(self, config, coord_list, worker_count, data, work_list, sta):
        self.config = config
        self.coord_list = coord_list
        self.worker_count = worker_count
        self.data = data
        self.work_list = work_list
        self.sta = sta
        work = da.new(w.Worker, num=self.config.num_workers)
        da.setup(work, (self.coord_list, self.config))
        da.start(work)
        self.work_list = list(work)
        self.attrVersionDict = {}
        self.pendingReadReq = {}
        self.currRunningWriteReq = {}
        self.sta = staticAnalysis.StaticAnalysis(self.config.attr_file, self.coord_list)
        self.common = None

    def _da_run_internal(self):
        while True:
            super()._label('_st_label_1761', block=False)
            i = req = None

            def ExistentialOpExpr_1762():
                nonlocal i, req
                for (_, _, (_ConstantPattern1782_, (req, i))) in self._CoordinatorReceivedEvent_1:
                    if (_ConstantPattern1782_ == 'handleReq'):
                        if True:
                            return True
                return False
            i = req = None

            def ExistentialOpExpr_1791():
                nonlocal i, req
                for (_, _, (_ConstantPattern1809_, (req, i))) in self._CoordinatorReceivedEvent_2:
                    if (_ConstantPattern1809_ == 'readAttr'):
                        if True:
                            return True
                return False
            req = None

            def ExistentialOpExpr_1818():
                nonlocal req
                for (_, _, (_ConstantPattern1834_, req)) in self._CoordinatorReceivedEvent_3:
                    if (_ConstantPattern1834_ == 'result'):
                        if True:
                            return True
                return False
            req = None

            def ExistentialOpExpr_1841():
                nonlocal req
                for (_, _, (_ConstantPattern1857_, req)) in self._CoordinatorReceivedEvent_4:
                    if (_ConstantPattern1857_ == 'restart'):
                        if True:
                            return True
                return False
            req = None

            def ExistentialOpExpr_1864():
                nonlocal req
                for (_, _, (_ConstantPattern1880_, req)) in self._CoordinatorReceivedEvent_5:
                    if (_ConstantPattern1880_ == 'reply_db_read'):
                        if True:
                            return True
                return False
            _st_label_1761 = 0
            self._timer_start()
            while (_st_label_1761 == 0):
                _st_label_1761 += 1
                if ExistentialOpExpr_1762():
                    pass
                    _st_label_1761 += 1
                elif ExistentialOpExpr_1791():
                    pass
                    _st_label_1761 += 1
                elif ExistentialOpExpr_1818():
                    pass
                    _st_label_1761 += 1
                elif ExistentialOpExpr_1841():
                    pass
                    _st_label_1761 += 1
                elif ExistentialOpExpr_1864():
                    pass
                    _st_label_1761 += 1
                elif self._timer_expired:
                    self.output('timeout because of inactivity')
                    _st_label_1761 += 1
                else:
                    super()._label('_st_label_1761', block=True, timeout=(TIMEOUT * 10))
                    _st_label_1761 -= 1
            else:
                if (_st_label_1761 != 2):
                    continue
            if (_st_label_1761 != 2):
                break

    def now(self):
        return time.time()

    def send_attr_read_request_to_attr_database(self, req):
        req.curr_coordinator = self.id
        self.output('Coordinator: sending attribute read request to DB')
        self._send(('req_db_read', req), self.data)

    def update_db_result_with_catched(self, x, req):
        self.output('Coordinator: extract catched and database fetched attributes for use by evaluator worker')
        if (x.type == 'sub'):
            catched_sub_attr = req.catched_attr.get_sub_attr()
            db_sub_attr = req.db_attr.get_sub_attr()
            if (len(catched_sub_attr) > 0):
                for (k, v) in catched_sub_attr.items():
                    if (k in db_sub_attr):
                        req.db_attr.get_sub_attr()[k] = v
            req.catched_attr.set_sub_attr(req.db_attr.get_sub_attr())
            x = staticAnalysis.Obj(req.subj_id, 'sub')
            for (k, v) in req.catched_attr.get_sub_attr().items():
                self.createVersionForPreviousSessionRead(x, k, v)
        else:
            catched_res_attr = req.catched_attr.get_res_attr()
            db_res_attr = req.db_attr.get_res_attr()
            if (len(catched_res_attr) > 0):
                for (k, v) in catched_res_attr.items():
                    if (k in db_res_attr):
                        req.db_attr.get_res_attr()[k] = v
            req.catched_attr.set_res_attr(req.db_attr.get_res_attr())
            x = staticAnalysis.Obj(req.res_id, 'res')
            for (k, v) in req.catched_attr.get_res_attr().items():
                self.createVersionForPreviousSessionRead(x, k, v)
        self.output('Coordinator:Attribute set ready for evaluation req id is ')

    def latestVersionBefore(self, x, attr, ts):
        aIdx = ((x.id + '_') + attr)
        if (aIdx in self.attrVersionDict):
            length = len(self.attrVersionDict[aIdx])
            for i in range((length - 1), (- 1), (- 1)):
                if (self.attrVersionDict[aIdx][i].rts < ts):
                    return self.attrVersionDict[aIdx][i]
        return self.createVersionForPreviousSessionRead(x, attr, None)

    def latestVersion(self, x, attr):
        return self.latestVersionBefore(x, attr, time.time())

    def addVersionToAttribVersionDictionary(self, x, attr, v):
        aIdx = ((x.id + '_') + attr)
        if (not (aIdx in self.attrVersionDict)):
            self.attrVersionDict[aIdx] = []
        self.attrVersionDict[aIdx].append(v)
        return self.attrVersionDict[aIdx][(- 1)]

    def createVersionForPreviousSessionRead(self, x, attr, val):
        print('createVersionForPreviousSessionRead called', x.type)
        v = version.Version(0, 0, val)
        return self.addVersionToAttribVersionDictionary(x, attr, v)

    def updateVersionAttribDictAtCoord(self, req, x):
        updates = req.worker_attr.get_updated_attr_sub()
        if (len(req.worker_attr.get_updated_attr_res()) >= 1):
            updates = req.worker_attr.get_updated_attr_res()
        print('attr need to be updated', updates)
        for (attr, val) in updates.items():
            v = version.Version(time.time(), time.time(), val)
            self.addVersionToAttribVersionDictionary(x, attr, v)

    def findVersionBeforeTs(self, aIdx, attr, req, resultSet):
        if (aIdx in self.attrVersionDict):
            for i in range((len(self.attrVersionDict[aIdx]) - 1), (- 1), (- 1)):
                v = self.attrVersionDict[aIdx][i]
                if ((v.rts <= req.ts) and (not (v.val == None))):
                    resultSet[attr] = v.val
                    return True
        return False

    def cachedUpdates(self, x, req):
        defRead = self.sta.defReadAttr(x, req)
        mightRead = self.sta.mightReadAttr(x, req)
        uniounAttr = (defRead | mightRead)
        resultSet = {}
        needDataFromDb = False
        for attr in uniounAttr:
            aIdx = ((x.id + '_') + attr)
            if (self.findVersionBeforeTs(aIdx, attr, req, resultSet) == False):
                needDataFromDb = True
        print('needDataFromDb', needDataFromDb, x.type)
        if (x.type == 'sub'):
            req.catched_attr.set_sub_attr(resultSet)
        else:
            req.catched_attr.set_res_attr(resultSet)
        if (needDataFromDb == True):
            self.send_attr_read_request_to_attr_database(req)
            super()._label('_st_label_815', block=False)
            req1 = None

            def ExistentialOpExpr_816():
                nonlocal req1
                for (_, _, (_ConstantPattern833_, req1)) in self._CoordinatorReceivedEvent_0:
                    if (_ConstantPattern833_ == 'reply_db_read'):
                        if (req1.id == req.id):
                            return True
                return False
            _st_label_815 = 0
            while (_st_label_815 == 0):
                _st_label_815 += 1
                if ExistentialOpExpr_816():
                    _st_label_815 += 1
                else:
                    super()._label('_st_label_815', block=True)
                    _st_label_815 -= 1
            if (x.type == 'sub'):
                req.db_attr.set_sub_attr(req1.db_attr.get_sub_attr())
            else:
                req.db_attr.set_res_attr(req1.db_attr.get_res_attr())
            self.update_db_result_with_catched(x, req)
        return req

    def restart(self, req):
        print('In restart')
        self._send(('restart', req), self.sta.coord(self.sta.obj(req, req.rdonlyObj)))

    def handleRestartRequest(self, req):
        req.generateTimeStamp()
        req.reset_attr_objects()
        self.checkAndHandleRequest(req, 1)

    def checkForConflicts(self, req, x):
        updates = req.worker_attr.get_updated_attr_sub()
        if (len(req.worker_attr.get_updated_attr_res()) >= 1):
            updates = req.worker_attr.get_updated_attr_res()
        self.output('checkForConflicts', updates)
        for (attr, val) in updates.items():
            v = self.latestVersion(x, attr)
            self.output('checkForConflicts for req:', req.id, ' attr:', attr, ' v.rts:, v.wts:', v.rts, v.wts, ' req.ts:', req.ts)
            if (v.rts > req.ts):
                self.output('coordinator: checkForConflicts detected conflict for attr', attr, 'for req', req.id)
                return True
        return False

    def handleCurrWriteAndPendingReadReqs(self, req, i):
        print('currRunningWriteReq before', self.currRunningWriteReq, req, req.id)
        if (req.id in self.currRunningWriteReq.keys()):
            self.currRunningWriteReq.pop(req.id)
            self.startDelayedReadRequest(i)
        print('currRunningWriteReq after', self.currRunningWriteReq, req, req.id)

    def handleWorkerResponseForWriteRequests(self, req):
        x = self.sta.obj(req, req.updatedObj)
        conflict = self.checkForConflicts(req, x)
        updates = req.worker_attr.get_updated_attr_sub()
        if (len(req.worker_attr.get_updated_attr_res()) >= 1):
            updates = req.worker_attr.get_updated_attr_res()
        if (not conflict):
            super()._label('_st_label_1064', block=False)
            val = attr = None

            def UniversalOpExpr_1065():
                nonlocal val, attr
                for (attr, val) in updates.items():
                    if (not ((len(self.latestVersionBefore(x, attr, req.ts).pendingMightRead) == 0) or (((len(self.latestVersionBefore(x, attr, req.ts).pendingMightRead) == 1) and next(iter(self.latestVersionBefore(x, attr, req.ts).pendingMightRead))) == req.id))):
                        return False
                return True
            _st_label_1064 = 0
            while (_st_label_1064 == 0):
                _st_label_1064 += 1
                if UniversalOpExpr_1065():
                    _st_label_1064 += 1
                else:
                    super()._label('_st_label_1064', block=True)
                    _st_label_1064 -= 1
            conflict = self.checkForConflicts(req, x)
            if (not conflict):
                self._send(('req_db_write', req), self.data)
                self.updateVersionAttribDictAtCoord(req, x)
                uniounAttr = (self.sta.defReadAttr(x, req) | self.sta.mightReadAttr(x, req))
                for attr in uniounAttr:
                    v = self.latestVersionBefore(x, attr, req.ts)
                    if (req.id in v.pendingMightRead):
                        v.pendingMightRead.remove(req.id)
                    readAttr = req.worker_attr.read_attr_sub
                    if (not req.worker_attr.updated_attr_sub):
                        readAttr = req.worker_attr.read_attr_res
                    if (attr in readAttr):
                        v.rts = time.time()
                self._send(('result', req), req.curr_app)
                self._send(('readAttr', (req, req.rdonlyObj)), self.sta.coord(self.sta.obj(req, req.rdonlyObj)))
                self.handleCurrWriteAndPendingReadReqs(req, req.updatedObj)
            else:
                self.restart(req)
        else:
            self.restart(req)

    def handleWorkerResponseForReadRequests(self, req, i):
        x = self.sta.obj(req, i)
        for attr in self.sta.mightReadAttr(x, req):
            v = self.latestVersionBefore(x, attr, req.ts)
            if ((len(v.pendingMightRead) >= 1) and (req.id in v.pendingMightRead)):
                v.pendingMightRead.remove(req.id)
            readAttr = (req.worker_attr.read_attr_res, req.worker_attr.read_attr_sub)
            for r in readAttr:
                if (attr in r):
                    v.rts = time.time()
        if ((not req.worker_attr.get_updated_attr_sub()) and (not req.worker_attr.get_updated_attr_res())):
            self.handleCurrWriteAndPendingReadReqs(req, i)

    def handleReqAsCorod1(self, req):
        print('in handleReqAsCorod1 req id', req.id)
        x = self.sta.obj(req, 1)
        req.ts = self.now()
        req = self.cachedUpdates(x, req)
        if (not self.sta.mightWriteObj(req)):
            for attr in self.sta.defReadAttr(x, req):
                self.latestVersionBefore(x, attr, req.ts).rts = req.ts
        else:
            for attr in self.sta.defReadAttr(x, req):
                self.latestVersionBefore(x, attr, req.ts).pendingMightRead.add(req.id)
        for attr in self.sta.mightReadAttr(x, req):
            self.latestVersionBefore(x, attr, req.ts).pendingMightRead.add(req.id)
        self._send(('handleReq', (req, 2)), self.coord_list[0])

    def sendRequestToWorker(self, req):
        self._send(('req_cord', req), self.work_list[(self.worker_count % self.config.num_workers)])
        self.worker_count += 1
        print('Work sent to worker')

    def handleReqAsCorod2(self, req):
        print('in handleReqAsCorod2 req id', req.id)
        x = self.sta.obj(req, 2)
        req = self.cachedUpdates(x, req)
        if (not self.sta.mightWriteObj(req)):
            for attr in self.sta.defReadAttr(x, req):
                self.latestVersionBefore(x, attr, req.ts).rts = req.ts
        else:
            for attr in self.sta.defReadAttr(x, req):
                self.latestVersionBefore(x, attr, req.ts).pendingMightRead.add(req.id)
        for attr in self.sta.mightReadAttr(x, req):
            self.latestVersionBefore(x, attr, req.ts).pendingMightRead.add(req.id)
        self.sendRequestToWorker(req)

    def handleRequest(self, req, req_type):
        req.generateTimeStamp()
        if (req_type == 1):
            self.handleReqAsCorod1(req)
        else:
            self.handleReqAsCorod2(req)

    def startDelayedReadRequest(self, i):
        print('startDelayedReadRequest ', self.pendingReadReq)
        listToRemove = list()
        for (reqId, reqObj) in self.pendingReadReq.items():
            if (self.needDealyToPreventStarvation(reqObj, i) == False):
                listToRemove.append(reqId)
        for reqId in listToRemove:
            reqObj = self.pendingReadReq[reqId]
            self.pendingReadReq.pop(reqId)
            self.handleRequest(reqObj, i)

    def needDealyToPreventStarvation(self, req, req_type):
        self.output('needDealyToPreventStarvation req', req.id, 'sta.mightWriteObj(req)', self.sta.mightWriteObj(req))
        if self.sta.mightWriteObj(req):
            return False
        x = self.sta.obj(req, req_type)
        defRead = self.sta.defReadAttr(x, req)
        mightRead = self.sta.mightReadAttr(x, req)
        uniounAttr = (defRead | mightRead)
        self.output('needDealyToPreventStarvation currRunningWriteReq', self.currRunningWriteReq)
        for (reqId, reqObj) in self.currRunningWriteReq.items():
            mightWrite = self.sta.mightWriteAttr(self.sta.obj(reqObj, req_type), reqObj)
            if (mightWrite & uniounAttr):
                return True
        return False

    def checkAndHandleRequest(self, req, req_type):
        if (self.needDealyToPreventStarvation(req, req_type) == False):
            self.output('does not need to delay this req', self.sta.mightWriteObj(req))
            if (self.sta.mightWriteObj(req) and (not (req.id in self.currRunningWriteReq.keys()))):
                print('adding in currRunningWriteReq list req id', req.id)
                self.currRunningWriteReq[req.id] = req
            self.handleRequest(req, req_type)
        elif (not (req.id in self.pendingReadReq.keys())):
            self.pendingReadReq[req.id] = req

    def _Coordinator_handler_1893(self, a, b):
        if (a == 'handleReq'):
            self.output('received msg in Coordinator', a, ' with req id', b[0].id)
            self.checkAndHandleRequest(b[0], b[1])
        elif (a == 'readAttr'):
            self.output('received msg in Coordinator', a, ' with req id , ', b[0].id)
            self.handleWorkerResponseForReadRequests(b[0], b[1])
        elif (a == 'result'):
            self.output('received msg in Coordinator', a, ' with req id , ', b.id)
            self.handleWorkerResponseForWriteRequests(b)
        elif (a == 'restart'):
            self.output('received msg in Coordinator', a, ' with req id , ', b.id)
            self.handleRestartRequest(b)
        elif (a == 'reply_db_read'):
            self.output('received msg in Coordinator', a, ' with req id , ', b.id)
    _Coordinator_handler_1893._labels = None
    _Coordinator_handler_1893._notlabels = None
