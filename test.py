import datetime
import mysql.connector

s = {
	1:"pewpew",
	2:{
		1:'cheese',
		2:'banana'},
	3:{
		1:'zzzz',
		2:{
			1:'banana hammock',
			2:'cat burglar'},
		3:"burger"},
	4:"boing"}


		
		
for i in s:
	try:
		for ii in s[i]:
			try:
				for iii in s[i][ii]:
					print ('\t'*2 + s[i][ii][iii])
			except:
				print ('\t'*1 + s[i][ii])
	except:
		print('\t'*0 + s[i])
	
	
