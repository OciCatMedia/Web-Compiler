import datetime
import mysql.connector
import re


	
	
	
class WebSite:
	v_page = []
	v_meta = {
		'language':'en-ca',
		'appname':'OciCat Media',
		'author':'Matthew Moore',
		'keywords':'OciCat Media, Multimedia Provider,',
		'description':'',
		'title':'OciCat Media'
		}
	v_title = {
		'site':'OciCat Media',
		'page':''
		}	
	v_nav = {
		'site':[['Home',''],['Portfolio','portfolio'],['Contact','contact'],['About','about']],
		'foot':[['Site Map','sitemap.html'],['Policy','policy.html'],['License','license.html'],['GitHub','https://github.com/OciCatMedia']],
		'Home':[['Latest News','#news'],['Archived News','news']],
		'About':[['OciCat Media','#ocicatmedia'],['Matthew Moore','#matthewmoore'],['The OciCat','#theocicat']]
		}
	v_url = {
		'root':'http://ocicatmedia.github.io/',
		'asset':'asset/',
		'path':'..\wwwroot\\',
		'user':'http://ocicatmedia.github.io/user/'
		}
	v_cont = {
		'content':'',
		'foot':'Website design and code &copy; 2016 OciCat Media; all content - unless specified otherwise - &copy; 2013 OciCat Media.'
		}
	v_template = ''
		
	def __init__ (self):
		
		with open('template\\0.html', 'r') as tmp_template:
			WebSite.v_template = tmp_template.read()


		WebSite.v_template = WebSite.v_template.replace('<$NAV_FOOT$>',build_nav('foot',''))
		
		WebSite.v_template = WebSite.v_template.replace('<$META_LANGUAGE$>',WebSite.v_meta['language'])
		WebSite.v_template = WebSite.v_template.replace('<$META_APPNAME$>',WebSite.v_meta['appname'])
		WebSite.v_template = WebSite.v_template.replace('<$META_AUTHOR$>',WebSite.v_meta['author'])
		WebSite.v_template = WebSite.v_template.replace('<$META_KEYWORD$>',WebSite.v_meta['keywords'] + '<$META_KEYWORD$>')

		WebSite.v_template = WebSite.v_template.replace('<$URL_ROOT$>',WebSite.v_url['root'])
		WebSite.v_template = WebSite.v_template.replace('<$URL_ASSET$>',WebSite.v_url['asset'])

		WebSite.v_template = WebSite.v_template.replace('<$TITLE_SITE$>',WebSite.v_title['site'])

		WebSite.v_template = WebSite.v_template.replace('<$CONTENT_FOOTER$>',WebSite.v_cont['foot'])
		
	



