import telmod
import datetime
import re

def create_log_file(router_name):
    nowstr = str(datetime.datetime.now().strftime("%Y%m%d-%H%M(%S)"))
    logfilename = router_name + "-" + nowstr + "-log.txt"
    return open(logfilename, "w")

r1 = {"address":"192.168.44.10",
    "r_type":"cisco",
    "login_id":"satoru",
    "login_pass":"satoru",
    "second_pass":"satoru"}

r2 = {"address":"192.168.44.20",
    "r_type":"cisco",
    "login_id":"satoru",
    "login_pass":"satoru",
    "second_pass":"satoru"}

fn_r1 = create_log_file("r1")
telcl_r1 = telmod.RemoteAccess(**r1)

telcl_r1.init_telnet()

res_tmp1 = telcl_r1.send_com("sh ip int brief")
#ファイルに書き込むのはsend_comの戻り値
fn_r1.write(res_tmp1)

#正誤判断のためにclean_formatする
res_tmp2 = telcl_r1.clean_format(res_tmp1)
print (res_tmp2)


res = telcl_r1.disconnect()

fn_r1.close()
