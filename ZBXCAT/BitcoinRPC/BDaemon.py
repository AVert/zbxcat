from __future__ import print_function
from __future__ import absolute_import
import requests
import json

from .settings import *

class BDaemon(object):

	id_count = 0

	def __init__(self, network=NETWORK, user=RPCUSER, password=RPCPASSWORD, timeout=TIMEOUT):
		#TODO: check utf safety
		url = network_url(network)
		print('In mode:', network)
		self.network = url
		self.user = user.encode('utf8')
		self.password = password.encode('utf8')
		self.timeout = timeout


	def _call(self,  method, *args):
		jsondata = json.dumps({	'version': '2',
				'method': method,
				'params': args,
				'id': self.id_count})

		r = requests.post(self.network, auth=(self.user,self.password), data=jsondata, timeout=self.timeout)

		self.id_count += 1

		resp = json.loads(r.text)

		#TODO: deal with errors better.
		error = resp['error']
		if error:
			print(error)

		return resp['result']

	# REGTEST
	def generate(self, blocknum):
		return self._call('generate', blocknum)

	def importaddress(self, script):
		return self._call('importaddress', script)

	#Block Info
	def getBlockHash(self, blockheight):
		return self._call('getblockhash', blockheight)

	def getBlockByHash(self, blockhash):
		return self._call('getblock', blockhash)

	def getBlockByHeight(self, blockheight):
		return self.getBlockByHash(self.getBlockHash(blockheight))

	# Custom methods to get Network Info
	def getNetworkHeight(self):
		return self._call('getblockcount')

	def getNetworkDifficulty(self):
		return self._call('getdifficulty')

	def getVersion(self):
		info = self._call('getnetworkinfo')
		client = info['subversion']
		version = client.strip('/').split(':')[1]
		return version

	def getConnectionCount(self):
		return self._call('getconnectioncount')

	# Wallet Info
	def getbalance(self):
		return self._call('getbalance')

	def listunspent(self, minconf=1):
		return self._call('listunspent', minconf)

	#Raw Txs
	def gettransaction(self, txid):
		return self._call('gettransaction', txid)

	def getrawtransaction(self, txid, verbose=0):
		# default verbose=0 returns serialized, hex-encoded data
		# verbose=1, returns a JSON obj of tx
		return self._call('getrawtransaction', txid, verbose)

	def decoderawtransaction(self, txhex):
		return self._call('decoderawtransaction', txhex)

	def sendrawtransaction(self, txhex):
		return self._call('sendrawtransaction', txhex)

	def getnewaddress(self):
		return self._call('getnewaddress')

	def sendtoaddress(self, taddress, amount):
		return self._call('sendtoaddress', taddress, amount)

	def listunspent(self):
		return self._call('listunspent')
