import telmod

r1 = {"address":"192.168.44.10",
    "r_type":"cisco",
    "login_id":"satoru",
    "login_pass":"satoru",
    "second_pass":"satoru"}

telcl = telmod.RemoteAccess(**r1)

res = telcl.init_telnet()
print(res)

res = telcl.send_com("sh ip int brief")
print(res)

res = telcl.disconnect()
print(res)
