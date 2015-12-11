#!/usr/bin/env python
from hashlib import md5
from time import sleep
from m3scout.lib.db.m3scout_db import M3ScoutDB
from m3scout.lib.email import Email
from m3scout.lib.craigslist import Craigslist
from m3scout.lib.eag import EAG
from m3scout.lib.carscom import CarsCom
from m3scout.lib.autotrader import AutoTrader


import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class M3ScoutDaemon(object):
    
    SYSTEMS = []
    
    def __init__(self, ):
        logger.debug("Initiating DBO")
        self.DB = M3ScoutDB()
        self.SYSTEMS = [
            Craigslist(
                search_q='query=M3&autoMinYear=2005&autoMaxYear=2006',
                sub_site='cta',
                search_term='BMW M3'
            ),
            EAG(),
            CarsCom(
                search_q=[
                ('dlId', ''), ('dgId', ''), ('AmbMkNm', 'BMW'),
                ('AmbMdNm', '-+M3'), ('AmbMkId', '20005'),
                ('AmbMdId', '21392'), ('searchSource', 'ADVANCED_SEARCH'),
                ('rd', '100000'), ('zc', '89123'), ('uncpo', '2'),
                ('cpo', ''), ('stkTyp', 'U'), ('bsId', '20203'),
                ('VType', '20203'), ('mkId', '20005'), ('mdId', '21392'),
                ('alMkId', '20005'), ('prMn', '10000'), ('prMx', '30000'),
                ('clrId', ''), ('yrMn', '2005'), ('yrMx', '2006'),
                ('drvTrnId', ''), ('mlgMn', ''), ('mlgMx', ''),
                ('transTypeId', ''), ('kw', ''), ('kwm', 'ANY'),
                ('ldId', ''), ('rpp', '250'), ('slrTypeId', ''),
            ]),
            AutoTrader(
                search_q=[
                    ('endYear', '2006'), ('listingType', 'used'),
                    ('listingTypes', 'used'), ('makeCode1', 'BMW'),
                    ('maxMileage', '100000'), ('maxPrice', '30000'),
                    ('minPrice', '10000'), ('Log', '0'),
                    ('mmt', '%5BBMW%5BM3%5B%5D%5D%5B%5D%5D'),
                    ('modelCode1', 'M3'), ('numRecords', '100'),
                    ('searchRadius', '0'), ('showcaseOwnerId', '1385264'),
                    ('startYear', '2005'), ('vehicleStyleCodes', 'COUPE'),
                ]
            )
        ]
    
    def run(self, ):
        logger.debug("Running script forever")
        while True:
            new_listings = 0
            for sys in self.SYSTEMS:
                logger.info("Scraping %s", sys.CLS_NAME)
                items = sys.get_all()
                logger.info(
                    "Got %s items from %s", len(items), sys.CLS_NAME
                )
                for item in items:
                    # Check to see if this exists
                    # in the DB already
                    exists = self.DB.Items.query.filter(
                        self.DB.Items.id==item['id']
                    ).first()
                    if not exists:
                        logger.debug(
                            "Grabbing details for posting %s", item['link']
                        )
                        details = sys.get_details(item['link'])
                        data = dict(item.items() + details.items())
                        data['status'] = 1
                        data['source'] = sys.CLS_NAME
                        hashable = u'%s%s' % (data['short_text'], data['body'])
                        data['md5sum'] = md5(
                            hashable.encode("utf8", 'ignore')
                        ).hexdigest()
                        logger.debug(
                            "Got MD5 of %s for post id %s",
                            data['md5sum'],
                            data['id']
                        )
                        # Duplicate check
                        is_dupe = self.DB.Items.query.filter(
                            self.DB.Items.md5sum==data['md5sum']
                        ).first()
                        if not is_dupe:
                            new_listings += 1
                            logger.debug(
                                "Adding item with ID %s to DB", data['id']
                            )
                            self.DB.insert(
                                self.DB.Items(**data)
                            )
                        else:
                            logger.debug(
                                "Post %s is a duplicate of %s",
                                data['id'],
                                is_dupe.id
                            )
                        sleep(5) #< Maybe we won't timeout?
                    else:
                        logger.debug(
                            "Post %s already in DB", item['id']
                        )
            if new_listings > 0:
                e = Email()
                e.send_email(
                    'tass2001@gmail.com',
                    'M3Scout - %s new listings found!' % new_listings,
                )
            logger.debug("Sleeping for an hour")
            sleep(3600)
    
if __name__ == '__main__':
    daemon = M3ScoutDaemon()
    daemon.run()