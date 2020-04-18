#!/usr/local/bin/python

import psutil
import os
import subprocess
import re
import shutil

FREE_MEMORY_INDEX = 1
ACTIVE_MEMORY_INDEX = 2
INACTIVE_MEMORY_INDEX = 3
WIRED_MEMORY_INDEX = 6

class healthExtractor():
    def __init__(self, cpu_time_analyzes = 1):
        self.matcher = re.compile('\d+')
        self.cpu_time_analyzes =  cpu_time_analyzes
    
    def get_cpu_count(self):
        return os.cpu_count()
    
    def get_cpu_load(self):
        return [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]

    def get_cpu_percent(self):
        return psutil.cpu_percent(self.cpu_time_analyzes)
    
    def get_total_ram(self):
        total_ram = subprocess.run(['sysctl', 'hw.memsize'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        return int(self.matcher.search(total_ram).group()) / 1024**3
    
    def get_virtual_memory(self):
        return subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
        
    def get_used_ram(self):
        vmLines = self.get_virtual_memory().split('\n')
        wired_memory = (int(self.matcher.search(vmLines[WIRED_MEMORY_INDEX]).group()) * 4096) / 1024 ** 3
        active_memory = (int(self.matcher.search(vmLines[ACTIVE_MEMORY_INDEX]).group()) * 4096) / 1024 ** 3
        return round(wired_memory+active_memory, 2)
    
    def get_memory_used_percent(self):
        return (self.get_used_ram() / self.get_total_ram()) * 100.0

    def get_disk_stats(self):
        top_command = subprocess.run(['top', '-l 1', '-n 0'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

        total, used, free = shutil.disk_usage("/")

        read_written = top_command[9].split(':')[1].split(',')
        read = read_written[0].split(' ')[1]
        written = read_written[1].split(' ')[1]
        return dict(
            {
                'total_disk_space': round(total / 1024 ** 3, 1),
                'used_disk_space': round(used / 1024 ** 3, 1),
                'free_disk_space': round(free / 1024 ** 3, 1),
                'read_write': {
                    'read': read,
                    'written': written
                }
            }
        )
    
    def get_all_system_statistics(self):
        return dict(
            {
                'cpu_count': self.get_cpu_count(), 
                'cpu_load': self.get_cpu_load(),
                'cpu_percent': self.get_cpu_percent(),
                'ram': {
                    'total_ram': self.get_total_ram(),
                    'used_ram': self.get_used_ram(),
                    'memory_used_percent': self.get_memory_used_percent()
                },
                'disk': self.get_disk_stats()
            }
        )
