# -*- coding: utf-8 -*-

import sys, json, logging
from six import string_types
import lxml.etree as ET

class AlbopopJsonConverter():

    def __init__( self , xsl = "xml2json-style1.xsl" ):

        if xsl:
            self.xslt = ET.parse(xsl)

    def xml2json_raw( self , xml = None , xsl = "" ):

        if xsl:
            xslt = ET.parse(xsl)
        else:
            xslt = self.xslt

        if isinstance( xml , string_types ):
            dom = ET.fromstring(xml)
        else:
            dom = ET.parse(xml)

        transform = ET.XSLT(xslt)

        return json.loads(transform(dom).__str__().replace('""','"'))

    def xml2json( self , xml = None , xsl = "" ):

        raw = self.xml2json_raw(xml,xsl)
        return self.normalize(raw)

    def remove_dollar( self , obj = {} ):

        if not obj or not isinstance(obj,dict):
            return obj

        for k,v in obj.items():
            if isinstance(v,dict) and not set(v.keys()) - set(['$']):
                obj[k] = v['$']

        return obj

    def remove_dollars( self , arr = [] ):

        if not arr:
            return arr

        for i,v in enumerate(arr):
            if isinstance(v,dict):
                arr[i] = self.remove_dollar(v)

        return arr

    def move_domains( self , arr = [] , prefix = "" ):

        if not arr:
            return arr

        obj = {}
        for item in arr:
            if isinstance(item,dict) and not set(item.keys()) - set(['@domain','$']):
                obj[item['@domain'].split('#')[1].replace(prefix,"")] = item['$']

        return obj

    def remove_at( self , obj = {} ):

        if not obj:
            return obj

        for k in obj:
            if k.startswith('@'):
                obj[k[1:]] = obj[k]
                del obj[k]

        return obj

    def normalize( self , raw = {} ):

        if not raw:
            return raw

        raw['rss'] = self.remove_at(raw['rss'])
        raw['rss']['channel'] = self.remove_dollar(raw['rss']['channel'])
        raw['rss']['channel']['item'] = self.remove_dollars(raw['rss']['channel']['item'])
        raw['rss']['channel'].update(self.move_domains(raw['rss']['channel']['category'],'channel-category-'))
        del raw['rss']['channel']['category']
        for index,item in enumerate(raw['rss']['channel']['item']):
            raw['rss']['channel']['item'][index].update(self.move_domains(item['category'],'item-category-'))
            del raw['rss']['channel']['item'][index]['category']

        return raw

if __name__ == "__main__":
    ajc = AlbopopJsonConverter()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fi:
            with open(sys.argv[1]+".json",'w') as fo:
                json.dump(ajc.xml2json(fi),fo)

