# -*- coding: utf-8 -*-
import time, datetime, decimal
from lxml import etree
import urllib2
import urllib

'''
Control switches
'''
PARSEHTML = False
CALCULATE = False

'''
Parsers
'''
class HTMLParserEastern( object ):
    def __init__(self, html, encoding='utf-8', **argv ):
        argv.update( {'html':html, 'encoding':encoding })
        self.encoding_ = encoding
        
        self.headers_ = ['superlr', 'superlc', 'ddlr', 'ddlc', 'zdlr', 'zdlc','xdlr', 'xdlc']
        
        resp = html.read()
        self.root_ = etree.HTML(  resp.decode( encoding )  )
    
    def get_headers(self):
        '''
        Get the headers that were searched.
        '''
        return self.headers_
        
    def extract_ts(self ):
        '''
        Extract section of data in first section of the html, 
        indicated by the "<span id=data_superlr>" etc..
        Requires the definition of "headers".
        '''
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
        '''
        Extract historical data from the html page.
        Handles the section indicated by "<table id=dt_1>".
        No headers are required to be definied.
        '''  
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
                            if u'万' in txt: txt = txt.replace(u'万', 'e4')
                            arow += [ txt ]
                    history += [ arow ]
                    print len( arow ),
        print '\n\t total row:', len( history )
        return history
    
    def extract_mkt(self):
        '''
        Extract the name of the market.
        '''
        for mkt in self.root_.xpath('//div[@class="tit"]/text()'):
            if u'资金流向(' in mkt:
                return mkt.strip()
        return None
    
class WebGrabber( object ):
    def __init__(self, url ):
        self.url_ = url
        
    def header(self, reqUrl ):
        req = urllib2.Request( reqUrl )
        req.add_header('content-type', 'application/json')
        req.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36')
        return req
    
    def grab(self, local=True):
        '''
        Connect to the url or local bufferred files, then calling parser.
        local [in]: indicated whether using local buffer files, or directly connect to URL.
        
        TODO:
        use selenium to fetch dynamic contents in URL. Right now, local buffer files is a work around.
        Local buffer files need to be manually saved --- controlled by the global switch: PARSEHTML=False.
        '''
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
        mkt = parser.extract_mkt()
        if len(history):
            print 'selected history date from: %s to %s'%(
                                                      history[-1][0],
                                                      history[0][0])
        if response: response.close()
        
        return ( timeseries, history, parser.get_headers(), mkt, )

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
    '''
    Open URLs and manually save to buffer files.
    This is a workaround. Ultimately, selenium or alike should be used.
    '''
    urls = ['http://data.eastmoney.com/zjlx/',
        'http://data.eastmoney.com/zjlx/zs399006.html',
        'http://data.eastmoney.com/zjlx/zs399001.html',
        'http://data.eastmoney.com/zjlx/zs000001.html',
        'http://data.eastmoney.com/zjlx/zs399005.html']
    browser = webbrowser.get()
    browser.open( urls[0], new=2 )
    for item in urls[1:]:
        browser.open_new_tab( item )


def get_files( root ):
    for afile in os.listdir( root ):
        if os.path.isfile( os.path.join(root, afile )):
            yield afile

def eastern_process_html_files( dirname ):   
    '''
    Parse local buffer files.
    dirname [in]: the local directory, usually looks like: ./20160102/
    '''
    
    with open(os.path.join(dirname, 'ts.csv'), 'w') as outfile:
        cw = outfile 
        market_to_data = {}
        header_not_ready = True
        header = None
        for afile in get_files( dirname ):
            if not afile.endswith('.html'): continue
            fullname = os.path.join( dirname, afile )
            print fullname
            modtime = os.path.getmtime(fullname )
            ts, hs, header, market = WebGrabber( fullname ).grab()
            if market in market_to_data.keys():
                market_to_data[ market ] += [ [datetime.datetime.utcfromtimestamp( modtime )] + ts ]
            else:
                market_to_data[ market ] = [ [datetime.datetime.utcfromtimestamp( modtime )] + ts ]
                
        for market, data in market_to_data.items():
            if header_not_ready: 
                cw.write( ','.join( ['market', 'timestamp' ] + header )+'\n' )
                header_not_ready = False
            for a in data: 
                if market: cw.write( market.encode('utf-8')+',' )
                else: cw.write( ','.join(['Overall Market'])+',' )
                cw.write( ','.join( [str(s) for s in a] )+'\n' )
    outfile.close()

    markets = set()
    for afile in get_files( dirname ):
        if not afile.endswith('html'): continue
        fullname = os.path.join( dirname, afile)
        print '\n\n', fullname
        modtime = os.path.getmtime( fullname )
        
        eastmoney = WebGrabber( fullname )
        ts, hs, headers, market = eastmoney.grab()
        
        if not market: market = 'Overall Market'
        if market in markets: continue
        else: markets.add( market )
        
        if len(hs)>0:
            ofilename = os.path.join(dirname, "%s.csv"%afile)
            ofile = open( ofilename, 'w')
            ofile.write( 'Market:,%s\n'%market.encode('utf-8') )
            ofile.write( u'Timestamp:, %s\n'%( datetime.datetime.utcfromtimestamp( modtime ) ))
            ofile.write( ',closing,,major,,%s\n'%( ','.join( headers ) ) )
            for row in hs:                    
                ofile.write( ','.join( row ).encode('utf-8') )
                ofile.write('\n')
            ofile.close()
            print 'file written: %s'%( ofilename ) 
            
            ''' debug 
            with open( ofilename, 'r') as infile:
                reader = csv.reader( infile )
                for row in reader:
                    for fd in row:
                        print fd.decode('utf-8'),
                    print ''
            infile.close()
             end '''

import csv
def eastern_calc( dirname ):
    market_data_map = {}
    
    for afile in get_files( dirname ):
        if afile.endswith( '.csv'):
            fullname = os.path.join( dirname, afile )
            
            with open( fullname, 'r') as infile:
                creader = csv.reader( infile )
                market = creader.next()[1]
                timestamp = creader.next()[1] 
                print timestamp, market
                
                creader.next()
                for row in creader:
                    print ', '.join([ s.decode('utf-8') for s in row ] )               
                
                
import webbrowser, os        
if __name__ == '__main__':
    print get_current_ymd()
        
    if CALCULATE:
        eastern_calc( '.\\%s'%get_current_ymd())
    else:
        if not PARSEHTML:
            eastern_view_pages( )
    
        if PARSEHTML:
            url = '.\\%s'%get_current_ymd()
            #url = '.\\20160204'
            if not os.path.exists( url ):
                os.mkdir( url )
            eastern_process_html_files( url )