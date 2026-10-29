"""Canonical, language-independent registry for the CBOM ground-truth corpus.

Every marker in every annotated template references one of the asset IDs below
(algorithms, related crypto material, the certificate, the protocol) or a
library-component ID defined per language in languages.py.
"""

# --------------------------------------------------------------------------
# Scenarios (identical order and semantics in all five implementations)
# --------------------------------------------------------------------------
SCENARIOS = [
    ("S01", "SHA-256 digest of MESSAGE", "Known answer (Wikipedia / NIST example message)"),
    ("S02", "SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE", "Known answers"),
    ("S03", "Legacy MD5 and SHA-1 digests of MESSAGE", "Known answers; deliberately weak algorithms"),
    ("S04", "SHAKE128 XOF, 32-byte output", "Known answer"),
    ("S05", "HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key", "Known answer (Wikipedia HMAC example)"),
    ("S06", "HKDF-SHA256 extract-and-expand, L=42", "Known answer (RFC 5869 A.1)"),
    ("S07", "PBKDF2-HMAC-SHA256, c=80000, dkLen=64", "Known answer (RFC 7914 section 11)"),
    ("S08", "scrypt N=16384 r=8 p=1, dkLen=64", "Known answer (RFC 7914 section 12)"),
    ("S09", "Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt", "Deterministic; identical across languages"),
    ("S10", "bcrypt cost 12 with random salt, then verify", "Randomized; prints verify=true"),
    ("S11", "AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD", "Known answer (GCM spec test case 16)"),
    ("S12", "ChaCha20-Poly1305 encrypt/decrypt, random key and nonce", "Randomized round trip"),
    ("S13", "AES-256-CBC with PKCS#7 padding, random key and IV", "Randomized round trip"),
    ("S14", "AES-128-ECB with PKCS#7 padding, hard-coded key", "Known answer: first block = FIPS 197 C.1"),
    ("S15", "AES-256-CTR, random key and 128-bit initial counter block", "Randomized round trip"),
    ("S16", "3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV", "Randomized round trip"),
    ("S17", "RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256", "Randomized"),
    ("S18", "ECDSA P-256 / SHA-256 sign and verify", "Randomized"),
    ("S19", "Ed25519 from a hard-coded seed: public key, signature, verify", "Known public key (RFC 8032 test 1); deterministic signature"),
    ("S20", "X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets", "Randomized; prints agreement booleans"),
    ("S21", "ML-KEM-768 key generation, encapsulation, decapsulation", "Randomized; prints sizes"),
    ("S22", "ML-DSA-65 key generation, signing, verification", "Randomized; prints signature size"),
    ("S23", "Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified", "Randomized"),
    ("S24", "TLS 1.3-only client configuration (no network I/O)", "Configuration only"),
]

# --------------------------------------------------------------------------
# Algorithm assets
#   prim  : CycloneDX 1.6 cryptoProperties.algorithmProperties.primitive
#   cls   : classicalSecurityLevel (bits) - None when it depends on secret entropy
#   q     : nistQuantumSecurityLevel (0 = broken by a CRQC or below category 1)
# --------------------------------------------------------------------------
ALGORITHMS = {}


def _alg(aid, name, prim, family, pset=None, mode=None, padding=None, curve=None,
         cls=None, q=None, oid=None, std=(), nist="", cnsa="", quantum="", deps=(),
         note="", implicit=False):
    ALGORITHMS[aid] = dict(id=aid, name=name, primitive=prim, family=family,
                           parameterSetIdentifier=pset, mode=mode, padding=padding,
                           curve=curve, classicalSecurityLevel=cls,
                           nistQuantumSecurityLevel=q, oid=oid, standards=list(std),
                           nistStatus=nist, cnsa2=cnsa, quantum=quantum,
                           dependsOn=list(deps), note=note, implicit=implicit)


SHOR = "Broken by Shor's algorithm on a CRQC"
GROVER = "Generic quantum speed-up only (Grover/BHT)"

_alg("sha-256", "SHA-256", "hash", "SHA-2", "256", cls=128, q=2,
     oid="2.16.840.1.101.3.4.2.1", std=["FIPS 180-4"], nist="Approved",
     cnsa="Not CNSA 2.0 (requires SHA-384/SHA-512)", quantum=GROVER,
     note="Collision resistance 128 bits; reference point of NIST PQ category 2.")
_alg("sha-384", "SHA-384", "hash", "SHA-2", "384", cls=192, q=4,
     oid="2.16.840.1.101.3.4.2.2", std=["FIPS 180-4"], nist="Approved",
     cnsa="CNSA 2.0 compliant", quantum=GROVER, implicit=True,
     note="Only implicit: PRF hash of the TLS_AES_256_GCM_SHA384 cipher suite (S24).")
_alg("sha-512", "SHA-512", "hash", "SHA-2", "512", cls=256, q=4,
     oid="2.16.840.1.101.3.4.2.3", std=["FIPS 180-4"], nist="Approved",
     cnsa="CNSA 2.0 compliant", quantum=GROVER,
     note="Category >= 4 (SHA-384 collision is the highest hash-based NIST reference point).")
_alg("sha3-256", "SHA3-256", "hash", "SHA-3", "256", cls=128, q=2,
     oid="2.16.840.1.101.3.4.2.8", std=["FIPS 202"], nist="Approved",
     cnsa="Not CNSA 2.0", quantum=GROVER)
_alg("blake2b-512", "BLAKE2b-512", "hash", "BLAKE2", "512", cls=256, q=4,
     oid="1.3.6.1.4.1.1722.12.2.1.16", std=["RFC 7693"],
     nist="Not NIST-approved", cnsa="Not CNSA 2.0", quantum=GROVER)
_alg("md5", "MD5", "hash", "MD5", "128", cls=18, q=0,
     oid="1.2.840.113549.2.5", std=["RFC 1321", "RFC 6151"],
     nist="Not approved (collisions found in seconds)", cnsa="Not CNSA 2.0",
     quantum="Already broken classically",
     note="classicalSecurityLevel reflects the ~2^18 practical collision attack.")
_alg("sha-1", "SHA-1", "hash", "SHA-1", "160", cls=63, q=0,
     oid="1.3.14.3.2.26", std=["FIPS 180-4", "RFC 3174"],
     nist="Disallowed for signature generation (SP 800-131A r2); NIST retires SHA-1 by 2030-12-31",
     cnsa="Not CNSA 2.0", quantum="Already broken classically (chosen-prefix collision ~2^63)")
_alg("shake128", "SHAKE128", "xof", "SHA-3", "128", cls=128, q=2,
     oid="2.16.840.1.101.3.4.2.11", std=["FIPS 202"], nist="Approved",
     cnsa="Not CNSA 2.0", quantum=GROVER,
     note="Used with a 256-bit output (min(d/2,128) = 128-bit collision resistance).")
_alg("hmac-sha256", "HMAC-SHA256", "mac", "HMAC", "256", cls=256, q=5,
     oid="1.2.840.113549.2.9", std=["FIPS 198-1", "RFC 2104"],
     nist="Approved (key >= 112 bits required; this corpus uses a 24-bit test key)",
     cnsa="Not CNSA 2.0 (SHA-384+ required)", quantum=GROVER, deps=["sha-256"],
     note="Algorithm-level strength assumes a >=256-bit key; see m.hmac-key for the actual key.")
_alg("hkdf-sha256", "HKDF-SHA256", "kdf", "HKDF", "SHA-256", cls=256, q=5,
     oid="1.2.840.113549.1.9.16.3.29", std=["RFC 5869", "SP 800-56C r2"],
     nist="Approved (two-step KDF, SP 800-56C r2)", cnsa="Not CNSA 2.0 (SHA-384+ required)",
     quantum=GROVER, deps=["hmac-sha256", "sha-256"])
_alg("pbkdf2-hmac-sha256", "PBKDF2-HMAC-SHA256", "kdf", "PBKDF2", "SHA-256",
     oid="1.2.840.113549.1.5.12", std=["SP 800-132", "RFC 8018"],
     nist="Approved (SP 800-132); 80,000 iterations is below the OWASP 2023 figure of 600,000",
     cnsa="Not CNSA 2.0", quantum=GROVER, deps=["hmac-sha256", "sha-256"],
     note="Strength is bounded by password entropy, so no fixed security level is assigned.")
_alg("scrypt", "scrypt", "kdf", "scrypt", "N=16384,r=8,p=1",
     oid="1.3.6.1.4.1.11591.4.11", std=["RFC 7914"], nist="Not NIST-approved",
     cnsa="Not CNSA 2.0", quantum=GROVER, deps=["pbkdf2-hmac-sha256"],
     note="Memory-hard password KDF (internally PBKDF2-HMAC-SHA256 + Salsa20/8).")
