# CBOM ground-truth corpus - Go

`main.go` is the Go implementation of a 24-scenario cryptography program that is logically identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic asset appears in it: **181 occurrences** of **84 assets** (33 algorithms, 49 items of related crypto material, 1 certificate, 1 protocol) drawn from **4 library components**, plus **90 non-asset mentions** of algorithm names that a scanner should *not* report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.

## Files

| File | Purpose |
|---|---|
| `main.go` | The program (418 lines, ASCII, LF line endings) |
| `go.mod` | Build manifest |
| `README.md` | This document |
| `cbom.cdx.json` | Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema) |
| `ground-truth.json` | Complete occurrence ledger, asset inventory and non-asset mentions |

## Build and run

```sh
go mod tidy   # resolves and records go.sum
go run .
```

Verified in the build environment with Go 1.26.8: go build with x/crypto v0.58.0, CIRCL v1.6.5 and x/sys v0.49.0 from tagged sources; gofmt and go vet clean. Standard output was byte-identical to the other four implementations (see the corpus README).

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
| Occurrences | 181 |
| Occurrences with role `imp` | 28 |
| Occurrences with role `typ` | 1 |
| Occurrences with role `alg` | 20 |
| Occurrences with role `spec` | 1 |
| Occurrences with role `ctor` | 16 |
| Occurrences with role `op` | 69 |
| Occurrences with role `prm` | 28 |
| Occurrences with role `mat` | 16 |
| Occurrences with role `cfg` | 2 |
| Algorithm assets (incl. implicit) | 33 |
| Implicit assets (no source occurrence) | 3 |
| Related crypto material | 49 |
| Certificates | 1 |
| Protocols | 1 |
| Library components | 4 |
| Non-asset mentions | 90 |

## Libraries

