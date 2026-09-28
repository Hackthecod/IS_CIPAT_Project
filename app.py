import streamlit as st
import pandas as pd
from core.auth import AuthManager
from core.crypto import CryptoEngine
from core.ledger import AuditLedger
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Initialize System Components in Streamlit State
if 'auth' not in st.session_state:
    st.session_state.auth = AuthManager()
if 'crypto' not in st.session_state:
    st.session_state.crypto = CryptoEngine()
if 'ledger' not in st.session_state:
    st.session_state.ledger = AuditLedger()
if 'homomorphic_sums' not in st.session_state:
    # Encrypted counts for Candidate A (Index 0) and Candidate B (Index 1)
    st.session_state.homomorphic_sums = {
        "Candidate A": st.session_state.crypto.encrypt_vote(0),
        "Candidate B": st.session_state.crypto.encrypt_vote(0)
    }

st.set_page_config(page_title="Cryptographic E-Voting System", layout="wide")
st.title("🛡️ Secure E-Voting System")

# Navigation Sidebar
menu = st.sidebar.radio("Navigation Module", [
    "1. Voter Registration & Authentication",
    "2. Cast Encrypted Vote",
    "3. Cryptographic Audit Ledger",
    "4. Live Decryption & Results",
    "5. Security Audit & Tamper Demo"
])

# MODULE 1: AUTHENTICATION
if menu == "1. Voter Registration & Authentication":
    st.subheader("Voter Authentication & Keypair Provisioning")
    
    col1, col2 = st.columns(2)
    with col1:
        voter_id = st.text_input("Enter National ID / Voter ID:")
        username = st.text_input("Enter Full Name:")
        
        if st.button("Register & Issue Cryptographic Keys"):
            if voter_id and username:
                res = st.session_state.auth.register_voter(username, voter_id)
                if res["status"]:
                    priv_key, pub_key = st.session_state.crypto.generate_rsa_keypair()
                    st.session_state[f"rsa_priv_{voter_id}"] = priv_key
                    st.session_state[f"rsa_pub_{voter_id}"] = pub_key
                    st.success(f"Voter registered! Derived SHA-256 ID Hash: {res['voter_hash'][:16]}...")
                    st.info("RSA-2048 Signing Keys automatically injected into local session.")
                else:
                    st.error(res["msg"])
            else:
                st.warning("Provide all details.")

# MODULE 2: CAST VOTE
elif menu == "2. Cast Encrypted Vote":
    st.subheader("Homomorphic Voting Console")
    
    voter_id = st.text_input("Confirm Registered Voter ID:")
    candidate = st.radio("Select Candidate:", ["Candidate A", "Candidate B"])
    
    if st.button("Sign & Submit Ballot"):
        if not voter_id or f"rsa_priv_{voter_id}" not in st.session_state:
            st.error("Voter not authenticated or keypair missing.")
        elif st.session_state.auth.has_voted(voter_id):
            st.error("Access Denied: Double voting detected. Keypair already spent.")
        else:
            # 1. Homomorphic Encryption
            enc_vote = st.session_state.crypto.encrypt_vote(1)
            enc_vote_str = str(enc_vote.ciphertext())[:20] + "..."
            
            # 2. Digital Signature
            priv_key = st.session_state[f"rsa_priv_{voter_id}"]
            signature = st.session_state.crypto.sign_vote(priv_key, enc_vote_str)
            
            # 3. Signature Verification
            pub_key = st.session_state[f"rsa_pub_{voter_id}"]
            if st.session_state.crypto.verify_signature(pub_key, signature, enc_vote_str):
                # 4. Homomorphic Aggregation
                st.session_state.homomorphic_sums[candidate] += enc_vote
                
                # 5. Ledger Storage
                block = st.session_state.ledger.add_vote(enc_vote_str)
                st.session_state.auth.mark_voted(voter_id)
                
                st.success("Vote Verified and Stored Anonymously!")
                st.json({"Block Index": block["index"], "Block Hash": block["hash"], "Payload": enc_vote_str})
            else:
                st.error("Signature Validation Failed!")

# MODULE 3: LEDGER
elif menu == "3. Cryptographic Audit Ledger":
    st.subheader("Immutable Hash-Chain Ledger")
    df = pd.DataFrame(st.session_state.ledger.chain)
    st.dataframe(df, use_container_width=True)

# MODULE 4: TALLY
elif menu == "4. Live Decryption & Results":
    st.subheader("Homomorphic Aggregation Results")
    st.caption("Votes are decrypted ONLY in aggregate form using Paillier Private Key.")
    
    if st.button("Compute & Decrypt Tally"):
        res_a = st.session_state.crypto.decrypt_aggregate(st.session_state.homomorphic_sums["Candidate A"])
        res_b = st.session_state.crypto.decrypt_aggregate(st.session_state.homomorphic_sums["Candidate B"])
        
        st.bar_chart({"Candidate A": res_a, "Candidate B": res_b})
        st.metric("Candidate A Total", res_a)
        st.metric("Candidate B Total", res_b)

# MODULE 5: TAMPER DEMO
elif menu == "5. Security Audit & Tamper Demo":
    st.subheader("Vote-Tampering & Ledger Breakdown Demonstration")
    
    is_valid, bad_idx = st.session_state.ledger.verify_integrity()
    if is_valid:
        st.success("Ledger Integrity Verified: All SHA-256 block hashes match.")
    else:
        st.error(f"INTEGRITY FAILURE: Block {bad_idx} has been tampered with!")

    st.divider()
    st.write("### Simulate Database Exploit / Direct Row Modification")
    target_idx = st.number_input("Target Block Index to Manipulate:", min_value=1, max_value=max(1, len(st.session_state.ledger.chain)-1))
    
    if st.button("Inject Malicious Payload"):
        st.session_state.ledger.tamper_block(target_idx, "MALICIOUS_ALTERED_PAYLOAD")
        st.warning(f"Manipulated Block {target_idx} directly in memory.")
        st.rerun()