_alg("argon2id", "Argon2id", "kdf", "Argon2", "t=2,m=19456,p=1,v=0x13",
     std=["RFC 9106"], nist="Not NIST-approved (OWASP first choice for password storage)",
     cnsa="Not CNSA 2.0", quantum=GROVER,
     note="No standard OID is assigned. Internally uses BLAKE2b.")
_alg("bcrypt", "bcrypt", "kdf", "bcrypt", "cost=12",
     std=["Provos & Mazieres, USENIX 1999"], nist="Not NIST-approved",
     cnsa="Not CNSA 2.0", quantum=GROVER,
     note="Eksblowfish-based password hash; passwords truncated at 72 bytes.")
_alg("aes-256-gcm", "AES-256-GCM", "ae", "AES", "256", mode="gcm", cls=256, q=5,
     oid="2.16.840.1.101.3.4.1.46", std=["FIPS 197", "SP 800-38D"], nist="Approved",
     cnsa="CNSA 2.0 compliant (AES-256)", quantum=GROVER,
     note="128-bit tag, 96-bit IV. Hard-coded key/IV in S11 are a published test vector.")
_alg("aes-128-gcm", "AES-128-GCM", "ae", "AES", "128", mode="gcm", cls=128, q=1,
     oid="2.16.840.1.101.3.4.1.6", std=["FIPS 197", "SP 800-38D"], nist="Approved",
     cnsa="Not CNSA 2.0 (AES-256 required)", quantum=GROVER, implicit=True,
     note="Only implicit: TLS_AES_128_GCM_SHA256 cipher suite (S24).")
_alg("chacha20-poly1305", "ChaCha20-Poly1305", "ae", "ChaCha20", "256", mode="other",
     cls=256, q=5, oid="1.2.840.113549.1.9.16.3.18", std=["RFC 8439"],
     nist="Not NIST-approved", cnsa="Not CNSA 2.0", quantum=GROVER,
     note="Stream-cipher AEAD; mode reported as 'other'.")
_alg("aes-256-cbc", "AES-256-CBC-PKCS7", "block-cipher", "AES", "256", mode="cbc",
     padding="pkcs7", cls=256, q=5, oid="2.16.840.1.101.3.4.1.42",
     std=["FIPS 197", "SP 800-38A"],
     nist="Approved mode; unauthenticated (padding-oracle risk without a MAC)",
     cnsa="AES-256 meets CNSA 2.0 key size", quantum=GROVER)
_alg("aes-128-ecb", "AES-128-ECB-PKCS7", "block-cipher", "AES", "128", mode="ecb",
     padding="pkcs7", cls=128, q=1, oid="2.16.840.1.101.3.4.1.1",
     std=["FIPS 197", "SP 800-38A"],
     nist="Approved block cipher, but ECB leaks plaintext block equality - flag as weak mode",
     cnsa="Not CNSA 2.0 (AES-256 required)", quantum=GROVER)
_alg("aes-256-ctr", "AES-256-CTR", "block-cipher", "AES", "256", mode="ctr",
     cls=256, q=5, std=["FIPS 197", "SP 800-38A"],
     nist="Approved mode; unauthenticated", cnsa="AES-256 meets CNSA 2.0 key size",
     quantum=GROVER, note="No NIST OID is registered for AES-CTR.")
_alg("3des-cbc", "3DES-CBC-PKCS7 (3-key TDEA)", "block-cipher", "3DES", "168", mode="cbc",
     padding="pkcs7", cls=112, q=0, oid="1.2.840.113549.3.7",
     std=["SP 800-67 r2 (withdrawn 2024-01-01)", "SP 800-38A"],
     nist="Disallowed for encryption after 2023-12-31 (SP 800-131A r2); decryption legacy-use only",
     cnsa="Not CNSA 2.0", quantum="Below NIST category 1 (112-bit classical)",
     note="64-bit block size (Sweet32 birthday bound).")
_alg("rsa-3072", "RSA-3072 key pair", "pke", "RSA", "3072", cls=128, q=0,
     oid="1.2.840.113549.1.1.1", std=["FIPS 186-5", "RFC 8017"],
     nist="Acceptable; quantum-vulnerable - disallowed after 2035 (NIST IR 8547)",
     cnsa="CNSA 1.0 only (>=3072); not CNSA 2.0", quantum=SHOR,
     note="The same key pair is used for encryption (OAEP) and two signature schemes - a key-separation finding (SP 800-57 Pt 1 section 5.2).")
