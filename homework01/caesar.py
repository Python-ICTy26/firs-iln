import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

    for i in range(len(plaintext)):
        ciphertext += alphabet[(alphabet.find(plaintext[i]) + shift) % 26] if plaintext[i] in alphabet else (
            alphabet_lower[(alphabet_lower.find(plaintext[i]) + shift) % 26] if plaintext[i] in alphabet_lower else
            plaintext[i])
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

    for i in range(len(ciphertext)):
        plaintext += alphabet[(alphabet.find(ciphertext[i]) - shift) % 26] if ciphertext[i] in alphabet else (
            alphabet_lower[(alphabet_lower.find(ciphertext[i]) - shift) % 26] if ciphertext[i] in alphabet_lower else
            ciphertext[i])
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.

     >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker_brute_force("python", d)
    0
    >>> caesar_breaker_brute_force("sbwkrq", d)
    3
    """
    best_shift = 0
    for shift in range(26):
        if decrypt_caesar(ciphertext, shift=shift) in dictionary:
            best_shift = shift
    return best_shift
