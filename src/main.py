"""
Enrico Tedeschi @ UiT - Norges Arktiske Universitet, Faculty of Computer Science.
enrico.tedeschi@uit.no

INF 3203 - Advanced Distributed Systems

Assignment 1 - Blockchain Mining Competition

Usage:
        -h                  : display usage information
        -i [b, u]           : display information for blocks or users   #TODO
        -t                  : request N transactions                    #TODO
        -m                  : mine a block                              #TODO
        -v b                : visualize blockchain, saved to vis/blockchain/blockchain.pdf
        -d                  : request DIFFICULTY level
"""
__author__ = "Enrico Tedeschi"
__copyright__ = "Copyright (C) 2023 Enrico Tedeschi"
__license__ = "GNU General Public License."
__version__ = "v1.0"

import sys
import getopt
import random
import requests
import json
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.flask_utils import flask_call
from abstractions.block import Blockchain
from server import BLOCK_PROPOSAL, REQUEST_DIFFICULTY, GET_BLOCKCHAIN, ADDRESS, PORT
from utils.view import visualize_blockchain, visualize_blockchain_terminal

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:tmdv:")
        # print(f'opts : {opts}\nargs : {args}')
        valid_args = False
        for opt, arg in opts:
            if opt == "-h":  # usage
                print(__doc__)
                valid_args = True
                break
            if opt == "-m":  # mine block
                # TODO: IMPLEMENT BLOCK MINING
                response, _, _ = flask_call('POST', BLOCK_PROPOSAL, data=None)
                print(response)
                valid_args = True
            if opt == "-i":
                # INFO
                if arg == "b":
                    # TODO: GET INFO ABOUT BLOCKCHAIN
                    print("To be implemented ...")
                    valid_args = True
                elif arg == "u":
                    # TODO: GET INFO ABOUT USERS
                    print("To be implemented ...")
                    valid_args = True
                else:
                    valid_args = False
            if opt == "-t":
                # TODO: Implement GET_TXS
                print("To be implemented ...")
                valid_args = True
            if opt == "-v":
                if arg == "b":
                    # fetch blockchain from server
                    # get blockchain info
                    _, blockchain, code = flask_call('GET', GET_BLOCKCHAIN)
                    if blockchain:
                        b_chain = Blockchain.load_json(json.dumps(blockchain))
                        # saves the blockchain as pdf in "vis/blockchain/blockchain.pdf"
                        visualize_blockchain(b_chain.block_list, n_blocks=40)
                        visualize_blockchain_terminal(b_chain.block_list, n_blocks=40)
                    valid_args = True
            if opt == "-d":
                response, table, code = flask_call('GET', REQUEST_DIFFICULTY)
                print(response)
                print(table)
                valid_args = True
        if valid_args is False:
            print(__doc__)
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)
    except ValueError as e:
        print(e)
        print(__doc__)
        sys.exit(2)  # exit due to misuse of shell/bash --> check documentation
    except KeyboardInterrupt as e:
        print(e)

def connect_to_server():
    """

    :return:
    """
    url = 'https://' + ADDRESS + ':' + PORT + '/'
    response = requests.get(url, verify=False)
    return response

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main(sys.argv[1:])