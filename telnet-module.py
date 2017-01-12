import telnetlib
import datetime
import sys

class RemoteAccess:
	"""
	class used for accessing network equipments
	valid type : cisco-ios, cisco-iosxe, cisco-iosxr, juniper
	ref:http://bty.sakura.ne.jp/wp/archives/975
	"""
	
	def __init__(self, address, type, login_id, login_pass, second_pass):
		self.address = address
		self.type = type
		self.login_id = login_id
		self.login_pass = login_pass
		self.second_pass = second_pass
	
	def __auth_failed(self, message):
		self.session.terminate()
		print message
		sys.exit()
	
	def init_telnet(self):
		"telnet and login with login/pass"
		tn = telnetlib.Telnet(self.address)

		if type == cisco-ios:
		"telnetlib使う場合、Telnet.read_untilは文字列を待ち受ける"
		Telnet.expectは正規表現のリストをとれる（どれかにあたればOK）
	
	def telnet_main:
	    """
	    telnet module main
	    """

	def telnet_error:
	    """
	    adding error catch
	    """


