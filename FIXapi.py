from datetime import datetime, timezone
from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC


import base64
import socket
import ssl
import random
import string
import uuid



def get_time():
    return datetime.now(timezone.utc).strftime('%Y%m%d-%H:%M:%S.%f')[:-3]


def sign(payload,private_key):
    sign = eddsa.new(private_key,'rfc8032')
    sign_data = sign.sign(payload.encode("ASCII"))                        # 签名
    signature = base64.b64encode(sign_data).decode('ASCII')  
    return signature


def get_final_message(fix_message):
    
    temp_str = f"8=FIX.4.4|9={len(fix_message)}|" + fix_message
    chesum = sum(ord(char) for char in temp_str.replace('|','\x01'))
    final_msg = temp_str + f"10={chesum%256:03}|"

    return final_msg.replace('|','\x01')


def logon_message(apikey, prvkey): 
    api_key = apikey
    private_key = prvkey                             # 获取私钥
    private_key = ECC.import_key(private_key)

    utc_timestamp = get_time()
    sender_comp_id=''.join(random.sample(string.ascii_letters + string.digits,8))
    target_comp_id='SPOT'
    msg_seq_num=1
    payload = chr(1).join(['A',sender_comp_id,target_comp_id,str(msg_seq_num),utc_timestamp])
    signature = sign(payload,private_key)

    fix_message=(f"35=A|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={utc_timestamp}|"
    f"95={len(signature)}|"f"96={signature}|"f"98=0|"f"108=60|"f"141=Y|"f"553={api_key}|"f"25035=1|")
    send_msg = get_final_message(fix_message)
    return (send_msg, sender_comp_id, target_comp_id, msg_seq_num)



def logout_message(sender_comp_id, target_comp_id, msg_seq_num):
    fix_message=(f"35=5|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"f"58={uuid.uuid4()}|")
    send_msg = get_final_message(fix_message)
    return send_msg



def heartBeat(sender_comp_id, target_comp_id, msg_seq_num, TestReqID):
    fix_message=(f"35=0|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"f"{TestReqID}|")
    send_msg = get_final_message(fix_message)
    
    return send_msg



def connect(hostname, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)

    ssl_sock.connect((hostname,port))

    return ssl_sock
    


def NewOrderSingle(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=D|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg


def OrderCancelRequest(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=F|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg


def OrderCancelRequestAndNewOrderSingle(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=XCN|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg

def OrderMassCancelRequest(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=q|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg

def NewOrderList(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=E|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg

def LimitQuery(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=XLQ|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg

def InstrumentListRequest(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=x|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg

def MarketDataRequest(sender_comp_id,target_comp_id, msg_seq_num, msg):
    fix_message = (f"35=V|"f"49={sender_comp_id}|"f"56={target_comp_id}|"f"34={msg_seq_num}|"f"52={get_time()}|"+msg)
    send_msg = get_final_message(fix_message)
    return send_msg
