# -*- coding: utf-8 -*-
import time, datetime, decimal
from lxml import etree
import urllib2
import urllib

DEVELOPMENT = True

class HTMLParser( object ):
    def __init__(self, html, encoding='utf-8', **argv ):
        argv.update( {'html':html, 'encoding':encoding })
        self.encoding_ = encoding
        
        self.headers_ = ['superlr', 'superlc', 'ddlr', 'ddlc', 'zdlr', 'zdlc','xdlr', 'xdlc']
        
        resp, trunks = '', True
        if not DEVELOPMENT:
            while trunks:
                trunks =  html.read(512)
                resp += trunks
        else: resp = html.read()
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
        timeseries = parser.extract_ts( )
        history = parser.extract_hs( )
        if len(history):
            print 'selected history date from: %s to %s'%(
                                                      history[-1][0],
                                                      history[0][0])
        if response: response.close()
        
        return ( timeseries, history, parser.get_headers(), )

import webbrowser, os
        
if __name__ == '__main__':
    if not DEVELOPMENT:
        url = ['http://data.eastmoney.com/zjlx/',
        'http://data.eastmoney.com/zjlx/zs399006.html',
        'http://data.eastmoney.com/zjlx/zs399001.html',
        'http://data.eastmoney.com/zjlx/zs000001.html']
        browser = webbrowser.get()
        browser.open( url[0], new=2 )
        for item in url[1:]:
            browser.open_new_tab( item )

    if DEVELOPMENT:
        def get_files( root ):
            for file in os.listdir( root ):
                if os.path.isfile( os.path.join(root, file )):
                    yield file
                    
        url = '.\\20160201'
        for file in get_files( url ):
            if not file.endswith('html'): continue
            fullname = os.path.join( url, file)
            print '\n\n', fullname
            eastmoney = WebGrabber( fullname )
            ts, hs, headers = eastmoney.grab()
            if len(hs)>0:
                ofilename = os.path.join(url, "%s.csv"%file)
                ofile = open( ofilename, 'w')
                ofile.write( ',closing,,major,,%s\n'%( ','.join( headers ) ))
                for row in hs:                    
                    ofile.write( ','.join( row ).encode('GBK') )
                    ofile.write('\n')
                ofile.close()
                print 'file written: %s'%( ofilename )