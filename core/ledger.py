import hashlib
import json
from datetime import datetime

class AuditLedger:
    """Implements a cryptographic hash-linked chain for anonymous vote storage."""
    def __init__(self):
        self.chain = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": str(datetime.now()),
            "encrypted_vote": "GENESIS",
            "previous_hash": "0" * 64,
            "hash": ""
        }
        genesis["hash"] = self._compute_hash(genesis)
        self.chain.append(genesis)

    def _compute_hash(self, block: dict) -> str:
        block_string = f"{block['index']}{block['timestamp']}{block['encrypted_vote']}{block['previous_hash']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_vote(self, encrypted_vote_repr: str) -> dict:
        prev_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": str(datetime.now()),
            "encrypted_vote": encrypted_vote_repr,
            "previous_hash": prev_block["hash"],
            "hash": ""
        }
        new_block["hash"] = self._compute_hash(new_block)
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> tuple[bool, int]:
        """Checks if any block in the ledger has been tampered with."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            
            if curr["previous_hash"] != prev["hash"]:
                return False, i
            if curr["hash"] != self._compute_hash(curr):
                return False, i
        return True, -1

    def tamper_block(self, index: int, fake_vote_repr: str):
        """Simulate malicious database edit for demonstration."""
        if 0 < index < len(self.chain):
            self.chain[index]["encrypted_vote"] = fake_vote_repr