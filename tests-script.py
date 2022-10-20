#!/usr/bin/env python3

import pyspeedtest
import platform
import datetime
import json
import time
import os

TEST_NB = 50
BROWSERS = ["safari"]
BASE_DIR='test_' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
SLEEP=60
IFACE = 'en0'

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
    
for i in range(TEST_NB):
    for b in BROWSERS:
        
        print("Iteration:", i+1, "Browser:", b )
        
        directory=BASE_DIR + '/{}_{}'.format(b,i)
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            #result = pyspeedtest.run_speedtest(browser=b, pcap_path="{}/trace.pcap".format(directory), pcap_iface=IFACE)
            result = pyspeedtest.run_speedtest(browser=b, pcap_path="/dev/null", pcap_iface=IFACE)
            result['browser'] = b
            result['iteration'] = i
            result['time'] = time.time()
            result['platform'] = platform.system()
            json.dump(result, open("{}/result.json".format(directory),"w"))
        except Exception as e:
            print ("Error:", e
                )
            
        time.sleep(SLEEP)