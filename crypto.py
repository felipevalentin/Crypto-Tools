from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import urllib.request
import base64


def hex_digest_sha256(file):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file)
    digest = digest.finalize()
    hex_digest = digest.hex()
    return hex_digest


def generate_keys(size):
    """
    Interface para gerar chaves, salvar, serializar e decodifica-las.
    """
    private_key = generate_private_key(size)
    public_key = private_key.public_key()
    private_serialize = serialize_private_key(private_key)
    public_serialize = serialize_public_key(public_key)
    decoded_private = private_serialize.decode()
    decoded_public = public_serialize.decode()

    return (decoded_public, decoded_private)


def generate_private_key(size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size,
    )
    return private_key


def serialize_private_key(private_key):
    # é utilizado o formato PKCS8 e enconding PEM por sugestão do cryptography
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem


def serialize_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem


def decipherECB(link, password):
    """
    Interface para fazer donwload do arquivo, descriptografar e remover padding
    """

    # Senha deve estar em bytes
    if not isinstance(password, (bytes, bytearray, memoryview)):
        password = password.encode()

    filename, encoded_data = request_link(link)
    decoded_data = base64.b64decode(encoded_data)
    data = decrypt_data(decoded_data, password)

    return (filename, data)


def request_link(link):
    req = urllib.request.urlopen(link)
    encoded_data = req.read()
    filename = req.info().get_filename()
    return (filename, encoded_data)


def decrypt_data(encrypt_data, password):
    cipher = Cipher(algorithms.AES(password), modes.ECB())
    decryptor = cipher.decryptor()
    data_padded = decryptor.update(encrypt_data) + decryptor.finalize()
    data = unpadding(data_padded)
    return data


def unpadding(padded_data):
    # Só descriptografa mensagems com padding pkcs7
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data
