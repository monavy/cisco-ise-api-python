import re
import requests
import json
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def json_pretty_print(json_dict):
    """pretty print json data"""
    return json.dumps(json_dict,
                      indent=2,
                      sort_keys=True)

def get_endpoint_list(creds,mac_add):
    '''get list of endpoints that match criteria'''
    #rest_url = creds.get('ise_server') + '/ers/config/endpoint?filter=mac.CONTAINS.' + str(mac_add) + '&size=100&page=1'
    rest_url = creds.get('ise_server') + '/ers/config/endpoint?filter=mac.CONTAINS.' + str(mac_add)

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    #r = None
    try:
        r = None
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), headers=headers, verify=False)
        r.close()
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            #print json_pretty_print(r_json)
            return r_json
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return get_endpoint_list(creds,mac_add)
        pass


def get_endpoint(creds,mac_add):
    '''get list of endpoints that match criteria'''
    rest_url = creds.get('ise_server') + '/ers/config/endpoint?filter=mac.EQ.' + str(mac_add)

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    r = None
    try:
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), headers=headers, verify=False)
        r.close()
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return r_json
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return get_endpoint(creds,mac_add)
        pass


def get_endpoint_group(creds,gid):
    '''get endpoint group details'''
    rest_url = creds.get('ise_server') + '/ers/config/endpointgroup/' + str(gid)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    try:
        r = None
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), headers=headers, verify=False)
        r.close()
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return r_json
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return get_endpoint_group(creds,gid)
        pass


def search_group_id(creds,gid_name):
    '''searching a group id by group name'''
    rest_url = creds.get('ise_server') + '/ers/config/endpointgroup?filter=name.EQ.' + str(gid_name)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    r = None
    try:
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), headers=headers, verify=False)
        r.close()
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return r_json
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return search_group_id(creds,gid_name)
        pass

def get_endpoint_by_id(creds,eid):
    '''get endpoint details by its id'''
    rest_url = creds.get('ise_server') + '/ers/config/endpoint/' + str(eid)
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    r = None
    try:
        r = requests.get(url=rest_url, auth=(creds.get('ise_user'), creds.get('ise_pass')), headers=headers, verify=False)
        r.close()
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return r_json
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return get_endpoint_by_id(creds,eid)
        pass


def create_endpoint(creds_edit,creds_read,mac_add,role,desc):
    rest_url = creds_edit.get('ise_server') + '/ers/config/endpoint'
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    '''get group_id from group name'''
    gid = None
    group_json = search_group_id(creds_read,role)

    '''should only return one group object'''
    '''otherwise put it in the unknown group'''
    if group_json.get('SearchResult').get('total') == 1:
        for group in group_json.get('SearchResult').get('resources'):
            gid = group.get('id')
    else:
        group_json = search_group_id(creds_read,'Unknown')
        for group in group_json.get('SearchResult').get('resources'):
            gid = group.get('id')

    '''construct object payload to submit'''
    payload = {
            "ERSEndPoint" : {
                "id" : "",
                "name" : mac_add,
                "description" : desc,
                "mac" : mac_add,
                "staticProfileAssignment" : False,
                "groupId" : gid,
                "staticGroupAssignment" : True,
            }
    }

    print json_pretty_print(payload)
    try:
        r = None
        r = requests.post(url=rest_url, 
                          auth=(creds_edit.get('ise_user'), creds_edit.get('ise_pass')), 
                          headers=headers, 
                          data=json.dumps(payload), 
                          verify=False)
        r.close()
        r_json = r.json()
    except Exception, e:
        error = e
        #print error
        if 'Max retries exceeded' in str(error):
            time.sleep(.500)
            return create_endpoint(creds_edit,creds_read,mac_add,role,desc)
        pass

    '''successful submit returns nothing'''
    '''this one is to handle records arealy present'''
    try:
        if r_json:
            return r_json.get('ERSResponse').get('messages')
    except Exception, e:
        error2 = e

