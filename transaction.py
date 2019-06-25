#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author Maxime Hutinet


import main


class Transaction:

    def __init__(self, seller, buyer, amount):
        self.seller = seller
        self.buyer = buyer
        self.amount = amount
        self.id = main.HashData(self.seller + self.buyer + str(self.amount))

    def __repr__(self):
        dash = "\n--------------\n"
        return dash + "Transaction : " + self.id \
               + "\n- Seller : " + self.seller \
               + "\n- Buyer : " + self.buyer \
               + "\n- Amount : " + str(self.amount)
