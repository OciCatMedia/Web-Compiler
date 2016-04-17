import datetime
import mysql.connector
import re
import os, sys


	
	
	
class WebSite:
	v_template = ''
	v_meta = {}
	v_title = {}	
	v_url = {}
	v_nav = {}

	v_page = {}

		
	def __init__ (self):
		
		# establish RAW TEMPLATE	
		with open('template\\base.html', 'r') as tmp_template:
			WebSite.v_template = tmp_template.read()
		
		# establish PAGE CONTENT PLACEHOLDER	
		with open('template\\page.html', 'r') as tmp_template:
			WebSite.v_ph_content = tmp_template.read()

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
		WebSite.v_title['site'] = WebSite.v_meta['appname']
		WebSite.v_template = WebSite.v_template.replace('<$TITLE_SITE$>',WebSite.v_title['site'])
		
		# retrieve and populate GLOBAL URL values
		lv_query = "SELECT * FROM ocm_webcompile.default_url"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_url[i['Url_Name']] = i['Url_Value']
			WebSite.v_template = WebSite.v_template.replace('<$URL_' + i['Url_Name'].upper() + '$>',i['Url_Value'])

		# retrieve SITE SECTION names
		lv_query = "SELECT Section_Name FROM ocm_webcompile.site_section"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_nav[i['Section_Name']] = []
			WebSite.v_page[i['Section_Name']] = []
		
		
		# retrieve NAVIGATION structures
		lv_query = "SELECT Nav_Title, Section_Name, Page_Path FROM ocm_webcompile.site_nav INNER JOIN ocm_webcompile.site_section ON site_nav.Section_ID = site_section.Section_ID INNER JOIN ocm_webcompile.site_page ON site_nav.Page_ID = site_page.Page_ID ORDER BY site_nav.Section_ID, Nav_Order"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			if (len(i['Page_Path'])):
				WebSite.v_nav[i['Section_Name']].append([i['Nav_Title'],WebSite.v_url['root'] + re.sub('^(|(.+?)/)$','\g<1>index',i['Page_Path']) + '.html'])
			else:
				WebSite.v_nav[i['Section_Name']].append([i['Nav_Title'],WebSite.v_url['root']])
			
		# construct FOOTER NAVIGATION
		lv_footnav = ''
		for i in WebSite.v_nav['foot']:
			lv_footnav = lv_footnav + '<li><a href="' + i[1] + '">' + i[0] + '</a></li>'
		
		WebSite.v_template = WebSite.v_template.replace('<$NAV_FOOT$>',lv_footnav)
		
		# construct HTML PAGES
		lv_query = "SELECT Page_ID, Page_Title, Page_Name, Page_Path, Page_MetaDesc, Page_MetaKey, Page_Content, Page_Type, Section_Name FROM ocm_webcompile.site_page INNER JOIN ocm_webcompile.site_section ON site_page.Section_ID = site_section.Section_ID ORDER BY site_section.Section_ID"
		cursor_webcompile.execute(lv_query)
		query_result = cursor_webcompile.fetchall()
		
		for i in query_result:
			WebSite.v_page[i['Section_Name']].append(WebPage(i))

		cursor_webcompile.close()
		cnx_webcompile.close()		
		
	


		
			

