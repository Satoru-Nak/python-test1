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

def init_telnet_proc(r_list, test_router_list, test_id):
    """
    r_listからtelnetセッションを生成
    引数：r_list : router情報dict, test_router_list : testに必要なrouter名list
    戻り：RemoteAccessインスタンスをdictにまとめて、ログ用ファイルハンドラをdictにまとめて
    処理概要：
    1. r_listにtestに必要なルータ情報が含まれているかをチェック
    2. 初期処理、ログファイル生成、RemoteAccessクラスインスタンス化、telnet（ログインまで）
    """
    raw_fn = {}
    telctl = {}
    error_flg = False
    #r_listにtestに必要なルータ情報が含まれているかをチェック
    for router_name in test_router_list:
        if router_name not in r_list:
            error_flg = True
            break

    if error_flg:
        print("r_list not defined correctly...")
    else:
        #初期準備  r_listからlog fileを生成＋初期接続
        for r_name,r_data in r_list.items():
            raw_fn[r_name] = create_log_file(r_name,test_id)
            telctl[r_name] = telmod.RemoteAccess(**r_data)
            telctl[r_name].init_telnet()

        return([telctl , raw_fn])

def send_com_para(cmd_list, telctl, raw_fn):
    """
    cmd_listはkey=router名（r_listのkey),value=流し込むコマンドのリスト
    送られる順番はkeyのアルファベット順で、１つのルータですべてのコマンド実行が
    完了してから次のコマンド実行に移る
    """
    for rs, c_list in sorted(cmd_list.items()):
        #rsがtelctl, raw_fnに含まれることを確認して
        if rs in telctl and rs in raw_fn:
            #流し込み
            telctl[rs].send_com_list_wf(c_list, raw_fn[rs])
            telctl[rs].send_com(" ",raw_fn[rs])
        else:
            print("router not defined in cmd_list key...")

def terminate_telnet_proc(telctl, raw_fn):
    """
    終了処理　file close + telnet切断
    """
    for fn in raw_fn.values():
        fn.close()

    for telcl in telctl.values():
        telcl.disconnect()
