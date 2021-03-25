"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from queue import Queue
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_max_size_per_producer = queue_size_per_producer

        self.carts = {} # {cart_id, list(products)}
        self.producers = {} # {producer_id, products_queue}
        self.consumers = {} # {consumer_id, [carts]}
        self.carts_counter = 0

        self.reg_prod_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Get next available index from producers dict
        # Sync with a lock because length of the dict can be change by another prod
        with self.reg_prod_lock:
            prod_id = len(self.producers)
        # Init the queue for the caller producer
        self.producers[prod_id] = Queue(maxsize=self.queue_max_size_per_producer)
        return prod_id


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if self.producers[producer_id].qsize() < self.queue_max_size_per_producer:
            print(self.producers[producer_id].qsize())
            self.producers[producer_id].put(product)
            return True
        else:
            return False


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # Update carts number
        self.carts_counter += 1

        cart_id = self.carts_counter

        # Add cart_id into cart dictionary
        self.carts[cart_id] = list()

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        pass

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass
