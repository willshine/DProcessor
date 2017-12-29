# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 10:40:11 2016

@author: will
"""

import multiprocessing
import time
import datetime
from dateFuncs import *

def get_current_strtime():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

class DProcessor:
    """

    """

    def __init__(self, func_items, pnum=30):
        self.pnum = pnum
        self.origin_funcs = func_items
        self.run_funcs = []
        self.fail_funcs = []
        self.succ_funcs = []
        self.h_processes = {}

    def __is_p_alive(self):
        for func in self.run_funcs:
            if self.h_processes[func[0]].is_alive():
                return True
        return False

    def __get_p_unalive(self):
        for func in self.run_funcs:
            if not self.h_processes[func[0]].is_alive():
                return self.run_funcs.index(func)
        return -1

    def set_pnum(self, num):
        self.pnum = num

    def set_funcs(self, func_items):
        self.origin_funcs = func_items
        self.run_funcs = []
        self.fail_funcs = []
        self.succ_funcs = []
        self.h_processes = {}

    def run(self):
        if len(self.origin_funcs) <= self.pnum:
            self.run_funcs.extend(self.origin_funcs)
            self.origin_funcs = []
        else:
            self.run_funcs.extend(self.origin_funcs[0:self.pnum])
            self.origin_funcs = self.origin_funcs[self.pnum:]
        for every_func in self.run_funcs:
            func_name = every_func[0]
            func_meta = every_func[1]
            if len(every_func) > 2:
                f_args = every_func[2:]
            else:
                f_args = []
            print get_current_strtime() + ": " + func_name + " is running now.\n"
            h_process = multiprocessing.Process(target=func_meta, name=func_name, args=f_args)
            self.h_processes[func_name] = h_process
            h_process.start()
        while self.run_funcs:
            while True:
                e_i = self.__get_p_unalive()
                if e_i != -1:
                    p_exitcode = self.h_processes[self.run_funcs[e_i][0]].exitcode
                    if p_exitcode == 0:
                        r_func = self.run_funcs[e_i]
                        r_func.append(p_exitcode)
                        self.succ_funcs.append(r_func)
                        print get_current_strtime() + ": " + self.run_funcs[e_i][0] + " is succ.\n"
                    else:
                        r_func = self.run_funcs[e_i]
                        r_func.append(p_exitcode)
                        self.fail_funcs.append(r_func)
                        print get_current_strtime() + " Error: " + self.run_funcs[e_i][0] + " is fail.\n"

                    del self.run_funcs[e_i]
                    if self.origin_funcs:
                        p_func = self.origin_funcs.pop()
                        self.run_funcs.append(p_func)
                        func_name = p_func[0]
                        func_meta = p_func[1]
                        if len(p_func) > 2:
                            f_args = p_func[2:]
                        else:
                            f_args = []
                        print get_current_strtime() + ": " + func_name + " is running now.\n"
                        h_process = multiprocessing.Process(target=func_meta, name=func_name, args=f_args)
                        self.h_processes[func_name] = h_process
                        h_process.start()
                else:
                    break
            time.sleep(0.5)
        return self.succ_funcs, self.fail_funcs
