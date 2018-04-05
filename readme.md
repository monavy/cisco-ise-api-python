# Quick Start Guide 

## Pre-requisites

- ISE API Admin credentials
  1) under Administration->Admin Access->Administrators->Admin Users
     - create an API Admin account with:
     "MnT Admin" and "ERS Admin" group rights

  2) under Administration->Sytem->Settings
     - Enable ERS for Read/Write on Admin Node
     - Enable ERS for Read in all Other Nodes
       (note: at the moment, ERS API read/write actions are limited to
        only ten (10) concurrent connections, use the other
        nodes for read actions and leave the admin node
        for write/update/delete actions)

  3) need target Endpoint Groups from ISE
     - Guest
     - Unknown
     - RegisteredDevices
     - ETC..

## ISE Personas and ERS API Admin Credentials 

- edit "local_helpers/accounts_db.py" with the correct ise admin credentials
  and correct PAN and MNT node urls


## Usage

- chmod +x *.py

- ./create_endpoint.py source_endpoint_list.csv 
- ./update_endpoint.py source_endpoint_list.csv 
- ./delete_endpoint.py source_endpoint_list.csv 
- ./import_endpoint_from_nac.py source_endpoint_from_nac_export.csv 

- ./search_endpoint_by_mac.py  39:c9:86:14:41:00
- ./get_session_by_ip.py 10.10.46.3 
- ./reauth_session_by_ip.py 10.10.46.3 
- ./get_mac_from_session_by_ip.py 10.10.46.3
