#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author Maxime Hutinet

import hashlib
import random
import time
import matplotlib.pyplot as plt
from block import *
from blockchain import *
from transaction import *
import names
import datetime
from colortext import ColorText


def DisplayResult(initWord, word, hash, timeElapsed, nonce, complexity):
    """
    Display the results of the mining operation of a word
    :param initWord: Init word
    :param word: Word modified to fit the xNumber of zero of complexity
    :param hash: Hash found
    :param timeElapsed: Time elapsed to find the hash matching the complexity
    :param nonce: Random number to add to solve the complexity
    :param complexity: Number of zero we want to get in the hash
    """
    print("Initial word : {}\n"
          "Word changed : {}\n"
          "Nonce : {}\n"
          "Hash : {}\n"
          "Complexity : {}\n"
          "Time elapsed : {}\n".format(initWord, word, nonce, hash, complexity, timeElapsed))


def DisplayGraph(listComplexity, listTimeElapsed):
    """
    Display a graph of the complexity vs time
    :param listComplexity: List of complexity
    :param listTimeElapsed: List of time elapsed
    """
    fig, ax = plt.subplots()
    ax.plot(listComplexity, listTimeElapsed)
    ax.set_title('Complexity vs Time elapsed')
    ax.set_xlabel('Complexity')
    ax.set_ylabel('Seconds')

    plt.show()


def DisplayResultMerkle(listOriginalWords, listHash, finalHash):
    """
    Display the result of the Merkle tree
    :param listOriginalWords: List with the original words
    :param listWords: List with the modified words
    :param listHash: List of hash
    :param finalHash: Final hash
    """
    print(
        ColorText.OkBlue("######### Merkle Tree #########\n\n") +
        ColorText.OkBlue("Original word") + " -> " +
        ColorText.OkGreen("Hash")
    )
    for i in range(len(listOriginalWords)):
        print(
            ColorText.OkBlue(listOriginalWords[i]) + " -> " +
            ColorText.OkGreen(listHash[i])
        )

    print(ColorText.Fail("\nFinal hash of the root : {}\n").format(finalHash[0]))


def HashData(data):
    """
    Perform the SHA256 of a data
    :param data: Data to hash
    :return: Hash of the data with the SHA256 algorithme
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def GenerateRandomDigit(min, max):
    """
    Generate a random number between a certain range
    :param min: Range min
    :param max: Range max
    :return: Random number between the range
    """
    return str(random.randint(min, max))


def CheckNumberOfZeros(data, complexity):
    """
    Check if a data begins with a certain number of zero matching the complexity
    :param data: Data to check
    :return: True if there are four zeros at the beginning, else False
    """
    data = list(data[:complexity])
    return data.count("0") == complexity


def GetStatTimeVSComplexity(data, minComplexity, maxComplexity):
    """
    Return the time elapsed by complexity for a certain word
    :param data: Data to process
    :param minComplexity: Min complexity (number of zero)
    :param maxComplexity: Max complexity
    :return: Two list : one of the complexity, one with the time
    """
    listTimeElapsed = []
    listComplexity = []

    for i in range(minComplexity, maxComplexity + 1):
        _, _, timeElapsed, _ = FindWordWithZero(data, 1, 10000000, i)
        listComplexity.append(i)
        listTimeElapsed.append(timeElapsed)

    return listComplexity, listTimeElapsed


def FindWordWithZero(data, minRand=1, maxRand=1000000, complexity=1):
    """
    Find a hash respecting the complexity of x amount of zero at the beginning
    :param data: Data to process
    :param minRand: lower bound
    :param maxRand: hight bound
    :param complexity:
    :return: Tuple with the word, matching hash with four zeros and time elapsed
    """
    start_time = time.time()

    newData = data
    hashData = HashData(data)
    randomNonce = 0

    while CheckNumberOfZeros(hashData, complexity) is False:
        randomNonce = GenerateRandomDigit(minRand, maxRand)
        newData = data + randomNonce
        hashData = HashData(newData)

    return newData, hashData, time.time() - start_time, randomNonce


def ProcessMerkleTree(listData):
    """
    Create a MerkleTree based on a list of data and return its root
    :param listData: List with the different data to hash
    :return: List with the final hash
    """
    newList = listData
    lengthList = len(listData)

    # If there is only one element left in the list we exit
    if lengthList is 1:
        return newList

    # If the list in odd, we double the last item
    elif lengthList % 2 is 1:
        newList.append(listData[-1])

    listHash = []

    for i in range(0, lengthList, 2):
        listHash.append(HashData(newList[i] + newList[i + 1]))

    return ProcessMerkleTree(listHash)


def CreateRandomTransactions(numberOfTransaction):
    '''
    Generation a list of random transaction
    :param numberOfTransaction: Number of transaction to generate
    :return: a list of transaction
    '''
    return [Transaction(names.get_first_name(), names.get_first_name(), random.randint(1, 1000000)) for _ in range(numberOfTransaction)]


if __name__ == '__main__':

    '''
    Analysis of the time elapsed to perform the mining on the word blockchain
    '''

    listComplexity, listTimeElapsed = GetStatTimeVSComplexity("blockchain", 1, 5)

    DisplayGraph(listComplexity, listTimeElapsed)

    '''
    Creation of a blockchain
    '''

    NB_BLOCK = 3
    NB_TRANSACTION = 4
    COMPLEXITY = 3

    # Creation of a random list of transaction
    listTransaction = [CreateRandomTransactions(NB_TRANSACTION) for _ in range(NB_BLOCK)]

    blockchain = Blockchain(COMPLEXITY)

    for i in range(NB_BLOCK):
        blockchain.addBlock(Block(i, datetime.datetime.now(), listTransaction[i]))
        blockchain.mine()

    # Here we modifier the hash of the block 1 for fun
    blockchain.listBlock[1].addBlockHash("orsgb22342")

    blockchain.addBlock(Block(3, datetime.datetime.now(), listTransaction[0]))
    blockchain.mine()
    blockchain.displayBlockchain()
