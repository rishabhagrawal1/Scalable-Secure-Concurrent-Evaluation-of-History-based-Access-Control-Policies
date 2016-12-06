import sys
import time
seed = 1000

##From Subject to Worker tentative attributes
class CatchedAttributes:
    def __init__(self):
        self.sub_attr = {}
        self.res_attr = {}

    def set_sub_attr(self, sub_attr):
        self.sub_attr = sub_attr

    def set_res_attr(self, res_attr):
        self.res_attr = res_attr

    def get_sub_attr(self):
        return self.sub_attr

    def get_res_attr(self):
        return self.res_attr

##From DB to worker attributes based on subj and res
class FromDBAttributes:
    def __init__(self):
        self.sub_attr = {}
        self.res_attr = {}

    def set_sub_attr(self, sub_attr):
        self.sub_attr = sub_attr

    def set_res_attr(self, res_attr):
        self.res_attr = res_attr

    def get_sub_attr(self):
        return self.sub_attr

    def get_res_attr(self):
        return self.res_attr

##From worker to subject attributes need to be updated and read in the process of evaluation
class FromWorkerAttributes:
    def __init__(self):
        self.updated_attr_sub = {}
        self.read_attr_sub = {}
        self.updated_attr_res = {}
        self.read_attr_res = {}

    def set_updated_attr_sub(self, updated_attr_sub):
        self.updated_attr_sub = updated_attr_sub

    def set_read_attr_sub(self, read_attr_sub):
        self.read_attr_sub = read_attr_sub

    def set_updated_attr_res(self, updated_attr_res):
        self.updated_attr_res = updated_attr_res

    def set_read_attr_res(self, read_attr_res):
        self.read_attr_res = read_attr_res

    def get_updated_attr_sub(self):
        return self.updated_attr_sub

    def get_read_attr_sub(self):
        return self.read_attr_sub

    def get_updated_attr_res(self):
        return self.updated_attr_res

    def get_read_attr_res(self):
        return self.read_attr_res

class Request:
    def __init__(self):
        self.subj_id = -1
        self.res_id = -1
        self.action = None
        self.position = None
        self.ts = 0
        self.id = -1
        self.result = False
        self.updatedObj = -1
        self.rdonlyObj = -1
        self.curr_coordinator = None
        self.curr_app = None
        self.catched_attr = CatchedAttributes()
        self.db_attr = FromDBAttributes()
        self.worker_attr = FromWorkerAttributes()

    def generateReqId(self, counter):
        self.ReqId = seed + counter

    def generateTimeStamp(self):
        clk = time.time()
        self.ts = clk

    def reset_attr_objects(self):
        self.catched_attr = CatchedAttributes()
        self.db_attr = FromDBAttributes()
        self.worker_attr = FromWorkerAttributes()

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def set_curr_app(self, curr_app):
        self.curr_app = curr_app

    def get_curr_app(self):
        return self.curr_app

class HistoryRequest(Request):
    def __init__(self):
        Request.__init__(self)

class DrmRequest(Request):
    def __init__(self, type):
        Request.__init__(self)
        self.type = type

