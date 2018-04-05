"""
This module is used to store creds.
"""
'''PANs - only primary can be used for read/write actions'''
'''       such as create, delete, update endpoints       '''
'''                                                      '''
'''Secondary PAN can be used for read-only actions       '''
'''                                                      '''
accounts_pan = [
    {
        'ise_server': 'https://ise-pan1.localdomain:9060',
        'ise_user': 'ersadmin',
        'ise_pass': 'ersAdminPassword',
        'ise_role': 'primary'
    },
    {
        'ise_server': 'https://ise-pan2.localdomain:9060',
        'ise_user': 'ersadmin',
        'ise_pass': 'ersAdminPassword',
        'ise_role': 'secondary'
    }
]

'''MNTs - all MNTs can be used for their related actions          '''
'''       such as quering endpoint sessions or sending CoA actions'''
'''                                                               '''
accounts_mnt = [
    {
        'ise_server': 'https://ise-mnt1.localdomain',
        'ise_user': 'ersadmin',
        'ise_pass': 'ersAdminPassword'
    },
    {
        'ise_server': 'https://ise-mnt2.localdomain',
        'ise_user': 'ersadmin',
        'ise_pass': 'ersAdminPassword'
    }
]

