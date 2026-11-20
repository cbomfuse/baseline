# CBOM ground-truth corpus - TypeScript

`src/main.ts` is the TypeScript implementation of a 24-scenario cryptography program that is logically identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic asset appears in it: **192 occurrences** of **84 assets** (33 algorithms, 49 items of related crypto material, 1 certificate, 1 protocol) drawn from **7 library components**, plus **96 non-asset mentions** of algorithm names that a scanner should *not* report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.

## Files

| File | Purpose |
|---|---|
| `src/main.ts` | The program (365 lines, ASCII, LF line endings) |
| `package.json` | Build manifest |
| `tsconfig.json` | Build manifest |
| `README.md` | This document |
| `cbom.cdx.json` | Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema) |
| `ground-truth.json` | Complete occurrence ledger, asset inventory and non-asset mentions |

## Build and run

```sh
npm install
npm run build
npm start
```

Verified in the build environment with Node.js 22.22.2 (bundled OpenSSL 3.5.5), TypeScript 7.0.2: npm install, tsc with 0 diagnostics, node dist/main.js. Standard output was byte-identical to the other four implementations (see the corpus README).

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
| Occurrences | 192 |
| Occurrences with role `imp` | 12 |
| Occurrences with role `alg` | 44 |
| Occurrences with role `ctor` | 19 |
| Occurrences with role `init` | 1 |
| Occurrences with role `op` | 66 |
| Occurrences with role `prm` | 31 |
| Occurrences with role `mat` | 16 |
| Occurrences with role `cfg` | 3 |
| Algorithm assets (incl. implicit) | 33 |
| Implicit assets (no source occurrence) | 3 |
| Related crypto material | 49 |
| Certificates | 1 |
| Protocols | 1 |
| Library components | 7 |
| Non-asset mentions | 96 |

## Libraries

| ID | Component | Version | purl | License | Scope | Import occurrences | Other occurrences | Assets provided | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `lib.node` | Node.js runtime (node:crypto, node:tls, WebCrypto) | 22.22.2 | `pkg:generic/node@22.22.2` | MIT | runtime | TS-001, TS-002 | 147 | sha-256, sha-512, md5, sha-1, shake128, hmac-sha256, hkdf-sha256, pbkdf2-hmac-sha256, scrypt, aes-256-gcm, aes-256-cbc, aes-128-ecb, aes-256-ctr, 3des-cbc, rsa-3072, rsa-oaep-sha256, rsassa-pss-sha256, rsassa-pkcs1v15-sha256, ecdsa-p256-sha256, ecdh-p256, x25519, csprng, tls13-client, m.hmac-key, m.hkdf-ikm, m.hkdf-salt, m.hkdf-info, m.pbkdf2-password, m.pbkdf2-salt, m.scrypt-password, m.scrypt-salt, m.password, m.argon2-salt, m.gcm-key, m.gcm-iv, m.gcm-aad, m.cbc-key, m.cbc-iv, m.ecb-key, m.ctr-iv, m.tdes-key, m.tdes-iv, m.ed25519-seed, m.session-info | Bundles OpenSSL 3.5.5; WebCrypto exposed as crypto.webcrypto |
| `lib.noble-hashes` | @noble/hashes | 2.4.0 | `pkg:npm/%40noble/hashes@2.4.0` | MIT | required | TS-006, TS-007, TS-008 | 8 | sha3-256, blake2b-512, argon2id | Pure TypeScript: SHA3-256, BLAKE2b, Argon2id |
| `lib.noble-ciphers` | @noble/ciphers | 2.4.0 | `pkg:npm/%40noble/ciphers@2.4.0` | MIT | required | TS-003, TS-004 | 8 | chacha20-poly1305, csprng, m.chacha-key, m.chacha-nonce | Pure TypeScript: ChaCha20-Poly1305, randomBytes (wraps crypto.getRandomValues) |
| `lib.noble-curves` | @noble/curves | 2.4.0 | `pkg:npm/%40noble/curves@2.4.0` | MIT | required | TS-005 | 3 | ed25519 | Pure TypeScript: Ed25519 |
| `lib.noble-pq` | @noble/post-quantum | 0.7.1 | `pkg:npm/%40noble/post-quantum@0.7.1` | MIT | required | TS-009, TS-010 | 6 | ml-kem-768, ml-dsa-65 | Pure TypeScript: ML-KEM-768, ML-DSA-65 |
| `lib.bcryptjs` | bcryptjs | 3.0.3 | `pkg:npm/bcryptjs@3.0.3` | BSD-3-Clause | required | TS-012 | 4 | bcrypt, csprng | Pure JavaScript bcrypt |
| `lib.peculiar-x509` | @peculiar/x509 | 3.1.0 | `pkg:npm/%40peculiar/x509@3.1.0` | MIT | required | TS-011 | 4 | ecdsa-p256-sha256, cert.self-signed | X.509 builder on top of WebCrypto (needs the reflect-metadata polyfill) |

## Algorithm assets

Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):

| Asset | Name | Primitive | Family | Parameter set | Mode | Padding | Curve | Functions | OID | Occurrences | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.1 | 15 | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | - | - | - | 2.16.840.1.101.3.4.2.2 | implicit | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | - | - | digest | 2.16.840.1.101.3.4.2.3 | 3 | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.8 | 1 | - |
| `blake2b-512` | BLAKE2b-512 | hash | BLAKE2 | 512 | - | - | - | digest | 1.3.6.1.4.1.1722.12.2.1.16 | 2 | - |
| `md5` | MD5 | hash | MD5 | 128 | - | - | - | digest | 1.2.840.113549.2.5 | 3 | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | - | - | digest | 1.3.14.3.2.26 | 3 | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | - | - | digest | 2.16.840.1.101.3.4.2.11 | 4 | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | - | - | tag | 1.2.840.113549.2.9 | 3 | sha-256 |
| `hkdf-sha256` | HKDF-SHA256 | kdf | HKDF | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.9.16.3.29 | 6 | hmac-sha256, sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.5.12 | 7 | hmac-sha256, sha-256 |
| `scrypt` | scrypt | kdf | scrypt | N=16384,r=8,p=1 | - | - | - | keyderive | 1.3.6.1.4.1.11591.4.11 | 5 | pbkdf2-hmac-sha256 |
| `argon2id` | Argon2id | kdf | Argon2 | t=2,m=19456,p=1,v=0x13 | - | - | - | keyderive | - | 5 | - |
| `bcrypt` | bcrypt | kdf | bcrypt | cost=12 | - | - | - | keyderive, verify | - | 3 | - |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | gcm | - | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.46 | 8 | - |
| `aes-128-gcm` | AES-128-GCM | ae | AES | 128 | gcm | - | - | - | 2.16.840.1.101.3.4.1.6 | implicit | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | other | - | - | decrypt, encrypt | 1.2.840.113549.1.9.16.3.18 | 4 | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | cbc | pkcs7 | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.42 | 6 | - |
| `aes-128-ecb` | AES-128-ECB-PKCS7 | block-cipher | AES | 128 | ecb | pkcs7 | - | encrypt | 2.16.840.1.101.3.4.1.1 | 3 | - |
| `aes-256-ctr` | AES-256-CTR | block-cipher | AES | 256 | ctr | - | - | decrypt, encrypt, keygen | - | 7 | - |
| `3des-cbc` | 3DES-CBC-PKCS7 (3-key TDEA) | block-cipher | 3DES | 168 | cbc | pkcs7 | - | decrypt, encrypt | 1.2.840.113549.3.7 | 6 | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | - | - | keygen | 1.2.840.113549.1.1.1 | 4 | - |
| `mgf1-sha256` | MGF1-SHA256 | other | MGF1 | SHA-256 | - | - | - | - | 1.2.840.113549.1.1.8 | implicit | sha-256 |
| `rsa-oaep-sha256` | RSAES-OAEP-SHA256 (RSA-3072) | pke | RSA | 3072 | - | oaep | - | decrypt, encrypt | 1.2.840.113549.1.1.7 | 6 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pss-sha256` | RSASSA-PSS-SHA256 (RSA-3072) | signature | RSA | 3072 | - | other | - | sign, verify | 1.2.840.113549.1.1.10 | 8 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pkcs1v15-sha256` | RSASSA-PKCS1-v1_5-SHA256 (RSA-3072) | signature | RSA | 3072 | - | pkcs1v15 | - | sign, verify | 1.2.840.113549.1.1.11 | 6 | rsa-3072, sha-256 |
| `ecdsa-p256-sha256` | ECDSA P-256 with SHA-256 | signature | ECDSA | P-256 | - | - | secp256r1 | keygen, sign, verify | 1.2.840.10045.4.3.2 | 12 | sha-256 |
| `ecdh-p256` | ECDH P-256 | key-agree | ECDH | P-256 | - | - | secp256r1 | keyderive, keygen | 1.3.132.1.12 | 8 | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | - | - | curve25519 | keyderive, keygen | 1.3.101.110 | 6 | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | - | - | edwards25519 | keygen, sign, verify | 1.3.101.112 | 3 | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | - | - | decapsulate, encapsulate, keygen | 2.16.840.1.101.3.4.4.2 | 3 | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | - | - | keygen, sign, verify | 2.16.840.1.101.3.4.3.18 | 3 | - |
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
| `sha-256` | TS-029, TS-030, TS-031, TS-049, TS-052, TS-058, TS-129, TS-132, TS-134, TS-138, TS-142, TS-145, TS-151, TS-158, TS-183 |
| `sha-512` | TS-032, TS-033, TS-034 |
| `sha3-256` | TS-035 |
| `blake2b-512` | TS-036, TS-037 |
| `md5` | TS-038, TS-039, TS-040 |
| `sha-1` | TS-041, TS-042, TS-043 |
| `shake128` | TS-044, TS-045, TS-046, TS-047 |
| `hmac-sha256` | TS-048, TS-049 (parameter:sha-256), TS-050 |
| `hkdf-sha256` | TS-051, TS-052 (parameter:sha-256), TS-053, TS-157, TS-158 (parameter:sha-256), TS-159 |
| `pbkdf2-hmac-sha256` | TS-054, TS-055, TS-056, TS-057, TS-058 (parameter:sha-256), TS-059, TS-060 |
| `scrypt` | TS-061, TS-062, TS-063, TS-064, TS-065 |
| `argon2id` | TS-066, TS-067, TS-068, TS-069, TS-070 |
| `bcrypt` | TS-072, TS-073, TS-074 |
| `aes-256-gcm` | TS-075, TS-076, TS-077, TS-078, TS-079, TS-080, TS-081, TS-082 |
| `chacha20-poly1305` | TS-087, TS-088, TS-089, TS-090 |
| `aes-256-cbc` | TS-095, TS-096, TS-097, TS-098, TS-099, TS-100 |
| `aes-128-ecb` | TS-101, TS-102, TS-103 |
| `aes-256-ctr` | TS-104, TS-105, TS-106, TS-109, TS-110, TS-111, TS-112 |
| `3des-cbc` | TS-117, TS-118, TS-119, TS-120, TS-121, TS-122 |
| `rsa-3072` | TS-123, TS-124, TS-125, TS-126 |
| `rsa-oaep-sha256` | TS-127, TS-128, TS-129 (parameter:sha-256), TS-130, TS-131, TS-132 (parameter:sha-256) |
| `rsassa-pss-sha256` | TS-133, TS-134 (parameter:sha-256), TS-135, TS-136, TS-137, TS-138 (parameter:sha-256), TS-139, TS-140 |
| `rsassa-pkcs1v15-sha256` | TS-141, TS-142 (parameter:sha-256), TS-143, TS-144, TS-145 (parameter:sha-256), TS-146 |
| `ecdsa-p256-sha256` | TS-147, TS-148, TS-149, TS-150, TS-151 (parameter:sha-256), TS-152, TS-153, TS-181, TS-182, TS-183 (parameter:sha-256), TS-184, TS-188 |
| `ecdh-p256` | TS-166, TS-167, TS-168, TS-169, TS-170, TS-171, TS-172, TS-173 |
| `x25519` | TS-160, TS-161, TS-162, TS-163, TS-164, TS-165 |
| `ed25519` | TS-154, TS-155, TS-156 |
| `ml-kem-768` | TS-174, TS-175, TS-176 |
| `ml-dsa-65` | TS-177, TS-178, TS-179 |
| `csprng` | TS-071, TS-083, TS-085, TS-091, TS-093, TS-107, TS-113, TS-115, TS-186 |
| `cert.self-signed` | TS-180, TS-185, TS-187 |
| `tls13-client` | TS-189, TS-190, TS-191, TS-192 |

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
| Occurrences | TS-180, TS-185, TS-187 |

