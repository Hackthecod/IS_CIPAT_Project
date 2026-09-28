import hashlib
import uuid
from datetime import datetime

class AuthManager:
    """Handles Voter Registration, MFA Token Mocking, and Session Identity."""
    def __init__(self):
        # In-memory storage for demonstration
        self.voters_db = {}
        self.voted_users = set()

    def register_voter(self, username: str, voter_id: str) -> dict:
        if voter_id in self.voters_db:
            return {"status": False, "msg": "Voter ID already registered."}
        
        # Salted Hash for credentials
        voter_hash = hashlib.sha256(f"{voter_id}:{username}".encode()).hexdigest()
        
        self.voters_db[voter_id] = {
            "username": username,
            "voter_hash": voter_hash,
            "registered_at": str(datetime.now())
        }
        return {"status": True, "voter_hash": voter_hash}

    def has_voted(self, voter_id: str) -> bool:
        return voter_id in self.voted_users

    def mark_voted(self, voter_id: str):
        self.voted_users.add(voter_id)