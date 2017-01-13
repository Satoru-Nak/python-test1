# -*- coding: utf-8 -*-

import telnetlib
import datetime
import sys
import re

class RemoteAccess:
	"""
	class used for accessing network equipments
	valid type : cisco-ios, cisco-iosxe, cisco-iosxr, juniper
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
		return(res)

	def write_b(self, my_str):
		res = self.tn.write(my_str.encode('ascii')+b"\n")

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
		return(res)

	def send_com(self, cmd):
		"""
		cmdを送って結果を戻す
		戻り値がbyte文字列の場合、encodeしてstring型で返す
		"""
		self.write_b(cmd)
		res = self.read_untilb(self.prompt2)#この時点でresはbyte string

		if isinstance(res, bytes):
			return(res.decode("utf-8"))
		else:
			return(res)

		#telnetlib使う場合、Telnet.read_untilは文字列を待ち受ける"
		#Telnet.expectは正規表現のリストをとれる（どれかにあたればOK）

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
		return(res)