def search_endpoint_by_mac(creds,mac_add):
    '''   '''
    try:
        '''get potential list of matches'''
        r_json = get_endpoint_list(creds,mac_add)
    except Exception, e:
        error = e
        #print error
        pass
    
    r = None
    try:
        if r_json.get('SearchResult').get('total') >= 1:
            result_list = []
            for endpoint in r_json.get('SearchResult').get('resources'):
                eid = None
                eid = str(endpoint.get('id'))
                if eid:
                    try:
                        '''get endpoint details'''
                        eid_json = get_endpoint_by_id(creds,eid)
                        #print json_pretty_print(eid_json)
                        result_list.append(eid_json)

                    except Exception, e:
                        error = e
                        pass

            return result_list 
            #print str(result_list)

        else:
            print '\n ' + str(mac_add) + ' not found\n'
            if 'text' in r_json:
                print r_json['text']


    except Exception, e:
        error = e
        #print error
        pass

def delete_endpoint_by_mac(creds_edit,creds_read,mac_add):
    '''   '''
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    try:
        '''get potential matche'''
        endpoint_json = get_endpoint(creds_read,mac_add)
    except Exception, e:
        error = e
        #print error
        pass

    if endpoint_json.get('SearchResult').get('total') >= 1:
            for endpoint in endpoint_json.get('SearchResult').get('resources'):
                eid = None
                eid = str(endpoint.get('id'))
                if eid:
                    try:
                        r = None
                        rest_url = creds_edit.get('ise_server') + '/ers/config/endpoint/' + str(eid)
                        r = requests.delete(url=rest_url,auth=(creds_edit.get('ise_user'), creds_edit.get('ise_pass')),headers=headers, verify=False)
                        r.close()
                        r_json = r.json()

                    except Exception, e:
                        error = e
                        if 'Max retries exceeded' in str(error):
                            time.sleep(.500)
                            return delete_endpoint_by_mac(creds_edit,creds_read,mac_add)
                        pass

                    print str(mac_add) + ' marked for deletion.\n'
                    #return str(mac_add) + ' marked for deletion.\n'

    else:
        print '\n ' + str(mac_add) + ' not found\n'
        if 'text' in endpoint_json:
            print endpoint_json['text']
        #else:
        #    r.raise_for_status()


def update_endpoint(creds_edit,creds_read,mac_add,role,desc):
    '''get group_id from group name'''
    gid = None
    group_json = search_group_id(creds_read,role)

    '''should only return one group object'''
    '''otherwise put it in the unknown group'''
    if group_json.get('SearchResult').get('total') == 1:
        for group in group_json.get('SearchResult').get('resources'):
            gid = group.get('id')
    else:
        group_json = search_group_id(creds_read,'Unknown')
        for group in group_json.get('SearchResult').get('resources'):
            gid = group.get('id')

    '''   '''
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'cache-control': "no-cache",
        }

    try:
        '''get potential match'''
        endpoint_json = get_endpoint(creds_read,mac_add)
    except Exception, e:
        error = e
        #print error
        pass

    if endpoint_json.get('SearchResult').get('total') >= 1:
            for endpoint in endpoint_json.get('SearchResult').get('resources'):
                eid = None
                eid = str(endpoint.get('id'))
                if eid:

                    payload = {
                        "ERSEndPoint" : {
                            #"name" : mac_add,
                            "description" : desc,
                            #"mac" : mac_add,
                            "staticProfileAssignment" : False,
                            "groupId" : gid,
                            "staticGroupAssignment" : True,
                        }
                    }

                    try:
                        r = None
                        rest_url = creds_edit.get('ise_server') + '/ers/config/endpoint/' + str(eid)
                        r = requests.put(url=rest_url,
                                         auth=(creds_edit.get('ise_user'),
                                         creds_edit.get('ise_pass')),
                                         headers=headers,
                                         data=json.dumps(payload), 
                                         verify=False)
                        r.close()
                        r_json = r.json()

                    except Exception, e:
                        error = e
                        if 'Max retries exceeded' in str(error):
                            time.sleep(.500)
                            return update_endpoint(creds_edit_creds_read,mac_add,role,desc)
                        pass

                    to_update = None
                    to_update = get_endpoint_by_id(creds_read,eid)
                    return to_update

    else:
        print '\n ' + str(mac_add) + ' not found\n'
        if 'text' in endpoint_json:
            print endpoint_json['text']
