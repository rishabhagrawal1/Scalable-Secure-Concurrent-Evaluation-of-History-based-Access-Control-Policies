import sys
import request
import json

class Obj:
    def __init__(self, id, type):
        self.id = id
        self.type = type

##Object of attribute versions to be used in latestVersion and latestVersionBefore
class StaticAnalysis:
    def __init__(self, attr_file, coord_list):
        self.attr_file = attr_file  
        self.attr_data = None
        self.coord_list = coord_list
    
    def calculateHash(self, id):
        count = 0
        for i in id:
            count += ord(i)
        return count
        
    def loadAttrFileObj(self):  
        try:    
            if(os.path.exists(attr_file)):
                with open(attr_file, encoding='utf-8') as attrs:
                    self.attr_data = json.loads(attrs.read())
                    output("Trying to print the type of attr_data",type(attr_data))
        except:
            output("Error in reading Attribute file")

    def mightWriteObj(self, req):
        req_attr = dir(req)
        result_set = set()
        if(not self.attr_data):
            return result_set
        for element in self.attr_data['attribute_properties']:
            if(element.keys() in req_attr and element.values[0][1]['write'] == 'mutable'):
               result_set.add(element.values[0][2]['obj'])
        return result_set
        
    def defReadAttr(self, x, req):
        req_attr = dir(req)
        result_set = set()
        if(not self.attr_data):
            return result_set
        for element in self.attr_data['attribute_properties']:
            if(element.keys() in req_attr and element.values[0][2]['obj'] == x and element.values[0][0]['read'] == 'def'):
               result_set.add(element.keys())
        return result_set
    
    def mightReadAttr(self, x, req):
        req_attr = dir(req)
        result_set = set()
        if(not self.attr_data):
            return result_set
        for element in self.attr_data['attribute_properties']:
            if(element.keys() in req_attr and element.values[0][2]['obj'] == x and element.values[0][0]['read'] == 'might'):
                result_set.add(element.keys())
        return result_set
        
    def mightWriteAttr(self, x, req):
        req_attr = dir(req)
        result_set = set()
        if(not self.attr_data):
            return result_set
        for element in self.attr_data['attribute_properties']:
            if(element.keys() in req_attr and element.values[0][2]['obj'] == x and element.values[0][1]['write'] == 'mutable'):
                result_set.add(element.keys())
        return result_set
        
    def obj(self, req, i):
        result = 'sub'
        result_set = self.mightWriteObj(req)
        if(len(result_set) == 1):
            if(next(iter(result_set)) == 'sub' and i == 1):
                result = 'res'
            elif(next(iter(result_set)) == 'res' and i == 2):
                result = 'res'
        else:
            if(i == 2):
                result = 'res'
        if (result == 'sub'):
            ob = Obj(req.subj_id, result)
        else:
            ob = Obj(req.res_id, result)
        return ob
        
    def coord(self, obj):
        return self.coord_list[self.calculateHash(obj.id) % len(self.coord_list)]
        
        
        
        
        
        
