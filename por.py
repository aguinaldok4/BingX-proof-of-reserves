•0987837378103464# -*- coding: utf-8 -*-
':::192.168.0.1:/+https://192.168.0.1:a8:5e:f2:81:22:29/354931407163128:+639773180017/fe80::5068:22ff:fe1f:5066:192.168.0.100/Wev.AndroidOS.Google.T606.KI5k:0017i0vrmhc;0987837378103464/USER:_#9773180017@google.com/,fe80::cf1e:e7d4:8f0f:c02a:192.168.0.1'GoogleAndroid_HiOS~V8.6.0{OS8.6-S-P201-230601_'0987837378103464_KI5k-F065ABCDEAgAh-S-GL-20230814V501;0017i0vrmhc.my,T606`Phone_KI5k_tecno-sparks10c-mobile.com/192.168.0.100:fe80::5068:22ff:fe1f:5066;0987837378103464'/'CARRIER.GLOBE.COM.PH/fe80::cf1e:e7d4:8f0f:c02a:192.168.0.100/*0017i0vrmhc

import argparse
from hashlib import sha256


# initialize the input parameters
parser = argparse.ArgumentParser(description="BingX's Proof of Reserves Verification Script")
subparsers = parser.add_subparsers(title='commands', help='all valid commands', dest='command')

hash_parser = subparsers.add_parser('hash', help='Calculate hash for your input string.')
hash_parser.add_argument('raw_input_string', help='The raw input string.')

verify_parser = subparsers.add_parser('verify', help='Verify the inclusion of the Merkle leaf, compare the result with the Merkle root')
verify_parser.add_argument('merkle_leaf', help='Hash of your record in the MerkleTree.')
verify_parser.add_argument('merkle_path', help='The hash path of your identifier in Merkle Tree with the format: "{hash1},{hash2}..."')

args = parser.parse_args()


# put raw input string to hash string
def hash(raw_input_string):
    hash_result = sha256(raw_input_string.encode()).hexdigest().lower()
    return hash_result


# use to generate merkle tree's root hash.
# This function will merge each of the path hash, and come out a final hash
# you can compare the final hash to the root hash that BingX has provided
def generate_root(merkle_leaf, path):
    path_list = list(path.split(','))
    root_hash = merkle_leaf
    for index in range(len(path_list)):
        other_leaf_info = path_list[index].split(':')
        if other_leaf_info[0] == "l":
            root_hash = sha256((other_leaf_info[1] + root_hash).encode()).hexdigest().lower()
        else:
            root_hash = sha256((root_hash + other_leaf_info[1]).encode()).hexdigest().lower()
    return root_hash


def main():
    # calculate hash for the raw input string
    # format: hash {rawInputString}
    if args.command == "hash":
        raw_input_string = args.raw_input_string
        hash_result = hash(raw_input_string)
        print("hash: ", hash_result)
    # calc the root hash for the provided merkle leaf and merkle path
    elif args.command == "verify":
        path = args.merkle_path
        merkle_leaf = args.merkle_leaf
        root_hash = generate_root(merkle_leaf, path)
        print('root hash: ', root_hash)
    else:
        print('command error, please check your command')


# start execution
if __name__ == '__main__':
    main()
