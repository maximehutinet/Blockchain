#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author Maxime Hutinet

import main
from colortext import ColorText


class Blockchain:
    '''
    Classe representing a blockchain
    '''
    def __init__(self, complexity):
        self.listBlock = []
        self.complexity = complexity
        print(ColorText.OkBlue("######### Blockchain #########\n"))

    def addBlock(self, block):
        '''
        Add a block to the blockchain
        :param block: The block to add
        '''
        localBlock = block
        # Here we modify the attribute hashPreviousBlock of the block we want to
        # add to make it point to the previous block hash
        try:
            localBlock.hashPreviousBlock = self.listBlock[-1].blockHash

        except IndexError:
            pass

        if self.verify()[0]:
            self.listBlock.append(localBlock)
            print(ColorText.OkGreen("[VERIFICATION] - Pass"))
        else:
            print(ColorText.Fail("[VERIFICATION] - The block {} is not correct ! Cannot add the block {}".format(self.verify()[1], localBlock.blockIndex)))

    def verify(self):
        '''
        Make sure that our blockchain is valid
        :return: A tuple with a boolean if it passes the verification and the index of
        the block if it didn't
        '''
        verificationResult = True
        indexBlocError = 0
        for i, block in enumerate(self.listBlock):
            blockData = block.header + block.merkleRoot + block.concatenatedTransactionHash
            if main.HashData(blockData + block.nonce) == block.blockHash:
                continue
            else:
                verificationResult = False
                indexBlocError = i
                break

        return verificationResult, indexBlocError

    def mine(self):
        '''
        Mine the blockchain by forming the block and performing the mining challenge
        in order to add a hash and nonce to the block header
        '''

        # We form the last block on the list
        self.listBlock[-1].formBlock()
        # We create the hash of the last block on the list
        self.listBlock[-1].createHashBlock(self.complexity)

    def displayBlockchain(self):
        '''
        Display the different blocks in the blockchain
        '''
        for block in self.listBlock:
            print(block)
            print("    ^     ")
            print("    |     ")
