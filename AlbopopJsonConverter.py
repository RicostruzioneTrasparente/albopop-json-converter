# -*- coding: utf-8 -*-

import sys, json, re, logging
from six import string_types
import lxml.etree as ET
if __name__ == '__main__':
    from AlbopopJsonValidator import AlbopopJsonValidator
else:
    from .AlbopopJsonValidator import AlbopopJsonValidator
import pkg_resources

class AlbopopJsonConverter():

    def __init__( self , xsl = "xml2json-style1.xsl" ):

        if xsl:
            self.xslt = ET.parse(pkg_resources.resource_filename(__name__,xsl))

    def xml2json_raw( self , xml = None , xsl = "" ):

        if xsl:
            xslt = ET.parse(xsl)
        else:
            xslt = self.xslt

        if isinstance( xml , string_types ):
            dom = ET.fromstring(xml)
        else:
            dom = ET.parse(xml)

        for d in dom.iter():
            if d.text:
                d.text = d.text.replace('"','&quote;').replace('\\','&#92;')

        transform = ET.XSLT(xslt)

        return json.loads(transform(dom).__str__())

    def xml2json( self , xml = None , xsl = "" ):

        raw = self.xml2json_raw(xml,xsl)
        return self.normalize(raw)

    def get_items( self , channel = {} ):

        ajv = AlbopopJsonValidator()

        if not ajv.validate(channel):
            logging.error("JSON is not valid against %s" % ajv.schema_file)
            for error in ajv.errors:
                logging.warning("- %s" % error.message)
            return []

        if not channel or not isinstance(channel,dict):
            return channel

        items = []
        for item in channel['rss']['channel']['item']:

            new_channel = {
                "title": channel['rss']['channel']['title'],
                "link": channel['rss']['channel']['link'],
                "description": channel['rss']['channel']['description'],
                "language": channel['rss']['channel']['language'],
                "pubDate": channel['rss']['channel']['pubDate'],
                "webMaster": channel['rss']['channel']['webMaster'],
                "docs": channel['rss']['channel']['docs'],
                "uid": channel['rss']['channel'].get('uid'),
                "type": channel['rss']['channel']['type'],
                "name": channel['rss']['channel']['name']
            }

            new_item = {
                "title": item['title'],
                "link": item['link'],
                "description": item['description'],
                "pubDate": item['pubDate'],
                "guid": item['guid'],
                "country": item.get( 'country' , channel.get('country') ),
                "region": item.get( 'region' , channel.get('region') ),
                "province": item.get( 'province' , channel.get('province') ),
                "municipality": item.get( 'municipality' , channel.get('municipality') ),
                "latitude": item.get('latitude'),
                "longitude": item.get('longitude'),
                "uid": item['uid'],
                "type": item.get('type'),
                "pubStart": item.get('pubStart'),
                "pubEnd": item.get('pubEnd'),
                "relStart": item.get('relStart'),
                "exeStart": item.get('exeStart'),
                "chapter": item.get('chapter'),
                "unit": item.get('unit'),
                "amount": item.get('amount'),
                "currency": item.get('currency'),
                "annotation": item.get('annotation'),
                "channel": {
                    k: new_channel[k]
                    for k in new_channel
                    if new_channel[k] is not None
                }
            }

            new_item['location'] = [
                new_item['longitude'],
                new_item['latitude']
            ] if new_item['longitude'] and new_item['latitude'] else None

            items.append({
                k: new_item[k]
                for k in new_item
                if new_item[k] is not None
            })

        return items

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
                obj[item['@domain'].split('#')[1].replace(prefix,"")] = item.get('$','')

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

        if 'item' in raw['rss']['channel']:
            if isinstance(raw['rss']['channel']['item'],dict):
                raw['rss']['channel']['item'] = [raw['rss']['channel']['item']]
        else:
            raw['rss']['channel']['item'] = []

        raw['rss']['channel']['item'] = self.remove_dollars(raw['rss']['channel']['item'])
        raw['rss']['channel'].update(self.move_domains(raw['rss']['channel']['category'],'channel-category-'))
        del raw['rss']['channel']['category']

        for index,item in enumerate(raw['rss']['channel']['item']):

            if 'enclosure' in item:
                if isinstance(item['enclosure'],dict):
                    item['enclosure'] = [self.remove_at(item['enclosure'])]
            else:
                item['enclosure'] = []

            raw['rss']['channel']['item'][index].update(self.move_domains(item['category'],'item-category-'))
            del raw['rss']['channel']['item'][index]['category']

            for k,v in item.items():
                if isinstance( v , string_types ):
                    item[k] = re.sub( r' {2,}' , r' ' , v.strip() )

        return raw

if __name__ == "__main__":
    ajc = AlbopopJsonConverter()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fi:
            result = ajc.xml2json(fi)
            with open(sys.argv[1]+".json",'w') as fo:
                json.dump(result,fo)

