import hmac, hashlib

def decrypt_elite_payload(encrypted_blob, key):
    # Only Mohamed's key can unlock these exploits
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted_blob))

# Example of an "Uncopyable" encrypted SSTI payload
ENCRYPTED_SSTI = "LwkfGxoWGB8L..." # Looks like gibberish to everyone else
