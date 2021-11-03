import pytest
import json
from requests import post, exceptions
import re
import os
import time
from datetime import datetime


#serial = '53434F4D1A01D7CC'
#serial = '48575443B47ACD9F'
#serial = '49534B5461267888'
#serial = '52544B4702700010'
#serial = '51544543B3C97288'
serial = '48575443463C9EA3'
#serial = '454C545887000238'
#serial = '48575443463C79A3'


acs_url_reutov = {'get_rpc': 'http://78.37.124.122:8050/rtk/CPEManager/DMInterfaces/rest/v1/action/GetRPCMethods', 
            'fr': 'http://78.37.124.122:8050/rtk/CPEManager/DMInterfaces/rest/v1/action/FactoryReset',
            'activate_hsi': 'http://78.37.124.122:8050/rtk/WSSS/rest/v1/action/diagnose_Layer2Bridging', 
            'activate_iptv': 'http://78.37.124.122:8050/rtk/WSSS/rest/v1/action/diagnose_Layer2Bridging', 
            'spw': 'http://172.17.87.238:9673/rtk/CPEManager/DMInterfaces/rest/v1/action/SetParameterValues', 
            'gpw': 'http://172.17.87.238:9673/rtk/CPEManager/DMInterfaces/rest/v1/action/GetParameterValues', 
            'ppp_down': 'http://172.17.87.238:9673/rtk/CPEManager/DMInterfaces/rest/v1/action/SetParameterValues', }

acs_url_nwt = {'get_rpc': 'http://10.160.191.12:4673/live/CPEManager/DMInterfaces/rest/v1/action/GetRPCMethods', 
            'fr': 'http://10.160.191.12:4673/live/CPEManager/DMInterfaces/rest/v1/action/FactoryReset',
            'activate_hsi': 'http://10.160.191.12:4673/live/CPEManager/AXServiceStorage/Interfaces/rest/v1/action/activate_HSI', 
            'activate_iptv': 'http://10.160.191.12:4673/live/CPEManager/AXServiceStorage/Interfaces/rest/v1/action/activate_IPTV', 
            'spw': 'http://10.160.191.12:4673/live/CPEManager/DMInterfaces/rest/v1/action/SetParameterValues', 
            'gpw': 'http://10.160.191.12:4673/live/CPEManager/DMInterfaces/rest/v1/action/GetParameterValues', 
            'ppp_down': 'http://10.160.191.12:4673/live/CPEManager/DMInterfaces/rest/v1/action/SetParameterValues', }

post_fields_reutov = {'get_rpc': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync": 1, "Lifetime": 60}}' % serial)), 
                'fr': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync": 1, "Lifetime": 60}}' % serial)),
                'sa_pwd': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.LANConfigSecurity.ConfigPassword", "value": "1029384756"}]}' % serial)),
                'ppp_down': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Enable", "value": 0}]}' % serial)),
                'ppp_up': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Enable", "value": 1}]}' % serial)),
                'get_ext_ip': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": ["InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress"]}' % serial)),
                'get_tree': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": ["InternetGatewayDevice."]}' % serial)),
                'activate_hsi': json.loads(json.dumps('{"ServiceIdentifiers": {"cpeid": "%s"}, "DiagnosticTests": ["nicko_PPPoE_LAN1_LAN2_SSID1_SSID5"], "CommandOptions": {}, "DiagnosticTestsGroups": []}' % serial)),
                'activate_iptv': json.loads(json.dumps('{"ServiceIdentifiers": {"cpeid": "%s"}, "DiagnosticTests": ["nicko_IPTV_3-4"], "CommandOptions": {}, "DiagnosticTestsGroups": []}' % serial)), }

post_fields_nwt = {'get_rpc': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync": 1, "Lifetime": 60}}' % serial)), 
                'fr': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync": 1, "Lifetime": 60}}' % serial)),
                'sa_pwd': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.LANConfigSecurity.ConfigPassword", "value": "1029384756"}]}' % serial)),
                'ppp_down': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Enable", "value": 0}]}' % serial)),
                'ppp_up': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": [{"key": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Enable", "value": 1}]}' % serial)),
                'get_ext_ip': json.loads(json.dumps('{"CPEIdentifier": {"cpeid": "%s"}, "CommandOptions": {"Sync":1, "Lifetime":60}, "Parameters": ["InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress"]}' % serial)),
                'activate_hsi': json.loads(json.dumps('{"ServiceIdentifiers": {"cpeid": "%s", "cid": "123", "cid2": "MA5680T", "portNumber": 1, "portType": "ETH"}, "CommandOptions": {"Lifetime": 0, "Retry": 5}, "ServiceParameters": {"connectionType": "Routing", "password": "rtk", "username": "rtk", "portType": "ETH", "portNumber": 1}}' % serial)),
                'activate_iptv': json.loads(json.dumps('{"ServiceIdentifiers": {"cpeid": "%s", "cid": "123", "cid2": "MA5680T", "portNumber": 1, "portType": "ETH"}, "CommandOptions": {"Lifetime": 0, "Retry": 5}, "ServiceParameters": {"portType": "ETH", "portNumber": 1}}' % serial)),}              

