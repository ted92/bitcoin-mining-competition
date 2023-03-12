import hashlib
import rsa
import base64
import json

def verify_signature(message, signature, pubkey):
    """
    verify a signature
    :param pubkey:
    :param message: t.hash
    :param signature
    :return: bool
    """
    try:
        b_msg = bytes(message, 'utf-8')
        result = rsa.verify(b_msg, signature, pubkey)
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def save_key(key):
    """
    serializes public/private key
    :param key:
    :return:
    """
    return key.save_pkcs1(format="PEM").decode('utf-8')

def load_public(pub):
    """
    deserializes public key
    :param pub:
    :return:
    """
    return rsa.PublicKey.load_pkcs1(pub.encode('utf-8'))

def load_private(pvt):
    """
    deserialize private key
    :param pvt:
    :return:
    """
    return rsa.PrivateKey.load_pkcs1(pvt.encode('utf-8'))

def save_signature(signature):
    """

    :param signature: signature saved with "rsa.sign(b_msg, self.privkey, 'SHA-1')"
    :return:
    """
    serialized_signature = base64.b64encode(signature).decode('utf-8')
    return serialized_signature

def load_signature(serialized_signature):
    """

    :param serialized_signature: signature in format base64
    :return:
    """
    signature = base64.b64decode(serialized_signature.encode('utf-8'))
    return signature


def hash_function(data):
    """
    hash data using SHA256
    :param data:
    :return: hashed value
    """
    return hashlib.sha256(data.encode()).hexdigest()

def double_hash(data):
    """
    it double 256SHA hashes data, used in proof-of-work
    :param data:
    :return:
    """
    hash_obj = hashlib.sha256()
    # Update the hash object with the bytes of the input data
    hash_obj.update(data.encode())
    # Get the hexadecimal representation of the hash
    hex_hash = hash_obj.hexdigest()
    # Create a new SHA-256 hash object
    hash_obj = hashlib.sha256()
    # Update the new hash object with the bytes of the hexadecimal hash
    hash_obj.update(hex_hash.encode())
    # Get the final hexadecimal representation of the double SHA-256 hash
    d_hash = hash_obj.hexdigest()
    return d_hash