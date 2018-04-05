#!/usr/bin/env python

import re
import sys
from local_helpers import accounts_db, utils_endpoint

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        sys.exit('\nusage: ./script.py <string>\n')

    mac_address = str.strip(re.sub(':|\.', '', sys.argv[1]))
    mac_address = mac_address.lower()

    if (len(mac_address) > 12):
        print 'Invalid MAC Address size'
        sys.exit()
    else:
        '''correct mac address format'''
        mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))


    '''get credentials from accounts_db'''
    creds_read = None
    try:
        for creds in accounts_db.accounts_pan:
            if creds.get('ise_role') == str('secondary'):
                creds_read = creds

    except Exception, e:
        print e
        sys.exit()

    try:
        results = utils_endpoint.search_endpoint_by_mac(creds,mac_address)
    except Exception, e:
        pass
        #print e
        #sys.exit()

    if results:
        for result in results:
            print utils_endpoint.json_pretty_print(result)
