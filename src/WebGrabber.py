# -*- coding: utf-8 -*-
import time, datetime, decimal
from lxml import etree
import urllib2
import urllib

PARSEHTML = True

class HTMLParserEastern( object ):
    def __init__(self, html, encoding='utf-8', **argv ):
        argv.update( {'html':html, 'encoding':encoding })
        self.encoding_ = encoding
        
        self.headers_ = ['superlr', 'superlc', 'ddlr', 'ddlc', 'zdlr', 'zdlc','xdlr', 'xdlc']
        
        resp = html.read()
        self.root_ = etree.HTML(  resp.decode( encoding )  )
    
    def get_headers(self):
        return self.headers_
        
    def extract_ts(self ):
        root = self.root_
        #for td in root.iterfind('.//td')
        #for txt in root.xpath('//td/span/text()'):
        categories = self.headers_
        values = []
        print datetime.datetime.now()
        print 'timeseries: ', 
        for ids in categories:
            rst = root.xpath('//span[@id="data_%s"]/text()'%ids)
            if len(rst)==0: continue
            print '%se8'%( rst[0] ),
            values += [ decimal.Decimal(rst[0]) ]
        print ''
        return values
    
    def extract_hs(self):    
        root = self.root_
        # Grab historical data
        history = []
        print 'history: \n\t fields in a row:', 
        for table in root.findall('.//table[@id="dt_1"]'):
            for tbody in table.findall('.//tbody'):
                for tr in tbody.findall('.//tr'):
                    arow = []
                    for td in tr.findall('.//td'):
                        if td.text: arow += [ td.text.strip() ]
                        for span in td.findall('.//span'):   
                            txt = span.text
                            if u'亿' in txt: txt = txt.replace(u'亿', 'e8') 
                            arow += [ txt ]
                    history += [ arow ]
                    print len( arow ),
        print '\n\t total row:', len( history )
        return history
    
class WebGrabber( object ):
    def __init__(self, url ):
        self.url_ = url
        
    def header(self, reqUrl ):
        req = urllib2.Request( reqUrl )
        req.add_header('content-type', 'application/json')
        req.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36')
        return req
    
    def grab(self, local=True):
        response = None
        if not local:
            header = self.header( self.url_)
            response = urllib2.urlopen( header )
            charset = response.headers.getheader('Content-Type')
            print charset
        else:
            response = open( self.url_ )
        parser = HTMLParserEastern( response, encoding='GBK')
        timeseries = parser.extract_ts( )
        history = parser.extract_hs( )
        if len(history):
            print 'selected history date from: %s to %s'%(
                                                      history[-1][0],
                                                      history[0][0])
        if response: response.close()
        
        return ( timeseries, history, parser.get_headers(), )

''' 
Generic functions
'''
def get_current_ymd():
    #cur = datetime.datetime.now()
    return datetime.date.today().strftime('%Y%m%d')
def get_ymd( adatetime ):
    return adatetime.strftime('%Y%m%d')

''' 
Applications for Eastern .com
'''
def eastern_view_pages(  ):
    urls = ['http://data.eastmoney.com/zjlx/',
        'http://data.eastmoney.com/zjlx/zs399006.html',
        'http://data.eastmoney.com/zjlx/zs399001.html',
        'http://data.eastmoney.com/zjlx/zs000001.html']
    browser = webbrowser.get()
    browser.open( urls[0], new=2 )
    for item in urls[1:]:
        browser.open_new_tab( item )

def eastern_process_html_files( dirname ):   
    def get_files( root ):
        for afile in os.listdir( root ):
            if os.path.isfile( os.path.join(root, afile )):
                yield afile
    
    for afile in get_files( dirname ):
        if not afile.endswith('html'): continue
        fullname = os.path.join( dirname, afile)
        print '\n\n', fullname
        modtime = os.path.getmtime( fullname )
        
        eastmoney = WebGrabber( fullname )
        ts, hs, headers = eastmoney.grab()
        if len(hs)>0:
            ofilename = os.path.join(dirname, "%s.csv"%afile)
            ofile = open( ofilename, 'w')
            ofile.write( 'timestamp: %s,closing,,major,,%s\n'%( datetime.datetime.utcfromtimestamp( modtime ),
                                                        ','.join( headers ) ) )
            for row in hs:                    
                ofile.write( ','.join( row ).encode('GBK') )
                ofile.write('\n')
            ofile.close()
            print 'file written: %s'%( ofilename ) 
                
import webbrowser, os        
if __name__ == '__main__':
    print get_current_ymd()            
                
    if not PARSEHTML:
        eastern_view_pages( )

    if PARSEHTML:
        url = '.\\%s'%get_current_ymd()
        if not os.path.exists( url ):
            os.mkdir( url )
        eastern_process_html_files( url )
        
        