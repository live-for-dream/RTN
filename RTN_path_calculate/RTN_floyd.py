import random
import copy
import os, sys
import datetime
import RTN_log
try:
    import configparser
except:
    import ConfigParser as configparser

class RTN_path(object):
    def __init__(self, conf_path):
        self.node_max = 256
        self.max_distance = 65536
        self.conf = configparser.SafeConfigParser()
        self.result = []
        try:
            self.conf.read(conf_path)
        except:
            RTN_log.log_error("config error")
            exit(-1)

        if not self.conf.has_section('global') or not self.conf.has_option('global', 'node_num'):
            RTN_log.log_error("no section \'global\' or no option \'node_num\' in \'global\' section ")
            exit(-1)
        self.node_num = self.conf.getint('global', 'node_num')
        if self.node_num < 3 or self.node_num > self.node_max:
            RTN_log.log_error("invalid node_num, node_num should be in range (3, %d)" % (self.node_max))
            exit(-1)

        self.paths = [[0 for i in range(self.node_num)] for i in range(self.node_num)]
        self.dis = [[0 for i in range(self.node_num)] for i in range(self.node_num)]
        self.result = [[[] for i in range(self.node_num)] for i in range(self.node_num)]
        if self.conf.has_option('global', 'output'):
            self.output = self.conf.get('global', 'output')
        else:
            self.output = "RTN_paths"
        dt = datetime.datetime.now()
        out_put_file = "%s_%s" % (self.output, dt.strftime("%Y%m%d-%H-%M"))
        self.output_fd = os.open(out_put_file, os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        for i in range(0, self.node_num, 1):
            section_name = 'node-%03d' % (i)
            for j in range(0, self.node_num, 1):
                self.paths[i][j] = j
                self.dis[i][j] = self.max_distance
                option_name = 'node-%03d' % (j)

                if self.conf.has_section(section_name) and self.conf.has_option(section_name, option_name):
                    distance = self.conf.getint(section_name, option_name)
                    print "distance: [%d]\n" % (distance)
                    if distance < 0 or distance > self.max_distance:
                        RTN_log.log_info('invaild distance between %s and $s, which should be in range (0, %d)'\
                                         % (section_name, option_name, self.max_distance))
                    else:
                        self.dis[i][j] = distance
                if i == j:
                        self.dis[i][j] = 0

    def RTN_path_calculate(self):
        for k in range(0, self.node_num, 1):
            for i in range(0, self.node_num, 1):
                for j in range(0, self.node_num, 1):
                    if self.dis[i][j] > self.dis[i][k] + self.dis[k][j]:
                        self.dis[i][j] = self.dis[i][k] + self.dis[k][j]
                        self.paths[i][j] = k


    def RTN_process_single_result(self, node_i, node_j):
        node_k = self.paths[node_i][node_j]
        if node_k == node_j:
            return [node_i, node_j]
        node_k = self.paths[node_i][node_j]
        tmp_result = [node_i]
        tmp_result.extend(self.RTN_process_single_result(node_k, node_j))
        return tmp_result
    def RTN_process_all_result(self):
        for i in range(0, self.node_num, 1):
            for j in range(0, self.node_num, 1):
                if i == j:
                    continue
                self.result[i][j] = self.RTN_process_single_result(i, j)

    def RTN_path_output(self):

        for i in range(0, self.node_num, 1):
            for j in range(0, self.node_num, 1):
                if i == j:
                    continue
                record = "node: %03d -> %03d path: %s\n" % (i, j, self.result[i][j])
                os.write(self.output_fd, record)



    def RTN_origin_dis_output(self, data, info):
        for i in range(0, self.node_num, 1):
            record = "\tnode-%03d: %s: %s\n" % (i, info, data[i])
            os.write(self.output_fd, record)

r_path = RTN_path('config')
r_path.RTN_origin_dis_output(r_path.dis, "distance")
r_path.RTN_origin_dis_output(r_path.paths, "paths")
r_path.RTN_path_calculate()
r_path.RTN_process_all_result()
r_path.RTN_path_output()