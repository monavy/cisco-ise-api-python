#!/usr/bin/env python

import re
import os
import sys
import threading
import random
from local_helpers import accounts_db, utils_endpoint

if __name__ == "__main__":

    if (len(sys.argv) != 2):
        sys.exit('\nusage: ./script.py <source-list-file>\n')

    src_file_path = sys.argv[1]
    if os.path.exists(src_file_path):
        switch_list = src_file_path
    else:
        sys.exit('\nfile: ' + src_file_path + ' could not be found\n')


    '''get credentials from accounts_db'''
    creds_edit = None
    creds_read = None
    try:
        for creds in accounts_db.accounts_pan:
            if creds.get('ise_role') == str('primary'):
                creds_edit = creds
            if creds.get('ise_role') == str('secondary'):
                creds_read = creds

    except Exception, e:
        print e
        sys.exit()

    f = open(switch_list, "r")

    entry_list = []
    multi_thread = []

    for line_entry in iter(f):
        '''skip lines with comments'''
        if '#' in line_entry:
            next
        else:
            my_line = re.split('[,]+', re.sub('\n|\r','',line_entry))
            mac_add = my_line[0]
            role = my_line[1]
            desc = my_line[2]

            mac_address = str.strip(re.sub(':|\.', '', mac_add))
            mac_address = mac_address.lower()

            '''ISE does not take spaces. Replace space with a dash'''
            role = str.strip(re.sub(' ', '-', role))

            if (len(mac_address) != 12):
                print 'Invalid MAC Address: ' + str(mac_address)
            else:
                '''correct mac address format'''
                mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))

            results = None

            try:
                utils_endpoint.delete_endpoint_by_mac(creds_edit,creds_read,mac_address)
            #    thread_call = threading.Thread(
            #        target=utils_endpoint.delete_endpoint_by_mac,
            #        args=(creds_edit,creds_read,mac_address))
            #    multi_thread.append(thread_call)
            #    thread_call.start()
            except Exception, e:
                #print e
                pass
                #sys.exit()

    #"""wait for all threads to finish"""
    #for t in multi_thread:
    #    t.join()
