from m3scout.lib.basesite import BaseSite

class Craigslist(BaseSite):
    
    SEARCH_Q = None
    SUB_SITE = None
    SEARCH_TERM = '' #< Title must contain this
    SITES_URL = 'https://geo.craigslist.org/iso/us'
    CLS_NAME = 'Craigslist'
    
    def __init__(self, **kwargs):
        self.SEARCH_Q = kwargs.get('search_q')
        self.SUB_SITE = kwargs.get('sub_site')
        self.SEARCH_TERM = kwargs.get('search_term')
        
    def get_details(self, post,):
        doc = self.getParsed(post)
        data = {
            'info': getattr(
                doc.find('p', {'class': 'attrgroup'}), 'text', u''
            ),
            'body': getattr(
                doc.find('section', {'id': 'postingbody'}), 'text', u''
            ),
        }
        return data
    
    def get_locations(self, ):
        ''' Returns a list of all craigslist
        sites in the US
        @return list    List of URLs
        '''
        site_list = []
        doc = self.getParsed(self.SITES_URL)
        items = doc.find('div', id='postingbody')
        for city in items.find_all('a'):
            site_list.append(city.get('href').replace('http', 'https'))
        return site_list
    
    def get_results(self, url, ):
        results = []
        doc = self.getParsed(
            '%s/search/%s?%s' % (url, self.SUB_SITE, self.SEARCH_Q)
        )
        for item in doc.find_all('p', {'class': 'row'}):
            item_info = item.find('a', {'class': 'hdrlnk'})
            item_text = item_info.text
            # The price may be unlisted
            item_price = getattr(
                item.find('span', {'class': 'price'}), 'text', 'N/A'
            )
            item_url = item_info.get('href')
            if 'http' not in item_url:
                item_url = '%s/%s' % (url, item_url)
            if self.SEARCH_TERM.lower() in item_text.lower():
                listing = {
                    'id': item.get('data-pid'),
                    'link': item_url,
                    'short_text': item_text,
                    'price': item_price
                }
                results.append(listing)
        return results
        
    def get_all(self, ):
        return_list = []
        for site in self.get_locations():
            for item in self.get_results(site):
                return_list.append(item)
        return return_list
    
    def get_all_detailed(self, ):
        return_list = []
        for site in self.get_locations():
            res = self.get_results(site)
            for listing in res:
                print listing
                data = self.get_details(listing['link'])
                return_list.append(
                    dict(data.items() + listing.items())
                )
        return return_list
