#!/bin/bash/python3
# This script can find the file Hash[md5, sha1, sha256] value.
import hashlib              # Import the Hashlib library

def hash_find(get_list):    # Define a function
    
    for file in get_list:              # For Loop it's  find the element of a list
        with open(file, "rb") as f:    # Open every element with read + binary mode
            data = f.read()            # It's read the open file
            hash_md5 = hashlib.md5(data).hexdigest()        # Collecting the md5 hash value.
            hash_sha1 = hashlib.sha1(data).hexdigest()      # Collecting the sha1 hash value.
            hash_sha256 = hashlib.sha256(data).hexdigest()  # Collecting the sha256 hash value.

        print("\nFile Path is\t\t:-:\t", file)              # Print the file path
        print("MD5 Hash value\t\t:-:\t", hash_md5)          # Print the md5 hash value.
        print("SHA1 Hash value\t\t:-:\t", hash_sha1)        # Print the sha1 hash value.
        print("SHA256 Hash value\t:-:\t", hash_sha256)      # Print the sha256 hash value.

file_list = ["C:\\Users\\MN\\Desktop\\Ethical_hacker.jpg", "C:\\Users\\MN\\Desktop\\Windows_7_x64-2024-03-23-13-39-50.png"]
hash_find(file_list) # Function call & pass the list as value