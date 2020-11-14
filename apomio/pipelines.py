# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from apomio.model import Offer, db_connect, create_table

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ApomioPipeline:
#     def process_item(self, item, spider):
#         return item

class ApomioPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        offer = Offer()
        item.setdefault('reviews', 0)
        item.setdefault('payment', "NA")
        item.setdefault('delivery', "NA")
        offer.pzn = item["pzn"]
        offer.product = item["product"]
        offer.provider = item["provider"]
        offer.rate = item["rate"]
        offer.reviews = item["reviews"]
        offer.payment = item["payment"]
        offer.delivery = item["delivery"]
        offer.price = item["price"]
        offer.total_price = item["total_price"]

        try:
            session.add(offer)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


# Deal with duplicates: update the corresponding information
class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        # logging.info("****DuplicatesPipeline: database connected****")

    def process_item(self, item, spider):
        session = self.Session()
        exist_offer = session.query(Offer).filter_by(pzn=item["pzn"], provider=item["provider"]).first()
        if exist_offer is not None:  # the current offer exists
            # session.close()
            try:
                # session.add(offer)
                item.setdefault('reviews', 0)
                item.setdefault('payment', "NA")
                item.setdefault('delivery', "NA")
                session.query(Offer).filter_by(pzn=item["pzn"], provider=item["provider"]).update(
                    {"rate": item["rate"],
                     "reviews": item["reviews"],
                     "payment": item["payment"],
                     "delivery": item["delivery"],
                     "price": item["price"],
                     "total_price": item["total_price"]}, synchronize_session=False)
                session.commit()
                raise DropItem("Duplicate item found: %s, updated." % item["pzn"])
            except:
                session.rollback()
                raise

            finally:
                session.close()

            # return item
        else:
            return item
            session.close()
