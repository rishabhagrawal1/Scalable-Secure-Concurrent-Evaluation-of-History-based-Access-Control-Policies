import sys

class Config:
    def __init__(self, conf_file, policy_file, data_file, attr_file):
        #self.conf_data = conf_data
        self.num_client = 1
        self.num_coordinator = 1
        self.num_workers = 1
        self.conf_file = conf_file
        self.policy_file = policy_file
        self.data_file = data_file
        self.attr_file = attr_file

    def parse_conf_data(self, conf_data):
        self.num_client = int(conf_data["num_client"])
        self.num_coordinator = int(conf_data["num_coordinator"])
        self.num_workers = int(conf_data["num_workers"])

