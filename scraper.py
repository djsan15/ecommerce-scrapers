#INPUT DATA
designer_urls_amazon={
'http://www.amazon.in/s/ref=sr_pg_1?rh=n%3A1571271031%2Cp_4%3AIndian+Poshakh&ie=UTF8&qid=1481197273':'ahs2',
}
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
'https://in.exclusively.com/brand/Qbik'
# 'http://in.exclusively.com/search?keyword=vandana&categoryId=0&internalRequestType=filter&q=Brand%3AVandana%20Sethi',
# 'http://in.exclusively.com/search?keyword=soup&categoryId=0'
#'http://in.exclusively.com/search?keyword=blushing%20couture&categoryId=0&internalRequestType=filter&sort=rec',
# 'http://in.exclusively.com/search?keyword=Nidhika+Shekhar&categoryId=0',
# 'http://in.exclusively.com/search?keyword=sadan+pane&categoryId=0',
# 'http://in.exclusively.com/search?keyword=Sonia+Jetleey&categoryId=0',
# 'http://in.exclusively.com/search?keyword=Soup%20By%20Sougat%20Paul&categoryId=0&internalRequestType=filter&sort=rec',
# 'http://in.exclusively.com/search?keyword=study+by+janak&categoryId=0',
# 'http://in.exclusively.com/search?keyword=tanko+by+shipra&categoryId=0',
# 'http://in.exclusively.com/search?keyword=%09Vandana+Sethi&categoryId=0',
# 'http://in.exclusively.com/search?keyword=Vemanya&categoryId=0',
# 'http://in.exclusively.com/search?keyword=soup&categoryId=0&internalRequestType=filter&q=Brand%3ASOUP%20by%20Sougat%20Paul'
	]



#DO NOT EDIT BELOW THIS
from urllib2 import urlopen,Request
import urllib2
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
import traceback
import re
#execfile('/home/sanchit/glitstreet-project/scraper.py')
scraper_url_exc='http://in.exclusively.com'
scraper_url_voy = 'https://www.voylla.com'

def get_html(url):
	html=""
	request = Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
	try:
		html = urlopen(request,timeout=30).read()
	except socket.timeout:
		print "TIMEOUT: sleeping for 100 secs"
		time.sleep(100)
		try:
			html = urlopen(request,timeout=30).read()
		except:
			print "TIMEOUT"
	except urllib2.URLError:
		print "TIMEOUT (URL ERROR): sleeping for 100 secs"
		time.sleep(100)
		try:
			html = urlopen(request,timeout=30).read()
		except:
			print "TIMEOUT (URL ERROR)"
	except:
		print "Sleeping 5 mins"
		time.sleep(300)
		try:
			html = urlopen(request).read()
		except:
			print "Sleeping 15 mins"
			time.sleep(900)
			try:
				html = urlopen(request).read()
			except:
				print "Sleeping 1 hr"
				time.sleep(3600)
				html = urlopen(request).read()
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
	print designer_url
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
	for u in infinite_urls:
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
		print str(traceback.format_exc().splitlines()[-1])
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
	prod['prod_url'] = prod_url
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
		prod['prod_code'] = soup.select('td.golden_color span:nth-of-type(1)')[0].text.strip().encode('ascii', 'ignore')
	except:
		pass
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
	headers = ['designer name','name','selling price','description','colour','material','dimensions','image_urls','prod_url','prod_code']
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

def get_price_amaz(asin):
	url = 'http://www.amazon.in/gp/offer-listing/'+asin
	html = get_html(url)
	soup= BeautifulSoup(html,'lxml')
	try:
		price = soup.select('span.a-size-large > span')[0].text.strip().encode('ascii', 'ignore')
	except:
		price = ''
	return price

