# CBOM ground-truth corpus - C#

`Program.cs` is the C# implementation of a 24-scenario cryptography program that is logically identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic asset appears in it: **212 occurrences** of **85 assets** (34 algorithms, 49 items of related crypto material, 1 certificate, 1 protocol) drawn from **2 library components**, plus **95 non-asset mentions** of algorithm names that a scanner should *not* report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.

## Files

| File | Purpose |
|---|---|
| `Program.cs` | The program (407 lines, ASCII, LF line endings) |
| `CryptoShowcase.csproj` | Build manifest |
| `README.md` | This document |
| `cbom.cdx.json` | Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema) |
| `ground-truth.json` | Complete occurrence ledger, asset inventory and non-asset mentions |

## Build and run

```sh
dotnet run -c Release
```

Verified in the build environment with .NET SDK 10.0.113 (runtime 10.0.13): dotnet build -c Release against BouncyCastle.Cryptography 2.7.0 compiled from the release-2.7.0 tag; 0 warnings. Standard output was byte-identical to the other four implementations (see the corpus README).

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
| Occurrences | 212 |
| Occurrences with role `imp` | 11 |
| Occurrences with role `typ` | 3 |
| Occurrences with role `alg` | 38 |
| Occurrences with role `spec` | 8 |
| Occurrences with role `ctor` | 25 |
| Occurrences with role `init` | 14 |
| Occurrences with role `op` | 65 |
| Occurrences with role `prm` | 30 |
| Occurrences with role `mat` | 16 |
| Occurrences with role `cfg` | 2 |
| Algorithm assets (incl. implicit) | 34 |
| Implicit assets (no source occurrence) | 3 |
| Related crypto material | 49 |
| Certificates | 1 |
| Protocols | 1 |
| Library components | 2 |
| Non-asset mentions | 95 |

## Libraries

| ID | Component | Version | purl | License | Scope | Import occurrences | Other occurrences | Assets provided | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `lib.dotnet` | .NET base class library | 10.0.13 | `pkg:generic/dotnet-runtime@10.0.13` | MIT | runtime | CS-001, CS-002, CS-003, CS-004 | 117 | sha-256, sha-512, md5, sha-1, shake128, hmac-sha256, hkdf-sha256, pbkdf2-hmac-sha256, argon2id, aes-256-gcm, chacha20-poly1305, aes-256-cbc, aes-128-ecb, 3des-cbc, rsa-3072, rsa-oaep-sha256, rsassa-pss-sha256, rsassa-pkcs1v15-sha256, ecdsa-p256-sha256, ecdh-p256, csprng, cert.self-signed, tls13-client, m.hmac-key, m.hkdf-ikm, m.hkdf-salt, m.hkdf-info, m.pbkdf2-password, m.pbkdf2-salt, m.scrypt-password, m.scrypt-salt, m.password, m.argon2-salt, m.bcrypt-salt, m.gcm-key, m.gcm-iv, m.gcm-aad, m.chacha-key, m.chacha-nonce, m.cbc-iv, m.ecb-key, m.ctr-key, m.ctr-iv, m.tdes-iv, m.ed25519-seed, m.session-info | System.Security.Cryptography, System.Net.Security; on Linux backed by the system OpenSSL (3.0.13 in the verification environment) |
| `lib.bccs` | BouncyCastle.Cryptography | 2.7.0 | `pkg:nuget/BouncyCastle.Cryptography@2.7.0` | MIT | required | CS-005, CS-006, CS-007, CS-008, CS-009, CS-010, CS-011 | 84 | sha3-256, blake2b-512, shake128, scrypt, argon2id, bcrypt, aes-256-ctr, x25519, ed25519, ml-kem-768, ml-dsa-65, bc-digest-drbg | Managed implementations: SHA3, SHAKE, BLAKE2b, scrypt, Argon2, bcrypt, AES-CTR, Ed25519, X25519, ML-KEM, ML-DSA |

## Algorithm assets

Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):

| Asset | Name | Primitive | Family | Parameter set | Mode | Padding | Curve | Functions | OID | Occurrences | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.1 | 12 | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | - | - | - | 2.16.840.1.101.3.4.2.2 | implicit | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | - | - | digest | 2.16.840.1.101.3.4.2.3 | 1 | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.8 | 2 | - |
| `blake2b-512` | BLAKE2b-512 | hash | BLAKE2 | 512 | - | - | - | digest | 1.3.6.1.4.1.1722.12.2.1.16 | 3 | - |
| `md5` | MD5 | hash | MD5 | 128 | - | - | - | digest | 1.2.840.113549.2.5 | 1 | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | - | - | digest | 1.3.14.3.2.26 | 1 | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | - | - | digest | 2.16.840.1.101.3.4.2.11 | 4 | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | - | - | tag | 1.2.840.113549.2.9 | 1 | sha-256 |
| `hkdf-sha256` | HKDF-SHA256 | kdf | HKDF | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.9.16.3.29 | 6 | hmac-sha256, sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.5.12 | 4 | hmac-sha256, sha-256 |
| `scrypt` | scrypt | kdf | scrypt | N=16384,r=8,p=1 | - | - | - | keyderive | 1.3.6.1.4.1.11591.4.11 | 5 | pbkdf2-hmac-sha256 |
| `argon2id` | Argon2id | kdf | Argon2 | t=2,m=19456,p=1,v=0x13 | - | - | - | keyderive | - | 10 | - |
| `bcrypt` | bcrypt | kdf | bcrypt | cost=12 | - | - | - | keyderive, verify | - | 4 | - |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | gcm | - | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.46 | 4 | - |
| `aes-128-gcm` | AES-128-GCM | ae | AES | 128 | gcm | - | - | - | 2.16.840.1.101.3.4.1.6 | implicit | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | other | - | - | decrypt, encrypt | 1.2.840.113549.1.9.16.3.18 | 3 | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | cbc | pkcs7 | - | decrypt, encrypt, keygen | 2.16.840.1.101.3.4.1.42 | 8 | - |
| `aes-128-ecb` | AES-128-ECB-PKCS7 | block-cipher | AES | 128 | ecb | pkcs7 | - | encrypt | 2.16.840.1.101.3.4.1.1 | 4 | - |
| `aes-256-ctr` | AES-256-CTR | block-cipher | AES | 256 | ctr | - | - | decrypt, encrypt | - | 12 | - |
| `3des-cbc` | 3DES-CBC-PKCS7 (3-key TDEA) | block-cipher | 3DES | 168 | cbc | pkcs7 | - | decrypt, encrypt, keygen | 1.2.840.113549.3.7 | 6 | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | - | - | keygen | 1.2.840.113549.1.1.1 | 2 | - |
| `mgf1-sha256` | MGF1-SHA256 | other | MGF1 | SHA-256 | - | - | - | - | 1.2.840.113549.1.1.8 | implicit | sha-256 |
| `rsa-oaep-sha256` | RSAES-OAEP-SHA256 (RSA-3072) | pke | RSA | 3072 | - | oaep | - | decrypt, encrypt | 1.2.840.113549.1.1.7 | 4 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pss-sha256` | RSASSA-PSS-SHA256 (RSA-3072) | signature | RSA | 3072 | - | other | - | sign, verify | 1.2.840.113549.1.1.10 | 6 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pkcs1v15-sha256` | RSASSA-PKCS1-v1_5-SHA256 (RSA-3072) | signature | RSA | 3072 | - | pkcs1v15 | - | sign, verify | 1.2.840.113549.1.1.11 | 6 | rsa-3072, sha-256 |
| `ecdsa-p256-sha256` | ECDSA P-256 with SHA-256 | signature | ECDSA | P-256 | - | - | secp256r1 | keygen, sign, verify | 1.2.840.10045.4.3.2 | 14 | sha-256 |
| `ecdh-p256` | ECDH P-256 | key-agree | ECDH | P-256 | - | - | secp256r1 | keyderive, keygen | 1.3.132.1.12 | 6 | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | - | - | curve25519 | keyderive, keygen | 1.3.101.110 | 7 | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | - | - | edwards25519 | keygen, sign, verify | 1.3.101.112 | 8 | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | - | - | decapsulate, encapsulate, keygen | 2.16.840.1.101.3.4.4.2 | 13 | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | - | - | keygen, sign, verify | 2.16.840.1.101.3.4.3.18 | 16 | - |
| `csprng` | Platform CSPRNG | drbg | CSPRNG | - | - | - | - | generate | - | 8 | - |
| `bc-digest-drbg` | BC DigestRandomGenerator (SHA-256) | drbg | Hash-based PRNG | SHA-256 | - | - | - | - | - | 2 | sha-256 |

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
| `bc-digest-drbg` | - | - | Bouncy Castle C# SecureRandom default | Not a SP 800-90A DRBG | n/a | Not applicable | BC C# 'new SecureRandom()' = SHA-256 DigestRandomGenerator auto-seeded from the OS RNG. |

Occurrences per algorithm (`direct` = the span names this asset; `parameter:x` = span names x inside this composite; `produced` = span produces this material):

| Asset | Occurrence IDs |
|---|---|
| `sha-256` | CS-030, CS-045, CS-049, CS-128, CS-131, CS-134, CS-137, CS-142, CS-144, CS-159, CS-201, CS-208 |
| `sha-512` | CS-031 |
| `sha3-256` | CS-032, CS-033 |
| `blake2b-512` | CS-034, CS-035, CS-036 |
| `md5` | CS-037 |
| `sha-1` | CS-038 |
| `shake128` | CS-039, CS-040, CS-041, CS-042 |
| `hmac-sha256` | CS-043 |
| `hkdf-sha256` | CS-044, CS-045 (parameter:sha-256), CS-046, CS-158, CS-159 (parameter:sha-256), CS-160 |
| `pbkdf2-hmac-sha256` | CS-047, CS-048, CS-049 (parameter:sha-256), CS-050 |
| `scrypt` | CS-051, CS-052, CS-053, CS-054, CS-055 |
| `argon2id` | CS-056, CS-057, CS-058, CS-059, CS-060, CS-061, CS-062, CS-063, CS-064, CS-065 |
| `bcrypt` | CS-068, CS-069, CS-070, CS-071 |
| `aes-256-gcm` | CS-072, CS-073, CS-074, CS-075 |
| `chacha20-poly1305` | CS-080, CS-081, CS-082 |
| `aes-256-cbc` | CS-083, CS-084, CS-085, CS-086, CS-089, CS-090, CS-091, CS-092 |
| `aes-128-ecb` | CS-093, CS-094, CS-095, CS-096 |
| `aes-256-ctr` | CS-101, CS-102, CS-103, CS-104, CS-105, CS-106, CS-107, CS-108, CS-109, CS-110, CS-111, CS-112 |
| `3des-cbc` | CS-113, CS-114, CS-117, CS-118, CS-119, CS-120 |
| `rsa-3072` | CS-121, CS-122 |
| `rsa-oaep-sha256` | CS-123, CS-124, CS-125, CS-126 |
| `rsassa-pss-sha256` | CS-127, CS-128 (parameter:sha-256), CS-129, CS-130, CS-131 (parameter:sha-256), CS-132 |
| `rsassa-pkcs1v15-sha256` | CS-133, CS-134 (parameter:sha-256), CS-135, CS-136, CS-137 (parameter:sha-256), CS-138 |
| `ecdsa-p256-sha256` | CS-139, CS-140, CS-141, CS-142 (parameter:sha-256), CS-143, CS-144 (parameter:sha-256), CS-198, CS-199, CS-201 (parameter:sha-256), CS-203, CS-206, CS-207, CS-208 (parameter:sha-256), CS-209 |
| `ecdh-p256` | CS-163, CS-164, CS-165, CS-166, CS-167, CS-168 |
| `x25519` | CS-153, CS-154, CS-155, CS-156, CS-157, CS-161, CS-162 |
| `ed25519` | CS-145, CS-146, CS-147, CS-148, CS-149, CS-150, CS-151, CS-152 |
| `ml-kem-768` | CS-169, CS-170, CS-171, CS-172, CS-173, CS-174, CS-175, CS-176, CS-177, CS-178, CS-179, CS-180, CS-181 |
| `ml-dsa-65` | CS-182, CS-183, CS-184, CS-185, CS-186, CS-187, CS-188, CS-189, CS-190, CS-191, CS-192, CS-193, CS-194, CS-195, CS-196, CS-197 |
| `csprng` | CS-066, CS-076, CS-078, CS-087, CS-097, CS-099, CS-115, CS-205 |
| `bc-digest-drbg` | CS-028, CS-029 |
| `cert.self-signed` | CS-200, CS-202, CS-204 |
| `tls13-client` | CS-210, CS-211, CS-212 |

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
| Occurrences | CS-200, CS-202, CS-204 |

