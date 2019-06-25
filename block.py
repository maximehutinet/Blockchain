#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author Maxime Hutinet


from main import *


class Block:
    '''
    Class representing a block
    '''
    def __init__(self, blockIndex, miningDate, listTransaction):
        self.header = None
        self.blockIndex = str(blockIndex)
        self.miningDate = str(miningDate)
        self.hashPreviousBlock = ""
        self.nonce = ""
        self.blockHash = ""
        self.merkleRoot = None
        self.listTransaction = listTransaction
        self.listHashTransaction = []
        self.concatenatedTransactionHash = ""

    def addNonce(self, nonce):
        '''
        Add a nonce to the block.
        :param nonce: Nonce matching the hash
        '''
        self.nonce = nonce

    def addBlockHash(self, blockhash):
        '''
        Add a hash to the block
        :param blockhash: Hash of the block matching the complexity required
        '''
        self.blockHash = blockhash

    def createHashTransactions(self):
        '''
        Loop through the transaction and hash them.
        '''
        self.listHashTransaction = [transaction.id for transaction in self.listTransaction]

    def processMerkleRoot(self):
        '''
        Process the Merkle tree of the different transaction and add the root to the block.
        '''
        self.merkleRoot = ProcessMerkleTree(self.listHashTransaction)[0]

    def createHeader(self):
        '''
        Concatenate all the information of the header and add it to the block.
        '''
        self.header = self.blockIndex + self.hashPreviousBlock + self.miningDate

    def concatenateHashTransaction(self):
        '''
        Concatenate the transaction hash and add it to the block.
        '''
        for hash in self.listHashTransaction:
            self.concatenatedTransactionHash += hash

    def formBlock(self):
        '''
        Perfom all the task necessary to create the block header.
        '''
        self.createHashTransactions()
        self.concatenateHashTransaction()
        self.processMerkleRoot()
        self.createHeader()

    def createHashBlock(self, complexity):
        '''
        Perform the hash of the block according to a certain complexity and add it
        to the block.
        :param complexity: complexity required to mine
        :return:
        '''
        blockData = self.header + self.merkleRoot + self.concatenatedTransactionHash
        _, self.blockHash, _, self.nonce = FindWordWithZero(blockData, 1, 10000000, complexity)

    def displayTransaction(self):
        '''
        Display the different transaction of a block
        '''
        for transaction in self.listTransaction:
            print(transaction)

    def __repr__(self):
        pound = "\n##########\n"
        return pound + "Block : " + self.blockIndex \
               + "\n- Hash previous block : " + self.hashPreviousBlock \
               + "\n- Mining Date : " + self.miningDate \
               + "\n- Block Hash : " + self.blockHash \
               + "\n- Nonce : " + self.nonce \
               + "\n- Merkle root : " + self.merkleRoot \
               + "\n- Number of transaction : " + str(len(self.listTransaction)) \
               + pound
