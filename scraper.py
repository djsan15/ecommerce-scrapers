#INPUT DATA
designer_urls_voylla={
'https://www.voylla.com/jewellery/earrings?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=999+to+3600&collection%5B%5D=Traditional+and+imitation':80,
'https://www.voylla.com/jewellery/earrings?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=1299+to+2600&collection%5B%5D=Classic':161,
'https://www.voylla.com/jewellery/earrings?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=349+to+499&theme%5B%5D=classic&occasion%5B%5D=Party+wear&occasion%5B%5D=Special+occasions':332,
'https://www.voylla.com/jewellery/earrings/ear-cuffs':19,
'https://www.voylla.com/jewellery/earrings/hoops?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=739+to+5000':107,
'https://www.voylla.com/jewellery/rings/solitaire?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=1200+to+5000':190,
'https://www.voylla.com/jewellery/rings/statement?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=174+to+5000':123,
'https://www.voylla.com/jewellery/necklaces?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=299+to+1049':650,
'https://www.voylla.com/jewellery/bracelets/cuffs?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=174+to+5000':86,
'https://www.voylla.com/jewellery/bracelets/slave':18,
'https://www.voylla.com/silver/silver-necklaces?utf8=%E2%9C%93&per_page=&vprice_between%5D%5B%5D=1580+to+5000':10,
	}

designer_urls_exclusively = [
#'http://in.exclusively.com/search?keyword=blushing%20couture&categoryId=0&internalRequestType=filter&sort=rec',
# 'http://in.exclusively.com/search?keyword=Nidhika+Shekhar&categoryId=0',
# 'http://in.exclusively.com/search?keyword=sadan+pane&categoryId=0',
# 'http://in.exclusively.com/search?keyword=Sonia+Jetleey&categoryId=0',
'http://in.exclusively.com/search?keyword=Soup%20By%20Sougat%20Paul&categoryId=0&internalRequestType=filter&sort=rec',
'http://in.exclusively.com/search?keyword=study+by+janak&categoryId=0',
'http://in.exclusively.com/search?keyword=tanko+by+shipra&categoryId=0',
'http://in.exclusively.com/search?keyword=%09Vandana+Sethi&categoryId=0',
'http://in.exclusively.com/search?keyword=Vemanya&categoryId=0',
	]



#DO NOT EDIT BELOW THIS
from urllib2 import urlopen,Request
import urllib
from bs4 import BeautifulSoup
import pprint
import json
from sys import argv
from urlparse import urlparse
import HTMLParser
import time
import os.path
import os
import collections
import csv
import requests
import math
import datetime
import uuid
import socket
#execfile('/home/sanchit/glitstreet-project/scraper.py')
scraper_url_exc='http://in.exclusively.com'
scraper_url_voy = 'https://www.voylla.com'

def get_html(url):
	html=""
	try:
		html = urlopen(url,timeout=30).read()
	except socket.timeout:
		print "TIMEOUT: sleeping for 5 mins"
		time.sleep(100)
		try:
			html = urlopen(url,timeout=30).read()
		except:
			print "TIMEOUT"
	except:
		print "Sleeping 5 mins"
		time.sleep(300)
		try:
			html = urlopen(url).read()
		except:
			print "Sleeping 15 mins"
			time.sleep(900)
			try:
				html = urlopen(url).read()
			except:
				print "Sleeping 1 hr"
				time.sleep(3600)
				html = urlopen(url).read()
	return html

def get_product_data_exc(prod_url):
	prod_url = prod_url.replace(' ','%20')
	if scraper_url_exc not in prod_url:
		prod_url = scraper_url_exc + prod_url
	time.sleep(1)
	print '------FETCHING DATA FOR: '+prod_url+'  ---------------'
	att_headers = []
	image_count=0
	html = get_html(prod_url)
	soup= BeautifulSoup(html,'lxml')
	prod = {}
	try:
		prod['designer name'] = soup.select('p.designerName span:nth-of-type(1)')[0].text.strip()
	except:
		prod['designer name'] = ' '
	try:
		prod['name'] = soup.select("p.prdName")[0].text.strip()
	except:
		prod['name']= ' '
	try:
		prod['selling price'] = soup.select('span.productFinalPrice')[0].text.strip()
	except:
		prod['selling price']= ' '
	try:
		prod['description'] = soup.select('input.description')[0].attrs.get('value','').replace(';',' ').strip()# p.prdInfo.text
	except:
		prod['description']= ' '
	attrs_soup = soup.select('li.pad-xsm-tb')
	for att in attrs_soup:
		k= att.select('span.col-xs-5')[0].text.strip().lower()
		if k in ['colour','fabric']:
			try:
				prod[k] = att.select('span.col-xs-7')[0].text.strip()
			except:
				prod[k] = ' '
	prod['image_urls']=[]
	for image_url in soup.select('img.pdpImgTag'):
		image_count+=1
		prod['image_urls'].append(str(image_url.attrs.get('src')).strip())
	print prod
	print '----------------DONE---------------------'
	return {'prod':prod,'att_headers':att_headers,'image_count':image_count}

