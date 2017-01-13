import test0001
import utils_module as utilm
import time

#fn = utilm.create_log_file("r1",r"C:\Users\NTTCOM\SoftwareEng\python-test1","test0001")
#fn = utilm.create_log_file("r1","test0001")

#fn.write("testing")
#fn.close()

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

test0001.rollback_state_test0001(r_list)
time.sleep(5)

test0001.execute_test0001(r_list)
time.sleep(5)
test0001.rollback_state_test0001(r_list)
