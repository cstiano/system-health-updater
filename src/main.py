#!/usr/local/bin/python

from extractor.healthExtractor import healthExtractor
from communication.healthService import healthService
import sys

BASE_URL = sys.argv[1]
ROUTE = sys.argv[2]

if __name__ == "__main__":
    healthService = healthService(BASE_URL, ROUTE)
    healthExtractor = healthExtractor(cpu_time_analyzes=10)

    while(True):
        systemHealthInfo = healthExtractor.get_all_system_statistics()
        response, error = healthService.post(systemHealthInfo)
        if error != None:
            print("System Health Updater Bad URL Format")
            sys.exit()
            