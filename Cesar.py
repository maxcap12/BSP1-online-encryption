def encrypt_cesar(key: str, text: str):
    encrypted = ""
    for char in text:
        if not char.isalpha():
            encrypted += char
        else:
            asInt = ord(char) - ord('a') + int(key) % 26
            encrypted += chr(asInt % 26 + ord('a'))

    return encrypted


def decrypt_cesar(key: str, text: str):
    decrypted = ""
    for char in text:
        if not char.isalpha():
            decrypted += char
        else:
            asInt = ord(char) - ord('a') - int(key) % 26
            decrypted += chr(asInt % 26 + ord('a'))

    return decrypted
