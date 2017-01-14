import datetime
import telmod
import utils_module as utilm
import time
import collections

def execute_test0001(r_list):
    print("executing test0001...")
    raw_fn = {}
    telctl = {}
    test_id = "test0001"
    test_router_list = ["r1","r2"]

    #初期処理
    telctl, raw_fn = utilm.init_telnet_proc(r_list, test_router_list, test_id)

    #試験内容記述
    initc_r = ["term len 0",
                "terminal monitor",
                "sh ver",
                "sh diag",
                "sh users",
                "sh ip int brief",
                "sh run | sec bgp"
                ]

    r1_conf = ["conf t",
                "router bgp 65000",
                "neighbor 172.16.1.2 remote-as 65000",
                "end"
                ]

    r2_conf = ["conf t",
                "router bgp 65000",
                "neighbor 172.16.1.1 remote-as 65000",
                "end"
                ]

    afc_r =  ["sh run | s bgp",
                "sh ip bgp summary",
                "sh ip bgp neighbor",
                "sh ip bgp",
                "sh ip route"
                ]

    cmd_list1 = {"r1":initc_r, "r2":initc_r}
    cmd_list2 = {"r1":r1_conf, "r2":r2_conf}
    cmd_list3 = {"r1":afc_r, "r2":afc_r}

    #試験開始
    utilm.send_com_para(cmd_list1 , telctl , raw_fn)
    utilm.send_com_para(cmd_list2 , telctl , raw_fn)

    telctl["r1"].send_com("!wait until bgp comes up..." , raw_fn["r1"])
    telctl["r2"].send_com("!wait until bgp comes up..." , raw_fn["r2"])
    #print("DEBUG:start waiting for bgp to come up")
    telctl["r1"].wait_state(r"%BGP-5-ADJCHANGE:",raw_fn["r1"],60)
    #print("DEBUG:bgp might came up")

    utilm.send_com_para(cmd_list3 , telctl , raw_fn)

    #終了処理
    utilm.terminate_telnet_proc(telctl, raw_fn)


def rollback_state_test0001(r_list):
    print("DEBUG:rollback test0001...")
    raw_fn = {}
    telctl = {}
    test_id = "test0001_rollback"
    test_router_list = ["r1","r2"]

    #初期処理
    telctl, raw_fn = utilm.init_telnet_proc(r_list, test_router_list, test_id)

    #config消去および状態確認
    r_conf = ["conf t",
                "no router bgp 65000",
                "end"
                ]

    afc_r = ["term len 0",
                "sh run | sec bgp",
                "sh ip bgp summary",
                "sh ip bgp"
                ]

    cmd_list1 = {"r1":r_conf, "r2":r_conf}
    cmd_list2 = {"r1":afc_r, "r2":afc_r}

    #試験開始
    utilm.send_com_para(cmd_list1 , telctl , raw_fn)

    telctl["r1"].send_com("!wait for 1 sec",raw_fn["r1"])
    telctl["r2"].send_com("!wait for 1 sec",raw_fn["r2"])
    time.sleep(1)
    utilm.send_com_para(cmd_list2 , telctl , raw_fn)

    #終了処理
    utilm.terminate_telnet_proc(telctl, raw_fn)

if __name__ == "__main__":
    pass