_alg("mgf1-sha256", "MGF1-SHA256", "other", "MGF1", "SHA-256",
     oid="1.2.840.113549.1.1.8", std=["RFC 8017"], nist="Approved (as part of OAEP/PSS)",
     cnsa="Not CNSA 2.0", quantum=GROVER, deps=["sha-256"])
_alg("rsa-oaep-sha256", "RSAES-OAEP-SHA256 (RSA-3072)", "pke", "RSA", "3072",
     padding="oaep", cls=128, q=0, oid="1.2.840.113549.1.1.7",
     std=["RFC 8017", "SP 800-56B r2"], nist="Approved; quantum-vulnerable (IR 8547)",
     cnsa="CNSA 1.0 only", quantum=SHOR, deps=["rsa-3072", "sha-256", "mgf1-sha256"],
     note="Label hash SHA-256 and MGF1 hash SHA-256, empty label.")
_alg("rsassa-pss-sha256", "RSASSA-PSS-SHA256 (RSA-3072)", "signature", "RSA", "3072",
     padding="other", cls=128, q=0, oid="1.2.840.113549.1.1.10",
     std=["RFC 8017", "FIPS 186-5"], nist="Approved; quantum-vulnerable (IR 8547)",
     cnsa="CNSA 1.0 only", quantum=SHOR, deps=["rsa-3072", "sha-256", "mgf1-sha256"],
     note="CycloneDX has no 'pss' padding value, so padding='other'. Salt length 32, trailer 0xBC.")
_alg("rsassa-pkcs1v15-sha256", "RSASSA-PKCS1-v1_5-SHA256 (RSA-3072)", "signature", "RSA",
     "3072", padding="pkcs1v15", cls=128, q=0, oid="1.2.840.113549.1.1.11",
     std=["RFC 8017", "FIPS 186-5"], nist="Approved; quantum-vulnerable (IR 8547)",
     cnsa="CNSA 1.0 only", quantum=SHOR, deps=["rsa-3072", "sha-256"])
_alg("ecdsa-p256-sha256", "ECDSA P-256 with SHA-256", "signature", "ECDSA", "P-256",
     curve="secp256r1", cls=128, q=0, oid="1.2.840.10045.4.3.2",
     std=["FIPS 186-5", "SP 800-186"], nist="Approved; quantum-vulnerable (IR 8547)",
     cnsa="Not CNSA (P-384 required)", quantum=SHOR, deps=["sha-256"])
_alg("ecdh-p256", "ECDH P-256", "key-agree", "ECDH", "P-256", curve="secp256r1",
     cls=128, q=0, oid="1.3.132.1.12", std=["SP 800-56A r3", "SP 800-186"],
     nist="Approved; quantum-vulnerable (IR 8547)", cnsa="Not CNSA (P-384 required)",
     quantum=SHOR)
_alg("x25519", "X25519", "key-agree", "ECDH", "Curve25519", curve="curve25519",
     cls=128, q=0, oid="1.3.101.110", std=["RFC 7748"],
     nist="Not listed in SP 800-56A r3", cnsa="Not CNSA", quantum=SHOR)
_alg("ed25519", "Ed25519", "signature", "EdDSA", "Ed25519", curve="edwards25519",
     cls=128, q=0, oid="1.3.101.112", std=["RFC 8032", "FIPS 186-5"],
     nist="Approved (FIPS 186-5); quantum-vulnerable (IR 8547)", cnsa="Not CNSA",
     quantum=SHOR, deps=["sha-512"], note="SHA-512 is used internally (implicit).")
_alg("ml-kem-768", "ML-KEM-768", "kem", "ML-KEM", "768", cls=192, q=3,
     oid="2.16.840.1.101.3.4.4.2", std=["FIPS 203"], nist="Approved",
     cnsa="Not CNSA 2.0 (ML-KEM-1024 required)", quantum="Designed to resist CRQC",
     deps=["sha3-256", "shake128"], note="Uses SHA3/SHAKE internally (implicit).")
_alg("ml-dsa-65", "ML-DSA-65", "signature", "ML-DSA", "65", cls=192, q=3,
     oid="2.16.840.1.101.3.4.3.18", std=["FIPS 204"], nist="Approved",
     cnsa="Not CNSA 2.0 (ML-DSA-87 required)", quantum="Designed to resist CRQC",
     note="Hedged (randomized) signing, empty context string.")
