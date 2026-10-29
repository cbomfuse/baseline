# CBOM ground-truth corpus - Python

`crypto_showcase.py` is the Python implementation of a 24-scenario cryptography program that is logically identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic asset appears in it: **195 occurrences** of **84 assets** (33 algorithms, 49 items of related crypto material, 1 certificate, 1 protocol) drawn from **6 library components**, plus **164 non-asset mentions** of algorithm names that a scanner should *not* report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.

## Files

| File | Purpose |
|---|---|
| `crypto_showcase.py` | The program (365 lines, ASCII, LF line endings) |
| `requirements.txt` | Build manifest |
| `README.md` | This document |
| `cbom.cdx.json` | Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema) |
| `ground-truth.json` | Complete occurrence ledger, asset inventory and non-asset mentions |

## Build and run

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python3 crypto_showcase.py
```

Verified in the build environment with CPython 3.12.3 (Ubuntu 24.04, x86_64): venv with requirements.txt, python3 crypto_showcase.py. Standard output was byte-identical to the other four implementations (see the corpus README).

## Expected output

Deterministic lines are known-answer tests (published vectors where one exists); randomized scenarios print only booleans and sizes, so the output is identical on every run and in every language.

```text
[S01] SHA-256            d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592
[S02] SHA-512            07e547d9586f6a73f73fbac0435ed76951218fb7d0c8d788a309d785436bbb642e93a252a954f23912547d1e8a3b5ed6e1bfd7097821233fa0538f3db854fee6
[S02] SHA3-256           69070dda01975c8c120c3aada1b282394e7f032fa9cf32f4cb2259a0897dfc04
[S02] BLAKE2b-512        a8add4bdddfd93e4877d2746e62817b116364a1fa7bc148d95090bc7333b3673f82401cf7aa2e4cb1ecd90296e3f14cb5413f8ed77be73045b13914cdcd6a918
[S03] MD5                9e107d9d372bb6826bd81d3542a419d6
[S03] SHA-1              2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
[S04] SHAKE128           f4202e3c5852f9182a0430fd8144f0a74b95e7417ecae17db0f8cfeed0e3e66e
[S05] HMAC-SHA256        f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8
[S06] HKDF-SHA256        3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865
[S07] PBKDF2-SHA256      4ddcd8f60b98be21830cee5ef22701f9641a4418d04c0414aeff08876b34ab56a1d425a1225833549adb841b51c9b3176a272bdebba1d078478f62b397f33c8d
[S08] scrypt             7023bdcb3afd7348461c06cd81fd38ebfda8fbba904f8e3ea9b543f6545da1f2d5432955613f0fcf62d49705242a9af9e61e85dc0d651e40dfcf017b45575887
[S09] Argon2id           d67be636093852d3dcef015c096c399035a9c19bdec40abde477558ec2aa6a5d
[S10] bcrypt             verify=true
[S11] AES-256-GCM        ct=522dc1f099567d07f47f37a32a84427d643a8cdcbfe5c0c97598a2bd2555d1aa8cb08e48590dbb3da7b08b1056828838c5f61e6393ba7a0abcc9f662 tag=76fc6ece0f4e1768cddf8853bb2d551b roundtrip=true
[S12] ChaCha20-Poly1305  roundtrip=true
[S13] AES-256-CBC        roundtrip=true
[S14] AES-128-ECB        69c4e0d86a7b0430d8cdb78070b4c55a954f64f2e4e86e9eee82d20216684899
[S15] AES-256-CTR        roundtrip=true
[S16] 3DES-CBC           roundtrip=true
[S17] RSA-3072 OAEP      roundtrip=true
[S17] RSA-3072 PSS       verify=true
[S17] RSA-3072 PKCS1v15  verify=true
[S18] ECDSA P-256        verify=true
[S19] Ed25519            pk=d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a sig=a13ce76707a395cbc14e253aee10ffab8cd64978ab2c226afaee9d7002a06e26547d741dfc07bee41d781b0aeb6eec7f135e391439ee0dccfe9335ae3b338803 verify=true
[S20] X25519             agree=true
[S20] ECDH P-256         agree=true
[S20] HKDF session key   match=true
[S21] ML-KEM-768         agree=true ct=1088 ss=32
[S22] ML-DSA-65          verify=true sig=3309
[S23] X.509 self-signed  verify=true
[S24] TLS 1.3 client     configured=true
```

## How occurrences are recorded

An **occurrence** is a contiguous span of source text that names, configures or exercises a cryptographic asset. Coordinates use these conventions:

| Field | Convention |
|---|---|
| Line | 1-based |
| Column | 1-based, counted in Unicode code points (the source is pure ASCII, so it equals the byte column) |
| End | Exclusive: the position just after the last character of the span |
| Char / byte offset | 0-based offset from the start of the file; ranges are half-open `[start, end)` |
| Nesting | Spans may nest (for example a transformation string inside a `getInstance` call); each span is its own occurrence |
| CycloneDX `offset` | Written as column - 1 (0-based column); absolute ranges are in `additionalContext` |

Roles:

| Role | Meaning |
|---|---|
| `imp` | Import / using / package reference that brings a crypto API into scope |
| `typ` | Algorithm-specific type reference in a declaration |
| `alg` | Algorithm, mode, padding, curve or hash identifier (string, enum, constant, class or function name) |
| `spec` | Construction of an algorithm parameter or key specification object |
| `ctor` | Instantiation / factory call that creates a primitive, context or engine |
| `init` | Initialisation of a primitive with key, parameters and/or direction |
| `op` | Cryptographic operation invocation (qualifier = CycloneDX-style function) |
| `prm` | Security-relevant parameter literal (qualifier = parameter name) |
| `mat` | Definition of hard-coded related crypto material (identifier through initializer) |
| `cfg` | Protocol configuration element (qualifier = setting) |

Recording rules: data-feeding calls (`update`, `updateAAD`, `setAAD`, `Write`, `BlockUpdate`, `doPhase`) are not recorded separately; imports are recorded only for crypto-specific modules; material produced by an operation is attributed to that operation's span (`produces`); a hash or MGF identifier used inside a composite scheme is recorded against the hash asset with the composite as its parent (`^`), and it is also listed under the parent asset; a call site that serves two assets depending on the caller is recorded once per asset.

## Summary

| Measure | Count |
|---|---|
| Occurrences | 195 |
| Occurrences with role `imp` | 22 |
| Occurrences with role `alg` | 44 |
| Occurrences with role `ctor` | 17 |
| Occurrences with role `op` | 66 |
| Occurrences with role `prm` | 28 |
| Occurrences with role `mat` | 16 |
| Occurrences with role `cfg` | 2 |
| Algorithm assets (incl. implicit) | 33 |
| Implicit assets (no source occurrence) | 2 |
| Related crypto material | 49 |
| Certificates | 1 |
| Protocols | 1 |
| Library components | 6 |
| Non-asset mentions | 164 |

## Libraries

| ID | Component | Version | purl | License | Scope | Import occurrences | Other occurrences | Assets provided | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `lib.py-stdlib` | CPython standard library | 3.12.3 | `pkg:generic/cpython@3.12.3` | PSF-2.0 | runtime | PY-001, PY-002, PY-003, PY-004 | 41 | sha-256, sha-512, md5, shake128, hmac-sha256, pbkdf2-hmac-sha256, csprng, cert.self-signed, tls13-client, m.hmac-key, m.hkdf-ikm, m.hkdf-salt, m.hkdf-info, m.pbkdf2-password, m.pbkdf2-salt, m.scrypt-password, m.scrypt-salt, m.password, m.argon2-salt, m.gcm-key, m.gcm-iv, m.gcm-aad, m.cbc-key, m.cbc-iv, m.ecb-key, m.ctr-key, m.ctr-iv, m.ed25519-seed, m.session-info | hashlib, hmac, secrets, ssl, os.urandom; hashlib and ssl delegate to the system OpenSSL (3.0.13 in the verification environment) |
| `lib.pyca` | cryptography (pyca) | 50.0.2 | `pkg:pypi/cryptography@50.0.2` | Apache-2.0 OR BSD-3-Clause | required | PY-011, PY-012, PY-013, PY-014, PY-015, PY-016, PY-017, PY-018, PY-019, PY-020 | 91 | sha-256, blake2b-512, sha-1, hkdf-sha256, scrypt, aes-256-gcm, aes-256-cbc, aes-128-ecb, rsa-3072, mgf1-sha256, rsa-oaep-sha256, rsassa-pss-sha256, rsassa-pkcs1v15-sha256, ecdsa-p256-sha256, ecdh-p256, x25519, ml-kem-768, ml-dsa-65, cert.self-signed | Rust/OpenSSL-backed primitives; the manylinux wheel statically links OpenSSL 4.0.3 |
| `lib.pycryptodome` | PyCryptodome | 4.2.0 | `pkg:pypi/pycryptodome@4.2.0` | BSD-2-Clause AND Unlicense | required | PY-007, PY-008, PY-009, PY-010 | 28 | sha3-256, chacha20-poly1305, aes-256-ctr, 3des-cbc, csprng, m.chacha-key, m.chacha-nonce, m.tdes-key, m.tdes-iv | Self-contained C implementations (Crypto.* namespace) |
| `lib.pynacl` | PyNaCl | 1.6.2 | `pkg:pypi/pynacl@1.6.2` | Apache-2.0 | required | PY-021, PY-022 | 3 | ed25519 | Bindings to the bundled libsodium |
| `lib.argon2-cffi` | argon2-cffi | 25.1.0 | `pkg:pypi/argon2-cffi@25.1.0` | MIT | required | PY-005 | 6 | argon2id | Argon2 via argon2-cffi-bindings 26.1.0 (reference C implementation) |
| `lib.bcrypt` | bcrypt | 5.0.0 | `pkg:pypi/bcrypt@5.0.0` | Apache-2.0 | required | PY-006 | 4 | bcrypt, csprng | pyca bcrypt (Rust implementation) |

## Algorithm assets

Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):

| Asset | Name | Primitive | Family | Parameter set | Mode | Padding | Curve | Functions | OID | Occurrences | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.1 | 15 | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | - | - | - | 2.16.840.1.101.3.4.2.2 | implicit | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | - | - | digest | 2.16.840.1.101.3.4.2.3 | 1 | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.8 | 1 | - |
| `blake2b-512` | BLAKE2b-512 | hash | BLAKE2 | 512 | - | - | - | digest | 1.3.6.1.4.1.1722.12.2.1.16 | 4 | - |
| `md5` | MD5 | hash | MD5 | 128 | - | - | - | digest | 1.2.840.113549.2.5 | 2 | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | - | - | digest | 1.3.14.3.2.26 | 3 | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | - | - | digest | 2.16.840.1.101.3.4.2.11 | 2 | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | - | - | tag | 1.2.840.113549.2.9 | 2 | sha-256 |
| `hkdf-sha256` | HKDF-SHA256 | kdf | HKDF | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.9.16.3.29 | 8 | hmac-sha256, sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.5.12 | 4 | hmac-sha256, sha-256 |
| `scrypt` | scrypt | kdf | scrypt | N=16384,r=8,p=1 | - | - | - | keyderive | 1.3.6.1.4.1.11591.4.11 | 6 | pbkdf2-hmac-sha256 |
| `argon2id` | Argon2id | kdf | Argon2 | t=2,m=19456,p=1,v=0x13 | - | - | - | keyderive | - | 6 | - |
| `bcrypt` | bcrypt | kdf | bcrypt | cost=12 | - | - | - | keyderive, verify | - | 3 | - |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | gcm | - | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.46 | 3 | - |
| `aes-128-gcm` | AES-128-GCM | ae | AES | 128 | gcm | - | - | - | 2.16.840.1.101.3.4.1.6 | implicit | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | other | - | - | decrypt, encrypt | 1.2.840.113549.1.9.16.3.18 | 4 | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | cbc | pkcs7 | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.42 | 7 | - |
| `aes-128-ecb` | AES-128-ECB-PKCS7 | block-cipher | AES | 128 | ecb | pkcs7 | - | encrypt | 2.16.840.1.101.3.4.1.1 | 5 | - |
| `aes-256-ctr` | AES-256-CTR | block-cipher | AES | 256 | ctr | - | - | decrypt, encrypt | - | 6 | - |
| `3des-cbc` | 3DES-CBC-PKCS7 (3-key TDEA) | block-cipher | 3DES | 168 | cbc | pkcs7 | - | decrypt, encrypt, keygen | 1.2.840.113549.3.7 | 9 | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | - | - | keygen | 1.2.840.113549.1.1.1 | 3 | - |
| `mgf1-sha256` | MGF1-SHA256 | other | MGF1 | SHA-256 | - | - | - | - | 1.2.840.113549.1.1.8 | 4 | sha-256 |
| `rsa-oaep-sha256` | RSAES-OAEP-SHA256 (RSA-3072) | pke | RSA | 3072 | - | oaep | - | decrypt, encrypt | 1.2.840.113549.1.1.7 | 5 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pss-sha256` | RSASSA-PSS-SHA256 (RSA-3072) | signature | RSA | 3072 | - | other | - | sign, verify | 1.2.840.113549.1.1.10 | 7 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pkcs1v15-sha256` | RSASSA-PKCS1-v1_5-SHA256 (RSA-3072) | signature | RSA | 3072 | - | pkcs1v15 | - | sign, verify | 1.2.840.113549.1.1.11 | 5 | rsa-3072, sha-256 |
| `ecdsa-p256-sha256` | ECDSA P-256 with SHA-256 | signature | ECDSA | P-256 | - | - | secp256r1 | keygen, sign, verify | 1.2.840.10045.4.3.2 | 13 | sha-256 |
| `ecdh-p256` | ECDH P-256 | key-agree | ECDH | P-256 | - | - | secp256r1 | keyderive, keygen | 1.3.132.1.12 | 8 | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | - | - | curve25519 | keyderive, keygen | 1.3.101.110 | 4 | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | - | - | edwards25519 | sign, verify | 1.3.101.112 | 3 | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | - | - | decapsulate, encapsulate, keygen | 2.16.840.1.101.3.4.4.2 | 3 | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | - | - | keygen, sign, verify | 2.16.840.1.101.3.4.3.18 | 3 | - |
| `csprng` | Platform CSPRNG | drbg | CSPRNG | - | - | - | - | generate | - | 10 | - |

Security and compliance:

| Asset | Classical bits | NIST PQ category | Standards | NIST status | CNSA 2.0 | Quantum | Note |
|---|---|---|---|---|---|---|---|
| `sha-256` | 128 | 2 | FIPS 180-4 | Approved | Not CNSA 2.0 (requires SHA-384/SHA-512) | Generic quantum speed-up only (Grover/BHT) | Collision resistance 128 bits; reference point of NIST PQ category 2. |
| `sha-384` | 192 | 4 | FIPS 180-4 | Approved | CNSA 2.0 compliant | Generic quantum speed-up only (Grover/BHT) | Only implicit: PRF hash of the TLS_AES_256_GCM_SHA384 cipher suite (S24). |
| `sha-512` | 256 | 4 | FIPS 180-4 | Approved | CNSA 2.0 compliant | Generic quantum speed-up only (Grover/BHT) | Category >= 4 (SHA-384 collision is the highest hash-based NIST reference point). |
| `sha3-256` | 128 | 2 | FIPS 202 | Approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | - |
| `blake2b-512` | 256 | 4 | RFC 7693 | Not NIST-approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | - |
| `md5` | 18 | 0 | RFC 1321; RFC 6151 | Not approved (collisions found in seconds) | Not CNSA 2.0 | Already broken classically | classicalSecurityLevel reflects the ~2^18 practical collision attack. |
| `sha-1` | 63 | 0 | FIPS 180-4; RFC 3174 | Disallowed for signature generation (SP 800-131A r2); NIST retires SHA-1 by 2030-12-31 | Not CNSA 2.0 | Already broken classically (chosen-prefix collision ~2^63) | - |
| `shake128` | 128 | 2 | FIPS 202 | Approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Used with a 256-bit output (min(d/2,128) = 128-bit collision resistance). |
| `hmac-sha256` | 256 | 5 | FIPS 198-1; RFC 2104 | Approved (key >= 112 bits required; this corpus uses a 24-bit test key) | Not CNSA 2.0 (SHA-384+ required) | Generic quantum speed-up only (Grover/BHT) | Algorithm-level strength assumes a >=256-bit key; see m.hmac-key for the actual key. |
| `hkdf-sha256` | 256 | 5 | RFC 5869; SP 800-56C r2 | Approved (two-step KDF, SP 800-56C r2) | Not CNSA 2.0 (SHA-384+ required) | Generic quantum speed-up only (Grover/BHT) | - |
| `pbkdf2-hmac-sha256` | - | - | SP 800-132; RFC 8018 | Approved (SP 800-132); 80,000 iterations is below the OWASP 2023 figure of 600,000 | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Strength is bounded by password entropy, so no fixed security level is assigned. |
| `scrypt` | - | - | RFC 7914 | Not NIST-approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Memory-hard password KDF (internally PBKDF2-HMAC-SHA256 + Salsa20/8). |
| `argon2id` | - | - | RFC 9106 | Not NIST-approved (OWASP first choice for password storage) | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | No standard OID is assigned. Internally uses BLAKE2b. |
| `bcrypt` | - | - | Provos & Mazieres, USENIX 1999 | Not NIST-approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Eksblowfish-based password hash; passwords truncated at 72 bytes. |
| `aes-256-gcm` | 256 | 5 | FIPS 197; SP 800-38D | Approved | CNSA 2.0 compliant (AES-256) | Generic quantum speed-up only (Grover/BHT) | 128-bit tag, 96-bit IV. Hard-coded key/IV in S11 are a published test vector. |
| `aes-128-gcm` | 128 | 1 | FIPS 197; SP 800-38D | Approved | Not CNSA 2.0 (AES-256 required) | Generic quantum speed-up only (Grover/BHT) | Only implicit: TLS_AES_128_GCM_SHA256 cipher suite (S24). |
| `chacha20-poly1305` | 256 | 5 | RFC 8439 | Not NIST-approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Stream-cipher AEAD; mode reported as 'other'. |
| `aes-256-cbc` | 256 | 5 | FIPS 197; SP 800-38A | Approved mode; unauthenticated (padding-oracle risk without a MAC) | AES-256 meets CNSA 2.0 key size | Generic quantum speed-up only (Grover/BHT) | - |
| `aes-128-ecb` | 128 | 1 | FIPS 197; SP 800-38A | Approved block cipher, but ECB leaks plaintext block equality - flag as weak mode | Not CNSA 2.0 (AES-256 required) | Generic quantum speed-up only (Grover/BHT) | - |
| `aes-256-ctr` | 256 | 5 | FIPS 197; SP 800-38A | Approved mode; unauthenticated | AES-256 meets CNSA 2.0 key size | Generic quantum speed-up only (Grover/BHT) | No NIST OID is registered for AES-CTR. |
| `3des-cbc` | 112 | 0 | SP 800-67 r2 (withdrawn 2024-01-01); SP 800-38A | Disallowed for encryption after 2023-12-31 (SP 800-131A r2); decryption legacy-use only | Not CNSA 2.0 | Below NIST category 1 (112-bit classical) | 64-bit block size (Sweet32 birthday bound). |
| `rsa-3072` | 128 | 0 | FIPS 186-5; RFC 8017 | Acceptable; quantum-vulnerable - disallowed after 2035 (NIST IR 8547) | CNSA 1.0 only (>=3072); not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | The same key pair is used for encryption (OAEP) and two signature schemes - a key-separation finding (SP 800-57 Pt 1 section 5.2). |
| `mgf1-sha256` | - | - | RFC 8017 | Approved (as part of OAEP/PSS) | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | - |
| `rsa-oaep-sha256` | 128 | 0 | RFC 8017; SP 800-56B r2 | Approved; quantum-vulnerable (IR 8547) | CNSA 1.0 only | Broken by Shor's algorithm on a CRQC | Label hash SHA-256 and MGF1 hash SHA-256, empty label. |
| `rsassa-pss-sha256` | 128 | 0 | RFC 8017; FIPS 186-5 | Approved; quantum-vulnerable (IR 8547) | CNSA 1.0 only | Broken by Shor's algorithm on a CRQC | CycloneDX has no 'pss' padding value, so padding='other'. Salt length 32, trailer 0xBC. |
| `rsassa-pkcs1v15-sha256` | 128 | 0 | RFC 8017; FIPS 186-5 | Approved; quantum-vulnerable (IR 8547) | CNSA 1.0 only | Broken by Shor's algorithm on a CRQC | - |
| `ecdsa-p256-sha256` | 128 | 0 | FIPS 186-5; SP 800-186 | Approved; quantum-vulnerable (IR 8547) | Not CNSA (P-384 required) | Broken by Shor's algorithm on a CRQC | - |
| `ecdh-p256` | 128 | 0 | SP 800-56A r3; SP 800-186 | Approved; quantum-vulnerable (IR 8547) | Not CNSA (P-384 required) | Broken by Shor's algorithm on a CRQC | - |
| `x25519` | 128 | 0 | RFC 7748 | Not listed in SP 800-56A r3 | Not CNSA | Broken by Shor's algorithm on a CRQC | - |
| `ed25519` | 128 | 0 | RFC 8032; FIPS 186-5 | Approved (FIPS 186-5); quantum-vulnerable (IR 8547) | Not CNSA | Broken by Shor's algorithm on a CRQC | SHA-512 is used internally (implicit). |
| `ml-kem-768` | 192 | 3 | FIPS 203 | Approved | Not CNSA 2.0 (ML-KEM-1024 required) | Designed to resist CRQC | Uses SHA3/SHAKE internally (implicit). |
| `ml-dsa-65` | 192 | 3 | FIPS 204 | Approved | Not CNSA 2.0 (ML-DSA-87 required) | Designed to resist CRQC | Hedged (randomized) signing, empty context string. |
| `csprng` | - | - | SP 800-90A r1 / OS RNG (implementation-specific) | Depends on implementation (see per-language notes) | n/a | Not applicable | Implementation differs per runtime; see the language README. |

Occurrences per algorithm (`direct` = the span names this asset; `parameter:x` = span names x inside this composite; `produced` = span produces this material):

| Asset | Occurrence IDs |
|---|---|
| `sha-256` | PY-039, PY-054, PY-056, PY-060, PY-134, PY-135, PY-140, PY-143, PY-145, PY-148, PY-150, PY-155, PY-158, PY-163, PY-190 |
| `sha-512` | PY-040 |
| `sha3-256` | PY-041 |
| `blake2b-512` | PY-042, PY-043, PY-044, PY-045 |
| `md5` | PY-046, PY-047 |
| `sha-1` | PY-048, PY-049, PY-050 |
| `shake128` | PY-051, PY-052 |
| `hmac-sha256` | PY-053, PY-054 (parameter:sha-256) |
| `hkdf-sha256` | PY-055, PY-056 (parameter:sha-256), PY-057, PY-058, PY-162, PY-163 (parameter:sha-256), PY-164, PY-165 |
| `pbkdf2-hmac-sha256` | PY-059, PY-060 (parameter:sha-256), PY-061, PY-062 |
| `scrypt` | PY-063, PY-064, PY-065, PY-066, PY-067, PY-068 |
| `argon2id` | PY-069, PY-070, PY-071, PY-072, PY-073, PY-074 |
| `bcrypt` | PY-076, PY-077, PY-078 |
| `aes-256-gcm` | PY-079, PY-080, PY-081 |
| `chacha20-poly1305` | PY-086, PY-087, PY-088, PY-089 |
| `aes-256-cbc` | PY-094, PY-095, PY-096, PY-097, PY-098, PY-099, PY-100 |
| `aes-128-ecb` | PY-101, PY-102, PY-103, PY-104, PY-105 |
| `aes-256-ctr` | PY-110, PY-111, PY-112, PY-113, PY-114, PY-115 |
| `3des-cbc` | PY-116, PY-121, PY-122, PY-123, PY-124, PY-125, PY-126, PY-127, PY-128 |
| `rsa-3072` | PY-129, PY-130, PY-131 |
| `mgf1-sha256` | PY-133, PY-134 (parameter:sha-256), PY-139, PY-140 (parameter:sha-256) |
| `rsa-oaep-sha256` | PY-132, PY-133 (parameter:mgf1-sha256), PY-135 (parameter:sha-256), PY-136, PY-137 |
| `rsassa-pss-sha256` | PY-138, PY-139 (parameter:mgf1-sha256), PY-141, PY-142, PY-143 (parameter:sha-256), PY-144, PY-145 (parameter:sha-256) |
| `rsassa-pkcs1v15-sha256` | PY-146, PY-147, PY-148 (parameter:sha-256), PY-149, PY-150 (parameter:sha-256) |
| `ecdsa-p256-sha256` | PY-151, PY-152, PY-153, PY-154, PY-155 (parameter:sha-256), PY-156, PY-157, PY-158 (parameter:sha-256), PY-184, PY-185, PY-190 (parameter:sha-256), PY-191, PY-192 |
| `ecdh-p256` | PY-170, PY-171, PY-172, PY-173, PY-174, PY-175, PY-176, PY-177 |
| `x25519` | PY-166, PY-167, PY-168, PY-169 |
| `ed25519` | PY-159, PY-160, PY-161 |
| `ml-kem-768` | PY-178, PY-179, PY-180 |
| `ml-dsa-65` | PY-181, PY-182, PY-183 |
| `csprng` | PY-075, PY-082, PY-084, PY-090, PY-092, PY-106, PY-108, PY-117, PY-119, PY-187 |
| `cert.self-signed` | PY-186, PY-188, PY-189 |
| `tls13-client` | PY-193, PY-194, PY-195 |

## Certificate and protocol assets

| Property | Value |
|---|---|
| Asset | `cert.self-signed` |
| Format | X.509 v3 |
| Subject / issuer | CN=cbom-corpus.example / CN=cbom-corpus.example |
| Signature algorithm | `ecdsa-p256-sha256` |
| Subject public key | `m.cert-public-key` |
| Validity | runtime: now - 1 minute to runtime: now + 365 days |
| Serial | 64-bit random from the CSPRNG |
| Occurrences | PY-186, PY-188, PY-189 |

| Property | Value |
|---|---|
| Asset | `tls13-client` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_128_GCM_SHA256 (0x13,0x01); TLS_AES_256_GCM_SHA384 (0x13,0x02); TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03) |
| Note | Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime defaults. |
| Occurrences | PY-193, PY-194, PY-195 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Provenance | Test-vector value | Used with | Scenario | Defined / produced at | Note |
|---|---|---|---|---|---|---|---|---|---|
| `m.hmac-key` | HMAC key | secret-key | 24 | hardcoded | "key" (ASCII) | `hmac-sha256` | S05 | PY-023 @ 44:1 | 24-bit key - far below the 112-bit minimum; test vector only |
| `m.hkdf-ikm` | HKDF input keying material | secret-key | 176 | hardcoded | 0x0b * 22 | `hkdf-sha256` | S06 | PY-024 @ 45:1 | RFC 5869 A.1 |
| `m.hkdf-salt` | HKDF salt | salt | 104 | hardcoded | 000102...0c | `hkdf-sha256` | S06 | PY-025 @ 46:1 | RFC 5869 A.1 |
| `m.hkdf-info` | HKDF info | additional-data | 80 | hardcoded | f0f1...f9 | `hkdf-sha256` | S06 | PY-026 @ 47:1 | RFC 5869 A.1 |
| `m.hkdf-okm` | HKDF output keying material | secret-key | 336 | derived | - | `hkdf-sha256` | S06 | PY-058 @ 127:32 (produced) | - |
| `m.pbkdf2-password` | PBKDF2 password | password | 64 | hardcoded | "Password" | `pbkdf2-hmac-sha256` | S07 | PY-027 @ 48:1 | RFC 7914 section 11 |
| `m.pbkdf2-salt` | PBKDF2 salt | salt | 32 | hardcoded | "NaCl" | `pbkdf2-hmac-sha256` | S07 | PY-028 @ 49:1 | 32-bit salt is below the SP 800-132 minimum of 128 bits |
| `m.pbkdf2-dk` | PBKDF2 derived key | secret-key | 512 | derived | - | `pbkdf2-hmac-sha256` | S07 | PY-059 @ 132:15 (produced) | - |
| `m.scrypt-password` | scrypt password | password | 104 | hardcoded | "pleaseletmein" | `scrypt` | S08 | PY-029 @ 50:1 | RFC 7914 section 12 |
| `m.scrypt-salt` | scrypt salt | salt | 112 | hardcoded | "SodiumChloride" | `scrypt` | S08 | PY-030 @ 51:1 | - |
| `m.scrypt-dk` | scrypt derived key | secret-key | 512 | derived | - | `scrypt` | S08 | PY-068 @ 141:27 (produced) | - |
| `m.password` | Application password | password | 224 | hardcoded | "correct horse battery staple" | `argon2id` | S09 | PY-031 @ 52:1 | Shared by S09 (Argon2id) and S10 (bcrypt) |
| `m.argon2-salt` | Argon2id salt | salt | 128 | hardcoded | "cbom-corpus-salt" | `argon2id` | S09 | PY-032 @ 53:1 | - |
| `m.argon2-dk` | Argon2id output | secret-key | 256 | derived | - | `argon2id` | S09 | PY-069 @ 146:11 (produced) | - |
| `m.bcrypt-salt` | bcrypt salt | salt | 128 | csprng | - | `bcrypt` | S10 | PY-075 @ 160:12 (produced) | - |
| `m.bcrypt-hash` | bcrypt hash string | credential | 480 | derived | - | `bcrypt` | S10 | PY-077 @ 161:14 (produced) | 60-character modular-crypt string ($2a$/$2b$) |
| `m.gcm-key` | AES-256-GCM key | secret-key | 256 | hardcoded | feffe992... | `aes-256-gcm` | S11 | PY-033 @ 54:1 | GCM spec test case 16 |
| `m.gcm-iv` | AES-GCM IV | nonce | 96 | hardcoded | cafebabefacedbaddecaf888 | `aes-256-gcm` | S11 | PY-034 @ 55:1 | Static nonce - reuse with the same key is catastrophic outside a KAT |
| `m.gcm-aad` | AES-GCM additional authenticated data | additional-data | 160 | hardcoded | feedface... | `aes-256-gcm` | S11 | PY-035 @ 56:1 | GCM spec test case 16 |
| `m.chacha-key` | ChaCha20-Poly1305 key | secret-key | 256 | csprng | - | `chacha20-poly1305` | S12 | PY-082 @ 177:11 (produced); PY-083 @ 177:28 | - |
| `m.chacha-nonce` | ChaCha20-Poly1305 nonce | nonce | 96 | csprng | - | `chacha20-poly1305` | S12 | PY-084 @ 178:13 (produced); PY-085 @ 178:30 | - |
| `m.cbc-key` | AES-256-CBC key | secret-key | 256 | csprng | - | `aes-256-cbc` | S13 | PY-090 @ 188:11 (produced); PY-091 @ 188:22 | - |
| `m.cbc-iv` | AES-CBC IV | initialization-vector | 128 | csprng | - | `aes-256-cbc` | S13 | PY-092 @ 189:10 (produced); PY-093 @ 189:21 | - |
| `m.ecb-key` | AES-128-ECB key | secret-key | 128 | hardcoded | 000102...0f | `aes-128-ecb` | S14 | PY-036 @ 61:1 | FIPS 197 appendix C.1 |
| `m.ctr-key` | AES-256-CTR key | secret-key | 256 | csprng | - | `aes-256-ctr` | S15 | PY-106 @ 212:11 (produced); PY-107 @ 212:31 | - |
| `m.ctr-iv` | AES-CTR initial counter block | initialization-vector | 128 | csprng | - | `aes-256-ctr` | S15 | PY-108 @ 213:21 (produced); PY-109 @ 213:41 | - |
| `m.tdes-key` | 3DES key | secret-key | 192 | csprng | - | `3des-cbc` | S16 | PY-116 @ 223:11 (produced); PY-118 @ 223:51 | 192 bits incl. parity = 168 effective |
| `m.tdes-iv` | 3DES IV | initialization-vector | 64 | csprng | - | `3des-cbc` | S16 | PY-119 @ 224:10 (produced); PY-120 @ 224:27 | - |
| `m.rsa-private-key` | RSA-3072 private key | private-key | 3072 | keygen | - | `rsa-3072` | S17 | PY-129 @ 234:19 (produced) | - |
| `m.rsa-public-key` | RSA-3072 public key | public-key | 3072 | keygen | - | `rsa-3072` | S17 | PY-129 @ 234:19 (produced) | e = 65537 |
| `m.ecdsa-private-key` | ECDSA P-256 private key | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | PY-151 @ 262:19 (produced) | - |
| `m.ecdsa-public-key` | ECDSA P-256 public key | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | PY-151 @ 262:19 (produced) | - |
| `m.ed25519-seed` | Ed25519 private key seed | private-key | 256 | hardcoded | 9d61b19d... | `ed25519` | S19 | PY-037 @ 63:1 | RFC 8032 section 7.1 TEST 1 |
| `m.ed25519-public-key` | Ed25519 public key | public-key | 256 | derived | d75a9801... | `ed25519` | S19 | PY-159 @ 270:19 (produced) | Derived from the seed |
| `m.x25519-private-key-a` | X25519 private key (party A) | private-key | 256 | keygen | - | `x25519` | S20 | PY-166 @ 284:13 (produced) | - |
| `m.x25519-private-key-b` | X25519 private key (party B) | private-key | 256 | keygen | - | `x25519` | S20 | PY-167 @ 285:11 (produced) | - |
| `m.x25519-shared-secret` | X25519 shared secret | shared-secret | 256 | agreed | - | `x25519` | S20 | PY-168 @ 286:15 (produced); PY-169 @ 287:13 (produced) | - |
| `m.ecdh-private-key-a` | ECDH P-256 private key (party A) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | PY-170 @ 290:16 (produced) | - |
| `m.ecdh-private-key-b` | ECDH P-256 private key (party B) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | PY-172 @ 291:14 (produced) | - |
| `m.ecdh-shared-secret` | ECDH P-256 shared secret | shared-secret | 256 | agreed | - | `ecdh-p256` | S20 | PY-174 @ 292:15 (produced); PY-176 @ 293:13 (produced) | - |
| `m.session-info` | Session-key HKDF info | additional-data | 208 | hardcoded | "cbom-corpus session key v1" | `hkdf-sha256` | S20 | PY-038 @ 64:1 | - |
| `m.session-key` | Session key (HKDF over X25519 || ECDH secrets) | secret-key | 256 | derived | - | `hkdf-sha256` | S20 | PY-165 @ 279:12 (produced) | - |
| `m.mlkem-decapsulation-key` | ML-KEM-768 decapsulation key | private-key | - | keygen | - | `ml-kem-768` | S21 | PY-178 @ 303:25 (produced) | 64-byte seed form or 2400-byte expanded form, library-dependent |
| `m.mlkem-encapsulation-key` | ML-KEM-768 encapsulation key | public-key | 9472 | keygen | - | `ml-kem-768` | S21 | PY-178 @ 303:25 (produced) | 1184 bytes |
| `m.mlkem-shared-secret` | ML-KEM-768 shared secret | shared-secret | 256 | agreed | - | `ml-kem-768` | S21 | PY-179 @ 305:33 (produced); PY-180 @ 306:17 (produced) | - |
| `m.mldsa-private-key` | ML-DSA-65 private key | private-key | - | keygen | - | `ml-dsa-65` | S22 | PY-181 @ 312:19 (produced) | 32-byte seed or 4032-byte expanded form, library-dependent |
| `m.mldsa-public-key` | ML-DSA-65 public key | public-key | 15616 | keygen | - | `ml-dsa-65` | S22 | PY-181 @ 312:19 (produced) | 1952 bytes |
| `m.cert-private-key` | Certificate private key (P-256) | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | PY-184 @ 320:11 (produced) | - |
| `m.cert-public-key` | Certificate subject public key (P-256) | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | PY-184 @ 320:11 (produced) | - |

## Scenario map

| Scenario | What it does | Output | Occurrences | Lines | Assets |
|---|---|---|---|---|---|
| S01 | SHA-256 digest of MESSAGE | Known answer (Wikipedia / NIST example message) | 1 | 86-86 | `sha-256` |
| S02 | SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | Known answers | 6 | 91-95 | `sha-512`, `sha3-256`, `blake2b-512` |
| S03 | Legacy MD5 and SHA-1 digests of MESSAGE | Known answers; deliberately weak algorithms | 5 | 100-104 | `md5`, `sha-1` |
| S04 | SHAKE128 XOF, 32-byte output | Known answer | 2 | 109-110 | `shake128` |
| S05 | HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | Known answer (Wikipedia HMAC example) | 3 | 44-115 | `sha-256`, `hmac-sha256`, `m.hmac-key` |
| S06 | HKDF-SHA256 extract-and-expand, L=42 | Known answer (RFC 5869 A.1) | 7 | 45-127 | `sha-256`, `hkdf-sha256`, `m.hkdf-ikm`, `m.hkdf-salt`, `m.hkdf-info`, `m.hkdf-okm` |
| S07 | PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | Known answer (RFC 7914 section 11) | 6 | 48-134 | `sha-256`, `pbkdf2-hmac-sha256`, `m.pbkdf2-password`, `m.pbkdf2-salt`, `m.pbkdf2-dk` |
| S08 | scrypt N=16384 r=8 p=1, dkLen=64 | Known answer (RFC 7914 section 12) | 8 | 50-141 | `scrypt`, `m.scrypt-password`, `m.scrypt-salt`, `m.scrypt-dk` |
| S09 | Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | Deterministic; identical across languages | 8 | 52-154 | `argon2id`, `m.password`, `m.argon2-salt`, `m.argon2-dk` |
| S10 | bcrypt cost 12 with random salt, then verify | Randomized; prints verify=true | 4 | 160-162 | `bcrypt`, `csprng`, `m.bcrypt-salt`, `m.bcrypt-hash` |
| S11 | AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | Known answer (GCM spec test case 16) | 6 | 54-171 | `aes-256-gcm`, `m.gcm-key`, `m.gcm-iv`, `m.gcm-aad` |
| S12 | ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | Randomized round trip | 8 | 177-182 | `chacha20-poly1305`, `csprng`, `m.chacha-key`, `m.chacha-nonce` |
| S13 | AES-256-CBC with PKCS#7 padding, random key and IV | Randomized round trip | 11 | 188-196 | `aes-256-cbc`, `csprng`, `m.cbc-key`, `m.cbc-iv` |
| S14 | AES-128-ECB with PKCS#7 padding, hard-coded key | Known answer: first block = FIPS 197 C.1 | 6 | 61-206 | `aes-128-ecb`, `m.ecb-key` |
| S15 | AES-256-CTR, random key and 128-bit initial counter block | Randomized round trip | 10 | 212-217 | `aes-256-ctr`, `csprng`, `m.ctr-key`, `m.ctr-iv` |
| S16 | 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | Randomized round trip | 13 | 223-228 | `3des-cbc`, `csprng`, `m.tdes-key`, `m.tdes-iv` |
| S17 | RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | Randomized | 22 | 234-256 | `sha-256`, `rsa-3072`, `mgf1-sha256`, `rsa-oaep-sha256`, `rsassa-pss-sha256`, `rsassa-pkcs1v15-sha256`, `m.rsa-private-key`, `m.rsa-public-key` |
| S18 | ECDSA P-256 / SHA-256 sign and verify | Randomized | 8 | 262-264 | `sha-256`, `ecdsa-p256-sha256`, `m.ecdsa-private-key`, `m.ecdsa-public-key` |
| S19 | Ed25519 from a hard-coded seed: public key, signature, verify | Known public key (RFC 8032 test 1); deterministic signature | 4 | 63-273 | `ed25519`, `m.ed25519-seed`, `m.ed25519-public-key` |
| S20 | X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | Randomized; prints agreement booleans | 17 | 64-293 | `sha-256`, `hkdf-sha256`, `ecdh-p256`, `x25519`, `m.x25519-private-key-a`, `m.x25519-private-key-b`, `m.x25519-shared-secret`, `m.ecdh-private-key-a`, `m.ecdh-private-key-b`, `m.ecdh-shared-secret`, `m.session-info`, `m.session-key` |
| S21 | ML-KEM-768 key generation, encapsulation, decapsulation | Randomized; prints sizes | 3 | 303-306 | `ml-kem-768`, `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key`, `m.mlkem-shared-secret` |
| S22 | ML-DSA-65 key generation, signing, verification | Randomized; prints signature size | 3 | 312-314 | `ml-dsa-65`, `m.mldsa-private-key`, `m.mldsa-public-key` |
| S23 | Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | Randomized | 9 | 320-338 | `sha-256`, `ecdsa-p256-sha256`, `csprng`, `cert.self-signed`, `m.cert-private-key`, `m.cert-public-key` |
| S24 | TLS 1.3-only client configuration (no network I/O) | Configuration only | 3 | 345-347 | `tls13-client` |

## Occurrence ledger

Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.

| ID | Scn | Role | Asset (^parent) | Start L:C | End L:C | Chars | Bytes | Len | Nest | Scope | API symbol | Library | Produces | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PY-001 | - | `imp` | `lib.py-stdlib` | 14:1 | 14:15 | [495, 509) | [495, 509) | 14 | 0 | `<module>` | `hashlib` | `lib.py-stdlib` | - | `import hashlib` | - |
| PY-002 | - | `imp` | `lib.py-stdlib` | 15:1 | 15:12 | [510, 521) | [510, 521) | 11 | 0 | `<module>` | `hmac` | `lib.py-stdlib` | - | `import hmac` | - |
| PY-003 | - | `imp` | `lib.py-stdlib` | 17:1 | 17:15 | [532, 546) | [532, 546) | 14 | 0 | `<module>` | `secrets` | `lib.py-stdlib` | - | `import secrets` | - |
| PY-004 | - | `imp` | `lib.py-stdlib` | 18:1 | 18:11 | [547, 557) | [547, 557) | 10 | 0 | `<module>` | `ssl` | `lib.py-stdlib` | - | `import ssl` | - |
| PY-005 | - | `imp` | `lib.argon2-cffi` | 22:1 | 22:51 | [638, 688) | [638, 688) | 50 | 0 | `<module>` | `argon2.low_level` | `lib.argon2-cffi` | - | `from argon2.low_level import Type, hash_secret_raw` | - |
| PY-006 | - | `imp` | `lib.bcrypt` | 23:1 | 23:14 | [689, 702) | [689, 702) | 13 | 0 | `<module>` | `bcrypt` | `lib.bcrypt` | - | `import bcrypt` | - |
| PY-007 | - | `imp` | `lib.pycryptodome` | 24:1 | 24:55 | [703, 757) | [703, 757) | 54 | 0 | `<module>` | `Crypto.Cipher` | `lib.pycryptodome` | - | `from Crypto.Cipher import AES, DES3, ChaCha20_Poly1305` | - |
| PY-008 | - | `imp` | `lib.pycryptodome` | 25:1 | 25:33 | [758, 790) | [758, 790) | 32 | 0 | `<module>` | `Crypto.Hash` | `lib.pycryptodome` | - | `from Crypto.Hash import SHA3_256` | - |
| PY-009 | - | `imp` | `lib.pycryptodome` | 26:1 | 26:43 | [791, 833) | [791, 833) | 42 | 0 | `<module>` | `Crypto.Random` | `lib.pycryptodome` | - | `from Crypto.Random import get_random_bytes` | - |
| PY-010 | - | `imp` | `lib.pycryptodome` | 27:1 | 27:43 | [834, 876) | [834, 876) | 42 | 0 | `<module>` | `Crypto.Util.Padding` | `lib.pycryptodome` | - | `from Crypto.Util.Padding import pad, unpad` | - |
| PY-011 | - | `imp` | `lib.pyca` | 28:1 | 28:30 | [877, 906) | [877, 906) | 29 | 0 | `<module>` | `cryptography.x509` | `lib.pyca` | - | `from cryptography import x509` | - |
| PY-012 | - | `imp` | `lib.pyca` | 29:1 | 29:53 | [907, 959) | [907, 959) | 52 | 0 | `<module>` | `cryptography.exceptions` | `lib.pyca` | - | `from cryptography.exceptions import InvalidSignature` | - |
| PY-013 | - | `imp` | `lib.pyca` | 30:1 | 30:59 | [960, 1018) | [960, 1018) | 58 | 0 | `<module>` | `cryptography.hazmat.primitives` | `lib.pyca` | - | `from cryptography.hazmat.primitives import hashes, padding` | - |
| PY-014 | - | `imp` | `lib.pyca` | 31:1 | 31:84 | [1019, 1102) | [1019, 1102) | 83 | 0 | `<module>` | `cryptography.hazmat.primitives.asymmetric` | `lib.pyca` | - | `from cryptography.hazmat.primitives.asymmetric import ec, mldsa, mlkem, rsa, x25519` | - |
| PY-015 | - | `imp` | `lib.pyca` | 32:1 | 32:78 | [1103, 1180) | [1103, 1180) | 77 | 0 | `<module>` | `cryptography.hazmat.primitives.asymmetric.padding` | `lib.pyca` | - | `from cryptography.hazmat.primitives.asymmetric import padding as asym_padding` | - |
| PY-016 | - | `imp` | `lib.pyca` | 33:1 | 33:77 | [1181, 1257) | [1181, 1257) | 76 | 0 | `<module>` | `cryptography.hazmat.primitives.ciphers` | `lib.pyca` | - | `from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes` | - |
| PY-017 | - | `imp` | `lib.pyca` | 34:1 | 34:63 | [1258, 1320) | [1258, 1320) | 62 | 0 | `<module>` | `cryptography.hazmat.primitives.ciphers.aead` | `lib.pyca` | - | `from cryptography.hazmat.primitives.ciphers.aead import AESGCM` | - |
| PY-018 | - | `imp` | `lib.pyca` | 35:1 | 35:57 | [1321, 1377) | [1321, 1377) | 56 | 0 | `<module>` | `cryptography.hazmat.primitives.kdf.hkdf` | `lib.pyca` | - | `from cryptography.hazmat.primitives.kdf.hkdf import HKDF` | - |
| PY-019 | - | `imp` | `lib.pyca` | 36:1 | 36:61 | [1378, 1438) | [1378, 1438) | 60 | 0 | `<module>` | `cryptography.hazmat.primitives.kdf.scrypt` | `lib.pyca` | - | `from cryptography.hazmat.primitives.kdf.scrypt import Scrypt` | - |
| PY-020 | - | `imp` | `lib.pyca` | 37:1 | 37:42 | [1439, 1480) | [1439, 1480) | 41 | 0 | `<module>` | `cryptography.x509.oid` | `lib.pyca` | - | `from cryptography.x509.oid import NameOID` | - |
| PY-021 | - | `imp` | `lib.pynacl` | 38:1 | 38:46 | [1481, 1526) | [1481, 1526) | 45 | 0 | `<module>` | `nacl.exceptions` | `lib.pynacl` | - | `from nacl.exceptions import BadSignatureError` | - |
| PY-022 | - | `imp` | `lib.pynacl` | 39:1 | 39:36 | [1527, 1562) | [1527, 1562) | 35 | 0 | `<module>` | `nacl.signing` | `lib.pynacl` | - | `from nacl.signing import SigningKey` | - |
| PY-023 | S05 | `mat` | `m.hmac-key` | 44:1 | 44:18 | [1703, 1720) | [1703, 1720) | 17 | 0 | `<module>` | - | `lib.py-stdlib` | - | `HMAC_KEY = b"key"` | - |
| PY-024 | S06 | `mat` | `m.hkdf-ikm` | 45:1 | 45:36 | [1751, 1786) | [1751, 1786) | 35 | 0 | `<module>` | - | `lib.py-stdlib` | - | `HKDF_IKM = bytes.fromhex("0b" * 22)` | - |
| PY-025 | S06 | `mat` | `m.hkdf-salt` | 46:1 | 46:56 | [1803, 1858) | [1803, 1858) | 55 | 0 | `<module>` | - | `lib.py-stdlib` | - | `HKDF_SALT = bytes.fromhex("000102030405060708090a0b0c")` | - |
| PY-026 | S06 | `mat` | `m.hkdf-info` | 47:1 | 47:50 | [1859, 1908) | [1859, 1908) | 49 | 0 | `<module>` | - | `lib.py-stdlib` | - | `HKDF_INFO = bytes.fromhex("f0f1f2f3f4f5f6f7f8f9")` | - |
| PY-027 | S07 | `mat` | `m.pbkdf2-password` | 48:1 | 48:30 | [1909, 1938) | [1909, 1938) | 29 | 0 | `<module>` | - | `lib.py-stdlib` | - | `PBKDF2_PASSWORD = b"Password"` | - |
| PY-028 | S07 | `mat` | `m.pbkdf2-salt` | 49:1 | 49:22 | [1962, 1983) | [1962, 1983) | 21 | 0 | `<module>` | - | `lib.py-stdlib` | - | `PBKDF2_SALT = b"NaCl"` | - |
| PY-029 | S08 | `mat` | `m.scrypt-password` | 50:1 | 50:35 | [1984, 2018) | [1984, 2018) | 34 | 0 | `<module>` | - | `lib.py-stdlib` | - | `SCRYPT_PASSWORD = b"pleaseletmein"` | - |
| PY-030 | S08 | `mat` | `m.scrypt-salt` | 51:1 | 51:32 | [2042, 2073) | [2042, 2073) | 31 | 0 | `<module>` | - | `lib.py-stdlib` | - | `SCRYPT_SALT = b"SodiumChloride"` | - |
| PY-031 | S09 | `mat` | `m.password` | 52:1 | 52:43 | [2074, 2116) | [2074, 2116) | 42 | 0 | `<module>` | - | `lib.py-stdlib` | - | `PASSWORD = b"correct horse battery staple"` | - |
| PY-032 | S09 | `mat` | `m.argon2-salt` | 53:1 | 53:34 | [2117, 2150) | [2117, 2150) | 33 | 0 | `<module>` | - | `lib.py-stdlib` | - | `ARGON2_SALT = b"cbom-corpus-salt"` | - |
| PY-033 | S11 | `mat` | `m.gcm-key` | 54:1 | 54:92 | [2151, 2242) | [2151, 2242) | 91 | 0 | `<module>` | - | `lib.py-stdlib` | - | `GCM_KEY = bytes.fromhex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")` | - |
| PY-034 | S11 | `mat` | `m.gcm-iv` | 55:1 | 55:51 | [2243, 2293) | [2243, 2293) | 50 | 0 | `<module>` | - | `lib.py-stdlib` | - | `GCM_IV = bytes.fromhex("cafebabefacedbaddecaf888")` | - |
| PY-035 | S11 | `mat` | `m.gcm-aad` | 56:1 | 56:68 | [2294, 2361) | [2294, 2361) | 67 | 0 | `<module>` | - | `lib.py-stdlib` | - | `GCM_AAD = bytes.fromhex("feedfacedeadbeeffeedfacedeadbeefabaddad2")` | - |
| PY-036 | S14 | `mat` | `m.ecb-key` | 61:1 | 61:60 | [2529, 2588) | [2529, 2588) | 59 | 0 | `<module>` | - | `lib.py-stdlib` | - | `ECB_KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")` | - |
| PY-037 | S19 | `mat` | `m.ed25519-seed` | 63:1 | 63:97 | [2680, 2776) | [2680, 2776) | 96 | 0 | `<module>` | - | `lib.py-stdlib` | - | `ED25519_SEED = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")` | - |
| PY-038 | S20 | `mat` | `m.session-info` | 64:1 | 64:45 | [2777, 2821) | [2777, 2821) | 44 | 0 | `<module>` | - | `lib.py-stdlib` | - | `SESSION_INFO = b"cbom-corpus session key v1"` | - |
| PY-039 | S01 | `op:digest` | `sha-256` | 86:28 | 86:51 | [3282, 3305) | [3282, 3305) | 23 | 0 | `s01_sha256` | `hashlib.sha256` | `lib.py-stdlib` | - | `hashlib.sha256(MESSAGE)` | - |
| PY-040 | S02 | `op:digest` | `sha-512` | 91:28 | 91:51 | [3422, 3445) | [3422, 3445) | 23 | 0 | `s02_sha2_sha3_blake2` | `hashlib.sha512` | `lib.py-stdlib` | - | `hashlib.sha512(MESSAGE)` | - |
| PY-041 | S02 | `op:digest` | `sha3-256` | 92:29 | 92:50 | [3487, 3508) | [3487, 3508) | 21 | 0 | `s02_sha2_sha3_blake2` | `Crypto.Hash.SHA3_256.new` | `lib.pycryptodome` | - | `SHA3_256.new(MESSAGE)` | - |
| PY-042 | S02 | `ctor` | `blake2b-512` | 93:13 | 93:44 | [3534, 3565) | [3534, 3565) | 31 | 0 | `s02_sha2_sha3_blake2` | `cryptography.hazmat.primitives.hashes.Hash` | `lib.pyca` | - | `hashes.Hash(hashes.BLAKE2b(64))` | - |
| PY-043 | S02 | `alg` | `blake2b-512` | 93:25 | 93:43 | [3546, 3564) | [3546, 3564) | 18 | 1 | `s02_sha2_sha3_blake2` | `cryptography.hazmat.primitives.hashes.BLAKE2b` | `lib.pyca` | - | `hashes.BLAKE2b(64)` | - |
| PY-044 | S02 | `prm:digest-size-bytes` | `blake2b-512` | 93:40 | 93:42 | [3561, 3563) | [3561, 3563) | 2 | 2 | `s02_sha2_sha3_blake2` | - | `lib.pyca` | - | `64` | - |
| PY-045 | S02 | `op:digest` | `blake2b-512` | 95:32 | 95:48 | [3623, 3639) | [3623, 3639) | 16 | 0 | `s02_sha2_sha3_blake2` | `cryptography.hazmat.primitives.hashes.Hash.finalize` | `lib.pyca` | - | `blake.finalize()` | - |
| PY-046 | S03 | `op:digest` | `md5` | 100:11 | 100:54 | [3734, 3777) | [3734, 3777) | 43 | 0 | `s03_legacy_hashes` | `hashlib.md5` | `lib.py-stdlib` | - | `hashlib.md5(MESSAGE, usedforsecurity=False)` | - |
| PY-047 | S03 | `prm:usedforsecurity` | `md5` | 100:32 | 100:53 | [3755, 3776) | [3755, 3776) | 21 | 1 | `s03_legacy_hashes` | - | `lib.py-stdlib` | - | `usedforsecurity=False` | usedforsecurity |
| PY-048 | S03 | `ctor` | `sha-1` | 102:12 | 102:38 | [3829, 3855) | [3829, 3855) | 26 | 0 | `s03_legacy_hashes` | `cryptography.hazmat.primitives.hashes.Hash` | `lib.pyca` | - | `hashes.Hash(hashes.SHA1())` | - |
| PY-049 | S03 | `alg` | `sha-1` | 102:24 | 102:37 | [3841, 3854) | [3841, 3854) | 13 | 1 | `s03_legacy_hashes` | `cryptography.hazmat.primitives.hashes.SHA1` | `lib.pyca` | - | `hashes.SHA1()` | - |
| PY-050 | S03 | `op:digest` | `sha-1` | 104:26 | 104:41 | [3906, 3921) | [3906, 3921) | 15 | 0 | `s03_legacy_hashes` | `cryptography.hazmat.primitives.hashes.Hash.finalize` | `lib.pyca` | - | `sha1.finalize()` | - |
| PY-051 | S04 | `op:digest` | `shake128` | 109:11 | 109:37 | [4012, 4038) | [4012, 4038) | 26 | 0 | `s04_shake128` | `hashlib.shake_128` | `lib.py-stdlib` | - | `hashlib.shake_128(MESSAGE)` | - |
| PY-052 | S04 | `prm:output-length-bytes` | `shake128` | 110:43 | 110:45 | [4081, 4083) | [4081, 4083) | 2 | 0 | `s04_shake128` | - | `lib.py-stdlib` | - | `32` | - |
| PY-053 | S05 | `op:tag` | `hmac-sha256` | 115:11 | 115:54 | [4148, 4191) | [4148, 4191) | 43 | 0 | `s05_hmac_sha256` | `hmac.new` | `lib.py-stdlib` | - | `hmac.new(HMAC_KEY, MESSAGE, hashlib.sha256)` | - |
| PY-054 | S05 | `alg` | `sha-256` ^`hmac-sha256` | 115:39 | 115:53 | [4176, 4190) | [4176, 4190) | 14 | 1 | `s05_hmac_sha256` | `hashlib.sha256` | `lib.py-stdlib` | - | `hashlib.sha256` | digestmod |
| PY-055 | S06 | `ctor` | `hkdf-sha256` | 121:12 | 126:6 | [4314, 4427) | [4314, 4427) | 113 | 0 | `s06_hkdf_sha256` | `cryptography.hazmat.primitives.kdf.hkdf.HKDF` | `lib.pyca` | - | `HKDF( … (+5 lines)` | - |
| PY-056 | S06 | `alg` | `sha-256` ^`hkdf-sha256` | 122:19 | 122:34 | [4338, 4353) | [4338, 4353) | 15 | 1 | `s06_hkdf_sha256` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-057 | S06 | `prm:output-length-bytes` | `hkdf-sha256` | 123:16 | 123:18 | [4370, 4372) | [4370, 4372) | 2 | 1 | `s06_hkdf_sha256` | - | `lib.pyca` | - | `42` | - |
| PY-058 | S06 | `op:keyderive` | `hkdf-sha256` | 127:32 | 127:53 | [4459, 4480) | [4459, 4480) | 21 | 0 | `s06_hkdf_sha256` | `cryptography.hazmat.primitives.kdf.hkdf.HKDF.derive` | `lib.pyca` | `m.hkdf-okm` | `hkdf.derive(HKDF_IKM)` | - |
| PY-059 | S07 | `op:keyderive` | `pbkdf2-hmac-sha256` | 132:15 | 134:6 | [4556, 4647) | [4556, 4647) | 91 | 0 | `s07_pbkdf2` | `hashlib.pbkdf2_hmac` | `lib.py-stdlib` | `m.pbkdf2-dk` | `hashlib.pbkdf2_hmac( … (+2 lines)` | - |
| PY-060 | S07 | `alg` | `sha-256` ^`pbkdf2-hmac-sha256` | 133:9 | 133:17 | [4585, 4593) | [4585, 4593) | 8 | 1 | `s07_pbkdf2` | - | `lib.py-stdlib` | - | `"sha256"` | hash-name-string |
| PY-061 | S07 | `prm:iterations` | `pbkdf2-hmac-sha256` | 133:49 | 133:55 | [4625, 4631) | [4625, 4631) | 6 | 1 | `s07_pbkdf2` | - | `lib.py-stdlib` | - | `80_000` | - |
| PY-062 | S07 | `prm:output-length-bytes` | `pbkdf2-hmac-sha256` | 133:63 | 133:65 | [4639, 4641) | [4639, 4641) | 2 | 1 | `s07_pbkdf2` | - | `lib.py-stdlib` | - | `64` | - |
| PY-063 | S08 | `ctor` | `scrypt` | 140:11 | 140:65 | [4748, 4802) | [4748, 4802) | 54 | 0 | `s08_scrypt` | `cryptography.hazmat.primitives.kdf.scrypt.Scrypt` | `lib.pyca` | - | `Scrypt(salt=SCRYPT_SALT, length=64, n=2**14, r=8, p=1)` | - |
| PY-064 | S08 | `prm:output-length-bytes` | `scrypt` | 140:43 | 140:45 | [4780, 4782) | [4780, 4782) | 2 | 1 | `s08_scrypt` | - | `lib.pyca` | - | `64` | - |
| PY-065 | S08 | `prm:N` | `scrypt` | 140:49 | 140:54 | [4786, 4791) | [4786, 4791) | 5 | 1 | `s08_scrypt` | - | `lib.pyca` | - | `2**14` | computed |
| PY-066 | S08 | `prm:r` | `scrypt` | 140:58 | 140:59 | [4795, 4796) | [4795, 4796) | 1 | 1 | `s08_scrypt` | - | `lib.pyca` | - | `8` | - |
| PY-067 | S08 | `prm:p` | `scrypt` | 140:63 | 140:64 | [4800, 4801) | [4800, 4801) | 1 | 1 | `s08_scrypt` | - | `lib.pyca` | - | `1` | - |
| PY-068 | S08 | `op:keyderive` | `scrypt` | 141:27 | 141:54 | [4829, 4856) | [4829, 4856) | 27 | 0 | `s08_scrypt` | `cryptography.hazmat.primitives.kdf.scrypt.Scrypt.derive` | `lib.pyca` | `m.scrypt-dk` | `kdf.derive(SCRYPT_PASSWORD)` | - |
| PY-069 | S09 | `op:keyderive` | `argon2id` | 146:11 | 154:6 | [4920, 5108) | [4920, 5108) | 188 | 0 | `s09_argon2id` | `argon2.low_level.hash_secret_raw` | `lib.argon2-cffi` | `m.argon2-dk` | `hash_secret_raw( … (+8 lines)` | - |
| PY-070 | S09 | `prm:iterations` | `argon2id` | 149:19 | 149:20 | [5006, 5007) | [5006, 5007) | 1 | 1 | `s09_argon2id` | - | `lib.argon2-cffi` | - | `2` | - |
| PY-071 | S09 | `prm:memory-kib` | `argon2id` | 150:21 | 150:27 | [5029, 5035) | [5029, 5035) | 6 | 1 | `s09_argon2id` | - | `lib.argon2-cffi` | - | `19_456` | - |
| PY-072 | S09 | `prm:parallelism` | `argon2id` | 151:21 | 151:22 | [5057, 5058) | [5057, 5058) | 1 | 1 | `s09_argon2id` | - | `lib.argon2-cffi` | - | `1` | - |
| PY-073 | S09 | `prm:output-length-bytes` | `argon2id` | 152:18 | 152:20 | [5077, 5079) | [5077, 5079) | 2 | 1 | `s09_argon2id` | - | `lib.argon2-cffi` | - | `32` | - |
| PY-074 | S09 | `alg` | `argon2id` | 153:14 | 153:21 | [5094, 5101) | [5094, 5101) | 7 | 1 | `s09_argon2id` | `argon2.low_level.Type.ID` | `lib.argon2-cffi` | - | `Type.ID` | - |
| PY-075 | S10 | `op:generate` | `csprng` | 160:12 | 160:37 | [5201, 5226) | [5201, 5226) | 25 | 0 | `s10_bcrypt` | `bcrypt.gensalt` | `lib.bcrypt` | `m.bcrypt-salt` | `bcrypt.gensalt(rounds=12)` | gensalt |
| PY-076 | S10 | `prm:cost` | `bcrypt` | 160:34 | 160:36 | [5223, 5225) | [5223, 5225) | 2 | 1 | `s10_bcrypt` | - | `lib.bcrypt` | - | `12` | cost-in-gensalt |
| PY-077 | S10 | `op:keyderive` | `bcrypt` | 161:14 | 161:43 | [5240, 5269) | [5240, 5269) | 29 | 0 | `s10_bcrypt` | `bcrypt.hashpw` | `lib.bcrypt` | `m.bcrypt-hash` | `bcrypt.hashpw(PASSWORD, salt)` | - |
| PY-078 | S10 | `op:verify` | `bcrypt` | 162:10 | 162:42 | [5279, 5311) | [5279, 5311) | 32 | 0 | `s10_bcrypt` | `bcrypt.checkpw` | `lib.bcrypt` | - | `bcrypt.checkpw(PASSWORD, hashed)` | - |
| PY-079 | S11 | `ctor` | `aes-256-gcm` | 168:12 | 168:27 | [5440, 5455) | [5440, 5455) | 15 | 0 | `s11_aes256_gcm` | `cryptography.hazmat.primitives.ciphers.aead.AESGCM` | `lib.pyca` | - | `AESGCM(GCM_KEY)` | keysize-from-key |
| PY-080 | S11 | `op:encrypt` | `aes-256-gcm` | 169:14 | 169:58 | [5469, 5513) | [5469, 5513) | 44 | 0 | `s11_aes256_gcm` | `cryptography.hazmat.primitives.ciphers.aead.AESGCM.encrypt` | `lib.pyca` | - | `aead.encrypt(GCM_IV, GCM_PLAINTEXT, GCM_AAD)` | - |
| PY-081 | S11 | `op:decrypt` | `aes-256-gcm` | 171:14 | 171:51 | [5576, 5613) | [5576, 5613) | 37 | 0 | `s11_aes256_gcm` | `cryptography.hazmat.primitives.ciphers.aead.AESGCM.decrypt` | `lib.pyca` | - | `aead.decrypt(GCM_IV, sealed, GCM_AAD)` | - |
| PY-082 | S12 | `op:generate` | `csprng` | 177:11 | 177:31 | [5814, 5834) | [5814, 5834) | 20 | 0 | `s12_chacha20_poly1305` | `Crypto.Random.get_random_bytes` | `lib.pycryptodome` | `m.chacha-key` | `get_random_bytes(32)` | - |
| PY-083 | S12 | `prm:length-bytes` | `m.chacha-key` | 177:28 | 177:30 | [5831, 5833) | [5831, 5833) | 2 | 1 | `s12_chacha20_poly1305` | - | `lib.pycryptodome` | - | `32` | - |
| PY-084 | S12 | `op:generate` | `csprng` | 178:13 | 178:33 | [5847, 5867) | [5847, 5867) | 20 | 0 | `s12_chacha20_poly1305` | `Crypto.Random.get_random_bytes` | `lib.pycryptodome` | `m.chacha-nonce` | `get_random_bytes(12)` | - |
| PY-085 | S12 | `prm:length-bytes` | `m.chacha-nonce` | 178:30 | 178:32 | [5864, 5866) | [5864, 5866) | 2 | 1 | `s12_chacha20_poly1305` | - | `lib.pycryptodome` | - | `12` | - |
| PY-086 | S12 | `ctor:encrypt` | `chacha20-poly1305` | 179:14 | 179:57 | [5881, 5924) | [5881, 5924) | 43 | 0 | `s12_chacha20_poly1305` | `Crypto.Cipher.ChaCha20_Poly1305.new` | `lib.pycryptodome` | - | `ChaCha20_Poly1305.new(key=key, nonce=nonce)` | - |
| PY-087 | S12 | `op:encrypt` | `chacha20-poly1305` | 180:23 | 180:57 | [5947, 5981) | [5947, 5981) | 34 | 0 | `s12_chacha20_poly1305` | `Crypto.Cipher.ChaCha20_Poly1305.ChaCha20Poly1305Cipher.encrypt_and_digest` | `lib.pycryptodome` | - | `sealer.encrypt_and_digest(MESSAGE)` | - |
| PY-088 | S12 | `ctor:decrypt` | `chacha20-poly1305` | 181:14 | 181:57 | [5995, 6038) | [5995, 6038) | 43 | 0 | `s12_chacha20_poly1305` | `Crypto.Cipher.ChaCha20_Poly1305.new` | `lib.pycryptodome` | - | `ChaCha20_Poly1305.new(key=key, nonce=nonce)` | - |
| PY-089 | S12 | `op:decrypt` | `chacha20-poly1305` | 182:17 | 182:59 | [6055, 6097) | [6055, 6097) | 42 | 0 | `s12_chacha20_poly1305` | `Crypto.Cipher.ChaCha20_Poly1305.ChaCha20Poly1305Cipher.decrypt_and_verify` | `lib.pycryptodome` | - | `opener.decrypt_and_verify(ciphertext, tag)` | - |
| PY-090 | S13 | `op:generate` | `csprng` | 188:11 | 188:25 | [6259, 6273) | [6259, 6273) | 14 | 0 | `s13_aes256_cbc` | `os.urandom` | `lib.py-stdlib` | `m.cbc-key` | `os.urandom(32)` | - |
| PY-091 | S13 | `prm:length-bytes` | `m.cbc-key` | 188:22 | 188:24 | [6270, 6272) | [6270, 6272) | 2 | 1 | `s13_aes256_cbc` | - | `lib.py-stdlib` | - | `32` | - |
| PY-092 | S13 | `op:generate` | `csprng` | 189:10 | 189:24 | [6283, 6297) | [6283, 6297) | 14 | 0 | `s13_aes256_cbc` | `os.urandom` | `lib.py-stdlib` | `m.cbc-iv` | `os.urandom(16)` | - |
| PY-093 | S13 | `prm:length-bytes` | `m.cbc-iv` | 189:21 | 189:23 | [6294, 6296) | [6294, 6296) | 2 | 1 | `s13_aes256_cbc` | - | `lib.py-stdlib` | - | `16` | - |
| PY-094 | S13 | `alg` | `aes-256-cbc` | 190:14 | 190:32 | [6311, 6329) | [6311, 6329) | 18 | 0 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.padding.PKCS7` | `lib.pyca` | - | `padding.PKCS7(128)` | padding |
| PY-095 | S13 | `ctor` | `aes-256-cbc` | 192:14 | 192:56 | [6408, 6450) | [6408, 6450) | 42 | 0 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.ciphers.Cipher` | `lib.pyca` | - | `Cipher(algorithms.AES(key), modes.CBC(iv))` | - |
| PY-096 | S13 | `alg` | `aes-256-cbc` | 192:21 | 192:40 | [6415, 6434) | [6415, 6434) | 19 | 1 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.ciphers.algorithms.AES` | `lib.pyca` | - | `algorithms.AES(key)` | keysize-from-key |
| PY-097 | S13 | `alg` | `aes-256-cbc` | 192:42 | 192:55 | [6436, 6449) | [6436, 6449) | 13 | 1 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.ciphers.modes.CBC` | `lib.pyca` | - | `modes.CBC(iv)` | - |
| PY-098 | S13 | `op:encrypt` | `aes-256-cbc` | 193:17 | 193:35 | [6467, 6485) | [6467, 6485) | 18 | 0 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.ciphers.Cipher.encryptor` | `lib.pyca` | - | `cipher.encryptor()` | - |
| PY-099 | S13 | `op:decrypt` | `aes-256-cbc` | 195:17 | 195:35 | [6567, 6585) | [6567, 6585) | 18 | 0 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.ciphers.Cipher.decryptor` | `lib.pyca` | - | `cipher.decryptor()` | - |
| PY-100 | S13 | `alg` | `aes-256-cbc` | 196:16 | 196:34 | [6601, 6619) | [6601, 6619) | 18 | 0 | `s13_aes256_cbc` | `cryptography.hazmat.primitives.padding.PKCS7` | `lib.pyca` | - | `padding.PKCS7(128)` | padding |
| PY-101 | S14 | `alg` | `aes-128-ecb` | 203:14 | 203:32 | [6919, 6937) | [6919, 6937) | 18 | 0 | `s14_aes128_ecb` | `cryptography.hazmat.primitives.padding.PKCS7` | `lib.pyca` | - | `padding.PKCS7(128)` | padding |
| PY-102 | S14 | `ctor` | `aes-128-ecb` | 205:14 | 205:58 | [7022, 7066) | [7022, 7066) | 44 | 0 | `s14_aes128_ecb` | `cryptography.hazmat.primitives.ciphers.Cipher` | `lib.pyca` | - | `Cipher(algorithms.AES(ECB_KEY), modes.ECB())` | - |
| PY-103 | S14 | `alg` | `aes-128-ecb` | 205:21 | 205:44 | [7029, 7052) | [7029, 7052) | 23 | 1 | `s14_aes128_ecb` | `cryptography.hazmat.primitives.ciphers.algorithms.AES` | `lib.pyca` | - | `algorithms.AES(ECB_KEY)` | keysize-from-key |
| PY-104 | S14 | `alg` | `aes-128-ecb` | 205:46 | 205:57 | [7054, 7065) | [7054, 7065) | 11 | 1 | `s14_aes128_ecb` | `cryptography.hazmat.primitives.ciphers.modes.ECB` | `lib.pyca` | - | `modes.ECB()` | - |
| PY-105 | S14 | `op:encrypt` | `aes-128-ecb` | 206:17 | 206:35 | [7083, 7101) | [7083, 7101) | 18 | 0 | `s14_aes128_ecb` | `cryptography.hazmat.primitives.ciphers.Cipher.encryptor` | `lib.pyca` | - | `cipher.encryptor()` | - |
| PY-106 | S15 | `op:generate` | `csprng` | 212:11 | 212:34 | [7251, 7274) | [7251, 7274) | 23 | 0 | `s15_aes256_ctr` | `secrets.token_bytes` | `lib.py-stdlib` | `m.ctr-key` | `secrets.token_bytes(32)` | - |
| PY-107 | S15 | `prm:length-bytes` | `m.ctr-key` | 212:31 | 212:33 | [7271, 7273) | [7271, 7273) | 2 | 1 | `s15_aes256_ctr` | - | `lib.py-stdlib` | - | `32` | - |
| PY-108 | S15 | `op:generate` | `csprng` | 213:21 | 213:44 | [7295, 7318) | [7295, 7318) | 23 | 0 | `s15_aes256_ctr` | `secrets.token_bytes` | `lib.py-stdlib` | `m.ctr-iv` | `secrets.token_bytes(16)` | - |
| PY-109 | S15 | `prm:length-bytes` | `m.ctr-iv` | 213:41 | 213:43 | [7315, 7317) | [7315, 7317) | 2 | 1 | `s15_aes256_ctr` | - | `lib.py-stdlib` | - | `16` | - |
| PY-110 | S15 | `ctor:encrypt` | `aes-256-ctr` | 214:17 | 214:83 | [7335, 7401) | [7335, 7401) | 66 | 0 | `s15_aes256_ctr` | `Crypto.Cipher.AES.new` | `lib.pycryptodome` | - | `AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=counter_block)` | ctr-full-block |
| PY-111 | S15 | `alg` | `aes-256-ctr` | 214:30 | 214:42 | [7348, 7360) | [7348, 7360) | 12 | 1 | `s15_aes256_ctr` | `Crypto.Cipher.AES.MODE_CTR` | `lib.pycryptodome` | - | `AES.MODE_CTR` | - |
| PY-112 | S15 | `op:encrypt` | `aes-256-ctr` | 215:18 | 215:44 | [7419, 7445) | [7419, 7445) | 26 | 0 | `s15_aes256_ctr` | `Crypto.Cipher._mode_ctr.CtrMode.encrypt` | `lib.pycryptodome` | - | `encryptor.encrypt(MESSAGE)` | - |
| PY-113 | S15 | `ctor:decrypt` | `aes-256-ctr` | 216:17 | 216:83 | [7462, 7528) | [7462, 7528) | 66 | 0 | `s15_aes256_ctr` | `Crypto.Cipher.AES.new` | `lib.pycryptodome` | - | `AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=counter_block)` | ctr-full-block |
| PY-114 | S15 | `alg` | `aes-256-ctr` | 216:30 | 216:42 | [7475, 7487) | [7475, 7487) | 12 | 1 | `s15_aes256_ctr` | `Crypto.Cipher.AES.MODE_CTR` | `lib.pycryptodome` | - | `AES.MODE_CTR` | - |
| PY-115 | S15 | `op:decrypt` | `aes-256-ctr` | 217:17 | 217:46 | [7545, 7574) | [7545, 7574) | 29 | 0 | `s15_aes256_ctr` | `Crypto.Cipher._mode_ctr.CtrMode.decrypt` | `lib.pycryptodome` | - | `decryptor.decrypt(ciphertext)` | - |
| PY-116 | S16 | `op:keygen` | `3des-cbc` | 223:11 | 223:55 | [7734, 7778) | [7734, 7778) | 44 | 0 | `s16_tdea_cbc` | `Crypto.Cipher.DES3.adjust_key_parity` | `lib.pycryptodome` | `m.tdes-key` | `DES3.adjust_key_parity(get_random_bytes(24))` | parity |
| PY-117 | S16 | `op:generate` | `csprng` | 223:34 | 223:54 | [7757, 7777) | [7757, 7777) | 20 | 1 | `s16_tdea_cbc` | `Crypto.Random.get_random_bytes` | `lib.pycryptodome` | - | `get_random_bytes(24)` | - |
| PY-118 | S16 | `prm:length-bytes` | `m.tdes-key` | 223:51 | 223:53 | [7774, 7776) | [7774, 7776) | 2 | 2 | `s16_tdea_cbc` | - | `lib.pycryptodome` | - | `24` | - |
| PY-119 | S16 | `op:generate` | `csprng` | 224:10 | 224:29 | [7788, 7807) | [7788, 7807) | 19 | 0 | `s16_tdea_cbc` | `Crypto.Random.get_random_bytes` | `lib.pycryptodome` | `m.tdes-iv` | `get_random_bytes(8)` | - |
| PY-120 | S16 | `prm:length-bytes` | `m.tdes-iv` | 224:27 | 224:28 | [7805, 7806) | [7805, 7806) | 1 | 1 | `s16_tdea_cbc` | - | `lib.pycryptodome` | - | `8` | - |
| PY-121 | S16 | `ctor:encrypt` | `3des-cbc` | 225:17 | 225:52 | [7824, 7859) | [7824, 7859) | 35 | 0 | `s16_tdea_cbc` | `Crypto.Cipher.DES3.new` | `lib.pycryptodome` | - | `DES3.new(key, DES3.MODE_CBC, iv=iv)` | - |
| PY-122 | S16 | `alg` | `3des-cbc` | 225:31 | 225:44 | [7838, 7851) | [7838, 7851) | 13 | 1 | `s16_tdea_cbc` | `Crypto.Cipher.DES3.MODE_CBC` | `lib.pycryptodome` | - | `DES3.MODE_CBC` | - |
| PY-123 | S16 | `op:encrypt` | `3des-cbc` | 226:18 | 226:52 | [7877, 7911) | [7877, 7911) | 34 | 0 | `s16_tdea_cbc` | `Crypto.Cipher._mode_cbc.CbcMode.encrypt` | `lib.pycryptodome` | - | `encryptor.encrypt(pad(MESSAGE, 8))` | - |
| PY-124 | S16 | `alg` | `3des-cbc` | 226:36 | 226:51 | [7895, 7910) | [7895, 7910) | 15 | 1 | `s16_tdea_cbc` | `Crypto.Util.Padding.pad` | `lib.pycryptodome` | - | `pad(MESSAGE, 8)` | pad-default-pkcs7 |
| PY-125 | S16 | `ctor:decrypt` | `3des-cbc` | 227:17 | 227:52 | [7928, 7963) | [7928, 7963) | 35 | 0 | `s16_tdea_cbc` | `Crypto.Cipher.DES3.new` | `lib.pycryptodome` | - | `DES3.new(key, DES3.MODE_CBC, iv=iv)` | - |
| PY-126 | S16 | `alg` | `3des-cbc` | 227:31 | 227:44 | [7942, 7955) | [7942, 7955) | 13 | 1 | `s16_tdea_cbc` | `Crypto.Cipher.DES3.MODE_CBC` | `lib.pycryptodome` | - | `DES3.MODE_CBC` | - |
| PY-127 | S16 | `alg` | `3des-cbc` | 228:17 | 228:56 | [7980, 8019) | [7980, 8019) | 39 | 0 | `s16_tdea_cbc` | `Crypto.Util.Padding.unpad` | `lib.pycryptodome` | - | `unpad(decryptor.decrypt(ciphertext), 8)` | pad-default-pkcs7 |
| PY-128 | S16 | `op:decrypt` | `3des-cbc` | 228:23 | 228:52 | [7986, 8015) | [7986, 8015) | 29 | 1 | `s16_tdea_cbc` | `Crypto.Cipher._mode_cbc.CbcMode.decrypt` | `lib.pycryptodome` | - | `decryptor.decrypt(ciphertext)` | - |
| PY-129 | S17 | `op:keygen` | `rsa-3072` | 234:19 | 234:81 | [8200, 8262) | [8200, 8262) | 62 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key` | `lib.pyca` | `m.rsa-private-key`, `m.rsa-public-key` | `rsa.generate_private_key(public_exponent=65537, key_size=3072)` | - |
| PY-130 | S17 | `prm:public-exponent` | `rsa-3072` | 234:60 | 234:65 | [8241, 8246) | [8241, 8246) | 5 | 1 | `s17_rsa3072` | - | `lib.pyca` | - | `65537` | - |
| PY-131 | S17 | `prm:key-size-bits` | `rsa-3072` | 234:76 | 234:80 | [8257, 8261) | [8257, 8261) | 4 | 1 | `s17_rsa3072` | - | `lib.pyca` | - | `3072` | - |
| PY-132 | S17 | `alg` | `rsa-oaep-sha256` | 237:12 | 241:6 | [8317, 8444) | [8317, 8444) | 127 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.padding.OAEP` | `lib.pyca` | - | `asym_padding.OAEP( … (+4 lines)` | - |
| PY-133 | S17 | `alg` | `mgf1-sha256` ^`rsa-oaep-sha256` | 238:13 | 238:47 | [8348, 8382) | [8348, 8382) | 34 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.padding.MGF1` | `lib.pyca` | - | `asym_padding.MGF1(hashes.SHA256())` | - |
| PY-134 | S17 | `alg` | `sha-256` ^`mgf1-sha256` | 238:31 | 238:46 | [8366, 8381) | [8366, 8381) | 15 | 2 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-135 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 239:19 | 239:34 | [8402, 8417) | [8402, 8417) | 15 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-136 | S17 | `op:encrypt` | `rsa-oaep-sha256` | 242:18 | 242:51 | [8462, 8495) | [8462, 8495) | 33 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey.encrypt` | `lib.pyca` | - | `public_key.encrypt(MESSAGE, oaep)` | - |
| PY-137 | S17 | `op:decrypt` | `rsa-oaep-sha256` | 243:17 | 243:54 | [8512, 8549) | [8512, 8549) | 37 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.decrypt` | `lib.pyca` | - | `private_key.decrypt(ciphertext, oaep)` | - |
| PY-138 | S17 | `alg` | `rsassa-pss-sha256` | 246:11 | 249:6 | [8637, 8732) | [8637, 8732) | 95 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.padding.PSS` | `lib.pyca` | - | `asym_padding.PSS( … (+3 lines)` | - |
| PY-139 | S17 | `alg` | `mgf1-sha256` ^`rsassa-pss-sha256` | 247:13 | 247:47 | [8667, 8701) | [8667, 8701) | 34 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.padding.MGF1` | `lib.pyca` | - | `asym_padding.MGF1(hashes.SHA256())` | - |
| PY-140 | S17 | `alg` | `sha-256` ^`mgf1-sha256` | 247:31 | 247:46 | [8685, 8700) | [8685, 8700) | 15 | 2 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-141 | S17 | `prm:salt-length-bytes` | `rsassa-pss-sha256` | 248:21 | 248:23 | [8723, 8725) | [8723, 8725) | 2 | 1 | `s17_rsa3072` | - | `lib.pyca` | - | `32` | - |
| PY-142 | S17 | `op:sign` | `rsassa-pss-sha256` | 250:17 | 250:64 | [8749, 8796) | [8749, 8796) | 47 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.sign` | `lib.pyca` | - | `private_key.sign(MESSAGE, pss, hashes.SHA256())` | - |
| PY-143 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 250:48 | 250:63 | [8780, 8795) | [8780, 8795) | 15 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-144 | S17 | `op:verify` | `rsassa-pss-sha256` | 251:27 | 251:86 | [8823, 8882) | [8823, 8882) | 59 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey.verify` | `lib.pyca` | - | `public_key.verify(signature, MESSAGE, pss, hashes.SHA256())` | - |
| PY-145 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 251:70 | 251:85 | [8866, 8881) | [8866, 8881) | 15 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-146 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 254:13 | 254:36 | [8951, 8974) | [8951, 8974) | 23 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15` | `lib.pyca` | - | `asym_padding.PKCS1v15()` | - |
| PY-147 | S17 | `op:sign` | `rsassa-pkcs1v15-sha256` | 255:17 | 255:66 | [8991, 9040) | [8991, 9040) | 49 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.sign` | `lib.pyca` | - | `private_key.sign(MESSAGE, pkcs1, hashes.SHA256())` | - |
| PY-148 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 255:50 | 255:65 | [9024, 9039) | [9024, 9039) | 15 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-149 | S17 | `op:verify` | `rsassa-pkcs1v15-sha256` | 256:27 | 256:88 | [9067, 9128) | [9067, 9128) | 61 | 0 | `s17_rsa3072` | `cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey.verify` | `lib.pyca` | - | `public_key.verify(signature, MESSAGE, pkcs1, hashes.SHA256())` | - |
| PY-150 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 256:72 | 256:87 | [9112, 9127) | [9112, 9127) | 15 | 1 | `s17_rsa3072` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-151 | S18 | `op:keygen` | `ecdsa-p256-sha256` | 262:19 | 262:58 | [9271, 9310) | [9271, 9310) | 39 | 0 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.generate_private_key` | `lib.pyca` | `m.ecdsa-private-key`, `m.ecdsa-public-key` | `ec.generate_private_key(ec.SECP256R1())` | - |
| PY-152 | S18 | `alg` | `ecdsa-p256-sha256` | 262:43 | 262:57 | [9295, 9309) | [9295, 9309) | 14 | 1 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.SECP256R1` | `lib.pyca` | - | `ec.SECP256R1()` | - |
| PY-153 | S18 | `op:sign` | `ecdsa-p256-sha256` | 263:17 | 263:69 | [9327, 9379) | [9327, 9379) | 52 | 0 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey.sign` | `lib.pyca` | - | `private_key.sign(MESSAGE, ec.ECDSA(hashes.SHA256()))` | - |
| PY-154 | S18 | `alg` | `ecdsa-p256-sha256` | 263:43 | 263:68 | [9353, 9378) | [9353, 9378) | 25 | 1 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.ECDSA` | `lib.pyca` | - | `ec.ECDSA(hashes.SHA256())` | - |
| PY-155 | S18 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 263:52 | 263:67 | [9362, 9377) | [9362, 9377) | 15 | 2 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-156 | S18 | `op:verify` | `ecdsa-p256-sha256` | 264:27 | 264:105 | [9406, 9484) | [9406, 9484) | 78 | 0 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey.verify` | `lib.pyca` | - | `private_key.public_key().verify(signature, MESSAGE, ec.ECDSA(hashes.SHA256()))` | - |
| PY-157 | S18 | `alg` | `ecdsa-p256-sha256` | 264:79 | 264:104 | [9458, 9483) | [9458, 9483) | 25 | 1 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.asymmetric.ec.ECDSA` | `lib.pyca` | - | `ec.ECDSA(hashes.SHA256())` | - |
| PY-158 | S18 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 264:88 | 264:103 | [9467, 9482) | [9467, 9482) | 15 | 2 | `s18_ecdsa_p256` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-159 | S19 | `ctor` | `ed25519` | 270:19 | 270:43 | [9630, 9654) | [9630, 9654) | 24 | 0 | `s19_ed25519` | `nacl.signing.SigningKey` | `lib.pynacl` | `m.ed25519-public-key` | `SigningKey(ED25519_SEED)` | seed-ctor |
| PY-160 | S19 | `op:sign` | `ed25519` | 271:14 | 271:39 | [9668, 9693) | [9668, 9693) | 25 | 0 | `s19_ed25519` | `nacl.signing.SigningKey.sign` | `lib.pynacl` | - | `signing_key.sign(MESSAGE)` | - |
| PY-161 | S19 | `op:verify` | `ed25519` | 273:27 | 273:71 | [9760, 9804) | [9760, 9804) | 44 | 0 | `s19_ed25519` | `nacl.signing.VerifyKey.verify` | `lib.pynacl` | - | `verify_key.verify(MESSAGE, signed.signature)` | - |
| PY-162 | S20 | `ctor` | `hkdf-sha256` | 278:12 | 278:84 | [9981, 10053) | [9981, 10053) | 72 | 0 | `derive_session_key` | `cryptography.hazmat.primitives.kdf.hkdf.HKDF` | `lib.pyca` | - | `HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=SESSION_INFO)` | - |
| PY-163 | S20 | `alg` | `sha-256` ^`hkdf-sha256` | 278:27 | 278:42 | [9996, 10011) | [9996, 10011) | 15 | 1 | `derive_session_key` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-164 | S20 | `prm:output-length-bytes` | `hkdf-sha256` | 278:51 | 278:53 | [10020, 10022) | [10020, 10022) | 2 | 1 | `derive_session_key` | - | `lib.pyca` | - | `32` | - |
| PY-165 | S20 | `op:keyderive` | `hkdf-sha256` | 279:12 | 279:38 | [10065, 10091) | [10065, 10091) | 26 | 0 | `derive_session_key` | `cryptography.hazmat.primitives.kdf.hkdf.HKDF.derive` | `lib.pyca` | `m.session-key` | `hkdf.derive(shared_secret)` | - |
| PY-166 | S20 | `op:keygen` | `x25519` | 284:13 | 284:47 | [10198, 10232) | [10198, 10232) | 34 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey.generate` | `lib.pyca` | `m.x25519-private-key-a` | `x25519.X25519PrivateKey.generate()` | - |
| PY-167 | S20 | `op:keygen` | `x25519` | 285:11 | 285:45 | [10243, 10277) | [10243, 10277) | 34 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey.generate` | `lib.pyca` | `m.x25519-private-key-b` | `x25519.X25519PrivateKey.generate()` | - |
| PY-168 | S20 | `op:agree` | `x25519` | 286:15 | 286:47 | [10292, 10324) | [10292, 10324) | 32 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey.exchange` | `lib.pyca` | `m.x25519-shared-secret` | `alice.exchange(bob.public_key())` | - |
| PY-169 | S20 | `op:agree` | `x25519` | 287:13 | 287:45 | [10337, 10369) | [10337, 10369) | 32 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey.exchange` | `lib.pyca` | `m.x25519-shared-secret` | `bob.exchange(alice.public_key())` | - |
| PY-170 | S20 | `op:keygen` | `ecdh-p256` | 290:16 | 290:55 | [10447, 10486) | [10447, 10486) | 39 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.generate_private_key` | `lib.pyca` | `m.ecdh-private-key-a` | `ec.generate_private_key(ec.SECP256R1())` | - |
| PY-171 | S20 | `alg` | `ecdh-p256` | 290:40 | 290:54 | [10471, 10485) | [10471, 10485) | 14 | 1 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.SECP256R1` | `lib.pyca` | - | `ec.SECP256R1()` | - |
| PY-172 | S20 | `op:keygen` | `ecdh-p256` | 291:14 | 291:53 | [10500, 10539) | [10500, 10539) | 39 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.generate_private_key` | `lib.pyca` | `m.ecdh-private-key-b` | `ec.generate_private_key(ec.SECP256R1())` | - |
| PY-173 | S20 | `alg` | `ecdh-p256` | 291:38 | 291:52 | [10524, 10538) | [10524, 10538) | 14 | 1 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.SECP256R1` | `lib.pyca` | - | `ec.SECP256R1()` | - |
| PY-174 | S20 | `op:agree` | `ecdh-p256` | 292:15 | 292:64 | [10554, 10603) | [10554, 10603) | 49 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey.exchange` | `lib.pyca` | `m.ecdh-shared-secret` | `alice_ec.exchange(ec.ECDH(), bob_ec.public_key())` | - |
| PY-175 | S20 | `alg` | `ecdh-p256` | 292:33 | 292:42 | [10572, 10581) | [10572, 10581) | 9 | 1 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.ECDH` | `lib.pyca` | - | `ec.ECDH()` | - |
| PY-176 | S20 | `op:agree` | `ecdh-p256` | 293:13 | 293:62 | [10616, 10665) | [10616, 10665) | 49 | 0 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey.exchange` | `lib.pyca` | `m.ecdh-shared-secret` | `bob_ec.exchange(ec.ECDH(), alice_ec.public_key())` | - |
| PY-177 | S20 | `alg` | `ecdh-p256` | 293:29 | 293:38 | [10632, 10641) | [10632, 10641) | 9 | 1 | `s20_key_agreement` | `cryptography.hazmat.primitives.asymmetric.ec.ECDH` | `lib.pyca` | - | `ec.ECDH()` | - |
| PY-178 | S21 | `op:keygen` | `ml-kem-768` | 303:25 | 303:60 | [10986, 11021) | [10986, 11021) | 35 | 0 | `s21_ml_kem_768` | `cryptography.hazmat.primitives.asymmetric.mlkem.MLKEM768PrivateKey.generate` | `lib.pyca` | `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key` | `mlkem.MLKEM768PrivateKey.generate()` | - |
| PY-179 | S21 | `op:encapsulate` | `ml-kem-768` | 305:33 | 305:64 | [11109, 11140) | [11109, 11140) | 31 | 0 | `s21_ml_kem_768` | `cryptography.hazmat.primitives.asymmetric.mlkem.MLKEM768PublicKey.encapsulate` | `lib.pyca` | `m.mlkem-shared-secret` | `encapsulation_key.encapsulate()` | - |
| PY-180 | S21 | `op:decapsulate` | `ml-kem-768` | 306:17 | 306:58 | [11157, 11198) | [11157, 11198) | 41 | 0 | `s21_ml_kem_768` | `cryptography.hazmat.primitives.asymmetric.mlkem.MLKEM768PrivateKey.decapsulate` | `lib.pyca` | `m.mlkem-shared-secret` | `decapsulation_key.decapsulate(ciphertext)` | - |
| PY-181 | S22 | `op:keygen` | `ml-dsa-65` | 312:19 | 312:53 | [11396, 11430) | [11396, 11430) | 34 | 0 | `s22_ml_dsa_65` | `cryptography.hazmat.primitives.asymmetric.mldsa.MLDSA65PrivateKey.generate` | `lib.pyca` | `m.mldsa-private-key`, `m.mldsa-public-key` | `mldsa.MLDSA65PrivateKey.generate()` | - |
| PY-182 | S22 | `op:sign` | `ml-dsa-65` | 313:17 | 313:42 | [11447, 11472) | [11447, 11472) | 25 | 0 | `s22_ml_dsa_65` | `cryptography.hazmat.primitives.asymmetric.mldsa.MLDSA65PrivateKey.sign` | `lib.pyca` | - | `private_key.sign(MESSAGE)` | - |
| PY-183 | S22 | `op:verify` | `ml-dsa-65` | 314:27 | 314:78 | [11499, 11550) | [11499, 11550) | 51 | 0 | `s22_ml_dsa_65` | `cryptography.hazmat.primitives.asymmetric.mldsa.MLDSA65PublicKey.verify` | `lib.pyca` | - | `private_key.public_key().verify(signature, MESSAGE)` | - |
| PY-184 | S23 | `op:keygen` | `ecdsa-p256-sha256` | 320:11 | 320:50 | [11709, 11748) | [11709, 11748) | 39 | 0 | `s23_x509_self_signed` | `cryptography.hazmat.primitives.asymmetric.ec.generate_private_key` | `lib.pyca` | `m.cert-private-key`, `m.cert-public-key` | `ec.generate_private_key(ec.SECP256R1())` | - |
| PY-185 | S23 | `alg` | `ecdsa-p256-sha256` | 320:35 | 320:49 | [11733, 11747) | [11733, 11747) | 14 | 1 | `s23_x509_self_signed` | `cryptography.hazmat.primitives.asymmetric.ec.SECP256R1` | `lib.pyca` | - | `ec.SECP256R1()` | - |
| PY-186 | S23 | `ctor` | `cert.self-signed` | 324:9 | 324:34 | [11891, 11916) | [11891, 11916) | 25 | 0 | `s23_x509_self_signed` | `cryptography.x509.CertificateBuilder` | `lib.pyca` | - | `x509.CertificateBuilder()` | - |
| PY-187 | S23 | `op:generate` | `csprng` | 328:24 | 328:44 | [12033, 12053) | [12033, 12053) | 20 | 0 | `s23_x509_self_signed` | `secrets.randbits` | `lib.py-stdlib` | - | `secrets.randbits(64)` | serial |
| PY-188 | S23 | `prm:validity-days` | `cert.self-signed` | 330:47 | 330:50 | [12155, 12158) | [12155, 12158) | 3 | 0 | `s23_x509_self_signed` | - | `lib.py-stdlib` | - | `365` | - |
| PY-189 | S23 | `op:sign` | `cert.self-signed` | 332:19 | 332:53 | [12185, 12219) | [12185, 12219) | 34 | 0 | `s23_x509_self_signed` | `cryptography.x509.CertificateBuilder.sign` | `lib.pyca` | - | `builder.sign(key, hashes.SHA256())` | - |
| PY-190 | S23 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 332:37 | 332:52 | [12203, 12218) | [12203, 12218) | 15 | 1 | `s23_x509_self_signed` | `cryptography.hazmat.primitives.hashes.SHA256` | `lib.pyca` | - | `hashes.SHA256()` | - |
| PY-191 | S23 | `op:verify` | `ecdsa-p256-sha256` | 334:17 | 338:10 | [12255, 12439) | [12255, 12439) | 184 | 0 | `s23_x509_self_signed` | `cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey.verify` | `lib.pyca` | - | `certificate.public_key().verify( … (+4 lines)` | - |
| PY-192 | S23 | `alg` | `ecdsa-p256-sha256` | 337:13 | 337:59 | [12382, 12428) | [12382, 12428) | 46 | 1 | `s23_x509_self_signed` | `cryptography.hazmat.primitives.asymmetric.ec.ECDSA` | `lib.pyca` | - | `ec.ECDSA(certificate.signature_hash_algorithm)` | hash-from-cert |
| PY-193 | S24 | `ctor` | `tls13-client` | 345:15 | 345:43 | [12612, 12640) | [12612, 12640) | 28 | 0 | `s24_tls13_client` | `ssl.create_default_context` | `lib.py-stdlib` | - | `ssl.create_default_context()` | - |
| PY-194 | S24 | `cfg:min-version` | `tls13-client` | 346:5 | 346:53 | [12645, 12693) | [12645, 12693) | 48 | 0 | `s24_tls13_client` | `ssl.SSLContext.minimum_version` | `lib.py-stdlib` | - | `context.minimum_version = ssl.TLSVersion.TLSv1_3` | - |
| PY-195 | S24 | `cfg:max-version` | `tls13-client` | 347:5 | 347:53 | [12698, 12746) | [12698, 12746) | 48 | 0 | `s24_tls13_client` | `ssl.SSLContext.maximum_version` | `lib.py-stdlib` | - | `context.maximum_version = ssl.TLSVersion.TLSv1_3` | - |