def get_product_data_amaz(prod_url,fetch_price=False,asin='None',des_name='None',ssp2=''):
	html = get_html(prod_url)
	soup= BeautifulSoup(html,'lxml')
	prod={'asin':asin,'designer name':des_name, 'selling price 2':ssp2.encode('ascii', 'ignore')}
	try:
		if asin =='None':
			if str(prod_url.split('?')[0].split('/')[-1]).startswith('ref='):
				prod['asin'] = prod_url.split('?')[0].split('/')[-2]
			else:
				prod['asin'] = prod_url.split('?')[0].split('/')[-1]
	except:
		pass
	try:
		prod['name'] = soup.select("h1.a-size-large span.a-size-large")[0].text.strip().encode('ascii', 'ignore')
	except:
		prod['name']= ' '
	try:
		prod['selling price'] = soup.select('td.a-span12 span.a-size-medium')[0].text[1:].strip().encode('ascii', 'ignore')
	except:
		prod['selling price']= ' '
	if fetch_price and not str(prod['selling price 2']).strip() and not str(prod['selling price']).strip():
		prod['selling price 2'] = get_price_amaz(str(prod['asin']))
	#Choose greater of 2
	try:
		prod_sp= prod['selling price'].strip()
		prod_sp2 = prod['selling price 2'].strip()
		prod_prices = filter(None,prod_sp.split('-')+[prod_sp2])
		if prod_prices:
			for i in xrange(0,len(prod_prices)):
				prod_prices[i]=float(re.sub('[^0-9.]+', '',prod_prices[i]).strip('. '))
			prod['selling price'] = str(max(prod_prices))
		elif not prod_sp and prod_sp2:
			prod['selling price'] = prod_sp2
	except:
		if not prod['selling price'].strip() and prod['selling price 2']:
			prod['selling price'] = prod['selling price 2']
	try:
		prod['description']= ''
		for para in soup.select('div.a-row div.a-section p'):
			prod['description'] += para.text.strip().encode('ascii', 'ignore')
	except:
		prod['description']= ' '
	prod['colour'] = ''
	prod['dimensions']=''
	prod_att_keys = soup.select('th.a-span5')
	prod_att_values = soup.select('td.a-span7')
	att_dict={}
	for i,kv in enumerate(prod_att_keys):
		k=kv.text.strip().lower()
		if k=='colour' or k == 'color':
			prod['colour'] += prod_att_values[i].text.strip() +','
		elif k=='material':
			prod['material'] = prod_att_values[i].text.strip()
		elif k=='item width' or k=='item length' or k=='item weight' or k=='weight':
			prod['dimensions'] += str(kv.text.strip()) + ' : '+prod_att_values[i].text.strip()+', '
		elif k=='brand' and des_name=='None':
			prod['designer name']=str(prod_att_values[i].text.strip())
	try:
		first_detail = soup.select('td.bucket div.content > ul > li:nth-of-type(1)')[0].text
		if 'dimension' in first_detail.lower() or 'weight' in first_detail.lower():
			prod['dimensions'] += first_detail.split(':',1)[0].strip() +' : '+first_detail.split(':',1)[1].strip()
	except:
		pass
	prod['dimensions'] = prod['dimensions'].replace('\n','').strip()
	prod["sizes"] = ""
	try:
		prod["sizes"] += str(soup.select('span.selection')[0].text).strip().replace('\n','')+ ", "
	except:
		pass
	try:
		prod["sizes"] += ','.join(str(soup.select('span.twister-dropdown-highlight select.a-native-dropdown')[0].text).replace('\n','').strip().replace('Select','').split())
	except:
		pass
	prod['other_desc']=""
	for s in soup.select('div.a-fixed-right-grid-col span.a-list-item'):
		prod['other_desc'] += s.text.strip() +'| '
	prod['other_desc'] = prod['other_desc'].encode('ascii', 'ignore')
	prod['ipn']=''
	for s in soup.select('div.content > ul > li'):
		if 'part num' in s.text.lower():
			prod['ipn'] = s.text.strip().encode('ascii', 'ignore')
	# Hi Res IMAGES
	prod['image_urls']=[]
	all_scripts  = soup.find_all("script", {"src":False})
	image_script = None
	for s in all_scripts:
		if 'maintainHeight' in s.text:
			image_script = s
	if image_script:
		var_index = image_script.text.strip().index('var data')
		text_value = image_script.text.strip()[var_index:].split(';')[0]
		json_value = '{%s}' % (text_value.split('{', 1)[1].rsplit('}', 1)[0],)
		value = json.loads(json_value.replace("'",'"'))
		for i in value['colorImages']['initial']:
			if i['hiRes']:
				prod['image_urls'].append(i['hiRes'])
			elif i['large']:
				prod['image_urls'].append(i['large'])
			elif i['main'].keys():
				try:
					im_url = i['main'].keys()[0]
				except:
					continue
				try:
					prod['image_urls'].append(im_url[:im_url.index('._')]+im_url[im_url.index('_.')+1:])
				except:
					prod['image_urls'].append(im_url)
	return prod