class WebPage:

	def __init__ (self,pagequery):
		self.v_template = WebSite.v_template
		self.v_section = pagequery['Section_Name']
		
		self.v_pageid = pagequery['Page_ID']
		self.v_pagetitle = pagequery['Page_Title']
		self.v_pagename = pagequery['Page_Name']
		self.v_pagepath = re.sub('^(|(.+?)/)$','\g<1>index',pagequery['Page_Path']) + '.html'

		self.v_metakey = pagequery['Page_MetaKey']
		self.v_metadesc = pagequery['Page_MetaDesc']
		self.v_metalink = '<$META_LINK$>'
	
		self.v_content = pagequery['Page_Content']
		
		self.v_sitenav = ''
		self.v_pagenav = ''
		
		self.v_url = {}
		self.v_url['absolute'] = WebSite.v_url['root'] + self.v_pagepath
		self.v_url['child'] = re.sub('\.html$','/', self.v_url['absolute'])
		
		# construct SITE NAVIGATION
		for i in WebSite.v_nav['site']:
			lv_sitenav = '<a href="' + i[1] + '">' + i[0] + '</a></li>'
			if (i[0].upper() == self.v_section.upper()):
				lv_sitenav = '<li class="active">' + lv_sitenav
			else:
				lv_sitenav = '<li>' + lv_sitenav
			self.v_sitenav = self.v_sitenav + lv_sitenav

		# construct PAGE NAVIGATION
		for i in WebSite.v_nav[self.v_section]:
			lv_pagenav = '<a href="' + i[1] + '">' + i[0] + '</a></li>'
			if (i[1] == WebSite.v_url['root'] + self.v_pagepath):
				lv_pagenav = '<li class="active">' + lv_pagenav
			else:
				lv_pagenav = '<li>' + lv_pagenav
			self.v_pagenav = self.v_pagenav + lv_pagenav
		
		if (not len(self.v_pagenav)):
			self.v_pagenav = '<li><a></a></li>'

		# construct BREADCRUMB
		self.v_breadcrumblevel = 1
		self.v_breadcrumb = '<ol><li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + '" itemprop="item"><span itemprop="name">' + WebSite.v_title['site'] + '</span></a><meta itemprop="position" content="' + str(self.v_breadcrumblevel) + '"></li>'
		if (re.search("[^/]+/[^/]+", self.v_pagepath)):
			self.v_breadcrumblevel += 1
			self.v_breadcrumb = self.v_breadcrumb + '<li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + self.v_pagepath.split('/')[0] + '.html" itemprop="item"><span itemprop="name">' + self.v_section.title() + '</span></a><meta itemprop="position" content="' + str(self.v_breadcrumblevel) + '"></li>'
		self.v_breadcrumblevel += 1
		self.v_breadcrumb = self.v_breadcrumb + '<li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + WebSite.v_url['root'] + self.v_pagepath + '" itemprop="item"><span itemprop="name">' + self.v_pagetitle + '</span></a><meta itemprop="position" content="' + str(self.v_breadcrumblevel) + '"></li>'
		self.v_breadcrumb = self.v_breadcrumb + '<$NAV_BREADCRUMB$></ol>'
		
		# inject BREADCRUMB CONSTRUCT
		self.v_template = self.v_template.replace('<$NAV_BREADCRUMB$>',self.v_breadcrumb)
		
		
		
		
		if (pagequery['Page_Type'] != 'page'):
			component[pagequery['Page_Type']](self)
		else:
			self.v_template = self.v_template.replace('<$CONTENT_WRAPPER$>',WebSite.v_ph_content)
		
		
		
		
		
		
		
		
		# inject NAVIGATION CONSTRUCTS
		self.v_template = self.v_template.replace('<$NAV_SITE$>',self.v_sitenav)
		self.v_template = self.v_template.replace('<$NAV_PAGE$>',self.v_pagenav)
		
		# inject CONTENT
		self.v_template = self.v_template.replace('<$META_KEYWORD$>',self.v_metakey)
		self.v_template = self.v_template.replace('<$META_DESCRIPTION$>',self.v_metadesc)
		self.v_template = self.v_template.replace('<$META_TITLE$>',self.v_pagetitle)
		self.v_template = self.v_template.replace('<$META_LINK$>',self.v_metalink)

		self.v_template = self.v_template.replace('<$TITLE_PAGE$>',self.v_pagename)

		self.v_template = self.v_template.replace('<$CONTENT$>',self.v_content)
		
		
		self.v_template = re.sub('<\$([^\$]*)\$>', '', self.v_template)

		if not os.path.exists(os.path.dirname(WebSite.v_url['path'] + self.v_pagepath.replace('/','\\'))):
			os.makedirs(os.path.dirname(WebSite.v_url['path'] + self.v_pagepath.replace('/','\\')))
		
		with open(WebSite.v_url['path'] + self.v_pagepath.replace('/','\\'), 'w') as tmp_template:
			tmp_template.write(self.v_template)



