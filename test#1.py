from cryptography.fernet import Fernet


def gen(n):
    i = 0
    while i != n:
        yield i
        i += 1

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt(text, n):
    if text == '' or text == None:
        return text
    if n <= 0:
        return text
    text = text.lower()
    length = len(text)
    evens = ''
    odds = ''
    for Letter in gen(length):
        if Letter % 2 == 1:
            evens += text[Letter]
        else:
            odds += text[Letter]
    result =  evens + odds
    for times in range(n - 1):
        result = encrypt(result, 1)
    # print(result)
    return result

def decrypter(func):
    def wrapper(text, *args):
        key = load_key()
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(text).decode()
        result = func(decrypted_text, *args)
        return result
    return wrapper

@decrypter
def decrypt(text, n):
    return encrypt(text, n)


if __name__ == '__main__':
    print(encrypt('Abcdefghij', 2))
    generate_key()
    key = load_key()
    text = 'Abcdefghij'
    encoded_text = text.encode()
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(encoded_text)
    print(decrypt(encrypted_text, 2))
    