"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
from time import sleep

from tema import constants


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.id_ = kwargs['name']
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        # Loop through carts
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            # Loop through operations for every cart
            for operation in cart:
                if operation[constants.TYPE] == constants.ADD_OPERATION:
                    # Loop until the consumer added every product
                    quantity_to_be_added = operation[constants.QUANTITY]
                    products_added = 0
                    while products_added < quantity_to_be_added:
                        operation_success = self.marketplace.add_to_cart\
                            (cart_id, operation[constants.PRODUCT])
                        # If adding to cart fails, consumer should wait and try again
                        if operation_success is False:
                            sleep(self.retry_wait_time)
                        else:
                            # Count the number of successfully added products
                            products_added += 1
                elif operation[constants.TYPE] == constants.REMOVE_OPERATION:
                    quantity_to_be_removed = operation[constants.QUANTITY]
                    products_removed = 0
                    while products_removed < quantity_to_be_removed:
                        self.marketplace.remove_from_cart(cart_id, operation[constants.PRODUCT])
                        # Count the number of removed products
                        products_removed += 1

            # Place the order after filling the carts
            self.marketplace.place_order(cart_id)