| ID | Component | Version | purl | License | Scope | Import occurrences | Other occurrences | Assets provided | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `lib.go-stdlib` | Go standard library | 1.26.8 | `pkg:golang/stdlib@1.26.8` | BSD-3-Clause | runtime | GO-001, GO-002, GO-003, GO-004, GO-005, GO-006, GO-007, GO-008, GO-009, GO-010, GO-011, GO-012, GO-013, GO-014, GO-015, GO-016, GO-017, GO-018, GO-019, GO-020, GO-021, GO-022 | 131 | sha-256, sha-512, sha3-256, md5, sha-1, shake128, hmac-sha256, hkdf-sha256, pbkdf2-hmac-sha256, aes-256-gcm, chacha20-poly1305, aes-256-cbc, aes-128-ecb, aes-256-ctr, 3des-cbc, rsa-3072, rsa-oaep-sha256, rsassa-pss-sha256, rsassa-pkcs1v15-sha256, ecdsa-p256-sha256, ecdh-p256, x25519, ed25519, ml-kem-768, csprng, cert.self-signed, tls13-client, m.hmac-key, m.hkdf-ikm, m.hkdf-salt, m.hkdf-info, m.pbkdf2-password, m.pbkdf2-salt, m.scrypt-password, m.scrypt-salt, m.password, m.argon2-salt, m.gcm-key, m.gcm-iv, m.gcm-aad, m.cbc-key, m.cbc-iv, m.ecb-key, m.ctr-key, m.ctr-iv, m.tdes-key, m.tdes-iv, m.ed25519-seed, m.session-info | crypto/* packages, including crypto/mlkem, crypto/hkdf, crypto/pbkdf2 and crypto/sha3 |
| `lib.xcrypto` | golang.org/x/crypto | v0.58.0 | `pkg:golang/golang.org/x/crypto@v0.58.0` | BSD-3-Clause | required | GO-024, GO-025, GO-026, GO-027, GO-028 | 17 | blake2b-512, scrypt, argon2id, bcrypt, chacha20-poly1305, m.chacha-key, m.chacha-nonce | argon2, bcrypt, blake2b, chacha20poly1305, scrypt |
| `lib.circl` | Cloudflare CIRCL | v1.6.5 | `pkg:golang/github.com/cloudflare/circl@v1.6.5` | BSD-3-Clause | required | GO-023 | 5 | ml-dsa-65 | ML-DSA-65 (sign/mldsa/mldsa65) |
| `lib.xsys` | golang.org/x/sys | v0.49.0 | `pkg:golang/golang.org/x/sys@v0.49.0` | BSD-3-Clause | transitive | - | 0 | - | CPU feature detection for x/crypto and CIRCL; not referenced directly |

## Algorithm assets

Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):

| Asset | Name | Primitive | Family | Parameter set | Mode | Padding | Curve | Functions | OID | Occurrences | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.1 | 14 | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | - | - | - | 2.16.840.1.101.3.4.2.2 | implicit | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | - | - | digest | 2.16.840.1.101.3.4.2.3 | 1 | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.8 | 1 | - |
| `blake2b-512` | BLAKE2b-512 | hash | BLAKE2 | 512 | - | - | - | digest | 1.3.6.1.4.1.1722.12.2.1.16 | 1 | - |
| `md5` | MD5 | hash | MD5 | 128 | - | - | - | digest | 1.2.840.113549.2.5 | 1 | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | - | - | digest | 1.3.14.3.2.26 | 1 | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | - | - | digest | 2.16.840.1.101.3.4.2.11 | 2 | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | - | - | tag | 1.2.840.113549.2.9 | 3 | sha-256 |
| `hkdf-sha256` | HKDF-SHA256 | kdf | HKDF | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.9.16.3.29 | 6 | hmac-sha256, sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.5.12 | 4 | hmac-sha256, sha-256 |
| `scrypt` | scrypt | kdf | scrypt | N=16384,r=8,p=1 | - | - | - | keyderive | 1.3.6.1.4.1.11591.4.11 | 5 | pbkdf2-hmac-sha256 |
| `argon2id` | Argon2id | kdf | Argon2 | t=2,m=19456,p=1,v=0x13 | - | - | - | keyderive | - | 5 | - |
| `bcrypt` | bcrypt | kdf | bcrypt | cost=12 | - | - | - | keyderive, verify | - | 3 | - |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | gcm | - | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.46 | 4 | - |
| `aes-128-gcm` | AES-128-GCM | ae | AES | 128 | gcm | - | - | - | 2.16.840.1.101.3.4.1.6 | implicit | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | other | - | - | decrypt, encrypt | 1.2.840.113549.1.9.16.3.18 | 3 | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | cbc | pkcs7 | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.42 | 7 | - |
| `aes-128-ecb` | AES-128-ECB-PKCS7 | block-cipher | AES | 128 | ecb | pkcs7 | - | encrypt | 2.16.840.1.101.3.4.1.1 | 4 | - |
| `aes-256-ctr` | AES-256-CTR | block-cipher | AES | 256 | ctr | - | - | decrypt, encrypt | - | 5 | - |
| `3des-cbc` | 3DES-CBC-PKCS7 (3-key TDEA) | block-cipher | 3DES | 168 | cbc | pkcs7 | - | decrypt, encrypt | 1.2.840.113549.3.7 | 7 | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | - | - | keygen | 1.2.840.113549.1.1.1 | 2 | - |
| `mgf1-sha256` | MGF1-SHA256 | other | MGF1 | SHA-256 | - | - | - | - | 1.2.840.113549.1.1.8 | implicit | sha-256 |
| `rsa-oaep-sha256` | RSAES-OAEP-SHA256 (RSA-3072) | pke | RSA | 3072 | - | oaep | - | decrypt, encrypt | 1.2.840.113549.1.1.7 | 4 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pss-sha256` | RSASSA-PSS-SHA256 (RSA-3072) | signature | RSA | 3072 | - | other | - | sign, verify | 1.2.840.113549.1.1.10 | 7 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pkcs1v15-sha256` | RSASSA-PKCS1-v1_5-SHA256 (RSA-3072) | signature | RSA | 3072 | - | pkcs1v15 | - | sign, verify | 1.2.840.113549.1.1.11 | 5 | rsa-3072, sha-256 |
| `ecdsa-p256-sha256` | ECDSA P-256 with SHA-256 | signature | ECDSA | P-256 | - | - | secp256r1 | keygen, sign, verify | 1.2.840.10045.4.3.2 | 9 | sha-256 |
| `ecdh-p256` | ECDH P-256 | key-agree | ECDH | P-256 | - | - | secp256r1 | keyderive, keygen | 1.3.132.1.12 | 5 | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | - | - | curve25519 | keyderive, keygen | 1.3.101.110 | 5 | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | - | - | edwards25519 | keygen, sign, verify | 1.3.101.112 | 4 | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | - | - | decapsulate, encapsulate, keygen | 2.16.840.1.101.3.4.4.2 | 3 | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | - | - | keygen, sign, verify | 2.16.840.1.101.3.4.3.18 | 5 | - |
| `csprng` | Platform CSPRNG | drbg | CSPRNG | - | - | - | - | generate | - | 9 | - |

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
| `sha-256` | GO-045, GO-054, GO-057, GO-060, GO-125, GO-127, GO-128, GO-129, GO-133, GO-135, GO-137, GO-139, GO-142, GO-150 |
| `sha-512` | GO-046 |
| `sha3-256` | GO-047 |
| `blake2b-512` | GO-048 |
| `md5` | GO-049 |
| `sha-1` | GO-050 |
| `shake128` | GO-051, GO-052 |
| `hmac-sha256` | GO-053, GO-054 (parameter:sha-256), GO-055 |
| `hkdf-sha256` | GO-056, GO-057 (parameter:sha-256), GO-058, GO-149, GO-150 (parameter:sha-256), GO-151 |
| `pbkdf2-hmac-sha256` | GO-059, GO-060 (parameter:sha-256), GO-061, GO-062 |
| `scrypt` | GO-063, GO-064, GO-065, GO-066, GO-067 |
| `argon2id` | GO-068, GO-069, GO-070, GO-071, GO-072 |
| `bcrypt` | GO-073, GO-074, GO-075 |
| `aes-256-gcm` | GO-076, GO-077, GO-078, GO-079 |
| `chacha20-poly1305` | GO-084, GO-085, GO-086 |
| `aes-256-cbc` | GO-091, GO-092, GO-093, GO-094, GO-095, GO-096, GO-097 |
| `aes-128-ecb` | GO-098, GO-099, GO-100, GO-101 |
| `aes-256-ctr` | GO-106, GO-107, GO-108, GO-109, GO-110 |
| `3des-cbc` | GO-115, GO-116, GO-117, GO-118, GO-119, GO-120, GO-121 |
| `rsa-3072` | GO-122, GO-123 |
| `rsa-oaep-sha256` | GO-124, GO-125 (parameter:sha-256), GO-126, GO-127 (parameter:sha-256) |
| `rsassa-pss-sha256` | GO-128 (parameter:sha-256), GO-130, GO-131, GO-132, GO-133 (parameter:sha-256), GO-134, GO-135 (parameter:sha-256) |
| `rsassa-pkcs1v15-sha256` | GO-129 (parameter:sha-256), GO-136, GO-137 (parameter:sha-256), GO-138, GO-139 (parameter:sha-256) |
| `ecdsa-p256-sha256` | GO-140, GO-141, GO-142 (parameter:sha-256), GO-143, GO-144, GO-170, GO-171, GO-175, GO-178 |
| `ecdh-p256` | GO-157, GO-158, GO-159, GO-160, GO-161 |
| `x25519` | GO-152, GO-153, GO-154, GO-155, GO-156 |
| `ed25519` | GO-145, GO-146, GO-147, GO-148 |
| `ml-kem-768` | GO-162, GO-163, GO-164 |
| `ml-dsa-65` | GO-165, GO-166, GO-167, GO-168, GO-169 |
| `csprng` | GO-081, GO-083, GO-088, GO-090, GO-103, GO-105, GO-112, GO-114, GO-172 |
| `cert.self-signed` | GO-173, GO-174, GO-176, GO-177 |
| `tls13-client` | GO-179, GO-180, GO-181 |

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
| Occurrences | GO-173, GO-174, GO-176, GO-177 |

| Property | Value |
|---|---|
| Asset | `tls13-client` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_128_GCM_SHA256 (0x13,0x01); TLS_AES_256_GCM_SHA384 (0x13,0x02); TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03) |
| Note | Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime defaults. |
| Occurrences | GO-179, GO-180, GO-181 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Provenance | Test-vector value | Used with | Scenario | Defined / produced at | Note |
|---|---|---|---|---|---|---|---|---|---|
| `m.hmac-key` | HMAC key | secret-key | 24 | hardcoded | "key" (ASCII) | `hmac-sha256` | S05 | GO-029 @ 50:5 | 24-bit key - far below the 112-bit minimum; test vector only |
| `m.hkdf-ikm` | HKDF input keying material | secret-key | 176 | hardcoded | 0x0b * 22 | `hkdf-sha256` | S06 | GO-030 @ 51:5 | RFC 5869 A.1 |
| `m.hkdf-salt` | HKDF salt | salt | 104 | hardcoded | 000102...0c | `hkdf-sha256` | S06 | GO-031 @ 52:5 | RFC 5869 A.1 |
| `m.hkdf-info` | HKDF info | additional-data | 80 | hardcoded | f0f1...f9 | `hkdf-sha256` | S06 | GO-032 @ 53:5 | RFC 5869 A.1 |
| `m.hkdf-okm` | HKDF output keying material | secret-key | 336 | derived | - | `hkdf-sha256` | S06 | GO-056 @ 142:14 (produced) | - |
| `m.pbkdf2-password` | PBKDF2 password | password | 64 | hardcoded | "Password" | `pbkdf2-hmac-sha256` | S07 | GO-033 @ 54:5 | RFC 7914 section 11 |
| `m.pbkdf2-salt` | PBKDF2 salt | salt | 32 | hardcoded | "NaCl" | `pbkdf2-hmac-sha256` | S07 | GO-034 @ 55:5 | 32-bit salt is below the SP 800-132 minimum of 128 bits |
| `m.pbkdf2-dk` | PBKDF2 derived key | secret-key | 512 | derived | - | `pbkdf2-hmac-sha256` | S07 | GO-059 @ 149:18 (produced) | - |
| `m.scrypt-password` | scrypt password | password | 104 | hardcoded | "pleaseletmein" | `scrypt` | S08 | GO-035 @ 56:5 | RFC 7914 section 12 |
| `m.scrypt-salt` | scrypt salt | salt | 112 | hardcoded | "SodiumChloride" | `scrypt` | S08 | GO-036 @ 57:5 | - |
| `m.scrypt-dk` | scrypt derived key | secret-key | 512 | derived | - | `scrypt` | S08 | GO-063 @ 156:18 (produced) | - |
| `m.password` | Application password | password | 224 | hardcoded | "correct horse battery staple" | `argon2id` | S09 | GO-037 @ 58:5 | Shared by S09 (Argon2id) and S10 (bcrypt) |
| `m.argon2-salt` | Argon2id salt | salt | 128 | hardcoded | "cbom-corpus-salt" | `argon2id` | S09 | GO-038 @ 59:5 | - |
| `m.argon2-dk` | Argon2id output | secret-key | 256 | derived | - | `argon2id` | S09 | GO-068 @ 163:9 (produced) | - |
| `m.bcrypt-salt` | bcrypt salt | salt | 128 | csprng | - | `bcrypt` | S10 | GO-073 @ 169:15 (produced) | - |
| `m.bcrypt-hash` | bcrypt hash string | credential | 480 | derived | - | `bcrypt` | S10 | GO-073 @ 169:15 (produced) | 60-character modular-crypt string ($2a$/$2b$) |
| `m.gcm-key` | AES-256-GCM key | secret-key | 256 | hardcoded | feffe992... | `aes-256-gcm` | S11 | GO-039 @ 60:5 | GCM spec test case 16 |
| `m.gcm-iv` | AES-GCM IV | nonce | 96 | hardcoded | cafebabefacedbaddecaf888 | `aes-256-gcm` | S11 | GO-040 @ 61:5 | Static nonce - reuse with the same key is catastrophic outside a KAT |
| `m.gcm-aad` | AES-GCM additional authenticated data | additional-data | 160 | hardcoded | feedface... | `aes-256-gcm` | S11 | GO-041 @ 62:5 | GCM spec test case 16 |
| `m.chacha-key` | ChaCha20-Poly1305 key | secret-key | 256 | csprng | - | `chacha20-poly1305` | S12 | GO-080 @ 190:22; GO-081 @ 191:2 (produced) | - |
| `m.chacha-nonce` | ChaCha20-Poly1305 nonce | nonce | 96 | csprng | - | `chacha20-poly1305` | S12 | GO-082 @ 192:24; GO-083 @ 193:2 (produced) | - |
| `m.cbc-key` | AES-256-CBC key | secret-key | 256 | csprng | - | `aes-256-cbc` | S13 | GO-087 @ 204:22; GO-088 @ 205:2 (produced) | - |
| `m.cbc-iv` | AES-CBC IV | initialization-vector | 128 | csprng | - | `aes-256-cbc` | S13 | GO-089 @ 206:21; GO-090 @ 207:2 (produced) | - |
| `m.ecb-key` | AES-128-ECB key | secret-key | 128 | hardcoded | 000102...0f | `aes-128-ecb` | S14 | GO-042 @ 65:5 | FIPS 197 appendix C.1 |
| `m.ctr-key` | AES-256-CTR key | secret-key | 256 | csprng | - | `aes-256-ctr` | S15 | GO-102 @ 232:22; GO-103 @ 233:2 (produced) | - |
| `m.ctr-iv` | AES-CTR initial counter block | initialization-vector | 128 | csprng | - | `aes-256-ctr` | S15 | GO-104 @ 234:31; GO-105 @ 235:2 (produced) | - |
| `m.tdes-key` | 3DES key | secret-key | 192 | csprng | - | `3des-cbc` | S16 | GO-111 @ 247:22; GO-112 @ 248:2 (produced) | 192 bits incl. parity = 168 effective |
| `m.tdes-iv` | 3DES IV | initialization-vector | 64 | csprng | - | `3des-cbc` | S16 | GO-113 @ 249:21; GO-114 @ 250:2 (produced) | - |
| `m.rsa-private-key` | RSA-3072 private key | private-key | 3072 | keygen | - | `rsa-3072` | S17 | GO-122 @ 263:21 (produced) | - |
| `m.rsa-public-key` | RSA-3072 public key | public-key | 3072 | keygen | - | `rsa-3072` | S17 | GO-122 @ 263:21 (produced) | e = 65537 |
| `m.ecdsa-private-key` | ECDSA P-256 private key | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | GO-140 @ 288:21 (produced) | - |
| `m.ecdsa-public-key` | ECDSA P-256 public key | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | GO-140 @ 288:21 (produced) | - |
| `m.ed25519-seed` | Ed25519 private key seed | private-key | 256 | hardcoded | 9d61b19d... | `ed25519` | S19 | GO-043 @ 67:5 | RFC 8032 section 7.1 TEST 1 |
| `m.ed25519-public-key` | Ed25519 public key | public-key | 256 | derived | d75a9801... | `ed25519` | S19 | GO-145 @ 299:16 (produced) | Derived from the seed |
| `m.x25519-private-key-a` | X25519 private key (party A) | private-key | 256 | keygen | - | `x25519` | S20 | GO-153 @ 315:16 (produced) | - |
| `m.x25519-private-key-b` | X25519 private key (party B) | private-key | 256 | keygen | - | `x25519` | S20 | GO-154 @ 317:14 (produced) | - |
| `m.x25519-shared-secret` | X25519 shared secret | shared-secret | 256 | agreed | - | `x25519` | S20 | GO-155 @ 319:17 (produced); GO-156 @ 321:15 (produced) | - |
| `m.ecdh-private-key-a` | ECDH P-256 private key (party A) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | GO-158 @ 326:18 (produced) | - |
| `m.ecdh-private-key-b` | ECDH P-256 private key (party B) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | GO-159 @ 328:16 (produced) | - |
| `m.ecdh-shared-secret` | ECDH P-256 shared secret | shared-secret | 256 | agreed | - | `ecdh-p256` | S20 | GO-160 @ 330:17 (produced); GO-161 @ 332:15 (produced) | - |
| `m.session-info` | Session-key HKDF info | additional-data | 208 | hardcoded | "cbom-corpus session key v1" | `hkdf-sha256` | S20 | GO-044 @ 68:5 | - |
| `m.session-key` | Session key (HKDF over X25519 || ECDH secrets) | secret-key | 256 | derived | - | `hkdf-sha256` | S20 | GO-149 @ 307:14 (produced) | - |
| `m.mlkem-decapsulation-key` | ML-KEM-768 decapsulation key | private-key | - | keygen | - | `ml-kem-768` | S21 | GO-162 @ 343:27 (produced) | 64-byte seed form or 2400-byte expanded form, library-dependent |
| `m.mlkem-encapsulation-key` | ML-KEM-768 encapsulation key | public-key | 9472 | keygen | - | `ml-kem-768` | S21 | GO-162 @ 343:27 (produced) | 1184 bytes |
| `m.mlkem-shared-secret` | ML-KEM-768 shared secret | shared-secret | 256 | agreed | - | `ml-kem-768` | S21 | GO-163 @ 345:30 (produced); GO-164 @ 346:20 (produced) | - |
| `m.mldsa-private-key` | ML-DSA-65 private key | private-key | - | keygen | - | `ml-dsa-65` | S22 | GO-165 @ 353:32 (produced) | 32-byte seed or 4032-byte expanded form, library-dependent |
| `m.mldsa-public-key` | ML-DSA-65 public key | public-key | 15616 | keygen | - | `ml-dsa-65` | S22 | GO-165 @ 353:32 (produced) | 1952 bytes |
| `m.cert-private-key` | Certificate private key (P-256) | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | GO-170 @ 363:14 (produced) | - |
| `m.cert-public-key` | Certificate subject public key (P-256) | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | GO-170 @ 363:14 (produced) | - |

## Scenario map

| Scenario | What it does | Output | Occurrences | Lines | Assets |
|---|---|---|---|---|---|
| S01 | SHA-256 digest of MESSAGE | Known answer (Wikipedia / NIST example message) | 1 | 105-105 | `sha-256` |
| S02 | SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | Known answers | 3 | 111-115 | `sha-512`, `sha3-256`, `blake2b-512` |
| S03 | Legacy MD5 and SHA-1 digests of MESSAGE | Known answers; deliberately weak algorithms | 2 | 121-123 | `md5`, `sha-1` |
| S04 | SHAKE128 XOF, 32-byte output | Known answer | 2 | 129-129 | `shake128` |
| S05 | HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | Known answer (Wikipedia HMAC example) | 4 | 50-137 | `sha-256`, `hmac-sha256`, `m.hmac-key` |
| S06 | HKDF-SHA256 extract-and-expand, L=42 | Known answer (RFC 5869 A.1) | 6 | 51-142 | `sha-256`, `hkdf-sha256`, `m.hkdf-ikm`, `m.hkdf-salt`, `m.hkdf-info`, `m.hkdf-okm` |
| S07 | PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | Known answer (RFC 7914 section 11) | 6 | 54-149 | `sha-256`, `pbkdf2-hmac-sha256`, `m.pbkdf2-password`, `m.pbkdf2-salt`, `m.pbkdf2-dk` |
| S08 | scrypt N=16384 r=8 p=1, dkLen=64 | Known answer (RFC 7914 section 12) | 7 | 56-156 | `scrypt`, `m.scrypt-password`, `m.scrypt-salt`, `m.scrypt-dk` |
| S09 | Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | Deterministic; identical across languages | 7 | 58-163 | `argon2id`, `m.password`, `m.argon2-salt`, `m.argon2-dk` |
| S10 | bcrypt cost 12 with random salt, then verify | Randomized; prints verify=true | 3 | 169-171 | `bcrypt`, `m.bcrypt-salt`, `m.bcrypt-hash` |
| S11 | AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | Known answer (GCM spec test case 16) | 7 | 60-182 | `aes-256-gcm`, `m.gcm-key`, `m.gcm-iv`, `m.gcm-aad` |
| S12 | ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | Randomized round trip | 7 | 190-197 | `chacha20-poly1305`, `csprng`, `m.chacha-key`, `m.chacha-nonce` |
| S13 | AES-256-CBC with PKCS#7 padding, random key and IV | Randomized round trip | 11 | 204-215 | `aes-256-cbc`, `csprng`, `m.cbc-key`, `m.cbc-iv` |
| S14 | AES-128-ECB with PKCS#7 padding, hard-coded key | Known answer: first block = FIPS 197 C.1 | 5 | 65-225 | `aes-128-ecb`, `m.ecb-key` |
| S15 | AES-256-CTR, random key and 128-bit initial counter block | Randomized round trip | 9 | 232-241 | `aes-256-ctr`, `csprng`, `m.ctr-key`, `m.ctr-iv` |
| S16 | 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | Randomized round trip | 11 | 247-258 | `3des-cbc`, `csprng`, `m.tdes-key`, `m.tdes-iv` |
| S17 | RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | Randomized | 18 | 263-282 | `sha-256`, `rsa-3072`, `rsa-oaep-sha256`, `rsassa-pss-sha256`, `rsassa-pkcs1v15-sha256`, `m.rsa-private-key`, `m.rsa-public-key` |
| S18 | ECDSA P-256 / SHA-256 sign and verify | Randomized | 5 | 288-293 | `sha-256`, `ecdsa-p256-sha256`, `m.ecdsa-private-key`, `m.ecdsa-public-key` |
| S19 | Ed25519 from a hard-coded seed: public key, signature, verify | Known public key (RFC 8032 test 1); deterministic signature | 5 | 67-302 | `ed25519`, `m.ed25519-seed`, `m.ed25519-public-key` |
| S20 | X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | Randomized; prints agreement booleans | 14 | 68-332 | `sha-256`, `hkdf-sha256`, `ecdh-p256`, `x25519`, `m.x25519-private-key-a`, `m.x25519-private-key-b`, `m.x25519-shared-secret`, `m.ecdh-private-key-a`, `m.ecdh-private-key-b`, `m.ecdh-shared-secret`, `m.session-info`, `m.session-key` |
| S21 | ML-KEM-768 key generation, encapsulation, decapsulation | Randomized; prints sizes | 3 | 343-346 | `ml-kem-768`, `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key`, `m.mlkem-shared-secret` |
| S22 | ML-DSA-65 key generation, signing, verification | Randomized; prints signature size | 5 | 353-357 | `ml-dsa-65`, `m.mldsa-private-key`, `m.mldsa-public-key` |
| S23 | Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | Randomized | 9 | 363-379 | `ecdsa-p256-sha256`, `csprng`, `cert.self-signed`, `m.cert-private-key`, `m.cert-public-key` |
| S24 | TLS 1.3-only client configuration (no network I/O) | Configuration only | 3 | 385-389 | `tls13-client` |

## Occurrence ledger

Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.

| ID | Scn | Role | Asset (^parent) | Start L:C | End L:C | Chars | Bytes | Len | Nest | Scope | API symbol | Library | Produces | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GO-001 | - | `imp` | `lib.go-stdlib` | 10:2 | 10:10 | [351, 359) | [351, 359) | 8 | 0 | `<package main>` | `crypto` | `lib.go-stdlib` | - | `"crypto"` | - |
| GO-002 | - | `imp` | `lib.go-stdlib` | 11:2 | 11:14 | [361, 373) | [361, 373) | 12 | 0 | `<package main>` | `crypto/aes` | `lib.go-stdlib` | - | `"crypto/aes"` | - |
| GO-003 | - | `imp` | `lib.go-stdlib` | 12:2 | 12:17 | [375, 390) | [375, 390) | 15 | 0 | `<package main>` | `crypto/cipher` | `lib.go-stdlib` | - | `"crypto/cipher"` | - |
| GO-004 | - | `imp` | `lib.go-stdlib` | 13:2 | 13:14 | [392, 404) | [392, 404) | 12 | 0 | `<package main>` | `crypto/des` | `lib.go-stdlib` | - | `"crypto/des"` | - |
| GO-005 | - | `imp` | `lib.go-stdlib` | 14:2 | 14:15 | [406, 419) | [406, 419) | 13 | 0 | `<package main>` | `crypto/ecdh` | `lib.go-stdlib` | - | `"crypto/ecdh"` | - |
| GO-006 | - | `imp` | `lib.go-stdlib` | 15:2 | 15:16 | [421, 435) | [421, 435) | 14 | 0 | `<package main>` | `crypto/ecdsa` | `lib.go-stdlib` | - | `"crypto/ecdsa"` | - |
| GO-007 | - | `imp` | `lib.go-stdlib` | 16:2 | 16:18 | [437, 453) | [437, 453) | 16 | 0 | `<package main>` | `crypto/ed25519` | `lib.go-stdlib` | - | `"crypto/ed25519"` | - |
| GO-008 | - | `imp` | `lib.go-stdlib` | 17:2 | 17:19 | [455, 472) | [455, 472) | 17 | 0 | `<package main>` | `crypto/elliptic` | `lib.go-stdlib` | - | `"crypto/elliptic"` | - |
| GO-009 | - | `imp` | `lib.go-stdlib` | 18:2 | 18:15 | [474, 487) | [474, 487) | 13 | 0 | `<package main>` | `crypto/hkdf` | `lib.go-stdlib` | - | `"crypto/hkdf"` | - |
| GO-010 | - | `imp` | `lib.go-stdlib` | 19:2 | 19:15 | [489, 502) | [489, 502) | 13 | 0 | `<package main>` | `crypto/hmac` | `lib.go-stdlib` | - | `"crypto/hmac"` | - |
| GO-011 | - | `imp` | `lib.go-stdlib` | 20:2 | 20:14 | [504, 516) | [504, 516) | 12 | 0 | `<package main>` | `crypto/md5` | `lib.go-stdlib` | - | `"crypto/md5"` | - |
| GO-012 | - | `imp` | `lib.go-stdlib` | 21:2 | 21:16 | [518, 532) | [518, 532) | 14 | 0 | `<package main>` | `crypto/mlkem` | `lib.go-stdlib` | - | `"crypto/mlkem"` | - |
| GO-013 | - | `imp` | `lib.go-stdlib` | 22:2 | 22:17 | [534, 549) | [534, 549) | 15 | 0 | `<package main>` | `crypto/pbkdf2` | `lib.go-stdlib` | - | `"crypto/pbkdf2"` | - |
| GO-014 | - | `imp` | `lib.go-stdlib` | 23:2 | 23:15 | [551, 564) | [551, 564) | 13 | 0 | `<package main>` | `crypto/rand` | `lib.go-stdlib` | - | `"crypto/rand"` | - |
| GO-015 | - | `imp` | `lib.go-stdlib` | 24:2 | 24:14 | [566, 578) | [566, 578) | 12 | 0 | `<package main>` | `crypto/rsa` | `lib.go-stdlib` | - | `"crypto/rsa"` | - |
| GO-016 | - | `imp` | `lib.go-stdlib` | 25:2 | 25:15 | [580, 593) | [580, 593) | 13 | 0 | `<package main>` | `crypto/sha1` | `lib.go-stdlib` | - | `"crypto/sha1"` | - |
| GO-017 | - | `imp` | `lib.go-stdlib` | 26:2 | 26:17 | [595, 610) | [595, 610) | 15 | 0 | `<package main>` | `crypto/sha256` | `lib.go-stdlib` | - | `"crypto/sha256"` | - |
| GO-018 | - | `imp` | `lib.go-stdlib` | 27:2 | 27:15 | [612, 625) | [612, 625) | 13 | 0 | `<package main>` | `crypto/sha3` | `lib.go-stdlib` | - | `"crypto/sha3"` | - |
| GO-019 | - | `imp` | `lib.go-stdlib` | 28:2 | 28:17 | [627, 642) | [627, 642) | 15 | 0 | `<package main>` | `crypto/sha512` | `lib.go-stdlib` | - | `"crypto/sha512"` | - |
| GO-020 | - | `imp` | `lib.go-stdlib` | 29:2 | 29:14 | [644, 656) | [644, 656) | 12 | 0 | `<package main>` | `crypto/tls` | `lib.go-stdlib` | - | `"crypto/tls"` | - |
| GO-021 | - | `imp` | `lib.go-stdlib` | 30:2 | 30:15 | [658, 671) | [658, 671) | 13 | 0 | `<package main>` | `crypto/x509` | `lib.go-stdlib` | - | `"crypto/x509"` | - |
| GO-022 | - | `imp` | `lib.go-stdlib` | 31:2 | 31:20 | [673, 691) | [673, 691) | 18 | 0 | `<package main>` | `crypto/x509/pkix` | `lib.go-stdlib` | - | `"crypto/x509/pkix"` | - |
| GO-023 | - | `imp` | `lib.circl` | 37:2 | 37:50 | [737, 785) | [737, 785) | 48 | 0 | `<package main>` | `github.com/cloudflare/circl/sign/mldsa/mldsa65` | `lib.circl` | - | `"github.com/cloudflare/circl/sign/mldsa/mldsa65"` | - |
| GO-024 | - | `imp` | `lib.xcrypto` | 38:2 | 38:30 | [787, 815) | [787, 815) | 28 | 0 | `<package main>` | `golang.org/x/crypto/argon2` | `lib.xcrypto` | - | `"golang.org/x/crypto/argon2"` | - |
| GO-025 | - | `imp` | `lib.xcrypto` | 39:2 | 39:30 | [817, 845) | [817, 845) | 28 | 0 | `<package main>` | `golang.org/x/crypto/bcrypt` | `lib.xcrypto` | - | `"golang.org/x/crypto/bcrypt"` | - |
| GO-026 | - | `imp` | `lib.xcrypto` | 40:2 | 40:31 | [847, 876) | [847, 876) | 29 | 0 | `<package main>` | `golang.org/x/crypto/blake2b` | `lib.xcrypto` | - | `"golang.org/x/crypto/blake2b"` | - |
| GO-027 | - | `imp` | `lib.xcrypto` | 41:2 | 41:40 | [878, 916) | [878, 916) | 38 | 0 | `<package main>` | `golang.org/x/crypto/chacha20poly1305` | `lib.xcrypto` | - | `"golang.org/x/crypto/chacha20poly1305"` | - |
| GO-028 | - | `imp` | `lib.xcrypto` | 42:2 | 42:30 | [918, 946) | [918, 946) | 28 | 0 | `<package main>` | `golang.org/x/crypto/scrypt` | `lib.xcrypto` | - | `"golang.org/x/crypto/scrypt"` | - |
| GO-029 | S05 | `mat` | `m.hmac-key` | 50:5 | 50:28 | [1238, 1261) | [1238, 1261) | 23 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `hmacKey = []byte("key")` | - |
| GO-030 | S06 | `mat` | `m.hkdf-ikm` | 51:5 | 51:45 | [1266, 1306) | [1266, 1306) | 40 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `hkdfIKM = bytes.Repeat([]byte{0x0b}, 22)` | - |
| GO-031 | S06 | `mat` | `m.hkdf-salt` | 52:5 | 52:53 | [1311, 1359) | [1311, 1359) | 48 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `hkdfSalt = mustHex("000102030405060708090a0b0c")` | - |
| GO-032 | S06 | `mat` | `m.hkdf-info` | 53:5 | 53:47 | [1364, 1406) | [1364, 1406) | 42 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `hkdfInfo = mustHex("f0f1f2f3f4f5f6f7f8f9")` | - |
| GO-033 | S07 | `mat` | `m.pbkdf2-password` | 54:5 | 54:32 | [1411, 1438) | [1411, 1438) | 27 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `pbkdf2Password = "Password"` | - |
| GO-034 | S07 | `mat` | `m.pbkdf2-salt` | 55:5 | 55:32 | [1443, 1470) | [1443, 1470) | 27 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `pbkdf2Salt = []byte("NaCl")` | - |
| GO-035 | S08 | `mat` | `m.scrypt-password` | 56:5 | 56:45 | [1475, 1515) | [1475, 1515) | 40 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `scryptPassword = []byte("pleaseletmein")` | - |
| GO-036 | S08 | `mat` | `m.scrypt-salt` | 57:5 | 57:42 | [1520, 1557) | [1520, 1557) | 37 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `scryptSalt = []byte("SodiumChloride")` | - |
| GO-037 | S09 | `mat` | `m.password` | 58:5 | 58:54 | [1562, 1611) | [1562, 1611) | 49 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `password = []byte("correct horse battery staple")` | - |
| GO-038 | S09 | `mat` | `m.argon2-salt` | 59:5 | 59:44 | [1616, 1655) | [1616, 1655) | 39 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `argon2Salt = []byte("cbom-corpus-salt")` | - |
| GO-039 | S11 | `mat` | `m.gcm-key` | 60:5 | 60:89 | [1660, 1744) | [1660, 1744) | 84 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `gcmKey = mustHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")` | - |
| GO-040 | S11 | `mat` | `m.gcm-iv` | 61:5 | 61:48 | [1749, 1792) | [1749, 1792) | 43 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `gcmIV = mustHex("cafebabefacedbaddecaf888")` | - |
| GO-041 | S11 | `mat` | `m.gcm-aad` | 62:5 | 62:65 | [1797, 1857) | [1797, 1857) | 60 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `gcmAAD = mustHex("feedfacedeadbeeffeedfacedeadbeefabaddad2")` | - |
| GO-042 | S14 | `mat` | `m.ecb-key` | 65:5 | 65:57 | [2019, 2071) | [2019, 2071) | 52 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `ecbKey = mustHex("000102030405060708090a0b0c0d0e0f")` | - |
| GO-043 | S19 | `mat` | `m.ed25519-seed` | 67:5 | 67:94 | [2139, 2228) | [2139, 2228) | 89 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `ed25519Seed = mustHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")` | - |
| GO-044 | S20 | `mat` | `m.session-info` | 68:5 | 68:47 | [2233, 2275) | [2233, 2275) | 42 | 0 | `<package main>` | - | `lib.go-stdlib` | - | `sessionInfo = "cbom-corpus session key v1"` | - |
| GO-045 | S01 | `op:digest` | `sha-256` | 105:12 | 105:34 | [2971, 2993) | [2971, 2993) | 22 | 0 | `s01SHA256` | `crypto/sha256.Sum256` | `lib.go-stdlib` | - | `sha256.Sum256(message)` | - |
| GO-046 | S02 | `op:digest` | `sha-512` | 111:18 | 111:40 | [3135, 3157) | [3135, 3157) | 22 | 0 | `s02SHA2SHA3BLAKE2` | `crypto/sha512.Sum512` | `lib.go-stdlib` | - | `sha512.Sum512(message)` | - |
| GO-047 | S02 | `op:digest` | `sha3-256` | 113:16 | 113:36 | [3234, 3254) | [3234, 3254) | 20 | 0 | `s02SHA2SHA3BLAKE2` | `crypto/sha3.Sum256` | `lib.go-stdlib` | - | `sha3.Sum256(message)` | - |
| GO-048 | S02 | `op:digest` | `blake2b-512` | 115:17 | 115:40 | [3331, 3354) | [3331, 3354) | 23 | 0 | `s02SHA2SHA3BLAKE2` | `golang.org/x/crypto/blake2b.Sum512` | `lib.xcrypto` | - | `blake2b.Sum512(message)` | - |
| GO-049 | S03 | `op:digest` | `md5` | 121:15 | 121:31 | [3504, 3520) | [3504, 3520) | 16 | 0 | `s03LegacyHashes` | `crypto/md5.Sum` | `lib.go-stdlib` | - | `md5.Sum(message)` | - |
| GO-050 | S03 | `op:digest` | `sha-1` | 123:16 | 123:33 | [3590, 3607) | [3590, 3607) | 17 | 0 | `s03LegacyHashes` | `crypto/sha1.Sum` | `lib.go-stdlib` | - | `sha1.Sum(message)` | - |
| GO-051 | S04 | `op:digest` | `shake128` | 129:9 | 129:38 | [3741, 3770) | [3741, 3770) | 29 | 0 | `s04SHAKE128` | `crypto/sha3.SumSHAKE128` | `lib.go-stdlib` | - | `sha3.SumSHAKE128(message, 32)` | - |
| GO-052 | S04 | `prm:output-length-bytes` | `shake128` | 129:35 | 129:37 | [3767, 3769) | [3767, 3769) | 2 | 1 | `s04SHAKE128` | - | `lib.go-stdlib` | - | `32` | - |
| GO-053 | S05 | `ctor` | `hmac-sha256` | 135:9 | 135:38 | [3875, 3904) | [3875, 3904) | 29 | 0 | `s05HMACSHA256` | `crypto/hmac.New` | `lib.go-stdlib` | - | `hmac.New(sha256.New, hmacKey)` | - |
| GO-054 | S05 | `alg` | `sha-256` ^`hmac-sha256` | 135:18 | 135:28 | [3884, 3894) | [3884, 3894) | 10 | 1 | `s05HMACSHA256` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New` | hash-constructor |
| GO-055 | S05 | `op:tag` | `hmac-sha256` | 137:48 | 137:60 | [3972, 3984) | [3972, 3984) | 12 | 0 | `s05HMACSHA256` | `hash.Hash.Sum` | `lib.go-stdlib` | - | `mac.Sum(nil)` | - |
| GO-056 | S06 | `op:keyderive` | `hkdf-sha256` | 142:14 | 142:75 | [4057, 4118) | [4057, 4118) | 61 | 0 | `s06HKDFSHA256` | `crypto/hkdf.Key` | `lib.go-stdlib` | `m.hkdf-okm` | `hkdf.Key(sha256.New, hkdfIKM, hkdfSalt, string(hkdfInfo), 42)` | - |
| GO-057 | S06 | `alg` | `sha-256` ^`hkdf-sha256` | 142:23 | 142:33 | [4066, 4076) | [4066, 4076) | 10 | 1 | `s06HKDFSHA256` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New` | hash-constructor |
| GO-058 | S06 | `prm:output-length-bytes` | `hkdf-sha256` | 142:72 | 142:74 | [4115, 4117) | [4115, 4117) | 2 | 1 | `s06HKDFSHA256` | - | `lib.go-stdlib` | - | `42` | - |
| GO-059 | S07 | `op:keyderive` | `pbkdf2-hmac-sha256` | 149:18 | 149:80 | [4250, 4312) | [4250, 4312) | 62 | 0 | `s07PBKDF2` | `crypto/pbkdf2.Key` | `lib.go-stdlib` | `m.pbkdf2-dk` | `pbkdf2.Key(sha256.New, pbkdf2Password, pbkdf2Salt, 80_000, 64)` | - |
| GO-060 | S07 | `alg` | `sha-256` ^`pbkdf2-hmac-sha256` | 149:29 | 149:39 | [4261, 4271) | [4261, 4271) | 10 | 1 | `s07PBKDF2` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New` | hash-constructor |
| GO-061 | S07 | `prm:iterations` | `pbkdf2-hmac-sha256` | 149:69 | 149:75 | [4301, 4307) | [4301, 4307) | 6 | 1 | `s07PBKDF2` | - | `lib.go-stdlib` | - | `80_000` | - |
| GO-062 | S07 | `prm:output-length-bytes` | `pbkdf2-hmac-sha256` | 149:77 | 149:79 | [4309, 4311) | [4309, 4311) | 2 | 1 | `s07PBKDF2` | - | `lib.go-stdlib` | - | `64` | - |
| GO-063 | S08 | `op:keyderive` | `scrypt` | 156:18 | 156:73 | [4438, 4493) | [4438, 4493) | 55 | 0 | `s08Scrypt` | `golang.org/x/crypto/scrypt.Key` | `lib.xcrypto` | `m.scrypt-dk` | `scrypt.Key(scryptPassword, scryptSalt, 1<<14, 8, 1, 64)` | - |
| GO-064 | S08 | `prm:N` | `scrypt` | 156:57 | 156:62 | [4477, 4482) | [4477, 4482) | 5 | 1 | `s08Scrypt` | - | `lib.xcrypto` | - | `1<<14` | computed |
| GO-065 | S08 | `prm:r` | `scrypt` | 156:64 | 156:65 | [4484, 4485) | [4484, 4485) | 1 | 1 | `s08Scrypt` | - | `lib.xcrypto` | - | `8` | - |
| GO-066 | S08 | `prm:p` | `scrypt` | 156:67 | 156:68 | [4487, 4488) | [4487, 4488) | 1 | 1 | `s08Scrypt` | - | `lib.xcrypto` | - | `1` | - |
| GO-067 | S08 | `prm:output-length-bytes` | `scrypt` | 156:70 | 156:72 | [4490, 4492) | [4490, 4492) | 2 | 1 | `s08Scrypt` | - | `lib.xcrypto` | - | `64` | - |
| GO-068 | S09 | `op:keyderive` | `argon2id` | 163:9 | 163:61 | [4607, 4659) | [4607, 4659) | 52 | 0 | `s09Argon2id` | `golang.org/x/crypto/argon2.IDKey` | `lib.xcrypto` | `m.argon2-dk` | `argon2.IDKey(password, argon2Salt, 2, 19_456, 1, 32)` | mode-ctor |
| GO-069 | S09 | `prm:iterations` | `argon2id` | 163:44 | 163:45 | [4642, 4643) | [4642, 4643) | 1 | 1 | `s09Argon2id` | - | `lib.xcrypto` | - | `2` | - |
| GO-070 | S09 | `prm:memory-kib` | `argon2id` | 163:47 | 163:53 | [4645, 4651) | [4645, 4651) | 6 | 1 | `s09Argon2id` | - | `lib.xcrypto` | - | `19_456` | - |
| GO-071 | S09 | `prm:parallelism` | `argon2id` | 163:55 | 163:56 | [4653, 4654) | [4653, 4654) | 1 | 1 | `s09Argon2id` | - | `lib.xcrypto` | - | `1` | - |
| GO-072 | S09 | `prm:output-length-bytes` | `argon2id` | 163:58 | 163:60 | [4656, 4658) | [4656, 4658) | 2 | 1 | `s09Argon2id` | - | `lib.xcrypto` | - | `32` | - |
| GO-073 | S10 | `op:keyderive` | `bcrypt` | 169:15 | 169:56 | [4761, 4802) | [4761, 4802) | 41 | 0 | `s10Bcrypt` | `golang.org/x/crypto/bcrypt.GenerateFromPassword` | `lib.xcrypto` | `m.bcrypt-hash`, `m.bcrypt-salt` | `bcrypt.GenerateFromPassword(password, 12)` | bcrypt-internal-salt |
| GO-074 | S10 | `prm:cost` | `bcrypt` | 169:53 | 169:55 | [4799, 4801) | [4799, 4801) | 2 | 1 | `s10Bcrypt` | - | `lib.xcrypto` | - | `12` | - |
| GO-075 | S10 | `op:verify` | `bcrypt` | 171:8 | 171:53 | [4822, 4867) | [4822, 4867) | 45 | 0 | `s10Bcrypt` | `golang.org/x/crypto/bcrypt.CompareHashAndPassword` | `lib.xcrypto` | - | `bcrypt.CompareHashAndPassword(hash, password)` | - |
| GO-076 | S11 | `ctor` | `aes-256-gcm` | 177:16 | 177:37 | [5006, 5027) | [5006, 5027) | 21 | 0 | `s11AES256GCM` | `crypto/aes.NewCipher` | `lib.go-stdlib` | - | `aes.NewCipher(gcmKey)` | keysize-from-key |
| GO-077 | S11 | `ctor` | `aes-256-gcm` | 179:15 | 179:35 | [5054, 5074) | [5054, 5074) | 20 | 0 | `s11AES256GCM` | `crypto/cipher.NewGCM` | `lib.go-stdlib` | - | `cipher.NewGCM(block)` | mode-ctor |
| GO-078 | S11 | `op:encrypt` | `aes-256-gcm` | 181:12 | 181:55 | [5098, 5141) | [5098, 5141) | 43 | 0 | `s11AES256GCM` | `crypto/cipher.AEAD.Seal` | `lib.go-stdlib` | - | `aead.Seal(nil, gcmIV, gcmPlaintext, gcmAAD)` | - |
| GO-079 | S11 | `op:decrypt` | `aes-256-gcm` | 182:17 | 182:54 | [5158, 5195) | [5158, 5195) | 37 | 0 | `s11AES256GCM` | `crypto/cipher.AEAD.Open` | `lib.go-stdlib` | - | `aead.Open(nil, gcmIV, sealed, gcmAAD)` | - |
| GO-080 | S12 | `prm:length-bytes` | `m.chacha-key` | 190:22 | 190:46 | [5484, 5508) | [5484, 5508) | 24 | 0 | `s12ChaCha20Poly1305` | `golang.org/x/crypto/chacha20poly1305.KeySize` | `lib.xcrypto` | - | `chacha20poly1305.KeySize` | - |
| GO-081 | S12 | `op:generate` | `csprng` | 191:2 | 191:16 | [5511, 5525) | [5511, 5525) | 14 | 0 | `s12ChaCha20Poly1305` | `crypto/rand.Read` | `lib.go-stdlib` | `m.chacha-key` | `rand.Read(key)` | - |
| GO-082 | S12 | `prm:length-bytes` | `m.chacha-nonce` | 192:24 | 192:50 | [5549, 5575) | [5549, 5575) | 26 | 0 | `s12ChaCha20Poly1305` | `golang.org/x/crypto/chacha20poly1305.NonceSize` | `lib.xcrypto` | - | `chacha20poly1305.NonceSize` | - |
| GO-083 | S12 | `op:generate` | `csprng` | 193:2 | 193:18 | [5578, 5594) | [5578, 5594) | 16 | 0 | `s12ChaCha20Poly1305` | `crypto/rand.Read` | `lib.go-stdlib` | `m.chacha-nonce` | `rand.Read(nonce)` | - |
| GO-084 | S12 | `ctor` | `chacha20-poly1305` | 194:15 | 194:40 | [5609, 5634) | [5609, 5634) | 25 | 0 | `s12ChaCha20Poly1305` | `golang.org/x/crypto/chacha20poly1305.New` | `lib.xcrypto` | - | `chacha20poly1305.New(key)` | - |
| GO-085 | S12 | `op:encrypt` | `chacha20-poly1305` | 196:12 | 196:47 | [5658, 5693) | [5658, 5693) | 35 | 0 | `s12ChaCha20Poly1305` | `crypto/cipher.AEAD.Seal` | `lib.go-stdlib` | - | `aead.Seal(nil, nonce, message, nil)` | - |
| GO-086 | S12 | `op:decrypt` | `chacha20-poly1305` | 197:17 | 197:51 | [5710, 5744) | [5710, 5744) | 34 | 0 | `s12ChaCha20Poly1305` | `crypto/cipher.AEAD.Open` | `lib.go-stdlib` | - | `aead.Open(nil, nonce, sealed, nil)` | - |
| GO-087 | S13 | `prm:length-bytes` | `m.cbc-key` | 204:22 | 204:24 | [5936, 5938) | [5936, 5938) | 2 | 0 | `s13AES256CBC` | - | `lib.go-stdlib` | - | `32` | - |
| GO-088 | S13 | `op:generate` | `csprng` | 205:2 | 205:16 | [5941, 5955) | [5941, 5955) | 14 | 0 | `s13AES256CBC` | `crypto/rand.Read` | `lib.go-stdlib` | `m.cbc-key` | `rand.Read(key)` | - |
| GO-089 | S13 | `prm:length-bytes` | `m.cbc-iv` | 206:21 | 206:34 | [5976, 5989) | [5976, 5989) | 13 | 0 | `s13AES256CBC` | `crypto/aes.BlockSize` | `lib.go-stdlib` | - | `aes.BlockSize` | - |
| GO-090 | S13 | `op:generate` | `csprng` | 207:2 | 207:15 | [5992, 6005) | [5992, 6005) | 13 | 0 | `s13AES256CBC` | `crypto/rand.Read` | `lib.go-stdlib` | `m.cbc-iv` | `rand.Read(iv)` | - |
| GO-091 | S13 | `ctor` | `aes-256-cbc` | 208:16 | 208:34 | [6021, 6039) | [6021, 6039) | 18 | 0 | `s13AES256CBC` | `crypto/aes.NewCipher` | `lib.go-stdlib` | - | `aes.NewCipher(key)` | keysize-from-key |
| GO-092 | S13 | `alg` | `aes-256-cbc` | 210:12 | 210:44 | [6063, 6095) | [6063, 6095) | 32 | 0 | `s13AES256CBC` | - | `lib.go-stdlib` | - | `pkcs7Pad(message, aes.BlockSize)` | manual-pkcs7 |
| GO-093 | S13 | `op:encrypt` | `aes-256-cbc` | 212:2 | 212:67 | [6138, 6203) | [6138, 6203) | 65 | 0 | `s13AES256CBC` | `crypto/cipher.BlockMode.CryptBlocks` | `lib.go-stdlib` | - | `cipher.NewCBCEncrypter(block, iv).CryptBlocks(ciphertext, padded)` | - |
| GO-094 | S13 | `ctor:encrypt` | `aes-256-cbc` | 212:2 | 212:35 | [6138, 6171) | [6138, 6171) | 33 | 1 | `s13AES256CBC` | `crypto/cipher.NewCBCEncrypter` | `lib.go-stdlib` | - | `cipher.NewCBCEncrypter(block, iv)` | mode-ctor |
| GO-095 | S13 | `op:decrypt` | `aes-256-cbc` | 214:2 | 214:70 | [6249, 6317) | [6249, 6317) | 68 | 0 | `s13AES256CBC` | `crypto/cipher.BlockMode.CryptBlocks` | `lib.go-stdlib` | - | `cipher.NewCBCDecrypter(block, iv).CryptBlocks(plaintext, ciphertext)` | - |
| GO-096 | S13 | `ctor:decrypt` | `aes-256-cbc` | 214:2 | 214:35 | [6249, 6282) | [6249, 6282) | 33 | 1 | `s13AES256CBC` | `crypto/cipher.NewCBCDecrypter` | `lib.go-stdlib` | - | `cipher.NewCBCDecrypter(block, iv)` | mode-ctor |
| GO-097 | S13 | `alg` | `aes-256-cbc` | 215:69 | 215:90 | [6386, 6407) | [6386, 6407) | 21 | 0 | `s13AES256CBC` | - | `lib.go-stdlib` | - | `pkcs7Unpad(plaintext)` | manual-pkcs7 |
| GO-098 | S14 | `ctor` | `aes-128-ecb` | 220:16 | 220:37 | [6523, 6544) | [6523, 6544) | 21 | 0 | `s14AES128ECB` | `crypto/aes.NewCipher` | `lib.go-stdlib` | - | `aes.NewCipher(ecbKey)` | keysize-from-key |
| GO-099 | S14 | `alg` | `aes-128-ecb` | 222:12 | 222:49 | [6568, 6605) | [6568, 6605) | 37 | 0 | `s14AES128ECB` | - | `lib.go-stdlib` | - | `pkcs7Pad(ecbPlaintext, aes.BlockSize)` | manual-pkcs7 |
| GO-100 | S14 | `prm:block-size-bytes` | `aes-128-ecb` | 224:36 | 224:49 | [6682, 6695) | [6682, 6695) | 13 | 0 | `s14AES128ECB` | `crypto/aes.BlockSize` | `lib.go-stdlib` | - | `aes.BlockSize` | manual-ecb |
| GO-101 | S14 | `op:encrypt` | `aes-128-ecb` | 225:3 | 225:74 | [6700, 6771) | [6700, 6771) | 71 | 0 | `s14AES128ECB` | `crypto/cipher.Block.Encrypt` | `lib.go-stdlib` | - | `block.Encrypt(ciphertext[i:i+aes.BlockSize], padded[i:i+aes.BlockSize])` | manual-ecb |
| GO-102 | S15 | `prm:length-bytes` | `m.ctr-key` | 232:22 | 232:24 | [6901, 6903) | [6901, 6903) | 2 | 0 | `s15AES256CTR` | - | `lib.go-stdlib` | - | `32` | - |
| GO-103 | S15 | `op:generate` | `csprng` | 233:2 | 233:16 | [6906, 6920) | [6906, 6920) | 14 | 0 | `s15AES256CTR` | `crypto/rand.Read` | `lib.go-stdlib` | `m.ctr-key` | `rand.Read(key)` | - |
| GO-104 | S15 | `prm:length-bytes` | `m.ctr-iv` | 234:31 | 234:44 | [6951, 6964) | [6951, 6964) | 13 | 0 | `s15AES256CTR` | `crypto/aes.BlockSize` | `lib.go-stdlib` | - | `aes.BlockSize` | - |
| GO-105 | S15 | `op:generate` | `csprng` | 235:2 | 235:25 | [6967, 6990) | [6967, 6990) | 23 | 0 | `s15AES256CTR` | `crypto/rand.Read` | `lib.go-stdlib` | `m.ctr-iv` | `rand.Read(counterBlock)` | - |
| GO-106 | S15 | `ctor` | `aes-256-ctr` | 236:16 | 236:34 | [7006, 7024) | [7006, 7024) | 18 | 0 | `s15AES256CTR` | `crypto/aes.NewCipher` | `lib.go-stdlib` | - | `aes.NewCipher(key)` | keysize-from-key |
| GO-107 | S15 | `op:encrypt` | `aes-256-ctr` | 239:2 | 239:70 | [7080, 7148) | [7080, 7148) | 68 | 0 | `s15AES256CTR` | `crypto/cipher.Stream.XORKeyStream` | `lib.go-stdlib` | - | `cipher.NewCTR(block, counterBlock).XORKeyStream(ciphertext, message)` | - |
| GO-108 | S15 | `ctor:encrypt` | `aes-256-ctr` | 239:2 | 239:36 | [7080, 7114) | [7080, 7114) | 34 | 1 | `s15AES256CTR` | `crypto/cipher.NewCTR` | `lib.go-stdlib` | - | `cipher.NewCTR(block, counterBlock)` | mode-ctor |
| GO-109 | S15 | `op:decrypt` | `aes-256-ctr` | 241:2 | 241:72 | [7194, 7264) | [7194, 7264) | 70 | 0 | `s15AES256CTR` | `crypto/cipher.Stream.XORKeyStream` | `lib.go-stdlib` | - | `cipher.NewCTR(block, counterBlock).XORKeyStream(plaintext, ciphertext)` | - |
| GO-110 | S15 | `ctor:decrypt` | `aes-256-ctr` | 241:2 | 241:36 | [7194, 7228) | [7194, 7228) | 34 | 1 | `s15AES256CTR` | `crypto/cipher.NewCTR` | `lib.go-stdlib` | - | `cipher.NewCTR(block, counterBlock)` | mode-ctor |
| GO-111 | S16 | `prm:length-bytes` | `m.tdes-key` | 247:22 | 247:24 | [7445, 7447) | [7445, 7447) | 2 | 0 | `s16TDEACBC` | - | `lib.go-stdlib` | - | `24` | - |
| GO-112 | S16 | `op:generate` | `csprng` | 248:2 | 248:16 | [7450, 7464) | [7450, 7464) | 14 | 0 | `s16TDEACBC` | `crypto/rand.Read` | `lib.go-stdlib` | `m.tdes-key` | `rand.Read(key)` | - |
| GO-113 | S16 | `prm:length-bytes` | `m.tdes-iv` | 249:21 | 249:34 | [7485, 7498) | [7485, 7498) | 13 | 0 | `s16TDEACBC` | `crypto/des.BlockSize` | `lib.go-stdlib` | - | `des.BlockSize` | - |
| GO-114 | S16 | `op:generate` | `csprng` | 250:2 | 250:15 | [7501, 7514) | [7501, 7514) | 13 | 0 | `s16TDEACBC` | `crypto/rand.Read` | `lib.go-stdlib` | `m.tdes-iv` | `rand.Read(iv)` | - |
| GO-115 | S16 | `ctor` | `3des-cbc` | 251:16 | 251:43 | [7530, 7557) | [7530, 7557) | 27 | 0 | `s16TDEACBC` | `crypto/des.NewTripleDESCipher` | `lib.go-stdlib` | - | `des.NewTripleDESCipher(key)` | - |
| GO-116 | S16 | `alg` | `3des-cbc` | 253:12 | 253:44 | [7581, 7613) | [7581, 7613) | 32 | 0 | `s16TDEACBC` | - | `lib.go-stdlib` | - | `pkcs7Pad(message, des.BlockSize)` | manual-pkcs7 |
| GO-117 | S16 | `op:encrypt` | `3des-cbc` | 255:2 | 255:67 | [7656, 7721) | [7656, 7721) | 65 | 0 | `s16TDEACBC` | `crypto/cipher.BlockMode.CryptBlocks` | `lib.go-stdlib` | - | `cipher.NewCBCEncrypter(block, iv).CryptBlocks(ciphertext, padded)` | - |
| GO-118 | S16 | `ctor:encrypt` | `3des-cbc` | 255:2 | 255:35 | [7656, 7689) | [7656, 7689) | 33 | 1 | `s16TDEACBC` | `crypto/cipher.NewCBCEncrypter` | `lib.go-stdlib` | - | `cipher.NewCBCEncrypter(block, iv)` | mode-ctor |
| GO-119 | S16 | `op:decrypt` | `3des-cbc` | 257:2 | 257:70 | [7767, 7835) | [7767, 7835) | 68 | 0 | `s16TDEACBC` | `crypto/cipher.BlockMode.CryptBlocks` | `lib.go-stdlib` | - | `cipher.NewCBCDecrypter(block, iv).CryptBlocks(plaintext, ciphertext)` | - |
| GO-120 | S16 | `ctor:decrypt` | `3des-cbc` | 257:2 | 257:35 | [7767, 7800) | [7767, 7800) | 33 | 1 | `s16TDEACBC` | `crypto/cipher.NewCBCDecrypter` | `lib.go-stdlib` | - | `cipher.NewCBCDecrypter(block, iv)` | mode-ctor |
| GO-121 | S16 | `alg` | `3des-cbc` | 258:66 | 258:87 | [7901, 7922) | [7901, 7922) | 21 | 0 | `s16TDEACBC` | - | `lib.go-stdlib` | - | `pkcs7Unpad(plaintext)` | manual-pkcs7 |
| GO-122 | S17 | `op:keygen` | `rsa-3072` | 263:21 | 263:55 | [8041, 8075) | [8041, 8075) | 34 | 0 | `s17RSA3072` | `crypto/rsa.GenerateKey` | `lib.go-stdlib` | `m.rsa-private-key`, `m.rsa-public-key` | `rsa.GenerateKey(rand.Reader, 3072)` | go126-rand-ignored |
| GO-123 | S17 | `prm:key-size-bits` | `rsa-3072` | 263:50 | 263:54 | [8070, 8074) | [8070, 8074) | 4 | 1 | `s17RSA3072` | - | `lib.go-stdlib` | - | `3072` | - |
| GO-124 | S17 | `op:encrypt` | `rsa-oaep-sha256` | 267:21 | 267:88 | [8145, 8212) | [8145, 8212) | 67 | 0 | `s17RSA3072` | `crypto/rsa.EncryptOAEP` | `lib.go-stdlib` | - | `rsa.EncryptOAEP(sha256.New(), rand.Reader, publicKey, message, nil)` | oaep-mgf-same-hash |
| GO-125 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 267:37 | 267:49 | [8161, 8173) | [8161, 8173) | 12 | 1 | `s17RSA3072` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New()` | - |
| GO-126 | S17 | `op:decrypt` | `rsa-oaep-sha256` | 269:20 | 269:83 | [8244, 8307) | [8244, 8307) | 63 | 0 | `s17RSA3072` | `crypto/rsa.DecryptOAEP` | `lib.go-stdlib` | - | `rsa.DecryptOAEP(sha256.New(), nil, privateKey, ciphertext, nil)` | - |
| GO-127 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 269:36 | 269:48 | [8260, 8272) | [8260, 8272) | 12 | 1 | `s17RSA3072` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New()` | - |
| GO-128 | S17 | `op:digest` | `sha-256` ^`rsassa-pss-sha256` | 273:12 | 273:34 | [8424, 8446) | [8424, 8446) | 22 | 0 | `s17RSA3072` | `crypto/sha256.Sum256` | `lib.go-stdlib` | - | `sha256.Sum256(message)` | prehash |
| GO-129 | S17 | `op:digest` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 273:12 | 273:34 | [8424, 8446) | [8424, 8446) | 22 | 1 | `s17RSA3072` | `crypto/sha256.Sum256` | `lib.go-stdlib` | - | `sha256.Sum256(message)` | prehash |
| GO-130 | S17 | `spec` | `rsassa-pss-sha256` | 274:16 | 274:72 | [8462, 8518) | [8462, 8518) | 56 | 0 | `s17RSA3072` | `crypto/rsa.PSSOptions` | `lib.go-stdlib` | - | `&rsa.PSSOptions{SaltLength: rsa.PSSSaltLengthEqualsHash}` | - |
| GO-131 | S17 | `prm:salt-length-bytes` | `rsassa-pss-sha256` | 274:44 | 274:71 | [8490, 8517) | [8490, 8517) | 27 | 1 | `s17RSA3072` | `crypto/rsa.PSSSaltLengthEqualsHash` | `lib.go-stdlib` | - | `rsa.PSSSaltLengthEqualsHash` | - |
| GO-132 | S17 | `op:sign` | `rsassa-pss-sha256` | 275:23 | 275:97 | [8541, 8615) | [8541, 8615) | 74 | 0 | `s17RSA3072` | `crypto/rsa.SignPSS` | `lib.go-stdlib` | - | `rsa.SignPSS(rand.Reader, privateKey, crypto.SHA256, digest[:], pssOptions)` | - |
| GO-133 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 275:60 | 275:73 | [8578, 8591) | [8578, 8591) | 13 | 1 | `s17RSA3072` | `crypto.SHA256` | `lib.go-stdlib` | - | `crypto.SHA256` | - |
| GO-134 | S17 | `op:verify` | `rsassa-pss-sha256` | 277:11 | 277:87 | [8638, 8714) | [8638, 8714) | 76 | 0 | `s17RSA3072` | `crypto/rsa.VerifyPSS` | `lib.go-stdlib` | - | `rsa.VerifyPSS(publicKey, crypto.SHA256, digest[:], pssSignature, pssOptions)` | - |
| GO-135 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 277:36 | 277:49 | [8663, 8676) | [8663, 8676) | 13 | 1 | `s17RSA3072` | `crypto.SHA256` | `lib.go-stdlib` | - | `crypto.SHA256` | - |
| GO-136 | S17 | `op:sign` | `rsassa-pkcs1v15-sha256` | 280:25 | 280:84 | [8809, 8868) | [8809, 8868) | 59 | 0 | `s17RSA3072` | `crypto/rsa.SignPKCS1v15` | `lib.go-stdlib` | - | `rsa.SignPKCS1v15(nil, privateKey, crypto.SHA256, digest[:])` | - |
| GO-137 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 280:59 | 280:72 | [8843, 8856) | [8843, 8856) | 13 | 1 | `s17RSA3072` | `crypto.SHA256` | `lib.go-stdlib` | - | `crypto.SHA256` | - |
| GO-138 | S17 | `op:verify` | `rsassa-pkcs1v15-sha256` | 282:13 | 282:84 | [8893, 8964) | [8893, 8964) | 71 | 0 | `s17RSA3072` | `crypto/rsa.VerifyPKCS1v15` | `lib.go-stdlib` | - | `rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, digest[:], pkcs1Signature)` | - |
| GO-139 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 282:43 | 282:56 | [8923, 8936) | [8923, 8936) | 13 | 1 | `s17RSA3072` | `crypto.SHA256` | `lib.go-stdlib` | - | `crypto.SHA256` | - |
| GO-140 | S18 | `op:keygen` | `ecdsa-p256-sha256` | 288:21 | 288:68 | [9119, 9166) | [9119, 9166) | 47 | 0 | `s18ECDSAP256` | `crypto/ecdsa.GenerateKey` | `lib.go-stdlib` | `m.ecdsa-private-key`, `m.ecdsa-public-key` | `ecdsa.GenerateKey(elliptic.P256(), rand.Reader)` | go126-rand-ignored |
| GO-141 | S18 | `alg` | `ecdsa-p256-sha256` | 288:39 | 288:54 | [9137, 9152) | [9137, 9152) | 15 | 1 | `s18ECDSAP256` | `crypto/elliptic.P256` | `lib.go-stdlib` | - | `elliptic.P256()` | - |
| GO-142 | S18 | `op:digest` | `sha-256` ^`ecdsa-p256-sha256` | 290:12 | 290:34 | [9190, 9212) | [9190, 9212) | 22 | 0 | `s18ECDSAP256` | `crypto/sha256.Sum256` | `lib.go-stdlib` | - | `sha256.Sum256(message)` | prehash |
| GO-143 | S18 | `op:sign` | `ecdsa-p256-sha256` | 291:20 | 291:70 | [9232, 9282) | [9232, 9282) | 50 | 0 | `s18ECDSAP256` | `crypto/ecdsa.SignASN1` | `lib.go-stdlib` | - | `ecdsa.SignASN1(rand.Reader, privateKey, digest[:])` | go126-rand-ignored |
| GO-144 | S18 | `op:verify` | `ecdsa-p256-sha256` | 293:8 | 293:69 | [9302, 9363) | [9302, 9363) | 61 | 0 | `s18ECDSAP256` | `crypto/ecdsa.VerifyASN1` | `lib.go-stdlib` | - | `ecdsa.VerifyASN1(&privateKey.PublicKey, digest[:], signature)` | - |
| GO-145 | S19 | `op:keygen` | `ed25519` | 299:16 | 299:51 | [9505, 9540) | [9505, 9540) | 35 | 0 | `s19Ed25519` | `crypto/ed25519.NewKeyFromSeed` | `lib.go-stdlib` | `m.ed25519-public-key` | `ed25519.NewKeyFromSeed(ed25519Seed)` | seed-ctor |
| GO-146 | S19 | `typ` | `ed25519` | 300:36 | 300:53 | [9576, 9593) | [9576, 9593) | 17 | 0 | `s19Ed25519` | `crypto/ed25519.PublicKey` | `lib.go-stdlib` | - | `ed25519.PublicKey` | - |
| GO-147 | S19 | `op:sign` | `ed25519` | 301:15 | 301:48 | [9609, 9642) | [9609, 9642) | 33 | 0 | `s19Ed25519` | `crypto/ed25519.Sign` | `lib.go-stdlib` | - | `ed25519.Sign(privateKey, message)` | - |
| GO-148 | S19 | `op:verify` | `ed25519` | 302:8 | 302:53 | [9650, 9695) | [9650, 9695) | 45 | 0 | `s19Ed25519` | `crypto/ed25519.Verify` | `lib.go-stdlib` | - | `ed25519.Verify(publicKey, message, signature)` | - |
| GO-149 | S20 | `op:keyderive` | `hkdf-sha256` | 307:14 | 307:70 | [9861, 9917) | [9861, 9917) | 56 | 0 | `deriveSessionKey` | `crypto/hkdf.Key` | `lib.go-stdlib` | `m.session-key` | `hkdf.Key(sha256.New, sharedSecret, nil, sessionInfo, 32)` | - |
| GO-150 | S20 | `alg` | `sha-256` ^`hkdf-sha256` | 307:23 | 307:33 | [9870, 9880) | [9870, 9880) | 10 | 1 | `deriveSessionKey` | `crypto/sha256.New` | `lib.go-stdlib` | - | `sha256.New` | hash-constructor |
| GO-151 | S20 | `prm:output-length-bytes` | `hkdf-sha256` | 307:67 | 307:69 | [9914, 9916) | [9914, 9916) | 2 | 1 | `deriveSessionKey` | - | `lib.go-stdlib` | - | `32` | - |
| GO-152 | S20 | `alg` | `x25519` | 314:12 | 314:25 | [10041, 10054) | [10041, 10054) | 13 | 0 | `s20KeyAgreement` | `crypto/ecdh.X25519` | `lib.go-stdlib` | - | `ecdh.X25519()` | - |
| GO-153 | S20 | `op:keygen` | `x25519` | 315:16 | 315:47 | [10070, 10101) | [10070, 10101) | 31 | 0 | `s20KeyAgreement` | `crypto/ecdh.Curve.GenerateKey` | `lib.go-stdlib` | `m.x25519-private-key-a` | `x25519.GenerateKey(rand.Reader)` | go126-rand-ignored |
| GO-154 | S20 | `op:keygen` | `x25519` | 317:14 | 317:45 | [10127, 10158) | [10127, 10158) | 31 | 0 | `s20KeyAgreement` | `crypto/ecdh.Curve.GenerateKey` | `lib.go-stdlib` | `m.x25519-private-key-b` | `x25519.GenerateKey(rand.Reader)` | go126-rand-ignored |
| GO-155 | S20 | `op:agree` | `x25519` | 319:17 | 319:44 | [10187, 10214) | [10187, 10214) | 27 | 0 | `s20KeyAgreement` | `crypto/ecdh.PrivateKey.ECDH` | `lib.go-stdlib` | `m.x25519-shared-secret` | `alice.ECDH(bob.PublicKey())` | - |
| GO-156 | S20 | `op:agree` | `x25519` | 321:15 | 321:42 | [10241, 10268) | [10241, 10268) | 27 | 0 | `s20KeyAgreement` | `crypto/ecdh.PrivateKey.ECDH` | `lib.go-stdlib` | `m.x25519-shared-secret` | `bob.ECDH(alice.PublicKey())` | - |
| GO-157 | S20 | `alg` | `ecdh-p256` | 325:10 | 325:21 | [10366, 10377) | [10366, 10377) | 11 | 0 | `s20KeyAgreement` | `crypto/ecdh.P256` | `lib.go-stdlib` | - | `ecdh.P256()` | - |
| GO-158 | S20 | `op:keygen` | `ecdh-p256` | 326:18 | 326:47 | [10395, 10424) | [10395, 10424) | 29 | 0 | `s20KeyAgreement` | `crypto/ecdh.Curve.GenerateKey` | `lib.go-stdlib` | `m.ecdh-private-key-a` | `p256.GenerateKey(rand.Reader)` | go126-rand-ignored |
| GO-159 | S20 | `op:keygen` | `ecdh-p256` | 328:16 | 328:45 | [10452, 10481) | [10452, 10481) | 29 | 0 | `s20KeyAgreement` | `crypto/ecdh.Curve.GenerateKey` | `lib.go-stdlib` | `m.ecdh-private-key-b` | `p256.GenerateKey(rand.Reader)` | go126-rand-ignored |
| GO-160 | S20 | `op:agree` | `ecdh-p256` | 330:17 | 330:48 | [10510, 10541) | [10510, 10541) | 31 | 0 | `s20KeyAgreement` | `crypto/ecdh.PrivateKey.ECDH` | `lib.go-stdlib` | `m.ecdh-shared-secret` | `aliceEC.ECDH(bobEC.PublicKey())` | - |
| GO-161 | S20 | `op:agree` | `ecdh-p256` | 332:15 | 332:46 | [10568, 10599) | [10568, 10599) | 31 | 0 | `s20KeyAgreement` | `crypto/ecdh.PrivateKey.ECDH` | `lib.go-stdlib` | `m.ecdh-shared-secret` | `bobEC.ECDH(aliceEC.PublicKey())` | - |
| GO-162 | S21 | `op:keygen` | `ml-kem-768` | 343:27 | 343:49 | [10987, 11009) | [10987, 11009) | 22 | 0 | `s21MLKEM768` | `crypto/mlkem.GenerateKey768` | `lib.go-stdlib` | `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key` | `mlkem.GenerateKey768()` | - |
| GO-163 | S21 | `op:encapsulate` | `ml-kem-768` | 345:30 | 345:79 | [11051, 11100) | [11051, 11100) | 49 | 0 | `s21MLKEM768` | `crypto/mlkem.EncapsulationKey768.Encapsulate` | `lib.go-stdlib` | `m.mlkem-shared-secret` | `decapsulationKey.EncapsulationKey().Encapsulate()` | - |
| GO-164 | S21 | `op:decapsulate` | `ml-kem-768` | 346:20 | 346:60 | [11120, 11160) | [11120, 11160) | 40 | 0 | `s21MLKEM768` | `crypto/mlkem.DecapsulationKey768.Decapsulate` | `lib.go-stdlib` | `m.mlkem-shared-secret` | `decapsulationKey.Decapsulate(ciphertext)` | - |
| GO-165 | S22 | `op:keygen` | `ml-dsa-65` | 353:32 | 353:64 | [11394, 11426) | [11394, 11426) | 32 | 0 | `s22MLDSA65` | `github.com/cloudflare/circl/sign/mldsa/mldsa65.GenerateKey` | `lib.circl` | `m.mldsa-private-key`, `m.mldsa-public-key` | `mldsa65.GenerateKey(rand.Reader)` | - |
| GO-166 | S22 | `prm:signature-size-bytes` | `ml-dsa-65` | 355:28 | 355:49 | [11466, 11487) | [11466, 11487) | 21 | 0 | `s22MLDSA65` | `github.com/cloudflare/circl/sign/mldsa/mldsa65.SignatureSize` | `lib.circl` | - | `mldsa65.SignatureSize` | - |
| GO-167 | S22 | `op:sign` | `ml-dsa-65` | 356:8 | 356:65 | [11496, 11553) | [11496, 11553) | 57 | 0 | `s22MLDSA65` | `github.com/cloudflare/circl/sign/mldsa/mldsa65.SignTo` | `lib.circl` | - | `mldsa65.SignTo(privateKey, message, nil, true, signature)` | ctx-default |
| GO-168 | S22 | `prm:randomized` | `ml-dsa-65` | 356:49 | 356:53 | [11537, 11541) | [11537, 11541) | 4 | 1 | `s22MLDSA65` | - | `lib.circl` | - | `true` | hedged |
| GO-169 | S22 | `op:verify` | `ml-dsa-65` | 357:8 | 357:58 | [11562, 11612) | [11562, 11612) | 50 | 0 | `s22MLDSA65` | `github.com/cloudflare/circl/sign/mldsa/mldsa65.Verify` | `lib.circl` | - | `mldsa65.Verify(publicKey, message, nil, signature)` | - |
| GO-170 | S23 | `op:keygen` | `ecdsa-p256-sha256` | 363:14 | 363:61 | [11773, 11820) | [11773, 11820) | 47 | 0 | `s23X509SelfSigned` | `crypto/ecdsa.GenerateKey` | `lib.go-stdlib` | `m.cert-private-key`, `m.cert-public-key` | `ecdsa.GenerateKey(elliptic.P256(), rand.Reader)` | go126-rand-ignored |
| GO-171 | S23 | `alg` | `ecdsa-p256-sha256` | 363:32 | 363:47 | [11791, 11806) | [11791, 11806) | 15 | 1 | `s23X509SelfSigned` | `crypto/elliptic.P256` | `lib.go-stdlib` | - | `elliptic.P256()` | - |
| GO-172 | S23 | `op:generate` | `csprng` | 365:17 | 365:75 | [11849, 11907) | [11849, 11907) | 58 | 0 | `s23X509SelfSigned` | `crypto/rand.Int` | `lib.go-stdlib` | - | `rand.Int(rand.Reader, new(big.Int).Lsh(big.NewInt(1), 64))` | serial |
| GO-173 | S23 | `ctor` | `cert.self-signed` | 368:14 | 374:3 | [11952, 12205) | [11952, 12205) | 253 | 0 | `s23X509SelfSigned` | `crypto/x509.Certificate` | `lib.go-stdlib` | - | `&x509.Certificate{ … (+6 lines)` | - |
| GO-174 | S23 | `prm:validity-days` | `cert.self-signed` | 372:31 | 372:34 | [12136, 12139) | [12136, 12139) | 3 | 1 | `s23X509SelfSigned` | - | `lib.go-stdlib` | - | `365` | - |
| GO-175 | S23 | `alg` | `ecdsa-p256-sha256` | 373:23 | 373:43 | [12181, 12201) | [12181, 12201) | 20 | 1 | `s23X509SelfSigned` | `crypto/x509.ECDSAWithSHA256` | `lib.go-stdlib` | - | `x509.ECDSAWithSHA256` | - |
| GO-176 | S23 | `op:sign` | `cert.self-signed` | 375:14 | 375:90 | [12219, 12295) | [12219, 12295) | 76 | 0 | `s23X509SelfSigned` | `crypto/x509.CreateCertificate` | `lib.go-stdlib` | - | `x509.CreateCertificate(rand.Reader, template, template, &key.PublicKey, key)` | - |
| GO-177 | S23 | `op:encode` | `cert.self-signed` | 377:22 | 377:48 | [12329, 12355) | [12329, 12355) | 26 | 0 | `s23X509SelfSigned` | `crypto/x509.ParseCertificate` | `lib.go-stdlib` | - | `x509.ParseCertificate(der)` | - |
| GO-178 | S23 | `op:verify` | `ecdsa-p256-sha256` | 379:8 | 379:120 | [12375, 12487) | [12375, 12487) | 112 | 0 | `s23X509SelfSigned` | `crypto/x509.Certificate.CheckSignature` | `lib.go-stdlib` | - | `certificate.CheckSignature(certificate.SignatureAlgorithm, certificate.RawTBSCertificate, certificate.Signature)` | - |
| GO-179 | S24 | `ctor` | `tls13-client` | 385:12 | 389:3 | [12663, 12771) | [12663, 12771) | 108 | 0 | `s24TLS13Client` | `crypto/tls.Config` | `lib.go-stdlib` | - | `&tls.Config{ … (+4 lines)` | - |
| GO-180 | S24 | `cfg:min-version` | `tls13-client` | 386:15 | 386:31 | [12690, 12706) | [12690, 12706) | 16 | 1 | `s24TLS13Client` | `crypto/tls.VersionTLS13` | `lib.go-stdlib` | - | `tls.VersionTLS13` | - |
| GO-181 | S24 | `cfg:max-version` | `tls13-client` | 387:15 | 387:31 | [12722, 12738) | [12722, 12738) | 16 | 1 | `s24TLS13Client` | `crypto/tls.VersionTLS13` | `lib.go-stdlib` | - | `tls.VersionTLS13` | - |

## Full text of multi-line evidence

**GO-173** (`cert.self-signed`, 368:14 to 374:3):

```text
&x509.Certificate{
		SerialNumber:       serial,
		Subject:            pkix.Name{CommonName: tlsServerName},
		NotBefore:          now.Add(-time.Minute),
		NotAfter:           now.Add(365 * 24 * time.Hour),
		SignatureAlgorithm: x509.ECDSAWithSHA256,
	}
```

**GO-179** (`tls13-client`, 385:12 to 389:3):

```text
&tls.Config{
		MinVersion: tls.VersionTLS13,
		MaxVersion: tls.VersionTLS13,
		ServerName: tlsServerName,
	}
```

## Non-asset mentions (negative ground truth)

Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.

| ID | L:C | Bytes | Match | Context | Containing token / line | Why it is not an asset |
|---|---|---|---|---|---|---|
| GO-N001 | 47:62 | [1080, 1084) | `HMAC` | comment | `// Hard-coded material (public test vectors only): Wikipedia HMAC example key,` | Comment text; documentation only |
| GO-N002 | 48:47 | [1144, 1147) | `GCM` | comment | `// RFC 5869 A.1, RFC 7914 sections 11 and 12, GCM specification test case 16,` | Comment text; documentation only |
| GO-N003 | 103:9 | [2920, 2927) | `SHA-256` | comment | `// S01: SHA-256 (FIPS 180-4)` | Comment text; documentation only |
| GO-N004 | 106:15 | [3008, 3015) | `SHA-256` | string | `"SHA-256"` | Output label passed to emit(); printed text only |
| GO-N005 | 109:9 | [3060, 3067) | `SHA-512` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| GO-N006 | 109:18 | [3069, 3077) | `SHA3-256` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| GO-N007 | 109:28 | [3079, 3086) | `BLAKE2b` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| GO-N008 | 112:15 | [3172, 3179) | `SHA-512` | string | `"SHA-512"` | Output label passed to emit(); printed text only |
| GO-N009 | 114:15 | [3269, 3277) | `SHA3-256` | string | `"SHA3-256"` | Output label passed to emit(); printed text only |
| GO-N010 | 116:15 | [3369, 3376) | `BLAKE2b` | string | `"BLAKE2b-512"` | Output label passed to emit(); printed text only |
| GO-N011 | 122:15 | [3535, 3538) | `MD5` | string | `"MD5"` | Output label passed to emit(); printed text only |
| GO-N012 | 124:15 | [3622, 3627) | `SHA-1` | string | `"SHA-1"` | Output label passed to emit(); printed text only |
| GO-N013 | 127:9 | [3676, 3684) | `SHAKE128` | comment | `// S04: SHAKE128 extendable-output function` | Comment text; documentation only |
| GO-N014 | 130:15 | [3785, 3793) | `SHAKE128` | string | `"SHAKE128"` | Output label passed to emit(); printed text only |
| GO-N015 | 133:9 | [3832, 3836) | `HMAC` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| GO-N016 | 133:14 | [3837, 3843) | `SHA256` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| GO-N017 | 137:15 | [3939, 3943) | `HMAC` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| GO-N018 | 137:20 | [3944, 3950) | `SHA256` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| GO-N019 | 140:9 | [3998, 4002) | `HKDF` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| GO-N020 | 140:14 | [4003, 4009) | `SHA256` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| GO-N021 | 144:15 | [4145, 4149) | `HKDF` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| GO-N022 | 144:20 | [4150, 4156) | `SHA256` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| GO-N023 | 147:9 | [4195, 4201) | `PBKDF2` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| GO-N024 | 147:16 | [4202, 4206) | `HMAC` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| GO-N025 | 147:21 | [4207, 4213) | `SHA256` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| GO-N026 | 151:15 | [4339, 4345) | `PBKDF2` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| GO-N027 | 151:22 | [4346, 4352) | `SHA256` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| GO-N028 | 154:9 | [4395, 4401) | `scrypt` | comment | `// S08: scrypt` | Comment text; documentation only |
| GO-N029 | 158:15 | [4520, 4526) | `scrypt` | string | `"scrypt"` | Output label passed to emit(); printed text only |
| GO-N030 | 161:9 | [4569, 4577) | `Argon2id` | comment | `// S09: Argon2id` | Comment text; documentation only |
| GO-N031 | 164:15 | [4674, 4682) | `Argon2id` | string | `"Argon2id"` | Output label passed to emit(); printed text only |
| GO-N032 | 167:9 | [4721, 4727) | `bcrypt` | comment | `// S10: bcrypt` | Comment text; documentation only |
| GO-N033 | 172:15 | [4889, 4895) | `bcrypt` | string | `"bcrypt"` | Output label passed to emit(); printed text only |
| GO-N034 | 175:9 | [4939, 4946) | `AES-256` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| GO-N035 | 175:17 | [4947, 4950) | `GCM` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| GO-N036 | 185:15 | [5265, 5272) | `AES-256` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| GO-N037 | 185:23 | [5273, 5276) | `GCM` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| GO-N038 | 188:9 | [5405, 5422) | `ChaCha20-Poly1305` | comment | `// S12: ChaCha20-Poly1305 (RFC 8439)` | Comment text; documentation only |
| GO-N039 | 199:15 | [5771, 5788) | `ChaCha20-Poly1305` | string | `"ChaCha20-Poly1305"` | Output label passed to emit(); printed text only |
| GO-N040 | 202:9 | [5861, 5868) | `AES-256` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| GO-N041 | 202:17 | [5869, 5872) | `CBC` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| GO-N042 | 215:15 | [6332, 6339) | `AES-256` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| GO-N043 | 215:23 | [6340, 6343) | `CBC` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| GO-N044 | 218:9 | [6431, 6438) | `AES-128` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| GO-N045 | 218:17 | [6439, 6442) | `ECB` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| GO-N046 | 227:15 | [6789, 6796) | `AES-128` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| GO-N047 | 227:23 | [6797, 6800) | `ECB` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| GO-N048 | 230:9 | [6846, 6853) | `AES-256` | comment | `// S15: AES-256-CTR` | Comment text; documentation only |
| GO-N049 | 230:17 | [6854, 6857) | `CTR` | comment | `// S15: AES-256-CTR` | Comment text; documentation only |
| GO-N050 | 242:15 | [7279, 7286) | `AES-256` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| GO-N051 | 242:23 | [7287, 7290) | `CTR` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| GO-N052 | 245:9 | [7366, 7370) | `3DES` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| GO-N053 | 245:15 | [7372, 7376) | `TDEA` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| GO-N054 | 245:21 | [7378, 7381) | `CBC` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| GO-N055 | 258:15 | [7850, 7854) | `3DES` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| GO-N056 | 258:20 | [7855, 7858) | `CBC` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| GO-N057 | 261:9 | [7946, 7949) | `RSA` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| GO-N058 | 261:20 | [7957, 7961) | `OAEP` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| GO-N059 | 261:26 | [7963, 7966) | `PSS` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| GO-N060 | 271:15 | [8334, 8337) | `RSA` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| GO-N061 | 271:24 | [8343, 8347) | `OAEP` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| GO-N062 | 278:15 | [8736, 8739) | `RSA` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| GO-N063 | 278:24 | [8745, 8748) | `PSS` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| GO-N064 | 283:15 | [8986, 8989) | `RSA` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| GO-N065 | 283:24 | [8995, 9003) | `PKCS1v15` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| GO-N066 | 286:9 | [9052, 9057) | `ECDSA` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| GO-N067 | 286:15 | [9058, 9063) | `P-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| GO-N068 | 286:26 | [9069, 9076) | `SHA-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| GO-N069 | 294:15 | [9378, 9383) | `ECDSA` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| GO-N070 | 294:21 | [9384, 9389) | `P-256` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| GO-N071 | 297:9 | [9433, 9440) | `Ed25519` | comment | `// S19: Ed25519 from a fixed seed (RFC 8032)` | Comment text; documentation only |
| GO-N072 | 303:15 | [9710, 9717) | `Ed25519` | string | `"Ed25519"` | Output label passed to emit(); printed text only |
| GO-N073 | 312:9 | [9953, 9959) | `X25519` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| GO-N074 | 312:18 | [9962, 9966) | `ECDH` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| GO-N075 | 312:23 | [9967, 9972) | `P-256` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| GO-N076 | 312:44 | [9988, 9992) | `HKDF` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| GO-N077 | 314:2 | [10031, 10037) | `x25519` | identifier | `x25519` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| GO-N078 | 323:15 | [10295, 10301) | `X25519` | string | `"X25519"` | Output label passed to emit(); printed text only |
| GO-N079 | 325:2 | [10358, 10362) | `p256` | identifier | `p256` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| GO-N080 | 334:15 | [10626, 10630) | `ECDH` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| GO-N081 | 334:20 | [10631, 10636) | `P-256` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| GO-N082 | 338:15 | [10836, 10840) | `HKDF` | string | `"HKDF session key"` | Output label passed to emit(); printed text only |
| GO-N083 | 341:9 | [10918, 10928) | `ML-KEM-768` | comment | `// S21: ML-KEM-768 (FIPS 203)` | Comment text; documentation only |
| GO-N084 | 348:15 | [11187, 11197) | `ML-KEM-768` | string | `"ML-KEM-768"` | Output label passed to emit(); printed text only |
| GO-N085 | 351:9 | [11322, 11331) | `ML-DSA-65` | comment | `// S22: ML-DSA-65 (FIPS 204)` | Comment text; documentation only |
| GO-N086 | 358:15 | [11627, 11636) | `ML-DSA-65` | string | `"ML-DSA-65"` | Output label passed to emit(); printed text only |
| GO-N087 | 361:21 | [11715, 11720) | `X.509` | comment | `// S23: self-signed X.509 certificate` | Comment text; documentation only |
| GO-N088 | 380:15 | [12509, 12514) | `X.509` | string | `"X.509 self-signed"` | Output label passed to emit(); printed text only |
| GO-N089 | 383:9 | [12570, 12573) | `TLS` | comment | `// S24: TLS 1.3-only client configuration (no connection is made)` | Comment text; documentation only |
| GO-N090 | 390:15 | [12786, 12789) | `TLS` | string | `"TLS 1.3 client"` | Output label passed to emit(); printed text only |

## Implicit and runtime-dependent cryptography

Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where source-level ground truth and the cryptography that actually executes can diverge.

| Asset | What happens |
|---|---|
| `csprng` | crypto/rand reads getrandom(2). Since Go 1.26, rsa/ecdsa/ecdh key generation and ECDSA signing ignore the io.Reader they are given and always use this source. |
| `bcrypt` | x/crypto/bcrypt always emits the $2a$ prefix and generates its own salt. |
| `argon2id` | argon2.IDKey hard-codes version 0x13; 'Argon2id' is identified only by the function name IDKey. |
| `mgf1-sha256` | rsa.EncryptOAEP and rsa.SignPSS use the OAEP/PSS hash for MGF1 implicitly. |
| `aes-256-gcm` | cipher.NewGCM fixes a 16-byte tag and 12-byte nonce (implicit). |
| `tls13-client` | TLS 1.3 cipher suites are not configurable in crypto/tls; all three RFC 8446 suites are enabled implicitly. Default key-exchange preferences include the X25519MLKEM768 post-quantum hybrid (Go >= 1.24). |
| `sha-512` | crypto/ed25519 uses SHA-512 internally. |

Default `crypto/tls` key-exchange preferences in Go 1.26: X25519MLKEM768, SecP256r1MLKEM768, SecP384r1MLKEM1024, X25519, P-256, P-384, P-521.

## Detection notes

Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.

| Note | Explanation | Occurrences |
|---|---|---|
| `hash-constructor` | Hash passed as a constructor/function reference rather than by name. | GO-054, GO-057, GO-060, GO-150 |
| `computed` | Parameter is a constant expression, not a literal (evaluates to 16384). | GO-064 |
| `mode-ctor` | Mode is named only by the constructor/function name. | GO-068, GO-077, GO-094, GO-096, GO-108, GO-110, GO-118, GO-120 |
| `bcrypt-internal-salt` | The 16-byte salt is generated inside the library from the OS CSPRNG; the program has no salt variable. | GO-073 |
| `keysize-from-key` | Key size is not named in code; it follows from the length of the key bytes (data-flow dependent). | GO-076, GO-091, GO-098, GO-106 |
| `manual-pkcs7` | PKCS#7 padding implemented in application code (pkcs7Pad/pkcs7Unpad); no library padding identifier exists. | GO-092, GO-097, GO-099, GO-116, GO-121 |
| `manual-ecb` | ECB realised by looping raw single-block encryption; the string 'ECB' never appears in code. | GO-100, GO-101 |
| `go126-rand-ignored` | Since Go 1.26 the io.Reader argument is ignored and the runtime's secure source is always used (GODEBUG=cryptocustomrand=1 restores the old behaviour). | GO-122, GO-140, GO-143, GO-153, GO-154, GO-158, GO-159, GO-170 |
| `oaep-mgf-same-hash` | MGF1 hash is implicit and equals the OAEP hash (SHA-256); MGF1 has no source occurrence here. | GO-124 |
| `prehash` | Caller pre-hashes the message; the digest feeds the signature scheme. | GO-128, GO-129, GO-142 |
| `seed-ctor` | Key pair is derived deterministically from the hard-coded 32-byte seed. | GO-145 |
| `ctx-default` | Empty context string (FIPS 204 pure ML-DSA). | GO-167 |
| `hedged` | Hedged (randomised) ML-DSA signing is selected explicitly; this is the FIPS 204 default. | GO-168 |
| `serial` | CSPRNG output used for the certificate serial number (not key material). | GO-172 |

## Machine-readable files

`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset (with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts (NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.