_alg("csprng", "Platform CSPRNG", "drbg", "CSPRNG",
     std=["SP 800-90A r1 / OS RNG (implementation-specific)"],
     nist="Depends on implementation (see per-language notes)", cnsa="n/a",
     quantum="Not applicable",
     note="Implementation differs per runtime; see the language README.")
_alg("bc-digest-drbg", "BC DigestRandomGenerator (SHA-256)", "drbg", "Hash-based PRNG",
     "SHA-256", std=["Bouncy Castle C# SecureRandom default"],
     nist="Not a SP 800-90A DRBG", cnsa="n/a", quantum="Not applicable",
     deps=["sha-256"], note="BC C# 'new SecureRandom()' = SHA-256 DigestRandomGenerator auto-seeded from the OS RNG.")

# --------------------------------------------------------------------------
# Related crypto material (CycloneDX relatedCryptoMaterialProperties.type)
#   prov: hardcoded | csprng | keygen | derived | agreed
# --------------------------------------------------------------------------
MATERIALS = {}


def _mat(mid, name, mtype, bits, prov, alg, scenario, value=None, note=""):
    MATERIALS[mid] = dict(id=mid, name=name, type=mtype, size=bits, provenance=prov,
                          algorithmRef=alg, scenario=scenario, value=value, note=note)


_mat("m.hmac-key", "HMAC key", "secret-key", 24, "hardcoded", "hmac-sha256", "S05", '"key" (ASCII)',
     "24-bit key - far below the 112-bit minimum; test vector only")
