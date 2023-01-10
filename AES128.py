# algorithm explanation from : https://etutorials.org/Networking/802.11+security.+wi-fi+protected+access+and+802.11i/Appendixes/Appendix+A.+Overview+of+the+AES+Block+Cipher/Steps+in+the+AES+Encryption+Process/
#                              https://www.youtube.com/watch?v=pSCoquEJsIo
# sBox and sBoxInv from : https://gist.github.com/raullenchai/2920069

sBox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

sBoxInv = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
           0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
           0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
           0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
           0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
           0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
           0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
           0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
           0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
           0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
           0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
           0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
           0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
           0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
           0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
           0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]

rcon = [[1, 0, 0, 0],
        [2, 0, 0, 0],
        [4, 0, 0, 0],
        [8, 0, 0, 0],
        [16, 0, 0, 0],
        [32, 0, 0, 0],
        [64, 0, 0, 0],
        [128, 0, 0, 0],
        [27, 0, 0, 0],
        [54, 0, 0, 0],
        [108, 0, 0, 0]]


def breakIntoBlock(text: str) -> list:
    """
    break a text into square matrices with 1 character of the for each entry, if the length of the text is not a
    multiple of the 16 variable, the missing values of the last block are replaced by spaces
    :param text: text to break
    :return: list of 4 lists
    """
    # creation of the matrix
    blocks = []

    # add a space to the text while its length is not a multiple of blockLen
    while len(text) % 16:
        text += ' '

    # loop of the length of the text divided by 16
    for block in range(len(text) // 16):
        # create a new block with
        blocks.append([[ord(text[row + col * 4 + block * 16])
                        for row in range(4)] for col in range(4)])

    return blocks


def breakKey(key: str) -> list:
    """
    break a key into square matrix with 2 hexadecimal characters for each entry
    :param key: key to break
    :return: list of 4 lists
    """
    # creation of the matrix
    keyBlock = []

    for i in range(4):
        # creation of the column of the matrix
        keyBlock.append([])
        for j in range(4):
            # add the values of the j th column of the key in the j th column of the matrix
            keyBlock[-1].append(int(key[i * 8 + j * 2:i * 8 + j * 2 + 2], 16))
    return [keyBlock]


def mergeBlocks(blocks: list) -> str:
    """
    merge a list of matrices into a text
    :param blocks: blocks to merge
    :return: string containing all the text
    """
    # initialisation of the text
    text = ""
    # loop through the list of matrices
    for block in blocks:
        # loop through the matrix
        for row in block:
            # loop through the row of the matrix
            for char in row:
                # add the entry to the variable containing the text
                text += chr(char)

    return text


def subBytes(block: list) -> list:
    """
    substitute each entry of a matrix by its corresponding value of the sBox
    :param block: matrix to substitue
    :return: new matrix with the substituted entries
    """
    # creation of the new matrix
    newBlock = []

    # loop through the rows of the matrix
    for row in block:
        # creation of the row of the new matrix
        newBlock.append([])
        # loop through the entries of the row
        for char in row:
            # add the substituted value to the new matrix
            newBlock[-1].append(sBox[char])

    return newBlock


def invSubBytes(block: list) -> list:
    """
    get the entries of the initial matrix from the substituted ones
    :param block: block containing the substituted values
    :return: initial matrix
    """
    # creation of the new matrix
    newBlock = []

    # loop through the rows of the matrix
    for row in block:
        # creation of the row of the new matrix
        newBlock.append([])
        # loo through the entries of the row
        for char in row:
            # add the initial value to the new matrix
            newBlock[-1].append(sBoxInv[char])

    return newBlock


def shiftRowsBlock(block: list) -> list:
    """
    shift each rows of a matrix  to the left by a certain number of times
    :param block: matrix to shift
    :return: new matrix with the rows shifted
    """
    # loop through the rows of the matrix
    for i in range(len(block)):
        # shift the i th row to the left i times
        block[i] = shiftRows(block[i], i)

    return block


def invShiftRowsBloc(block: list) -> list:
    """
    shift each rows of a matrix  to the right by a certain number of times
    :param block: matrix to shift
    :return: new matrix with the rows shifted
    """
    # loop through the rows of the matrix
    for i in range(len(block)):
        # shift the i th row to the right i times, which corresponds to -i times to the left
        block[i] = shiftRows(block[i], -i)

    return block


def shiftRows(row: list, n: int) -> list:
    """
    shift the values of the list n times to the left
    :param row: row to shift
    :param n: number of times to shift the row
    :return: shifted list
    """
    return row[n:] + row[:n]


def mixColumns(block: list) -> list:
    """
    multiply the matrix by a fixed one in a finite field
    :param block: matrix to multiply
    :return: new matrix
    """
    # creation of the new matrix
    newBlock = [[] for _ in range(4)]

    for i in range(4):
        # multiply each entry of the 2 matrices
        newBlock[0].append(multiplyBy3(block[3][i]) ^ multiplyBy2(block[0][i]) ^ block[1][i] ^ block[2][i])
        newBlock[1].append(multiplyBy3(block[0][i]) ^ multiplyBy2(block[1][i]) ^ block[2][i] ^ block[3][i])
        newBlock[2].append(multiplyBy3(block[1][i]) ^ multiplyBy2(block[2][i]) ^ block[3][i] ^ block[0][i])
        newBlock[3].append(multiplyBy3(block[2][i]) ^ multiplyBy2(block[3][i]) ^ block[0][i] ^ block[1][i])

    return newBlock


def invMixColumns(block: list) -> list:
    """
    inverse of the previous function, get the initial matrix from the one resulting of the multiplication
    the initial matrix is obtained by multiplying the obtained one by the fixed one 3 times
    :param block: matrix obtained by the multiplication
    :return: initial matrix
    """
    return mixColumns(mixColumns(mixColumns(block)))


def multiplyBy2(val: int) -> int:
    """
    multiply a value by 2 in a finite field
    :param val: value to multiply
    :return: result of the multiplication
    """
    # shift the bits by one to the left (= multiply by 2)
    newVal = val << 1
    # reduce the result to 255 if its bigger
    newVal &= 0xff

    # check if the original value is smaller than 128,
    # so the result of the multiplication is smaller than 256 and can be contained in a byte
    if val >> 7 != 0:
        # else xor it by 27
        newVal ^= 0x1b

    return newVal


def multiplyBy3(val: int) -> int:
    """
    multiply a value by 3 in a finite field
    :param val: value to multiply
    :return: result of the multiplication
    """
    return multiplyBy2(val) ^ val


def xorRoundKey(block: list, key: list) -> list:
    """
    xor each entry of 2 matrices
    :param block: matrix representing the text to encrypt/decrypt
    :param key: matrix representing the key
    :return: new matrix containing the new values
    """
    for i in range(4):
        for j in range(4):
            block[i][j] ^= key[i][j]

    return block


def roundKeys(key: str, rounds: int) -> list:
    """
    generate multiple keys from one
    :param key: initial key
    :param rounds: number of keys to generate
    :return: list of matrices representing the keys
    """
    # break of the initial key into a matrix
    keys = breakKey(key)

    for r in range(rounds):
        newKey = [[], [], [], []]
        # get the 4th column of the last key
        lastColumn = [k[-1] for k in keys[-1]]
        # shift its rows
        lastColumnRotate = shiftRows(lastColumn, 1)
        # replace the values by the corresponding values of the sBox
        lastColumnSBox = [sBox[b] for b in lastColumnRotate]
        # xor the values with the values of the previous column and
        # the values of the column of the same index in the previous key
        lastColumnRcon = [lastColumnSBox[i] ^ rcon[r][i] ^ keys[-1][i][0] for i in range(4)]

        for i in range(4):
            newKey[i].append(lastColumnRcon[i])

        for i in range(3):
            for j in range(4):
                # xor the values with the values of the previous column
                lastColumnRcon[j] ^= keys[-1][j][i + 1]
                newKey[j].append(lastColumnRcon[j])

        keys.append(newKey)

    return keys


def encrypt_aes128(key: str, text: str) -> str:
    """
    encrypt a plain text using the AES 128 algorithm
    :param key: 32 hexadecimal characters key
    :param text: plain text
    :return: cipher text
    """
    # generate 10 keys
    keys = roundKeys(key, 10)
    # break the text into blocks
    textBlock = breakIntoBlock(text)

    # perform the initial round, the 8 main rounds, and the final one on each block
    for block in textBlock:
        block = xorRoundKey(block, keys[0])

        for i in range(1, 10):
            block = subBytes(block)
            block = shiftRowsBlock(block)
            block = mixColumns(block)
            block = xorRoundKey(block, keys[i])

        block = subBytes(block)
        block = shiftRowsBlock(block)
        block = xorRoundKey(block, keys[-1])

    return mergeBlocks(textBlock)


def decrypt_aes128(key: str, text: str) -> str:
    """
    decrypt a cipher text using the AES 128 algorithm
    :param key: 32 hexadecimal characters key
    :param text: cipher text
    :return: plain text
    """
    # generate 10 keys
    keys = roundKeys(key, 10)
    # break the text into blocks
    textBlock = breakIntoBlock(text)

    # perform the initial round, the 8 main rounds, and the final one on each block
    for block in textBlock:
        block = xorRoundKey(block, keys[0])
        block = invSubBytes(block)

        for i in range(1, 10):
            block = xorRoundKey(block, keys[i])
            block = invMixColumns(block)
            block = invShiftRowsBloc(block)
            block = invSubBytes(block)

        block = xorRoundKey(block, keys[-1])

    return mergeBlocks(textBlock)