## Full text of multi-line evidence

**PY-055** (`hkdf-sha256`, 121:12 to 126:6):

```text
HKDF(
        algorithm=hashes.SHA256(),
        length=42,
        salt=HKDF_SALT,
        info=HKDF_INFO,
    )
```

**PY-059** (`pbkdf2-hmac-sha256`, 132:15 to 134:6):

```text
hashlib.pbkdf2_hmac(
        "sha256", PBKDF2_PASSWORD, PBKDF2_SALT, 80_000, dklen=64
    )
```

**PY-069** (`argon2id`, 146:11 to 154:6):

```text
hash_secret_raw(
        secret=PASSWORD,
        salt=ARGON2_SALT,
        time_cost=2,
        memory_cost=19_456,
        parallelism=1,
        hash_len=32,
        type=Type.ID,
    )
```

**PY-132** (`rsa-oaep-sha256`, 237:12 to 241:6):

```text
asym_padding.OAEP(
        mgf=asym_padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
```

**PY-138** (`rsassa-pss-sha256`, 246:11 to 249:6):

```text
asym_padding.PSS(
        mgf=asym_padding.MGF1(hashes.SHA256()),
        salt_length=32,
    )
```

**PY-191** (`ecdsa-p256-sha256`, 334:17 to 338:10):

