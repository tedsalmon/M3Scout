from m3scout.lib.basesite import BaseSite

class CarsCom(BaseSite):
    
    SITES_URL = 'http://www.cars.com/for-sale/searchresults.action'
    SEARCH_OPTS = None
    CLS_NAME = 'Cars.com'
    
    def __init__(self, **kwargs):
        self.SEARCH_OPTS = kwargs.get('search_q')
        
    def get_details(self, post,):
        doc = self.getParsed(post)
        info = []
        detail_items = doc.find(
            'ul', {'class': 'vehicle-details list'}
        ).find_all('li')
        for detail in detail_items:
            info.append(detail.text)
        body = []
        body_items = doc.find_all('span', {'class': 'seller-notes'})
        for item in body_items:
            body.append(item.text)
        data = {
            'info': ' '.join(info),
            'body': ''.join(body).replace('\n', '').replace('\t', '')
        }
        return data
    
        
    def get_all(self, ):
        return_list = []
        search_opts = ['%s=%s' % (k,v) for k,v in self.SEARCH_OPTS]
        doc = self.getParsed('%s?%s' % (self.SITES_URL, '&'.join(search_opts)))
        
        for item in doc.find_all('div', {'class': 'vehicle'}):
            link = item.find('a', {'class': 'js-vr-vdp-link'})
            listing = {
                'id': item.get('id'),
                'link': 'http://www.cars.com%s' % link.get('href'),
                'price': item.find('span', {'class': 'priceSort'}).text,
                'short_text':'%s %s- %s' % (
                    item.find('span', {'class':'modelYearSort'}).text,
                    item.find('span', {'class': 'mmtSort'}).text,
                    item.find(
                        'p', {'class': 'description'}
                    ).text.replace('\n', '')
                ),
            }
            return_list.append(listing)
        return return_list

