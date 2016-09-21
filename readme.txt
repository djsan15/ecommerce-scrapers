SETUP:
python get-pip.py
pip install virtualenv
virtualenv .vir
.vir\scripts\activate
pip install beautifulsoup4
pip install requests
pip install pprint
pip install lxml-3.6.4-cp27-cp27m-win_amd64.whl

RUN:
1. Open terminal window in this folder
2. Run "vir\scripts\activate"
3. python
4. execfile('scraper.py')
5. main_exc() #for exclusively
6. main_voy() #for voylla
