
import da
_config_object = {'clock': 'Lamport', 'channel': 'fifo'}
import sys, os
import json, random, copy
sys.path.insert(0, '../config')
from config import Config

class Main(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([])

    def setup(self, conf_file, policy_file, data_file, attr_file, random_input):
        self.conf_file = conf_file
        self.policy_file = policy_file
        self.data_file = data_file
        self.attr_file = attr_file
        self.random_input = random_input
        pass

    def _da_run_internal(self):
        if os.path.exists(self.conf_file):
            with open(self.conf_file, encoding='utf-8') as conf:
                conf_data = json.loads(conf.read())
                if (self.random_input == True):
                    conf_data = self.generateRandomConfig(conf_data)
            config_obj = self.read_configuration(conf_data)
            self.init_all_processes(config_obj)
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                self.output('User requested abort')
                sys.exit(0)
        else:
            self.output('error in opening file')

    def read_configuration(self, conf_data):
        config_obj = Config(self.conf_file, self.policy_file, self.data_file, self.attr_file)
        config_obj.parse_conf_data(conf_data)
        return config_obj

    def init_all_processes(self, config):
        try:
            cl = da.import_da('client')
            co = da.import_da('coordinator')
            d = da.import_da('database')
        except ImportError:
            self.output('Error in import', sep='|')
        try:
            coord = da.new(co.Coordinator, num=config.num_coordinator)
            data = da.new(d.Database, num=1)
            clie = da.new(cl.Client, num=config.num_client)
        except:
            self.output('Error in process creation')
        try:
            coord_list = list(coord)
            data_list = list(data)
            counter = 0
            for a in clie:
                da.setup(a, (config, coord_list, counter))
                counter += 1
            da.setup(coord, (config, coord_list, 0, data, None, None))
            m = list()
            m.append(self.data_file)
            da.setup(data, m)
        except:
            self.output('Error in setup')
        try:
            da.start(clie)
            da.start(coord)
            da.start(data)
        except:
            self.output('Error in starting processes')

    def generateRandomConfig(self, conf_data):
        conf_data_random = copy.deepcopy(conf_data)
        conf_data_random['operations'] = []
        self.output(conf_data_random)
        self.output(conf_data)
        operations = conf_data['operations']
        for i in range(0, 100):
            x = random.randint(0, (len(conf_data['operations']) - 1))
            print(x, type(x), len(conf_data['operations']))
            conf_data_random['operations'].append(operations[x])
        with open(self.conf_file, 'w', encoding='utf-8') as conf:
            json.dump(conf_data_random, conf)
        return conf_data_random

def main():
    conf_file = (sys.argv[1] if (len(sys.argv) > 1) else '../tests/test/conf2.json')
    policy_file = (sys.argv[2] if (len(sys.argv) > 2) else '../tests/policy/policy2.xml')
    data_file = (sys.argv[3] if (len(sys.argv) > 3) else '../tests/data/data2.json')
    attr_file = (sys.argv[4] if (len(sys.argv) > 4) else '../tests/attr/attr2.json')
    random_input = (sys.argv[5] if (len(sys.argv) > 5) else False)
    print(random_input)
    m = da.new(Main)
    da.setup(m, (conf_file, policy_file, data_file, attr_file, random_input))
    da.start(m)
if (__name__ == '__main__'):
    main()