| Property | Value |
|---|---|
| Asset | `tls13-client` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_128_GCM_SHA256 (0x13,0x01); TLS_AES_256_GCM_SHA384 (0x13,0x02); TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03) |
| Note | Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime defaults. |
| Occurrences | TS-189, TS-190, TS-191, TS-192 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Provenance | Test-vector value | Used with | Scenario | Defined / produced at | Note |
|---|---|---|---|---|---|---|---|---|---|
| `m.hmac-key` | HMAC key | secret-key | 24 | hardcoded | "key" (ASCII) | `hmac-sha256` | S05 | TS-013 @ 32:7 | 24-bit key - far below the 112-bit minimum; test vector only |
| `m.hkdf-ikm` | HKDF input keying material | secret-key | 176 | hardcoded | 0x0b * 22 | `hkdf-sha256` | S06 | TS-014 @ 34:7 | RFC 5869 A.1 |
| `m.hkdf-salt` | HKDF salt | salt | 104 | hardcoded | 000102...0c | `hkdf-sha256` | S06 | TS-015 @ 35:7 | RFC 5869 A.1 |
| `m.hkdf-info` | HKDF info | additional-data | 80 | hardcoded | f0f1...f9 | `hkdf-sha256` | S06 | TS-016 @ 36:7 | RFC 5869 A.1 |
| `m.hkdf-okm` | HKDF output keying material | secret-key | 336 | derived | - | `hkdf-sha256` | S06 | TS-051 @ 112:15 (produced) | - |
| `m.pbkdf2-password` | PBKDF2 password | password | 64 | hardcoded | "Password" | `pbkdf2-hmac-sha256` | S07 | TS-017 @ 38:7 | RFC 7914 section 11 |
| `m.pbkdf2-salt` | PBKDF2 salt | salt | 32 | hardcoded | "NaCl" | `pbkdf2-hmac-sha256` | S07 | TS-018 @ 39:7 | 32-bit salt is below the SP 800-132 minimum of 128 bits |
| `m.pbkdf2-dk` | PBKDF2 derived key | secret-key | 512 | derived | - | `pbkdf2-hmac-sha256` | S07 | TS-056 @ 119:22 (produced) | - |
| `m.scrypt-password` | scrypt password | password | 104 | hardcoded | "pleaseletmein" | `scrypt` | S08 | TS-019 @ 40:7 | RFC 7914 section 12 |
| `m.scrypt-salt` | scrypt salt | salt | 112 | hardcoded | "SodiumChloride" | `scrypt` | S08 | TS-020 @ 41:7 | - |
| `m.scrypt-dk` | scrypt derived key | secret-key | 512 | derived | - | `scrypt` | S08 | TS-061 @ 129:19 (produced) | - |
| `m.password` | Application password | password | 224 | hardcoded | "correct horse battery staple" | `argon2id` | S09 | TS-021 @ 42:7 | Shared by S09 (Argon2id) and S10 (bcrypt) |
| `m.argon2-salt` | Argon2id salt | salt | 128 | hardcoded | "cbom-corpus-salt" | `argon2id` | S09 | TS-022 @ 43:7 | - |
| `m.argon2-dk` | Argon2id output | secret-key | 256 | derived | - | `argon2id` | S09 | TS-066 @ 135:15 (produced) | - |
| `m.bcrypt-salt` | bcrypt salt | salt | 128 | csprng | - | `bcrypt` | S10 | TS-071 @ 141:16 (produced) | - |
| `m.bcrypt-hash` | bcrypt hash string | credential | 480 | derived | - | `bcrypt` | S10 | TS-073 @ 142:16 (produced) | 60-character modular-crypt string ($2a$/$2b$) |
| `m.gcm-key` | AES-256-GCM key | secret-key | 256 | hardcoded | feffe992... | `aes-256-gcm` | S11 | TS-023 @ 45:7 | GCM spec test case 16 |
| `m.gcm-iv` | AES-GCM IV | nonce | 96 | hardcoded | cafebabefacedbaddecaf888 | `aes-256-gcm` | S11 | TS-024 @ 46:7 | Static nonce - reuse with the same key is catastrophic outside a KAT |
| `m.gcm-aad` | AES-GCM additional authenticated data | additional-data | 160 | hardcoded | feedface... | `aes-256-gcm` | S11 | TS-025 @ 47:7 | GCM spec test case 16 |
| `m.chacha-key` | ChaCha20-Poly1305 key | secret-key | 256 | csprng | - | `chacha20-poly1305` | S12 | TS-083 @ 162:15 (produced); TS-084 @ 162:27 | - |
| `m.chacha-nonce` | ChaCha20-Poly1305 nonce | nonce | 96 | csprng | - | `chacha20-poly1305` | S12 | TS-085 @ 163:17 (produced); TS-086 @ 163:29 | - |
| `m.cbc-key` | AES-256-CBC key | secret-key | 256 | csprng | - | `aes-256-cbc` | S13 | TS-091 @ 171:15 (produced); TS-092 @ 171:34 | - |
| `m.cbc-iv` | AES-CBC IV | initialization-vector | 128 | csprng | - | `aes-256-cbc` | S13 | TS-093 @ 172:14 (produced); TS-094 @ 172:33 | - |
| `m.ecb-key` | AES-128-ECB key | secret-key | 128 | hardcoded | 000102...0f | `aes-128-ecb` | S14 | TS-026 @ 53:7 | FIPS 197 appendix C.1 |
| `m.ctr-key` | AES-256-CTR key | secret-key | 256 | csprng | - | `aes-256-ctr` | S15 | TS-104 @ 189:21 (produced) | - |
| `m.ctr-iv` | AES-CTR initial counter block | initialization-vector | 128 | csprng | - | `aes-256-ctr` | S15 | TS-107 @ 190:19 (produced); TS-108 @ 190:68 | - |
| `m.tdes-key` | 3DES key | secret-key | 192 | csprng | - | `3des-cbc` | S16 | TS-113 @ 199:15 (produced); TS-114 @ 199:34 | 192 bits incl. parity = 168 effective |
| `m.tdes-iv` | 3DES IV | initialization-vector | 64 | csprng | - | `3des-cbc` | S16 | TS-115 @ 200:14 (produced); TS-116 @ 200:33 | - |
| `m.rsa-private-key` | RSA-3072 private key | private-key | 3072 | keygen | - | `rsa-3072` | S17 | TS-123 @ 210:37 (produced) | - |
| `m.rsa-public-key` | RSA-3072 public key | public-key | 3072 | keygen | - | `rsa-3072` | S17 | TS-123 @ 210:37 (produced) | e = 65537 |
| `m.ecdsa-private-key` | ECDSA P-256 private key | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | TS-147 @ 250:22 (produced) | - |
| `m.ecdsa-public-key` | ECDSA P-256 public key | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | TS-147 @ 250:22 (produced) | - |
| `m.ed25519-seed` | Ed25519 private key seed | private-key | 256 | hardcoded | 9d61b19d... | `ed25519` | S19 | TS-027 @ 56:7 | RFC 8032 section 7.1 TEST 1 |
| `m.ed25519-public-key` | Ed25519 public key | public-key | 256 | derived | d75a9801... | `ed25519` | S19 | TS-154 @ 259:21 (produced) | Derived from the seed |
| `m.x25519-private-key-a` | X25519 private key (party A) | private-key | 256 | keygen | - | `x25519` | S20 | TS-160 @ 272:17 (produced) | - |
| `m.x25519-private-key-b` | X25519 private key (party B) | private-key | 256 | keygen | - | `x25519` | S20 | TS-162 @ 273:15 (produced) | - |
| `m.x25519-shared-secret` | X25519 shared secret | shared-secret | 256 | agreed | - | `x25519` | S20 | TS-164 @ 274:18 (produced); TS-165 @ 275:16 (produced) | - |
| `m.ecdh-private-key-a` | ECDH P-256 private key (party A) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | TS-170 @ 280:23 (produced) | - |
| `m.ecdh-private-key-b` | ECDH P-256 private key (party B) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | TS-171 @ 281:21 (produced) | - |
| `m.ecdh-shared-secret` | ECDH P-256 shared secret | shared-secret | 256 | agreed | - | `ecdh-p256` | S20 | TS-172 @ 282:18 (produced); TS-173 @ 283:16 (produced) | - |
| `m.session-info` | Session-key HKDF info | additional-data | 208 | hardcoded | "cbom-corpus session key v1" | `hkdf-sha256` | S20 | TS-028 @ 57:7 | - |
| `m.session-key` | Session key (HKDF over X25519 || ECDH secrets) | secret-key | 256 | derived | - | `hkdf-sha256` | S20 | TS-157 @ 266:15 (produced) | - |
| `m.mlkem-decapsulation-key` | ML-KEM-768 decapsulation key | private-key | - | keygen | - | `ml-kem-768` | S21 | TS-174 @ 293:36 (produced) | 64-byte seed form or 2400-byte expanded form, library-dependent |
| `m.mlkem-encapsulation-key` | ML-KEM-768 encapsulation key | public-key | 9472 | keygen | - | `ml-kem-768` | S21 | TS-174 @ 293:36 (produced) | 1184 bytes |
| `m.mlkem-shared-secret` | ML-KEM-768 shared secret | shared-secret | 256 | agreed | - | `ml-kem-768` | S21 | TS-175 @ 294:40 (produced); TS-176 @ 295:21 (produced) | - |
| `m.mldsa-private-key` | ML-DSA-65 private key | private-key | - | keygen | - | `ml-dsa-65` | S22 | TS-177 @ 301:36 (produced) | 32-byte seed or 4032-byte expanded form, library-dependent |
| `m.mldsa-public-key` | ML-DSA-65 public key | public-key | 15616 | keygen | - | `ml-dsa-65` | S22 | TS-177 @ 301:36 (produced) | 1952 bytes |
| `m.cert-private-key` | Certificate private key (P-256) | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | TS-184 @ 311:22 (produced) | - |
| `m.cert-public-key` | Certificate subject public key (P-256) | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | TS-184 @ 311:22 (produced) | - |

## Scenario map

