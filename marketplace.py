"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import copy
import threading
from threading import Lock

from tema.ProductWrapper import ProductWrapper


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

        self.carts = {} # {cart_id, list(ProductWrapper)}
        self.producers = {} # {producer_id, [products]}
        self.consumers = {} # {consumer_id, [carts]}
        self.carts_counter = 0

        self.reg_prod_lock = Lock()
        self.cart_lock = Lock()
        self.producers_lock = Lock()


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Get next available index from producers dict
        # Sync with a lock because length of the dict can be change by another prod
        with self.reg_prod_lock:
            prod_id = len(self.producers)
        # Init the list for the caller producer
        self.producers[prod_id] = list()
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
        # Check if producer's list is full
        if len(self.producers[producer_id]) < self.queue_max_size_per_producer:
            # Add the product in the producer's list
            self.producers[producer_id].append(product)
            return True
        else:
            return False


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # Update carts number
        with self.cart_lock:
            cart_id = self.carts_counter
            self.carts_counter += 1

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
        producers_copy = copy.deepcopy(self.producers)
        # Iterate through every producer
        for (producer_id, products) in producers_copy.items():
            # Iterate through every producer's list
            if product in products:
                product_wrapper = ProductWrapper(product, producer_id)
                self.carts[cart_id].append(product_wrapper)
                self.producers[producer_id].remove(product)
                #print(threading.current_thread().name + " bought " + str(product) + " in cart " + str(cart_id))
                return True
            return False



    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for cart_product in self.carts[cart_id]:
            if cart_product.name == product:
                # Find product's producer so that I know where to put it back
                prod_id = cart_product.producer_id
                removed_prod = cart_product
                break;

        self.carts[cart_id].remove(removed_prod)
        #print(threading.current_thread().name + " removed " + str(product)+ " from cart " + str(cart_id))
        self.producers[prod_id].append(product)






    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        #print(threading.current_thread().name + " " + str(len(self.carts)))
        for product in self.carts[cart_id]:
            print(threading.current_thread().name + " bought " + str(product.name))


        cart = [product.name for product in self.carts[cart_id]]
        return cart

