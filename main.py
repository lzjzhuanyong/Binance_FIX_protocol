import tkinter as tk
import tkinter.ttk as ttk
import time
import re

import socketMonitorApp

root = tk.Tk()

root.title('FIX API test tool')
root.geometry('800x600')


'--- Top ---'
frame_top = ttk.Frame(root)
frame_top.configure(borderwidth=2,relief='solid',height=260,width=900)
frame_top.pack(side="top",anchor='w')

notebook_style = ttk.Style()
notebook_style.theme_use('alt')
notebook_style.configure('Lefttab.TNotebook',anchor='w',padding=[10,5,10,5])

notebook = ttk.Notebook(frame_top,style='Lefttab.TNotebook',height=260, width=900)

note_frame1 = ttk.Frame()
note_frame2 = ttk.Frame()

notebook.add(note_frame1,text='message sending')
notebook.add(note_frame2,text='connection')

notebook.pack(fill='x',expand=True)



'''-------message sending frame---------'''
msg_chosen_frame = ttk.Frame(note_frame1,borderwidth=2,relief='solid')
msg_chosen_frame.pack(side='left', anchor='nw',fill='y')

label = ttk.Label(msg_chosen_frame,text="Application Message",width=34)
label.pack()
app_msgs = tk.Listbox(msg_chosen_frame,justify='left', selectmode='browse')

msg_item = ['NewOrderSingle<D>', 'OrderCancelRequest<F>','OrderCancelRequestAndNewOrderSingle<XCN>','OrderMassCancelRequest<q>',
            'NewOrderList<E>','LimitQuery<XLQ>','InstrumentListRequest<x>','MarketDataRequest<V>']

msg_chosen_sbar = ttk.Scrollbar(app_msgs, command=app_msgs.yview)
msg_chosen_sbar.pack(side='right', fill='y')
app_msgs.configure(activestyle="dotbox", yscrollcommand=msg_chosen_sbar.set)
for item in msg_item:
    app_msgs.insert(tk.END, item)
app_msgs.pack(expand=True, fill='both', side='top')


def on_select(event):
    global selected_msg_type
    selected_index = app_msgs.curselection()
    if selected_index:
        selected_item = app_msgs.get(selected_index[0])
        
        selected_msg_type = selected_item
        switch_frame(selected_item)

def switch_frame(frame_item):
    global current_container
    global current_scrollbar
    global current_params
    current_container.pack_forget()
    current_scrollbar.pack_forget()

    next_container,next_scrollbar, next_params = messages_list.get(frame_item)
    
    next_container.pack(side="left", fill="both", expand=True)
    next_scrollbar.pack(side="right", fill="y")
    current_container = next_container
    current_scrollbar = next_scrollbar
    current_params = next_params


app_msgs.bind("<<ListboxSelect>>",on_select)

parameter_bottom_frame = ttk.Frame(note_frame1, borderwidth=2, relief='solid', width=52)
parameter_bottom_frame.pack(side='left',fill='y',padx=5)

parameter_title_label = ttk.Label(parameter_bottom_frame,text='Parameters setting',font=('Arial', 12), width=52)
parameter_title_label.pack()


messages_list = {}


def NewOrderSingle_parameters():

    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["ClOrdID(11)","OrderQty(38)","OrdType(40)","ExecInst(18)","Price(44)",
                        "Side(54)","Symbol(55)","TimeInForce(59)","MaxFloor(111)","CashOrderQty(152)",
                        "TargetStrategy(847)","StrategyID(7940)","SelfTradePreventionMode(25001)",
                        "TriggerType(1100)","TriggerAction(1101)","TriggerPrice(1102)",
                        "TriggerPriceType(1107)","TriggerPriceDirection(1109)","TriggerTrailingDeltaBips(25009)",
                        "SOR(25032)"]
    

    parameters_list = {}
    
    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=26,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 16)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))

    messages_list['NewOrderSingle<D>'] = (container,scrollbar,parameters_list)

    return container,scrollbar,parameters_list

