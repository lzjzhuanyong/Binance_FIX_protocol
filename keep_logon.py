from datetime import datetime, timezone
from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC

import os
import base64
import socket
import ssl
import random
import string


def get_time():
    return datetime.now(timezone.utc).strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

def sign(payload):
    sign = eddsa.new(private_key,'rfc8032')
    sign_data = sign.sign(payload.encode("ASCII"))                        # 签名
    signature = base64.b64encode(sign_data).decode('ASCII')  
    return signature

def get_final_message(fix_message):
    
    temp_str = f"8=FIX.4.4|9={len(fix_message)}|" + fix_message
    chesum = sum(ord(char) for char in temp_str.replace('|','\x01'))
    final_msg = temp_str + f"10={chesum%256:03}|"

    return final_msg.replace('|','\x01')



api_key = ""

dir = os.path.dirname(__file__)
f = open(dir+"/private_key.pem", "rb")
private_key = f.read()                                # 获取私钥
private_key = ECC.import_key(private_key)



utc_timestamp = get_time()
sender_comp_id=''.join(random.sample(string.ascii_letters + string.digits,8))
target_comp_id='SPOT'
msg_seq_num=1
payload = chr(1).join(['A',sender_comp_id,target_comp_id,str(msg_seq_num),utc_timestamp])
signature = sign(payload)

fix_message=(f"35=A|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34=1|"f"52={utc_timestamp}|"
f"95={len(signature)}|"f"96={signature}|"f"98=0|"f"108=10|"f"141=Y|"f"553={api_key}|"f"25035=2|")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock)
ssl_sock.connect(('fix-oe.testnet.binance.vision', 9000))

send_msg = get_final_message(fix_message)
print(type(send_msg.encode('ASCII')))
print("send: ",send_msg.replace('\x01','|'))
# send logon message
ssl_sock.sendall(send_msg.encode('ASCII'))
msg_seq_num += 1
# get response


while True:

    response = ssl_sock.recv(4096)

    if response:
        
        data_str = response.decode('ASCII')
        print("recv: ",data_str.replace("\x01","|"))
        data_list = data_str.split('\x01')

        if data_list[2] == '35=1':  # send Heartbeat to keep connected
            TestReqID = data_list[-3]
            #print(TestReqID)
            fix_message=(f"35=0|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"f"{TestReqID}|")
            send_msg = get_final_message(fix_message)
            print("send: ",send_msg.replace('\x01','|'))
            ssl_sock.sendall(send_msg.encode('ASCII'))
            msg_seq_num += 1
            
