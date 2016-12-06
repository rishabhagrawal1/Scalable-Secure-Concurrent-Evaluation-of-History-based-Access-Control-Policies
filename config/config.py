import sys

class Config:
    def __init__(self, conf_data, config_file, policy_file, data_file, attr_file):
        self.conf_data = conf_data
        self.num_applications = 1
        self.num_coordinator = 1
        self.num_workers = 1
        self.config_file = config_file
        self.policy_file = policy_file
        self.data_file = data_file
        self.attr_file = attr_file

    def parse_conf_data(self):
        self.num_applications = int(self.conf_data["num_applications"])
        self.num_coordinator = int(self.conf_data["num_coordinator"])
        self.num_workers = int(self.conf_data["num_workers"])

