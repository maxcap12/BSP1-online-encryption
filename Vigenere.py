def encrypt_vigenere(key: str, text: str) -> str:
    encrypted_text = ""
    key_index = 0
    key_ord = [ord(val.lower()) - ord('a') for val in key]

    for char in text:
        if not char.isalpha():
            encrypted_text += char
        else:
            if char.isupper():
                asInt = ord(char) - ord('A') + key_ord[key_index % len(key)]
                encrypted_text += chr(asInt % 26 + ord('A'))
            else:
                asInt = ord(char) - ord('a') + key_ord[key_index % len(key)]
                encrypted_text += chr(asInt % 26 + ord('a'))

            key_index += 1

    return encrypted_text


def decrypt_vigenere(key: str, text: str) -> str:
    decrypt_text = ""
    key_index = 0
    key_ord = [ord(val.lower()) - ord('a') for val in key]

    for char in text:
        if not char.isalpha():
            decrypt_text += char
        else:
            if char.isupper():
                asInt = ord(char) - ord('A') - key_ord[key_index % len(key)]
                decrypt_text += chr(asInt % 26 + ord('A'))
            else:
                asInt = ord(char) - ord('a') - key_ord[key_index % len(key)]
                decrypt_text += chr(asInt % 26 + ord('a'))

            key_index += 1

    return decrypt_text
