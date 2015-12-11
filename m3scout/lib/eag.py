from m3scout.lib.basesite import BaseSite

class EAG(BaseSite):
    
    SITES_URL = 'http://enthusiastauto.com/e46_m3.html'
    CLS_NAME = 'EAG'
        
    def get_details(self, post,):
        doc = self.getParsed(post)
        info = []
        for detail in doc.find('div', {'class': 'indv_right'}).find_all('div'):
            info.append(detail.text)
        data = {
            'info': ' '.join(info),
            'body': doc.find('div', {'id': 'lblInfo'}).text
        }
        return data
    
        
    def get_all(self, ):
        return_list = []
        doc = self.getParsed(self.SITES_URL)
        for item in doc.find_all('div', {'class': 'vehicle_srch'}):
            link = item.find('a', {'class': 'action'}).get('href')
            listing = {
                'id': link.split('/')[-1].replace('.html', ''),
                'link': link,
                'price': item.find('h2').text.replace('PRICE: ', ''),
                'short_text': item.find('a', {'class': 'action'}).text,
            }
            return_list.append(listing)
        return return_list
