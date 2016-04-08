CREATE DATABASE IF NOT EXISTS ocm_webcompile DEFAULT CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_section (
	Section_ID TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
	Section_Title VARCHAR(100) NOT NULL,
	PRIMARY KEY (Section_ID),
	UNIQUE KEY UN_Section_Title (Section_Title)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ocm_webcompile.site_page (
	Page_ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	Page_Title VARCHAR(100) NOT NULL,
	Page_Name VARCHAR(100) NOT NULL,
	Page_Path VARCHAR(200) NOT NULL,
	Page_MetaDesc VARCHAR(200) NOT NULL,
	Page_MetaKey VARCHAR(200) NOT NULL,
	Page_Content TEXT,
	Page_Type ENUM('page','album','blog','portfolio','product','sitemap') NOT NULL DEFAULT 'page',
	Page_Update INT(10) UNSIGNED NOT NULL DEFAULT 0,
	Section_ID TINYINT(1) UNSIGNED NOT NULL,
	PRIMARY KEY (Page_ID),
	UNIQUE KEY UN_Page_Title (Page_Title),
	UNIQUE KEY UN_Page_Path (Page_Path),
	UNIQUE KEY UN_Page_Name (Page_Name)
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
	Blog_ID TINYINT(1) UNSIGNED NOT NULL,
	PRIMARY KEY (Post_ID)
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









/*		DEFAULT VALUES FOR OCICATMEDIA.COM		*/
INSERT INTO ocm_webcompile.site_section (Section_ID, Section_Title) VALUES (1,"site"),(2,"foot"),(3,"home"),(4,"blog"),(5,"portfolio"),(6,"about"),(7,"contact");
INSERT INTO ocm_webcompile.site_page (Page_ID, Page_Title, Page_Name, Page_Path, Page_MetaDesc, Page_MetaKey, Page_Content, Section_ID) VALUES (1,"OciCat Media","Home","","The homepage of the website for OciCat Media: a high quality media company offerning a multitude of services.","Multimedia, Photography, Drafting, Computer Aided Drafting, CAD, Film, Video, Development, Web Development, Programming","<%%>",3,'page',1458033060),(2,"OciCat Media Blog","Blog","news","Every blog post and news article pertaining to OciCat Media, its projects, and work are indexed here.","Blog, News","<%BLOG_ARTICLE_INDEX%>",4,'blog',1458033060),(3,"OciCat Media Portfolio","Portfolio","portfolio","All of OciCat Media's previous works are gathered in the portfolio, grouped by various forms of media.","Multimedia, Photography, Picture, Image, Drafting, Computer Aided Drafting, CAD, Film, Video","<%%>",5,'portfolio',1460105520),(4,"Photography","Photographs","portfolio/photography","The index page of the photography section of OciCat Media's professional portfolio.","Multimedia, Photography, Picture, Image","<%PORTFOLIO_PHOTO_INDEX%>",5,'album',1460105520),(5,"Drafting","Drafting Projects","portfolio/drafting","The index page of the drafting and CAD section of OciCat Media's professional portfolio.","Multimedia, Drafting, Computer Aided Drafting, CAD","<%PORTFOLIO_CAD_INDEX%>",5,'album',1460105520),(6,"Video","Videos","portfolio/video","The index page of the film and video section of OciCat Media's professional portfolio.","Multimedia, Film, Video","<%PORTFOLIO_VIDEO_INDEX%>",5,'album',1460105520),(7,"About","About","about","Read all about OciCat Media, its founder Matthew Moore, and even learn a little about the company's namesake: the Ocicat.","About, About Us, OciCat Media, The Ocicat, Ocicat, Matthew Moore","<%%>",6,'page',1458750540),(8,"About OciCat Media","About OciCat Media","about/ocicat-media","Read all about OciCat Media, its founding, and how it promises to be a great choice for your multimedia needs.","About, About Us, OciCat Media","<%%>",6,'page',1458750540),(9,"About Matthew Moore","About Matthew Moore","about/matthew-moore","Read all about the founder of OciCat Media, Matthew Moore.","About, About Us, Matthew Moore","<%%>",6,'page',1458750540),(10,"About the Ocicat","About the Ocicat","about/ocicat","Read about the origins of this mystifying feline, and the awesome it is made of.","About, About Us, The Ocicat, Ocicat","<%%>",6,'page',1458750540),(11,"Contact OciCat Media","Contact Us","contact","Find the information you need, to get in touch with OciCat Media here.","Contact, Contact Us, Contact OciCat Media","<%%>",7,'page',1460105520),(12,"Our Policies","Policies","policy","All of the policies and standards OciCat Media holds itself - and its work - to, gathered in one handy place.","Policy, Policies, Accessibility, Privacy, Discretion, Fair Use","<%%>",2,'page',1460105520),(13,"Our Licensing Details","Licenses","license","Check here for all of the information regarding our licenses, such as copyright, trademarks, and fair use policies.","License, Licenses, Copyright, Trademark, Fair Use","<%%>",2,'page',1460105520),(14,"OciCat Media Sitemap","Sitemap","sitemap","The sitemap for OciCatMedia.com","Sitemap","<%SITEMAP%>",2,'sitemap',1460105520);
INSERT INTO ocm_webcompile.site_nav (Nav_ID, Nav_Title, Nav_Order, Section_ID, Page_ID) VALUES (1,"Home",1,1,1),(2,"Blog",2,1,2),(3,"Portfolio",3,1,3),(4,"About",4,1,7),(5,"Contact",5,1,11),(6,"Policies",1,2,12),(7,"Licenses",2,2,13),(8,"Sitemap",3,2,14),(9,"Photography",1,5,4),(10,"Drafting",2,5,5),(11,"Video",3,5,6),(12,"OciCat Media",1,6,8),(13,"Matthew Moore",2,6,9),(14,"The Ocicat",3,6,10);

INSERT INTO ocm_webcompile.default_meta (Meta_ID, Meta_Tag, Meta_Value) VALUES (1,"language","en-ca"),(2,"appname","OciCat Media"),(3,"author","Matthew Moore"),(4,"keywords","OciCat Media, Multimedia Provider,"),(5,"description",""),(6,"title","OciCat Media");
INSERT INTO ocm_webcompile.default_url (Url_ID, Url_Name, Url_Value) VALUES (1,"root","http://ocicatmedia.github.io/"),(2,"asset","asset/"),(3,"path","..\wwwroot\\"),(4,"user","http://ocicatmedia.github.io/user/");






