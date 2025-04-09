from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes


# Encrypts a message using AES encryption in CBC mode
def encrypt_aes(message, key, iv):
    padded_message = pad(
        message.encode(), AES.block_size
    )  # Ensure the message length is a multiple of the block size
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize AES with key and IV
    encrypted_message = cipher.encrypt(padded_message)  # Encrypt the padded message
    # Return base64-encoded IV and encrypted message, separated by a colon
    return (
        b64encode(iv).decode("utf-8")
        + ":"
        + b64encode(encrypted_message).decode("utf-8")
    )


# Decrypts a message previously encrypted with AES in CBC mode
def decrypt_aes(encrypted_data, key):
    iv_b64, encrypted_message_b64 = encrypted_data.split(
        ":"
    )  # Extract IV and encrypted message
    iv = b64decode(iv_b64)  # Decode the base64 IV
    encrypted_message = b64decode(
        encrypted_message_b64
    )  # Decode the base64 encrypted message
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize AES with the same key and IV
    decrypted_message = unpad(
        cipher.decrypt(encrypted_message), AES.block_size
    )  # Decrypt and remove padding
    return decrypted_message.decode("utf-8")  # Return the original message as a string


# Encodes a password into bytes; serves as a placeholder for more advanced hashing
def hash_password(password):
    return password.encode("utf-8")