headers = {'header': json.loads('{"Content-Type":"application/json"}'),}

acs = {
    'reutov': {
        'username': 'nwt',
        'password': 'testlab123',
    },
    'nwt': {
        'username': 'user',
        'password': 'password',
    }
}

@pytest.fixture()
def acs_wait():
    i = 10
    while (i > 0):
        try:
            req = post(acs_url_reutov['get_rpc'], post_fields_reutov['get_rpc'], headers=headers['header'], auth=(acs['reutov']['username'], acs['reutov']['password']), timeout=20)
        except exceptions.Timeout:
            req = {'ERROR': '500', 'Reason': 'ONT is not on ACS'}
        print('RESULT')
        print(req)
        print('------------------')
        if "200" in str(req):
            i = 0
        else:
            time.sleep(10)
            i -= 1
    yield req

def gen_filename(pattern_name, pattern_ext):
        while True:
            pattern = '{}-{}.{}'
            t = int(time.time() * 1000)

            yield pattern.format(pattern_name, str(t), pattern_ext)

@pytest.mark.acs_connect
def test_acs_connect():
    time.sleep(10)
    i = 10
    while (i > 0):
        try:
            req = post(acs_url_reutov['get_rpc'], post_fields_reutov['get_rpc'], headers=headers['header'], auth=(acs['reutov']['username'], acs['reutov']['password']))
            print('RESULT')
            print(req.json())
            print('------------------')
            if "200" in str(req):
                i = 0
            else:
                time.sleep(5)
                i -= 1
                print('{} tries left'.format(i))
        except Exception as e:
            time.sleep(5)
            i -= 1
            print('{} tries left'.format(i))
    assert "200" in str(req)


def test_compare_tree(acs_wait):

    try:
        req = post(acs_url_reutov['gpw'], post_fields_reutov['get_tree'], headers=headers['header'], auth=(acs['reutov']['username'], acs['reutov']['password']))
        #print(req.json())
    except exceptions.Timeout:
        return "ERROR", {'ERROR': '500', 'Reason': 'ONT is not on ACS'}, None
    
    values = {}
    param_value = 'empty'
    param_key = 'empty'
    if acs_url_reutov['gpw'].find('GetParameterValues') != -1:
        with open('tr_tree.txt', 'w') as tr_tree:
            for key in req.json():
                for key2 in req.json()[key]:
                    if key2 == 'details':
                        for key3 in req.json()[key][key2]:
                            for key, value in key3.items():
                                if key == 'key':
                                    param_key = value
                                    value1 = ''.join([value, '\n'])
                                    tr_tree.write(value1)
                                elif key == 'value':
                                    param_value = value
                                if (param_key != 'empty') and (param_value != 'empty'):
                                    values[param_key] = param_value
                                    param_value = 'empty'
                                    param_key = 'empty'
        with open('tr_tree.txt', 'r') as tr_tree:
            tr_lines_s = []
            tr_lines = tr_tree.readlines()
            for line in tr_lines:
                    line_s = re.search(r'.*\.(\w+)$', line)
                    if line_s != None:
                        line_s = line_s.group(1)
                        tr_lines_s.append(line_s)
        with open('default_tree.txt', 'r') as default_tree:
                default_lines = default_tree.readlines()
#		default_lines = default_tree_low.readlines()

        txt_file = (('./result/diff_tree_' + '%s_'  + str(datetime.now().strftime('%d%m%Y')) + '.txt') %serial)
        valid = True
        with open(txt_file, 'w') as diff_tree:
            for line in default_lines:
                param = re.search(r'.*\.(\w+)$', line)
                if param != None:
                    param = param.group(1)
                    if param not in tr_lines_s:
                        diff_tree.write(line)
                        valid = False
                        print(line)
        print(len(tr_lines))
        assert len(tr_lines) > 0
