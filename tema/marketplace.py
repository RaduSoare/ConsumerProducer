"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import copy
import threading
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

        self.carts = {} # {cart_id, [tuple(product, product_publisher)]}
        self.producers = {} # {producer_id, [products]}

        self.cart_lock = Lock()
        self.producers_lock = Lock()


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Get next available index from producers dict
        # Sync with a lock because length of the dict can be change by another prod
        with self.producers_lock:
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
        return False


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # Update carts number
        # Uses a lock because another consumer can try to get a cart at the same time
        with self.cart_lock:
            cart_id = len(self.carts)

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
        with self.producers_lock:
            # Make a copy of the producers so that I can remove from the original
            producers_copy = copy.deepcopy(self.producers)
            # Iterate through every producer
            for (producer_id, products) in producers_copy.items():
                # Check if the product wanted is in the list of the current producer
                if product in products:
                    # Create a "wrapper" for the product to keep in memory
                    # who published the product
                    product_wrapper = (product, producer_id)
                    # Add the product in the cart
                    self.carts[cart_id].append(product_wrapper)
                    # Make the product unavailable for other consumers by
                    # removing it from producer's list
                    self.producers[producer_id].remove(product)
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
        with self.cart_lock:
            # Find the product which needs to be remove in the cart
            for cart_product in self.carts[cart_id]:
                if cart_product[0] == product:
                    # Find product's producer so that I know where to put it back
                    prod_id = cart_product[1]
                    removed_prod = cart_product
                    break
            # Remove the product from the cart
            self.carts[cart_id].remove(removed_prod)
        # Make the product available to other by adding it back in its publisher's list
        self.producers[prod_id].append(product)


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Print every product from the cart
        for product in self.carts[cart_id]:
            print(threading.current_thread().name + " bought " + str(product[0]))

        # Return a list of cart's products
        cart = [product[0] for product in self.carts[cart_id]]
        return cart