| Property | Value |
|---|---|
| Asset | `tls13-client` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_128_GCM_SHA256 (0x13,0x01); TLS_AES_256_GCM_SHA384 (0x13,0x02); TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03) |
| Note | Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime defaults. |
| Occurrences | CS-210, CS-211, CS-212 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Provenance | Test-vector value | Used with | Scenario | Defined / produced at | Note |
|---|---|---|---|---|---|---|---|---|---|
| `m.hmac-key` | HMAC key | secret-key | 24 | hardcoded | "key" (ASCII) | `hmac-sha256` | S05 | CS-012 @ 29:36 | 24-bit key - far below the 112-bit minimum; test vector only |
| `m.hkdf-ikm` | HKDF input keying material | secret-key | 176 | hardcoded | 0x0b * 22 | `hkdf-sha256` | S06 | CS-013 @ 31:36 | RFC 5869 A.1 |
| `m.hkdf-salt` | HKDF salt | salt | 104 | hardcoded | 000102...0c | `hkdf-sha256` | S06 | CS-014 @ 32:36 | RFC 5869 A.1 |
| `m.hkdf-info` | HKDF info | additional-data | 80 | hardcoded | f0f1...f9 | `hkdf-sha256` | S06 | CS-015 @ 33:36 | RFC 5869 A.1 |
| `m.hkdf-okm` | HKDF output keying material | secret-key | 336 | derived | - | `hkdf-sha256` | S06 | CS-044 @ 109:19 (produced) | - |
| `m.pbkdf2-password` | PBKDF2 password | password | 64 | hardcoded | "Password" | `pbkdf2-hmac-sha256` | S07 | CS-016 @ 35:36 | RFC 7914 section 11 |
| `m.pbkdf2-salt` | PBKDF2 salt | salt | 32 | hardcoded | "NaCl" | `pbkdf2-hmac-sha256` | S07 | CS-017 @ 36:36 | 32-bit salt is below the SP 800-132 minimum of 128 bits |
| `m.pbkdf2-dk` | PBKDF2 derived key | secret-key | 512 | derived | - | `pbkdf2-hmac-sha256` | S07 | CS-047 @ 116:23 (produced) | - |
| `m.scrypt-password` | scrypt password | password | 104 | hardcoded | "pleaseletmein" | `scrypt` | S08 | CS-018 @ 37:36 | RFC 7914 section 12 |
| `m.scrypt-salt` | scrypt salt | salt | 112 | hardcoded | "SodiumChloride" | `scrypt` | S08 | CS-019 @ 38:36 | - |
| `m.scrypt-dk` | scrypt derived key | secret-key | 512 | derived | - | `scrypt` | S08 | CS-051 @ 123:23 (produced) | - |
| `m.password` | Application password | password | 224 | hardcoded | "correct horse battery staple" | `argon2id` | S09 | CS-020 @ 39:26 | Shared by S09 (Argon2id) and S10 (bcrypt) |
| `m.argon2-salt` | Argon2id salt | salt | 128 | hardcoded | "cbom-corpus-salt" | `argon2id` | S09 | CS-021 @ 40:36 | - |
| `m.argon2-dk` | Argon2id output | secret-key | 256 | derived | - | `argon2id` | S09 | CS-065 @ 140:9 (produced) | - |
| `m.bcrypt-salt` | bcrypt salt | salt | 128 | csprng | - | `bcrypt` | S10 | CS-066 @ 147:20 (produced); CS-067 @ 147:51 | - |
| `m.bcrypt-hash` | bcrypt hash string | credential | 480 | derived | - | `bcrypt` | S10 | CS-068 @ 148:20 (produced) | 60-character modular-crypt string ($2a$/$2b$) |
| `m.gcm-key` | AES-256-GCM key | secret-key | 256 | hardcoded | feffe992... | `aes-256-gcm` | S11 | CS-022 @ 42:36 | GCM spec test case 16 |
| `m.gcm-iv` | AES-GCM IV | nonce | 96 | hardcoded | cafebabefacedbaddecaf888 | `aes-256-gcm` | S11 | CS-023 @ 43:36 | Static nonce - reuse with the same key is catastrophic outside a KAT |
| `m.gcm-aad` | AES-GCM additional authenticated data | additional-data | 160 | hardcoded | feedface... | `aes-256-gcm` | S11 | CS-024 @ 44:36 | GCM spec test case 16 |
| `m.chacha-key` | ChaCha20-Poly1305 key | secret-key | 256 | csprng | - | `chacha20-poly1305` | S12 | CS-076 @ 168:19 (produced); CS-077 @ 168:50 | - |
| `m.chacha-nonce` | ChaCha20-Poly1305 nonce | nonce | 96 | csprng | - | `chacha20-poly1305` | S12 | CS-078 @ 169:21 (produced); CS-079 @ 169:52 | - |
| `m.cbc-key` | AES-256-CBC key | secret-key | 256 | csprng | - | `aes-256-cbc` | S13 | CS-086 @ 184:9 (produced) | - |
| `m.cbc-iv` | AES-CBC IV | initialization-vector | 128 | csprng | - | `aes-256-cbc` | S13 | CS-087 @ 185:18 (produced); CS-088 @ 185:49 | - |
| `m.ecb-key` | AES-128-ECB key | secret-key | 128 | hardcoded | 000102...0f | `aes-128-ecb` | S14 | CS-025 @ 49:36 | FIPS 197 appendix C.1 |
| `m.ctr-key` | AES-256-CTR key | secret-key | 256 | csprng | - | `aes-256-ctr` | S15 | CS-097 @ 203:19 (produced); CS-098 @ 203:50 | - |
| `m.ctr-iv` | AES-CTR initial counter block | initialization-vector | 128 | csprng | - | `aes-256-ctr` | S15 | CS-099 @ 204:28 (produced); CS-100 @ 204:59 | - |
| `m.tdes-key` | 3DES key | secret-key | 192 | csprng | - | `3des-cbc` | S16 | CS-114 @ 218:9 (produced) | 192 bits incl. parity = 168 effective |
| `m.tdes-iv` | 3DES IV | initialization-vector | 64 | csprng | - | `3des-cbc` | S16 | CS-115 @ 219:18 (produced); CS-116 @ 219:49 | - |
| `m.rsa-private-key` | RSA-3072 private key | private-key | 3072 | keygen | - | `rsa-3072` | S17 | CS-121 @ 228:25 (produced) | - |
| `m.rsa-public-key` | RSA-3072 public key | public-key | 3072 | keygen | - | `rsa-3072` | S17 | CS-121 @ 228:25 (produced) | e = 65537 |
| `m.ecdsa-private-key` | ECDSA P-256 private key | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | CS-139 @ 246:27 (produced) | - |
| `m.ecdsa-public-key` | ECDSA P-256 public key | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | CS-139 @ 246:27 (produced) | - |
| `m.ed25519-seed` | Ed25519 private key seed | private-key | 256 | hardcoded | 9d61b19d... | `ed25519` | S19 | CS-026 @ 52:36 | RFC 8032 section 7.1 TEST 1 |
| `m.ed25519-public-key` | Ed25519 public key | public-key | 256 | derived | d75a9801... | `ed25519` | S19 | CS-146 @ 256:25 (produced) | Derived from the seed |
| `m.x25519-private-key-a` | X25519 private key (party A) | private-key | 256 | keygen | - | `x25519` | S20 | CS-161 @ 285:21 (produced) | - |
| `m.x25519-private-key-b` | X25519 private key (party B) | private-key | 256 | keygen | - | `x25519` | S20 | CS-162 @ 286:19 (produced) | - |
| `m.x25519-shared-secret` | X25519 shared secret | shared-secret | 256 | agreed | - | `x25519` | S20 | CS-157 @ 273:9 (produced) | - |
| `m.ecdh-private-key-a` | ECDH P-256 private key (party A) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | CS-163 @ 291:29 (produced) | - |
| `m.ecdh-private-key-b` | ECDH P-256 private key (party B) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | CS-165 @ 292:27 (produced) | - |
| `m.ecdh-shared-secret` | ECDH P-256 shared secret | shared-secret | 256 | agreed | - | `ecdh-p256` | S20 | CS-167 @ 293:22 (produced); CS-168 @ 294:20 (produced) | - |
| `m.session-info` | Session-key HKDF info | additional-data | 208 | hardcoded | "cbom-corpus session key v1" | `hkdf-sha256` | S20 | CS-027 @ 53:36 | - |
| `m.session-key` | Session key (HKDF over X25519 || ECDH secrets) | secret-key | 256 | derived | - | `hkdf-sha256` | S20 | CS-158 @ 279:16 (produced) | - |
| `m.mlkem-decapsulation-key` | ML-KEM-768 decapsulation key | private-key | - | keygen | - | `ml-kem-768` | S21 | CS-173 @ 307:23 (produced) | 64-byte seed form or 2400-byte expanded form, library-dependent |
| `m.mlkem-encapsulation-key` | ML-KEM-768 encapsulation key | public-key | 9472 | keygen | - | `ml-kem-768` | S21 | CS-173 @ 307:23 (produced) | 1184 bytes |
| `m.mlkem-shared-secret` | ML-KEM-768 shared secret | shared-secret | 256 | agreed | - | `ml-kem-768` | S21 | CS-177 @ 312:9 (produced); CS-181 @ 316:9 (produced) | - |
| `m.mldsa-private-key` | ML-DSA-65 private key | private-key | - | keygen | - | `ml-dsa-65` | S22 | CS-186 @ 325:23 (produced) | 32-byte seed or 4032-byte expanded form, library-dependent |
| `m.mldsa-public-key` | ML-DSA-65 public key | public-key | 15616 | keygen | - | `ml-dsa-65` | S22 | CS-186 @ 325:23 (produced) | 1952 bytes |
| `m.cert-private-key` | Certificate private key (P-256) | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | CS-198 @ 340:25 (produced) | - |
| `m.cert-public-key` | Certificate subject public key (P-256) | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | CS-198 @ 340:25 (produced) | - |

## Scenario map

| Scenario | What it does | Output | Occurrences | Lines | Assets |
|---|---|---|---|---|---|
| S01 | SHA-256 digest of MESSAGE | Known answer (Wikipedia / NIST example message) | 1 | 68-68 | `sha-256` |
| S02 | SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | Known answers | 6 | 74-79 | `sha-512`, `sha3-256`, `blake2b-512` |
| S03 | Legacy MD5 and SHA-1 digests of MESSAGE | Known answers; deliberately weak algorithms | 2 | 86-87 | `md5`, `sha-1` |
| S04 | SHAKE128 XOF, 32-byte output | Known answer | 4 | 93-96 | `shake128` |
| S05 | HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | Known answer (Wikipedia HMAC example) | 2 | 29-103 | `hmac-sha256`, `m.hmac-key` |
| S06 | HKDF-SHA256 extract-and-expand, L=42 | Known answer (RFC 5869 A.1) | 6 | 31-109 | `sha-256`, `hkdf-sha256`, `m.hkdf-ikm`, `m.hkdf-salt`, `m.hkdf-info`, `m.hkdf-okm` |
| S07 | PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | Known answer (RFC 7914 section 11) | 6 | 35-116 | `sha-256`, `pbkdf2-hmac-sha256`, `m.pbkdf2-password`, `m.pbkdf2-salt`, `m.pbkdf2-dk` |
| S08 | scrypt N=16384 r=8 p=1, dkLen=64 | Known answer (RFC 7914 section 12) | 7 | 37-123 | `scrypt`, `m.scrypt-password`, `m.scrypt-salt`, `m.scrypt-dk` |
| S09 | Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | Deterministic; identical across languages | 12 | 39-140 | `argon2id`, `m.password`, `m.argon2-salt`, `m.argon2-dk` |
| S10 | bcrypt cost 12 with random salt, then verify | Randomized; prints verify=true | 6 | 147-149 | `bcrypt`, `csprng`, `m.bcrypt-salt`, `m.bcrypt-hash` |
| S11 | AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | Known answer (GCM spec test case 16) | 7 | 42-161 | `aes-256-gcm`, `m.gcm-key`, `m.gcm-iv`, `m.gcm-aad` |
| S12 | ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | Randomized round trip | 7 | 168-175 | `chacha20-poly1305`, `csprng`, `m.chacha-key`, `m.chacha-nonce` |
| S13 | AES-256-CBC with PKCS#7 padding, random key and IV | Randomized round trip | 10 | 182-187 | `aes-256-cbc`, `csprng`, `m.cbc-key`, `m.cbc-iv` |
| S14 | AES-128-ECB with PKCS#7 padding, hard-coded key | Known answer: first block = FIPS 197 C.1 | 5 | 49-196 | `aes-128-ecb`, `m.ecb-key` |
| S15 | AES-256-CTR, random key and 128-bit initial counter block | Randomized round trip | 16 | 203-210 | `aes-256-ctr`, `csprng`, `m.ctr-key`, `m.ctr-iv` |
| S16 | 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | Randomized round trip | 8 | 217-221 | `3des-cbc`, `csprng`, `m.tdes-key`, `m.tdes-iv` |
| S17 | RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | Randomized | 18 | 228-239 | `sha-256`, `rsa-3072`, `rsa-oaep-sha256`, `rsassa-pss-sha256`, `rsassa-pkcs1v15-sha256`, `m.rsa-private-key`, `m.rsa-public-key` |
| S18 | ECDSA P-256 / SHA-256 sign and verify | Randomized | 6 | 246-248 | `sha-256`, `ecdsa-p256-sha256`, `m.ecdsa-private-key`, `m.ecdsa-public-key` |
| S19 | Ed25519 from a hard-coded seed: public key, signature, verify | Known public key (RFC 8032 test 1); deterministic signature | 9 | 52-264 | `ed25519`, `m.ed25519-seed`, `m.ed25519-public-key` |
| S20 | X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | Randomized; prints agreement booleans | 17 | 53-294 | `sha-256`, `hkdf-sha256`, `ecdh-p256`, `x25519`, `m.x25519-private-key-a`, `m.x25519-private-key-b`, `m.x25519-shared-secret`, `m.ecdh-private-key-a`, `m.ecdh-private-key-b`, `m.ecdh-shared-secret`, `m.session-info`, `m.session-key` |
| S21 | ML-KEM-768 key generation, encapsulation, decapsulation | Randomized; prints sizes | 13 | 305-316 | `ml-kem-768`, `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key`, `m.mlkem-shared-secret` |
| S22 | ML-DSA-65 key generation, signing, verification | Randomized; prints signature size | 16 | 323-333 | `ml-dsa-65`, `m.mldsa-private-key`, `m.mldsa-public-key` |
| S23 | Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | Randomized | 12 | 340-355 | `sha-256`, `ecdsa-p256-sha256`, `csprng`, `cert.self-signed`, `m.cert-private-key`, `m.cert-public-key` |
| S24 | TLS 1.3-only client configuration (no network I/O) | Configuration only | 3 | 362-374 | `tls13-client` |

