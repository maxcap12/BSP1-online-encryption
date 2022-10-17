from __future__ import annotations
import re
from AES128 import encrypt_aes128, decrypt_aes128
from Cesar import encrypt_cesar, decrypt_cesar


def check_key(method: str, key: str) -> bool | str:
    """
    check whether a given key is valid for a given algorithm
    :param method: the chosen algorithm
    :param key: the chosen key
    :return: True if the key is valid, False otherwise
    """
    # check for the AES128 encryption algorithm
    if method == "aes128":
        # it has to be a key of 128 bits in hexadecimal, so 32 hexadecimal characters
        return re.search("[^0-9a-fA-F]", key) is None and len(key) == 32

    # check for cesar encryption algorithm
    elif method == "cesar":
        # it has to be an integer
        return key.isdigit()

    # algorithm selection error
    else:
        return "algorithm selection error"


def crypto(action: str, method: str, key: str, filename: str, new_name: str, path: str = "") -> None:
    """
    open the file uploaded by the user, call the function to encrypt its content and save it in a new file
    :param action: encrypt or decrypt
    :param method: encryption algorithm selected
    :param key: key
    :param filename: name of the original file
    :param new_name: name of the new file
    :param path: path to the files
    :return: none
    """
    # open the original file
    with open(f"{path}{filename}", 'r') as file:
        # save the file content
        text = file.read()

    # this will contain the content of the new file
    new = ""

    # check if the user wants to encrypt
    if action == "encrypt":
        # check if the user has chosen the aes128 algorithm
        if method == "aes128":
            # call the aes128 encryption function
            new = encrypt_aes128(key, text)

        # check if the user has chosen the cesar algorithm
        elif method == "cesar":
            # call the cesar encryption function
            new = encrypt_cesar(key, text)

    # check if the user wants to decrypt
    elif action == "decrypt":
        # check if the user has chosen the aes128 algorithm
        if method == "aes128":
            # call the aes128 decryption method
            new = decrypt_aes128(key, text)

        # check if the user has chosen the cesar algorithm
        elif method == "cesar":
            # call the cesar decryption function
            new = decrypt_cesar(key, text)

    else:
        # action value error
        pass

    # create the new file
    with open(f"{path}{new_name}", 'w') as encrypted_file:
        encrypted_file.write(new)