_mat("m.hkdf-ikm", "HKDF input keying material", "secret-key", 176, "hardcoded", "hkdf-sha256", "S06", "0x0b * 22", "RFC 5869 A.1")
_mat("m.hkdf-salt", "HKDF salt", "salt", 104, "hardcoded", "hkdf-sha256", "S06", "000102...0c", "RFC 5869 A.1")
_mat("m.hkdf-info", "HKDF info", "additional-data", 80, "hardcoded", "hkdf-sha256", "S06", "f0f1...f9", "RFC 5869 A.1")
_mat("m.hkdf-okm", "HKDF output keying material", "secret-key", 336, "derived", "hkdf-sha256", "S06")
_mat("m.pbkdf2-password", "PBKDF2 password", "password", 64, "hardcoded", "pbkdf2-hmac-sha256", "S07", '"Password"', "RFC 7914 section 11")
_mat("m.pbkdf2-salt", "PBKDF2 salt", "salt", 32, "hardcoded", "pbkdf2-hmac-sha256", "S07", '"NaCl"', "32-bit salt is below the SP 800-132 minimum of 128 bits")
_mat("m.pbkdf2-dk", "PBKDF2 derived key", "secret-key", 512, "derived", "pbkdf2-hmac-sha256", "S07")
_mat("m.scrypt-password", "scrypt password", "password", 104, "hardcoded", "scrypt", "S08", '"pleaseletmein"', "RFC 7914 section 12")
_mat("m.scrypt-salt", "scrypt salt", "salt", 112, "hardcoded", "scrypt", "S08", '"SodiumChloride"')
_mat("m.scrypt-dk", "scrypt derived key", "secret-key", 512, "derived", "scrypt", "S08")
_mat("m.password", "Application password", "password", 224, "hardcoded", "argon2id", "S09", '"correct horse battery staple"', "Shared by S09 (Argon2id) and S10 (bcrypt)")
_mat("m.argon2-salt", "Argon2id salt", "salt", 128, "hardcoded", "argon2id", "S09", '"cbom-corpus-salt"')
_mat("m.argon2-dk", "Argon2id output", "secret-key", 256, "derived", "argon2id", "S09")
_mat("m.bcrypt-salt", "bcrypt salt", "salt", 128, "csprng", "bcrypt", "S10")
_mat("m.bcrypt-hash", "bcrypt hash string", "credential", 480, "derived", "bcrypt", "S10", None, "60-character modular-crypt string ($2a$/$2b$)")
_mat("m.gcm-key", "AES-256-GCM key", "secret-key", 256, "hardcoded", "aes-256-gcm", "S11", "feffe992...", "GCM spec test case 16")
_mat("m.gcm-iv", "AES-GCM IV", "nonce", 96, "hardcoded", "aes-256-gcm", "S11", "cafebabefacedbaddecaf888", "Static nonce - reuse with the same key is catastrophic outside a KAT")
_mat("m.gcm-aad", "AES-GCM additional authenticated data", "additional-data", 160, "hardcoded", "aes-256-gcm", "S11", "feedface...", "GCM spec test case 16")
_mat("m.chacha-key", "ChaCha20-Poly1305 key", "secret-key", 256, "csprng", "chacha20-poly1305", "S12")
_mat("m.chacha-nonce", "ChaCha20-Poly1305 nonce", "nonce", 96, "csprng", "chacha20-poly1305", "S12")
_mat("m.cbc-key", "AES-256-CBC key", "secret-key", 256, "csprng", "aes-256-cbc", "S13")
_mat("m.cbc-iv", "AES-CBC IV", "initialization-vector", 128, "csprng", "aes-256-cbc", "S13")
_mat("m.ecb-key", "AES-128-ECB key", "secret-key", 128, "hardcoded", "aes-128-ecb", "S14", "000102...0f", "FIPS 197 appendix C.1")
_mat("m.ctr-key", "AES-256-CTR key", "secret-key", 256, "csprng", "aes-256-ctr", "S15")
_mat("m.ctr-iv", "AES-CTR initial counter block", "initialization-vector", 128, "csprng", "aes-256-ctr", "S15")
_mat("m.tdes-key", "3DES key", "secret-key", 192, "csprng", "3des-cbc", "S16", None, "192 bits incl. parity = 168 effective")
_mat("m.tdes-iv", "3DES IV", "initialization-vector", 64, "csprng", "3des-cbc", "S16")
_mat("m.rsa-private-key", "RSA-3072 private key", "private-key", 3072, "keygen", "rsa-3072", "S17")
_mat("m.rsa-public-key", "RSA-3072 public key", "public-key", 3072, "keygen", "rsa-3072", "S17", None, "e = 65537")
_mat("m.ecdsa-private-key", "ECDSA P-256 private key", "private-key", 256, "keygen", "ecdsa-p256-sha256", "S18")
_mat("m.ecdsa-public-key", "ECDSA P-256 public key", "public-key", 256, "keygen", "ecdsa-p256-sha256", "S18")
_mat("m.ed25519-seed", "Ed25519 private key seed", "private-key", 256, "hardcoded", "ed25519", "S19", "9d61b19d...", "RFC 8032 section 7.1 TEST 1")
_mat("m.ed25519-public-key", "Ed25519 public key", "public-key", 256, "derived", "ed25519", "S19", "d75a9801...", "Derived from the seed")
_mat("m.x25519-private-key-a", "X25519 private key (party A)", "private-key", 256, "keygen", "x25519", "S20")
_mat("m.x25519-private-key-b", "X25519 private key (party B)", "private-key", 256, "keygen", "x25519", "S20")
_mat("m.x25519-shared-secret", "X25519 shared secret", "shared-secret", 256, "agreed", "x25519", "S20")
_mat("m.ecdh-private-key-a", "ECDH P-256 private key (party A)", "private-key", 256, "keygen", "ecdh-p256", "S20")
_mat("m.ecdh-private-key-b", "ECDH P-256 private key (party B)", "private-key", 256, "keygen", "ecdh-p256", "S20")
_mat("m.ecdh-shared-secret", "ECDH P-256 shared secret", "shared-secret", 256, "agreed", "ecdh-p256", "S20")
_mat("m.session-info", "Session-key HKDF info", "additional-data", 208, "hardcoded", "hkdf-sha256", "S20", '"cbom-corpus session key v1"')
_mat("m.session-key", "Session key (HKDF over X25519 || ECDH secrets)", "secret-key", 256, "derived", "hkdf-sha256", "S20")
_mat("m.mlkem-decapsulation-key", "ML-KEM-768 decapsulation key", "private-key", None, "keygen", "ml-kem-768", "S21", None, "64-byte seed form or 2400-byte expanded form, library-dependent")
_mat("m.mlkem-encapsulation-key", "ML-KEM-768 encapsulation key", "public-key", 9472, "keygen", "ml-kem-768", "S21", None, "1184 bytes")
_mat("m.mlkem-shared-secret", "ML-KEM-768 shared secret", "shared-secret", 256, "agreed", "ml-kem-768", "S21")
_mat("m.mldsa-private-key", "ML-DSA-65 private key", "private-key", None, "keygen", "ml-dsa-65", "S22", None, "32-byte seed or 4032-byte expanded form, library-dependent")
_mat("m.mldsa-public-key", "ML-DSA-65 public key", "public-key", 15616, "keygen", "ml-dsa-65", "S22", None, "1952 bytes")
_mat("m.cert-private-key", "Certificate private key (P-256)", "private-key", 256, "keygen", "ecdsa-p256-sha256", "S23")
_mat("m.cert-public-key", "Certificate subject public key (P-256)", "public-key", 256, "keygen", "ecdsa-p256-sha256", "S23")

