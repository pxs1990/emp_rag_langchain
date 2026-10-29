import hashlib


def generate_checksum(text):

    return hashlib.sha256(
        text.encode()
    ).hexdigest()