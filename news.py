import datetime
import mysql.connector

import template


print(template.site_nav('Home'))

print("\n\n")

print(template.page_nav('home','Latest News'))

cnx = mysql.connector.connect(user='localread')
cursor = cnx.cursor()

query = ("SELECT News_Title, News_Content, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(News_Epoch),'America/Toronto','UTC'), '%H:%i %b %e, %Y') AS News_Date, 'Aurani' AS User_Name FROM ocm_generic.site_news WHERE News_Live <= UNIX_TIMESTAMP(NOW()) ORDER BY News_Epoch")

cursor.execute(query)
result = cursor.fetchall()



#for (News_Title, News_Content, News_Date, User_Name) in result:
#	print(str(News_Title) + ":")
#	#print(str(News_Content))
#	print("\t-- " + str(User_Name) + "\t" + str(News_Date))
	

	
	

cursor.close()
cnx.close()