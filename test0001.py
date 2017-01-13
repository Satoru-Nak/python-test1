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

    #試験で使用するrouterがr_listに含まれているかどうか
    if "r1" and "r2" not in r_list:
        return("router instance doesn't exist in r_list...aborting")
    else:
        #初期準備  r_listからlog fileを生成＋初期接続
        for r_name,r_data in r_list.items():
            raw_fn[r_name] = utilm.create_log_file(r_name,test_id)
            telctl[r_name] = telmod.RemoteAccess(**r_data)
            telctl[r_name].init_telnet()


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

        utilm.send_com_para(cmd_list1 , telctl , raw_fn)
        #↓4行は↑にまとめられた
        #telctl["r1"].send_com_list_wf(initc_r , raw_fn["r1"])
        #telctl["r2"].send_com_list_wf(initc_r , raw_fn["r2"])
        #telctl["r1"].send_com_wf(" ",raw_fn["r1"])
        #telctl["r2"].send_com_wf(" ",raw_fn["r2"])

        utilm.send_com_para(cmd_list2 , telctl , raw_fn)
        #telctl["r1"].send_com_list_wf(r1_conf , raw_fn["r1"])
        #telctl["r2"].send_com_list_wf(r2_conf , raw_fn["r2"])

        telctl["r1"].send_com_wf("!wait until bgp comes up..." , raw_fn["r1"])
        telctl["r2"].send_com_wf("!wait until bgp comes up..." , raw_fn["r2"])
        #print("DEBUG:start waiting for bgp to come up")
        telctl["r1"].wait_state(r"%BGP-5-ADJCHANGE:",raw_fn["r1"],60)
        #print("DEBUG:bgp might came up")

        telctl["r1"].send_com_list_wf(afc_r , raw_fn["r1"])
        telctl["r2"].send_com_list_wf(afc_r , raw_fn["r2"])

        #終了処理　file close + telnet切断
        for fn in raw_fn.values():
            fn.close()

        for telcl in telctl.values():
            telcl.disconnect()

def rollback_state_test0001(r_list):
    print("DEBUG:rollback test0001...")
    raw_fn = {}
    telctl = {}
    test_id = "test0001_rollback"

    #試験で使用するrouterがr_listに含まれているかどうか
    if "r1" and "r2" not in r_list:
        return("router instance doesn't exist in r_list...aborting")
    else:
        #初期準備  r_listからlog fileを生成＋初期接続
        for r_name,r_data in r_list.items():
            raw_fn[r_name] = utilm.create_log_file(r_name,test_id)
            telctl[r_name] = telmod.RemoteAccess(**r_data)
            telctl[r_name].init_telnet()

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

        telctl["r1"].send_com_list_wf(r_conf , raw_fn["r1"])
        telctl["r2"].send_com_list_wf(r_conf , raw_fn["r2"])

        telctl["r1"].send_com_wf("!wait for 1 sec",raw_fn["r1"])
        telctl["r2"].send_com_wf("!wait for 1 sec",raw_fn["r2"])
        time.sleep(1)

        telctl["r1"].send_com_list_wf(afc_r , raw_fn["r1"])
        telctl["r2"].send_com_list_wf(afc_r , raw_fn["r2"])

        for fn in raw_fn.values():
            fn.close()

        for telcl in telctl.values():
            telcl.disconnect()
