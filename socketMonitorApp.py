import queue
import FIXapi
import threading
from urllib.parse import urlparse

import tkinter as tk

import tkinter.messagebox as msgbox


class socketMonitorApp:
    def __init__(self,root,display_message):
        
        self.root = root
        self.display_message = display_message

        self.message_queue = queue.Queue()
        self.sock = None
        
        self.sender_comp_id = ''
        self.target_comp_id = ''
        self.msg_seq_num = 1
        

    def socket_listener(self):
            
        while True:
            try:
                response = self.sock.recv(4096)
                if response:
                    self.message_queue.put(response.decode('ASCII'))
                    print("recv: ",response.decode('ASCII').replace("\x01","|"))
            except Exception as e:
                print(e)
                break

    def check_queue(self):
        try:
            msg = self.message_queue.get_nowait()
            show = "> recv: "+msg.replace('\x01','|')+'\n'
            self.display_message.insert(tk.END,show)

            data_list = msg.split('\x01')
            

            if data_list[2] == '35=1':  # send Heartbeat to keep connected
                TestReqID = data_list[-3]
                #print(TestReqID)
                heartBeat_msg = FIXapi.heartBeat(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, TestReqID)
                print("send: ",heartBeat_msg.replace("\x01","|"))

                self.sock.sendall(heartBeat_msg.encode('ASCII'))
                self.msg_seq_num += 1

                show = "> send: "+heartBeat_msg.replace('\x01','|')+'\n'
                self.display_message.insert(tk.END,show)

            elif data_list[2] == '35=5':
                self.sock.close()
                self.sock = None
                

        except queue.Empty:
            pass

        self.root.after(200, self.check_queue)


    def connect_fixapi(self,baseurl_input,apikey_input,privatekey_input):
        try:
            hostname, port = (urlparse(baseurl_input.get()).hostname,urlparse(baseurl_input.get()).port)
        
        except:
            msgbox.showerror(title='Error',message='Please provide correct URL!')

        apikey = apikey_input.get()
        
        privatekey = privatekey_input.get('1.0','end')
    
        self.sock = FIXapi.connect(hostname,port)
        login_msg, self.sender_comp_id, self.target_comp_id, self.msg_seq_num = FIXapi.logon_message(apikey,privatekey)
        print("send: ",login_msg.replace("\x01","|"))
        
        self.sock.sendall(login_msg.encode('ASCII'))
        self.msg_seq_num += 1
        show = "> send: "+login_msg.replace('\x01','|')+'\n'
        
        self.display_message.insert(tk.END,show)

        thread = threading.Thread(target=self.socket_listener, daemon=True)
        thread.start()

        self.check_queue()


    def disconnect_fixapi(self):
        logout_msg = FIXapi.logout_message(self.sender_comp_id, self.target_comp_id, self.msg_seq_num)
        print("send: ",logout_msg.replace("\x01","|"))
        
        self.sock.sendall(logout_msg.encode('ASCII'))
        self.msg_seq_num += 1
        show = "> send: "+logout_msg.replace('\x01','|')+'\n'
        
        self.display_message.insert(tk.END,show)
        
        
        

    def sending(self, msg_type, parametersList):

        if self.sock:
            send_message = ''
            for param in parametersList:
                
                if parametersList[param].get():
                    send_message = send_message + param + '=' + parametersList[param].get() + '|'
            

            if msg_type == 'NewOrderSingle<D>':
                NewOrderSingle_msg = FIXapi.NewOrderSingle(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",NewOrderSingle_msg.replace("\x01","|"))
            
                self.sock.sendall(NewOrderSingle_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+NewOrderSingle_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

            elif msg_type == "OrderCancelRequest<F>":
                OrderCancelRequest_msg = FIXapi.OrderCancelRequest(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",OrderCancelRequest_msg.replace("\x01","|"))
            
                self.sock.sendall(OrderCancelRequest_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+OrderCancelRequest_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)
            
            elif msg_type == "OrderCancelRequestAndNewOrderSingle<XCN>":
                OrderCancelRequestAndNewOrderSingle_msg = FIXapi.OrderCancelRequestAndNewOrderSingle(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",OrderCancelRequestAndNewOrderSingle_msg.replace("\x01","|"))
            
                self.sock.sendall(OrderCancelRequestAndNewOrderSingle_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+OrderCancelRequestAndNewOrderSingle_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

            elif msg_type == "OrderMassCancelRequest<q>":
                OrderMassCancelRequest_msg = FIXapi.OrderMassCancelRequest(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",OrderMassCancelRequest_msg.replace("\x01","|"))
            
                self.sock.sendall(OrderMassCancelRequest_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+OrderMassCancelRequest_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)


            elif msg_type == "NewOrderList<E>":
                NewOrderList_msg = FIXapi.NewOrderList(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",NewOrderList_msg.replace("\x01","|"))
            
                self.sock.sendall(NewOrderList_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+NewOrderList_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

            elif msg_type == "LimitQuery<XLQ>":
                LimitQuery_msg = FIXapi.LimitQuery(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",LimitQuery_msg.replace("\x01","|"))
            
                self.sock.sendall(LimitQuery_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+LimitQuery_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

            elif msg_type == "InstrumentListRequest<x>":
                InstrumentListRequest_msg = FIXapi.InstrumentListRequest(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",InstrumentListRequest_msg.replace("\x01","|"))
            
                self.sock.sendall(InstrumentListRequest_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+InstrumentListRequest_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

            elif msg_type == "MarketDataRequest<V>":
                MarketDataRequest_msg = FIXapi.MarketDataRequest(self.sender_comp_id, self.target_comp_id, self.msg_seq_num, send_message)
                print("send: ",MarketDataRequest_msg.replace("\x01","|"))
            
                self.sock.sendall(MarketDataRequest_msg.encode('ASCII'))
                self.msg_seq_num += 1
                show = "> send: "+MarketDataRequest_msg.replace('\x01','|')+'\n'
                
                self.display_message.insert(tk.END,show)

        
        else:
            msgbox.showerror(title='Error',message='Establish connection first!')
