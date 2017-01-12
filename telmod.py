# -*- coding: utf-8 -*-

import telnetlib
import datetime
import sys

class RemoteAccess:
	"""
	class used for accessing network equipments
	valid type : cisco-ios, cisco-iosxe, cisco-iosxr, juniper
	ref:http://bty.sakura.ne.jp/wp/archives/975
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
		res = self.tn.read_until(my_str.encode('ascii'))
		return(res)

	def write_b(self, my_str):
		res = self.tn.write(my_str.encode('ascii')+b"\n")

	def init_telnet(self):
		#telnet and login with login/pass
		self.prompt1 = ">"
		self.prompt2 = "#"

		self.tn = telnetlib.Telnet(self.address)

		self.read_untilb("Username:")
		self.write_b(self.login_id)
		self.read_untilb("Password:")
		self.write_b(self.login_pass)

		"""
		self.read_untilb(self.tn , "Username:")
		self.write_b(self.tn , self.login_id)
		self.read_untilb(self.tn , "Password:")
		self.write_b(self.tn , self.login_pass)
		"""
		"""
		self.tn.read_until(b"Username:")
		self.tn.write(self.login_id.encode("ascii") + b"\n")
		self.tn.read_until(b"Password:")
		self.tn.write(self.login_pass.encode("ascii") + b"\n")
		"""
		self.tn.read_until(self.prompt1.encode("ascii"))
		self.tn.write(b"enable\n")
		self.tn.read_until(b"Password:")
		self.tn.write(self.second_pass.encode("ascii") + b"\n")
		res = self.tn.read_until(self.prompt2.encode("ascii"))
		return(res)

	def send_com(self, cmd):
		"send cmd and return result output"
		self.tn.write(cmd.encode("ascii") + b"\n")
		res = self.tn.read_until(self.prompt2.encode("ascii"))
		return(res)
		#telnetlib使う場合、Telnet.read_untilは文字列を待ち受ける"
		#Telnet.expectは正規表現のリストをとれる（どれかにあたればOK）

	def disconnect(self):
		self.tn.write(b"exit\n")
		res = self.tn.read_all()
		return(res)