| Scenario | What it does | Output | Occurrences | Lines | Assets |
|---|---|---|---|---|---|
| S01 | SHA-256 digest of MESSAGE | Known answer (Wikipedia / NIST example message) | 3 | 82-82 | `sha-256` |
| S02 | SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | Known answers | 6 | 87-89 | `sha-512`, `sha3-256`, `blake2b-512` |
| S03 | Legacy MD5 and SHA-1 digests of MESSAGE | Known answers; deliberately weak algorithms | 6 | 94-95 | `md5`, `sha-1` |
| S04 | SHAKE128 XOF, 32-byte output | Known answer | 4 | 100-101 | `shake128` |
| S05 | HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | Known answer (Wikipedia HMAC example) | 4 | 32-107 | `sha-256`, `hmac-sha256`, `m.hmac-key` |
| S06 | HKDF-SHA256 extract-and-expand, L=42 | Known answer (RFC 5869 A.1) | 6 | 34-112 | `sha-256`, `hkdf-sha256`, `m.hkdf-ikm`, `m.hkdf-salt`, `m.hkdf-info`, `m.hkdf-okm` |
| S07 | PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | Known answer (RFC 7914 section 11) | 9 | 38-123 | `sha-256`, `pbkdf2-hmac-sha256`, `m.pbkdf2-password`, `m.pbkdf2-salt`, `m.pbkdf2-dk` |
| S08 | scrypt N=16384 r=8 p=1, dkLen=64 | Known answer (RFC 7914 section 12) | 7 | 40-129 | `scrypt`, `m.scrypt-password`, `m.scrypt-salt`, `m.scrypt-dk` |
| S09 | Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | Deterministic; identical across languages | 7 | 42-135 | `argon2id`, `m.password`, `m.argon2-salt`, `m.argon2-dk` |
| S10 | bcrypt cost 12 with random salt, then verify | Randomized; prints verify=true | 4 | 141-143 | `bcrypt`, `csprng`, `m.bcrypt-salt`, `m.bcrypt-hash` |
| S11 | AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | Known answer (GCM spec test case 16) | 11 | 45-156 | `aes-256-gcm`, `m.gcm-key`, `m.gcm-iv`, `m.gcm-aad` |
| S12 | ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | Randomized round trip | 8 | 162-165 | `chacha20-poly1305`, `csprng`, `m.chacha-key`, `m.chacha-nonce` |
| S13 | AES-256-CBC with PKCS#7 padding, random key and IV | Randomized round trip | 10 | 171-176 | `aes-256-cbc`, `csprng`, `m.cbc-key`, `m.cbc-iv` |
| S14 | AES-128-ECB with PKCS#7 padding, hard-coded key | Known answer: first block = FIPS 197 C.1 | 4 | 53-183 | `aes-128-ecb`, `m.ecb-key` |
| S15 | AES-256-CTR, random key and 128-bit initial counter block | Randomized round trip | 9 | 189-193 | `aes-256-ctr`, `csprng`, `m.ctr-key`, `m.ctr-iv` |
| S16 | 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | Randomized round trip | 10 | 199-204 | `3des-cbc`, `csprng`, `m.tdes-key`, `m.tdes-iv` |
| S17 | RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | Randomized | 24 | 210-244 | `sha-256`, `rsa-3072`, `rsa-oaep-sha256`, `rsassa-pss-sha256`, `rsassa-pkcs1v15-sha256`, `m.rsa-private-key`, `m.rsa-public-key` |
| S18 | ECDSA P-256 / SHA-256 sign and verify | Randomized | 7 | 250-253 | `sha-256`, `ecdsa-p256-sha256`, `m.ecdsa-private-key`, `m.ecdsa-public-key` |
| S19 | Ed25519 from a hard-coded seed: public key, signature, verify | Known public key (RFC 8032 test 1); deterministic signature | 4 | 56-261 | `ed25519`, `m.ed25519-seed`, `m.ed25519-public-key` |
| S20 | X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | Randomized; prints agreement booleans | 18 | 57-283 | `sha-256`, `hkdf-sha256`, `ecdh-p256`, `x25519`, `m.x25519-private-key-a`, `m.x25519-private-key-b`, `m.x25519-shared-secret`, `m.ecdh-private-key-a`, `m.ecdh-private-key-b`, `m.ecdh-shared-secret`, `m.session-info`, `m.session-key` |
| S21 | ML-KEM-768 key generation, encapsulation, decapsulation | Randomized; prints sizes | 3 | 293-295 | `ml-kem-768`, `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key`, `m.mlkem-shared-secret` |
| S22 | ML-DSA-65 key generation, signing, verification | Randomized; prints signature size | 3 | 301-303 | `ml-dsa-65`, `m.mldsa-private-key`, `m.mldsa-public-key` |
| S23 | Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | Randomized | 9 | 309-321 | `sha-256`, `ecdsa-p256-sha256`, `csprng`, `cert.self-signed`, `m.cert-private-key`, `m.cert-public-key` |
| S24 | TLS 1.3-only client configuration (no network I/O) | Configuration only | 4 | 327-331 | `tls13-client` |

## Occurrence ledger

Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.