def get_product_urls(infinite_url,selector):
	prod_urls= []
	soup= BeautifulSoup(get_html(infinite_url),'lxml')
	s= soup.select(selector)
	for a in s:
		prod_urls.append(a.attrs.get('href'))
	return prod_urls

def get_designer_data_exc(designer_url):
	time.sleep(5)
	print "---------------FETCHING DESIGNER PRODUCT URLS----------------------"
	product_urls=[]
	ppp=24
	html = get_html(designer_url)
	soup= BeautifulSoup(html,'lxml')
	s= soup.select('div.imgdiv a')
	for a in s:
		product_urls.append(a.attrs.get('href'))
	infinite_urls=[]
	resultcount= int(soup.select('label#resultcount')[0].text.split('[')[1].split()[0])
	for i in range(1,int(resultcount/ppp)):
		infinite_urls.append(designer_url+'&start='+str(i*ppp))
	if resultcount % ppp !=0:
		infinite_urls.append(designer_url+'&start='+str(int(resultcount/ppp)*ppp))
	# print infinite_urls
	for u in infinite_urls[:1]:
		product_urls += get_product_urls(u,'div.imgdiv a')
	print len(product_urls)
	print '----------------DONE---------------------'
	return product_urls

def csv_exporter(designer_name,prod,headers):
	directory = os.getcwd()+'/'
	file_name = directory+designer_name+'.csv'
	file_exists=False
	if not os.path.exists(directory):
		os.makedirs(directory)
	if os.path.isfile(file_name):
		myfile = open(file_name, 'ab')
		file_exists = True
	else:
		myfile = open(file_name, 'wb')
	try:
		writer = csv.writer(myfile)
		if not file_exists:
			writer.writerow(headers)
		row = []
		for k in headers:
			row.append(prod.get(k,' '))
		writer.writerow(row)
	except:
		print "csv writer exception"
	finally:
		myfile.close()

def main_exc():
	designer_urls = designer_urls_exclusively
	headers = ['designer name','name','selling price','description','colour','fabric','image_urls']
	for designer_url in designer_urls:
		designer_page_data = get_designer_data_exc(designer_url)
		for u in designer_page_data:
			prod_data = get_product_data_exc(scraper_url_exc+u.replace(' ','%20'))
			csv_exporter('exclusively-'+designer_url.split('/')[-1].split('?')[0].replace('%20',' ').replace('&',''),prod_data['prod'],headers)

def get_designer_data_voy(designer_url,resultcount=36):
	print "---------------FETCHING DESIGNER PRODUCT URLS----------------------"
	product_urls=[]
	ppp=36
	html = get_html(designer_url)
	soup= BeautifulSoup(html,'lxml')
	s = soup.select('div.product_listing_image a')
	for a in s:
		product_urls.append(a.attrs.get('href'))
	infinite_urls=[]
	resultcount= int(resultcount)
	total_pages = int(math.ceil(resultcount/ppp))
	for i in range(2,total_pages+1):
		infinite_urls.append(designer_url+'&page='+str(i))
	for u in infinite_urls:
		product_urls += get_product_urls(u,'div.product_listing_image a')
	# print product_urls
	print len(product_urls)
	print '----------------DONE---------------------'
	return product_urls

