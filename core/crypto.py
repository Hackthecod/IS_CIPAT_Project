from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from phe import paillier

class CryptoEngine:
    """Manages RSA Keypairs for Digital Signatures and Paillier Homomorphic Encryption for Ballots."""
    def __init__(self):
        # Generate Paillier Keypair for Homomorphic Ballot Summation
        self.pai_public_key, self.pai_private_key = paillier.generate_paillier_keypair(n_length=1024)

    def generate_rsa_keypair(self):
        """Generates RSA keys for voter signing."""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def sign_vote(self, private_key, vote_payload: str) -> bytes:
        """Digitally sign the encrypted vote payload using voter's private key."""
        signature = private_key.sign(
            vote_payload.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, public_key, signature: bytes, vote_payload: str) -> bool:
        """Verifies voter signature against payload."""
        try:
            public_key.verify(
                signature,
                vote_payload.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def encrypt_vote(self, choice_index: int):
        """Encrypts a binary choice using Paillier Homomorphic Encryption."""
        return self.pai_public_key.encrypt(choice_index)

    def decrypt_aggregate(self, encrypted_sum):
        """Decrypts the homomorphically added votes."""
        return self.pai_private_key.decrypt(encrypted_sum)