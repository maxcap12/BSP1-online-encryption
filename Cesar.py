def encrypt_cesar(key: str, text: str) -> str:
    """
    encrypt a text using the cesar algorithm
    :param key: key used
    :param text: text to encrypt
    :return: text encrypted
    """
    # it will contain the encrypted text
    encrypted = ""

    for char in text:
        # if the character is not a letter it's not modified
        if not char.isalpha():
            encrypted += char
        else:
            if char.isupper():
                # encrypt letters with the key
                asInt = ord(char) - ord('A') + int(key) % 26
                encrypted += chr(asInt % 26 + ord('A'))
            else:
                # encrypt letters with the key
                asInt = ord(char) - ord('a') + int(key) % 26
                encrypted += chr(asInt % 26 + ord('a'))

    # return the encrypted text
    return encrypted


def decrypt_cesar(key: str, text: str):
    """
    decrypt a text using the cesar algorithm
    :param key: key used
    :param text: text to decrypt
    :return: text decrypted
    """
    # it will contain the decrypted text
    decrypted = ""

    for char in text:
        # if the character is not a letter it's not modified
        if not char.isalpha():
            decrypted += char
        else:
            if char.isupper():
                # encrypt letters with the key
                asInt = ord(char) - ord('A') - int(key) % 26
                decrypted += chr(asInt % 26 + ord('A'))
            else:
                # decrypt the letter with the key
                asInt = ord(char) - ord('a') - int(key) % 26
                decrypted += chr(asInt % 26 + ord('a'))

    # return the decrypted text
    return decrypted