# --------------------------------------------------------------------------
# Certificate and protocol assets
# --------------------------------------------------------------------------
CERTIFICATES = {
    "cert.self-signed": dict(
        id="cert.self-signed", name="Self-signed X.509 v3 certificate", scenario="S23",
        subjectName="CN=cbom-corpus.example", issuerName="CN=cbom-corpus.example",
        notValidBefore="runtime: now - 1 minute", notValidAfter="runtime: now + 365 days",
        signatureAlgorithmRef="ecdsa-p256-sha256", subjectPublicKeyRef="m.cert-public-key",
        certificateFormat="X.509", serial="64-bit random from the CSPRNG"),
}

PROTOCOLS = {
    "tls13-client": dict(
        id="tls13-client", name="TLS 1.3 client configuration", scenario="S24",
        type="tls", version="1.3",
        cipherSuites=[
            dict(name="TLS_AES_128_GCM_SHA256", identifiers=["0x13", "0x01"],
                 algorithms=["aes-128-gcm", "sha-256"]),
            dict(name="TLS_AES_256_GCM_SHA384", identifiers=["0x13", "0x02"],
                 algorithms=["aes-256-gcm", "sha-384"]),
            dict(name="TLS_CHACHA20_POLY1305_SHA256", identifiers=["0x13", "0x03"],
                 algorithms=["chacha20-poly1305", "sha-256"]),
        ],
        note="Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly "
             "where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit "
             "defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime "
             "defaults."),
}

# --------------------------------------------------------------------------
# Occurrence roles (marker vocabulary)
# --------------------------------------------------------------------------
ROLES = {
    "imp": "Import / using / package reference that brings a crypto API into scope",
    "typ": "Algorithm-specific type reference in a declaration",
    "alg": "Algorithm, mode, padding, curve or hash identifier (string, enum, constant, class or function name)",
    "spec": "Construction of an algorithm parameter or key specification object",
    "ctor": "Instantiation / factory call that creates a primitive, context or engine",
    "init": "Initialisation of a primitive with key, parameters and/or direction",
    "op": "Cryptographic operation invocation (qualifier = CycloneDX-style function)",
    "prm": "Security-relevant parameter literal (qualifier = parameter name)",
    "mat": "Definition of hard-coded related crypto material (identifier through initializer)",
    "cfg": "Protocol configuration element (qualifier = setting)",
}

# map of op qualifiers to CycloneDX 1.6 cryptoFunctions enum
CDX_FUNCTION = {
    "digest": "digest", "tag": "tag", "keyderive": "keyderive", "encrypt": "encrypt",
    "decrypt": "decrypt", "sign": "sign", "verify": "verify", "keygen": "keygen",
    "encapsulate": "encapsulate", "decapsulate": "decapsulate", "agree": "keyderive",
    "generate": "generate", "encode": "other",
}

# Algorithm-name lexicon used for the non-asset (decoy) mention scan
DECOY_PATTERN = (
    r"(?i)(?<![A-Za-z0-9])("
    r"sha-?3[-_]?256|sha3|sha-?512|sha-?384|sha-?256|sha-?1|shake-?128|shake|blake2b?|md5|"
    r"hmac|hkdf|pbkdf2|scrypt|argon2(?:id)?|bcrypt|aes(?:-?256|-?128)?|gcm|cbc|ecb|ctr|"
    r"chacha20(?:-?poly1305)?|poly1305|3des|desede|tdea|des3|rsa|oaep|pss|pkcs1(?:v15)?|"
    r"pkcs[57]|ecdsa|ecdh|ed25519|x25519|p-?256|secp256r1|prime256v1|ml-?kem(?:-?768)?|"
    r"ml-?dsa(?:-?65)?|kyber|dilithium|x\.?509|tls(?:v?1\.?3|13)?"
    r")(?![A-Za-z])"
)