## Occurrence ledger

Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.

| ID | Scn | Role | Asset (^parent) | Start L:C | End L:C | Chars | Bytes | Len | Nest | Scope | API symbol | Library | Produces | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CS-001 | - | `imp` | `lib.dotnet` | 8:1 | 8:27 | [315, 341) | [315, 341) | 26 | 0 | `<class CryptoShowcase>` | `System.Net.Security` | `lib.dotnet` | - | `using System.Net.Security;` | - |
| CS-002 | - | `imp` | `lib.dotnet` | 9:1 | 9:38 | [342, 379) | [342, 379) | 37 | 0 | `<class CryptoShowcase>` | `System.Security.Authentication` | `lib.dotnet` | - | `using System.Security.Authentication;` | - |
| CS-003 | - | `imp` | `lib.dotnet` | 10:1 | 10:36 | [380, 415) | [380, 415) | 35 | 0 | `<class CryptoShowcase>` | `System.Security.Cryptography` | `lib.dotnet` | - | `using System.Security.Cryptography;` | - |
| CS-004 | - | `imp` | `lib.dotnet` | 11:1 | 11:53 | [416, 468) | [416, 468) | 52 | 0 | `<class CryptoShowcase>` | `System.Security.Cryptography.X509Certificates` | `lib.dotnet` | - | `using System.Security.Cryptography.X509Certificates;` | - |
| CS-005 | - | `imp` | `lib.bccs` | 13:1 | 13:41 | [488, 528) | [488, 528) | 40 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Agreement` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Agreement;` | - |
| CS-006 | - | `imp` | `lib.bccs` | 14:1 | 14:39 | [529, 567) | [529, 567) | 38 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Digests` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Digests;` | - |
| CS-007 | - | `imp` | `lib.bccs` | 15:1 | 15:42 | [568, 609) | [568, 609) | 41 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Generators` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Generators;` | - |
| CS-008 | - | `imp` | `lib.bccs` | 16:1 | 16:36 | [610, 645) | [610, 645) | 35 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Kems` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Kems;` | - |
| CS-009 | - | `imp` | `lib.bccs` | 17:1 | 17:42 | [646, 687) | [646, 687) | 41 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Parameters` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Parameters;` | - |
| CS-010 | - | `imp` | `lib.bccs` | 18:1 | 18:39 | [688, 726) | [688, 726) | 38 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Crypto.Signers` | `lib.bccs` | - | `using Org.BouncyCastle.Crypto.Signers;` | - |
| CS-011 | - | `imp` | `lib.bccs` | 19:1 | 19:33 | [727, 759) | [727, 759) | 32 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Security` | `lib.bccs` | - | `using Org.BouncyCastle.Security;` | - |
| CS-012 | S05 | `mat` | `m.hmac-key` | 29:36 | 29:76 | [1072, 1112) | [1072, 1112) | 40 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `HmacKey = Encoding.ASCII.GetBytes("key")` | - |
| CS-013 | S06 | `mat` | `m.hkdf-ikm` | 31:36 | 31:89 | [1169, 1222) | [1169, 1222) | 53 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `HkdfIkm = Enumerable.Repeat((byte)0x0b, 22).ToArray()` | - |
| CS-014 | S06 | `mat` | `m.hkdf-salt` | 32:36 | 32:98 | [1259, 1321) | [1259, 1321) | 62 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `HkdfSalt = Convert.FromHexString("000102030405060708090a0b0c")` | - |
| CS-015 | S06 | `mat` | `m.hkdf-info` | 33:36 | 33:92 | [1358, 1414) | [1358, 1414) | 56 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `HkdfInfo = Convert.FromHexString("f0f1f2f3f4f5f6f7f8f9")` | - |
| CS-016 | S07 | `mat` | `m.pbkdf2-password` | 35:36 | 35:88 | [1486, 1538) | [1486, 1538) | 52 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `Pbkdf2Password = Encoding.ASCII.GetBytes("Password")` | - |
| CS-017 | S07 | `mat` | `m.pbkdf2-salt` | 36:36 | 36:80 | [1575, 1619) | [1575, 1619) | 44 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `Pbkdf2Salt = Encoding.ASCII.GetBytes("NaCl")` | - |
| CS-018 | S08 | `mat` | `m.scrypt-password` | 37:36 | 37:93 | [1656, 1713) | [1656, 1713) | 57 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `ScryptPassword = Encoding.ASCII.GetBytes("pleaseletmein")` | - |
| CS-019 | S08 | `mat` | `m.scrypt-salt` | 38:36 | 38:90 | [1750, 1804) | [1750, 1804) | 54 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `ScryptSalt = Encoding.ASCII.GetBytes("SodiumChloride")` | - |
| CS-020 | S09 | `mat` | `m.password` | 39:26 | 39:67 | [1831, 1872) | [1831, 1872) | 41 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `Password = "correct horse battery staple"` | - |
| CS-021 | S09 | `mat` | `m.argon2-salt` | 40:36 | 40:92 | [1909, 1965) | [1909, 1965) | 56 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `Argon2Salt = Encoding.ASCII.GetBytes("cbom-corpus-salt")` | - |
| CS-022 | S11 | `mat` | `m.gcm-key` | 42:36 | 42:134 | [2040, 2138) | [2040, 2138) | 98 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `GcmKey = Convert.FromHexString("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")` | - |
| CS-023 | S11 | `mat` | `m.gcm-iv` | 43:36 | 43:93 | [2175, 2232) | [2175, 2232) | 57 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `GcmIv = Convert.FromHexString("cafebabefacedbaddecaf888")` | - |
| CS-024 | S11 | `mat` | `m.gcm-aad` | 44:36 | 44:110 | [2269, 2343) | [2269, 2343) | 74 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `GcmAad = Convert.FromHexString("feedfacedeadbeeffeedfacedeadbeefabaddad2")` | - |
| CS-025 | S14 | `mat` | `m.ecb-key` | 49:36 | 49:102 | [2628, 2694) | [2628, 2694) | 66 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `EcbKey = Convert.FromHexString("000102030405060708090a0b0c0d0e0f")` | - |
| CS-026 | S19 | `mat` | `m.ed25519-seed` | 52:36 | 52:139 | [2876, 2979) | [2876, 2979) | 103 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `Ed25519Seed = Convert.FromHexString("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")` | - |
| CS-027 | S20 | `mat` | `m.session-info` | 53:36 | 53:103 | [3016, 3083) | [3016, 3083) | 67 | 0 | `<class CryptoShowcase>` | - | `lib.dotnet` | - | `SessionInfo = Encoding.ASCII.GetBytes("cbom-corpus session key v1")` | - |
| CS-028 | shared | `typ` | `bc-digest-drbg` | 56:29 | 56:41 | [3178, 3190) | [3178, 3190) | 12 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Security.SecureRandom` | `lib.bccs` | - | `SecureRandom` | - |
| CS-029 | shared | `ctor` | `bc-digest-drbg` | 56:53 | 56:71 | [3202, 3220) | [3202, 3220) | 18 | 0 | `<class CryptoShowcase>` | `Org.BouncyCastle.Security.SecureRandom..ctor` | `lib.bccs` | - | `new SecureRandom()` | - |
| CS-030 | S01 | `op:digest` | `sha-256` | 68:36 | 68:60 | [3633, 3657) | [3633, 3657) | 24 | 0 | `S01Sha256` | `System.Security.Cryptography.SHA256.HashData` | `lib.dotnet` | - | `SHA256.HashData(Message)` | - |
| CS-031 | S02 | `op:digest` | `sha-512` | 74:36 | 74:60 | [3796, 3820) | [3796, 3820) | 24 | 0 | `S02Sha2Sha3Blake2` | `System.Security.Cryptography.SHA512.HashData` | `lib.dotnet` | - | `SHA512.HashData(Message)` | - |
| CS-032 | S02 | `op:digest` | `sha3-256` | 75:37 | 75:89 | [3860, 3912) | [3860, 3912) | 52 | 0 | `S02Sha2Sha3Blake2` | `Org.BouncyCastle.Security.DigestUtilities.CalculateDigest` | `lib.bccs` | - | `DigestUtilities.CalculateDigest("SHA3-256", Message)` | - |
| CS-033 | S02 | `alg` | `sha3-256` | 75:69 | 75:79 | [3892, 3902) | [3892, 3902) | 10 | 1 | `S02Sha2Sha3Blake2` | - | `lib.bccs` | - | `"SHA3-256"` | - |
| CS-034 | S02 | `ctor` | `blake2b-512` | 76:21 | 76:43 | [3936, 3958) | [3936, 3958) | 22 | 0 | `S02Sha2Sha3Blake2` | `Org.BouncyCastle.Crypto.Digests.Blake2bDigest..ctor` | `lib.bccs` | - | `new Blake2bDigest(512)` | - |
| CS-035 | S02 | `prm:digest-size-bits` | `blake2b-512` | 76:39 | 76:42 | [3954, 3957) | [3954, 3957) | 3 | 1 | `S02Sha2Sha3Blake2` | - | `lib.bccs` | - | `512` | - |
| CS-036 | S02 | `op:digest` | `blake2b-512` | 79:9 | 79:33 | [4077, 4101) | [4077, 4101) | 24 | 0 | `S02Sha2Sha3Blake2` | `Org.BouncyCastle.Crypto.Digests.Blake2bDigest.DoFinal` | `lib.bccs` | - | `blake.DoFinal(output, 0)` | - |
| CS-037 | S03 | `op:digest` | `md5` | 86:32 | 86:53 | [4285, 4306) | [4285, 4306) | 21 | 0 | `S03LegacyHashes` | `System.Security.Cryptography.MD5.HashData` | `lib.dotnet` | - | `MD5.HashData(Message)` | - |
| CS-038 | S03 | `op:digest` | `sha-1` | 87:34 | 87:56 | [4343, 4365) | [4343, 4365) | 22 | 0 | `S03LegacyHashes` | `System.Security.Cryptography.SHA1.HashData` | `lib.dotnet` | - | `SHA1.HashData(Message)` | - |
| CS-039 | S04 | `ctor` | `shake128` | 93:21 | 93:41 | [4488, 4508) | [4488, 4508) | 20 | 0 | `S04Shake128` | `Org.BouncyCastle.Crypto.Digests.ShakeDigest..ctor` | `lib.bccs` | - | `new ShakeDigest(128)` | - |
| CS-040 | S04 | `prm:security-strength-bits` | `shake128` | 93:37 | 93:40 | [4504, 4507) | [4504, 4507) | 3 | 1 | `S04Shake128` | - | `lib.bccs` | - | `128` | - |
| CS-041 | S04 | `prm:output-length-bytes` | `shake128` | 95:31 | 95:33 | [4595, 4597) | [4595, 4597) | 2 | 0 | `S04Shake128` | - | `lib.dotnet` | - | `32` | - |
| CS-042 | S04 | `op:digest` | `shake128` | 96:9 | 96:52 | [4608, 4651) | [4608, 4651) | 43 | 0 | `S04Shake128` | `Org.BouncyCastle.Crypto.Digests.ShakeDigest.OutputFinal` | `lib.bccs` | - | `shake.OutputFinal(output, 0, output.Length)` | - |
| CS-043 | S05 | `op:tag` | `hmac-sha256` | 103:40 | 103:77 | [4815, 4852) | [4815, 4852) | 37 | 0 | `S05HmacSha256` | `System.Security.Cryptography.HMACSHA256.HashData` | `lib.dotnet` | - | `HMACSHA256.HashData(HmacKey, Message)` | - |
| CS-044 | S06 | `op:keyderive` | `hkdf-sha256` | 109:19 | 109:92 | [4962, 5035) | [4962, 5035) | 73 | 0 | `S06HkdfSha256` | `System.Security.Cryptography.HKDF.DeriveKey` | `lib.dotnet` | `m.hkdf-okm` | `HKDF.DeriveKey(HashAlgorithmName.SHA256, HkdfIkm, 42, HkdfSalt, HkdfInfo)` | - |
| CS-045 | S06 | `alg` | `sha-256` ^`hkdf-sha256` | 109:34 | 109:58 | [4977, 5001) | [4977, 5001) | 24 | 1 | `S06HkdfSha256` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-046 | S06 | `prm:output-length-bytes` | `hkdf-sha256` | 109:69 | 109:71 | [5012, 5014) | [5012, 5014) | 2 | 1 | `S06HkdfSha256` | - | `lib.dotnet` | - | `42` | - |
| CS-047 | S07 | `op:keyderive` | `pbkdf2-hmac-sha256` | 116:23 | 116:114 | [5185, 5276) | [5185, 5276) | 91 | 0 | `S07Pbkdf2` | `System.Security.Cryptography.Rfc2898DeriveBytes.Pbkdf2` | `lib.dotnet` | `m.pbkdf2-dk` | `Rfc2898DeriveBytes.Pbkdf2(Pbkdf2Password, Pbkdf2Salt, 80_000, HashAlgorithmName.SHA256, 64)` | - |
| CS-048 | S07 | `prm:iterations` | `pbkdf2-hmac-sha256` | 116:77 | 116:83 | [5239, 5245) | [5239, 5245) | 6 | 1 | `S07Pbkdf2` | - | `lib.dotnet` | - | `80_000` | - |
| CS-049 | S07 | `alg` | `sha-256` ^`pbkdf2-hmac-sha256` | 116:85 | 116:109 | [5247, 5271) | [5247, 5271) | 24 | 1 | `S07Pbkdf2` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-050 | S07 | `prm:output-length-bytes` | `pbkdf2-hmac-sha256` | 116:111 | 116:113 | [5273, 5275) | [5273, 5275) | 2 | 1 | `S07Pbkdf2` | - | `lib.dotnet` | - | `64` | - |
| CS-051 | S08 | `op:keyderive` | `scrypt` | 123:23 | 123:85 | [5420, 5482) | [5420, 5482) | 62 | 0 | `S08Scrypt` | `Org.BouncyCastle.Crypto.Generators.SCrypt.Generate` | `lib.bccs` | `m.scrypt-dk` | `SCrypt.Generate(ScryptPassword, ScryptSalt, 1 << 14, 8, 1, 64)` | - |
| CS-052 | S08 | `prm:N` | `scrypt` | 123:67 | 123:74 | [5464, 5471) | [5464, 5471) | 7 | 1 | `S08Scrypt` | - | `lib.bccs` | - | `1 << 14` | computed |
| CS-053 | S08 | `prm:r` | `scrypt` | 123:76 | 123:77 | [5473, 5474) | [5473, 5474) | 1 | 1 | `S08Scrypt` | - | `lib.bccs` | - | `8` | - |
| CS-054 | S08 | `prm:p` | `scrypt` | 123:79 | 123:80 | [5476, 5477) | [5476, 5477) | 1 | 1 | `S08Scrypt` | - | `lib.bccs` | - | `1` | - |
| CS-055 | S08 | `prm:output-length-bytes` | `scrypt` | 123:82 | 123:84 | [5479, 5481) | [5479, 5481) | 2 | 1 | `S08Scrypt` | - | `lib.bccs` | - | `64` | - |
| CS-056 | S09 | `spec` | `argon2id` | 130:26 | 136:21 | [5626, 5888) | [5626, 5888) | 262 | 0 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Parameters.Argon2Parameters.Builder` | `lib.bccs` | - | `new Argon2Parameters.Builder(Argon2Parameters.Argon2id) … (+6 lines)` | - |
| CS-057 | S09 | `alg` | `argon2id` | 130:55 | 130:80 | [5655, 5680) | [5655, 5680) | 25 | 1 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Parameters.Argon2Parameters.Argon2id` | `lib.bccs` | - | `Argon2Parameters.Argon2id` | - |
| CS-058 | S09 | `prm:version` | `argon2id` | 131:26 | 131:52 | [5707, 5733) | [5707, 5733) | 26 | 1 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Parameters.Argon2Parameters.Version13` | `lib.bccs` | - | `Argon2Parameters.Version13` | - |
| CS-059 | S09 | `prm:iterations` | `argon2id` | 132:29 | 132:30 | [5763, 5764) | [5763, 5764) | 1 | 1 | `S09Argon2id` | - | `lib.bccs` | - | `2` | - |
| CS-060 | S09 | `prm:memory-kib` | `argon2id` | 133:29 | 133:35 | [5794, 5800) | [5794, 5800) | 6 | 1 | `S09Argon2id` | - | `lib.bccs` | - | `19_456` | - |
| CS-061 | S09 | `prm:parallelism` | `argon2id` | 134:30 | 134:31 | [5831, 5832) | [5831, 5832) | 1 | 1 | `S09Argon2id` | - | `lib.bccs` | - | `1` | - |
| CS-062 | S09 | `ctor` | `argon2id` | 137:25 | 137:51 | [5914, 5940) | [5914, 5940) | 26 | 0 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Generators.Argon2BytesGenerator..ctor` | `lib.bccs` | - | `new Argon2BytesGenerator()` | - |
| CS-063 | S09 | `init` | `argon2id` | 138:9 | 138:35 | [5950, 5976) | [5950, 5976) | 26 | 0 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Generators.Argon2BytesGenerator.Init` | `lib.bccs` | - | `generator.Init(parameters)` | - |
| CS-064 | S09 | `prm:output-length-bytes` | `argon2id` | 139:31 | 139:33 | [6008, 6010) | [6008, 6010) | 2 | 0 | `S09Argon2id` | - | `lib.dotnet` | - | `32` | - |
| CS-065 | S09 | `op:keyderive` | `argon2id` | 140:9 | 140:75 | [6021, 6087) | [6021, 6087) | 66 | 0 | `S09Argon2id` | `Org.BouncyCastle.Crypto.Generators.Argon2BytesGenerator.GenerateBytes` | `lib.bccs` | `m.argon2-dk` | `generator.GenerateBytes(Encoding.ASCII.GetBytes(Password), output)` | - |
| CS-066 | S10 | `op:generate` | `csprng` | 147:20 | 147:54 | [6222, 6256) | [6222, 6256) | 34 | 0 | `S10Bcrypt` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.bcrypt-salt` | `RandomNumberGenerator.GetBytes(16)` | - |
| CS-067 | S10 | `prm:length-bytes` | `m.bcrypt-salt` | 147:51 | 147:53 | [6253, 6255) | [6253, 6255) | 2 | 1 | `S10Bcrypt` | - | `lib.dotnet` | - | `16` | - |
| CS-068 | S10 | `op:keyderive` | `bcrypt` | 148:20 | 148:82 | [6277, 6339) | [6277, 6339) | 62 | 0 | `S10Bcrypt` | `Org.BouncyCastle.Crypto.Generators.OpenBsdBCrypt.Generate` | `lib.bccs` | `m.bcrypt-hash` | `OpenBsdBCrypt.Generate("2b", Password.ToCharArray(), salt, 12)` | - |
| CS-069 | S10 | `alg` | `bcrypt` | 148:43 | 148:47 | [6300, 6304) | [6300, 6304) | 4 | 1 | `S10Bcrypt` | - | `lib.bccs` | - | `"2b"` | bcrypt-version |
| CS-070 | S10 | `prm:cost` | `bcrypt` | 148:79 | 148:81 | [6336, 6338) | [6336, 6338) | 2 | 1 | `S10Bcrypt` | - | `lib.bccs` | - | `12` | - |
| CS-071 | S10 | `op:verify` | `bcrypt` | 149:18 | 149:75 | [6358, 6415) | [6358, 6415) | 57 | 0 | `S10Bcrypt` | `Org.BouncyCastle.Crypto.Generators.OpenBsdBCrypt.CheckPassword` | `lib.bccs` | - | `OpenBsdBCrypt.CheckPassword(hash, Password.ToCharArray())` | - |
| CS-072 | S11 | `ctor` | `aes-256-gcm` | 156:26 | 156:48 | [6589, 6611) | [6589, 6611) | 22 | 0 | `S11Aes256Gcm` | `System.Security.Cryptography.AesGcm..ctor` | `lib.dotnet` | - | `new AesGcm(GcmKey, 16)` | keysize-from-key |
| CS-073 | S11 | `prm:tag-length-bytes` | `aes-256-gcm` | 156:45 | 156:47 | [6608, 6610) | [6608, 6610) | 2 | 1 | `S11Aes256Gcm` | - | `lib.dotnet` | - | `16` | - |
| CS-074 | S11 | `op:encrypt` | `aes-256-gcm` | 159:9 | 159:67 | [6709, 6767) | [6709, 6767) | 58 | 0 | `S11Aes256Gcm` | `System.Security.Cryptography.AesGcm.Encrypt` | `lib.dotnet` | - | `aead.Encrypt(GcmIv, GcmPlaintext, ciphertext, tag, GcmAad)` | - |
| CS-075 | S11 | `op:decrypt` | `aes-256-gcm` | 161:9 | 161:64 | [6830, 6885) | [6830, 6885) | 55 | 0 | `S11Aes256Gcm` | `System.Security.Cryptography.AesGcm.Decrypt` | `lib.dotnet` | - | `aead.Decrypt(GcmIv, ciphertext, tag, plaintext, GcmAad)` | - |
| CS-076 | S12 | `op:generate` | `csprng` | 168:19 | 168:53 | [7146, 7180) | [7146, 7180) | 34 | 0 | `S12ChaCha20Poly1305` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.chacha-key` | `RandomNumberGenerator.GetBytes(32)` | - |
| CS-077 | S12 | `prm:length-bytes` | `m.chacha-key` | 168:50 | 168:52 | [7177, 7179) | [7177, 7179) | 2 | 1 | `S12ChaCha20Poly1305` | - | `lib.dotnet` | - | `32` | - |
| CS-078 | S12 | `op:generate` | `csprng` | 169:21 | 169:55 | [7202, 7236) | [7202, 7236) | 34 | 0 | `S12ChaCha20Poly1305` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.chacha-nonce` | `RandomNumberGenerator.GetBytes(12)` | - |
| CS-079 | S12 | `prm:length-bytes` | `m.chacha-nonce` | 169:52 | 169:54 | [7233, 7235) | [7233, 7235) | 2 | 1 | `S12ChaCha20Poly1305` | - | `lib.dotnet` | - | `12` | - |
| CS-080 | S12 | `ctor` | `chacha20-poly1305` | 170:26 | 170:51 | [7263, 7288) | [7263, 7288) | 25 | 0 | `S12ChaCha20Poly1305` | `System.Security.Cryptography.ChaCha20Poly1305..ctor` | `lib.dotnet` | - | `new ChaCha20Poly1305(key)` | - |
| CS-081 | S12 | `op:encrypt` | `chacha20-poly1305` | 173:9 | 173:54 | [7381, 7426) | [7381, 7426) | 45 | 0 | `S12ChaCha20Poly1305` | `System.Security.Cryptography.ChaCha20Poly1305.Encrypt` | `lib.dotnet` | - | `aead.Encrypt(nonce, Message, ciphertext, tag)` | - |
| CS-082 | S12 | `op:decrypt` | `chacha20-poly1305` | 175:9 | 175:56 | [7489, 7536) | [7489, 7536) | 47 | 0 | `S12ChaCha20Poly1305` | `System.Security.Cryptography.ChaCha20Poly1305.Decrypt` | `lib.dotnet` | - | `aead.Decrypt(nonce, ciphertext, tag, plaintext)` | - |
| CS-083 | S13 | `ctor` | `aes-256-cbc` | 182:25 | 182:37 | [7764, 7776) | [7764, 7776) | 12 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.Aes.Create` | `lib.dotnet` | - | `Aes.Create()` | - |
| CS-084 | S13 | `init` | `aes-256-cbc` | 183:9 | 183:26 | [7786, 7803) | [7786, 7803) | 17 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.SymmetricAlgorithm.KeySize` | `lib.dotnet` | - | `aes.KeySize = 256` | - |
| CS-085 | S13 | `prm:key-size-bits` | `aes-256-cbc` | 183:23 | 183:26 | [7800, 7803) | [7800, 7803) | 3 | 1 | `S13Aes256Cbc` | - | `lib.dotnet` | - | `256` | - |
| CS-086 | S13 | `op:keygen` | `aes-256-cbc` | 184:9 | 184:26 | [7813, 7830) | [7813, 7830) | 17 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.SymmetricAlgorithm.GenerateKey` | `lib.dotnet` | `m.cbc-key` | `aes.GenerateKey()` | - |
| CS-087 | S13 | `op:generate` | `csprng` | 185:18 | 185:52 | [7849, 7883) | [7849, 7883) | 34 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.cbc-iv` | `RandomNumberGenerator.GetBytes(16)` | - |
| CS-088 | S13 | `prm:length-bytes` | `m.cbc-iv` | 185:49 | 185:51 | [7880, 7882) | [7880, 7882) | 2 | 1 | `S13Aes256Cbc` | - | `lib.dotnet` | - | `16` | - |
| CS-089 | S13 | `op:encrypt` | `aes-256-cbc` | 186:26 | 186:72 | [7910, 7956) | [7910, 7956) | 46 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.SymmetricAlgorithm.EncryptCbc` | `lib.dotnet` | - | `aes.EncryptCbc(Message, iv, PaddingMode.PKCS7)` | mode-ctor |
| CS-090 | S13 | `alg` | `aes-256-cbc` | 186:54 | 186:71 | [7938, 7955) | [7938, 7955) | 17 | 1 | `S13Aes256Cbc` | `System.Security.Cryptography.PaddingMode.PKCS7` | `lib.dotnet` | - | `PaddingMode.PKCS7` | - |
| CS-091 | S13 | `op:decrypt` | `aes-256-cbc` | 187:25 | 187:74 | [7982, 8031) | [7982, 8031) | 49 | 0 | `S13Aes256Cbc` | `System.Security.Cryptography.SymmetricAlgorithm.DecryptCbc` | `lib.dotnet` | - | `aes.DecryptCbc(ciphertext, iv, PaddingMode.PKCS7)` | mode-ctor |
| CS-092 | S13 | `alg` | `aes-256-cbc` | 187:56 | 187:73 | [8013, 8030) | [8013, 8030) | 17 | 1 | `S13Aes256Cbc` | `System.Security.Cryptography.PaddingMode.PKCS7` | `lib.dotnet` | - | `PaddingMode.PKCS7` | - |
| CS-093 | S14 | `ctor` | `aes-128-ecb` | 194:25 | 194:37 | [8276, 8288) | [8276, 8288) | 12 | 0 | `S14Aes128Ecb` | `System.Security.Cryptography.Aes.Create` | `lib.dotnet` | - | `Aes.Create()` | - |
| CS-094 | S14 | `init` | `aes-128-ecb` | 195:9 | 195:25 | [8298, 8314) | [8298, 8314) | 16 | 0 | `S14Aes128Ecb` | `System.Security.Cryptography.SymmetricAlgorithm.Key` | `lib.dotnet` | - | `aes.Key = EcbKey` | keysize-from-key |
| CS-095 | S14 | `op:encrypt` | `aes-128-ecb` | 196:26 | 196:73 | [8341, 8388) | [8341, 8388) | 47 | 0 | `S14Aes128Ecb` | `System.Security.Cryptography.SymmetricAlgorithm.EncryptEcb` | `lib.dotnet` | - | `aes.EncryptEcb(EcbPlaintext, PaddingMode.PKCS7)` | mode-ctor |
| CS-096 | S14 | `alg` | `aes-128-ecb` | 196:55 | 196:72 | [8370, 8387) | [8370, 8387) | 17 | 1 | `S14Aes128Ecb` | `System.Security.Cryptography.PaddingMode.PKCS7` | `lib.dotnet` | - | `PaddingMode.PKCS7` | - |
| CS-097 | S15 | `op:generate` | `csprng` | 203:19 | 203:53 | [8575, 8609) | [8575, 8609) | 34 | 0 | `S15Aes256Ctr` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.ctr-key` | `RandomNumberGenerator.GetBytes(32)` | - |
| CS-098 | S15 | `prm:length-bytes` | `m.ctr-key` | 203:50 | 203:52 | [8606, 8608) | [8606, 8608) | 2 | 1 | `S15Aes256Ctr` | - | `lib.dotnet` | - | `32` | - |
| CS-099 | S15 | `op:generate` | `csprng` | 204:28 | 204:62 | [8638, 8672) | [8638, 8672) | 34 | 0 | `S15Aes256Ctr` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.ctr-iv` | `RandomNumberGenerator.GetBytes(16)` | - |
| CS-100 | S15 | `prm:length-bytes` | `m.ctr-iv` | 204:59 | 204:61 | [8669, 8671) | [8669, 8671) | 2 | 1 | `S15Aes256Ctr` | - | `lib.dotnet` | - | `16` | - |
| CS-101 | S15 | `ctor` | `aes-256-ctr` | 205:25 | 205:71 | [8698, 8744) | [8698, 8744) | 46 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Security.CipherUtilities.GetCipher` | `lib.bccs` | - | `CipherUtilities.GetCipher("AES/CTR/NoPadding")` | - |
| CS-102 | S15 | `alg` | `aes-256-ctr` | 205:51 | 205:70 | [8724, 8743) | [8724, 8743) | 19 | 1 | `S15Aes256Ctr` | - | `lib.bccs` | - | `"AES/CTR/NoPadding"` | - |
| CS-103 | S15 | `init:encrypt` | `aes-256-ctr` | 206:9 | 206:88 | [8754, 8833) | [8754, 8833) | 79 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.IBufferedCipher.Init` | `lib.bccs` | - | `encryptor.Init(true, new ParametersWithIV(new KeyParameter(key), counterBlock))` | - |
| CS-104 | S15 | `spec` | `aes-256-ctr` | 206:30 | 206:87 | [8775, 8832) | [8775, 8832) | 57 | 1 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.Parameters.ParametersWithIV..ctor` | `lib.bccs` | - | `new ParametersWithIV(new KeyParameter(key), counterBlock)` | - |
| CS-105 | S15 | `spec` | `aes-256-ctr` | 206:51 | 206:72 | [8796, 8817) | [8796, 8817) | 21 | 2 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.Parameters.KeyParameter..ctor` | `lib.bccs` | - | `new KeyParameter(key)` | keysize-from-key |
| CS-106 | S15 | `op:encrypt` | `aes-256-ctr` | 207:26 | 207:52 | [8860, 8886) | [8860, 8886) | 26 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.IBufferedCipher.DoFinal` | `lib.bccs` | - | `encryptor.DoFinal(Message)` | - |
| CS-107 | S15 | `ctor` | `aes-256-ctr` | 208:25 | 208:71 | [8912, 8958) | [8912, 8958) | 46 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Security.CipherUtilities.GetCipher` | `lib.bccs` | - | `CipherUtilities.GetCipher("AES/CTR/NoPadding")` | - |
| CS-108 | S15 | `alg` | `aes-256-ctr` | 208:51 | 208:70 | [8938, 8957) | [8938, 8957) | 19 | 1 | `S15Aes256Ctr` | - | `lib.bccs` | - | `"AES/CTR/NoPadding"` | - |
| CS-109 | S15 | `init:decrypt` | `aes-256-ctr` | 209:9 | 209:89 | [8968, 9048) | [8968, 9048) | 80 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.IBufferedCipher.Init` | `lib.bccs` | - | `decryptor.Init(false, new ParametersWithIV(new KeyParameter(key), counterBlock))` | - |
| CS-110 | S15 | `spec` | `aes-256-ctr` | 209:31 | 209:88 | [8990, 9047) | [8990, 9047) | 57 | 1 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.Parameters.ParametersWithIV..ctor` | `lib.bccs` | - | `new ParametersWithIV(new KeyParameter(key), counterBlock)` | - |
| CS-111 | S15 | `spec` | `aes-256-ctr` | 209:52 | 209:73 | [9011, 9032) | [9011, 9032) | 21 | 2 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.Parameters.KeyParameter..ctor` | `lib.bccs` | - | `new KeyParameter(key)` | keysize-from-key |
| CS-112 | S15 | `op:decrypt` | `aes-256-ctr` | 210:25 | 210:54 | [9074, 9103) | [9074, 9103) | 29 | 0 | `S15Aes256Ctr` | `Org.BouncyCastle.Crypto.IBufferedCipher.DoFinal` | `lib.bccs` | - | `decryptor.DoFinal(ciphertext)` | - |
| CS-113 | S16 | `ctor` | `3des-cbc` | 217:26 | 217:44 | [9330, 9348) | [9330, 9348) | 18 | 0 | `S16TdeaCbc` | `System.Security.Cryptography.TripleDES.Create` | `lib.dotnet` | - | `TripleDES.Create()` | - |
| CS-114 | S16 | `op:keygen` | `3des-cbc` | 218:9 | 218:27 | [9358, 9376) | [9358, 9376) | 18 | 0 | `S16TdeaCbc` | `System.Security.Cryptography.SymmetricAlgorithm.GenerateKey` | `lib.dotnet` | `m.tdes-key` | `tdes.GenerateKey()` | desede-default-size |
| CS-115 | S16 | `op:generate` | `csprng` | 219:18 | 219:51 | [9395, 9428) | [9395, 9428) | 33 | 0 | `S16TdeaCbc` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | `m.tdes-iv` | `RandomNumberGenerator.GetBytes(8)` | - |
| CS-116 | S16 | `prm:length-bytes` | `m.tdes-iv` | 219:49 | 219:50 | [9426, 9427) | [9426, 9427) | 1 | 1 | `S16TdeaCbc` | - | `lib.dotnet` | - | `8` | - |
| CS-117 | S16 | `op:encrypt` | `3des-cbc` | 220:26 | 220:73 | [9455, 9502) | [9455, 9502) | 47 | 0 | `S16TdeaCbc` | `System.Security.Cryptography.SymmetricAlgorithm.EncryptCbc` | `lib.dotnet` | - | `tdes.EncryptCbc(Message, iv, PaddingMode.PKCS7)` | mode-ctor |
| CS-118 | S16 | `alg` | `3des-cbc` | 220:55 | 220:72 | [9484, 9501) | [9484, 9501) | 17 | 1 | `S16TdeaCbc` | `System.Security.Cryptography.PaddingMode.PKCS7` | `lib.dotnet` | - | `PaddingMode.PKCS7` | - |
| CS-119 | S16 | `op:decrypt` | `3des-cbc` | 221:25 | 221:75 | [9528, 9578) | [9528, 9578) | 50 | 0 | `S16TdeaCbc` | `System.Security.Cryptography.SymmetricAlgorithm.DecryptCbc` | `lib.dotnet` | - | `tdes.DecryptCbc(ciphertext, iv, PaddingMode.PKCS7)` | mode-ctor |
| CS-120 | S16 | `alg` | `3des-cbc` | 221:57 | 221:74 | [9560, 9577) | [9560, 9577) | 17 | 1 | `S16TdeaCbc` | `System.Security.Cryptography.PaddingMode.PKCS7` | `lib.dotnet` | - | `PaddingMode.PKCS7` | - |
| CS-121 | S17 | `op:keygen` | `rsa-3072` | 228:25 | 228:41 | [9818, 9834) | [9818, 9834) | 16 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.Create` | `lib.dotnet` | `m.rsa-private-key`, `m.rsa-public-key` | `RSA.Create(3072)` | lazy-keygen |
| CS-122 | S17 | `prm:key-size-bits` | `rsa-3072` | 228:36 | 228:40 | [9829, 9833) | [9829, 9833) | 4 | 1 | `S17Rsa3072` | - | `lib.dotnet` | - | `3072` | - |
| CS-123 | S17 | `op:encrypt` | `rsa-oaep-sha256` | 230:26 | 230:79 | [9862, 9915) | [9862, 9915) | 53 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.Encrypt` | `lib.dotnet` | - | `rsa.Encrypt(Message, RSAEncryptionPadding.OaepSHA256)` | - |
| CS-124 | S17 | `alg` | `rsa-oaep-sha256` | 230:47 | 230:78 | [9883, 9914) | [9883, 9914) | 31 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSAEncryptionPadding.OaepSHA256` | `lib.dotnet` | - | `RSAEncryptionPadding.OaepSHA256` | oaep-mgf-same-hash |
| CS-125 | S17 | `op:decrypt` | `rsa-oaep-sha256` | 231:25 | 231:81 | [9941, 9997) | [9941, 9997) | 56 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.Decrypt` | `lib.dotnet` | - | `rsa.Decrypt(ciphertext, RSAEncryptionPadding.OaepSHA256)` | - |
| CS-126 | S17 | `alg` | `rsa-oaep-sha256` | 231:49 | 231:80 | [9965, 9996) | [9965, 9996) | 31 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSAEncryptionPadding.OaepSHA256` | `lib.dotnet` | - | `RSAEncryptionPadding.OaepSHA256` | oaep-mgf-same-hash |
| CS-127 | S17 | `op:sign` | `rsassa-pss-sha256` | 234:28 | 234:100 | [10129, 10201) | [10129, 10201) | 72 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.SignData` | `lib.dotnet` | - | `rsa.SignData(Message, HashAlgorithmName.SHA256, RSASignaturePadding.Pss)` | - |
| CS-128 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 234:50 | 234:74 | [10151, 10175) | [10151, 10175) | 24 | 1 | `S17Rsa3072` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-129 | S17 | `alg` | `rsassa-pss-sha256` | 234:76 | 234:99 | [10177, 10200) | [10177, 10200) | 23 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSASignaturePadding.Pss` | `lib.dotnet` | - | `RSASignaturePadding.Pss` | pss-salt-hashlen |
| CS-130 | S17 | `op:verify` | `rsassa-pss-sha256` | 235:21 | 235:109 | [10223, 10311) | [10223, 10311) | 88 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.VerifyData` | `lib.dotnet` | - | `rsa.VerifyData(Message, pssSignature, HashAlgorithmName.SHA256, RSASignaturePadding.Pss)` | - |
| CS-131 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 235:59 | 235:83 | [10261, 10285) | [10261, 10285) | 24 | 1 | `S17Rsa3072` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-132 | S17 | `alg` | `rsassa-pss-sha256` | 235:85 | 235:108 | [10287, 10310) | [10287, 10310) | 23 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSASignaturePadding.Pss` | `lib.dotnet` | - | `RSASignaturePadding.Pss` | pss-salt-hashlen |
| CS-133 | S17 | `op:sign` | `rsassa-pkcs1v15-sha256` | 238:30 | 238:104 | [10405, 10479) | [10405, 10479) | 74 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.SignData` | `lib.dotnet` | - | `rsa.SignData(Message, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1)` | - |
| CS-134 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 238:52 | 238:76 | [10427, 10451) | [10427, 10451) | 24 | 1 | `S17Rsa3072` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-135 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 238:78 | 238:103 | [10453, 10478) | [10453, 10478) | 25 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSASignaturePadding.Pkcs1` | `lib.dotnet` | - | `RSASignaturePadding.Pkcs1` | - |
| CS-136 | S17 | `op:verify` | `rsassa-pkcs1v15-sha256` | 239:23 | 239:115 | [10503, 10595) | [10503, 10595) | 92 | 0 | `S17Rsa3072` | `System.Security.Cryptography.RSA.VerifyData` | `lib.dotnet` | - | `rsa.VerifyData(Message, pkcs1Signature, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1)` | - |
| CS-137 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 239:63 | 239:87 | [10543, 10567) | [10543, 10567) | 24 | 1 | `S17Rsa3072` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-138 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 239:89 | 239:114 | [10569, 10594) | [10569, 10594) | 25 | 1 | `S17Rsa3072` | `System.Security.Cryptography.RSASignaturePadding.Pkcs1` | `lib.dotnet` | - | `RSASignaturePadding.Pkcs1` | - |
| CS-139 | S18 | `op:keygen` | `ecdsa-p256-sha256` | 246:27 | 246:69 | [10781, 10823) | [10781, 10823) | 42 | 0 | `S18EcdsaP256` | `System.Security.Cryptography.ECDsa.Create` | `lib.dotnet` | `m.ecdsa-private-key`, `m.ecdsa-public-key` | `ECDsa.Create(ECCurve.NamedCurves.nistP256)` | - |
| CS-140 | S18 | `alg` | `ecdsa-p256-sha256` | 246:40 | 246:68 | [10794, 10822) | [10794, 10822) | 28 | 1 | `S18EcdsaP256` | `System.Security.Cryptography.ECCurve.NamedCurves.nistP256` | `lib.dotnet` | - | `ECCurve.NamedCurves.nistP256` | - |
| CS-141 | S18 | `op:sign` | `ecdsa-p256-sha256` | 247:25 | 247:74 | [10849, 10898) | [10849, 10898) | 49 | 0 | `S18EcdsaP256` | `System.Security.Cryptography.ECDsa.SignData` | `lib.dotnet` | - | `ecdsa.SignData(Message, HashAlgorithmName.SHA256)` | p1363-default |
| CS-142 | S18 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 247:49 | 247:73 | [10873, 10897) | [10873, 10897) | 24 | 1 | `S18EcdsaP256` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-143 | S18 | `op:verify` | `ecdsa-p256-sha256` | 248:18 | 248:80 | [10917, 10979) | [10917, 10979) | 62 | 0 | `S18EcdsaP256` | `System.Security.Cryptography.ECDsa.VerifyData` | `lib.dotnet` | - | `ecdsa.VerifyData(Message, signature, HashAlgorithmName.SHA256)` | - |
| CS-144 | S18 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 248:55 | 248:79 | [10954, 10978) | [10954, 10978) | 24 | 1 | `S18EcdsaP256` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-145 | S19 | `ctor` | `ed25519` | 255:26 | 255:70 | [11163, 11207) | [11163, 11207) | 44 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Parameters.Ed25519PrivateKeyParameters..ctor` | `lib.bccs` | - | `new Ed25519PrivateKeyParameters(Ed25519Seed)` | seed-ctor |
| CS-146 | S19 | `op:keygen` | `ed25519` | 256:25 | 256:55 | [11233, 11263) | [11233, 11263) | 30 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Parameters.Ed25519PrivateKeyParameters.GeneratePublicKey` | `lib.bccs` | `m.ed25519-public-key` | `privateKey.GeneratePublicKey()` | - |
| CS-147 | S19 | `ctor` | `ed25519` | 257:22 | 257:41 | [11286, 11305) | [11286, 11305) | 19 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer..ctor` | `lib.bccs` | - | `new Ed25519Signer()` | - |
| CS-148 | S19 | `init:sign` | `ed25519` | 258:9 | 258:38 | [11315, 11344) | [11315, 11344) | 29 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer.Init` | `lib.bccs` | - | `signer.Init(true, privateKey)` | - |
| CS-149 | S19 | `op:sign` | `ed25519` | 260:25 | 260:51 | [11426, 11452) | [11426, 11452) | 26 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer.GenerateSignature` | `lib.bccs` | - | `signer.GenerateSignature()` | - |
| CS-150 | S19 | `ctor` | `ed25519` | 261:24 | 261:43 | [11477, 11496) | [11477, 11496) | 19 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer..ctor` | `lib.bccs` | - | `new Ed25519Signer()` | - |
| CS-151 | S19 | `init:verify` | `ed25519` | 262:9 | 262:40 | [11506, 11537) | [11506, 11537) | 31 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer.Init` | `lib.bccs` | - | `verifier.Init(false, publicKey)` | - |
| CS-152 | S19 | `op:verify` | `ed25519` | 264:18 | 264:53 | [11614, 11649) | [11614, 11649) | 35 | 0 | `S19Ed25519` | `Org.BouncyCastle.Crypto.Signers.Ed25519Signer.VerifySignature` | `lib.bccs` | - | `verifier.VerifySignature(signature)` | - |
| CS-153 | S20 | `typ` | `x25519` | 268:39 | 268:65 | [11804, 11830) | [11804, 11830) | 26 | 0 | `X25519Agree` | `Org.BouncyCastle.Crypto.Parameters.X25519PrivateKeyParameters` | `lib.bccs` | - | `X25519PrivateKeyParameters` | - |
| CS-154 | S20 | `typ` | `x25519` | 268:78 | 268:103 | [11843, 11868) | [11843, 11868) | 25 | 0 | `X25519Agree` | `Org.BouncyCastle.Crypto.Parameters.X25519PublicKeyParameters` | `lib.bccs` | - | `X25519PublicKeyParameters` | - |
| CS-155 | S20 | `ctor` | `x25519` | 270:25 | 270:46 | [11908, 11929) | [11908, 11929) | 21 | 0 | `X25519Agree` | `Org.BouncyCastle.Crypto.Agreement.X25519Agreement..ctor` | `lib.bccs` | - | `new X25519Agreement()` | - |
| CS-156 | S20 | `init` | `x25519` | 271:9 | 271:35 | [11939, 11965) | [11939, 11965) | 26 | 0 | `X25519Agree` | `Org.BouncyCastle.Crypto.Agreement.X25519Agreement.Init` | `lib.bccs` | - | `agreement.Init(privateKey)` | - |
| CS-157 | S20 | `op:agree` | `x25519` | 273:9 | 273:57 | [12031, 12079) | [12031, 12079) | 48 | 0 | `X25519Agree` | `Org.BouncyCastle.Crypto.Agreement.X25519Agreement.CalculateAgreement` | `lib.bccs` | `m.x25519-shared-secret` | `agreement.CalculateAgreement(peerKey, secret, 0)` | - |
| CS-158 | S20 | `op:keyderive` | `hkdf-sha256` | 279:16 | 279:105 | [12196, 12285) | [12196, 12285) | 89 | 0 | `DeriveSessionKey` | `System.Security.Cryptography.HKDF.DeriveKey` | `lib.dotnet` | `m.session-key` | `HKDF.DeriveKey(HashAlgorithmName.SHA256, sharedSecret, 32, salt: null, info: SessionInfo)` | - |
| CS-159 | S20 | `alg` | `sha-256` ^`hkdf-sha256` | 279:31 | 279:55 | [12211, 12235) | [12211, 12235) | 24 | 1 | `DeriveSessionKey` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-160 | S20 | `prm:output-length-bytes` | `hkdf-sha256` | 279:71 | 279:73 | [12251, 12253) | [12251, 12253) | 2 | 1 | `DeriveSessionKey` | - | `lib.dotnet` | - | `32` | - |
| CS-161 | S20 | `op:keygen` | `x25519` | 285:21 | 285:61 | [12426, 12466) | [12426, 12466) | 40 | 0 | `S20KeyAgreement` | `Org.BouncyCastle.Crypto.Parameters.X25519PrivateKeyParameters..ctor` | `lib.bccs` | `m.x25519-private-key-a` | `new X25519PrivateKeyParameters(BcRandom)` | - |
| CS-162 | S20 | `op:keygen` | `x25519` | 286:19 | 286:59 | [12486, 12526) | [12486, 12526) | 40 | 0 | `S20KeyAgreement` | `Org.BouncyCastle.Crypto.Parameters.X25519PrivateKeyParameters..ctor` | `lib.bccs` | `m.x25519-private-key-b` | `new X25519PrivateKeyParameters(BcRandom)` | - |
| CS-163 | S20 | `op:keygen` | `ecdh-p256` | 291:29 | 291:81 | [12772, 12824) | [12772, 12824) | 52 | 0 | `S20KeyAgreement` | `System.Security.Cryptography.ECDiffieHellman.Create` | `lib.dotnet` | `m.ecdh-private-key-a` | `ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256)` | - |
| CS-164 | S20 | `alg` | `ecdh-p256` | 291:52 | 291:80 | [12795, 12823) | [12795, 12823) | 28 | 1 | `S20KeyAgreement` | `System.Security.Cryptography.ECCurve.NamedCurves.nistP256` | `lib.dotnet` | - | `ECCurve.NamedCurves.nistP256` | - |
| CS-165 | S20 | `op:keygen` | `ecdh-p256` | 292:27 | 292:79 | [12852, 12904) | [12852, 12904) | 52 | 0 | `S20KeyAgreement` | `System.Security.Cryptography.ECDiffieHellman.Create` | `lib.dotnet` | `m.ecdh-private-key-b` | `ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256)` | - |
| CS-166 | S20 | `alg` | `ecdh-p256` | 292:50 | 292:78 | [12875, 12903) | [12875, 12903) | 28 | 1 | `S20KeyAgreement` | `System.Security.Cryptography.ECCurve.NamedCurves.nistP256` | `lib.dotnet` | - | `ECCurve.NamedCurves.nistP256` | - |
| CS-167 | S20 | `op:agree` | `ecdh-p256` | 293:22 | 293:71 | [12927, 12976) | [12927, 12976) | 49 | 0 | `S20KeyAgreement` | `System.Security.Cryptography.ECDiffieHellman.DeriveRawSecretAgreement` | `lib.dotnet` | `m.ecdh-shared-secret` | `aliceEc.DeriveRawSecretAgreement(bobEc.PublicKey)` | - |
| CS-168 | S20 | `op:agree` | `ecdh-p256` | 294:20 | 294:69 | [12997, 13046) | [12997, 13046) | 49 | 0 | `S20KeyAgreement` | `System.Security.Cryptography.ECDiffieHellman.DeriveRawSecretAgreement` | `lib.dotnet` | `m.ecdh-shared-secret` | `bobEc.DeriveRawSecretAgreement(aliceEc.PublicKey)` | - |
| CS-169 | S21 | `ctor` | `ml-kem-768` | 305:25 | 305:52 | [13462, 13489) | [13462, 13489) | 27 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Generators.MLKemKeyPairGenerator..ctor` | `lib.bccs` | - | `new MLKemKeyPairGenerator()` | - |
| CS-170 | S21 | `init` | `ml-kem-768` | 306:9 | 306:95 | [13499, 13585) | [13499, 13585) | 86 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Generators.MLKemKeyPairGenerator.Init` | `lib.bccs` | - | `generator.Init(new MLKemKeyGenerationParameters(BcRandom, MLKemParameters.ml_kem_768))` | - |
| CS-171 | S21 | `spec` | `ml-kem-768` | 306:24 | 306:94 | [13514, 13584) | [13514, 13584) | 70 | 1 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Parameters.MLKemKeyGenerationParameters..ctor` | `lib.bccs` | - | `new MLKemKeyGenerationParameters(BcRandom, MLKemParameters.ml_kem_768)` | - |
| CS-172 | S21 | `alg` | `ml-kem-768` | 306:67 | 306:93 | [13557, 13583) | [13557, 13583) | 26 | 2 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Parameters.MLKemParameters.ml_kem_768` | `lib.bccs` | - | `MLKemParameters.ml_kem_768` | - |
| CS-173 | S21 | `op:keygen` | `ml-kem-768` | 307:23 | 307:50 | [13609, 13636) | [13609, 13636) | 27 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Generators.MLKemKeyPairGenerator.GenerateKeyPair` | `lib.bccs` | `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key` | `generator.GenerateKeyPair()` | - |
| CS-174 | S21 | `ctor` | `ml-kem-768` | 308:28 | 308:77 | [13665, 13714) | [13665, 13714) | 49 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemEncapsulator..ctor` | `lib.bccs` | - | `new MLKemEncapsulator(MLKemParameters.ml_kem_768)` | - |
| CS-175 | S21 | `alg` | `ml-kem-768` | 308:50 | 308:76 | [13687, 13713) | [13687, 13713) | 26 | 1 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Parameters.MLKemParameters.ml_kem_768` | `lib.bccs` | - | `MLKemParameters.ml_kem_768` | - |
| CS-176 | S21 | `init` | `ml-kem-768` | 309:9 | 309:42 | [13724, 13757) | [13724, 13757) | 33 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemEncapsulator.Init` | `lib.bccs` | - | `encapsulator.Init(keyPair.Public)` | bc-default-random |
| CS-177 | S21 | `op:encapsulate` | `ml-kem-768` | 312:9 | 312:105 | [13900, 13996) | [13900, 13996) | 96 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemEncapsulator.Encapsulate` | `lib.bccs` | `m.mlkem-shared-secret` | `encapsulator.Encapsulate(ciphertext, 0, ciphertext.Length, sharedSecret, 0, sharedSecret.Length)` | - |
| CS-178 | S21 | `ctor` | `ml-kem-768` | 313:28 | 313:77 | [14025, 14074) | [14025, 14074) | 49 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemDecapsulator..ctor` | `lib.bccs` | - | `new MLKemDecapsulator(MLKemParameters.ml_kem_768)` | - |
| CS-179 | S21 | `alg` | `ml-kem-768` | 313:50 | 313:76 | [14047, 14073) | [14047, 14073) | 26 | 1 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Parameters.MLKemParameters.ml_kem_768` | `lib.bccs` | - | `MLKemParameters.ml_kem_768` | - |
| CS-180 | S21 | `init` | `ml-kem-768` | 314:9 | 314:43 | [14084, 14118) | [14084, 14118) | 34 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemDecapsulator.Init` | `lib.bccs` | - | `decapsulator.Init(keyPair.Private)` | - |
| CS-181 | S21 | `op:decapsulate` | `ml-kem-768` | 316:9 | 316:99 | [14189, 14279) | [14189, 14279) | 90 | 0 | `S21MlKem768` | `Org.BouncyCastle.Crypto.Kems.MLKemDecapsulator.Decapsulate` | `lib.bccs` | `m.mlkem-shared-secret` | `decapsulator.Decapsulate(ciphertext, 0, ciphertext.Length, recovered, 0, recovered.Length)` | - |
| CS-182 | S22 | `ctor` | `ml-dsa-65` | 323:25 | 323:52 | [14536, 14563) | [14536, 14563) | 27 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Generators.MLDsaKeyPairGenerator..ctor` | `lib.bccs` | - | `new MLDsaKeyPairGenerator()` | - |
| CS-183 | S22 | `init` | `ml-dsa-65` | 324:9 | 324:94 | [14573, 14658) | [14573, 14658) | 85 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Generators.MLDsaKeyPairGenerator.Init` | `lib.bccs` | - | `generator.Init(new MLDsaKeyGenerationParameters(BcRandom, MLDsaParameters.ml_dsa_65))` | - |
| CS-184 | S22 | `spec` | `ml-dsa-65` | 324:24 | 324:93 | [14588, 14657) | [14588, 14657) | 69 | 1 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Parameters.MLDsaKeyGenerationParameters..ctor` | `lib.bccs` | - | `new MLDsaKeyGenerationParameters(BcRandom, MLDsaParameters.ml_dsa_65)` | - |
| CS-185 | S22 | `alg` | `ml-dsa-65` | 324:67 | 324:92 | [14631, 14656) | [14631, 14656) | 25 | 2 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Parameters.MLDsaParameters.ml_dsa_65` | `lib.bccs` | - | `MLDsaParameters.ml_dsa_65` | - |
| CS-186 | S22 | `op:keygen` | `ml-dsa-65` | 325:23 | 325:50 | [14682, 14709) | [14682, 14709) | 27 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Generators.MLDsaKeyPairGenerator.GenerateKeyPair` | `lib.bccs` | `m.mldsa-private-key`, `m.mldsa-public-key` | `generator.GenerateKeyPair()` | - |
| CS-187 | S22 | `ctor` | `ml-dsa-65` | 326:22 | 326:86 | [14732, 14796) | [14732, 14796) | 64 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner..ctor` | `lib.bccs` | - | `new MLDsaSigner(MLDsaParameters.ml_dsa_65, deterministic: false)` | - |
| CS-188 | S22 | `alg` | `ml-dsa-65` | 326:38 | 326:63 | [14748, 14773) | [14748, 14773) | 25 | 1 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Parameters.MLDsaParameters.ml_dsa_65` | `lib.bccs` | - | `MLDsaParameters.ml_dsa_65` | - |
| CS-189 | S22 | `prm:deterministic` | `ml-dsa-65` | 326:65 | 326:85 | [14775, 14795) | [14775, 14795) | 20 | 1 | `S22MlDsa65` | - | `lib.bccs` | - | `deterministic: false` | hedged |
| CS-190 | S22 | `init:sign` | `ml-dsa-65` | 327:9 | 327:79 | [14806, 14876) | [14806, 14876) | 70 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner.Init` | `lib.bccs` | - | `signer.Init(true, new ParametersWithRandom(keyPair.Private, BcRandom))` | - |
| CS-191 | S22 | `spec` | `ml-dsa-65` | 327:27 | 327:78 | [14824, 14875) | [14824, 14875) | 51 | 1 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Parameters.ParametersWithRandom..ctor` | `lib.bccs` | - | `new ParametersWithRandom(keyPair.Private, BcRandom)` | - |
| CS-192 | S22 | `op:sign` | `ml-dsa-65` | 329:25 | 329:51 | [14958, 14984) | [14958, 14984) | 26 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner.GenerateSignature` | `lib.bccs` | - | `signer.GenerateSignature()` | ctx-default |
| CS-193 | S22 | `ctor` | `ml-dsa-65` | 330:24 | 330:88 | [15009, 15073) | [15009, 15073) | 64 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner..ctor` | `lib.bccs` | - | `new MLDsaSigner(MLDsaParameters.ml_dsa_65, deterministic: false)` | - |
| CS-194 | S22 | `alg` | `ml-dsa-65` | 330:40 | 330:65 | [15025, 15050) | [15025, 15050) | 25 | 1 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Parameters.MLDsaParameters.ml_dsa_65` | `lib.bccs` | - | `MLDsaParameters.ml_dsa_65` | - |
| CS-195 | S22 | `prm:deterministic` | `ml-dsa-65` | 330:67 | 330:87 | [15052, 15072) | [15052, 15072) | 20 | 1 | `S22MlDsa65` | - | `lib.bccs` | - | `deterministic: false` | hedged |
| CS-196 | S22 | `init:verify` | `ml-dsa-65` | 331:9 | 331:45 | [15083, 15119) | [15083, 15119) | 36 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner.Init` | `lib.bccs` | - | `verifier.Init(false, keyPair.Public)` | - |
| CS-197 | S22 | `op:verify` | `ml-dsa-65` | 333:18 | 333:53 | [15196, 15231) | [15196, 15231) | 35 | 0 | `S22MlDsa65` | `Org.BouncyCastle.Crypto.Signers.MLDsaSigner.VerifySignature` | `lib.bccs` | - | `verifier.VerifySignature(signature)` | - |
| CS-198 | S23 | `op:keygen` | `ecdsa-p256-sha256` | 340:25 | 340:67 | [15473, 15515) | [15473, 15515) | 42 | 0 | `S23X509SelfSigned` | `System.Security.Cryptography.ECDsa.Create` | `lib.dotnet` | `m.cert-private-key`, `m.cert-public-key` | `ECDsa.Create(ECCurve.NamedCurves.nistP256)` | - |
| CS-199 | S23 | `alg` | `ecdsa-p256-sha256` | 340:38 | 340:66 | [15486, 15514) | [15486, 15514) | 28 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.ECCurve.NamedCurves.nistP256` | `lib.dotnet` | - | `ECCurve.NamedCurves.nistP256` | - |
| CS-200 | S23 | `ctor` | `cert.self-signed` | 341:23 | 341:99 | [15539, 15615) | [15539, 15615) | 76 | 0 | `S23X509SelfSigned` | `System.Security.Cryptography.X509Certificates.CertificateRequest..ctor` | `lib.dotnet` | - | `new CertificateRequest($"CN={TlsServerName}", key, HashAlgorithmName.SHA256)` | - |
| CS-201 | S23 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 341:74 | 341:98 | [15590, 15614) | [15590, 15614) | 24 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-202 | S23 | `op:sign` | `cert.self-signed` | 343:33 | 348:47 | [15690, 15903) | [15690, 15903) | 213 | 0 | `S23X509SelfSigned` | `System.Security.Cryptography.X509Certificates.CertificateRequest.Create` | `lib.dotnet` | - | `request.Create( … (+5 lines)` | - |
| CS-203 | S23 | `ctor` | `ecdsa-p256-sha256` | 345:13 | 345:55 | [15751, 15793) | [15751, 15793) | 42 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.X509Certificates.X509SignatureGenerator.CreateForECDsa` | `lib.dotnet` | - | `X509SignatureGenerator.CreateForECDsa(key)` | - |
| CS-204 | S23 | `prm:validity-days` | `cert.self-signed` | 347:25 | 347:28 | [15851, 15854) | [15851, 15854) | 3 | 1 | `S23X509SelfSigned` | - | `lib.dotnet` | - | `365` | - |
| CS-205 | S23 | `op:generate` | `csprng` | 348:13 | 348:46 | [15869, 15902) | [15869, 15902) | 33 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.RandomNumberGenerator.GetBytes` | `lib.dotnet` | - | `RandomNumberGenerator.GetBytes(8)` | serial |
| CS-206 | S23 | `ctor` | `ecdsa-p256-sha256` | 354:31 | 354:62 | [16169, 16200) | [16169, 16200) | 31 | 0 | `S23X509SelfSigned` | `System.Security.Cryptography.X509Certificates.ECDsaCertificateExtensions.GetECDsaPublicKey` | `lib.dotnet` | - | `certificate.GetECDsaPublicKey()` | - |
| CS-207 | S23 | `op:verify` | `ecdsa-p256-sha256` | 355:18 | 355:119 | [16220, 16321) | [16220, 16321) | 101 | 0 | `S23X509SelfSigned` | `System.Security.Cryptography.ECDsa.VerifyData` | `lib.dotnet` | - | `publicKey.VerifyData(tbs, signature, HashAlgorithmName.SHA256, DSASignatureFormat.Rfc3279DerSequence)` | der-signature |
| CS-208 | S23 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 355:55 | 355:79 | [16257, 16281) | [16257, 16281) | 24 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.HashAlgorithmName.SHA256` | `lib.dotnet` | - | `HashAlgorithmName.SHA256` | - |
| CS-209 | S23 | `alg` | `ecdsa-p256-sha256` | 355:81 | 355:118 | [16283, 16320) | [16283, 16320) | 37 | 1 | `S23X509SelfSigned` | `System.Security.Cryptography.DSASignatureFormat.Rfc3279DerSequence` | `lib.dotnet` | - | `DSASignatureFormat.Rfc3279DerSequence` | - |
| CS-210 | S24 | `ctor` | `tls13-client` | 362:23 | 366:10 | [16533, 16681) | [16533, 16681) | 148 | 0 | `S24Tls13Client` | `System.Net.Security.SslClientAuthenticationOptions..ctor` | `lib.dotnet` | - | `new SslClientAuthenticationOptions … (+4 lines)` | - |
| CS-211 | S24 | `cfg:versions` | `tls13-client` | 365:35 | 365:53 | [16652, 16670) | [16652, 16670) | 18 | 1 | `S24Tls13Client` | `System.Security.Authentication.SslProtocols.Tls13` | `lib.dotnet` | - | `SslProtocols.Tls13` | - |
| CS-212 | S24 | `cfg:cipher-suites` | `tls13-client` | 369:13 | 374:15 | [16747, 16999) | [16747, 16999) | 252 | 0 | `S24Tls13Client` | `System.Net.Security.CipherSuitesPolicy..ctor` | `lib.dotnet` | - | `options.CipherSuitesPolicy = new CipherSuitesPolicy( … (+5 lines)` | cipher-suites-platform |

## Full text of multi-line evidence

**CS-056** (`argon2id`, 130:26 to 136:21):

```text
new Argon2Parameters.Builder(Argon2Parameters.Argon2id)
            .WithVersion(Argon2Parameters.Version13)
            .WithIterations(2)
            .WithMemoryAsKB(19_456)
            .WithParallelism(1)
            .WithSalt(Argon2Salt)
            .Build()
```

**CS-202** (`cert.self-signed`, 343:33 to 348:47):

```text
request.Create(
            request.SubjectName,
            X509SignatureGenerator.CreateForECDsa(key),
            now.AddMinutes(-1),
            now.AddDays(365),
            RandomNumberGenerator.GetBytes(8))
```

**CS-210** (`tls13-client`, 362:23 to 366:10):

```text
new SslClientAuthenticationOptions
        {
            TargetHost = TlsServerName,
            EnabledSslProtocols = SslProtocols.Tls13,
        }
```

**CS-212** (`tls13-client`, 369:13 to 374:15):

```text
options.CipherSuitesPolicy = new CipherSuitesPolicy(
            [
                TlsCipherSuite.TLS_AES_128_GCM_SHA256,
                TlsCipherSuite.TLS_AES_256_GCM_SHA384,
                TlsCipherSuite.TLS_CHACHA20_POLY1305_SHA256,
            ])
```

## Non-asset mentions (negative ground truth)

Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.

| ID | L:C | Bytes | Match | Context | Containing token / line | Why it is not an asset |
|---|---|---|---|---|---|---|
| CS-N001 | 28:18 | [1020, 1024) | `HMAC` | comment | `// Wikipedia HMAC example key` | Comment text; documentation only |
| CS-N002 | 41:8 | [1974, 1977) | `GCM` | comment | `// GCM specification test case 16` | Comment text; documentation only |
| CS-N003 | 65:13 | [3535, 3542) | `SHA-256` | comment | `// S01: SHA-256 (FIPS 180-4)` | Comment text; documentation only |
| CS-N004 | 68:22 | [3619, 3626) | `SHA-256` | string | `"SHA-256"` | Output label passed to emit(); printed text only |
| CS-N005 | 71:13 | [3680, 3687) | `SHA-512` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| CS-N006 | 71:22 | [3689, 3697) | `SHA3-256` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| CS-N007 | 71:32 | [3699, 3706) | `BLAKE2b` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| CS-N008 | 74:22 | [3782, 3789) | `SHA-512` | string | `"SHA-512"` | Output label passed to emit(); printed text only |
| CS-N009 | 75:22 | [3845, 3853) | `SHA3-256` | string | `"SHA3-256"` | Output label passed to emit(); printed text only |
| CS-N010 | 80:22 | [4124, 4131) | `BLAKE2b` | string | `"BLAKE2b-512"` | Output label passed to emit(); printed text only |
| CS-N011 | 86:22 | [4275, 4278) | `MD5` | string | `"MD5"` | Output label passed to emit(); printed text only |
| CS-N012 | 87:22 | [4331, 4336) | `SHA-1` | string | `"SHA-1"` | Output label passed to emit(); printed text only |
| CS-N013 | 90:13 | [4388, 4396) | `SHAKE128` | comment | `// S04: SHAKE128 extendable-output function` | Comment text; documentation only |
| CS-N014 | 93:13 | [4480, 4485) | `shake` | identifier | `shake` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N015 | 94:9 | [4518, 4523) | `shake` | identifier | `shake` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N016 | 97:22 | [4674, 4682) | `SHAKE128` | string | `"SHAKE128"` | Output label passed to emit(); printed text only |
| CS-N017 | 100:13 | [4718, 4722) | `HMAC` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| CS-N018 | 100:18 | [4723, 4729) | `SHA256` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| CS-N019 | 103:22 | [4797, 4801) | `HMAC` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| CS-N020 | 103:27 | [4802, 4808) | `SHA256` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| CS-N021 | 106:13 | [4875, 4879) | `HKDF` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| CS-N022 | 106:18 | [4880, 4886) | `SHA256` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| CS-N023 | 110:22 | [5058, 5062) | `HKDF` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| CS-N024 | 110:27 | [5063, 5069) | `SHA256` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| CS-N025 | 113:13 | [5102, 5108) | `PBKDF2` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| CS-N026 | 113:20 | [5109, 5113) | `HMAC` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| CS-N027 | 113:25 | [5114, 5120) | `SHA256` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| CS-N028 | 117:22 | [5299, 5305) | `PBKDF2` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| CS-N029 | 117:29 | [5306, 5312) | `SHA256` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| CS-N030 | 120:13 | [5349, 5355) | `scrypt` | comment | `// S08: scrypt` | Comment text; documentation only |
| CS-N031 | 124:22 | [5505, 5511) | `scrypt` | string | `"scrypt"` | Output label passed to emit(); printed text only |
| CS-N032 | 127:13 | [5548, 5556) | `Argon2id` | comment | `// S09: Argon2id` | Comment text; documentation only |
| CS-N033 | 141:22 | [6110, 6118) | `Argon2id` | string | `"Argon2id"` | Output label passed to emit(); printed text only |
| CS-N034 | 144:13 | [6154, 6160) | `bcrypt` | comment | `// S10: bcrypt` | Comment text; documentation only |
| CS-N035 | 150:22 | [6438, 6444) | `bcrypt` | string | `"bcrypt"` | Output label passed to emit(); printed text only |
| CS-N036 | 153:13 | [6489, 6496) | `AES-256` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| CS-N037 | 153:21 | [6497, 6500) | `GCM` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| CS-N038 | 162:22 | [6908, 6915) | `AES-256` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| CS-N039 | 162:30 | [6916, 6919) | `GCM` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| CS-N040 | 165:13 | [7047, 7064) | `ChaCha20-Poly1305` | comment | `// S12: ChaCha20-Poly1305 (RFC 8439)` | Comment text; documentation only |
| CS-N041 | 176:22 | [7559, 7576) | `ChaCha20-Poly1305` | string | `"ChaCha20-Poly1305"` | Output label passed to emit(); printed text only |
| CS-N042 | 179:13 | [7663, 7670) | `AES-256` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| CS-N043 | 179:21 | [7671, 7674) | `CBC` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| CS-N044 | 182:19 | [7758, 7761) | `aes` | identifier | `aes` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N045 | 188:22 | [8054, 8061) | `AES-256` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| CS-N046 | 188:30 | [8062, 8065) | `CBC` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| CS-N047 | 191:13 | [8152, 8159) | `AES-128` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| CS-N048 | 191:21 | [8160, 8163) | `ECB` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| CS-N049 | 194:19 | [8270, 8273) | `aes` | identifier | `aes` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N050 | 197:22 | [8411, 8418) | `AES-128` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| CS-N051 | 197:30 | [8419, 8422) | `ECB` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| CS-N052 | 200:13 | [8462, 8469) | `AES-256` | comment | `// S15: AES-256-CTR (Bouncy Castle; .NET has no CTR mode)` | Comment text; documentation only |
| CS-N053 | 200:21 | [8470, 8473) | `CTR` | comment | `// S15: AES-256-CTR (Bouncy Castle; .NET has no CTR mode)` | Comment text; documentation only |
| CS-N054 | 200:53 | [8502, 8505) | `CTR` | comment | `// S15: AES-256-CTR (Bouncy Castle; .NET has no CTR mode)` | Comment text; documentation only |
| CS-N055 | 211:22 | [9126, 9133) | `AES-256` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| CS-N056 | 211:30 | [9134, 9137) | `CTR` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| CS-N057 | 214:13 | [9224, 9228) | `3DES` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| CS-N058 | 214:19 | [9230, 9234) | `TDEA` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| CS-N059 | 214:25 | [9236, 9239) | `CBC` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| CS-N060 | 222:22 | [9601, 9605) | `3DES` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| CS-N061 | 222:27 | [9606, 9609) | `CBC` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| CS-N062 | 225:13 | [9696, 9699) | `RSA` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| CS-N063 | 225:24 | [9707, 9711) | `OAEP` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| CS-N064 | 225:30 | [9713, 9716) | `PSS` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| CS-N065 | 228:19 | [9812, 9815) | `rsa` | identifier | `rsa` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N066 | 232:22 | [10020, 10023) | `RSA` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| CS-N067 | 232:31 | [10029, 10033) | `OAEP` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| CS-N068 | 236:22 | [10334, 10337) | `RSA` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| CS-N069 | 236:31 | [10343, 10346) | `PSS` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| CS-N070 | 240:22 | [10618, 10621) | `RSA` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| CS-N071 | 240:31 | [10627, 10635) | `PKCS1v15` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| CS-N072 | 243:13 | [10685, 10690) | `ECDSA` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| CS-N073 | 243:19 | [10691, 10696) | `P-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| CS-N074 | 243:30 | [10702, 10709) | `SHA-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| CS-N075 | 246:19 | [10773, 10778) | `ecdsa` | identifier | `ecdsa` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| CS-N076 | 249:22 | [11002, 11007) | `ECDSA` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| CS-N077 | 249:28 | [11008, 11013) | `P-256` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| CS-N078 | 252:13 | [11058, 11065) | `Ed25519` | comment | `// S19: Ed25519 from a fixed seed (RFC 8032)` | Comment text; documentation only |
| CS-N079 | 265:22 | [11672, 11679) | `Ed25519` | string | `"Ed25519"` | Output label passed to emit(); printed text only |
| CS-N080 | 282:13 | [12306, 12312) | `X25519` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| CS-N081 | 282:22 | [12315, 12319) | `ECDH` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| CS-N082 | 282:27 | [12320, 12325) | `P-256` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| CS-N083 | 282:48 | [12341, 12345) | `HKDF` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| CS-N084 | 289:22 | [12679, 12685) | `X25519` | string | `"X25519"` | Output label passed to emit(); printed text only |
| CS-N085 | 295:22 | [13069, 13073) | `ECDH` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| CS-N086 | 295:27 | [13074, 13079) | `P-256` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| CS-N087 | 299:22 | [13279, 13283) | `HKDF` | string | `"HKDF session key"` | Output label passed to emit(); printed text only |
| CS-N088 | 302:13 | [13372, 13382) | `ML-KEM-768` | comment | `// S21: ML-KEM-768 (FIPS 203)` | Comment text; documentation only |
| CS-N089 | 317:22 | [14302, 14312) | `ML-KEM-768` | string | `"ML-KEM-768"` | Output label passed to emit(); printed text only |
| CS-N090 | 320:13 | [14448, 14457) | `ML-DSA-65` | comment | `// S22: ML-DSA-65 (FIPS 204)` | Comment text; documentation only |
| CS-N091 | 334:22 | [15254, 15263) | `ML-DSA-65` | string | `"ML-DSA-65"` | Output label passed to emit(); printed text only |
| CS-N092 | 337:25 | [15343, 15348) | `X.509` | comment | `// S23: self-signed X.509 certificate, signature checked at the ASN.1 level` | Comment text; documentation only |
| CS-N093 | 356:22 | [16344, 16349) | `X.509` | string | `"X.509 self-signed"` | Output label passed to emit(); printed text only |
| CS-N094 | 359:13 | [16406, 16409) | `TLS` | comment | `// S24: TLS 1.3-only client configuration (no connection is made)` | Comment text; documentation only |
| CS-N095 | 377:22 | [17033, 17036) | `TLS` | string | `"TLS 1.3 client"` | Output label passed to emit(); printed text only |

## Implicit and runtime-dependent cryptography

Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where source-level ground truth and the cryptography that actually executes can diverge.

| Asset | What happens |
|---|---|
| `csprng` | RandomNumberGenerator, Aes/TripleDES.GenerateKey, RSA/ECDsa/ECDiffieHellman key generation use OpenSSL RAND_bytes on Linux (BCryptGenRandom on Windows). |
| `bc-digest-drbg` | Bouncy Castle's SecureRandom is a SHA-256 DigestRandomGenerator seeded from the OS; ML-KEM encapsulation uses a second, implicit instance. |
| `rsa-3072` | Public exponent 65537 is implicit; key generation is deferred until first use. |
| `mgf1-sha256` | RSAEncryptionPadding.OaepSHA256 and RSASignaturePadding.Pss imply MGF1-SHA256. |
| `tls13-client` | Cipher suites are only applied on Linux/macOS; on Windows SChannel defaults apply. Key-exchange groups come from the platform TLS stack (system OpenSSL 3.0 here: no post-quantum hybrid). |
| `sha-512` | Bouncy Castle Ed25519 uses SHA-512 internally. |

## Detection notes

Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.

| Note | Explanation | Occurrences |
|---|---|---|
| `computed` | Parameter is a constant expression, not a literal (evaluates to 16384). | CS-052 |
| `bcrypt-version` | Explicit bcrypt version prefix ($2b$). | CS-069 |
| `keysize-from-key` | Key size is not named in code; it follows from the length of the key bytes (data-flow dependent). | CS-072, CS-094, CS-105, CS-111 |
| `mode-ctor` | Mode is named only by the constructor/function name. | CS-089, CS-091, CS-095, CS-117, CS-119 |
| `desede-default-size` | Key size is implicit: SunJCE's DESede KeyGenerator defaults to 168 bits (3-key TDEA). | CS-114 |
| `lazy-keygen` | RSA.Create(3072) defers key generation until first use, so runtime key generation happens inside Encrypt(). | CS-121 |
| `oaep-mgf-same-hash` | MGF1 hash is implicit and equals the OAEP hash (SHA-256); MGF1 has no source occurrence here. | CS-124, CS-126 |
| `pss-salt-hashlen` | RSASignaturePadding.Pss implies MGF1 with the signing hash and a salt equal to the hash length (32 bytes). | CS-129, CS-132 |
| `p1363-default` | ECDsa.SignData returns IEEE P1363 (r||s) signatures by default, not DER. | CS-141 |
| `seed-ctor` | Key pair is derived deterministically from the hard-coded 32-byte seed. | CS-145 |
| `bc-default-random` | Uses BC's default SecureRandom (SHA-256 DigestRandomGenerator) because no random source is passed. | CS-176 |
| `hedged` | Hedged (randomised) ML-DSA signing is selected explicitly; this is the FIPS 204 default. | CS-189, CS-195 |
| `ctx-default` | Empty context string (FIPS 204 pure ML-DSA). | CS-192 |
| `serial` | CSPRNG output used for the certificate serial number (not key material). | CS-205 |
| `der-signature` | Signature format forced to DER (RFC 3279) because X.509 signatures are DER-encoded. | CS-207 |
| `cipher-suites-platform` | CipherSuitesPolicy throws PlatformNotSupportedException on Windows, hence the OS guard. | CS-212 |

## Machine-readable files

`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset (with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts (NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.
