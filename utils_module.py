import os
import datetime
import re
import telmod

log_file_base_path = r"C:\Users\NTTCOM\SoftwareEng\python-test1"

def create_log_file(router_name , test_id):
    """
    フォルダ："base_path + test_id"フォルダに保存 test_idにrollbackが含まれていた場合削除
    ファイル："test_id + router_name + 時間"ファイルを作成→保存
    """
    nowstr = str(datetime.datetime.now().strftime("%Y%m%d-%H%M(%S)"))
    #logファイル名
    logfilename = test_id + "-" + router_name + "-" + nowstr + "-log.txt"

    #保存場所　rollbackの場合も同じフォルダに保存（ファイル名は↑で別にする）
    fullfilepath = log_file_base_path + "\\" + re.sub(r"_rollback" , "" , test_id)
    #print("DEBUG log file created at " + fullfilepath + "\\" + logfilename)

    #create folder if it doesn't exist
    if not os.path.exists(fullfilepath):
        os.mkdir(fullfilepath)
        print("created files for " + test_id)

    return open(fullfilepath + "\\" + logfilename, "w")


def send_com_para(cmd_list, telctl, raw_fn):
    """
    cmd_listはkey=router名（r_listのkey),value=流し込むコマンドのリスト
    送られる順番はkeyのアルファベット順
    """
    for rs, c_list in sorted(cmd_list.items()):
        #rsがtelctl, raw_fnに含まれることを確認して
        if rs in telctl and rs in raw_fn:
            #流し込み
            telctl[rs].send_com_list_wf(c_list, raw_fn[rs])
            telctl[rs].send_com_wf(" ",raw_fn[rs])
        else:
            print("router not defined in cmd_list key...")
