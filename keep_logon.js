const crypto = require("crypto")
const fs = require("fs")
const tls = require("tls")



let utc_timestamp=get_time()
let sender_comp_id=random_string()
let target_comp_id='SPOT'
let msg_seq_num=1
let payload = ['A',sender_comp_id,target_comp_id,msg_seq_num,utc_timestamp].join(String.fromCharCode(1))
//console.log(payload)


let api_key = ""
let private_key = fs.readFileSync(__dirname+'/private_key.pem');
let private_key_obj = crypto.createPrivateKey(private_key);
let signature = crypto.sign(null,payload,private_key_obj).toString('base64')

//console.log(signature)
let fix_message = `35=A|49=${sender_comp_id}|56=${target_comp_id}|34=1|52=${utc_timestamp}|\
95=${signature.length}|96=${signature}|98=0|108=60|141=Y|553=${api_key}|25035=2|`

//console.log(fix_message)


let final_msg = get_final_message(fix_message)




const client = tls.connect(9000,"fix-oe.binance.com",
    ()=>{
        
        client.write(final_msg,'ascii');
        console.log("send: "+final_msg.replaceAll(String.fromCharCode(1),'|'))
        msg_seq_num++;
    });

    client.once('connect',()=>{
        
    })

    client.on('data',(data)=>{
        
        let response = data.toString();
        console.log("recv: "+response.replaceAll(String.fromCharCode(1),'|'));

        let data_list = response.split(String.fromCharCode(1));
        if(data_list[2]==='35=1'){
            let hearbeat_msg = `35=0|49=${sender_comp_id}|56=${target_comp_id}|34=${msg_seq_num}|52=${get_time()}|${data_list.at(-3)}|`;
            final_msg = get_final_message(hearbeat_msg);
            client.write(final_msg,'ascii');
            console.log("send: "+final_msg.replaceAll(String.fromCharCode(1),'|'))
            msg_seq_num++;
        }
    })

    client.on('error',(error)=>{
        console.log(error)
    });

    client.on('end',()=>{
        console.log('disconnected')
    });


    process.stdin.resume();







function get_final_message(fix_message){
    let temp_str = `8=FIX.4.4|9=${fix_message.length}|` + fix_message
    checksum = temp_str.replaceAll('|',String.fromCharCode(1)).split('').map(element=> element.charCodeAt()).reduce(
        (accumulator, currentValue) => accumulator + currentValue
      )
    let final_msg = temp_str + `10=${String(checksum%256).padStart(3,'0')}|`

    return final_msg.replaceAll('|',String.fromCharCode(1))
}
    




function get_time(){
    time = new Date()
    return time.getUTCFullYear()+
    String(time.getUTCMonth()+1).padStart(2, '0')+
    String(time.getUTCDate()).padStart(2,'0')+
    '-'+
    String(time.getUTCHours()).padStart(2,'0')+':'+
    String(time.getUTCMinutes()).padStart(2,'0')+':'+
    String(time.getUTCSeconds()).padStart(2,'0')+
    '.'+
    String(time.getMilliseconds()).padStart(3,'0')
}


function random_string(k){
    k = k || 8;
    let characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let c ='';
    for(let i=0; i<k; i++){
        c += characters.charAt(Math.floor(Math.random()*characters.length))
    }
    return c;
}
