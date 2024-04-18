from datetime import datetime
import mysql.connector
from xml.parsers.expat import ExpatError

conn = mysql.connector.connect(host='127.0.0.1', password = 'AATricks372!', user= 'root')
db_cursor = conn.cursor()
db_cursor.execute("USE npci")

# Execute a SELECT query to retrieve data from the npci_resp_table
db_cursor.execute("SELECT * FROM npci_resp_table")
print('database created')
rows = db_cursor.fetchall()

import xmltodict
import json
i = 1
# Process the retrieved data
data_passbook = []
for row in rows:
    user_txndata = {}
    xml_data = row[2]
    try:
        json_data = xmltodict.parse(xml_data)
        json_data_dump = json.dumps(json_data)
        json_data_loads = json.loads(json_data_dump)
        print(json_data_loads)
        if 'ns2:RespPay' in json_data_loads:
            if json_data_loads['ns2:RespPay']['Resp']['@result'] == 'SUCCESS':
                cust_ref = json_data_loads['ns2:RespPay']['Txn']['@custRef']
                ts = json_data_loads['ns2:RespPay']['Txn']['@ts']
                dt_object = datetime.fromisoformat(ts)
                # Convert datetime object to desired format
                normal_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                org_amount = json_data_loads['ns2:RespPay']['Resp']['Ref'][0]['@orgAmount']
                purpose = json_data_loads['ns2:RespPay']['Txn']['@purpose']
                txn_result = json_data_loads['ns2:RespPay']['Resp']['@result']
                # bal_amount = json_data_loads['ns2:RespPay']['Resp']['Ref'][1]['@balAmt']
                if purpose == '22':
                    purpose = 'Dr'
                elif purpose == '23':
                    purpose = 'Cr'
                # print(i," CustRef respay:", cust_ref)
                # print(ts)
                # print('org amount', org_amount)
                # print("purpose:", purpose)
                # print(txn_result)
                user_txndata= {
                    's_no.': i,
                    'db_s_no':row[0],
                    'cust_ref':cust_ref,
                    'ts':ts,
                    'org_amount':org_amount,
                    'purpose':purpose,
                    # 'bal_amount':bal_amount
                }
                data_passbook.append(user_txndata)
                i = i+1
                
            elif 'ns2:Ack' in json_data_loads:
                cust_ref = 'NA'
                # print("CustRef Ack:", cust_ref)
            # print(i)
    except ExpatError as e:
        print(f"Error parsing XML data: {e}")
print(data_passbook)

# cust_refs = [row[0] for row in rows]
# txn_id = [row[1] for row in rows]
# print(cust_refs)
# print(txn_id)
