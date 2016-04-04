import datetime
import mysql.connector
import re


	
	
	
class WebSite:
	v_page = []
	v_meta = {}
	v_title = {}	
	v_nav = {}
	v_url = {}
	v_cont = {}
	v_template = ''
		
	def __init__ (self):
		
		with open('template\\0.html', 'r') as tmp_template:
			WebSite.v_template = tmp_template.read()

			
		cnx_meta = mysql.connector.connect(user='localread')
		cursor_meta = cnx_meta.cursor(dictionary=True)
		
		query = ("SELECT * FROM ocm_webcompile.default_meta")
			
		cursor_meta.execute(query)
		news_article = cursor_meta.fetchall()
		
		for i in news_article:
			WebSite.v_meta[i['Meta_Tag']] = i['Meta_Value']
			WebSite.v_template = WebSite.v_template.replace('<$META_' + i['Meta_Tag'].upper() + '$>',i['Meta_Value'])
		
		WebSite.v_template = WebSite.v_template.replace('<$META_LINK$>','Barnacle Joe')
		
		
		
		print (WebSite.v_template)
		print(WebSite.v_meta)
		#CREATE TABLE IF NOT EXISTS  (
		#	Meta_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
		#	Meta_Tag VARCHAR(50) NOT NULL,
		#	Meta_Value VARCHAR(100) NOT NULL,
		#	PRIMARY KEY (Meta_ID)
		#) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			
			
			

		# WebSite.v_template = WebSite.v_template.replace('<$NAV_FOOT$>',build_nav('foot',''))
		
		# WebSite.v_template = WebSite.v_template.replace('<$META_LANGUAGE$>',WebSite.v_meta['language'])
		# WebSite.v_template = WebSite.v_template.replace('<$META_APPNAME$>',WebSite.v_meta['appname'])
		# WebSite.v_template = WebSite.v_template.replace('<$META_AUTHOR$>',WebSite.v_meta['author'])
		# WebSite.v_template = WebSite.v_template.replace('<$META_KEYWORD$>',WebSite.v_meta['keywords'] + '<$META_KEYWORD$>')

		# WebSite.v_template = WebSite.v_template.replace('<$URL_ROOT$>',WebSite.v_url['root'])
		# WebSite.v_template = WebSite.v_template.replace('<$URL_ASSET$>',WebSite.v_url['asset'])

		# WebSite.v_template = WebSite.v_template.replace('<$TITLE_SITE$>',WebSite.v_title['site'])

		# WebSite.v_template = WebSite.v_template.replace('<$CONTENT_FOOTER$>',WebSite.v_cont['foot'])
		
	


		
			

		cursor_meta.close()
		cnx_meta.close()		

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

		
		
		
		
		
		

	

		

		
website = WebSite()