```text
certificate.public_key().verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            ec.ECDSA(certificate.signature_hash_algorithm),
        )
```

## Non-asset mentions (negative ground truth)

Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.

| ID | L:C | Bytes | Match | Context | Containing token / line | Why it is not an asset |
|---|---|---|---|---|---|---|
| PY-N001 | 44:32 | [1734, 1738) | `HMAC` | comment | `HMAC_KEY = b"key"  # Wikipedia HMAC example key` | Comment text; documentation only |
| PY-N002 | 57:1 | [2362, 2365) | `GCM` | identifier | `GCM_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N003 | 62:1 | [2614, 2617) | `ECB` | identifier | `ECB_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N004 | 65:1 | [2822, 2825) | `TLS` | identifier | `TLS_SERVER_NAME` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N005 | 84:8 | [3208, 3215) | `SHA-256` | comment | `# S01: SHA-256 (FIPS 180-4)` | Comment text; documentation only |
| PY-N006 | 85:9 | [3237, 3243) | `sha256` | identifier | `s01_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N007 | 86:18 | [3272, 3279) | `SHA-256` | string | `"SHA-256"` | Output label passed to emit(); printed text only |
| PY-N008 | 89:8 | [3328, 3335) | `SHA-512` | comment | `# S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| PY-N009 | 89:17 | [3337, 3345) | `SHA3-256` | comment | `# S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| PY-N010 | 89:27 | [3347, 3354) | `BLAKE2b` | comment | `# S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| PY-N011 | 90:14 | [3372, 3376) | `sha3` | identifier | `s02_sha2_sha3_blake2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N012 | 90:19 | [3377, 3383) | `blake2` | identifier | `s02_sha2_sha3_blake2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N013 | 91:18 | [3412, 3419) | `SHA-512` | string | `"SHA-512"` | Output label passed to emit(); printed text only |
| PY-N014 | 92:18 | [3476, 3484) | `SHA3-256` | string | `"SHA3-256"` | Output label passed to emit(); printed text only |
| PY-N015 | 95:18 | [3609, 3616) | `BLAKE2b` | string | `"BLAKE2b-512"` | Output label passed to emit(); printed text only |
| PY-N016 | 100:5 | [3728, 3731) | `md5` | identifier | `md5` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N017 | 101:18 | [3795, 3798) | `MD5` | string | `"MD5"` | Output label passed to emit(); printed text only |
| PY-N018 | 101:24 | [3801, 3804) | `md5` | identifier | `md5` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N019 | 102:5 | [3822, 3826) | `sha1` | identifier | `sha1` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N020 | 103:5 | [3860, 3864) | `sha1` | identifier | `sha1` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N021 | 104:18 | [3898, 3903) | `SHA-1` | string | `"SHA-1"` | Output label passed to emit(); printed text only |
| PY-N022 | 107:8 | [3938, 3946) | `SHAKE128` | comment | `# S04: SHAKE128 extendable-output function` | Comment text; documentation only |
| PY-N023 | 108:9 | [3982, 3990) | `shake128` | identifier | `s04_shake128` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N024 | 110:18 | [4056, 4064) | `SHAKE128` | string | `"SHAKE128"` | Output label passed to emit(); printed text only |
| PY-N025 | 113:8 | [4095, 4099) | `HMAC` | comment | `# S05: HMAC-SHA256` | Comment text; documentation only |
| PY-N026 | 113:13 | [4100, 4106) | `SHA256` | comment | `# S05: HMAC-SHA256` | Comment text; documentation only |
| PY-N027 | 114:9 | [4115, 4119) | `hmac` | identifier | `s05_hmac_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N028 | 114:14 | [4120, 4126) | `sha256` | identifier | `s05_hmac_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N029 | 116:18 | [4209, 4213) | `HMAC` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| PY-N030 | 116:23 | [4214, 4220) | `SHA256` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| PY-N031 | 119:8 | [4249, 4253) | `HKDF` | comment | `# S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| PY-N032 | 119:13 | [4254, 4260) | `SHA256` | comment | `# S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| PY-N033 | 120:9 | [4280, 4284) | `hkdf` | identifier | `s06_hkdf_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N034 | 120:14 | [4285, 4291) | `sha256` | identifier | `s06_hkdf_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N035 | 121:5 | [4307, 4311) | `hkdf` | identifier | `hkdf` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N036 | 127:18 | [4445, 4449) | `HKDF` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| PY-N037 | 127:23 | [4450, 4456) | `SHA256` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| PY-N038 | 130:8 | [4497, 4503) | `PBKDF2` | comment | `# S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| PY-N039 | 130:15 | [4504, 4508) | `HMAC` | comment | `# S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| PY-N040 | 130:20 | [4509, 4515) | `SHA256` | comment | `# S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| PY-N041 | 131:9 | [4524, 4530) | `pbkdf2` | identifier | `s07_pbkdf2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N042 | 135:18 | [4665, 4671) | `PBKDF2` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| PY-N043 | 135:25 | [4672, 4678) | `SHA256` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| PY-N044 | 138:8 | [4705, 4711) | `scrypt` | comment | `# S08: scrypt` | Comment text; documentation only |
| PY-N045 | 139:9 | [4720, 4726) | `scrypt` | identifier | `s08_scrypt` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N046 | 141:18 | [4820, 4826) | `scrypt` | string | `"scrypt"` | Output label passed to emit(); printed text only |
| PY-N047 | 144:8 | [4873, 4881) | `Argon2id` | comment | `# S09: Argon2id` | Comment text; documentation only |
| PY-N048 | 145:9 | [4890, 4898) | `argon2id` | identifier | `s09_argon2id` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N049 | 155:18 | [5126, 5134) | `Argon2id` | string | `"Argon2id"` | Output label passed to emit(); printed text only |
| PY-N050 | 158:8 | [5157, 5163) | `bcrypt` | comment | `# S10: bcrypt` | Comment text; documentation only |
| PY-N051 | 159:9 | [5172, 5178) | `bcrypt` | identifier | `s10_bcrypt` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N052 | 163:18 | [5329, 5335) | `bcrypt` | string | `"bcrypt"` | Output label passed to emit(); printed text only |
| PY-N053 | 166:8 | [5369, 5376) | `AES-256` | comment | `# S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| PY-N054 | 166:16 | [5377, 5380) | `GCM` | comment | `# S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| PY-N055 | 167:9 | [5407, 5413) | `aes256` | identifier | `s11_aes256_gcm` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N056 | 167:16 | [5414, 5417) | `gcm` | identifier | `s11_aes256_gcm` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N057 | 172:18 | [5631, 5638) | `AES-256` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| PY-N058 | 172:26 | [5639, 5642) | `GCM` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| PY-N059 | 172:98 | [5711, 5714) | `GCM` | string | `"ct={ciphertext.hex()} tag={tag.hex()} roundtrip={flag(opened == GCM_PLAINTEXT)…` | Output label passed to emit(); printed text only |
| PY-N060 | 175:8 | [5738, 5755) | `ChaCha20-Poly1305` | comment | `# S12: ChaCha20-Poly1305 (RFC 8439)` | Comment text; documentation only |
| PY-N061 | 176:9 | [5775, 5783) | `chacha20` | identifier | `s12_chacha20_poly1305` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N062 | 176:18 | [5784, 5792) | `poly1305` | identifier | `s12_chacha20_poly1305` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N063 | 183:18 | [6115, 6132) | `ChaCha20-Poly1305` | string | `"ChaCha20-Poly1305"` | Output label passed to emit(); printed text only |
| PY-N064 | 186:8 | [6187, 6194) | `AES-256` | comment | `# S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| PY-N065 | 186:16 | [6195, 6198) | `CBC` | comment | `# S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| PY-N066 | 187:9 | [6227, 6233) | `aes256` | identifier | `s13_aes256_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N067 | 187:16 | [6234, 6237) | `cbc` | identifier | `s13_aes256_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N068 | 198:18 | [6755, 6762) | `AES-256` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| PY-N069 | 198:26 | [6763, 6766) | `CBC` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| PY-N070 | 201:8 | [6821, 6828) | `AES-128` | comment | `# S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| PY-N071 | 201:16 | [6829, 6832) | `ECB` | comment | `# S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| PY-N072 | 202:9 | [6884, 6890) | `aes128` | identifier | `s14_aes128_ecb` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N073 | 202:16 | [6891, 6894) | `ecb` | identifier | `s14_aes128_ecb` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N074 | 204:28 | [6974, 6977) | `ECB` | identifier | `ECB_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N075 | 207:18 | [7119, 7126) | `AES-128` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| PY-N076 | 207:26 | [7127, 7130) | `ECB` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| PY-N077 | 210:8 | [7199, 7206) | `AES-256` | comment | `# S15: AES-256-CTR` | Comment text; documentation only |
| PY-N078 | 210:16 | [7207, 7210) | `CTR` | comment | `# S15: AES-256-CTR` | Comment text; documentation only |
| PY-N079 | 211:9 | [7219, 7225) | `aes256` | identifier | `s15_aes256_ctr` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N080 | 211:16 | [7226, 7229) | `ctr` | identifier | `s15_aes256_ctr` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N081 | 218:18 | [7592, 7599) | `AES-256` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| PY-N082 | 218:26 | [7600, 7603) | `CTR` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| PY-N083 | 221:8 | [7658, 7662) | `3DES` | comment | `# S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| PY-N084 | 221:14 | [7664, 7668) | `TDEA` | comment | `# S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| PY-N085 | 221:20 | [7670, 7673) | `CBC` | comment | `# S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| PY-N086 | 222:9 | [7704, 7708) | `tdea` | identifier | `s16_tdea_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N087 | 222:14 | [7709, 7712) | `cbc` | identifier | `s16_tdea_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N088 | 229:18 | [8037, 8041) | `3DES` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| PY-N089 | 229:23 | [8042, 8045) | `CBC` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| PY-N090 | 232:8 | [8100, 8103) | `RSA` | comment | `# S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| PY-N091 | 232:19 | [8111, 8115) | `OAEP` | comment | `# S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| PY-N092 | 232:25 | [8117, 8120) | `PSS` | comment | `# S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| PY-N093 | 233:9 | [8163, 8166) | `rsa` | identifier | `s17_rsa3072` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N094 | 237:5 | [8310, 8314) | `oaep` | identifier | `oaep` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N095 | 244:18 | [8567, 8570) | `RSA` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| PY-N096 | 244:27 | [8576, 8580) | `OAEP` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| PY-N097 | 246:5 | [8631, 8634) | `pss` | identifier | `pss` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N098 | 252:18 | [8901, 8904) | `RSA` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| PY-N099 | 252:27 | [8910, 8913) | `PSS` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| PY-N100 | 254:5 | [8943, 8948) | `pkcs1` | identifier | `pkcs1` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N101 | 257:18 | [9147, 9150) | `RSA` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| PY-N102 | 257:27 | [9156, 9164) | `PKCS1v15` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| PY-N103 | 260:8 | [9198, 9203) | `ECDSA` | comment | `# S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| PY-N104 | 260:14 | [9204, 9209) | `P-256` | comment | `# S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| PY-N105 | 260:25 | [9215, 9222) | `SHA-256` | comment | `# S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| PY-N106 | 261:9 | [9231, 9236) | `ecdsa` | identifier | `s18_ecdsa_p256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N107 | 261:15 | [9237, 9241) | `p256` | identifier | `s18_ecdsa_p256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N108 | 265:18 | [9503, 9508) | `ECDSA` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| PY-N109 | 265:24 | [9509, 9514) | `P-256` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| PY-N110 | 268:8 | [9548, 9555) | `Ed25519` | comment | `# S19: Ed25519 from a fixed seed (RFC 8032)` | Comment text; documentation only |
| PY-N111 | 269:9 | [9593, 9600) | `ed25519` | identifier | `s19_ed25519` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N112 | 274:18 | [9823, 9830) | `Ed25519` | string | `"Ed25519"` | Output label passed to emit(); printed text only |
| PY-N113 | 278:5 | [9974, 9978) | `hkdf` | identifier | `hkdf` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N114 | 282:8 | [10101, 10107) | `X25519` | comment | `# S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| PY-N115 | 282:17 | [10110, 10114) | `ECDH` | comment | `# S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| PY-N116 | 282:22 | [10115, 10120) | `P-256` | comment | `# S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| PY-N117 | 282:43 | [10136, 10140) | `HKDF` | comment | `# S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| PY-N118 | 288:18 | [10387, 10393) | `X25519` | string | `"X25519"` | Output label passed to emit(); printed text only |
| PY-N119 | 294:18 | [10683, 10687) | `ECDH` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| PY-N120 | 294:23 | [10688, 10693) | `P-256` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| PY-N121 | 298:18 | [10847, 10851) | `HKDF` | string | `"HKDF session key"` | Output label passed to emit(); printed text only |
| PY-N122 | 301:8 | [10910, 10920) | `ML-KEM-768` | comment | `# S21: ML-KEM-768 (FIPS 203)` | Comment text; documentation only |
| PY-N123 | 307:18 | [11216, 11226) | `ML-KEM-768` | string | `"ML-KEM-768"` | Output label passed to emit(); printed text only |
| PY-N124 | 310:8 | [11328, 11337) | `ML-DSA-65` | comment | `# S22: ML-DSA-65 (FIPS 204)` | Comment text; documentation only |
| PY-N125 | 315:18 | [11569, 11578) | `ML-DSA-65` | string | `"ML-DSA-65"` | Output label passed to emit(); printed text only |
| PY-N126 | 318:20 | [11645, 11650) | `X.509` | comment | `# S23: self-signed X.509 certificate` | Comment text; documentation only |
| PY-N127 | 319:9 | [11671, 11675) | `x509` | identifier | `s23_x509_self_signed` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N128 | 321:12 | [11760, 11764) | `x509` | identifier | `x509` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N129 | 321:23 | [11771, 11775) | `x509` | identifier | `x509` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N130 | 321:63 | [11811, 11814) | `TLS` | identifier | `TLS_SERVER_NAME` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N131 | 340:18 | [12463, 12468) | `X.509` | string | `"X.509 self-signed"` | Output label passed to emit(); printed text only |
| PY-N132 | 343:8 | [12514, 12517) | `TLS` | comment | `# S24: TLS 1.3-only client context (no connection is made)` | Comment text; documentation only |
| PY-N133 | 344:9 | [12574, 12579) | `tls13` | identifier | `s24_tls13_client` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N134 | 349:18 | [12798, 12801) | `TLS` | string | `"TLS 1.3 client"` | Output label passed to emit(); printed text only |
| PY-N135 | 354:13 | [12890, 12896) | `sha256` | identifier | `s01_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N136 | 354:30 | [12907, 12911) | `sha3` | identifier | `s02_sha2_sha3_blake2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N137 | 354:35 | [12912, 12918) | `blake2` | identifier | `s02_sha2_sha3_blake2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N138 | 354:66 | [12943, 12951) | `shake128` | identifier | `s04_shake128` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N139 | 355:13 | [12965, 12969) | `hmac` | identifier | `s05_hmac_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N140 | 355:18 | [12970, 12976) | `sha256` | identifier | `s05_hmac_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N141 | 355:30 | [12982, 12986) | `hkdf` | identifier | `s06_hkdf_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N142 | 355:35 | [12987, 12993) | `sha256` | identifier | `s06_hkdf_sha256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N143 | 355:47 | [12999, 13005) | `pbkdf2` | identifier | `s07_pbkdf2` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N144 | 355:59 | [13011, 13017) | `scrypt` | identifier | `s08_scrypt` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N145 | 355:71 | [13023, 13031) | `argon2id` | identifier | `s09_argon2id` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N146 | 356:13 | [13045, 13051) | `bcrypt` | identifier | `s10_bcrypt` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N147 | 356:25 | [13057, 13063) | `aes256` | identifier | `s11_aes256_gcm` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N148 | 356:32 | [13064, 13067) | `gcm` | identifier | `s11_aes256_gcm` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N149 | 356:41 | [13073, 13081) | `chacha20` | identifier | `s12_chacha20_poly1305` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N150 | 356:50 | [13082, 13090) | `poly1305` | identifier | `s12_chacha20_poly1305` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N151 | 356:64 | [13096, 13102) | `aes256` | identifier | `s13_aes256_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N152 | 356:71 | [13103, 13106) | `cbc` | identifier | `s13_aes256_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N153 | 357:13 | [13120, 13126) | `aes128` | identifier | `s14_aes128_ecb` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N154 | 357:20 | [13127, 13130) | `ecb` | identifier | `s14_aes128_ecb` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N155 | 357:29 | [13136, 13142) | `aes256` | identifier | `s15_aes256_ctr` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N156 | 357:36 | [13143, 13146) | `ctr` | identifier | `s15_aes256_ctr` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N157 | 357:45 | [13152, 13156) | `tdea` | identifier | `s16_tdea_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N158 | 357:50 | [13157, 13160) | `cbc` | identifier | `s16_tdea_cbc` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N159 | 357:59 | [13166, 13169) | `rsa` | identifier | `s17_rsa3072` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N160 | 357:72 | [13179, 13184) | `ecdsa` | identifier | `s18_ecdsa_p256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N161 | 357:78 | [13185, 13189) | `p256` | identifier | `s18_ecdsa_p256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N162 | 358:13 | [13203, 13210) | `ed25519` | identifier | `s19_ed25519` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N163 | 359:13 | [13274, 13278) | `x509` | identifier | `s23_x509_self_signed` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| PY-N164 | 359:35 | [13296, 13301) | `tls13` | identifier | `s24_tls13_client` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |

