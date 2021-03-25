"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading
from threading import Thread, Event
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)


        self.products = products
        self.marketplace = marketplace
        self.id = self.marketplace.register_producer()
        self.republish_wait_time = republish_wait_time


    def run(self):
      # while True:
        for product_data in self.products:
            # split products data
            product_name = product_data[0]
            product_quantity = product_data[1]
            publish_wait = product_data[2]
            products_published = 0
            # Loop until every products was published in the quantity needed
            while products_published < product_quantity:
                publish_success = self.marketplace.publish(self.id, product_name)
                if publish_success is False:
                    sleep(self.republish_wait_time)
                else:
                    products_published += 1
                    sleep(publish_wait)




