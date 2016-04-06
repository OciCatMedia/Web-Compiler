import datetime
import mysql.connector
import re


	
	
	
class WebSite:
	v_page = []
	v_meta = {}
	v_title = {}	
	v_nav = []
	v_url = {}
	v_cont = {}
	v_template = ''
		
	def __init__ (self):
		
		# establish RAW TEMPLATE	
		with open('template\\0.html', 'r') as tmp_template:
			WebSite.v_template = tmp_template.read()

		# connect to DATABASE
		cnx_webcompile = mysql.connector.connect(user='localread')
		cursor_webcompile = cnx_webcompile.cursor(dictionary=True)

		# retrieve and populate GLOBAL METATAG VALUES
		lv_query = "SELECT * FROM ocm_webcompile.default_meta"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_meta[i['Meta_Tag']] = i['Meta_Value']
			WebSite.v_template = WebSite.v_template.replace('<$META_' + i['Meta_Tag'].upper() + '$>',i['Meta_Value'])

		# retrieve and populate GLOBAL URL values
		lv_query = "SELECT * FROM ocm_webcompile.default_url"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_url[i['Url_Name']] = i['Url_Value']
			WebSite.v_template = WebSite.v_template.replace('<$URL_' + i['Url_Name'].upper() + '$>',i['Url_Value'])

		# retrieve GLOBAL NAVIGATION structure
		lv_query = "SELECT site_section.Section_ID, Section_Title, Nav_Title, Page_Path FROM ocm_webcompile.site_section INNER JOIN ocm_webcompile.site_nav ON site_section.Section_ID = site_nav.Section_ID INNER JOIN ocm_webcompile.site_page ON site_nav.Page_ID = site_page.Page_ID WHERE site_section.Section_PrimNav = 1 ORDER BY site_section.Section_ID"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_nav.append([i['Section_ID'],i['Nav_Title'],re.sub('^(|(.+?)/)$','\g<1>index',i['Page_Path']) + '.html'])
			
		



		
		
		
			
			

			
			

		cursor_webcompile.close()
		cnx_webcompile.close()		
			
		# WebSite.v_template = WebSite.v_template.replace('<$NAV_FOOT$>',build_nav('foot',''))
		

		# WebSite.v_template = WebSite.v_template.replace('<$URL_ROOT$>',WebSite.v_url['root'])
		# WebSite.v_template = WebSite.v_template.replace('<$URL_ASSET$>',WebSite.v_url['asset'])

		# WebSite.v_template = WebSite.v_template.replace('<$TITLE_SITE$>',WebSite.v_title['site'])

		# WebSite.v_template = WebSite.v_template.replace('<$CONTENT_FOOTER$>',WebSite.v_cont['foot'])
		
	


		
			


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

		
		
		
		
		
		

	

		

		
website = WebSite()
#print (WebSite.v_template)
#print(WebSite.v_meta)
print(WebSite.v_nav)