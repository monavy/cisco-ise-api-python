#!/usr/bin/env python
import sys
import random
import json
import xml.etree.ElementTree as et
from local_helpers import accounts_db, mnt_sessions 

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        sys.exit('\nusage: ./script.py <ip_address>\n')

    ip_address = str.strip(sys.argv[1])
    ip_address = ip_address.lower()


    '''get credentials from accounts_db'''
    try:
        creds = random.choice(accounts_db.accounts_mnt)
    except Exception, e:
        print e
        sys.exit()

    endpoint_session = None
    try:
        results = mnt_sessions.get_session_by_ip(creds,ip_address)
        if results:
            root = et.fromstring(results)
            s_token = None
            s_param = None
            for s_param in root.iter('sessionParameters'):
                '''construct object payload to submit'''
                s_token =  {
                            "endpoint_mac" : str(s_param.find('calling_station_id').text),
                            "endpoint_ip" : str(s_param.find('framed_ip_address').text),
                            "psn_server" : str(s_param.find('acs_server').text),
                            "switch_ip" : str(s_param.find('nas_ip_address').text),
                            "auth_timestamp" : str(s_param.find('auth_acs_timestamp').text),
                           } 

            if s_token:
                print mnt_sessions.json_pretty_print(s_token)

    except Exception as e:
        error = e
        print error
        pass

    