class WebPage:
	
	def __init__ (self,nav_section,nav_page,page_title,meta_title,meta_keyword,meta_description):
		self.children = {'article':[],'archive':[]}
		
		self.v_template = website.v_template
		self.v_template = self.v_template.replace('<$NAV_SITE$>',build_nav('site',nav_section))
		self.v_template = self.v_template.replace('<$NAV_PAGE$>',build_nav(nav_section,nav_page))
		
		self.v_template = self.v_template.replace('<$META_KEYWORD$>',meta_keyword)
		self.v_template = self.v_template.replace('<$META_DESCRIPTION$>',meta_description)
		self.v_template = self.v_template.replace('<$META_TITLE$>',meta_title)
		
		self.v_template = self.v_template.replace('<$TITLE_PAGE$>',page_title)
		
		self.v_template = self.v_template.replace('<$META_TITLE$>',meta_title)
		
		

	def SiteNews (self):
		
		with open('template\\news\\article-content.html', 'r') as tmp_template:
			self.v_article = tmp_template.read()

		cnx_news = mysql.connector.connect(user='localread')
		cursor_news = cnx_news.cursor(dictionary=True)

		query = (
			"SELECT News_ID, News_Title, News_Content, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(News_Epoch),'America/Toronto','UTC'), '%H:%i %b %e, %Y') AS News_Date, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(News_Epoch),'America/Toronto','UTC'), '%Y-%m-%dT%H:%i:%sZ') AS News_DateRFC, 'Aurani' AS User_Name, COUNT(comment_ID) AS Comment_Count FROM ocm_generic.site_news LEFT JOIN ocm_generic.news_comment ON ocm_generic.site_news.News_ID = ocm_generic.news_comment.Comment_Title WHERE News_Live <= UNIX_TIMESTAMP(NOW()) GROUP BY News_ID ORDER BY News_Epoch DESC LIMIT 0,1")

		cursor_news.execute(query)
		news_article = cursor_news.fetchall()
		
		for article in news_article:
			tmp_url = {
				'path':'news\\',
				'url':'news/',
				'filename': str(article['News_ID']) + "-" + re.sub("[^\w\-]", "", re.sub("\s", "-", article['News_Title'])) + '.html'
			}
			
			self.children['article'].append(self.v_article)
			
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_ID$>',str(article['News_ID']))
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_CONTENT$>',article['News_Content'])
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_URL$>',website.v_url['root'] + tmp_url['url'] + tmp_url['filename'])

			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_AUTHOR$>',article['User_Name'])
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_AUTHORURL$>',website.v_url['user'] + article['User_Name'].lower() + '/')
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_AUTHORIMAGE$>',website.v_url['user'] + article['User_Name'].lower() + '/avatar.png')


			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_DATE$>',article['News_Date'])
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_DATERFC$>',article['News_DateRFC'])

			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_PUBLISHER$>',website.v_title['site'])
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_PUBLISHERLOGO$>',website.v_url['root'] + website.v_url['asset'] + 'logobkg.png')
			
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_IMAGE$>',website.v_url['root'] + website.v_url['asset'] + 'articledefault.png')
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_IMAGEWIDTH$>',str(700))
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_IMAGEHEIGHT$>',str(200))

			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_COMMENT_COUNT$>',str(article['Comment_Count']))

			self.children['archive'].append(self.children['article'][-1])
			
			
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_TITLE$>','<h2 itemprop="headline name">' + article['News_Title'] + '</h2>')
			self.children['archive'][-1] = self.children['archive'][-1].replace('<$NEWS_TITLE$>','<h3 itemprop="headline name"><a href="' + website.v_url['root'] + tmp_url['url'] + tmp_url['filename'] + '">' + article['News_Title'] + '</a></h3>')
			
			with open('template\\news\\article.html', 'r') as tmp_template:
				self.children['article'][-1] = tmp_template.read().replace('<$NEWS_ARTICLE_CONTENT$>',self.children['article'][-1])
			
			self.children['article'][-1] = self.v_template.replace('<$CONTENT$>',self.children['article'][-1])
			
			self.children['article'][-1] = self.children['article'][-1].replace('<$ARTICLE_NAME$>', article['News_Title'])
			self.children['article'][-1] = self.children['article'][-1].replace('<$NEWS_SECTION$>', 'Wednesday: ')
			self.children['article'][-1] = self.children['article'][-1].replace('<$ARTICLE_KEYWORD$>', 'more, words, stuff')
			self.children['article'][-1] = self.children['article'][-1].replace('<$ARTICLE_DESCRIPTION$>', 'a blog posting of stuff.')

			self.children['article'][-1] = self.children['article'][-1].replace('<$META_LINK$>', '<link rel="canonical" href="' + website.v_url['root'] + tmp_url['url'] + tmp_url['filename'] + '" />\n\t\t<link rel="prev" href="http://ocicatmedia.github.io/news/2.html" />')
			


			

			
			print(self.children['article'][-1])
			print('\n\n\n')
			print("========================================================")
			print("========================================================")
			print("========================================================")
			print('\n\n\n')

		cursor_news.close()
		cnx_news.close()		


		#'The official news for OciCat Media.'
		
		
		
		
		
		
		

def build_nav (type,active):
	tmp_nav = []
	tmp_ret = ''

	tmp_arr = WebSite.v_nav[type]

	for i in tmp_arr:
		if (re.match("#", i[1])):
			tmp_nav.append('<a href="' + i[1] + '">' + i[0] + '</a>')
		elif (re.match("[a-z]+://", i[1])):
			tmp_nav.append('<a href="' + i[1] + '" rel="external">' + i[0] + '</a>')
		else:
			tmp_nav.append('<a href="' + WebSite.v_url['root'] + i[1] + '/">' + i[0] + '</a>')

		if (i[0] == active):
			tmp_nav[-1] = '<li class="active">' + tmp_nav[-1] + '</li>'
		else:
			tmp_nav[-1] = '<li>' + tmp_nav[-1] + '</li>'
		
	for i in tmp_nav:
		tmp_ret = tmp_ret + i 
		
	tmp_ret = '<ul>' + tmp_ret + '</ul>'
	
	return tmp_ret
	

		

		
website = WebSite()
website.v_page.append(WebPage('Home','Archived News','<$ARTICLE_NAME$>','<$NEWS_SECTION$><$ARTICLE_NAME$>','News Post, Blog Post, OciCat Media News, <$ARTICLE_KEYWORD$>','<$ARTICLE_DESCRIPTION$>'))
website.v_page[-1].SiteNews()





#Site.build_nav('site','home')
#Site.build_nav('foot','')


#print(website.v_template)

#print (cheese.v_template)

#Site.build_nav('home','')
	
	
	
# for i in website.v_page:
	
	
	# for ii in i.v_template:
		
		# print (ii + " \t\t==================")
		# print (ii + " \t\t==================")
		# print (ii + " \t\t==================")
		# print (ii + " \t\t==================")
		# print (ii + " \t\t==================")
		# print (ii + " \t\t==================")
	
		# print(i.v_template[ii])
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#nav_page = {'index'['Home',''],['Portfolio','portfolio'],['Contact','contact'],['About','about']]


#<a href="#ocicatmedia">OciCat Media</a>
#<a href="#matthewmoore">Matthew Moore</a>
#<a href="#theocicat">The OciCat</a>