def get_product_data_voy(prod_url):
	prod_url= prod_url.replace(' ','%20')
	if scraper_url_voy not in prod_url:
		prod_url = scraper_url_voy + prod_url
	time.sleep(1)
	print '------FETCHING DATA FOR: '+prod_url+'  ---------------'
	att_headers = []
	image_count=0
	html = get_html(prod_url)
	soup= BeautifulSoup(html,'lxml')
	prod={}
	try:
		prod['name'] = soup.select("h1")[0].text.strip().encode('ascii', 'ignore')
	except:
		prod['name']= ' '
	try:
		prod['selling price'] = soup.select('dd span.price')[0].text.strip().split('.')[1].strip().replace(',','').encode('ascii', 'ignore')
	except:
		prod['selling price']= ' '
	try:
		prod['description']= ''
		for para in soup.select('div.pd-tab-height-nosz p'):
			prod['description'] += para.text.strip().encode('ascii', 'ignore')
	except:
		prod['description']= ' '
	try:
		prod['colour']=''
		prop_list  = soup.select('div[id^="product-properties-display"]')[1].select('td')
		for i,col in enumerate(prop_list):
			if 'colour' in col.text.lower():
				prod['colour'] += prop_list[i+1].text.strip().encode('ascii', 'ignore')+','
			if 'design:' in col.text.lower():
				prod['description'] += '|'+prop_list[i+1].text.strip().encode('ascii', 'ignore')+'|'
	except:
		prod['colour']=''
	try:
		cols = soup.select('td.title')
		for i,col in enumerate(cols):
			if 'material:' in col.text.lower():
				prod['material']= cols[i+1].text.strip().encode('ascii', 'ignore')
	except:
		prod['material'] = ' '
	prod['image_urls']=[]
	for image_url in soup.select('a.cloud-zoom'):
		image_count+=1
		im_url=''
		for sc in image_url.script:
			for s in sc.strip().split():
				if s[1:5] == 'http':
					im_url = s[1:-2]
		prod['image_urls'].append(str(im_url))
	try:
		prod['dimensions']=''
		cols = soup.select('div[id^="product-dimensions-display"]')[1].select('td')
		for i,col in enumerate(cols):
			if i%2 != 0:
				continue
			try:
				prod['dimensions'] += cols[i].text.encode('ascii', 'ignore')+cols[i+1].text.encode('ascii', 'ignore') +', '
			except:
				pass
	except:
		prod['dimensions']=' '
	prod['designer name']='Voylla'
	print prod
	print '----------------DONE---------------------'
	return {'prod':prod}

def main_voy():
	designer_urls = designer_urls_voylla
	headers = ['designer name','name','selling price','description','colour','material','dimensions','image_urls']
	for designer_url in designer_urls.keys():
		designer_page_data = get_designer_data_voy(designer_url,designer_urls[designer_url])
		for u in designer_page_data:
			prod_data = get_product_data_voy(scraper_url_voy+u.replace(' ','%20'))
			csv_exporter('voylla-'+designer_url.split('/')[-1].split('?')[0].replace('%20',' ').replace('&',''),prod_data['prod'],headers)

def get_designer_data_snap(designer_url,cat_id=0,start_count=0):
	try:
		root_cat_id = str(int(designer_url.split(':')[1]))
	except:
		root_cat_id = str(cat_id)
	parsed_url = urlparse(designer_url)
	query = ''
	for q in parsed_url.query.split('&'):
		query +=q +'&'
	cat_name = parsed_url.path.split('/')[-1]
	api_url = "https://www.snapdeal.com/acors/json/product/get/search/"+root_cat_id+"/"
	api_url2= "/20?"+query+"brandPageUrl=&keyword=&searchState=categoryRedirected="+cat_name+"|previousRequest=true|serviceabilityUsed=false&pincode=&vc=&webpageName=categoryPage&campaignId=&brandName=&isMC=false&clickSrc=unknown&showAds=true&cartId="
	print api_url+str(start_count)+api_url2
	product_urls=[]
	ppp=20
	html = get_html(api_url+str(start_count)+api_url2)
	soup= BeautifulSoup(html,'lxml')
	infinite_urls=[]
	resultcount= int(soup.select('div.jsNumberFound')[0].text)
	print resultcount
	for i in range(start_count,int(resultcount/ppp)):
		infinite_urls.append(api_url+str(i*ppp)+api_url2)
	if resultcount % ppp !=0:
		infinite_urls.append(api_url+str(int(resultcount/ppp)*ppp)+api_url2)
	for u in infinite_urls:
		product_urls += get_product_urls(u,'div.product-tuple-image a.dp-widget-link')
	# print product_urls
	return product_urls

def store_image(url,storename="default",productname="default-product",image_count=1):
	r = requests.get(url, stream=True)
	directory = os.getcwd() + '/images/'+storename+'/'+productname+'/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	try:
		filename = url.split('//')[2]
	except:
		filename = 'default-'+str(uuid.uuid4())+'.'+url.split('.')[-1].split('?')[0]
	try:
		if r.status_code == 200:
			with open(directory+filename, 'wb') as f:
				for chunk in r:
					f.write(chunk)
				f.close()
	except:
		print "COULD NOT DOWNLOAD"

def download_images(file_name):
	if file_name.split('.')[-1] !='csv':
		return "please enter a csv file"
	with open(file_name) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			image_urls =filter(None,str(row['image_urls'])[1:-1].split(','))
			if not image_urls:
				image_urls =[]
			print image_urls
			for i,im_url in enumerate(list(image_urls)):
				im_url = str(im_url.strip()).replace("'","").replace('"','').strip()
				if "images.voylla.com" in im_url:
					im_url= im_url.replace("/large/","/original/")
				print im_url
				store_image(im_url,row.get('designer name'),row.get('name'),i)
