import datetime
import mysql.connector
import re


	
	
	
class WebSite:
	v_template = ''
	v_meta = {}
	v_title = {}	
	v_url = {}
	v_nav = {}

	v_page = {}

		
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

		# set SITE TITLE
		WebSite.v_title['site'] = v_meta['appname']
		WebSite.v_template = WebSite.v_template.replace('<$TITLE_SITE$>',WebSite.v_title['site'])
		
		# retrieve and populate GLOBAL URL values
		lv_query = "SELECT * FROM ocm_webcompile.default_url"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_url[i['Url_Name']] = i['Url_Value']
			WebSite.v_template = WebSite.v_template.replace('<$URL_' + i['Url_Name'].upper() + '$>',i['Url_Value'])

		# retrieve NAVIGATION structures
		lv_query = "SELECT Nav_Title, Section_Name, Page_Path FROM ocm_webcompile.site_nav INNER JOIN ocm_webcompile.site_section ON site_nav.Section_ID = site_section.Section_ID INNER JOIN ocm_webcompile.site_page ON site_nav.Page_ID = site_page.Page_ID ORDER BY site_nav.Section_ID, Nav_Order"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_nav[i['Section_Name']].append([i['Nav_Title'],re.sub('^(|(.+?)/)$','\g<1>index',i['Page_Path']) + '.html'])
			
		# construct FOOTER NAVIGATION
		lv_footnav = ''
		for i in v_nav['foot']:
			lv_footnav = lv_footnav + '<li><a href="' + i[1] + '">' + i[0] + '</a></li>'
		
		lv_footnav = '<ul>' + lv_footnav + '</ul>'
		WebSite.v_template = WebSite.v_template.replace('<$NAV_FOOT$>',lv_footnav)
		
		# construct HTML PAGES
		lv_query = "SELECT Page_ID, Page_Title, Page_Name, Page_Path, Page_MetaDesc, Page_MetaKey, Page_Content, Page_Type, Section_Title FROM ocm_webcompile.site_page INNER JOIN ocm_webcompile.site_section ON site_page.Section_ID = site_section.Section_ID ORDER BY site_section.Section_ID"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_page[i['Section_Title']].append(WebPage(i))

		cursor_webcompile.close()
		cnx_webcompile.close()		
		
	


		
			

class WebPage:

	def __init__ (self,pagequery):
		self.v_template = WebSite.v_template
		self.v_section = pagequery['Section_Title']
		
		self.v_pagetitle = pagequery['Page_Title']
		self.v_pagename = pagequery['Page_Name']
		self.v_pagepath = re.sub('^(|(.+?)/)$','\g<1>index',pagequery['Page_Path']) + '.html'

		self.v_metakey = pagequery['Page_MetaKey']
		self.v_metadesc = pagequery['Page_MetaDesc']
		self.v_metalink = '<!-- link rel="canonical" -->'
	
		self.v_content = pagequery['Page_Content']
		
		self.v_sitenav = ''
		self.v_pagenav = ''
		
		# construct SITE NAVIGATION
		for i in WebSite.v_nav['site']:
			lv_sitenav = '<a href="' + i[1] + '">' + i[0] + '</a></li>'
			if (i[0].upper() == self.v_section.upper()):
				lv_sitenav = '<li class="active">' + lv_sitenav
			else:
				lv_sitenav = '<li>' + lv_sitenav
			self.v_sitenav = self.v_sitenav + lv_sitenav
			
		self.v_sitenav = '<ul>' + self.v_sitenav + '</ul>'

		# construct PAGE NAVIGATION
		for i in WebSite.v_nav[self.v_section]:
			lv_pagenav = '<a href="' + i[1] + '">' + i[0] + '</a></li>'
			if (i[1] == self.v_pagepath):
				lv_pagenav = '<li class="active">' + lv_pagenav
			else:
				lv_pagenav = '<li>' + lv_pagenav
			self.v_pagenav = self.v_pagenav + lv_pagenav
		if (len(self.v_pagenav)):
			self.v_pagenav = '<nav><h2 class="WCAG_hide">Page Navigation</h2><ul>' + self.v_pagenav + '</ul></nav>'
		
		# inject NAVIGATION CONSTRUCTS
		self.v_template = self.v_template.replace('<$NAV_SITE$>',self.v_sitenav)
		self.v_template = self.v_template.replace('<$NAV_PAGE$>',self.v_pagenav)

		# construct BREADCRUMB
		lv_breadcrumblevel = 1
		self.v_breadcrumb = '<ol><li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + '" itemprop="item"><span itemprop="name">' + WebSite.v_title['site'] + '</span></a><meta itemprop="position" content="' + lv_breadcrumblevel + '"></li>'
		if (re.search("[^/]+/[^/]+", self.v_pagepath)):
			lv_breadcrumblevel += 1
			self.v_breadcrumb = self.v_breadcrumb + '<li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + self.v_pagepath.split('/')[0] + '.html" itemprop="item"><span itemprop="name">' + self.v_section.title() + '</span></a><meta itemprop="position" content="' + lv_breadcrumblevel + '"></li>'
		lv_breadcrumblevel += 1
		self.v_breadcrumb = self.v_breadcrumb + '<li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + self.v_pagepath + '" itemprop="item"><span itemprop="name">' + self.v_pagetitle + '</span></a><meta itemprop="position" content="' + lv_breadcrumblevel + '"></li>'
		self.v_breadcrumb = self.v_breadcrumb + '<$NAV_BREADCRUMB$></ol>'
		
		# inject BREADCRUMB CONSTRUCT
		self.v_template = self.v_template.replace('<$NAV_BREADCRUMB$>',self.v_breadcrumb)
		
		
		
		
		if (pagequery['Page_Type'] != 'page'):
			component['Comp' + pagequery['Page_Type'].title()](pagequery['Page_ID'])
		
		
		
		
		
		
		
		
		
		
		# inject CONTENT
		self.v_template = self.v_template.replace('<$META_KEYWORD$>',self.v_metakey)
		self.v_template = self.v_template.replace('<$META_DESCRIPTION$>',self.v_metadesc)
		self.v_template = self.v_template.replace('<$META_TITLE$>',self.v_pagetitle)
		self.v_template = self.v_template.replace('<$META_LINK$>',self.v_metalink)

		self.v_template = self.v_template.replace('<$TITLE_PAGE$>',self.v_pagename)

		self.v_template = self.v_template.replace('<$CONTENT$>',self.v_content)