class CompAlbum:
	def __init__ (self, pageid):
		self.x = pageid

class CompBlog2:
	def __init__ (self, pageid):
		self.v_pageid = pageid
	
class CompBlog:
	def __init__ (self, lv_webpage):
		self.v_article = ''
		self.v_template = {}
		
		# establish RAW TEMPLATE (archive)
		with open('template\\blog\\archive.html', 'r') as tmp_template:
			self.v_template["archive"] = tmp_template.read()
		
		# establish ARCHIVE WRAPPER
		with open('template\\blog.html', 'r') as tmp_template:
			self.v_template["archivewrapper"] = tmp_template.read()
		
		# establish RAW TEMPLATE (post)
		with open('template\\blog\\post.html', 'r') as tmp_template:
			self.v_template["post"] = tmp_template.read()

		cnx_blog = mysql.connector.connect(user='localread')
		cursor_blog = cnx_blog.cursor(dictionary=True)

		# retrieve BLOG DETAILS
		lv_query = "SELECT comp_blog.Blog_ID, Blog_Title, COUNT(Post_ID) AS Blog_PostCount, MAX(Post_Epoch) AS Blog_LastPost FROM ocm_webcompile.comp_blog LEFT JOIN ocm_webcompile.comp_blog_post ON comp_blog.Blog_ID = comp_blog_post.Blog_ID WHERE comp_blog.Page_ID = " + str(lv_webpage.v_pageid)
		cursor_blog.execute(lv_query)
		query_result = cursor_blog.fetchall()
		
		self.v_blogID = query_result[0]['Blog_ID']
		self.v_blogtitle = query_result[0]['Blog_Title']
		self.v_postcount = query_result[0]['Blog_PostCount']
		self.v_postlast = query_result[0]['Blog_LastPost']

		# retrieve BLOG POSTS
		lv_query = "SELECT Post_ID, Post_Title, Post_Content, Post_Epoch, ocm_webcompile.Fuzzy_Date(Post_Live) AS Post_Fuzzy, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(Post_Live), @@session.time_zone,'UTC'),'%H:%i %b %e, %y') AS Post_Date, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(Post_Live), @@session.time_zone,'UTC'),'%Y-%m-%dT%H:%i:%SZ') AS Post_DateRFC, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(Post_Live), @@session.time_zone,'UTC'),'%Y/%m/%d') AS Post_Path, Post_Live, Post_IP, 'Aurani' AS User_Name FROM ocm_webcompile.comp_blog_post WHERE Blog_ID = " + str(self.v_blogID) + " AND Post_Live <= UNIX_TIMESTAMP() ORDER BY Post_Live DESC"
		cursor_blog.execute(lv_query)
		query_result = cursor_blog.fetchall()


		for i in query_result:
			lv_article = {}
			lv_article['archive'] = self.v_template['archive']
			lv_article['post'] = self.v_template['post']

			# retrieve PREVIOUS POST
			lv_query = "SELECT Post_Title, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(Post_Live), @@session.time_zone,'UTC'),'%Y/%m/%d') AS Post_Live FROM ocm_webcompile.comp_blog_post WHERE comp_blog_post.Post_Live < " + str(i['Post_Live']) + " ORDER BY Post_Live DESC LIMIT 0,1"
			cursor_blog.execute(lv_query)
			query_result = cursor_blog.fetchall()
			try:
				lv_article['prev'] = [query_result[0]['Post_Title'],query_result[0]['Post_Live']]
				lv_article['prev'].append(lv_webpage.v_url['child'] + lv_article['prev'][1] + '/' + re.sub('[^a-z\-]', '', lv_article['prev'][0].replace(' ', '-').lower()))
			except:
				lv_article['prev'] = ['','']
			
			# retrieve NEXT POST
			lv_query = "SELECT Post_Title, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(Post_Live), @@session.time_zone,'UTC'),'%Y/%m/%d') AS Post_Live FROM ocm_webcompile.comp_blog_post WHERE comp_blog_post.Post_Live > " + str(i['Post_Live']) + " ORDER BY Post_Live LIMIT 0,1"
			cursor_blog.execute(lv_query)
			query_result = cursor_blog.fetchall()
			try:
				lv_article['next'] = [query_result[0]['Post_Title'],query_result[0]['Post_Live']]
				lv_article['next'].append(lv_webpage.v_url['child'] + lv_article['next'][1] + '/' + re.sub('[^a-z\-]', '', lv_article['next'][0].replace(' ', '-').lower()))
			except:
				lv_article['next'] = ['','']
				
			# construct URL
			lv_article['url'] = re.sub('\.html$', '', lv_webpage.v_pagepath) + '/' + i['Post_Path'] + '/' + re.sub('[^a-z\-]', '', i['Post_Title'].replace(' ', '-').lower()) + '.html'
			lv_article['path'] = WebSite.v_url['path'] + lv_article['url'].replace('/','\\')
			lv_article['url'] = WebSite.v_url['root'] + lv_article['url']
						
			# construct PAGE NAVIGATION
			lv_pagenav = ''
			if (len(lv_article['prev'][0])):
				lv_pagenav = lv_pagenav + '<li title="' + lv_article['prev'][1] + '"><a href="' + lv_article['prev'][2] + '.html">previous post</a></li>'
			if (len(lv_article['next'][0])):
				lv_pagenav = lv_pagenav + '<li title="' + lv_article['next'][1] + '"><a href="' + lv_article['next'][2] + '.html">next post</a></li>'
			
			if (not len(lv_pagenav)):
				lv_pagenav = '<$NAV_PAGE$>'
			
			
			
			# inject CONTENT
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_ID$>',str(i['Post_ID']))
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_TITLE$>',i['Post_Title'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_CONTENT$>',i['Post_Content'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_LANGUAGE$>','en-ca')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_KEYWORD$>',lv_webpage.v_metakey)
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_URL$>',lv_article['url'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_FUZZY$>',i['Post_Fuzzy'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_DATE$>',i['Post_Date'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_DATERFC$>',i['Post_DateRFC'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_DATECOPY$>',i['Post_Path'][0:4])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_COMMENT_COUNT$>','0')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_AUTHOR$>',i['User_Name'])
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_AUTHORURL$>',WebSite.v_url['user'] + i['User_Name'].replace(' ', '').lower() + '.html')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_AUTHORIMAGE$>',WebSite.v_url['user'] + i['User_Name'].replace(' ', '').lower() + '/avatar.png')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_PUBLISHER$>','OciCat Media')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_PUBLISHERLOGO$>',WebSite.v_url['root'] + WebSite.v_url['asset'] + 'logobkg.png')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_IMAGE$>',WebSite.v_url['root'] + WebSite.v_url['asset'] + 'articledefault.png')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_IMAGEWIDTH$>','700')
			lv_article['post'] = lv_article['post'].replace('<$ARTICLE_IMAGEHEIGHT$>','200')
			lv_article['post'] = lv_article['post'].replace('<$BLOG_POST_COMMENT$>','<p>Comments are currently disabled.</p>')
			
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_ID$>',str(i['Post_ID']))
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_TITLE$>',i['Post_Title'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_CONTENT$>',i['Post_Content'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_LANGUAGE$>','en-ca')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_KEYWORD$>',lv_webpage.v_metakey)
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_URL$>',lv_article['url'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_FUZZY$>',i['Post_Fuzzy'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_DATE$>',i['Post_Date'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_DATERFC$>',i['Post_DateRFC'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_DATECOPY$>',i['Post_Path'][0:4])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_COMMENT_COUNT$>','0')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_AUTHOR$>',i['User_Name'])
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_AUTHORURL$>',WebSite.v_url['user'] + i['User_Name'].replace(' ', '').lower() + '.html')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_AUTHORIMAGE$>',WebSite.v_url['user'] + i['User_Name'].replace(' ', '').lower() + '/avatar.png')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_PUBLISHER$>','OciCat Media')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_PUBLISHERLOGO$>',WebSite.v_url['root'] + WebSite.v_url['asset'] + 'logobkg.png')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_IMAGE$>',WebSite.v_url['root'] + WebSite.v_url['asset'] + 'articledefault.png')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_IMAGEWIDTH$>','700')
			lv_article['archive'] = lv_article['archive'].replace('<$ARTICLE_IMAGEHEIGHT$>','200')
			lv_article['archive'] = lv_article['archive'].replace('<$BLOG_POST_COMMENT$>','<p>Comments are currently disabled.</p>')
			
			# construct POST WRAPPER
			lv_article['post'] = lv_webpage.v_template.replace('<$CONTENT_WRAPPER$>',lv_article['post'])
			
			# inject NAVIGATION CONSTRUCTS
			lv_article['post'] = lv_article['post'].replace('<$NAV_PAGE$>',lv_pagenav)
			lv_article['post'] = lv_article['post'].replace('<$NAV_SITE$>',lv_webpage.v_sitenav)

			#inject FINAL CONTENT
			lv_article['post'] = lv_article['post'].replace('<$META_KEYWORD$>',lv_webpage.v_metakey)
			lv_article['post'] = lv_article['post'].replace('<$META_DESCRIPTION$>',lv_webpage.v_metadesc)
			lv_article['post'] = lv_article['post'].replace('<$META_TITLE$>',i['Post_Title'])
			lv_article['post'] = re.sub('^(\s*)<\$META_LINK\$>.*$','\g<1><link href="' + lv_article['url'] + '" rel="canonical">\n\g<1><$META_LINK$>',lv_article['post'], flags=re.MULTILINE)
			if (len(lv_article['prev'][0])):
				lv_article['post'] = re.sub('^(\s*)<\$META_LINK\$>.*$','\g<1><link href="' + lv_article['prev'][2] + '.html" rel="prev">\n\g<1><$META_LINK$>', lv_article['post'], flags=re.MULTILINE)
			if (len(lv_article['next'][0])):
				lv_article['post'] = re.sub('^(\s*)<\$META_LINK\$>.*$','\g<1><link href="' + lv_article['next'][2] + '.html" rel="next">\n\g<1><$META_LINK$>', lv_article['post'], flags=re.MULTILINE)
			
			lv_article['post'] = lv_article['post'].replace('<$NAV_BREADCRUMB$>','<li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a href="' + lv_article['url'] + '" itemprop="item"><span itemprop="name">' + i['Post_Title'] + '</span></a><meta itemprop="position" content="' + str(lv_webpage.v_breadcrumblevel + 1) + '"></li>')
			lv_article['post'] = lv_article['post'].replace('<$CONTENT_ID$>','blog')
			lv_article['post'] = lv_article['post'].replace('<$RICH_ITEMTYPE$>','https://schema.org/BlogPosting')
				
		
			
			#lv_article['post'] = re.sub('<\$([^\$]*)\$>', '\n\nFIX THIS: \g<1> :FIX THIS\n\n', lv_article['post'])
			lv_article['post'] = re.sub('<\$([^\$]*)\$>', '', lv_article['post'])
				
				
				
			# write POST FILE	
			if not os.path.exists(os.path.dirname(lv_article['path'])):
				os.makedirs(os.path.dirname(lv_article['path']))
			
			with open(lv_article['path'], 'w') as tmp_template:
				tmp_template.write(lv_article['post'])
			
			self.v_article = self.v_article + '\n\n' + lv_article['archive']
			
		self.v_article = self.v_template["archivewrapper"].replace('<$CONTENT$>',self.v_article)
		self.v_article = lv_webpage.v_template.replace('<$CONTENT_WRAPPER$>',self.v_article)
		
		# construct PAGE NAVIGATION
		lv_pagenav = ''
		if (not len(lv_pagenav)):
			lv_pagenav = '<$NAV_PAGE$>'

		# inject NAVIGATION CONSTRUCTS
		self.v_article = self.v_article.replace('<$NAV_PAGE$>',lv_pagenav)
		self.v_article = self.v_article.replace('<$NAV_SITE$>',lv_webpage.v_sitenav)

		#inject FINAL CONTENT
		self.v_article = self.v_article.replace('<$META_KEYWORD$>',lv_webpage.v_metakey)
		self.v_article = self.v_article.replace('<$META_DESCRIPTION$>',lv_webpage.v_metadesc)
		self.v_article = self.v_article.replace('<$META_TITLE$>',lv_webpage.v_pagetitle)
		self.v_article = self.v_article.replace('<$CONTENT_ID$>','blog')
		self.v_article = self.v_article.replace('<$RICH_ITEMTYPE$>','https://schema.org/Blog')
		self.v_article = self.v_article.replace('<$BLOG_KEYWORD$>',lv_webpage.v_metakey)
		self.v_article = self.v_article.replace('<$BLOG_DESCRIPTION$>',lv_webpage.v_metadesc)
			
		#self.v_article = re.sub('<\$([^\$]*)\$>', '', self.v_article)
		
		lv_webpage.v_template = self.v_article
		
		#self.v_article = re.sub('<\$([^\$]*)\$>', '\n\nFIX THIS: \g<1> :FIX THIS\n\n', self.v_article)
		#self.v_article = re.sub('<\$([^\$]*)\$>', '', self.v_article)
		
		
		
		
			#print(lv_article['post'] + '\n\n\n\n\n\n\n')
			
		
		# <link href="<$URL_ROOT$><$URL_ASSET$>style.css" rel="stylesheet" type="text/css">
		# <link href="../wwwroot/asset/style.css" rel="stylesheet" type="text/css">
		# <$$>
	# </head>
	# <body itemscope itemtype="http://schema.org/WebPage">
		# <header>
			# <h1><$TITLE_SITE$></h1>
			# <nav><h2 class="WCAG_hide">Site Navigation</h2><ul><$NAV_SITE$></ul></nav>
		# </header>
		
		# <nav><h2 class="WCAG_hide">Page Navigation</h2><ul><$NAV_PAGE$></ul></nav>
		# <nav itemprop="breadcrumb" itemscope itemtype="http://schema.org/BreadcrumbList" aria-hidden="true"><h2>Breadcrumb</h2><$NAV_BREADCRUMB$></nav>
		
		# <main itemprop="mainEntity" itemscope itemtype="<$RICH_ITEMTYPE$>">
# <$CONTENT_WRAPPER$>
		# </main>
		
		# <footer>
			# <nav><h2 aria-hidden="true">Footer Navigation</h2><ul><$NAV_FOOT$></ul></nav>
			# <small>Website design and code &copy; 2016 OciCat Media; all content - unless specified otherwise - &copy; 2013 OciCat Media.<$CONTENT_FOOTER$></small>
		# </footer>
	# </body>






			


		
			
		
		
		#<$RICH_ITEMTYPE$> https://schema.org/BlogPosting
		

		
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
		self.x = pageid

class CompProduct:
	def __init__ (self, pageid):
		self.x = pageid

class CompSitemap:
	def __init__ (self, pageid):
		self.x = pageid
		
component = {'album':CompAlbum,'blog':CompBlog,'portfolio':CompPortfolio,'product':CompProduct,'sitemap':CompSitemap}
		
website = WebSite()
#print (WebSite.v_template)
#print(WebSite.v_meta)
#print(WebSite.v_nav)