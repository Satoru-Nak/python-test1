# -*- coding: utf-8 -*-

import telnetlib
import datetime
import sys
import re
import utils_module as utilm
import time

class RemoteAccess:
	"""
	class used for accessing network equipments
	valid type : cisco-ios, cisco-iosxe, cisco-iosxr, juniper
	adding comments
	"""

	def __init__(self, address, r_type, login_id, login_pass, second_pass):
		self.address = address
		self.r_type = r_type
		self.login_id = login_id
		self.login_pass = login_pass
		self.second_pass = second_pass

	def __auth_failed(self, message):
		self.session.terminate()
		print(message)
		sys.exit()

	def read_untilb(self, my_str):
		res = self.tn.read_until(my_str.encode('ascii'),5)
		#print(my_str + ":" + res.decode("utf-8"))
		return(res)

	def write_b(self, my_str):
		self.tn.write(my_str.encode('ascii')+b"\n")
		#print(my_str)

	def init_telnet(self):
		#telnet and login with login/pass
		self.prompt1 = ">"
		self.prompt2 = "#"

		self.tn = telnetlib.Telnet(self.address , 23 , 5)
		self.read_untilb("Username:")
		self.write_b(self.login_id)
		self.read_untilb("Password:")
		self.write_b(self.login_pass)
		self.read_untilb(self.prompt1)
		self.write_b("enable")
		self.read_untilb("Password:")
		self.write_b(self.second_pass)
		res = self.read_untilb(self.prompt2)

		print("DEBUG:telnet_init to " + self.address + " succeeded")
		return(res)

	def send_com(self, cmd, fn):
		"""
		cmdを送って次にpromptが返ってくるまでの文字列をstring型で戻す
		戻り値がbyte文字列の場合、encodeしてstring型で返す
		"""
		self.write_b(cmd)
		res = self.read_untilb(self.prompt2)#この時点でresはbyte string

		if isinstance(res, bytes):
			res = res.decode("utf-8")

		fn.write(res)
		time.sleep(0.1)

		return(res)
		#telnetlib使う場合、Telnet.read_untilは文字列を待ち受ける"
		#Telnet.expectは正規表現のリストをとれる（どれかにあたればOK）

	def send_com_list_wf(self, cmd_list, fn):
		"""
		★send_com_wfの拡張。cmd_listにコマンドをリストで送り、逐次流し込む
		注意：promptは固定になってしまっているので、untilのpromptが変化する際には使用不可
		"""
		for cmd in cmd_list:
			self.send_com(" ",fn) #コマンドの間に空行（send_comで改行される）
			self.send_com(cmd,fn)

	def wait_state(self, my_str, fn, timeout):
		"""
		特定の文字列表現が来るまで待つ
		"""
		res = self.tn.read_until(my_str.encode('ascii'),timeout)
		#print(my_str + res.decode("utf-8"))
		fn.write(res.decode("utf-8"))
		#return(res.decode("utf-8"))

	def clean_format(self, my_str):
		"""
		入力はstring
		my_strを改行で区切ってlist化、空行を削除し、空白が2個以上続いたら","に変換して出力
		→ここから結果確認に渡す
		"""
		orig_str = re.split(r'[\r\n,\n,\r]',my_str)

		res = []
		for line in orig_str:
			if line != "": #空行じゃなかったら
				res.append(re.sub(r'\s{2,}' , ',' , line))
		return(res)

	def disconnect(self):
		self.write_b("exit\n")
		res = self.tn.read_all()

		print("DEBUG:disconnect from " + self.address + " succeeded")
		return(res)
