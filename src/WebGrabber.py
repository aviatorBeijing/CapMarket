import time, datetime, decimal
from lxml import etree
import urllib2
import urllib

DEVELOPMENT = True

class HTMLParser( object ):
    def __init__(self, html, encoding='utf-8', **argv ):
        argv.update( {'html':html, 'encoding':encoding })
        self.encoding_ = encoding
        resp, trunks = '', True
        if not DEVELOPMENT:
            while trunks:
                trunks =  html.read(512)
                resp += trunks
        else: resp = html.read()
        self.root_ = etree.HTML(  resp.decode( encoding )  )
        
    def extract_ts(self ):
        root = self.root_
        #for td in root.iterfind('.//td')
        #for txt in root.xpath('//td/span/text()'):
        categories = ['superlr', 'superlc', 'ddlr', 'ddlc', 'zdlr', 'zdlc','xdlr', 'xdlc']
        values = []
        print datetime.datetime.now()
        for ids in categories:
            rst = root.xpath('//span[@id="data_%s"]/text()'%ids)
            if len(rst)==0: continue
            print ids, rst[0], '1/10 Billion'
            values += [ decimal.Decimal(rst[0]) ]
        print values
    
    def extract_hs(self):    
        root = self.root_
        # Grab historical data
        for table in root.findall('.//table[@id="dt_1"]'):
            for tbody in table.findall('.//tbody'):
                for tr in tbody.findall('.//tr'):
                    for td in tr.findall('.//td'):
                        if td.text: print td.text.strip(),
                        for span in td.findall('.//span'):    
                            print span.text,
                    print ''

    
class WebGrabber( object ):
    def __init__(self, url ):
        self.url_ = url
        
    def header(self, reqUrl ):
        req = urllib2.Request( reqUrl )
        req.add_header('content-type', 'application/json')
        req.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36')
        return req
    
    def grab(self):
        response = None
        if not DEVELOPMENT:
            header = self.header( self.url_)
            response = urllib2.urlopen( header )
            charset = response.headers.getheader('Content-Type')
            print charset
        else:
            response = open( self.url_ )
        parser = HTMLParser( response, encoding='GBK')
        parser.extract_ts( )
        parser.extract_hs( )
        
        if response: response.close()
        
if __name__ == '__main__':
    url = 'http://data.eastmoney.com/zjlx/zs399006.html'

    if DEVELOPMENT:
        url = 'D:\\workspace\\CapMkt\\src\\flow.html'
        #url = 'D:\\workspace\\CapMkt\\src\\tmp\\zs399006.html'
    eastmoney = WebGrabber( url )
    eastmoney.grab() 