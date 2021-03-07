from bluepy import btle
import time
import logging
import globals
import binascii
from multiconnect import Connector
import struct

class DelonghiPrimadona():
	def __init__(self):
		self.name = 'delonghi_primadona'
		self.ignoreRepeat = False

	def isvalid(self,name,manuf='',data='',mac=''):
		if name.lower().startswith("d17") or name.lower() == self.name:
			return True
			
	def parse(self,data,mac,name,manuf):
		action={}
		action['present'] = 1
		return action
	
	def connect(self,mac):
		logging.debug('Connecting : '+str(mac) + ' with bluetooth ' + str(globals.IFACE_DEVICE))
		i=0
		while True:
			i = i + 1
			try:
				conn = btle.Peripheral(mac,iface=globals.IFACE_DEVICE)
				globals.KEEPED_CONNECTION[mac]=conn
				logging.debug('Creating a new connection for ' + mac)
				break
			except Exception as e:
				logging.error(str(e))
				if i >= 4 :
					conn = False
					break
		if conn:
			logging.debug('** delonghi connection done for :'+mac)
		else:
			logging.warning('** delonghi connection failed for :'+mac)
		return conn
	
	def action(self,message):
		mac = message['device']['id']
		handle = message['command']['handle']
		value = message['command']['value']
		conn = self.connect(mac)
		conn.writeCharacteristic(int(handle,16), bytes.fromhex(value), True)
		logging.debug('Value ' + value + ' written in handle ' +handle)
		logging.debug('Refreshing ... ')
		result = self.read(mac)
		return result
	
	def read(self,mac):
		global result
		result={}
		try:
			conn = self.connect(mac)
		except Exception as e:
			try:
				conn.disconnect()
			except Exception as e:
				pass
			logging.error(str(e))
		return result

globals.COMPATIBILITY.append(DelonghiPrimadona)