| ID | Scn | Role | Asset (^parent) | Start L:C | End L:C | Chars | Bytes | Len | Nest | Scope | API symbol | Library | Produces | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TS-001 | - | `imp` | `lib.node` | 10:1 | 10:39 | [425, 463) | [425, 463) | 38 | 0 | `<module>` | `node:crypto` | `lib.node` | - | `import * as crypto from "node:crypto";` | - |
| TS-002 | - | `imp` | `lib.node` | 11:1 | 11:33 | [464, 496) | [464, 496) | 32 | 0 | `<module>` | `node:tls` | `lib.node` | - | `import * as tls from "node:tls";` | - |
| TS-003 | - | `imp` | `lib.noble-ciphers` | 12:1 | 12:61 | [497, 557) | [497, 557) | 60 | 0 | `<module>` | `@noble/ciphers/chacha.js` | `lib.noble-ciphers` | - | `import { chacha20poly1305 } from "@noble/ciphers/chacha.js";` | - |
| TS-004 | - | `imp` | `lib.noble-ciphers` | 13:1 | 13:55 | [558, 612) | [558, 612) | 54 | 0 | `<module>` | `@noble/ciphers/utils.js` | `lib.noble-ciphers` | - | `import { randomBytes } from "@noble/ciphers/utils.js";` | - |
| TS-005 | - | `imp` | `lib.noble-curves` | 14:1 | 14:52 | [613, 664) | [613, 664) | 51 | 0 | `<module>` | `@noble/curves/ed25519.js` | `lib.noble-curves` | - | `import { ed25519 } from "@noble/curves/ed25519.js";` | - |
| TS-006 | - | `imp` | `lib.noble-hashes` | 15:1 | 15:52 | [665, 716) | [665, 716) | 51 | 0 | `<module>` | `@noble/hashes/argon2.js` | `lib.noble-hashes` | - | `import { argon2id } from "@noble/hashes/argon2.js";` | - |
| TS-007 | - | `imp` | `lib.noble-hashes` | 16:1 | 16:51 | [717, 767) | [717, 767) | 50 | 0 | `<module>` | `@noble/hashes/blake2.js` | `lib.noble-hashes` | - | `import { blake2b } from "@noble/hashes/blake2.js";` | - |
| TS-008 | - | `imp` | `lib.noble-hashes` | 17:1 | 17:50 | [768, 817) | [768, 817) | 49 | 0 | `<module>` | `@noble/hashes/sha3.js` | `lib.noble-hashes` | - | `import { sha3_256 } from "@noble/hashes/sha3.js";` | - |
| TS-009 | - | `imp` | `lib.noble-pq` | 18:1 | 18:58 | [818, 875) | [818, 875) | 57 | 0 | `<module>` | `@noble/post-quantum/ml-dsa.js` | `lib.noble-pq` | - | `import { ml_dsa65 } from "@noble/post-quantum/ml-dsa.js";` | - |
| TS-010 | - | `imp` | `lib.noble-pq` | 19:1 | 19:59 | [876, 934) | [876, 934) | 58 | 0 | `<module>` | `@noble/post-quantum/ml-kem.js` | `lib.noble-pq` | - | `import { ml_kem768 } from "@noble/post-quantum/ml-kem.js";` | - |
| TS-011 | - | `imp` | `lib.peculiar-x509` | 20:1 | 20:40 | [935, 974) | [935, 974) | 39 | 0 | `<module>` | `@peculiar/x509` | `lib.peculiar-x509` | - | `import * as x509 from "@peculiar/x509";` | - |
| TS-012 | - | `imp` | `lib.bcryptjs` | 21:1 | 21:31 | [975, 1005) | [975, 1005) | 30 | 0 | `<module>` | `bcryptjs` | `lib.bcryptjs` | - | `import bcrypt from "bcryptjs";` | - |
| TS-013 | S05 | `mat` | `m.hmac-key` | 32:7 | 32:29 | [1339, 1361) | [1339, 1361) | 22 | 0 | `<module>` | - | `lib.node` | - | `HMAC_KEY = utf8("key")` | - |
| TS-014 | S06 | `mat` | `m.hkdf-ikm` | 34:7 | 34:47 | [1385, 1425) | [1385, 1425) | 40 | 0 | `<module>` | - | `lib.node` | - | `HKDF_IKM = new Uint8Array(22).fill(0x0b)` | - |
| TS-015 | S06 | `mat` | `m.hkdf-salt` | 35:7 | 35:56 | [1433, 1482) | [1433, 1482) | 49 | 0 | `<module>` | - | `lib.node` | - | `HKDF_SALT = fromHex("000102030405060708090a0b0c")` | - |
| TS-016 | S06 | `mat` | `m.hkdf-info` | 36:7 | 36:50 | [1490, 1533) | [1490, 1533) | 43 | 0 | `<module>` | - | `lib.node` | - | `HKDF_INFO = fromHex("f0f1f2f3f4f5f6f7f8f9")` | - |
| TS-017 | S07 | `mat` | `m.pbkdf2-password` | 38:7 | 38:41 | [1572, 1606) | [1572, 1606) | 34 | 0 | `<module>` | - | `lib.node` | - | `PBKDF2_PASSWORD = utf8("Password")` | - |
| TS-018 | S07 | `mat` | `m.pbkdf2-salt` | 39:7 | 39:33 | [1614, 1640) | [1614, 1640) | 26 | 0 | `<module>` | - | `lib.node` | - | `PBKDF2_SALT = utf8("NaCl")` | - |
| TS-019 | S08 | `mat` | `m.scrypt-password` | 40:7 | 40:46 | [1648, 1687) | [1648, 1687) | 39 | 0 | `<module>` | - | `lib.node` | - | `SCRYPT_PASSWORD = utf8("pleaseletmein")` | - |
| TS-020 | S08 | `mat` | `m.scrypt-salt` | 41:7 | 41:43 | [1695, 1731) | [1695, 1731) | 36 | 0 | `<module>` | - | `lib.node` | - | `SCRYPT_SALT = utf8("SodiumChloride")` | - |
| TS-021 | S09 | `mat` | `m.password` | 42:7 | 42:48 | [1739, 1780) | [1739, 1780) | 41 | 0 | `<module>` | - | `lib.node` | - | `PASSWORD = "correct horse battery staple"` | - |
| TS-022 | S09 | `mat` | `m.argon2-salt` | 43:7 | 43:45 | [1788, 1826) | [1788, 1826) | 38 | 0 | `<module>` | - | `lib.node` | - | `ARGON2_SALT = utf8("cbom-corpus-salt")` | - |
| TS-023 | S11 | `mat` | `m.gcm-key` | 45:7 | 45:92 | [1868, 1953) | [1868, 1953) | 85 | 0 | `<module>` | - | `lib.node` | - | `GCM_KEY = fromHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")` | - |
| TS-024 | S11 | `mat` | `m.gcm-iv` | 46:7 | 46:51 | [1961, 2005) | [1961, 2005) | 44 | 0 | `<module>` | - | `lib.node` | - | `GCM_IV = fromHex("cafebabefacedbaddecaf888")` | - |
| TS-025 | S11 | `mat` | `m.gcm-aad` | 47:7 | 47:68 | [2013, 2074) | [2013, 2074) | 61 | 0 | `<module>` | - | `lib.node` | - | `GCM_AAD = fromHex("feedfacedeadbeeffeedfacedeadbeefabaddad2")` | - |
| TS-026 | S14 | `mat` | `m.ecb-key` | 53:7 | 53:60 | [2276, 2329) | [2276, 2329) | 53 | 0 | `<module>` | - | `lib.node` | - | `ECB_KEY = fromHex("000102030405060708090a0b0c0d0e0f")` | - |
| TS-027 | S19 | `mat` | `m.ed25519-seed` | 56:7 | 56:97 | [2436, 2526) | [2436, 2526) | 90 | 0 | `<module>` | - | `lib.node` | - | `ED25519_SEED = fromHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")` | - |
| TS-028 | S20 | `mat` | `m.session-info` | 57:7 | 57:56 | [2534, 2583) | [2534, 2583) | 49 | 0 | `<module>` | - | `lib.node` | - | `SESSION_INFO = utf8("cbom-corpus session key v1")` | - |
| TS-029 | S01 | `op:digest` | `sha-256` | 82:26 | 82:83 | [3367, 3424) | [3367, 3424) | 57 | 0 | `s01Sha256` | `node:crypto.Hash.digest` | `lib.node` | - | `crypto.createHash("sha256").update(MESSAGE).digest("hex")` | - |
| TS-030 | S01 | `ctor` | `sha-256` | 82:26 | 82:53 | [3367, 3394) | [3367, 3394) | 27 | 1 | `s01Sha256` | `node:crypto.createHash` | `lib.node` | - | `crypto.createHash("sha256")` | - |
| TS-031 | S01 | `alg` | `sha-256` | 82:44 | 82:52 | [3385, 3393) | [3385, 3393) | 8 | 2 | `s01Sha256` | - | `lib.node` | - | `"sha256"` | - |
| TS-032 | S02 | `op:digest` | `sha-512` | 87:26 | 87:83 | [3531, 3588) | [3531, 3588) | 57 | 0 | `s02Sha2Sha3Blake2` | `node:crypto.Hash.digest` | `lib.node` | - | `crypto.createHash("sha512").update(MESSAGE).digest("hex")` | - |
| TS-033 | S02 | `ctor` | `sha-512` | 87:26 | 87:53 | [3531, 3558) | [3531, 3558) | 27 | 1 | `s02Sha2Sha3Blake2` | `node:crypto.createHash` | `lib.node` | - | `crypto.createHash("sha512")` | - |
| TS-034 | S02 | `alg` | `sha-512` | 87:44 | 87:52 | [3549, 3557) | [3549, 3557) | 8 | 2 | `s02Sha2Sha3Blake2` | - | `lib.node` | - | `"sha512"` | - |
| TS-035 | S02 | `op:digest` | `sha3-256` | 88:33 | 88:50 | [3623, 3640) | [3623, 3640) | 17 | 0 | `s02Sha2Sha3Blake2` | `@noble/hashes/sha3.js:sha3_256` | `lib.noble-hashes` | - | `sha3_256(MESSAGE)` | - |
| TS-036 | S02 | `op:digest` | `blake2b-512` | 89:36 | 89:67 | [3679, 3710) | [3679, 3710) | 31 | 0 | `s02Sha2Sha3Blake2` | `@noble/hashes/blake2.js:blake2b` | `lib.noble-hashes` | - | `blake2b(MESSAGE, { dkLen: 64 })` | - |
| TS-037 | S02 | `prm:output-length-bytes` | `blake2b-512` | 89:62 | 89:64 | [3705, 3707) | [3705, 3707) | 2 | 1 | `s02Sha2Sha3Blake2` | - | `lib.noble-hashes` | - | `64` | - |
| TS-038 | S03 | `op:digest` | `md5` | 94:22 | 94:76 | [3816, 3870) | [3816, 3870) | 54 | 0 | `s03LegacyHashes` | `node:crypto.Hash.digest` | `lib.node` | - | `crypto.createHash("md5").update(MESSAGE).digest("hex")` | - |
| TS-039 | S03 | `ctor` | `md5` | 94:22 | 94:46 | [3816, 3840) | [3816, 3840) | 24 | 1 | `s03LegacyHashes` | `node:crypto.createHash` | `lib.node` | - | `crypto.createHash("md5")` | - |
| TS-040 | S03 | `alg` | `md5` | 94:40 | 94:45 | [3834, 3839) | [3834, 3839) | 5 | 2 | `s03LegacyHashes` | - | `lib.node` | - | `"md5"` | - |
| TS-041 | S03 | `op:digest` | `sha-1` | 95:24 | 95:79 | [3896, 3951) | [3896, 3951) | 55 | 0 | `s03LegacyHashes` | `node:crypto.Hash.digest` | `lib.node` | - | `crypto.createHash("sha1").update(MESSAGE).digest("hex")` | - |
| TS-042 | S03 | `ctor` | `sha-1` | 95:24 | 95:49 | [3896, 3921) | [3896, 3921) | 25 | 1 | `s03LegacyHashes` | `node:crypto.createHash` | `lib.node` | - | `crypto.createHash("sha1")` | - |
| TS-043 | S03 | `alg` | `sha-1` | 95:42 | 95:48 | [3914, 3920) | [3914, 3920) | 6 | 2 | `s03LegacyHashes` | - | `lib.node` | - | `"sha1"` | - |
| TS-044 | S04 | `ctor` | `shake128` | 100:15 | 100:66 | [4046, 4097) | [4046, 4097) | 51 | 0 | `s04Shake128` | `node:crypto.createHash` | `lib.node` | - | `crypto.createHash("shake128", { outputLength: 32 })` | - |
| TS-045 | S04 | `alg` | `shake128` | 100:33 | 100:43 | [4064, 4074) | [4064, 4074) | 10 | 1 | `s04Shake128` | - | `lib.node` | - | `"shake128"` | - |
| TS-046 | S04 | `prm:output-length-bytes` | `shake128` | 100:61 | 100:63 | [4092, 4094) | [4092, 4094) | 2 | 1 | `s04Shake128` | - | `lib.node` | - | `32` | - |
| TS-047 | S04 | `op:digest` | `shake128` | 101:27 | 101:60 | [4125, 4158) | [4125, 4158) | 33 | 0 | `s04Shake128` | `node:crypto.Hash.digest` | `lib.node` | - | `xof.update(MESSAGE).digest("hex")` | - |
| TS-048 | S05 | `ctor` | `hmac-sha256` | 106:15 | 106:52 | [4231, 4268) | [4231, 4268) | 37 | 0 | `s05HmacSha256` | `node:crypto.createHmac` | `lib.node` | - | `crypto.createHmac("sha256", HMAC_KEY)` | - |
| TS-049 | S05 | `alg` | `sha-256` ^`hmac-sha256` | 106:33 | 106:41 | [4249, 4257) | [4249, 4257) | 8 | 1 | `s05HmacSha256` | - | `lib.node` | - | `"sha256"` | - |
| TS-050 | S05 | `op:tag` | `hmac-sha256` | 107:30 | 107:63 | [4299, 4332) | [4299, 4332) | 33 | 0 | `s05HmacSha256` | `node:crypto.Hmac.digest` | `lib.node` | - | `mac.update(MESSAGE).digest("hex")` | - |
| TS-051 | S06 | `op:keyderive` | `hkdf-sha256` | 112:15 | 112:76 | [4416, 4477) | [4416, 4477) | 61 | 0 | `s06HkdfSha256` | `node:crypto.hkdfSync` | `lib.node` | `m.hkdf-okm` | `crypto.hkdfSync("sha256", HKDF_IKM, HKDF_SALT, HKDF_INFO, 42)` | - |
| TS-052 | S06 | `alg` | `sha-256` ^`hkdf-sha256` | 112:31 | 112:39 | [4432, 4440) | [4432, 4440) | 8 | 1 | `s06HkdfSha256` | - | `lib.node` | - | `"sha256"` | - |
| TS-053 | S06 | `prm:output-length-bytes` | `hkdf-sha256` | 112:73 | 112:75 | [4474, 4476) | [4474, 4476) | 2 | 1 | `s06HkdfSha256` | - | `lib.node` | - | `42` | - |
| TS-054 | S07 | `ctor` | `pbkdf2-hmac-sha256` | 118:25 | 118:98 | [4637, 4710) | [4637, 4710) | 73 | 0 | `s07Pbkdf2` | `globalThis.crypto.subtle.importKey` | `lib.node` | - | `subtle.importKey("raw", PBKDF2_PASSWORD, "PBKDF2", false, ["deriveBits"])` | - |
| TS-055 | S07 | `alg` | `pbkdf2-hmac-sha256` | 118:66 | 118:74 | [4678, 4686) | [4678, 4686) | 8 | 1 | `s07Pbkdf2` | - | `lib.node` | - | `"PBKDF2"` | - |
| TS-056 | S07 | `op:keyderive` | `pbkdf2-hmac-sha256` | 119:22 | 123:4 | [4733, 4857) | [4733, 4857) | 124 | 0 | `s07Pbkdf2` | `globalThis.crypto.subtle.deriveBits` | `lib.node` | `m.pbkdf2-dk` | `subtle.deriveBits( … (+4 lines)` | - |
| TS-057 | S07 | `alg` | `pbkdf2-hmac-sha256` | 120:13 | 120:21 | [4764, 4772) | [4764, 4772) | 8 | 1 | `s07Pbkdf2` | - | `lib.node` | - | `"PBKDF2"` | - |
| TS-058 | S07 | `alg` | `sha-256` ^`pbkdf2-hmac-sha256` | 120:29 | 120:38 | [4780, 4789) | [4780, 4789) | 9 | 1 | `s07Pbkdf2` | - | `lib.node` | - | `"SHA-256"` | - |
| TS-059 | S07 | `prm:iterations` | `pbkdf2-hmac-sha256` | 120:71 | 120:77 | [4822, 4828) | [4822, 4828) | 6 | 1 | `s07Pbkdf2` | - | `lib.node` | - | `80_000` | - |
| TS-060 | S07 | `prm:output-length-bits` | `pbkdf2-hmac-sha256` | 122:5 | 122:8 | [4849, 4852) | [4849, 4852) | 3 | 1 | `s07Pbkdf2` | - | `lib.node` | - | `512` | - |
| TS-061 | S08 | `op:keyderive` | `scrypt` | 129:19 | 129:98 | [4969, 5048) | [4969, 5048) | 79 | 0 | `s08Scrypt` | `node:crypto.scryptSync` | `lib.node` | `m.scrypt-dk` | `crypto.scryptSync(SCRYPT_PASSWORD, SCRYPT_SALT, 64, { N: 2 ** 14, r: 8, p: 1 })` | - |
| TS-062 | S08 | `prm:output-length-bytes` | `scrypt` | 129:67 | 129:69 | [5017, 5019) | [5017, 5019) | 2 | 1 | `s08Scrypt` | - | `lib.node` | - | `64` | - |
| TS-063 | S08 | `prm:N` | `scrypt` | 129:76 | 129:83 | [5026, 5033) | [5026, 5033) | 7 | 1 | `s08Scrypt` | - | `lib.node` | - | `2 ** 14` | computed |
| TS-064 | S08 | `prm:r` | `scrypt` | 129:88 | 129:89 | [5038, 5039) | [5038, 5039) | 1 | 1 | `s08Scrypt` | - | `lib.node` | - | `8` | - |
| TS-065 | S08 | `prm:p` | `scrypt` | 129:94 | 129:95 | [5044, 5045) | [5044, 5045) | 1 | 1 | `s08Scrypt` | - | `lib.node` | - | `1` | - |
| TS-066 | S09 | `op:keyderive` | `argon2id` | 135:15 | 135:90 | [5156, 5231) | [5156, 5231) | 75 | 0 | `s09Argon2id` | `@noble/hashes/argon2.js:argon2id` | `lib.noble-hashes` | `m.argon2-dk` | `argon2id(utf8(PASSWORD), ARGON2_SALT, { t: 2, m: 19_456, p: 1, dkLen: 32 })` | - |
| TS-067 | S09 | `prm:iterations` | `argon2id` | 135:58 | 135:59 | [5199, 5200) | [5199, 5200) | 1 | 1 | `s09Argon2id` | - | `lib.noble-hashes` | - | `2` | - |
| TS-068 | S09 | `prm:memory-kib` | `argon2id` | 135:64 | 135:70 | [5205, 5211) | [5205, 5211) | 6 | 1 | `s09Argon2id` | - | `lib.noble-hashes` | - | `19_456` | - |
| TS-069 | S09 | `prm:parallelism` | `argon2id` | 135:75 | 135:76 | [5216, 5217) | [5216, 5217) | 1 | 1 | `s09Argon2id` | - | `lib.noble-hashes` | - | `1` | - |
| TS-070 | S09 | `prm:output-length-bytes` | `argon2id` | 135:85 | 135:87 | [5226, 5228) | [5226, 5228) | 2 | 1 | `s09Argon2id` | - | `lib.noble-hashes` | - | `32` | - |
| TS-071 | S10 | `op:generate` | `csprng` | 141:16 | 141:38 | [5334, 5356) | [5334, 5356) | 22 | 0 | `s10Bcrypt` | `bcryptjs.genSaltSync` | `lib.bcryptjs` | `m.bcrypt-salt` | `bcrypt.genSaltSync(12)` | - |
| TS-072 | S10 | `prm:cost` | `bcrypt` | 141:35 | 141:37 | [5353, 5355) | [5353, 5355) | 2 | 1 | `s10Bcrypt` | - | `lib.bcryptjs` | - | `12` | - |
| TS-073 | S10 | `op:keyderive` | `bcrypt` | 142:16 | 142:47 | [5373, 5404) | [5373, 5404) | 31 | 0 | `s10Bcrypt` | `bcryptjs.hashSync` | `lib.bcryptjs` | `m.bcrypt-hash` | `bcrypt.hashSync(PASSWORD, salt)` | - |
| TS-074 | S10 | `op:verify` | `bcrypt` | 143:14 | 143:48 | [5419, 5453) | [5419, 5453) | 34 | 0 | `s10Bcrypt` | `bcryptjs.compareSync` | `lib.bcryptjs` | - | `bcrypt.compareSync(PASSWORD, hash)` | - |
| TS-075 | S11 | `ctor` | `aes-256-gcm` | 149:21 | 149:97 | [5589, 5665) | [5589, 5665) | 76 | 0 | `s11Aes256Gcm` | `node:crypto.createCipheriv` | `lib.node` | - | `crypto.createCipheriv("aes-256-gcm", GCM_KEY, GCM_IV, { authTagLength: 16 })` | keysize-from-key |
| TS-076 | S11 | `alg` | `aes-256-gcm` | 149:43 | 149:56 | [5611, 5624) | [5611, 5624) | 13 | 1 | `s11Aes256Gcm` | - | `lib.node` | - | `"aes-256-gcm"` | - |
| TS-077 | S11 | `prm:tag-length-bytes` | `aes-256-gcm` | 149:92 | 149:94 | [5660, 5662) | [5660, 5662) | 2 | 1 | `s11Aes256Gcm` | - | `lib.node` | - | `16` | - |
| TS-078 | S11 | `op:encrypt` | `aes-256-gcm` | 151:22 | 151:89 | [5717, 5784) | [5717, 5784) | 67 | 0 | `s11Aes256Gcm` | `node:crypto.Cipheriv.final` | `lib.node` | - | `Buffer.concat([encryptor.update(GCM_PLAINTEXT), encryptor.final()])` | - |
| TS-079 | S11 | `ctor` | `aes-256-gcm` | 153:21 | 153:99 | [5844, 5922) | [5844, 5922) | 78 | 0 | `s11Aes256Gcm` | `node:crypto.createDecipheriv` | `lib.node` | - | `crypto.createDecipheriv("aes-256-gcm", GCM_KEY, GCM_IV, { authTagLength: 16 })` | - |
| TS-080 | S11 | `alg` | `aes-256-gcm` | 153:45 | 153:58 | [5868, 5881) | [5868, 5881) | 13 | 1 | `s11Aes256Gcm` | - | `lib.node` | - | `"aes-256-gcm"` | - |
| TS-081 | S11 | `prm:tag-length-bytes` | `aes-256-gcm` | 153:94 | 153:96 | [5917, 5919) | [5917, 5919) | 2 | 1 | `s11Aes256Gcm` | - | `lib.node` | - | `16` | - |
| TS-082 | S11 | `op:decrypt` | `aes-256-gcm` | 156:21 | 156:85 | [6002, 6066) | [6002, 6066) | 64 | 0 | `s11Aes256Gcm` | `node:crypto.Decipheriv.final` | `lib.node` | - | `Buffer.concat([decryptor.update(ciphertext), decryptor.final()])` | - |
| TS-083 | S12 | `op:generate` | `csprng` | 162:15 | 162:30 | [6281, 6296) | [6281, 6296) | 15 | 0 | `s12ChaCha20Poly1305` | `@noble/ciphers/utils.js:randomBytes` | `lib.noble-ciphers` | `m.chacha-key` | `randomBytes(32)` | - |
| TS-084 | S12 | `prm:length-bytes` | `m.chacha-key` | 162:27 | 162:29 | [6293, 6295) | [6293, 6295) | 2 | 1 | `s12ChaCha20Poly1305` | - | `lib.noble-ciphers` | - | `32` | - |
| TS-085 | S12 | `op:generate` | `csprng` | 163:17 | 163:32 | [6314, 6329) | [6314, 6329) | 15 | 0 | `s12ChaCha20Poly1305` | `@noble/ciphers/utils.js:randomBytes` | `lib.noble-ciphers` | `m.chacha-nonce` | `randomBytes(12)` | - |
| TS-086 | S12 | `prm:length-bytes` | `m.chacha-nonce` | 163:29 | 163:31 | [6326, 6328) | [6326, 6328) | 2 | 1 | `s12ChaCha20Poly1305` | - | `lib.noble-ciphers` | - | `12` | - |
| TS-087 | S12 | `op:encrypt` | `chacha20-poly1305` | 164:18 | 164:63 | [6348, 6393) | [6348, 6393) | 45 | 0 | `s12ChaCha20Poly1305` | `@noble/ciphers/chacha.js:chacha20poly1305.encrypt` | `lib.noble-ciphers` | - | `chacha20poly1305(key, nonce).encrypt(MESSAGE)` | - |
| TS-088 | S12 | `ctor` | `chacha20-poly1305` | 164:18 | 164:46 | [6348, 6376) | [6348, 6376) | 28 | 1 | `s12ChaCha20Poly1305` | `@noble/ciphers/chacha.js:chacha20poly1305` | `lib.noble-ciphers` | - | `chacha20poly1305(key, nonce)` | - |
| TS-089 | S12 | `op:decrypt` | `chacha20-poly1305` | 165:18 | 165:62 | [6412, 6456) | [6412, 6456) | 44 | 0 | `s12ChaCha20Poly1305` | `@noble/ciphers/chacha.js:chacha20poly1305.decrypt` | `lib.noble-ciphers` | - | `chacha20poly1305(key, nonce).decrypt(sealed)` | - |
| TS-090 | S12 | `ctor` | `chacha20-poly1305` | 165:18 | 165:46 | [6412, 6440) | [6412, 6440) | 28 | 1 | `s12ChaCha20Poly1305` | `@noble/ciphers/chacha.js:chacha20poly1305` | `lib.noble-ciphers` | - | `chacha20poly1305(key, nonce)` | - |
| TS-091 | S13 | `op:generate` | `csprng` | 171:15 | 171:37 | [6622, 6644) | [6622, 6644) | 22 | 0 | `s13Aes256Cbc` | `node:crypto.randomBytes` | `lib.node` | `m.cbc-key` | `crypto.randomBytes(32)` | - |
| TS-092 | S13 | `prm:length-bytes` | `m.cbc-key` | 171:34 | 171:36 | [6641, 6643) | [6641, 6643) | 2 | 1 | `s13Aes256Cbc` | - | `lib.node` | - | `32` | - |
| TS-093 | S13 | `op:generate` | `csprng` | 172:14 | 172:36 | [6659, 6681) | [6659, 6681) | 22 | 0 | `s13Aes256Cbc` | `node:crypto.randomBytes` | `lib.node` | `m.cbc-iv` | `crypto.randomBytes(16)` | - |
| TS-094 | S13 | `prm:length-bytes` | `m.cbc-iv` | 172:33 | 172:35 | [6678, 6680) | [6678, 6680) | 2 | 1 | `s13Aes256Cbc` | - | `lib.node` | - | `16` | - |
| TS-095 | S13 | `ctor` | `aes-256-cbc` | 173:21 | 173:66 | [6703, 6748) | [6703, 6748) | 45 | 0 | `s13Aes256Cbc` | `node:crypto.createCipheriv` | `lib.node` | - | `crypto.createCipheriv("aes-256-cbc", key, iv)` | openssl-default-padding |
| TS-096 | S13 | `alg` | `aes-256-cbc` | 173:43 | 173:56 | [6725, 6738) | [6725, 6738) | 13 | 1 | `s13Aes256Cbc` | - | `lib.node` | - | `"aes-256-cbc"` | - |
| TS-097 | S13 | `op:encrypt` | `aes-256-cbc` | 174:22 | 174:83 | [6771, 6832) | [6771, 6832) | 61 | 0 | `s13Aes256Cbc` | `node:crypto.Cipheriv.final` | `lib.node` | - | `Buffer.concat([encryptor.update(MESSAGE), encryptor.final()])` | - |
| TS-098 | S13 | `ctor` | `aes-256-cbc` | 175:21 | 175:68 | [6854, 6901) | [6854, 6901) | 47 | 0 | `s13Aes256Cbc` | `node:crypto.createDecipheriv` | `lib.node` | - | `crypto.createDecipheriv("aes-256-cbc", key, iv)` | openssl-default-padding |
| TS-099 | S13 | `alg` | `aes-256-cbc` | 175:45 | 175:58 | [6878, 6891) | [6878, 6891) | 13 | 1 | `s13Aes256Cbc` | - | `lib.node` | - | `"aes-256-cbc"` | - |
| TS-100 | S13 | `op:decrypt` | `aes-256-cbc` | 176:21 | 176:85 | [6923, 6987) | [6923, 6987) | 64 | 0 | `s13Aes256Cbc` | `node:crypto.Decipheriv.final` | `lib.node` | - | `Buffer.concat([decryptor.update(ciphertext), decryptor.final()])` | - |
| TS-101 | S14 | `ctor` | `aes-128-ecb` | 182:21 | 182:72 | [7179, 7230) | [7179, 7230) | 51 | 0 | `s14Aes128Ecb` | `node:crypto.createCipheriv` | `lib.node` | - | `crypto.createCipheriv("aes-128-ecb", ECB_KEY, null)` | openssl-default-padding |
| TS-102 | S14 | `alg` | `aes-128-ecb` | 182:43 | 182:56 | [7201, 7214) | [7201, 7214) | 13 | 1 | `s14Aes128Ecb` | - | `lib.node` | - | `"aes-128-ecb"` | - |
| TS-103 | S14 | `op:encrypt` | `aes-128-ecb` | 183:22 | 183:89 | [7253, 7320) | [7253, 7320) | 67 | 0 | `s14Aes128Ecb` | `node:crypto.Cipheriv.final` | `lib.node` | - | `Buffer.concat([encryptor.update(ECB_PLAINTEXT), encryptor.final()])` | - |
| TS-104 | S15 | `op:keygen` | `aes-256-ctr` | 189:21 | 189:104 | [7479, 7562) | [7479, 7562) | 83 | 0 | `s15Aes256Ctr` | `globalThis.crypto.subtle.generateKey` | `lib.node` | `m.ctr-key` | `subtle.generateKey({ name: "AES-CTR", length: 256 }, false, ["encrypt", "decrypt"])` | - |
| TS-105 | S15 | `alg` | `aes-256-ctr` | 189:48 | 189:57 | [7506, 7515) | [7506, 7515) | 9 | 1 | `s15Aes256Ctr` | - | `lib.node` | - | `"AES-CTR"` | - |
| TS-106 | S15 | `prm:key-size-bits` | `aes-256-ctr` | 189:67 | 189:70 | [7525, 7528) | [7525, 7528) | 3 | 1 | `s15Aes256Ctr` | - | `lib.node` | - | `256` | - |
| TS-107 | S15 | `op:generate` | `csprng` | 190:19 | 190:72 | [7582, 7635) | [7582, 7635) | 53 | 0 | `s15Aes256Ctr` | `globalThis.crypto.getRandomValues` | `lib.node` | `m.ctr-iv` | `globalThis.crypto.getRandomValues(new Uint8Array(16))` | - |
| TS-108 | S15 | `prm:length-bytes` | `m.ctr-iv` | 190:68 | 190:70 | [7631, 7633) | [7631, 7633) | 2 | 1 | `s15Aes256Ctr` | - | `lib.node` | - | `16` | - |
| TS-109 | S15 | `alg` | `aes-256-ctr` | 191:26 | 191:35 | [7662, 7671) | [7662, 7671) | 9 | 0 | `s15Aes256Ctr` | - | `lib.node` | - | `"AES-CTR"` | - |
| TS-110 | S15 | `prm:counter-bits` | `aes-256-ctr` | 191:54 | 191:57 | [7690, 7693) | [7690, 7693) | 3 | 0 | `s15Aes256Ctr` | - | `lib.node` | - | `128` | - |
| TS-111 | S15 | `op:encrypt` | `aes-256-ctr` | 192:28 | 192:64 | [7724, 7760) | [7724, 7760) | 36 | 0 | `s15Aes256Ctr` | `globalThis.crypto.subtle.encrypt` | `lib.node` | - | `subtle.encrypt(params, key, MESSAGE)` | - |
| TS-112 | S15 | `op:decrypt` | `aes-256-ctr` | 193:27 | 193:66 | [7788, 7827) | [7788, 7827) | 39 | 0 | `s15Aes256Ctr` | `globalThis.crypto.subtle.decrypt` | `lib.node` | - | `subtle.decrypt(params, key, ciphertext)` | - |
| TS-113 | S16 | `op:generate` | `csprng` | 199:15 | 199:37 | [7994, 8016) | [7994, 8016) | 22 | 0 | `s16TdeaCbc` | `node:crypto.randomBytes` | `lib.node` | `m.tdes-key` | `crypto.randomBytes(24)` | - |
| TS-114 | S16 | `prm:length-bytes` | `m.tdes-key` | 199:34 | 199:36 | [8013, 8015) | [8013, 8015) | 2 | 1 | `s16TdeaCbc` | - | `lib.node` | - | `24` | - |
| TS-115 | S16 | `op:generate` | `csprng` | 200:14 | 200:35 | [8031, 8052) | [8031, 8052) | 21 | 0 | `s16TdeaCbc` | `node:crypto.randomBytes` | `lib.node` | `m.tdes-iv` | `crypto.randomBytes(8)` | - |
| TS-116 | S16 | `prm:length-bytes` | `m.tdes-iv` | 200:33 | 200:34 | [8050, 8051) | [8050, 8051) | 1 | 1 | `s16TdeaCbc` | - | `lib.node` | - | `8` | - |
| TS-117 | S16 | `ctor` | `3des-cbc` | 201:21 | 201:67 | [8074, 8120) | [8074, 8120) | 46 | 0 | `s16TdeaCbc` | `node:crypto.createCipheriv` | `lib.node` | - | `crypto.createCipheriv("des-ede3-cbc", key, iv)` | openssl-default-padding |
| TS-118 | S16 | `alg` | `3des-cbc` | 201:43 | 201:57 | [8096, 8110) | [8096, 8110) | 14 | 1 | `s16TdeaCbc` | - | `lib.node` | - | `"des-ede3-cbc"` | - |
| TS-119 | S16 | `op:encrypt` | `3des-cbc` | 202:22 | 202:83 | [8143, 8204) | [8143, 8204) | 61 | 0 | `s16TdeaCbc` | `node:crypto.Cipheriv.final` | `lib.node` | - | `Buffer.concat([encryptor.update(MESSAGE), encryptor.final()])` | - |
| TS-120 | S16 | `ctor` | `3des-cbc` | 203:21 | 203:69 | [8226, 8274) | [8226, 8274) | 48 | 0 | `s16TdeaCbc` | `node:crypto.createDecipheriv` | `lib.node` | - | `crypto.createDecipheriv("des-ede3-cbc", key, iv)` | openssl-default-padding |
| TS-121 | S16 | `alg` | `3des-cbc` | 203:45 | 203:59 | [8250, 8264) | [8250, 8264) | 14 | 1 | `s16TdeaCbc` | - | `lib.node` | - | `"des-ede3-cbc"` | - |
| TS-122 | S16 | `op:decrypt` | `3des-cbc` | 204:21 | 204:85 | [8296, 8360) | [8296, 8360) | 64 | 0 | `s16TdeaCbc` | `node:crypto.Decipheriv.final` | `lib.node` | - | `Buffer.concat([decryptor.update(ciphertext), decryptor.final()])` | - |
| TS-123 | S17 | `op:keygen` | `rsa-3072` | 210:37 | 210:120 | [8563, 8646) | [8563, 8646) | 83 | 0 | `s17Rsa3072` | `node:crypto.generateKeyPairSync` | `lib.node` | `m.rsa-private-key`, `m.rsa-public-key` | `crypto.generateKeyPairSync("rsa", { modulusLength: 3072, publicExponent: 0x10001 })` | - |
| TS-124 | S17 | `alg` | `rsa-3072` | 210:64 | 210:69 | [8590, 8595) | [8590, 8595) | 5 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"rsa"` | - |
| TS-125 | S17 | `prm:key-size-bits` | `rsa-3072` | 210:88 | 210:92 | [8614, 8618) | [8614, 8618) | 4 | 1 | `s17Rsa3072` | - | `lib.node` | - | `3072` | - |
| TS-126 | S17 | `prm:public-exponent` | `rsa-3072` | 210:110 | 210:117 | [8636, 8643) | [8636, 8643) | 7 | 1 | `s17Rsa3072` | - | `lib.node` | - | `0x10001` | - |
| TS-127 | S17 | `op:encrypt` | `rsa-oaep-sha256` | 212:22 | 215:4 | [8670, 8802) | [8670, 8802) | 132 | 0 | `s17Rsa3072` | `node:crypto.publicEncrypt` | `lib.node` | - | `crypto.publicEncrypt( … (+3 lines)` | - |
| TS-128 | S17 | `alg` | `rsa-oaep-sha256` | 213:32 | 213:71 | [8723, 8762) | [8723, 8762) | 39 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_OAEP_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_OAEP_PADDING` | - |
| TS-129 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 213:83 | 213:91 | [8774, 8782) | [8774, 8782) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | oaep-mgf-same-hash |
| TS-130 | S17 | `op:decrypt` | `rsa-oaep-sha256` | 216:21 | 219:4 | [8824, 8961) | [8824, 8961) | 137 | 0 | `s17Rsa3072` | `node:crypto.privateDecrypt` | `lib.node` | - | `crypto.privateDecrypt( … (+3 lines)` | - |
| TS-131 | S17 | `alg` | `rsa-oaep-sha256` | 217:33 | 217:72 | [8879, 8918) | [8879, 8918) | 39 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_OAEP_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_OAEP_PADDING` | - |
| TS-132 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 217:84 | 217:92 | [8930, 8938) | [8930, 8938) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | oaep-mgf-same-hash |
| TS-133 | S17 | `op:sign` | `rsassa-pss-sha256` | 222:24 | 226:5 | [9061, 9192) | [9061, 9192) | 131 | 0 | `s17Rsa3072` | `node:crypto.sign` | `lib.node` | - | `crypto.sign("sha256", MESSAGE, { … (+4 lines)` | - |
| TS-134 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 222:36 | 222:44 | [9073, 9081) | [9073, 9081) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | - |
| TS-135 | S17 | `alg` | `rsassa-pss-sha256` | 224:14 | 224:52 | [9128, 9166) | [9128, 9166) | 38 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_PSS_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_PSS_PADDING` | - |
| TS-136 | S17 | `prm:salt-length-bytes` | `rsassa-pss-sha256` | 225:17 | 225:19 | [9184, 9186) | [9184, 9186) | 2 | 1 | `s17Rsa3072` | - | `lib.node` | - | `32` | - |
| TS-137 | S17 | `op:verify` | `rsassa-pss-sha256` | 227:17 | 232:4 | [9210, 9362) | [9210, 9362) | 152 | 0 | `s17Rsa3072` | `node:crypto.verify` | `lib.node` | - | `crypto.verify( … (+5 lines)` | - |
| TS-138 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 228:5 | 228:13 | [9229, 9237) | [9229, 9237) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | - |
| TS-139 | S17 | `alg` | `rsassa-pss-sha256` | 230:32 | 230:70 | [9283, 9321) | [9283, 9321) | 38 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_PSS_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_PSS_PADDING` | - |
| TS-140 | S17 | `prm:salt-length-bytes` | `rsassa-pss-sha256` | 230:84 | 230:86 | [9335, 9337) | [9335, 9337) | 2 | 1 | `s17Rsa3072` | - | `lib.node` | - | `32` | - |
| TS-141 | S17 | `op:sign` | `rsassa-pkcs1v15-sha256` | 235:26 | 238:5 | [9440, 9547) | [9440, 9547) | 107 | 0 | `s17Rsa3072` | `node:crypto.sign` | `lib.node` | - | `crypto.sign("sha256", MESSAGE, { … (+3 lines)` | - |
| TS-142 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 235:38 | 235:46 | [9452, 9460) | [9452, 9460) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | - |
| TS-143 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 237:14 | 237:48 | [9507, 9541) | [9507, 9541) | 34 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_PADDING` | - |
| TS-144 | S17 | `op:verify` | `rsassa-pkcs1v15-sha256` | 239:19 | 244:4 | [9567, 9701) | [9567, 9701) | 134 | 0 | `s17Rsa3072` | `node:crypto.verify` | `lib.node` | - | `crypto.verify( … (+5 lines)` | - |
| TS-145 | S17 | `alg` | `sha-256` ^`rsassa-pkcs1v15-sha256` | 240:5 | 240:13 | [9586, 9594) | [9586, 9594) | 8 | 1 | `s17Rsa3072` | - | `lib.node` | - | `"sha256"` | - |
| TS-146 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 242:32 | 242:66 | [9640, 9674) | [9640, 9674) | 34 | 1 | `s17Rsa3072` | `node:crypto.constants.RSA_PKCS1_PADDING` | `lib.node` | - | `crypto.constants.RSA_PKCS1_PADDING` | - |
| TS-147 | S18 | `op:keygen` | `ecdsa-p256-sha256` | 250:22 | 250:107 | [9882, 9967) | [9882, 9967) | 85 | 0 | `s18EcdsaP256` | `globalThis.crypto.subtle.generateKey` | `lib.node` | `m.ecdsa-private-key`, `m.ecdsa-public-key` | `subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, false, ["sign", "verify"])` | - |
| TS-148 | S18 | `alg` | `ecdsa-p256-sha256` | 250:49 | 250:56 | [9909, 9916) | [9909, 9916) | 7 | 1 | `s18EcdsaP256` | - | `lib.node` | - | `"ECDSA"` | - |
| TS-149 | S18 | `alg` | `ecdsa-p256-sha256` | 250:70 | 250:77 | [9930, 9937) | [9930, 9937) | 7 | 1 | `s18EcdsaP256` | - | `lib.node` | - | `"P-256"` | - |
| TS-150 | S18 | `alg` | `ecdsa-p256-sha256` | 251:29 | 251:36 | [9997, 10004) | [9997, 10004) | 7 | 0 | `s18EcdsaP256` | - | `lib.node` | - | `"ECDSA"` | - |
| TS-151 | S18 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 251:44 | 251:53 | [10012, 10021) | [10012, 10021) | 9 | 0 | `s18EcdsaP256` | - | `lib.node` | - | `"SHA-256"` | - |
| TS-152 | S18 | `op:sign` | `ecdsa-p256-sha256` | 252:27 | 252:75 | [10051, 10099) | [10051, 10099) | 48 | 0 | `s18EcdsaP256` | `globalThis.crypto.subtle.sign` | `lib.node` | - | `subtle.sign(algorithm, keys.privateKey, MESSAGE)` | p1363 |
| TS-153 | S18 | `op:verify` | `ecdsa-p256-sha256` | 253:20 | 253:80 | [10120, 10180) | [10120, 10180) | 60 | 0 | `s18EcdsaP256` | `globalThis.crypto.subtle.verify` | `lib.node` | - | `subtle.verify(algorithm, keys.publicKey, signature, MESSAGE)` | - |
| TS-154 | S19 | `op:keygen` | `ed25519` | 259:21 | 259:55 | [10326, 10360) | [10326, 10360) | 34 | 0 | `s19Ed25519` | `@noble/curves/ed25519.js:ed25519.getPublicKey` | `lib.noble-curves` | `m.ed25519-public-key` | `ed25519.getPublicKey(ED25519_SEED)` | seed-ctor |
| TS-155 | S19 | `op:sign` | `ed25519` | 260:21 | 260:56 | [10382, 10417) | [10382, 10417) | 35 | 0 | `s19Ed25519` | `@noble/curves/ed25519.js:ed25519.sign` | `lib.noble-curves` | - | `ed25519.sign(MESSAGE, ED25519_SEED)` | - |
| TS-156 | S19 | `op:verify` | `ed25519` | 261:14 | 261:59 | [10432, 10477) | [10432, 10477) | 45 | 0 | `s19Ed25519` | `@noble/curves/ed25519.js:ed25519.verify` | `lib.noble-curves` | - | `ed25519.verify(signature, MESSAGE, publicKey)` | - |
| TS-157 | S20 | `op:keyderive` | `hkdf-sha256` | 266:15 | 266:91 | [10651, 10727) | [10651, 10727) | 76 | 0 | `deriveSessionKey` | `node:crypto.hkdfSync` | `lib.node` | `m.session-key` | `crypto.hkdfSync("sha256", sharedSecret, new Uint8Array(0), SESSION_INFO, 32)` | - |
| TS-158 | S20 | `alg` | `sha-256` ^`hkdf-sha256` | 266:31 | 266:39 | [10667, 10675) | [10667, 10675) | 8 | 1 | `deriveSessionKey` | - | `lib.node` | - | `"sha256"` | - |
| TS-159 | S20 | `prm:output-length-bytes` | `hkdf-sha256` | 266:88 | 266:90 | [10724, 10726) | [10724, 10726) | 2 | 1 | `deriveSessionKey` | - | `lib.node` | - | `32` | - |
| TS-160 | S20 | `op:keygen` | `x25519` | 272:17 | 272:53 | [10873, 10909) | [10873, 10909) | 36 | 0 | `s20KeyAgreement` | `node:crypto.generateKeyPairSync` | `lib.node` | `m.x25519-private-key-a` | `crypto.generateKeyPairSync("x25519")` | - |
| TS-161 | S20 | `alg` | `x25519` | 272:44 | 272:52 | [10900, 10908) | [10900, 10908) | 8 | 1 | `s20KeyAgreement` | - | `lib.node` | - | `"x25519"` | - |
| TS-162 | S20 | `op:keygen` | `x25519` | 273:15 | 273:51 | [10925, 10961) | [10925, 10961) | 36 | 0 | `s20KeyAgreement` | `node:crypto.generateKeyPairSync` | `lib.node` | `m.x25519-private-key-b` | `crypto.generateKeyPairSync("x25519")` | - |
| TS-163 | S20 | `alg` | `x25519` | 273:42 | 273:50 | [10952, 10960) | [10952, 10960) | 8 | 1 | `s20KeyAgreement` | - | `lib.node` | - | `"x25519"` | - |
| TS-164 | S20 | `op:agree` | `x25519` | 274:18 | 274:98 | [10980, 11060) | [10980, 11060) | 80 | 0 | `s20KeyAgreement` | `node:crypto.diffieHellman` | `lib.node` | `m.x25519-shared-secret` | `crypto.diffieHellman({ privateKey: alice.privateKey, publicKey: bob.publicKey })` | - |
| TS-165 | S20 | `op:agree` | `x25519` | 275:16 | 275:96 | [11077, 11157) | [11077, 11157) | 80 | 0 | `s20KeyAgreement` | `node:crypto.diffieHellman` | `lib.node` | `m.x25519-shared-secret` | `crypto.diffieHellman({ privateKey: bob.privateKey, publicKey: alice.publicKey })` | - |
| TS-166 | S20 | `ctor` | `ecdh-p256` | 278:19 | 278:50 | [11235, 11266) | [11235, 11266) | 31 | 0 | `s20KeyAgreement` | `node:crypto.createECDH` | `lib.node` | - | `crypto.createECDH("prime256v1")` | - |
| TS-167 | S20 | `alg` | `ecdh-p256` | 278:37 | 278:49 | [11253, 11265) | [11253, 11265) | 12 | 1 | `s20KeyAgreement` | - | `lib.node` | - | `"prime256v1"` | curve-alias |
| TS-168 | S20 | `ctor` | `ecdh-p256` | 279:17 | 279:48 | [11284, 11315) | [11284, 11315) | 31 | 0 | `s20KeyAgreement` | `node:crypto.createECDH` | `lib.node` | - | `crypto.createECDH("prime256v1")` | - |
| TS-169 | S20 | `alg` | `ecdh-p256` | 279:35 | 279:47 | [11302, 11314) | [11302, 11314) | 12 | 1 | `s20KeyAgreement` | - | `lib.node` | - | `"prime256v1"` | curve-alias |
| TS-170 | S20 | `op:keygen` | `ecdh-p256` | 280:23 | 280:45 | [11339, 11361) | [11339, 11361) | 22 | 0 | `s20KeyAgreement` | `node:crypto.ECDH.generateKeys` | `lib.node` | `m.ecdh-private-key-a` | `aliceEc.generateKeys()` | - |
| TS-171 | S20 | `op:keygen` | `ecdh-p256` | 281:21 | 281:41 | [11383, 11403) | [11383, 11403) | 20 | 0 | `s20KeyAgreement` | `node:crypto.ECDH.generateKeys` | `lib.node` | `m.ecdh-private-key-b` | `bobEc.generateKeys()` | - |
| TS-172 | S20 | `op:agree` | `ecdh-p256` | 282:18 | 282:50 | [11422, 11454) | [11422, 11454) | 32 | 0 | `s20KeyAgreement` | `node:crypto.ECDH.computeSecret` | `lib.node` | `m.ecdh-shared-secret` | `aliceEc.computeSecret(bobPublic)` | - |
| TS-173 | S20 | `op:agree` | `ecdh-p256` | 283:16 | 283:48 | [11471, 11503) | [11471, 11503) | 32 | 0 | `s20KeyAgreement` | `node:crypto.ECDH.computeSecret` | `lib.node` | `m.ecdh-shared-secret` | `bobEc.computeSecret(alicePublic)` | - |
| TS-174 | S21 | `op:keygen` | `ml-kem-768` | 293:36 | 293:54 | [11863, 11881) | [11863, 11881) | 18 | 0 | `s21MlKem768` | `@noble/post-quantum/ml-kem.js:ml_kem768.keygen` | `lib.noble-pq` | `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key` | `ml_kem768.keygen()` | - |
| TS-175 | S21 | `op:encapsulate` | `ml-kem-768` | 294:40 | 294:72 | [11922, 11954) | [11922, 11954) | 32 | 0 | `s21MlKem768` | `@noble/post-quantum/ml-kem.js:ml_kem768.encapsulate` | `lib.noble-pq` | `m.mlkem-shared-secret` | `ml_kem768.encapsulate(publicKey)` | - |
| TS-176 | S21 | `op:decapsulate` | `ml-kem-768` | 295:21 | 295:65 | [11976, 12020) | [11976, 12020) | 44 | 0 | `s21MlKem768` | `@noble/post-quantum/ml-kem.js:ml_kem768.decapsulate` | `lib.noble-pq` | `m.mlkem-shared-secret` | `ml_kem768.decapsulate(cipherText, secretKey)` | - |
| TS-177 | S22 | `op:keygen` | `ml-dsa-65` | 301:36 | 301:53 | [12241, 12258) | [12241, 12258) | 17 | 0 | `s22MlDsa65` | `@noble/post-quantum/ml-dsa.js:ml_dsa65.keygen` | `lib.noble-pq` | `m.mldsa-private-key`, `m.mldsa-public-key` | `ml_dsa65.keygen()` | - |
| TS-178 | S22 | `op:sign` | `ml-dsa-65` | 302:21 | 302:54 | [12280, 12313) | [12280, 12313) | 33 | 0 | `s22MlDsa65` | `@noble/post-quantum/ml-dsa.js:ml_dsa65.sign` | `lib.noble-pq` | - | `ml_dsa65.sign(MESSAGE, secretKey)` | - |
| TS-179 | S22 | `op:verify` | `ml-dsa-65` | 303:14 | 303:60 | [12328, 12374) | [12328, 12374) | 46 | 0 | `s22MlDsa65` | `@noble/post-quantum/ml-dsa.js:ml_dsa65.verify` | `lib.noble-pq` | - | `ml_dsa65.verify(signature, MESSAGE, publicKey)` | - |
| TS-180 | S23 | `init` | `cert.self-signed` | 309:3 | 309:45 | [12569, 12611) | [12569, 12611) | 42 | 0 | `s23X509SelfSigned` | `@peculiar/x509:cryptoProvider.set` | `lib.peculiar-x509` | - | `x509.cryptoProvider.set(globalThis.crypto)` | provider-binding |
| TS-181 | S23 | `alg` | `ecdsa-p256-sha256` | 310:29 | 310:36 | [12641, 12648) | [12641, 12648) | 7 | 0 | `s23X509SelfSigned` | - | `lib.node` | - | `"ECDSA"` | - |
| TS-182 | S23 | `alg` | `ecdsa-p256-sha256` | 310:50 | 310:57 | [12662, 12669) | [12662, 12669) | 7 | 0 | `s23X509SelfSigned` | - | `lib.node` | - | `"P-256"` | - |
| TS-183 | S23 | `alg` | `sha-256` ^`ecdsa-p256-sha256` | 310:65 | 310:74 | [12677, 12686) | [12677, 12686) | 9 | 0 | `s23X509SelfSigned` | - | `lib.node` | - | `"SHA-256"` | - |
| TS-184 | S23 | `op:keygen` | `ecdsa-p256-sha256` | 311:22 | 311:78 | [12711, 12767) | [12711, 12767) | 56 | 0 | `s23X509SelfSigned` | `globalThis.crypto.subtle.generateKey` | `lib.node` | `m.cert-private-key`, `m.cert-public-key` | `subtle.generateKey(algorithm, false, ["sign", "verify"])` | - |
| TS-185 | S23 | `op:sign` | `cert.self-signed` | 313:29 | 320:5 | [12823, 13089) | [12823, 13089) | 266 | 0 | `s23X509SelfSigned` | `@peculiar/x509:X509CertificateGenerator.createSelfSigned` | `lib.peculiar-x509` | - | `x509.X509CertificateGenerator.createSelfSigned({ … (+7 lines)` | - |
| TS-186 | S23 | `op:generate` | `csprng` | 314:25 | 314:46 | [12896, 12917) | [12896, 12917) | 21 | 1 | `s23X509SelfSigned` | `node:crypto.randomBytes` | `lib.node` | - | `crypto.randomBytes(8)` | serial |
| TS-187 | S23 | `prm:validity-days` | `cert.self-signed` | 317:30 | 317:33 | [13023, 13026) | [13023, 13026) | 3 | 1 | `s23X509SelfSigned` | - | `lib.peculiar-x509` | - | `365` | - |
| TS-188 | S23 | `op:verify` | `ecdsa-p256-sha256` | 321:20 | 321:90 | [13110, 13180) | [13110, 13180) | 70 | 0 | `s23X509SelfSigned` | `@peculiar/x509:X509Certificate.verify` | `lib.peculiar-x509` | - | `certificate.verify({ publicKey: keys.publicKey, signatureOnly: true })` | - |
| TS-189 | S24 | `ctor` | `tls13-client` | 327:19 | 331:5 | [13355, 13530) | [13355, 13530) | 175 | 0 | `s24Tls13Client` | `node:tls.createSecureContext` | `lib.node` | - | `tls.createSecureContext({ … (+4 lines)` | - |
| TS-190 | S24 | `cfg:min-version` | `tls13-client` | 328:17 | 328:26 | [13397, 13406) | [13397, 13406) | 9 | 1 | `s24Tls13Client` | - | `lib.node` | - | `"TLSv1.3"` | - |
| TS-191 | S24 | `cfg:max-version` | `tls13-client` | 329:17 | 329:26 | [13424, 13433) | [13424, 13433) | 9 | 1 | `s24Tls13Client` | - | `lib.node` | - | `"TLSv1.3"` | - |
| TS-192 | S24 | `cfg:cipher-suites` | `tls13-client` | 330:14 | 330:90 | [13448, 13524) | [13448, 13524) | 76 | 1 | `s24Tls13Client` | - | `lib.node` | - | `"TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256"` | node-ciphers |

## Full text of multi-line evidence

**TS-056** (`pbkdf2-hmac-sha256`, 119:22 to 123:4):

```text
subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt: PBKDF2_SALT, iterations: 80_000 },
    baseKey,
    512,
  )
```

**TS-127** (`rsa-oaep-sha256`, 212:22 to 215:4):

```text
crypto.publicEncrypt(
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" },
    MESSAGE,
  )
```

**TS-130** (`rsa-oaep-sha256`, 216:21 to 219:4):

```text
crypto.privateDecrypt(
    { key: privateKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" },
    ciphertext,
  )
```

**TS-133** (`rsassa-pss-sha256`, 222:24 to 226:5):

```text
crypto.sign("sha256", MESSAGE, {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: 32,
  })
```

**TS-137** (`rsassa-pss-sha256`, 227:17 to 232:4):

```text
crypto.verify(
    "sha256",
    MESSAGE,
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_PSS_PADDING, saltLength: 32 },
    pssSignature,
  )
```

**TS-141** (`rsassa-pkcs1v15-sha256`, 235:26 to 238:5):

```text
crypto.sign("sha256", MESSAGE, {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PADDING,
  })
```

**TS-144** (`rsassa-pkcs1v15-sha256`, 239:19 to 244:4):

```text
crypto.verify(
    "sha256",
    MESSAGE,
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_PADDING },
    pkcs1Signature,
  )
```

**TS-185** (`cert.self-signed`, 313:29 to 320:5):

```text
x509.X509CertificateGenerator.createSelfSigned({
    serialNumber: toHex(crypto.randomBytes(8)),
    name: `CN=${TLS_SERVER_NAME}`,
    notBefore: new Date(now - 60_000),
    notAfter: new Date(now + 365 * 86_400_000),
    signingAlgorithm: algorithm,
    keys,
  })
```

**TS-189** (`tls13-client`, 327:19 to 331:5):

```text
tls.createSecureContext({
    minVersion: "TLSv1.3",
    maxVersion: "TLSv1.3",
    ciphers: "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
  })
```

## Non-asset mentions (negative ground truth)

Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.

| ID | L:C | Bytes | Match | Context | Containing token / line | Why it is not an asset |
|---|---|---|---|---|---|---|
| TS-N001 | 8:65 | [381, 385) | `x509` | comment | `// reflect-metadata is a runtime polyfill required by @peculiar/x509 (tsyringe).` | Comment text; documentation only |
| TS-N002 | 31:14 | [1316, 1320) | `HMAC` | comment | `// Wikipedia HMAC example key` | Comment text; documentation only |
| TS-N003 | 44:4 | [1831, 1834) | `GCM` | comment | `// GCM specification test case 16` | Comment text; documentation only |
| TS-N004 | 48:7 | [2082, 2085) | `GCM` | identifier | `GCM_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| TS-N005 | 54:7 | [2337, 2340) | `ECB` | identifier | `ECB_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| TS-N006 | 58:7 | [2591, 2594) | `TLS` | identifier | `TLS_SERVER_NAME` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| TS-N007 | 80:9 | [3292, 3299) | `SHA-256` | comment | `// S01: SHA-256 (FIPS 180-4)` | Comment text; documentation only |
| TS-N008 | 82:16 | [3357, 3364) | `SHA-256` | string | `"SHA-256"` | Output label passed to emit(); printed text only |
| TS-N009 | 85:9 | [3438, 3445) | `SHA-512` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| TS-N010 | 85:18 | [3447, 3455) | `SHA3-256` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| TS-N011 | 85:28 | [3457, 3464) | `BLAKE2b` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| TS-N012 | 87:16 | [3521, 3528) | `SHA-512` | string | `"SHA-512"` | Output label passed to emit(); printed text only |
| TS-N013 | 88:16 | [3606, 3614) | `SHA3-256` | string | `"SHA3-256"` | Output label passed to emit(); printed text only |
| TS-N014 | 89:16 | [3659, 3666) | `BLAKE2b` | string | `"BLAKE2b-512"` | Output label passed to emit(); printed text only |
| TS-N015 | 94:16 | [3810, 3813) | `MD5` | string | `"MD5"` | Output label passed to emit(); printed text only |
| TS-N016 | 95:16 | [3888, 3893) | `SHA-1` | string | `"SHA-1"` | Output label passed to emit(); printed text only |
| TS-N017 | 98:9 | [3965, 3973) | `SHAKE128` | comment | `// S04: SHAKE128 extendable-output function` | Comment text; documentation only |
| TS-N018 | 101:16 | [4114, 4122) | `SHAKE128` | string | `"SHAKE128"` | Output label passed to emit(); printed text only |
| TS-N019 | 104:9 | [4172, 4176) | `HMAC` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| TS-N020 | 104:14 | [4177, 4183) | `SHA256` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| TS-N021 | 107:16 | [4285, 4289) | `HMAC` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| TS-N022 | 107:21 | [4290, 4296) | `SHA256` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| TS-N023 | 110:9 | [4346, 4350) | `HKDF` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| TS-N024 | 110:14 | [4351, 4357) | `SHA256` | comment | `// S06: HKDF-SHA256 (RFC 5869)` | Comment text; documentation only |
| TS-N025 | 113:16 | [4494, 4498) | `HKDF` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| TS-N026 | 113:21 | [4499, 4505) | `SHA256` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| TS-N027 | 116:9 | [4532, 4538) | `PBKDF2` | comment | `// S07: PBKDF2-HMAC-SHA256 through WebCrypto` | Comment text; documentation only |
| TS-N028 | 116:16 | [4539, 4543) | `HMAC` | comment | `// S07: PBKDF2-HMAC-SHA256 through WebCrypto` | Comment text; documentation only |
| TS-N029 | 116:21 | [4544, 4550) | `SHA256` | comment | `// S07: PBKDF2-HMAC-SHA256 through WebCrypto` | Comment text; documentation only |
| TS-N030 | 124:16 | [4874, 4880) | `PBKDF2` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| TS-N031 | 124:23 | [4881, 4887) | `SHA256` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| TS-N032 | 127:9 | [4915, 4921) | `scrypt` | comment | `// S08: scrypt` | Comment text; documentation only |
| TS-N033 | 130:16 | [5065, 5071) | `scrypt` | string | `"scrypt"` | Output label passed to emit(); printed text only |
| TS-N034 | 133:9 | [5102, 5110) | `Argon2id` | comment | `// S09: Argon2id` | Comment text; documentation only |
| TS-N035 | 136:16 | [5248, 5256) | `Argon2id` | string | `"Argon2id"` | Output label passed to emit(); printed text only |
| TS-N036 | 139:9 | [5283, 5289) | `bcrypt` | comment | `// S10: bcrypt` | Comment text; documentation only |
| TS-N037 | 144:16 | [5470, 5476) | `bcrypt` | string | `"bcrypt"` | Output label passed to emit(); printed text only |
| TS-N038 | 147:9 | [5507, 5514) | `AES-256` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| TS-N039 | 147:17 | [5515, 5518) | `GCM` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| TS-N040 | 150:20 | [5686, 5689) | `GCM` | identifier | `GCM_AAD` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| TS-N041 | 154:20 | [5943, 5946) | `GCM` | identifier | `GCM_AAD` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| TS-N042 | 157:16 | [6083, 6090) | `AES-256` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| TS-N043 | 157:24 | [6091, 6094) | `GCM` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| TS-N044 | 157:102 | [6169, 6172) | `GCM` | string | `` `ct=${toHex(ciphertext)} tag=${toHex(tag)} roundtrip=${equal(plaintext, GCM_PLA… `` | Output label passed to emit(); printed text only |
| TS-N045 | 160:9 | [6199, 6216) | `ChaCha20-Poly1305` | comment | `// S12: ChaCha20-Poly1305 (RFC 8439)` | Comment text; documentation only |
| TS-N046 | 166:16 | [6473, 6490) | `ChaCha20-Poly1305` | string | `"ChaCha20-Poly1305"` | Output label passed to emit(); printed text only |
| TS-N047 | 169:9 | [6544, 6551) | `AES-256` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| TS-N048 | 169:17 | [6552, 6555) | `CBC` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| TS-N049 | 177:16 | [7004, 7011) | `AES-256` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| TS-N050 | 177:24 | [7012, 7015) | `CBC` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| TS-N051 | 180:9 | [7072, 7079) | `AES-128` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| TS-N052 | 180:17 | [7080, 7083) | `ECB` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| TS-N053 | 184:16 | [7337, 7344) | `AES-128` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| TS-N054 | 184:24 | [7345, 7348) | `ECB` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| TS-N055 | 187:9 | [7382, 7389) | `AES-256` | comment | `// S15: AES-256-CTR through WebCrypto` | Comment text; documentation only |
| TS-N056 | 187:17 | [7390, 7393) | `CTR` | comment | `// S15: AES-256-CTR through WebCrypto` | Comment text; documentation only |
| TS-N057 | 194:16 | [7844, 7851) | `AES-256` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| TS-N058 | 194:24 | [7852, 7855) | `CTR` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| TS-N059 | 197:9 | [7912, 7916) | `3DES` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| TS-N060 | 197:15 | [7918, 7922) | `TDEA` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| TS-N061 | 197:21 | [7924, 7927) | `CBC` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| TS-N062 | 205:16 | [8377, 8381) | `3DES` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| TS-N063 | 205:21 | [8382, 8385) | `CBC` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| TS-N064 | 208:9 | [8442, 8445) | `RSA` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| TS-N065 | 208:20 | [8453, 8457) | `OAEP` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| TS-N066 | 208:26 | [8459, 8462) | `PSS` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| TS-N067 | 220:16 | [8978, 8981) | `RSA` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| TS-N068 | 220:25 | [8987, 8991) | `OAEP` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| TS-N069 | 233:16 | [9379, 9382) | `RSA` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| TS-N070 | 233:25 | [9388, 9391) | `PSS` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| TS-N071 | 245:16 | [9718, 9721) | `RSA` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| TS-N072 | 245:25 | [9727, 9735) | `PKCS1v15` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| TS-N073 | 248:9 | [9771, 9776) | `ECDSA` | comment | `// S18: ECDSA P-256 with SHA-256 through WebCrypto` | Comment text; documentation only |
| TS-N074 | 248:15 | [9777, 9782) | `P-256` | comment | `// S18: ECDSA P-256 with SHA-256 through WebCrypto` | Comment text; documentation only |
| TS-N075 | 248:26 | [9788, 9795) | `SHA-256` | comment | `// S18: ECDSA P-256 with SHA-256 through WebCrypto` | Comment text; documentation only |
| TS-N076 | 254:16 | [10197, 10202) | `ECDSA` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| TS-N077 | 254:22 | [10203, 10208) | `P-256` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| TS-N078 | 257:9 | [10239, 10246) | `Ed25519` | comment | `// S19: Ed25519 from a fixed seed (RFC 8032)` | Comment text; documentation only |
| TS-N079 | 262:16 | [10494, 10501) | `Ed25519` | string | `"Ed25519"` | Output label passed to emit(); printed text only |
| TS-N080 | 270:9 | [10770, 10776) | `X25519` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| TS-N081 | 270:18 | [10779, 10783) | `ECDH` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| TS-N082 | 270:23 | [10784, 10789) | `P-256` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| TS-N083 | 270:44 | [10805, 10809) | `HKDF` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| TS-N084 | 276:16 | [11174, 11180) | `X25519` | string | `"X25519"` | Output label passed to emit(); printed text only |
| TS-N085 | 284:16 | [11520, 11524) | `ECDH` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| TS-N086 | 284:21 | [11525, 11530) | `P-256` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| TS-N087 | 288:16 | [11712, 11716) | `HKDF` | string | `"HKDF session key"` | Output label passed to emit(); printed text only |
| TS-N088 | 291:9 | [11775, 11785) | `ML-KEM-768` | comment | `// S21: ML-KEM-768 (FIPS 203)` | Comment text; documentation only |
| TS-N089 | 296:16 | [12037, 12047) | `ML-KEM-768` | string | `"ML-KEM-768"` | Output label passed to emit(); printed text only |
| TS-N090 | 299:9 | [12155, 12164) | `ML-DSA-65` | comment | `// S22: ML-DSA-65 (FIPS 204)` | Comment text; documentation only |
| TS-N091 | 304:16 | [12391, 12400) | `ML-DSA-65` | string | `"ML-DSA-65"` | Output label passed to emit(); printed text only |
| TS-N092 | 307:21 | [12467, 12472) | `X.509` | comment | `// S23: self-signed X.509 certificate (@peculiar/x509 on WebCrypto)` | Comment text; documentation only |
| TS-N093 | 307:50 | [12496, 12500) | `x509` | comment | `// S23: self-signed X.509 certificate (@peculiar/x509 on WebCrypto)` | Comment text; documentation only |
| TS-N094 | 322:16 | [13197, 13202) | `X.509` | string | `"X.509 self-signed"` | Output label passed to emit(); printed text only |
| TS-N095 | 325:9 | [13245, 13248) | `TLS` | comment | `// S24: TLS 1.3-only client configuration (no connection is made)` | Comment text; documentation only |
| TS-N096 | 332:16 | [13547, 13550) | `TLS` | string | `"TLS 1.3 client"` | Output label passed to emit(); printed text only |

## Implicit and runtime-dependent cryptography

Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where source-level ground truth and the cryptography that actually executes can diverge.

| Asset | What happens |
|---|---|
| `csprng` | crypto.randomBytes, crypto.webcrypto.getRandomValues, WebCrypto key generation and node:crypto key generation all use OpenSSL RAND_bytes (bundled OpenSSL 3.5.5); @noble/ciphers randomBytes wraps crypto.getRandomValues; bcryptjs genSaltSync uses crypto.randomBytes. |
| `aes-256-cbc` | PKCS#7 padding for aes-256-cbc / aes-128-ecb / des-ede3-cbc is OpenSSL's implicit default. |
| `mgf1-sha256` | OpenSSL uses the OAEP hash (oaepHash) and the signing hash (PSS) for MGF1 implicitly. |
| `ecdsa-p256-sha256` | WebCrypto ECDSA signatures are IEEE P1363 (r||s). |
| `tls13-client` | Only a secure context is created (no socket). Key-exchange groups are the bundled OpenSSL 3.5 defaults, which offer the X25519MLKEM768 post-quantum hybrid. |
| `sha-512` | @noble/curves Ed25519 uses SHA-512 internally. |

## Detection notes

Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.

| Note | Explanation | Occurrences |
|---|---|---|
| `computed` | Parameter is a constant expression, not a literal (evaluates to 16384). | TS-063 |
| `keysize-from-key` | Key size is not named in code; it follows from the length of the key bytes (data-flow dependent). | TS-075 |
| `openssl-default-padding` | PKCS#7 padding is OpenSSL's implicit default (setAutoPadding(true)). | TS-095, TS-098, TS-101, TS-117, TS-120 |
| `oaep-mgf-same-hash` | MGF1 hash is implicit and equals the OAEP hash (SHA-256); MGF1 has no source occurrence here. | TS-129, TS-132 |
| `p1363` | WebCrypto ECDSA signatures are raw IEEE P1363 (r||s), not DER. | TS-152 |
| `seed-ctor` | Key pair is derived deterministically from the hard-coded 32-byte seed. | TS-154 |
| `curve-alias` | Curve alias; normalise to P-256 (secp256r1 = prime256v1 = P-256). | TS-167, TS-169 |
| `provider-binding` | Binds @peculiar/x509 to the Node.js WebCrypto implementation (crypto provider selection). | TS-180 |
| `serial` | CSPRNG output used for the certificate serial number (not key material). | TS-186 |
| `node-ciphers` | Node.js takes TLS 1.3 suite names through the same 'ciphers' option as TLS 1.2 cipher strings; there is no separate ciphersuites option (an unknown key would be silently ignored). | TS-192 |

## Machine-readable files

`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset (with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts (NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.