## Implicit and runtime-dependent cryptography

Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where source-level ground truth and the cryptography that actually executes can diverge.

| Asset | What happens |
|---|---|
| `csprng` | os.urandom and secrets use getrandom(2); Crypto.Random.get_random_bytes and bcrypt.gensalt wrap os.urandom; key generation inside pyca/cryptography uses the bundled OpenSSL RAND_bytes; PyNaCl is not used for randomness here. |
| `aes-256-gcm` | AESGCM tag length is implicitly 16 bytes. |
| `argon2id` | Argon2 version 0x13 is the implicit argon2-cffi default. |
| `ecdsa-p256-sha256` | ECDSA signatures are DER-encoded (cryptography default). |
| `ml-dsa-65` | Hedged signing and an empty context string are implicit defaults. |
| `tls13-client` | TLS 1.3 cipher suites cannot be set from Python's ssl module; the effective suites are the OpenSSL defaults (TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_GCM_SHA256). Key-exchange groups are the system OpenSSL 3.0 defaults, which contain no post-quantum hybrid. |
| `sha-512` | Ed25519 (PyNaCl/libsodium) uses SHA-512 internally. |

## Detection notes

Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.

| Note | Explanation | Occurrences |
|---|---|---|
| `usedforsecurity` | usedforsecurity=False declares a non-security use; the MD5 asset still exists but a policy engine may lower its severity. | PY-047 |
| `digestmod` | Hash constructor passed as HMAC digestmod (function object, not a call). | PY-054 |
| `hash-name-string` | Hash chosen by the lowercase string 'sha256'; normalise to SHA-256. | PY-060 |
| `computed` | Parameter is a constant expression, not a literal (evaluates to 16384). | PY-065 |
| `gensalt` | bcrypt.gensalt() draws 16 salt bytes from os.urandom internally. | PY-075 |
| `cost-in-gensalt` | The bcrypt work factor is passed to the salt generator, not to hashpw(). | PY-076 |
| `keysize-from-key` | Key size is not named in code; it follows from the length of the key bytes (data-flow dependent). | PY-079, PY-096, PY-103 |
| `padding` | PKCS#7 padding object (block-size argument 128 is in bits). | PY-094, PY-100, PY-101 |
| `ctr-full-block` | nonce=b'' with a 16-byte initial_value makes the whole block a 128-bit big-endian counter (same as Java/Go/Node/BC). | PY-110, PY-113 |
| `parity` | Sets DES parity bits; PyCryptodome rejects degenerate keys (K1==K2 or K2==K3). | PY-116 |
| `pad-default-pkcs7` | pad()/unpad() default to style='pkcs7'; the padding scheme is implicit. | PY-124, PY-127 |
| `seed-ctor` | Key pair is derived deterministically from the hard-coded 32-byte seed. | PY-159 |
| `serial` | CSPRNG output used for the certificate serial number (not key material). | PY-187 |
| `hash-from-cert` | Hash algorithm is read from the certificate at run time (signature_hash_algorithm). | PY-192 |

## Machine-readable files

`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset (with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts (NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.
