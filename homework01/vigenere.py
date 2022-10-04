def extend_keyword(text: str, keyword: str) -> str:
    """
    Extends a keyword to the given text.
    """
    f, p = divmod(len(text), len(keyword))
    return keyword * f + keyword[:p]


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = extend_keyword(plaintext, keyword)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(plaintext)):
        ciphertext += (
            alphabet[(alphabet.find(plaintext[i]) + alphabet.find(keyword[i].upper())) % 26]
            if plaintext[i] in alphabet
            else (
                alphabet_lower[
                    (alphabet_lower.find(plaintext[i]) + alphabet.find(keyword[i].upper())) % 26
                    if keyword[i] in alphabet_lower
                    else plaintext[i]
                ]
            )
        )

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword = extend_keyword(ciphertext, keyword)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(ciphertext)):
        if ciphertext[i] == " ":
            plaintext += " "
        else:
            plaintext += (
                alphabet[(alphabet.find(ciphertext[i]) - alphabet.find(keyword[i].upper())) % 26]
                if ciphertext[i] in alphabet
                else (
                    alphabet_lower[
                        (alphabet_lower.find(ciphertext[i]) - alphabet.find(keyword[i].upper())) % 26
                        if ciphertext[i] in alphabet_lower
                        else ciphertext[i]
                    ]
                )
            )
    return plaintext