class CompAlbum:
	def __init__ (self, pageid):
		self.x = something

class CompBlog:
	def __init__ (self, pageid):
		self.v_pageid = pageid
		self.v_article = []
		
		# establish RAW TEMPLATE (article)
		with open('template\\blog\\article.html', 'r') as tmp_template:
			self.v_template = tmp_template.read()
		
		# establish RAW TEMPLATE (archive wrapper)
		with open('template\\blog\\article-archive.html', 'r') as tmp_template:
			self.v_template = tmp_template.read()

		# establish RAW TEMPLATE (post wrapper)
		with open('template\\blog\\article-post.html', 'r') as tmp_template:
			self.v_template = tmp_template.read()

		cnx_blog = mysql.connector.connect(user='localread')
		cursor_blog = cnx_blog.cursor(dictionary=True)

		lv_query = "SELECT Blog_ID, Blog_Title, COUNT(Post_ID) AS Blog_PostCount, MAX(Post_Epoch) AS Blog_LastPost FROM ocm_webcompile.comp_blog LEFT JOIN ocm_webcompile.comp_blog_post ON comp_blog.Blog_ID = comp_blog_post.Blog_ID WHERE comp_blog.Page_ID = self.v_pageid"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		self.v_blogID = query_result['Blog_ID']
		self.v_blogtitle = query_result['Blog_Title']
		self.v_postcount = query_result['Blog_PostCount']
		self.v_postlast = query_result['Blog_LastPost']
			
		
		
		

		
		cursor_blog.close()
		cnx_blog.close()		

		# comp_blog


		
		# CREATE TABLE IF NOT EXISTS ocm_webcompile.comp_blog (
			# Blog_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
			# Blog_Title VARCHAR(100) NOT NULL,
			# Page_ID INT(10) UNSIGNED NOT NULL,
			# PRIMARY KEY (Post_ID)
		# ) ENGINE=InnoDB;

		# CREATE TABLE IF NOT EXISTS ocm_webcompile. (
			# Post_ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
			# Post_Title VARCHAR(100) NOT NULL,
			# Post_Content TEXT NOT NULL,
			# Post_Epoch INT(10) UNSIGNED NOT NULL,
			# Blog_ID TINYINT(1) UNSIGNED NOT NULL,
			# PRIMARY KEY (Post_ID)
		# ) ENGINE=InnoDB;

		
		
class CompPortfolio:
	def __init__ (self, pageid):
		self.x = something

class CompProduct:
	def __init__ (self, pageid):
		self.x = something

class CompSitemap:
	def __init__ (self, pageid):
		self.x = something
		

		
website = WebSite()
#print (WebSite.v_template)
#print(WebSite.v_meta)
print(WebSite.v_nav)