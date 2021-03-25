"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

from tema import Constants


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

        self.id = kwargs['name']
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):

        # Loop through carts
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            # Loop through operations for every cart
            for operation in cart:
                if operation[Constants.TYPE] == Constants.ADD_OPERATION:
                    # Loop until add_to_cart succeeds
                    while True:
                        operation_success = self.marketplace.add_to_cart(cart_id, operation[Constants.PRODUCT])
                        # If adding to cart fails, consumer should wait
                        if operation_success is False:
                            sleep(self.retry_wait_time)
                        else:
                            break;
                elif operation[Constants.TYPE] == Constants.REMOVE_OPERATION:
                    self.marketplace.remove_from_cart(cart_id, operation[Constants.PRODUCT])

        # Place the order after filling the carts
        self.marketplace.place_order(cart_id)