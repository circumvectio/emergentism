import hashlib

# --- BIP340 Schnorr Pure Python Implementation ---
# Reference minimal implementation mapping K2 signatures to Nostr (NIP-01) keys.
# Utilizes secp256k1 curve parameters.

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + msg).digest()

def add_point(p1: tuple, p2: tuple) -> tuple:
    if p1 == (None, None):
        return p2
    if p2 == (None, None):
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 != y2:
        return (None, None)
    if x1 == x2:
        lam = (3 * x1 * x1 * pow(2 * y1, p - 2, p)) % p
    else:
        lam = ((y2 - y1) * pow(x2 - x1, p - 2, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def mul_point(p1: tuple, k: int) -> tuple:
    R = (None, None)
    for i in range(256):
        if (k >> i) & 1:
            R = add_point(R, p1)
        p1 = add_point(p1, p1)
    return R

def verify_schnorr(pubkey: bytes, msg: bytes, sig: bytes) -> bool:
    if len(pubkey) != 32:
        return False
    if len(sig) != 64:
        return False
    
    Px = int.from_bytes(pubkey, 'big')
    if Px >= p:
        return False
    
    # Lift X
    y_sq = (pow(Px, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if pow(y, 2, p) != y_sq:
        return False
    Py = y if y % 2 == 0 else p - y
    
    r = int.from_bytes(sig[0:32], 'big')
    s = int.from_bytes(sig[32:64], 'big')
    if r >= p or s >= n:
        return False
    
    e = int.from_bytes(tagged_hash("BIP0340/challenge", sig[0:32] + pubkey + msg), 'big') % n
    
    # R = s*G - e*P
    # Since P = (Px, Py), -P = (Px, p - Py)
    e_neg_P = mul_point((Px, p - Py), e)
    sG = mul_point((Gx, Gy), s)
    R = add_point(sG, e_neg_P)
    
    if R == (None, None):
        return False
    Rx, Ry = R
    if Ry % 2 != 0:
        return False
    if Rx != r:
        return False
    
    return True


# --- K2 API Gateway Wrapper ---

class K2CryptoVerifier:
    """
    Enforces the K2 boundary (cryptographic proof of mortal execution).
    """
    @staticmethod
    def verify_nostr_approval(
        pubkey_hex: str, 
        action_hash_hex: str, 
        signature_hex: str
    ) -> bool:
        """
        Verifies a Nostr (BIP-340 Schnorr) signature proving that the 
        authorized human explicitly signed the APU action proposal.
        """
        try:
            pubkey = bytes.fromhex(pubkey_hex)
            msg = bytes.fromhex(action_hash_hex)
            sig = bytes.fromhex(signature_hex)
            return verify_schnorr(pubkey, msg, sig)
        except Exception:
            return False

    @staticmethod
    def verify_eth_approval(
        address_hex: str, 
        action_hash_hex: str, 
        signature_hex: str
    ) -> bool:
        """
        Verifies an Ethereum (EIP-191 / EIP-712 compatible) signature proving that the
        authorized human explicitly signed the APU action proposal.
        """
        try:
            from eth_account import Account
            from eth_account.messages import encode_defunct

            msg = bytes.fromhex(action_hash_hex)
            signable_msg = encode_defunct(msg)
            
            recovered_address = Account.recover_message(signable_msg, signature=signature_hex)
            
            return recovered_address.lower() == address_hex.lower()
        except Exception:
            return False

    @staticmethod
    def generate_action_hash(proposal: dict, ruling: str) -> str:
        """
        Deterministically converts an APU proposal and ruling into a unique
        SHA256 hash that the human must sign via Nostr.
        """
        import json
        payload = json.dumps({"proposal": proposal, "ruling": ruling}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()
