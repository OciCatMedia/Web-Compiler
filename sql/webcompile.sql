CREATE DATABASE IF NOT EXISTS ocm_webcompile DEFAULT CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_section (
	Section_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Section_Name VARCHAR(100) NOT NULL,
	PRIMARY KEY (Section_ID),
	UNIQUE KEY UN_Section_Title (Section_Title)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_page (
	Page_ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	Page_Name VARCHAR(100) NOT NULL,
	Page_Path VARCHAR(200) NOT NULL,
	Page_Type ENUM('page','album','blog','portfolio','product','sitemap') NOT NULL DEFAULT 'page',
	Page_Publish INT(10) UNSIGNED NOT NULL DEFAULT 0,
	Section_ID TINYINT(1) UNSIGNED NOT NULL,
	PRIMARY KEY (Page_ID),
	UNIQUE KEY UN_Path_Name (Page_Path,Page_Name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_page_version (
	Version_ID BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	Version_Title VARCHAR(100) NOT NULL,
	Version_MetaDesc VARCHAR(200) NOT NULL,
	Version_MetaKey VARCHAR(200) NOT NULL,
	Version_Content TEXT,
	Version_Update INT(10) UNSIGNED NOT NULL DEFAULT 0,
	Version_Publish INT(10) UNSIGNED NOT NULL DEFAULT 0,
	Page_ID INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (Version_ID),
	UNIQUE KEY UN_Page_Title (Version_Title)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_nav (
	Nav_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Nav_Title VARCHAR(100) NOT NULL,
	Nav_Order TINYINT(1) UNSIGNED NOT NULL,
	Section_ID TINYINT(1) UNSIGNED NOT NULL,
	Page_ID INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (Nav_ID),
	UNIQUE KEY UN_Section_Order (Section_ID,Nav_Order)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS ocm_webcompile.default_meta (
	Meta_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Meta_Tag VARCHAR(50) NOT NULL,
	Meta_Value VARCHAR(100) NOT NULL,
	PRIMARY KEY (Meta_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS ocm_webcompile.default_url (
	Url_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Url_Name VARCHAR(50) NOT NULL,
	Url_Value VARCHAR(100) NOT NULL,
	PRIMARY KEY (Url_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS ocm_webcompile.comp_album (
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.comp_blog (
	Blog_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Blog_Title VARCHAR(100) NOT NULL,
	Page_ID INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (Post_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.comp_blog_post (
	Post_ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	Post_Title VARCHAR(100) NOT NULL,
	Post_Content TEXT NOT NULL,
	Post_Epoch INT(10) UNSIGNED NOT NULL,
	Post_Live INT(10) UNSIGNED NOT NULL,
	Post_IP VARCHAR(39) NOT NULL,
	Blog_ID TINYINT(1) UNSIGNED NOT NULL,
	User_ID INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (Post_ID)
) ENGINE=InnoDB;


/*		DEFAULT VALUES FOR OCICATMEDIA.COM		*/
INSERT INTO ocm_webcompile.site_section (Section_ID, Section_Title) VALUES (1,"site"),(2,"foot"),(3,"home"),(4,"blog"),(5,"portfolio"),(6,"about"),(7,"contact");
INSERT INTO ocm_webcompile.site_page (Page_ID, Page_Name, Page_Path, Page_Type, Page_Publish, Section_ID) VALUES (1,"Home","","page",1458033060,3),(2,"Blog","news","blog",1458033060,4),(3,"Portfolio","portfolio","portfolio",1460105520,5),(4,"Photographs","portfolio/photography","album",1460105520,5),(5,"Drafting Projects","portfolio/drafting","album",1460105520,5),(6,"Videos","portfolio/video","album",1460105520,5),(7,"About","about","page",1458750540,6),(8,"About OciCat Media","about/ocicat-media","page",1458750540,6),(9,"About Matthew Moore","about/matthew-moore","page",1458750540,6),(10,"About the Ocicat","about/ocicat","page",1458750540,6),(11,"Contact Us","contact","page",1460105520,7),(12,"Policies","policy","page",1460105520,2),(13,"Licenses","license","page",1460105520,2),(14,"Sitemap","sitemap","sitemap",1460105520,2);
INSERT INTO ocm_webcompile.site_page_version (Version_ID, Version_Title, Version_MetaDesc, Version_MetaKey, Version_Content, Version_Update, Version_Publish, Page_ID) VALUES (1,"OciCat Media","The homepage of the website for OciCat Media: a high quality media company offerning a multitude of services.","Multimedia, Photography, Drafting, Computer Aided Drafting, CAD, Film, Video, Development, Web Development, Programming","<$$>",1458033060,1458033060,1),(2,"OciCat Media Blog","Every blog post and news article pertaining to OciCat Media, its projects, and work are indexed here.","Blog, News","<$BLOG_ARTICLE_INDEX$>",1458033060,1458033060,2),(3,"OciCat Media Portfolio","All of OciCat Media's previous works are gathered in the portfolio, grouped by various forms of media.","Multimedia, Photography, Picture, Image, Drafting, Computer Aided Drafting, CAD, Film, Video","<$$>",1460105520,1460105520,3),(4,"Photography","The index page of the photography section of OciCat Media's professional portfolio.","Multimedia, Photography, Picture, Image","<$PORTFOLIO_PHOTO_INDEX$>",1460105520,1460105520,4),(5,"Drafting","The index page of the drafting and CAD section of OciCat Media's professional portfolio.","Multimedia, Drafting, Computer Aided Drafting, CAD","<$PORTFOLIO_CAD_INDEX$>",1460105520,1460105520,5),(6,"Video","The index page of the film and video section of OciCat Media's professional portfolio.","Multimedia, Film, Video","<$PORTFOLIO_VIDEO_INDEX$>",1460105520,1460105520,6),(7,"About","Read all about OciCat Media, its founder Matthew Moore, and even learn a little about the company's namesake: the Ocicat.","About, About Us, OciCat Media, The Ocicat, Ocicat, Matthew Moore","<$CONTENT GOES HERE$>",1458750540,1458750540,7),(8,"About OciCat Media","Read all about OciCat Media, its founding, and how it promises to be a great choice for your multimedia needs.","About, About Us, OciCat Media","<$CONTENT GOES HERE$>",1458750540,1458750540,8),(9,"About Matthew Moore","Read all about the founder of OciCat Media, Matthew Moore.","About, About Us, Matthew Moore","<$CONTENT GOES HERE$>",1458750540,1458750540,9),(10,"About the Ocicat","Read about the origins of this mystifying feline, and the awesome it is made of.","About, About Us, The Ocicat, Ocicat","<$CONTENT GOES HERE$>",1458750540,1458750540,10),(11,"Contact OciCat Media","Find the information you need, to get in touch with OciCat Media here.","Contact, Contact Us, Contact OciCat Media","<$CONTENT GOES HERE$>",1460105520,1460105520,11),(12,"Our Policies","All of the policies and standards OciCat Media holds itself - and its work - to, gathered in one handy place.","Policy, Policies, Accessibility, Privacy, Discretion, Fair Use","<$CONTENT GOES HERE$>",1460105520,1460105520,12),(13,"Our Licensing Details","Check here for all of the information regarding our licenses, such as copyright, trademarks, and fair use policies.","License, Licenses, Copyright, Trademark, Fair Use","<$CONTENT GOES HERE$>",1460105520,1460105520,13),(14,"OciCat Media Sitemap","The sitemap for OciCatMedia.com","Sitemap","<$SITEMAP$>",1460105520,1460105520,14);

INSERT INTO ocm_webcompile.site_nav (Nav_ID, Nav_Title, Nav_Order, Section_ID, Page_ID) VALUES (1,"Home",1,1,1),(2,"Blog",2,1,2),(3,"Portfolio",3,1,3),(4,"About",4,1,7),(5,"Contact",5,1,11),(6,"Policies",1,2,12),(7,"Licenses",2,2,13),(8,"Sitemap",3,2,14),(9,"Photography",1,5,4),(10,"Drafting",2,5,5),(11,"Video",3,5,6),(12,"OciCat Media",1,6,8),(13,"Matthew Moore",2,6,9),(14,"The Ocicat",3,6,10);

INSERT INTO ocm_webcompile.default_meta (Meta_ID, Meta_Tag, Meta_Value) VALUES (1,"language","en-ca"),(2,"appname","OciCat Media"),(3,"author","Matthew Moore"),(4,"keyword","OciCat Media, Multimedia Provider,<$META_KEYWORD$>"),(5,"description","<$META_DESCRIPTION$>"),(6,"title","<$META_TITLE$>"),(7,"link","<$META_LINK$>");
INSERT INTO ocm_webcompile.default_url (Url_ID, Url_Name, Url_Value) VALUES (1,"root","http://ocicatmedia.github.io/"),(2,"asset","asset/"),(3,"path","wwwroot\\"),(4,"user","http://ocicatmedia.github.io/user/");

INSERT INTO ocm_webcompile.comp_blog (Blog_ID, Blog_Title, Page_ID) VALUES (1,"OciCat Media News",2)
INSERT INTO ocm_webcompile.comp_blog_post (Post_ID, Post_Title, Post_Content, Post_Epoch, Post_Live, Post_IP, Blog_ID, User_ID) VALUES (1,"New Site is Live!","<p>It took longer than I had anticipated - due to unexpected projects cropping up - but the new OciCatMedia.com website is now live! It's been made to look sleeker and a tad more professional, and being functional. There are still features to add in the coming days, so check back if there's something missing!</p><p>Due to some unforseen issues on the migration from development to live environments, a couple of features are disabled temporarily.</p>",1421778821,1421778821,"127.0.0.1",1,1),(2,"New Site is Back(ish)!","<p>Well, the main components of the site are back, hopefully we won't be having more errors yet. The features are still disabled as we wrangle the database to accept my procedures.</p>",1421870762,1421870762,"127.0.0.1",1,1),(3,"Site's Running Smooth","<p>So the site is currently running at it's full potential. If you notice anything wrong, feel free to let me know via the contact page.</p>",1422458109,1422458109,"127.0.0.1",1,1),(4,"New Site Development is Underway","<p>I've begun working on yet another new version of this website. This time I'll be focusing on using it as a learning experience with <a rel=\"external\" href=\"https://nodejs.org\">Node.JS</a>, to expand my development repertoire.</p>",1456683882,1456683882,"127.0.0.1",1,1),(5,"New Site and Accessibility","<p>Current focus for the site is on the design and functionality. Functionally, I'm paying extra attention to accessibility and microdata. I intend this site - and my future work - to be fully compliant with <a rel=\"external\" href=\"https://www.w3.org/WAI/intro/aria\">WAI-ARIA</a>, <a rel=\"external\" href=\"https://www.w3.org/WAI/intro/wcag\">WCAG</a>, and <a rel=\"external\" href=\"https://developers.google.com/structured-data/rich-snippets/\">Google Rich Snippets</a>.</p>",1456775852,1456775852,"127.0.0.1",1,1),(6,"New Site Updates","<p>Keep up to date on the development of the website - and other projects of ours - over at the OciCat Media <a rel=\"external\" href=\"https://github.com/OciCatMedia/ocicatmedia.com\">GitHub Repository</a>.</p>",1456936331,1456936331,"127.0.0.1",1,1),(7,"And Now for Something Completely Different","<p>In order to get the site up and running as fast as I can, I'll be skipping on the <a rel=\"external\" href=\"https://nodejs.org\">Node.JS</a> at the moment; focus is being put on static pages, with a small <a rel=\"external\" href=\"https://www.python.org/\">Python</a> script to dynamically create the pages.</p>",1457019309,1457019309,"127.0.0.1",1,1),(8,"It's Alive!","<p>My <a rel=\"external\" href=\"https://www.python.org/\">Python</a> webpage compiler script is successfully creating static HTML pages, dynamically.</p><p>The next step will be generating this blog with it... So everything I've been entering in here will become visible to people.</p>",1460215390,1460215390,"127.0.0.1",1,1);















