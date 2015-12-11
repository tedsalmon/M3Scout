import re
from m3scout.lib.basesite import BaseSite

class AutoTrader(BaseSite):
    
    SITES_URL = 'http://www.autotrader.com/cars-for-sale/' \
                'Used+Cars/Coupe/BMW/M3/Las+Vegas+NV-89123'
    DETAIL_URL = 'http://www.autotrader.com/cars-for-sale/'\
                 'vehicledetails/overview-tab.xhtml?listingId='
    SEARCH_OPTS = None
    CLS_NAME = 'AutoTrader'
    
    def __init__(self, **kwargs):
        self.SEARCH_OPTS = kwargs.get('search_q')
    
    def get_details(self, post,):
        data = {}
        post_id = re.search("listingId\=(.*?)\&", post)
        if post_id:
            doc = self.getParsed('%s%s' % (self.DETAIL_URL, post_id.group(1)))
            data = {
                'info': "%s %s" % (
                    doc.find('span', {'class': 'heading-mileage'}).text,
                    doc.find(
                        'div', {'class': 'overview-infobar-subsection'}
                    ).text,
                ),
                'body': doc.find('div', {'class': 'overview-comments'}).text
            }
        return data
    
        
    def get_all(self, ):
        return_list = []
        search_opts = ['%s=%s' % (k,v) for k,v in self.SEARCH_OPTS]
        doc = self.getParsed('%s?%s' % (self.SITES_URL, '&'.join(search_opts)))
        for item in doc.find_all('div', {'class': 'listing'}):
            link = item.find('a', {'class': 'vehicle-title'})
            listing = {
                'id': item.get('id'),
                'link': 'http://autotrader.com%s' % link.get('href'),
                'price': item.find(
                    'h4', {'class': 'primary-price'}
                ).text.replace('\n', ''),
                'short_text': link.text.replace('\n', ''),
            }
            return_list.append(listing)
        return return_list