def get_designer_data_amaz(designer_url):
	print "---------------FETCHING DESIGNER PRODUCT URLS----------------------"
	search_results=[]
	api_url = designer_url +'&dataVersion=v0.2&cid=08e6b9c8bdfc91895ce634a035f3d00febd36433&format=json'
	html = get_html(api_url)
	html_json=json.loads(html)
	num_pages = int(html_json['pagination']['numPages'])
	for section in html_json['results']['sections']:
		for product in section['items']:
			sr={}
			sr['name'] = product['title']
			sr['asin'] = product['asin']
			sr['url'] = 'http://www.amazon.in' + product['link']['url']
			sr['brand_name']=product.get('brandName','None')
			try:
				sr['ssp2'] = product['prices']['usedAndNewOffers']['price']
			except:
				sr['ssp2'] = ""
			search_results.append(sr)
	for i in xrange(1,12):
		url = api_url +'&page='+str(i)
		print url
		time.sleep(5)
		html = get_html(url)
		html_json=json.loads(html)
		try:
			for section in html_json['results']['sections']:
				for product in section['items']:
					sr={}
					sr['name'] = product['title']
					sr['asin'] = product['asin']
					sr['url'] = 'http://www.amazon.in' + product['link']['url']
					sr['brand_name']=product.get('brandName','None')
					try:
						sr['ssp2'] = product['prices']['usedAndNewOffers']['price']
					except:
						sr['ssp2'] = ""
					search_results.append(sr)
		except:
			print 'ERROR!!!'
			print str(traceback.format_exc().splitlines()[-1])
	print len(search_results)
	print '----------------DONE---------------------'
	return search_results

def main_amaz():
	designer_urls = designer_urls_amazon
	headers = ['asin','designer name','name','selling price','description','colour','material','dimensions','image_urls','sizes','other_desc','selling price 2','ipn']
	for designer_url in designer_urls.keys():
		designer_page_data = get_designer_data_amaz(designer_url)
		for sr in designer_page_data:
			time.sleep(2)
			print sr['url']
			prod = get_product_data_amaz(sr['url'],sr['asin'],sr['brand_name'],ssp2=sr['ssp2'])
			csv_exporter('amazon-'+designer_urls[designer_url],prod,headers)

def update_amaz(file_name):
	headers = ['asin','designer name','name','selling price','description','colour','material','dimensions','image_urls','sizes','other_desc','selling price 2','ipn']
	if file_name.split('.')[-1] !='csv':
		return "please enter a csv file"
	asins = []
	csvfile = open(file_name)
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['asin'].strip() != 'asin':
			asins.append(str(row['asin']))
	csvfile.close()
	for asin in asins:
		url = "http://www.amazon.in/d/"+asin
		print url
		prod = get_product_data_amaz(url,True,asin,'',ssp2='')
		csv_exporter(file_name.split('.')[0]+'-update',prod,headers)

def store_image(url,sitename='default',storename="default-store",productname="default-product",image_count=1):
	r = requests.get(url, stream=True)
	directory = os.getcwd() + '/images/'+sitename+'/'+storename+'/'+productname+'/'
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
				im_url = str(im_url.strip()).replace("u'","").replace("'","").replace('"','').strip()
				if im_url != 'None':
					if "images.voylla.com" in im_url:
						im_url= im_url.replace("/large/","/original/")
					print im_url
					store_image(im_url,file_name.split('-')[0].split('.')[0],row.get('designer name'),row.get('prod_code'),i)

def get_amaz_desc(file_name):
	if file_name.split('.')[-1] !='csv':
		return "please enter a csv file"
	asins = []
	csvfile = open(file_name)
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['asin'].strip() != 'asin':
			# try:
			asins.append(row)
	csvfile.close()
	dest_name = file_name.split('.',1)[0]+'-temp.'+file_name.split('.',1)[1]
	headers = ['asin','designer name','name','selling price','description','colour','material','dimensions','image_urls','other_desc']
	dest = open(dest_name, 'w')
	writer = csv.writer(dest)
	writer.writerow(headers)
	dest.close()
	for asin in asins:
		try:
			url = "http://www.amazon.in/d/"+asin['asin']
			html = get_html(url)
			soup= BeautifulSoup(html,'lxml')
			other_desc=""
			for s in soup.select('div.a-fixed-right-grid-col ul.a-vertical span.a-list-item'):
				other_desc += s.text.strip()
			asin['other_desc'] = other_desc
			# print other_desc
			a = [asin[k] for k,v in asin.iteritems()]
			print a
			file_exists=False
			if os.path.isfile(dest_name):
				dest = open(dest_name, 'ab')
				file_exists = True
			else:
				dest = open(dest_name, 'wb')
			writer = csv.writer(dest)
			writer.writerow(a)
		except:
			pass
		finally:
			dest.close()