def OrderCancelRequest_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["ClOrdID(11)","OrigClOrdID(41)","Order ID(37)","OrigClListID(25015)","ListID(66)",
                        "Symbol(55)","CancelRestrictions(25002)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=26,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 16)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['OrderCancelRequest<F>'] = (container,scrollbar,parameters_list)

    return container,scrollbar, parameters_list

def OrderCancelRequestAndNewOrderSingle_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["OrderCancelRequestAndNewOrderSingleMode(25033)",
                        "OrderRateLimitExceededMode(25038)","OrderID(37)","CancelClOrdID(25034)","OrigClOrdID(41)",
                        "ClOrdID(11)","CancelRestrictions(25002)","OrderQty(38)","OrdType(40)","ExecInst(18)",
                        "Price(44)","Side(54)","Symbol(55)","TimeInForce(59)","MaxFloor(111)","CashOrderQty(152)",
                        "TargetStrategy(847)","StrategyID(7940)","SelfTradePreventionMode(25001)","TriggerType(1100)",
                        "TriggerAction(1101)","TriggerPrice(1102)","TriggerPriceType(1107)","TriggerPriceDirection(1109)",
                        "TriggerTrailingDeltaBips(25009)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=42,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 5)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['OrderCancelRequestAndNewOrderSingle<XCN>'] = (container,scrollbar,parameters_list)

    return container,scrollbar,parameters_list

def OrderMassCancelRequest_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["ClOrdID(11)","Symbol(55)","MassCancelRequestType(530)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=26,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 16)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['OrderMassCancelRequest<q>'] = (container,scrollbar,parameters_list)

    return container,scrollbar,parameters_list

def NewOrderList_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["ClListID(25014)","ContingencyType(1385)","NoOrders(73)",
                        "1_ClOrdID(11)","1_OrderQty(38)","1_OrdType(40)","1_ExecInst(18)","1_Price(44)","1_Side(54)","1_Symbol(55)","1_TimeInForce(59)",
                        "1_MaxFloor(111)","1_CashOrderQty(152)","1_TargetStrategy(847)","1_StrategyID(7940)","1_SelfTradePreventionMode(25001)",
                        "1_TriggerType(1100)","1_TriggerAction(1101)","1_TriggerPrice(1102)","1_TriggerPriceType(1107)","1_TriggerPriceDirection(1109)",
                        "1_TriggerTrailingDeltaBips(25009)","1_NoListTriggeringInstructions(25010)","1_ListTriggerType(25011)",
                        "1_ListTriggerTriggerIndex(25012)","1_ListTriggerAction(25013)",
                        "2_ClOrdID(11)","2_OrderQty(38)","2_OrdType(40)","2_ExecInst(18)","2_Price(44)","2_Side(54)","2_Symbol(55)","2_TimeInForce(59)",
                        "2_MaxFloor(111)","2_CashOrderQty(152)","2_TargetStrategy(847)","2_StrategyID(7940)","2_SelfTradePreventionMode(25001)",
                        "2_TriggerType(1100)","2_TriggerAction(1101)","2_TriggerPrice(1102)","2_TriggerPriceType(1107)","2_TriggerPriceDirection(1109)",
                        "2_TriggerTrailingDeltaBips(25009)","2_NoListTriggeringInstructions(25010)","2_ListTriggerType(25011)",
                        "2_ListTriggerTriggerIndex(25012)","2_ListTriggerAction(25013)",
                        "3_ClOrdID(11)","3_OrderQty(38)","3_OrdType(40)","3_ExecInst(18)","3_Price(44)","3_Side(54)","3_Symbol(55)","3_TimeInForce(59)",
                        "3_MaxFloor(111)","3_CashOrderQty(152)","3_TargetStrategy(847)","3_StrategyID(7940)","3_SelfTradePreventionMode(25001)",
                        "3_TriggerType(1100)","3_TriggerAction(1101)","3_TriggerPrice(1102)","3_TriggerPriceType(1107)","3_TriggerPriceDirection(1109)",
                        "3_TriggerTrailingDeltaBips(25009)","3_NoListTriggeringInstructions(25010)","3_ListTriggerType(25011)",
                        "3_ListTriggerTriggerIndex(25012)","3_ListTriggerAction(25013)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=30,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 14)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['NewOrderList<E>'] = (container,scrollbar,parameters_list)

    return container,scrollbar,parameters_list

def LimitQuery_parameters(var):
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["ReqID(6136)"]

    parameters_list = {}

    
    a = ttk.Label(table_frame,text=parameter_labels[0],font=('Arial', 12),width=26,anchor='center')
    a.grid(row=0,column=0)

    parameters_list[re.search(r'\((\d+)\)',parameter_labels[0]).group(1)] = ttk.Entry(table_frame, width = 16,textvariable=var)
    parameters_list[re.search(r'\((\d+)\)',parameter_labels[0]).group(1)].grid(row=0,column=1)
    



    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['LimitQuery<XLQ>'] = (container,scrollbar,parameters_list)

    return container,scrollbar, parameters_list

def InstrumentListRequest_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["InstrumentReqID(320)","InstrumentListRequestType(559)","Symbol(55)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=26,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 16)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['InstrumentListRequest<x>'] = (container,scrollbar,parameters_list)

    return container,scrollbar, parameters_list

def MarketDataRequest_parameters():
    container = tk.Canvas(parameter_bottom_frame)
    scrollbar = ttk.Scrollbar(parameter_bottom_frame, orient="vertical", command=container.yview)
    container.configure(yscrollcommand=scrollbar.set)

    table_frame = ttk.Frame(container)
    container.create_window((0, 0), window=table_frame, anchor="nw")


    parameter_labels = ["MDReqID(262)","SubscriptionRequestType(263)","MarketDepth(264)",
                        "AggregatedBook(266)","NoRelatedSym(146)","Symbol(55)","NoMDEntryTypes(267)","1_MDEntryType(269)","2_MDEntryType(269)"]

    parameters_list = {}

    for index in range(len(parameter_labels)):
        a = ttk.Label(table_frame,text=parameter_labels[index],font=('Arial', 12),width=26,anchor='center')
        a.grid(row=index,column=0)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)] = ttk.Entry(table_frame, width = 16)
        parameters_list[re.search(r'\((\d+)\)',parameter_labels[index]).group(1)].grid(row=index,column=1)


    table_frame.update_idletasks()
    container.config(scrollregion=container.bbox("all"))
    

    messages_list['MarketDataRequest<V>'] = (container,scrollbar,parameters_list)

    return container,scrollbar, parameters_list

current_container, current_scrollbar, current_params = NewOrderSingle_parameters()
current_container.pack(side="left", fill="both", expand=True)
current_scrollbar.pack(side="right", fill="y")
selected_msg_type = 'NewOrderSingle<D>'


OrderCancelRequest_parameters()
OrderCancelRequestAndNewOrderSingle_parameters()
OrderMassCancelRequest_parameters()
NewOrderList_parameters()

var = tk.StringVar(value=int(time.time()*1000))
LimitQuery_parameters(var)

InstrumentListRequest_parameters()
MarketDataRequest_parameters()


send_msg = ttk.Button(note_frame1,text="Send", padding=5, width=5, command=lambda: app.sending(selected_msg_type,current_params))
send_msg.pack(side='left',padx=5)


'''-------message sending frame end---------'''



'''----------connect frame-------'''
connect_frame = ttk.Frame(note_frame2)
connect_frame.pack(side='left', anchor='nw')
label_baseurl = tk.Label(connect_frame, text='Base URL:', font=('Arial', 12), width=25, height=2)
label_baseurl.grid(row=0,column=0,padx=25,rowspan=2)

init_value1 = tk.StringVar(value="tcp+tls://fix-oe.binance.com:9000")
baseurl_input = ttk.Entry(connect_frame,textvariable=init_value1, width=45)
baseurl_input.grid(row=0, column=1, padx=15, pady=15, ipady=5, rowspan=2, columnspan=2)

label_apikey = tk.Label(connect_frame, text='API KEY:', font=('Arial', 12), width=25, height=2)
label_apikey.grid(row=2, column=0, padx=25, rowspan=2)

init_value2 = tk.StringVar(value='')
apikey_input = ttk.Entry(connect_frame,textvariable=init_value2, width=45)
apikey_input.grid(row=2, column=1, padx=15, pady=15, ipady=5, rowspan=2, columnspan=2)


label_prvkey = tk.Label(connect_frame, text='PRIVATE KEY:', font=('Arial', 12), width=25, height=2)
label_prvkey.grid(row=4,column=0,padx=25,pady=15,rowspan=2,sticky='n')

privatekey_input = tk.Text(connect_frame, bg="#fff", width=58, height=4, relief='groove')


privatekey_input.grid(row=4, column=1, padx=16, pady=15, ipady=1, rowspan=2, columnspan=2,sticky='sw')



link = ttk.Button(connect_frame,text="Link", padding=5, width=5, command=lambda: app.connect_fixapi(baseurl_input,apikey_input,privatekey_input))
link.grid(row=7,column=1,sticky='w',padx=15)

close = ttk.Button(connect_frame,text="Close", padding=5, width=5, command=lambda: app.disconnect_fixapi())
close.grid(row=7,column=2,sticky='w')

'''----------connect frame end-------'''




'### Top ###'


ttk.Separator(root).pack(fill='x')

'--- bottom ---'
frame_bottom = ttk.Frame(root)
frame_bottom.configure(width=900)
frame_bottom.pack(side='bottom')

display_message = tk.Text(frame_bottom, bg="#fff")
display_message.configure(borderwidth=2,relief='solid',width=110)
display_message.pack(side='left',expand=True)

vbar = ttk.Scrollbar(frame_bottom, command=display_message.yview)
display_message.configure(yscrollcommand=vbar.set)

vbar.pack(side="right", fill="y")



if __name__ == "__main__":

    app = socketMonitorApp.socketMonitorApp(root,display_message)
    root.mainloop()
