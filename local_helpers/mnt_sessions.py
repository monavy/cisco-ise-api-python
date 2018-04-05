import re
import requests
import json
import time
import xml.etree.ElementTree as et

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def json_pretty_print(json_dict):
    """pretty print json data"""
    return json.dumps(json_dict,
                      indent=2,
                      sort_keys=True)


def get_session_by_ip(creds,ip_add):
    '''get list of endpoints that match criteria'''
    rest_url = creds.get('ise_server') + '/admin/API/mnt/Session/EndPointIPAddress/' + str(ip_add)

    r = None
    try:
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), verify=False)
        r.close()
        if r.status_code == 200 or r.status_code == 201:
            return r.content
    except Exception, e:
        #error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.300)
            return get_session_by_ip(creds,ip_add)
        pass

def reauth_session(creds,session):
    '''port reauth-disconnect actions'''
    '''(0) - default - re-auth'''
    '''(1) - re-auth with port-bounce'''
    '''(2) - re-auth with port-shut - NOT A GOOD IDEA! '''
    action = str('0') 

    rest_url = '{}{}{}{}{}{}{}'.format(
                  creds.get('ise_server'),
                  '/admin/API/mnt/CoA/Disconnect/',
                  str(session.get('psn_server')) + '/',
                  str(session.get('endpoint_mac')) + '/',
                  str(action) + '/',
                  str(session.get('switch_ip')) + '/',
                  str(session.get('endpoint_ip'))
               )

    r = None
    try:
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), verify=False)
        r.close()
        if r.status_code == 200 or r.status_code == 201:
            return r.content

    except Exception, e:
        #error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.300)
            return reauth_session(creds,session)
        pass

