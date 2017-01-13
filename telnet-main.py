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

r_list = {"r1":r1,"r2":r2}
raw_fn = {}
telctl = {}

for r_name,r_data in r_list.items():
    raw_fn[r_name] = create_log_file(r_name)
    telctl[r_name] = telmod.RemoteAccess(**r_data)
    telctl[r_name].init_telnet()

res_tmp1 = telctl["r1"].send_com("sh ip int brief")
raw_fn["r1"].write(res_tmp1)
res_tmp1 = telctl["r2"].send_com("sh ip int brief")
raw_fn["r2"].write(res_tmp1)

for fn in raw_fn.values():
    fn.close()

for telcl in telctl.values():
    telcl.disconnect()
