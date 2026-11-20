# CBOM ground-truth corpus - Java

`src/main/java/corpus/CryptoShowcase.java` is the Java implementation of a 24-scenario cryptography program that is logically identical in Python, Java, Go, TypeScript and C#. This file records every location where a cryptographic asset appears in it: **331 occurrences** of **84 assets** (33 algorithms, 49 items of related crypto material, 1 certificate, 1 protocol) drawn from **4 library components**, plus **107 non-asset mentions** of algorithm names that a scanner should *not* report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> All keys, IVs, salts, seeds and passwords in this program are published test vectors or are generated at run time. Weak and legacy algorithms (MD5, SHA-1, AES-ECB, 3DES, a 24-bit HMAC key) are deliberate so that policy checks have something to find.

## Files

| File | Purpose |
|---|---|
| `src/main/java/corpus/CryptoShowcase.java` | The program (494 lines, ASCII, LF line endings) |
| `pom.xml` | Build manifest |
| `README.md` | This document |
| `cbom.cdx.json` | Ground-truth CycloneDX 1.6 CBOM (validated against the official 1.6 JSON schema) |
| `ground-truth.json` | Complete occurrence ledger, asset inventory and non-asset mentions |

## Build and run

```sh
mvn -q compile exec:java
# or, without Maven: javac -cp bcprov.jar:bcpkix.jar:bcutil.jar -d out src/main/java/corpus/CryptoShowcase.java && java -cp out:bcprov.jar:bcpkix.jar:bcutil.jar corpus.CryptoShowcase
```

Verified in the build environment with OpenJDK 25.0.4.1: javac/java against Bouncy Castle 1.86 compiled from the r1rv86 tag (also re-run against the 1.80 jars); javac -Xlint:all reported no warnings. Standard output was byte-identical to the other four implementations (see the corpus README).

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
| Occurrences | 331 |
| Occurrences with role `imp` | 38 |
| Occurrences with role `typ` | 1 |
| Occurrences with role `alg` | 62 |
| Occurrences with role `spec` | 22 |
| Occurrences with role `ctor` | 57 |
| Occurrences with role `init` | 36 |
| Occurrences with role `op` | 65 |
| Occurrences with role `prm` | 30 |
| Occurrences with role `mat` | 16 |
| Occurrences with role `cfg` | 4 |
| Algorithm assets (incl. implicit) | 33 |
| Implicit assets (no source occurrence) | 2 |
| Related crypto material | 49 |
| Certificates | 1 |
| Protocols | 1 |
| Library components | 4 |
| Non-asset mentions | 107 |

## Libraries

| ID | Component | Version | purl | License | Scope | Import occurrences | Other occurrences | Assets provided | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `lib.jdk` | OpenJDK java.base JCA/JCE/JSSE providers | 25.0.4.1 | `pkg:generic/openjdk@25.0.4.1` | GPL-2.0-only WITH Classpath-exception-2.0 | runtime | JV-001, JV-002, JV-003, JV-004, JV-005, JV-006, JV-007, JV-008, JV-009, JV-010, JV-011, JV-012, JV-013, JV-014, JV-015, JV-016, JV-017, JV-018, JV-019, JV-020, JV-021, JV-022, JV-023, JV-024, JV-025, JV-026 | 255 | sha-256, sha-512, sha3-256, md5, sha-1, shake128, hmac-sha256, hkdf-sha256, pbkdf2-hmac-sha256, argon2id, aes-256-gcm, chacha20-poly1305, aes-256-cbc, aes-128-ecb, aes-256-ctr, 3des-cbc, rsa-3072, mgf1-sha256, rsa-oaep-sha256, rsassa-pss-sha256, rsassa-pkcs1v15-sha256, ecdsa-p256-sha256, ecdh-p256, x25519, ml-kem-768, ml-dsa-65, csprng, tls13-client, m.hmac-key, m.hkdf-ikm, m.hkdf-salt, m.hkdf-info, m.pbkdf2-password, m.pbkdf2-salt, m.scrypt-password, m.scrypt-salt, m.password, m.argon2-salt, m.bcrypt-salt, m.gcm-key, m.gcm-iv, m.gcm-aad, m.chacha-nonce, m.cbc-iv, m.ecb-key, m.ctr-iv, m.tdes-iv, m.ed25519-seed, m.session-info | Providers SUN, SunRsaSign, SunEC, SunJCE, SunJSSE; KDF (JEP 510), KEM, ML-KEM (JEP 496) and ML-DSA (JEP 497) APIs |
| `lib.bcprov` | Bouncy Castle provider (bcprov-jdk18on) | 1.86 | `pkg:maven/org.bouncycastle/bcprov-jdk18on@1.86` | MIT | required | JV-027, JV-030, JV-031, JV-032, JV-033, JV-034, JV-035, JV-036, JV-037 | 32 | blake2b-512, shake128, scrypt, argon2id, bcrypt, ed25519 | Lightweight API used directly (no JCA provider registration) |
| `lib.bcpkix` | Bouncy Castle PKIX (bcpkix-jdk18on) | 1.86 | `pkg:maven/org.bouncycastle/bcpkix-jdk18on@1.86` | MIT | required | JV-028, JV-029, JV-038 | 6 | ecdsa-p256-sha256, cert.self-signed | X.509 certificate builder and JCA content signer |
| `lib.bcutil` | Bouncy Castle utilities (bcutil-jdk18on) | 1.86 | `pkg:maven/org.bouncycastle/bcutil-jdk18on@1.86` | MIT | transitive | - | 0 | - | Transitive dependency of bcpkix; not referenced directly |

## Algorithm assets

Identity and parameters (`functions` lists the CycloneDX crypto functions actually exercised here):

| Asset | Name | Primitive | Family | Parameter set | Mode | Padding | Curve | Functions | OID | Occurrences | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.1 | 7 | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | - | - | - | 2.16.840.1.101.3.4.2.2 | implicit | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | - | - | digest | 2.16.840.1.101.3.4.2.3 | 3 | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | - | - | digest | 2.16.840.1.101.3.4.2.8 | 3 | - |
| `blake2b-512` | BLAKE2b-512 | hash | BLAKE2 | 512 | - | - | - | digest | 1.3.6.1.4.1.1722.12.2.1.16 | 3 | - |
| `md5` | MD5 | hash | MD5 | 128 | - | - | - | digest | 1.2.840.113549.2.5 | 3 | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | - | - | digest | 1.3.14.3.2.26 | 3 | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | - | - | digest | 2.16.840.1.101.3.4.2.11 | 4 | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | - | - | tag | 1.2.840.113549.2.9 | 6 | sha-256 |
| `hkdf-sha256` | HKDF-SHA256 | kdf | HKDF | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.9.16.3.29 | 10 | hmac-sha256, sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | - | - | keyderive | 1.2.840.113549.1.5.12 | 6 | hmac-sha256, sha-256 |
| `scrypt` | scrypt | kdf | scrypt | N=16384,r=8,p=1 | - | - | - | keyderive | 1.3.6.1.4.1.11591.4.11 | 5 | pbkdf2-hmac-sha256 |
| `argon2id` | Argon2id | kdf | Argon2 | t=2,m=19456,p=1,v=0x13 | - | - | - | keyderive | - | 10 | - |
| `bcrypt` | bcrypt | kdf | bcrypt | cost=12 | - | - | - | keyderive, verify | - | 4 | - |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | gcm | - | - | decrypt, encrypt | 2.16.840.1.101.3.4.1.46 | 12 | - |
| `aes-128-gcm` | AES-128-GCM | ae | AES | 128 | gcm | - | - | - | 2.16.840.1.101.3.4.1.6 | implicit | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | other | - | - | decrypt, encrypt, keygen | 1.2.840.113549.1.9.16.3.18 | 13 | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | cbc | pkcs7 | - | decrypt, encrypt, keygen | 2.16.840.1.101.3.4.1.42 | 15 | - |
| `aes-128-ecb` | AES-128-ECB-PKCS7 | block-cipher | AES | 128 | ecb | pkcs7 | - | encrypt | 2.16.840.1.101.3.4.1.1 | 6 | - |
| `aes-256-ctr` | AES-256-CTR | block-cipher | AES | 256 | ctr | - | - | decrypt, encrypt, keygen | - | 15 | - |
| `3des-cbc` | 3DES-CBC-PKCS7 (3-key TDEA) | block-cipher | 3DES | 168 | cbc | pkcs7 | - | decrypt, encrypt, keygen | 1.2.840.113549.3.7 | 13 | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | - | - | keygen | 1.2.840.113549.1.1.1 | 7 | - |
| `mgf1-sha256` | MGF1-SHA256 | other | MGF1 | SHA-256 | - | - | - | - | 1.2.840.113549.1.1.8 | 4 | sha-256 |
| `rsa-oaep-sha256` | RSAES-OAEP-SHA256 (RSA-3072) | pke | RSA | 3072 | - | oaep | - | decrypt, encrypt | 1.2.840.113549.1.1.7 | 11 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pss-sha256` | RSASSA-PSS-SHA256 (RSA-3072) | signature | RSA | 3072 | - | other | - | sign, verify | 1.2.840.113549.1.1.10 | 15 | rsa-3072, sha-256, mgf1-sha256 |
| `rsassa-pkcs1v15-sha256` | RSASSA-PKCS1-v1_5-SHA256 (RSA-3072) | signature | RSA | 3072 | - | pkcs1v15 | - | sign, verify | 1.2.840.113549.1.1.11 | 8 | rsa-3072, sha-256 |
| `ecdsa-p256-sha256` | ECDSA P-256 with SHA-256 | signature | ECDSA | P-256 | - | - | secp256r1 | keygen, sign, verify | 1.2.840.10045.4.3.2 | 23 | sha-256 |
| `ecdh-p256` | ECDH P-256 | key-agree | ECDH | P-256 | - | - | secp256r1 | keyderive, keygen | 1.3.132.1.12 | 12 | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | - | - | curve25519 | keyderive, keygen | 1.3.101.110 | 9 | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | - | - | edwards25519 | keygen, sign, verify | 1.3.101.112 | 8 | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | - | - | decapsulate, encapsulate, keygen | 2.16.840.1.101.3.4.4.2 | 9 | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | - | - | keygen, sign, verify | 2.16.840.1.101.3.4.3.18 | 11 | - |
| `csprng` | Platform CSPRNG | drbg | CSPRNG | - | - | - | - | generate | - | 8 | - |

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
| `sha-256` | JV-057, JV-058, JV-059, JV-207, JV-209, JV-219, JV-221 |
| `sha-512` | JV-060, JV-061, JV-062 |
| `sha3-256` | JV-063, JV-064, JV-065 |
| `blake2b-512` | JV-066, JV-067, JV-068 |
| `md5` | JV-069, JV-070, JV-071 |
| `sha-1` | JV-072, JV-073, JV-074 |
| `shake128` | JV-075, JV-076, JV-077, JV-078 |
| `hmac-sha256` | JV-079, JV-080, JV-081, JV-082, JV-083, JV-084 |
| `hkdf-sha256` | JV-085, JV-086, JV-087, JV-088, JV-089, JV-270, JV-271, JV-272, JV-273, JV-274 |
| `pbkdf2-hmac-sha256` | JV-090, JV-091, JV-092, JV-093, JV-094, JV-095 |
| `scrypt` | JV-096, JV-097, JV-098, JV-099, JV-100 |
| `argon2id` | JV-101, JV-102, JV-103, JV-104, JV-105, JV-106, JV-107, JV-108, JV-109, JV-110 |
| `bcrypt` | JV-113, JV-114, JV-115, JV-116 |
| `aes-256-gcm` | JV-117, JV-118, JV-119, JV-120, JV-121, JV-122, JV-123, JV-124, JV-125, JV-126, JV-127, JV-128 |
| `chacha20-poly1305` | JV-129, JV-130, JV-131, JV-134, JV-135, JV-136, JV-137, JV-138, JV-139, JV-140, JV-141, JV-142, JV-143 |
| `aes-256-cbc` | JV-144, JV-145, JV-146, JV-147, JV-148, JV-151, JV-152, JV-153, JV-154, JV-155, JV-156, JV-157, JV-158, JV-159, JV-160 |
| `aes-128-ecb` | JV-161, JV-162, JV-163, JV-164, JV-165, JV-166 |
| `aes-256-ctr` | JV-167, JV-168, JV-169, JV-170, JV-171, JV-174, JV-175, JV-176, JV-177, JV-178, JV-179, JV-180, JV-181, JV-182, JV-183 |
| `3des-cbc` | JV-184, JV-185, JV-186, JV-189, JV-190, JV-191, JV-192, JV-193, JV-194, JV-195, JV-196, JV-197, JV-198 |
| `rsa-3072` | JV-199, JV-200, JV-201, JV-202, JV-203, JV-204, JV-205 |
| `mgf1-sha256` | JV-208, JV-209 (parameter:sha-256), JV-220, JV-221 (parameter:sha-256) |
| `rsa-oaep-sha256` | JV-206, JV-207 (parameter:sha-256), JV-208 (parameter:mgf1-sha256), JV-210, JV-211, JV-212, JV-213, JV-214, JV-215, JV-216, JV-217 |
| `rsassa-pss-sha256` | JV-218, JV-219 (parameter:sha-256), JV-220 (parameter:mgf1-sha256), JV-222, JV-223, JV-224, JV-225, JV-226, JV-227, JV-228, JV-229, JV-230, JV-231, JV-232, JV-233 |
| `rsassa-pkcs1v15-sha256` | JV-234, JV-235, JV-236, JV-237, JV-238, JV-239, JV-240, JV-241 |
| `ecdsa-p256-sha256` | JV-242, JV-243, JV-244, JV-245, JV-246, JV-247, JV-248, JV-249, JV-250, JV-251, JV-252, JV-253, JV-254, JV-255, JV-310, JV-311, JV-312, JV-313, JV-314, JV-315, JV-319, JV-320, JV-323 |
| `ecdh-p256` | JV-265, JV-267, JV-269, JV-281, JV-282, JV-283, JV-284, JV-285, JV-286, JV-287, JV-288, JV-289 |
| `x25519` | JV-264, JV-266, JV-268, JV-275, JV-276, JV-277, JV-278, JV-279, JV-280 |
| `ed25519` | JV-256, JV-257, JV-258, JV-259, JV-260, JV-261, JV-262, JV-263 |
| `ml-kem-768` | JV-290, JV-291, JV-292, JV-293, JV-294, JV-295, JV-296, JV-297, JV-298 |
| `ml-dsa-65` | JV-299, JV-300, JV-301, JV-302, JV-303, JV-304, JV-305, JV-306, JV-307, JV-308, JV-309 |
| `csprng` | JV-055, JV-056, JV-112, JV-133, JV-150, JV-173, JV-188, JV-317 |
| `cert.self-signed` | JV-316, JV-318, JV-321, JV-322 |
| `tls13-client` | JV-324, JV-325, JV-326, JV-327, JV-328, JV-329, JV-330, JV-331 |

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
| Occurrences | JV-316, JV-318, JV-321, JV-322 |

| Property | Value |
|---|---|
| Asset | `tls13-client` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_128_GCM_SHA256 (0x13,0x01); TLS_AES_256_GCM_SHA384 (0x13,0x02); TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03) |
| Note | Versions pinned to TLS 1.3. The three RFC 8446 cipher suites are listed explicitly where the API allows it (Java, TypeScript, C# on Linux/macOS) and are the implicit defaults elsewhere (Python, Go). Key-exchange groups are always implicit runtime defaults. |
| Occurrences | JV-324, JV-325, JV-326, JV-327, JV-328, JV-329, JV-330, JV-331 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Provenance | Test-vector value | Used with | Scenario | Defined / produced at | Note |
|---|---|---|---|---|---|---|---|---|---|
| `m.hmac-key` | HMAC key | secret-key | 24 | hardcoded | "key" (ASCII) | `hmac-sha256` | S05 | JV-039 @ 62:33 | 24-bit key - far below the 112-bit minimum; test vector only |
| `m.hkdf-ikm` | HKDF input keying material | secret-key | 176 | hardcoded | 0x0b * 22 | `hkdf-sha256` | S06 | JV-040 @ 64:33 | RFC 5869 A.1 |
| `m.hkdf-salt` | HKDF salt | salt | 104 | hardcoded | 000102...0c | `hkdf-sha256` | S06 | JV-041 @ 65:33 | RFC 5869 A.1 |
| `m.hkdf-info` | HKDF info | additional-data | 80 | hardcoded | f0f1...f9 | `hkdf-sha256` | S06 | JV-042 @ 66:33 | RFC 5869 A.1 |
| `m.hkdf-okm` | HKDF output keying material | secret-key | 336 | derived | - | `hkdf-sha256` | S06 | JV-089 @ 166:42 (produced) | - |
| `m.pbkdf2-password` | PBKDF2 password | password | 64 | hardcoded | "Password" | `pbkdf2-hmac-sha256` | S07 | JV-043 @ 68:33 | RFC 7914 section 11 |
| `m.pbkdf2-salt` | PBKDF2 salt | salt | 32 | hardcoded | "NaCl" | `pbkdf2-hmac-sha256` | S07 | JV-044 @ 69:33 | 32-bit salt is below the SP 800-132 minimum of 128 bits |
| `m.pbkdf2-dk` | PBKDF2 derived key | secret-key | 512 | derived | - | `pbkdf2-hmac-sha256` | S07 | JV-095 @ 173:23 (produced) | - |
| `m.scrypt-password` | scrypt password | password | 104 | hardcoded | "pleaseletmein" | `scrypt` | S08 | JV-045 @ 70:33 | RFC 7914 section 12 |
| `m.scrypt-salt` | scrypt salt | salt | 112 | hardcoded | "SodiumChloride" | `scrypt` | S08 | JV-046 @ 71:33 | - |
| `m.scrypt-dk` | scrypt derived key | secret-key | 512 | derived | - | `scrypt` | S08 | JV-096 @ 179:23 (produced) | - |
| `m.password` | Application password | password | 224 | hardcoded | "correct horse battery staple" | `argon2id` | S09 | JV-047 @ 72:33 | Shared by S09 (Argon2id) and S10 (bcrypt) |
| `m.argon2-salt` | Argon2id salt | salt | 128 | hardcoded | "cbom-corpus-salt" | `argon2id` | S09 | JV-048 @ 73:33 | - |
| `m.argon2-dk` | Argon2id output | secret-key | 256 | derived | - | `argon2id` | S09 | JV-110 @ 195:9 (produced) | - |
| `m.bcrypt-salt` | bcrypt salt | salt | 128 | csprng | - | `bcrypt` | S10 | JV-111 @ 201:29; JV-112 @ 202:9 (produced) | - |
| `m.bcrypt-hash` | bcrypt hash string | credential | 480 | derived | - | `bcrypt` | S10 | JV-113 @ 203:20 (produced) | 60-character modular-crypt string ($2a$/$2b$) |
| `m.gcm-key` | AES-256-GCM key | secret-key | 256 | hardcoded | feffe992... | `aes-256-gcm` | S11 | JV-049 @ 75:33 | GCM spec test case 16 |
| `m.gcm-iv` | AES-GCM IV | nonce | 96 | hardcoded | cafebabefacedbaddecaf888 | `aes-256-gcm` | S11 | JV-050 @ 76:33 | Static nonce - reuse with the same key is catastrophic outside a KAT |
| `m.gcm-aad` | AES-GCM additional authenticated data | additional-data | 160 | hardcoded | feedface... | `aes-256-gcm` | S11 | JV-051 @ 77:33 | GCM spec test case 16 |
| `m.chacha-key` | ChaCha20-Poly1305 key | secret-key | 256 | csprng | - | `chacha20-poly1305` | S12 | JV-131 @ 229:19 (produced) | - |
| `m.chacha-nonce` | ChaCha20-Poly1305 nonce | nonce | 96 | csprng | - | `chacha20-poly1305` | S12 | JV-132 @ 230:30; JV-133 @ 231:9 (produced) | - |
| `m.cbc-key` | AES-256-CBC key | secret-key | 256 | csprng | - | `aes-256-cbc` | S13 | JV-148 @ 245:19 (produced) | - |
| `m.cbc-iv` | AES-CBC IV | initialization-vector | 128 | csprng | - | `aes-256-cbc` | S13 | JV-149 @ 246:27; JV-150 @ 247:9 (produced) | - |
| `m.ecb-key` | AES-128-ECB key | secret-key | 128 | hardcoded | 000102...0f | `aes-128-ecb` | S14 | JV-052 @ 82:33 | FIPS 197 appendix C.1 |
| `m.ctr-key` | AES-256-CTR key | secret-key | 256 | csprng | - | `aes-256-ctr` | S15 | JV-171 @ 268:19 (produced) | - |
| `m.ctr-iv` | AES-CTR initial counter block | initialization-vector | 128 | csprng | - | `aes-256-ctr` | S15 | JV-172 @ 269:37; JV-173 @ 270:9 (produced) | - |
| `m.tdes-key` | 3DES key | secret-key | 192 | csprng | - | `3des-cbc` | S16 | JV-186 @ 283:19 (produced) | 192 bits incl. parity = 168 effective |
| `m.tdes-iv` | 3DES IV | initialization-vector | 64 | csprng | - | `3des-cbc` | S16 | JV-187 @ 284:27; JV-188 @ 285:9 (produced) | - |
| `m.rsa-private-key` | RSA-3072 private key | private-key | 3072 | keygen | - | `rsa-3072` | S17 | JV-205 @ 299:23 (produced) | - |
| `m.rsa-public-key` | RSA-3072 public key | public-key | 3072 | keygen | - | `rsa-3072` | S17 | JV-205 @ 299:23 (produced) | e = 65537 |
| `m.ecdsa-private-key` | ECDSA P-256 private key | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | JV-247 @ 339:23 (produced) | - |
| `m.ecdsa-public-key` | ECDSA P-256 public key | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S18 | JV-247 @ 339:23 (produced) | - |
| `m.ed25519-seed` | Ed25519 private key seed | private-key | 256 | hardcoded | 9d61b19d... | `ed25519` | S19 | JV-053 @ 85:33 | RFC 8032 section 7.1 TEST 1 |
| `m.ed25519-public-key` | Ed25519 public key | public-key | 256 | derived | d75a9801... | `ed25519` | S19 | JV-257 @ 353:25 (produced) | Derived from the seed |
| `m.x25519-private-key-a` | X25519 private key (party A) | private-key | 256 | keygen | - | `x25519` | S20 | JV-277 @ 381:21 (produced) | - |
| `m.x25519-private-key-b` | X25519 private key (party B) | private-key | 256 | keygen | - | `x25519` | S20 | JV-278 @ 382:19 (produced) | - |
| `m.x25519-shared-secret` | X25519 shared secret | shared-secret | 256 | agreed | - | `x25519` | S20 | JV-268 @ 369:16 (produced) | - |
| `m.ecdh-private-key-a` | ECDH P-256 private key (party A) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | JV-286 @ 389:23 (produced) | - |
| `m.ecdh-private-key-b` | ECDH P-256 private key (party B) | private-key | 256 | keygen | - | `ecdh-p256` | S20 | JV-287 @ 390:21 (produced) | - |
| `m.ecdh-shared-secret` | ECDH P-256 shared secret | shared-secret | 256 | agreed | - | `ecdh-p256` | S20 | JV-269 @ 369:16 (produced) | - |
| `m.session-info` | Session-key HKDF info | additional-data | 208 | hardcoded | "cbom-corpus session key v1" | `hkdf-sha256` | S20 | JV-054 @ 86:33 | - |
| `m.session-key` | Session key (HKDF over X25519 || ECDH secrets) | secret-key | 256 | derived | - | `hkdf-sha256` | S20 | JV-274 @ 375:16 (produced) | - |
| `m.mlkem-decapsulation-key` | ML-KEM-768 decapsulation key | private-key | - | keygen | - | `ml-kem-768` | S21 | JV-292 @ 403:23 (produced) | 64-byte seed form or 2400-byte expanded form, library-dependent |
| `m.mlkem-encapsulation-key` | ML-KEM-768 encapsulation key | public-key | 9472 | keygen | - | `ml-kem-768` | S21 | JV-292 @ 403:23 (produced) | 1184 bytes |
| `m.mlkem-shared-secret` | ML-KEM-768 shared secret | shared-secret | 256 | agreed | - | `ml-kem-768` | S21 | JV-295 @ 405:28 (produced); JV-297 @ 408:25 (produced) | - |
| `m.mldsa-private-key` | ML-DSA-65 private key | private-key | - | keygen | - | `ml-dsa-65` | S22 | JV-301 @ 416:23 (produced) | 32-byte seed or 4032-byte expanded form, library-dependent |
| `m.mldsa-public-key` | ML-DSA-65 public key | public-key | 15616 | keygen | - | `ml-dsa-65` | S22 | JV-301 @ 416:23 (produced) | 1952 bytes |
| `m.cert-private-key` | Certificate private key (P-256) | private-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | JV-315 @ 432:23 (produced) | - |
| `m.cert-public-key` | Certificate subject public key (P-256) | public-key | 256 | keygen | - | `ecdsa-p256-sha256` | S23 | JV-315 @ 432:23 (produced) | - |

## Scenario map

| Scenario | What it does | Output | Occurrences | Lines | Assets |
|---|---|---|---|---|---|
| S01 | SHA-256 digest of MESSAGE | Known answer (Wikipedia / NIST example message) | 3 | 118-119 | `sha-256` |
| S02 | SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | Known answers | 9 | 124-131 | `sha-512`, `sha3-256`, `blake2b-512` |
| S03 | Legacy MD5 and SHA-1 digests of MESSAGE | Known answers; deliberately weak algorithms | 6 | 137-140 | `md5`, `sha-1` |
| S04 | SHAKE128 XOF, 32-byte output | Known answer | 4 | 145-148 | `shake128` |
| S05 | HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | Known answer (Wikipedia HMAC example) | 7 | 62-156 | `hmac-sha256`, `m.hmac-key` |
| S06 | HKDF-SHA256 extract-and-expand, L=42 | Known answer (RFC 5869 A.1) | 8 | 64-166 | `hkdf-sha256`, `m.hkdf-ikm`, `m.hkdf-salt`, `m.hkdf-info`, `m.hkdf-okm` |
| S07 | PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | Known answer (RFC 7914 section 11) | 8 | 68-173 | `pbkdf2-hmac-sha256`, `m.pbkdf2-password`, `m.pbkdf2-salt`, `m.pbkdf2-dk` |
| S08 | scrypt N=16384 r=8 p=1, dkLen=64 | Known answer (RFC 7914 section 12) | 7 | 70-179 | `scrypt`, `m.scrypt-password`, `m.scrypt-salt`, `m.scrypt-dk` |
| S09 | Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | Deterministic; identical across languages | 12 | 72-195 | `argon2id`, `m.password`, `m.argon2-salt`, `m.argon2-dk` |
| S10 | bcrypt cost 12 with random salt, then verify | Randomized; prints verify=true | 6 | 201-204 | `bcrypt`, `csprng`, `m.bcrypt-salt`, `m.bcrypt-hash` |
| S11 | AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | Known answer (GCM spec test case 16) | 15 | 75-219 | `aes-256-gcm`, `m.gcm-key`, `m.gcm-iv`, `m.gcm-aad` |
| S12 | ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | Randomized round trip | 15 | 228-237 | `chacha20-poly1305`, `csprng`, `m.chacha-key`, `m.chacha-nonce` |
| S13 | AES-256-CBC with PKCS#7 padding, random key and IV | Randomized round trip | 17 | 243-253 | `aes-256-cbc`, `csprng`, `m.cbc-key`, `m.cbc-iv` |
| S14 | AES-128-ECB with PKCS#7 padding, hard-coded key | Known answer: first block = FIPS 197 C.1 | 7 | 82-261 | `aes-128-ecb`, `m.ecb-key` |
| S15 | AES-256-CTR, random key and 128-bit initial counter block | Randomized round trip | 17 | 266-276 | `aes-256-ctr`, `csprng`, `m.ctr-key`, `m.ctr-iv` |
| S16 | 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | Randomized round trip | 15 | 282-291 | `3des-cbc`, `csprng`, `m.tdes-key`, `m.tdes-iv` |
| S17 | RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | Randomized | 43 | 297-332 | `sha-256`, `rsa-3072`, `mgf1-sha256`, `rsa-oaep-sha256`, `rsassa-pss-sha256`, `rsassa-pkcs1v15-sha256`, `m.rsa-private-key`, `m.rsa-public-key` |
| S18 | ECDSA P-256 / SHA-256 sign and verify | Randomized | 14 | 337-347 | `ecdsa-p256-sha256`, `m.ecdsa-private-key`, `m.ecdsa-public-key` |
| S19 | Ed25519 from a hard-coded seed: public key, signature, verify | Known public key (RFC 8032 test 1); deterministic signature | 9 | 85-361 | `ed25519`, `m.ed25519-seed`, `m.ed25519-public-key` |
| S20 | X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | Randomized; prints agreement booleans | 27 | 86-392 | `hkdf-sha256`, `ecdh-p256`, `x25519`, `m.x25519-private-key-a`, `m.x25519-private-key-b`, `m.x25519-shared-secret`, `m.ecdh-private-key-a`, `m.ecdh-private-key-b`, `m.ecdh-shared-secret`, `m.session-info`, `m.session-key` |
| S21 | ML-KEM-768 key generation, encapsulation, decapsulation | Randomized; prints sizes | 9 | 402-408 | `ml-kem-768`, `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key`, `m.mlkem-shared-secret` |
| S22 | ML-DSA-65 key generation, signing, verification | Randomized; prints signature size | 11 | 415-424 | `ml-dsa-65`, `m.mldsa-private-key`, `m.mldsa-public-key` |
| S23 | Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | Randomized | 14 | 430-446 | `ecdsa-p256-sha256`, `csprng`, `cert.self-signed`, `m.cert-private-key`, `m.cert-public-key` |
| S24 | TLS 1.3-only client configuration (no network I/O) | Configuration only | 8 | 456-464 | `tls13-client` |

## Occurrence ledger

Every occurrence, in file order. Evidence longer than one line is shortened here and given in full in the next section and in `ground-truth.json`.

| ID | Scn | Role | Asset (^parent) | Start L:C | End L:C | Chars | Bytes | Len | Nest | Scope | API symbol | Library | Produces | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JV-001 | - | `imp` | `lib.jdk` | 5:1 | 5:39 | [88, 126) | [88, 126) | 38 | 0 | `<class CryptoShowcase>` | `java.security.KeyPairGenerator` | `lib.jdk` | - | `import java.security.KeyPairGenerator;` | - |
| JV-002 | - | `imp` | `lib.jdk` | 6:1 | 6:36 | [127, 162) | [127, 162) | 35 | 0 | `<class CryptoShowcase>` | `java.security.MessageDigest` | `lib.jdk` | - | `import java.security.MessageDigest;` | - |
| JV-003 | - | `imp` | `lib.jdk` | 7:1 | 7:33 | [163, 195) | [163, 195) | 32 | 0 | `<class CryptoShowcase>` | `java.security.PrivateKey` | `lib.jdk` | - | `import java.security.PrivateKey;` | - |
| JV-004 | - | `imp` | `lib.jdk` | 8:1 | 8:32 | [196, 227) | [196, 227) | 31 | 0 | `<class CryptoShowcase>` | `java.security.PublicKey` | `lib.jdk` | - | `import java.security.PublicKey;` | - |
| JV-005 | - | `imp` | `lib.jdk` | 9:1 | 9:35 | [228, 262) | [228, 262) | 34 | 0 | `<class CryptoShowcase>` | `java.security.SecureRandom` | `lib.jdk` | - | `import java.security.SecureRandom;` | - |
| JV-006 | - | `imp` | `lib.jdk` | 10:1 | 10:32 | [263, 294) | [263, 294) | 31 | 0 | `<class CryptoShowcase>` | `java.security.Signature` | `lib.jdk` | - | `import java.security.Signature;` | - |
| JV-007 | - | `imp` | `lib.jdk` | 11:1 | 11:46 | [295, 340) | [295, 340) | 45 | 0 | `<class CryptoShowcase>` | `java.security.spec.ECGenParameterSpec` | `lib.jdk` | - | `import java.security.spec.ECGenParameterSpec;` | - |
| JV-008 | - | `imp` | `lib.jdk` | 12:1 | 12:45 | [341, 385) | [341, 385) | 44 | 0 | `<class CryptoShowcase>` | `java.security.spec.MGF1ParameterSpec` | `lib.jdk` | - | `import java.security.spec.MGF1ParameterSpec;` | - |
| JV-009 | - | `imp` | `lib.jdk` | 13:1 | 13:44 | [386, 429) | [386, 429) | 43 | 0 | `<class CryptoShowcase>` | `java.security.spec.PSSParameterSpec` | `lib.jdk` | - | `import java.security.spec.PSSParameterSpec;` | - |
| JV-010 | - | `imp` | `lib.jdk` | 14:1 | 14:50 | [430, 479) | [430, 479) | 49 | 0 | `<class CryptoShowcase>` | `java.security.spec.RSAKeyGenParameterSpec` | `lib.jdk` | - | `import java.security.spec.RSAKeyGenParameterSpec;` | - |
| JV-011 | - | `imp` | `lib.jdk` | 20:1 | 20:28 | [609, 636) | [609, 636) | 27 | 0 | `<class CryptoShowcase>` | `javax.crypto.Cipher` | `lib.jdk` | - | `import javax.crypto.Cipher;` | - |
| JV-012 | - | `imp` | `lib.jdk` | 21:1 | 21:25 | [637, 661) | [637, 661) | 24 | 0 | `<class CryptoShowcase>` | `javax.crypto.KDF` | `lib.jdk` | - | `import javax.crypto.KDF;` | - |
| JV-013 | - | `imp` | `lib.jdk` | 22:1 | 22:25 | [662, 686) | [662, 686) | 24 | 0 | `<class CryptoShowcase>` | `javax.crypto.KEM` | `lib.jdk` | - | `import javax.crypto.KEM;` | - |
| JV-014 | - | `imp` | `lib.jdk` | 23:1 | 23:34 | [687, 720) | [687, 720) | 33 | 0 | `<class CryptoShowcase>` | `javax.crypto.KeyAgreement` | `lib.jdk` | - | `import javax.crypto.KeyAgreement;` | - |
| JV-015 | - | `imp` | `lib.jdk` | 24:1 | 24:34 | [721, 754) | [721, 754) | 33 | 0 | `<class CryptoShowcase>` | `javax.crypto.KeyGenerator` | `lib.jdk` | - | `import javax.crypto.KeyGenerator;` | - |
| JV-016 | - | `imp` | `lib.jdk` | 25:1 | 25:25 | [755, 779) | [755, 779) | 24 | 0 | `<class CryptoShowcase>` | `javax.crypto.Mac` | `lib.jdk` | - | `import javax.crypto.Mac;` | - |
| JV-017 | - | `imp` | `lib.jdk` | 26:1 | 26:38 | [780, 817) | [780, 817) | 37 | 0 | `<class CryptoShowcase>` | `javax.crypto.SecretKeyFactory` | `lib.jdk` | - | `import javax.crypto.SecretKeyFactory;` | - |
| JV-018 | - | `imp` | `lib.jdk` | 27:1 | 27:43 | [818, 860) | [818, 860) | 42 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.GCMParameterSpec` | `lib.jdk` | - | `import javax.crypto.spec.GCMParameterSpec;` | - |
| JV-019 | - | `imp` | `lib.jdk` | 28:1 | 28:44 | [861, 904) | [861, 904) | 43 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.HKDFParameterSpec` | `lib.jdk` | - | `import javax.crypto.spec.HKDFParameterSpec;` | - |
| JV-020 | - | `imp` | `lib.jdk` | 29:1 | 29:42 | [905, 946) | [905, 946) | 41 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.IvParameterSpec` | `lib.jdk` | - | `import javax.crypto.spec.IvParameterSpec;` | - |
| JV-021 | - | `imp` | `lib.jdk` | 30:1 | 30:44 | [947, 990) | [947, 990) | 43 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.OAEPParameterSpec` | `lib.jdk` | - | `import javax.crypto.spec.OAEPParameterSpec;` | - |
| JV-022 | - | `imp` | `lib.jdk` | 31:1 | 31:37 | [991, 1027) | [991, 1027) | 36 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.PBEKeySpec` | `lib.jdk` | - | `import javax.crypto.spec.PBEKeySpec;` | - |
| JV-023 | - | `imp` | `lib.jdk` | 32:1 | 32:34 | [1028, 1061) | [1028, 1061) | 33 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.PSource` | `lib.jdk` | - | `import javax.crypto.spec.PSource;` | - |
| JV-024 | - | `imp` | `lib.jdk` | 33:1 | 33:40 | [1062, 1101) | [1062, 1101) | 39 | 0 | `<class CryptoShowcase>` | `javax.crypto.spec.SecretKeySpec` | `lib.jdk` | - | `import javax.crypto.spec.SecretKeySpec;` | - |
| JV-025 | - | `imp` | `lib.jdk` | 34:1 | 34:33 | [1102, 1134) | [1102, 1134) | 32 | 0 | `<class CryptoShowcase>` | `javax.net.ssl.SSLContext` | `lib.jdk` | - | `import javax.net.ssl.SSLContext;` | - |
| JV-026 | - | `imp` | `lib.jdk` | 35:1 | 35:36 | [1135, 1170) | [1135, 1170) | 35 | 0 | `<class CryptoShowcase>` | `javax.net.ssl.SSLParameters` | `lib.jdk` | - | `import javax.net.ssl.SSLParameters;` | - |
| JV-027 | - | `imp` | `lib.bcprov` | 36:1 | 36:44 | [1171, 1214) | [1171, 1214) | 43 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.asn1.x500.X500Name` | `lib.bcprov` | - | `import org.bouncycastle.asn1.x500.X500Name;` | - |
| JV-028 | - | `imp` | `lib.bcpkix` | 37:1 | 37:65 | [1215, 1279) | [1215, 1279) | 64 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.cert.jcajce.JcaX509CertificateConverter` | `lib.bcpkix` | - | `import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;` | - |
| JV-029 | - | `imp` | `lib.bcpkix` | 38:1 | 38:65 | [1280, 1344) | [1280, 1344) | 64 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder` | `lib.bcpkix` | - | `import org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder;` | - |
| JV-030 | - | `imp` | `lib.bcprov` | 39:1 | 39:54 | [1345, 1398) | [1345, 1398) | 53 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.digests.Blake2bDigest` | `lib.bcprov` | - | `import org.bouncycastle.crypto.digests.Blake2bDigest;` | - |
| JV-031 | - | `imp` | `lib.bcprov` | 40:1 | 40:52 | [1399, 1450) | [1399, 1450) | 51 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.digests.SHAKEDigest` | `lib.bcprov` | - | `import org.bouncycastle.crypto.digests.SHAKEDigest;` | - |
| JV-032 | - | `imp` | `lib.bcprov` | 41:1 | 41:64 | [1451, 1514) | [1451, 1514) | 63 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.generators.Argon2BytesGenerator` | `lib.bcprov` | - | `import org.bouncycastle.crypto.generators.Argon2BytesGenerator;` | - |
| JV-033 | - | `imp` | `lib.bcprov` | 42:1 | 42:57 | [1515, 1571) | [1515, 1571) | 56 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.generators.OpenBSDBCrypt` | `lib.bcprov` | - | `import org.bouncycastle.crypto.generators.OpenBSDBCrypt;` | - |
| JV-034 | - | `imp` | `lib.bcprov` | 43:1 | 43:50 | [1572, 1621) | [1572, 1621) | 49 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.generators.SCrypt` | `lib.bcprov` | - | `import org.bouncycastle.crypto.generators.SCrypt;` | - |
| JV-035 | - | `imp` | `lib.bcprov` | 44:1 | 44:56 | [1622, 1677) | [1622, 1677) | 55 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.params.Argon2Parameters` | `lib.bcprov` | - | `import org.bouncycastle.crypto.params.Argon2Parameters;` | - |
| JV-036 | - | `imp` | `lib.bcprov` | 45:1 | 45:67 | [1678, 1744) | [1678, 1744) | 66 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.params.Ed25519PrivateKeyParameters` | `lib.bcprov` | - | `import org.bouncycastle.crypto.params.Ed25519PrivateKeyParameters;` | - |
| JV-037 | - | `imp` | `lib.bcprov` | 46:1 | 46:54 | [1745, 1798) | [1745, 1798) | 53 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.crypto.signers.Ed25519Signer` | `lib.bcprov` | - | `import org.bouncycastle.crypto.signers.Ed25519Signer;` | - |
| JV-038 | - | `imp` | `lib.bcpkix` | 47:1 | 47:65 | [1799, 1863) | [1799, 1863) | 64 | 0 | `<class CryptoShowcase>` | `org.bouncycastle.operator.jcajce.JcaContentSignerBuilder` | `lib.bcpkix` | - | `import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;` | - |
| JV-039 | S05 | `mat` | `m.hmac-key` | 62:33 | 62:56 | [2437, 2460) | [2437, 2460) | 23 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `HMAC_KEY = ascii("key")` | - |
| JV-040 | S06 | `mat` | `m.hkdf-ikm` | 64:33 | 64:68 | [2514, 2549) | [2514, 2549) | 35 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `HKDF_IKM = fromHex("0b".repeat(22))` | - |
| JV-041 | S06 | `mat` | `m.hkdf-salt` | 65:33 | 65:82 | [2583, 2632) | [2583, 2632) | 49 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `HKDF_SALT = fromHex("000102030405060708090a0b0c")` | - |
| JV-042 | S06 | `mat` | `m.hkdf-info` | 66:33 | 66:76 | [2666, 2709) | [2666, 2709) | 43 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `HKDF_INFO = fromHex("f0f1f2f3f4f5f6f7f8f9")` | - |
| JV-043 | S07 | `mat` | `m.pbkdf2-password` | 68:33 | 68:61 | [2778, 2806) | [2778, 2806) | 28 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `PBKDF2_PASSWORD = "Password"` | - |
| JV-044 | S07 | `mat` | `m.pbkdf2-salt` | 69:33 | 69:60 | [2840, 2867) | [2840, 2867) | 27 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `PBKDF2_SALT = ascii("NaCl")` | - |
| JV-045 | S08 | `mat` | `m.scrypt-password` | 70:33 | 70:73 | [2901, 2941) | [2901, 2941) | 40 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `SCRYPT_PASSWORD = ascii("pleaseletmein")` | - |
| JV-046 | S08 | `mat` | `m.scrypt-salt` | 71:33 | 71:70 | [2975, 3012) | [2975, 3012) | 37 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `SCRYPT_SALT = ascii("SodiumChloride")` | - |
| JV-047 | S09 | `mat` | `m.password` | 72:33 | 72:74 | [3046, 3087) | [3046, 3087) | 41 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `PASSWORD = "correct horse battery staple"` | - |
| JV-048 | S09 | `mat` | `m.argon2-salt` | 73:33 | 73:72 | [3121, 3160) | [3121, 3160) | 39 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `ARGON2_SALT = ascii("cbom-corpus-salt")` | - |
| JV-049 | S11 | `mat` | `m.gcm-key` | 75:33 | 75:118 | [3232, 3317) | [3232, 3317) | 85 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `GCM_KEY = fromHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")` | - |
| JV-050 | S11 | `mat` | `m.gcm-iv` | 76:33 | 76:77 | [3351, 3395) | [3351, 3395) | 44 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `GCM_IV = fromHex("cafebabefacedbaddecaf888")` | - |
| JV-051 | S11 | `mat` | `m.gcm-aad` | 77:33 | 77:94 | [3429, 3490) | [3429, 3490) | 61 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `GCM_AAD = fromHex("feedfacedeadbeeffeedfacedeadbeefabaddad2")` | - |
| JV-052 | S14 | `mat` | `m.ecb-key` | 82:33 | 82:86 | [3772, 3825) | [3772, 3825) | 53 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `ECB_KEY = fromHex("000102030405060708090a0b0c0d0e0f")` | - |
| JV-053 | S19 | `mat` | `m.ed25519-seed` | 85:33 | 85:123 | [3988, 4078) | [3988, 4078) | 90 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `ED25519_SEED = fromHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")` | - |
| JV-054 | S20 | `mat` | `m.session-info` | 86:33 | 86:83 | [4112, 4162) | [4112, 4162) | 50 | 0 | `<class CryptoShowcase>` | - | `lib.jdk` | - | `SESSION_INFO = ascii("cbom-corpus session key v1")` | - |
| JV-055 | shared | `typ` | `csprng` | 89:26 | 89:38 | [4263, 4275) | [4263, 4275) | 12 | 0 | `<class CryptoShowcase>` | `java.security.SecureRandom` | `lib.jdk` | - | `SecureRandom` | - |
| JV-056 | shared | `ctor` | `csprng` | 89:45 | 89:63 | [4282, 4300) | [4282, 4300) | 18 | 0 | `<class CryptoShowcase>` | `java.security.SecureRandom.<init>` | `lib.jdk` | - | `new SecureRandom()` | securerandom-default |
| JV-057 | S01 | `ctor` | `sha-256` | 118:18 | 118:54 | [5159, 5195) | [5159, 5195) | 36 | 0 | `s01Sha256` | `java.security.MessageDigest.getInstance` | `lib.jdk` | - | `MessageDigest.getInstance("SHA-256")` | - |
| JV-058 | S01 | `alg` | `sha-256` | 118:44 | 118:53 | [5185, 5194) | [5185, 5194) | 9 | 1 | `s01Sha256` | - | `lib.jdk` | - | `"SHA-256"` | - |
| JV-059 | S01 | `op:digest` | `sha-256` | 119:38 | 119:56 | [5234, 5252) | [5234, 5252) | 18 | 0 | `s01Sha256` | `java.security.MessageDigest.digest` | `lib.jdk` | - | `md.digest(MESSAGE)` | - |
| JV-060 | S02 | `ctor` | `sha-512` | 124:22 | 124:58 | [5382, 5418) | [5382, 5418) | 36 | 0 | `s02Sha2Sha3Blake2` | `java.security.MessageDigest.getInstance` | `lib.jdk` | - | `MessageDigest.getInstance("SHA-512")` | - |
| JV-061 | S02 | `alg` | `sha-512` | 124:48 | 124:57 | [5408, 5417) | [5408, 5417) | 9 | 1 | `s02Sha2Sha3Blake2` | - | `lib.jdk` | - | `"SHA-512"` | - |
| JV-062 | S02 | `op:digest` | `sha-512` | 125:38 | 125:60 | [5457, 5479) | [5457, 5479) | 22 | 0 | `s02Sha2Sha3Blake2` | `java.security.MessageDigest.digest` | `lib.jdk` | - | `sha512.digest(MESSAGE)` | - |
| JV-063 | S02 | `ctor` | `sha3-256` | 126:20 | 126:57 | [5502, 5539) | [5502, 5539) | 37 | 0 | `s02Sha2Sha3Blake2` | `java.security.MessageDigest.getInstance` | `lib.jdk` | - | `MessageDigest.getInstance("SHA3-256")` | - |
| JV-064 | S02 | `alg` | `sha3-256` | 126:46 | 126:56 | [5528, 5538) | [5528, 5538) | 10 | 1 | `s02Sha2Sha3Blake2` | - | `lib.jdk` | - | `"SHA3-256"` | - |
| JV-065 | S02 | `op:digest` | `sha3-256` | 127:39 | 127:59 | [5579, 5599) | [5579, 5599) | 20 | 0 | `s02Sha2Sha3Blake2` | `java.security.MessageDigest.digest` | `lib.jdk` | - | `sha3.digest(MESSAGE)` | - |
| JV-066 | S02 | `ctor` | `blake2b-512` | 128:21 | 128:43 | [5623, 5645) | [5623, 5645) | 22 | 0 | `s02Sha2Sha3Blake2` | `org.bouncycastle.crypto.digests.Blake2bDigest.<init>` | `lib.bcprov` | - | `new Blake2bDigest(512)` | - |
| JV-067 | S02 | `prm:digest-size-bits` | `blake2b-512` | 128:39 | 128:42 | [5641, 5644) | [5641, 5644) | 3 | 1 | `s02Sha2Sha3Blake2` | - | `lib.bcprov` | - | `512` | - |
| JV-068 | S02 | `op:digest` | `blake2b-512` | 131:9 | 131:30 | [5756, 5777) | [5756, 5777) | 21 | 0 | `s02Sha2Sha3Blake2` | `org.bouncycastle.crypto.digests.Blake2bDigest.doFinal` | `lib.bcprov` | - | `blake.doFinal(out, 0)` | - |
| JV-069 | S03 | `ctor` | `md5` | 137:19 | 137:51 | [5952, 5984) | [5952, 5984) | 32 | 0 | `s03LegacyHashes` | `java.security.MessageDigest.getInstance` | `lib.jdk` | - | `MessageDigest.getInstance("MD5")` | - |
| JV-070 | S03 | `alg` | `md5` | 137:45 | 137:50 | [5978, 5983) | [5978, 5983) | 5 | 1 | `s03LegacyHashes` | - | `lib.jdk` | - | `"MD5"` | - |
| JV-071 | S03 | `op:digest` | `md5` | 138:34 | 138:53 | [6019, 6038) | [6019, 6038) | 19 | 0 | `s03LegacyHashes` | `java.security.MessageDigest.digest` | `lib.jdk` | - | `md5.digest(MESSAGE)` | - |
| JV-072 | S03 | `ctor` | `sha-1` | 139:20 | 139:54 | [6061, 6095) | [6061, 6095) | 34 | 0 | `s03LegacyHashes` | `java.security.MessageDigest.getInstance` | `lib.jdk` | - | `MessageDigest.getInstance("SHA-1")` | - |
| JV-073 | S03 | `alg` | `sha-1` | 139:46 | 139:53 | [6087, 6094) | [6087, 6094) | 7 | 1 | `s03LegacyHashes` | - | `lib.jdk` | - | `"SHA-1"` | - |
| JV-074 | S03 | `op:digest` | `sha-1` | 140:36 | 140:56 | [6132, 6152) | [6132, 6152) | 20 | 0 | `s03LegacyHashes` | `java.security.MessageDigest.digest` | `lib.jdk` | - | `sha1.digest(MESSAGE)` | - |
| JV-075 | S04 | `ctor` | `shake128` | 145:21 | 145:41 | [6263, 6283) | [6263, 6283) | 20 | 0 | `s04Shake128` | `org.bouncycastle.crypto.digests.SHAKEDigest.<init>` | `lib.bcprov` | - | `new SHAKEDigest(128)` | - |
| JV-076 | S04 | `prm:security-strength-bits` | `shake128` | 145:37 | 145:40 | [6279, 6282) | [6279, 6282) | 3 | 1 | `s04Shake128` | - | `lib.bcprov` | - | `128` | - |
| JV-077 | S04 | `prm:output-length-bytes` | `shake128` | 147:28 | 147:30 | [6362, 6364) | [6362, 6364) | 2 | 0 | `s04Shake128` | - | `lib.jdk` | - | `32` | - |
| JV-078 | S04 | `op:digest` | `shake128` | 148:9 | 148:42 | [6375, 6408) | [6375, 6408) | 33 | 0 | `s04Shake128` | `org.bouncycastle.crypto.digests.SHAKEDigest.doFinal` | `lib.bcprov` | - | `shake.doFinal(out, 0, out.length)` | - |
| JV-079 | S05 | `ctor` | `hmac-sha256` | 154:19 | 154:48 | [6555, 6584) | [6555, 6584) | 29 | 0 | `s05HmacSha256` | `javax.crypto.Mac.getInstance` | `lib.jdk` | - | `Mac.getInstance("HmacSHA256")` | - |
| JV-080 | S05 | `alg` | `hmac-sha256` | 154:35 | 154:47 | [6571, 6583) | [6571, 6583) | 12 | 1 | `s05HmacSha256` | - | `lib.jdk` | - | `"HmacSHA256"` | - |
| JV-081 | S05 | `init` | `hmac-sha256` | 155:9 | 155:60 | [6594, 6645) | [6594, 6645) | 51 | 0 | `s05HmacSha256` | `javax.crypto.Mac.init` | `lib.jdk` | - | `mac.init(new SecretKeySpec(HMAC_KEY, "HmacSHA256"))` | - |
| JV-082 | S05 | `spec` | `hmac-sha256` | 155:18 | 155:59 | [6603, 6644) | [6603, 6644) | 41 | 1 | `s05HmacSha256` | `javax.crypto.spec.SecretKeySpec.<init>` | `lib.jdk` | - | `new SecretKeySpec(HMAC_KEY, "HmacSHA256")` | - |
| JV-083 | S05 | `alg` | `hmac-sha256` | 155:46 | 155:58 | [6631, 6643) | [6631, 6643) | 12 | 2 | `s05HmacSha256` | - | `lib.jdk` | - | `"HmacSHA256"` | key-label |
| JV-084 | S05 | `op:tag` | `hmac-sha256` | 156:42 | 156:62 | [6688, 6708) | [6688, 6708) | 20 | 0 | `s05HmacSha256` | `javax.crypto.Mac.doFinal` | `lib.jdk` | - | `mac.doFinal(MESSAGE)` | - |
| JV-085 | S06 | `ctor` | `hkdf-sha256` | 161:20 | 161:50 | [6851, 6881) | [6851, 6881) | 30 | 0 | `s06HkdfSha256` | `javax.crypto.KDF.getInstance` | `lib.jdk` | - | `KDF.getInstance("HKDF-SHA256")` | - |
| JV-086 | S06 | `alg` | `hkdf-sha256` | 161:36 | 161:49 | [6867, 6880) | [6867, 6880) | 13 | 1 | `s06HkdfSha256` | - | `lib.jdk` | - | `"HKDF-SHA256"` | - |
| JV-087 | S06 | `spec` | `hkdf-sha256` | 162:22 | 165:43 | [6904, 7046) | [6904, 7046) | 142 | 0 | `s06HkdfSha256` | `javax.crypto.spec.HKDFParameterSpec.ofExtract` | `lib.jdk` | - | `HKDFParameterSpec.ofExtract() … (+3 lines)` | - |
| JV-088 | S06 | `prm:output-length-bytes` | `hkdf-sha256` | 165:40 | 165:42 | [7043, 7045) | [7043, 7045) | 2 | 1 | `s06HkdfSha256` | - | `lib.jdk` | - | `42` | - |
| JV-089 | S06 | `op:keyderive` | `hkdf-sha256` | 166:42 | 166:65 | [7089, 7112) | [7089, 7112) | 23 | 0 | `s06HkdfSha256` | `javax.crypto.KDF.deriveData` | `lib.jdk` | `m.hkdf-okm` | `hkdf.deriveData(params)` | - |
| JV-090 | S07 | `ctor` | `pbkdf2-hmac-sha256` | 171:23 | 171:75 | [7223, 7275) | [7223, 7275) | 52 | 0 | `s07Pbkdf2` | `javax.crypto.SecretKeyFactory.getInstance` | `lib.jdk` | - | `SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")` | - |
| JV-091 | S07 | `alg` | `pbkdf2-hmac-sha256` | 171:52 | 171:74 | [7252, 7274) | [7252, 7274) | 22 | 1 | `s07Pbkdf2` | - | `lib.jdk` | - | `"PBKDF2WithHmacSHA256"` | - |
| JV-092 | S07 | `spec` | `pbkdf2-hmac-sha256` | 172:20 | 172:91 | [7296, 7367) | [7296, 7367) | 71 | 0 | `s07Pbkdf2` | `javax.crypto.spec.PBEKeySpec.<init>` | `lib.jdk` | - | `new PBEKeySpec(PBKDF2_PASSWORD.toCharArray(), PBKDF2_SALT, 80_000, 512)` | - |
| JV-093 | S07 | `prm:iterations` | `pbkdf2-hmac-sha256` | 172:79 | 172:85 | [7355, 7361) | [7355, 7361) | 6 | 1 | `s07Pbkdf2` | - | `lib.jdk` | - | `80_000` | - |
| JV-094 | S07 | `prm:output-length-bits` | `pbkdf2-hmac-sha256` | 172:87 | 172:90 | [7363, 7366) | [7363, 7366) | 3 | 1 | `s07Pbkdf2` | - | `lib.jdk` | - | `512` | - |
| JV-095 | S07 | `op:keyderive` | `pbkdf2-hmac-sha256` | 173:23 | 173:51 | [7391, 7419) | [7391, 7419) | 28 | 0 | `s07Pbkdf2` | `javax.crypto.SecretKeyFactory.generateSecret` | `lib.jdk` | `m.pbkdf2-dk` | `factory.generateSecret(spec)` | - |
| JV-096 | S08 | `op:keyderive` | `scrypt` | 179:23 | 179:87 | [7566, 7630) | [7566, 7630) | 64 | 0 | `s08Scrypt` | `org.bouncycastle.crypto.generators.SCrypt.generate` | `lib.bcprov` | `m.scrypt-dk` | `SCrypt.generate(SCRYPT_PASSWORD, SCRYPT_SALT, 1 << 14, 8, 1, 64)` | - |
| JV-097 | S08 | `prm:N` | `scrypt` | 179:69 | 179:76 | [7612, 7619) | [7612, 7619) | 7 | 1 | `s08Scrypt` | - | `lib.bcprov` | - | `1 << 14` | computed |
| JV-098 | S08 | `prm:r` | `scrypt` | 179:78 | 179:79 | [7621, 7622) | [7621, 7622) | 1 | 1 | `s08Scrypt` | - | `lib.bcprov` | - | `8` | - |
| JV-099 | S08 | `prm:p` | `scrypt` | 179:81 | 179:82 | [7624, 7625) | [7624, 7625) | 1 | 1 | `s08Scrypt` | - | `lib.bcprov` | - | `1` | - |
| JV-100 | S08 | `prm:output-length-bytes` | `scrypt` | 179:84 | 179:86 | [7627, 7629) | [7627, 7629) | 2 | 1 | `s08Scrypt` | - | `lib.bcprov` | - | `64` | - |
| JV-101 | S09 | `spec` | `argon2id` | 185:22 | 191:25 | [7760, 8056) | [7760, 8056) | 296 | 0 | `s09Argon2id` | `org.bouncycastle.crypto.params.Argon2Parameters.Builder` | `lib.bcprov` | - | `new Argon2Parameters.Builder(Argon2Parameters.ARGON2_id) … (+6 lines)` | - |
| JV-102 | S09 | `alg` | `argon2id` | 185:51 | 185:77 | [7789, 7815) | [7789, 7815) | 26 | 1 | `s09Argon2id` | `org.bouncycastle.crypto.params.Argon2Parameters.ARGON2_id` | `lib.bcprov` | - | `Argon2Parameters.ARGON2_id` | - |
| JV-103 | S09 | `prm:version` | `argon2id` | 186:30 | 186:64 | [7846, 7880) | [7846, 7880) | 34 | 1 | `s09Argon2id` | `org.bouncycastle.crypto.params.Argon2Parameters.ARGON2_VERSION_13` | `lib.bcprov` | - | `Argon2Parameters.ARGON2_VERSION_13` | - |
| JV-104 | S09 | `prm:iterations` | `argon2id` | 187:33 | 187:34 | [7914, 7915) | [7914, 7915) | 1 | 1 | `s09Argon2id` | - | `lib.bcprov` | - | `2` | - |
| JV-105 | S09 | `prm:memory-kib` | `argon2id` | 188:33 | 188:39 | [7949, 7955) | [7949, 7955) | 6 | 1 | `s09Argon2id` | - | `lib.bcprov` | - | `19_456` | - |
| JV-106 | S09 | `prm:parallelism` | `argon2id` | 189:34 | 189:35 | [7990, 7991) | [7990, 7991) | 1 | 1 | `s09Argon2id` | - | `lib.bcprov` | - | `1` | - |
| JV-107 | S09 | `ctor` | `argon2id` | 192:25 | 192:51 | [8082, 8108) | [8082, 8108) | 26 | 0 | `s09Argon2id` | `org.bouncycastle.crypto.generators.Argon2BytesGenerator.<init>` | `lib.bcprov` | - | `new Argon2BytesGenerator()` | - |
| JV-108 | S09 | `init` | `argon2id` | 193:9 | 193:31 | [8118, 8140) | [8118, 8140) | 22 | 0 | `s09Argon2id` | `org.bouncycastle.crypto.generators.Argon2BytesGenerator.init` | `lib.bcprov` | - | `generator.init(params)` | - |
| JV-109 | S09 | `prm:output-length-bytes` | `argon2id` | 194:28 | 194:30 | [8169, 8171) | [8169, 8171) | 2 | 0 | `s09Argon2id` | - | `lib.jdk` | - | `32` | - |
| JV-110 | S09 | `op:keyderive` | `argon2id` | 195:9 | 195:54 | [8182, 8227) | [8182, 8227) | 45 | 0 | `s09Argon2id` | `org.bouncycastle.crypto.generators.Argon2BytesGenerator.generateBytes` | `lib.bcprov` | `m.argon2-dk` | `generator.generateBytes(ascii(PASSWORD), out)` | - |
| JV-111 | S10 | `prm:length-bytes` | `m.bcrypt-salt` | 201:29 | 201:31 | [8358, 8360) | [8358, 8360) | 2 | 0 | `s10Bcrypt` | - | `lib.jdk` | - | `16` | - |
| JV-112 | S10 | `op:generate` | `csprng` | 202:9 | 202:28 | [8371, 8390) | [8371, 8390) | 19 | 0 | `s10Bcrypt` | `java.security.SecureRandom.nextBytes` | `lib.jdk` | `m.bcrypt-salt` | `RNG.nextBytes(salt)` | - |
| JV-113 | S10 | `op:keyderive` | `bcrypt` | 203:20 | 203:82 | [8411, 8473) | [8411, 8473) | 62 | 0 | `s10Bcrypt` | `org.bouncycastle.crypto.generators.OpenBSDBCrypt.generate` | `lib.bcprov` | `m.bcrypt-hash` | `OpenBSDBCrypt.generate("2b", PASSWORD.toCharArray(), salt, 12)` | - |
| JV-114 | S10 | `alg` | `bcrypt` | 203:43 | 203:47 | [8434, 8438) | [8434, 8438) | 4 | 1 | `s10Bcrypt` | - | `lib.bcprov` | - | `"2b"` | bcrypt-version |
| JV-115 | S10 | `prm:cost` | `bcrypt` | 203:79 | 203:81 | [8470, 8472) | [8470, 8472) | 2 | 1 | `s10Bcrypt` | - | `lib.bcprov` | - | `12` | - |
| JV-116 | S10 | `op:verify` | `bcrypt` | 204:18 | 204:75 | [8492, 8549) | [8492, 8549) | 57 | 0 | `s10Bcrypt` | `org.bouncycastle.crypto.generators.OpenBSDBCrypt.checkPassword` | `lib.bcprov` | - | `OpenBSDBCrypt.checkPassword(hash, PASSWORD.toCharArray())` | - |
| JV-117 | S11 | `spec` | `aes-256-gcm` | 210:19 | 210:52 | [8715, 8748) | [8715, 8748) | 33 | 0 | `s11Aes256Gcm` | `javax.crypto.spec.SecretKeySpec.<init>` | `lib.jdk` | - | `new SecretKeySpec(GCM_KEY, "AES")` | keysize-from-key |
| JV-118 | S11 | `alg` | `aes-256-gcm` | 210:46 | 210:51 | [8742, 8747) | [8742, 8747) | 5 | 1 | `s11Aes256Gcm` | - | `lib.jdk` | - | `"AES"` | - |
| JV-119 | S11 | `spec` | `aes-256-gcm` | 211:19 | 211:52 | [8768, 8801) | [8768, 8801) | 33 | 0 | `s11Aes256Gcm` | `javax.crypto.spec.GCMParameterSpec.<init>` | `lib.jdk` | - | `new GCMParameterSpec(128, GCM_IV)` | - |
| JV-120 | S11 | `prm:tag-length-bits` | `aes-256-gcm` | 211:40 | 211:43 | [8789, 8792) | [8789, 8792) | 3 | 1 | `s11Aes256Gcm` | - | `lib.jdk` | - | `128` | - |
| JV-121 | S11 | `ctor` | `aes-256-gcm` | 212:25 | 212:64 | [8827, 8866) | [8827, 8866) | 39 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/GCM/NoPadding")` | - |
| JV-122 | S11 | `alg` | `aes-256-gcm` | 212:44 | 212:63 | [8846, 8865) | [8846, 8865) | 19 | 1 | `s11Aes256Gcm` | - | `lib.jdk` | - | `"AES/GCM/NoPadding"` | - |
| JV-123 | S11 | `init:encrypt` | `aes-256-gcm` | 213:9 | 213:54 | [8876, 8921) | [8876, 8921) | 45 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, key, gcm)` | - |
| JV-124 | S11 | `op:encrypt` | `aes-256-gcm` | 215:22 | 215:54 | [8982, 9014) | [8982, 9014) | 32 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(GCM_PLAINTEXT)` | - |
| JV-125 | S11 | `ctor` | `aes-256-gcm` | 216:25 | 216:64 | [9040, 9079) | [9040, 9079) | 39 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/GCM/NoPadding")` | - |
| JV-126 | S11 | `alg` | `aes-256-gcm` | 216:44 | 216:63 | [9059, 9078) | [9059, 9078) | 19 | 1 | `s11Aes256Gcm` | - | `lib.jdk` | - | `"AES/GCM/NoPadding"` | - |
| JV-127 | S11 | `init:decrypt` | `aes-256-gcm` | 217:9 | 217:54 | [9089, 9134) | [9089, 9134) | 45 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, key, gcm)` | - |
| JV-128 | S11 | `op:decrypt` | `aes-256-gcm` | 219:22 | 219:47 | [9195, 9220) | [9195, 9220) | 25 | 0 | `s11Aes256Gcm` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(sealed)` | - |
| JV-129 | S12 | `ctor` | `chacha20-poly1305` | 228:28 | 228:64 | [9668, 9704) | [9668, 9704) | 36 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.KeyGenerator.getInstance` | `lib.jdk` | - | `KeyGenerator.getInstance("ChaCha20")` | - |
| JV-130 | S12 | `alg` | `chacha20-poly1305` | 228:53 | 228:63 | [9693, 9703) | [9693, 9703) | 10 | 1 | `s12ChaCha20Poly1305` | - | `lib.jdk` | - | `"ChaCha20"` | - |
| JV-131 | S12 | `op:keygen` | `chacha20-poly1305` | 229:19 | 229:45 | [9724, 9750) | [9724, 9750) | 26 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.KeyGenerator.generateKey` | `lib.jdk` | `m.chacha-key` | `keyGenerator.generateKey()` | keygen-default-random |
| JV-132 | S12 | `prm:length-bytes` | `m.chacha-nonce` | 230:30 | 230:32 | [9781, 9783) | [9781, 9783) | 2 | 0 | `s12ChaCha20Poly1305` | - | `lib.jdk` | - | `12` | - |
| JV-133 | S12 | `op:generate` | `csprng` | 231:9 | 231:29 | [9794, 9814) | [9794, 9814) | 20 | 0 | `s12ChaCha20Poly1305` | `java.security.SecureRandom.nextBytes` | `lib.jdk` | `m.chacha-nonce` | `RNG.nextBytes(nonce)` | - |
| JV-134 | S12 | `ctor` | `chacha20-poly1305` | 232:25 | 232:64 | [9840, 9879) | [9840, 9879) | 39 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("ChaCha20-Poly1305")` | - |
| JV-135 | S12 | `alg` | `chacha20-poly1305` | 232:44 | 232:63 | [9859, 9878) | [9859, 9878) | 19 | 1 | `s12ChaCha20Poly1305` | - | `lib.jdk` | - | `"ChaCha20-Poly1305"` | - |
| JV-136 | S12 | `init:encrypt` | `chacha20-poly1305` | 233:9 | 233:77 | [9889, 9957) | [9889, 9957) | 68 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(nonce))` | - |
| JV-137 | S12 | `spec` | `chacha20-poly1305` | 233:50 | 233:76 | [9930, 9956) | [9930, 9956) | 26 | 1 | `s12ChaCha20Poly1305` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(nonce)` | - |
| JV-138 | S12 | `op:encrypt` | `chacha20-poly1305` | 234:22 | 234:48 | [9980, 10006) | [9980, 10006) | 26 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(MESSAGE)` | - |
| JV-139 | S12 | `ctor` | `chacha20-poly1305` | 235:25 | 235:64 | [10032, 10071) | [10032, 10071) | 39 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("ChaCha20-Poly1305")` | - |
| JV-140 | S12 | `alg` | `chacha20-poly1305` | 235:44 | 235:63 | [10051, 10070) | [10051, 10070) | 19 | 1 | `s12ChaCha20Poly1305` | - | `lib.jdk` | - | `"ChaCha20-Poly1305"` | - |
| JV-141 | S12 | `init:decrypt` | `chacha20-poly1305` | 236:9 | 236:77 | [10081, 10149) | [10081, 10149) | 68 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(nonce))` | - |
| JV-142 | S12 | `spec` | `chacha20-poly1305` | 236:50 | 236:76 | [10122, 10148) | [10122, 10148) | 26 | 1 | `s12ChaCha20Poly1305` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(nonce)` | - |
| JV-143 | S12 | `op:decrypt` | `chacha20-poly1305` | 237:22 | 237:47 | [10172, 10197) | [10172, 10197) | 25 | 0 | `s12ChaCha20Poly1305` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(sealed)` | - |
| JV-144 | S13 | `ctor` | `aes-256-cbc` | 243:28 | 243:59 | [10416, 10447) | [10416, 10447) | 31 | 0 | `s13Aes256Cbc` | `javax.crypto.KeyGenerator.getInstance` | `lib.jdk` | - | `KeyGenerator.getInstance("AES")` | - |
| JV-145 | S13 | `alg` | `aes-256-cbc` | 243:53 | 243:58 | [10441, 10446) | [10441, 10446) | 5 | 1 | `s13Aes256Cbc` | - | `lib.jdk` | - | `"AES"` | aes-keygen-label |
| JV-146 | S13 | `init` | `aes-256-cbc` | 244:9 | 244:31 | [10457, 10479) | [10457, 10479) | 22 | 0 | `s13Aes256Cbc` | `javax.crypto.KeyGenerator.init` | `lib.jdk` | - | `keyGenerator.init(256)` | - |
| JV-147 | S13 | `prm:key-size-bits` | `aes-256-cbc` | 244:27 | 244:30 | [10475, 10478) | [10475, 10478) | 3 | 1 | `s13Aes256Cbc` | - | `lib.jdk` | - | `256` | - |
| JV-148 | S13 | `op:keygen` | `aes-256-cbc` | 245:19 | 245:45 | [10499, 10525) | [10499, 10525) | 26 | 0 | `s13Aes256Cbc` | `javax.crypto.KeyGenerator.generateKey` | `lib.jdk` | `m.cbc-key` | `keyGenerator.generateKey()` | keygen-default-random |
| JV-149 | S13 | `prm:length-bytes` | `m.cbc-iv` | 246:27 | 246:29 | [10553, 10555) | [10553, 10555) | 2 | 0 | `s13Aes256Cbc` | - | `lib.jdk` | - | `16` | - |
| JV-150 | S13 | `op:generate` | `csprng` | 247:9 | 247:26 | [10566, 10583) | [10566, 10583) | 17 | 0 | `s13Aes256Cbc` | `java.security.SecureRandom.nextBytes` | `lib.jdk` | `m.cbc-iv` | `RNG.nextBytes(iv)` | - |
| JV-151 | S13 | `ctor` | `aes-256-cbc` | 248:25 | 248:67 | [10609, 10651) | [10609, 10651) | 42 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/CBC/PKCS5Padding")` | - |
| JV-152 | S13 | `alg` | `aes-256-cbc` | 248:44 | 248:66 | [10628, 10650) | [10628, 10650) | 22 | 1 | `s13Aes256Cbc` | - | `lib.jdk` | - | `"AES/CBC/PKCS5Padding"` | pkcs5-is-pkcs7 |
| JV-153 | S13 | `init:encrypt` | `aes-256-cbc` | 249:9 | 249:74 | [10661, 10726) | [10661, 10726) | 65 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv))` | - |
| JV-154 | S13 | `spec` | `aes-256-cbc` | 249:50 | 249:73 | [10702, 10725) | [10702, 10725) | 23 | 1 | `s13Aes256Cbc` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(iv)` | - |
| JV-155 | S13 | `op:encrypt` | `aes-256-cbc` | 250:26 | 250:52 | [10753, 10779) | [10753, 10779) | 26 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(MESSAGE)` | - |
| JV-156 | S13 | `ctor` | `aes-256-cbc` | 251:25 | 251:67 | [10805, 10847) | [10805, 10847) | 42 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/CBC/PKCS5Padding")` | - |
| JV-157 | S13 | `alg` | `aes-256-cbc` | 251:44 | 251:66 | [10824, 10846) | [10824, 10846) | 22 | 1 | `s13Aes256Cbc` | - | `lib.jdk` | - | `"AES/CBC/PKCS5Padding"` | pkcs5-is-pkcs7 |
| JV-158 | S13 | `init:decrypt` | `aes-256-cbc` | 252:9 | 252:74 | [10857, 10922) | [10857, 10922) | 65 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv))` | - |
| JV-159 | S13 | `spec` | `aes-256-cbc` | 252:50 | 252:73 | [10898, 10921) | [10898, 10921) | 23 | 1 | `s13Aes256Cbc` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(iv)` | - |
| JV-160 | S13 | `op:decrypt` | `aes-256-cbc` | 253:25 | 253:54 | [10948, 10977) | [10948, 10977) | 29 | 0 | `s13Aes256Cbc` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(ciphertext)` | - |
| JV-161 | S14 | `ctor` | `aes-128-ecb` | 259:25 | 259:67 | [11213, 11255) | [11213, 11255) | 42 | 0 | `s14Aes128Ecb` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/ECB/PKCS5Padding")` | - |
| JV-162 | S14 | `alg` | `aes-128-ecb` | 259:44 | 259:66 | [11232, 11254) | [11232, 11254) | 22 | 1 | `s14Aes128Ecb` | - | `lib.jdk` | - | `"AES/ECB/PKCS5Padding"` | pkcs5-is-pkcs7 |
| JV-163 | S14 | `init:encrypt` | `aes-128-ecb` | 260:9 | 260:79 | [11265, 11335) | [11265, 11335) | 70 | 0 | `s14Aes128Ecb` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(ECB_KEY, "AES"))` | - |
| JV-164 | S14 | `spec` | `aes-128-ecb` | 260:45 | 260:78 | [11301, 11334) | [11301, 11334) | 33 | 1 | `s14Aes128Ecb` | `javax.crypto.spec.SecretKeySpec.<init>` | `lib.jdk` | - | `new SecretKeySpec(ECB_KEY, "AES")` | keysize-from-key |
| JV-165 | S14 | `alg` | `aes-128-ecb` | 260:72 | 260:77 | [11328, 11333) | [11328, 11333) | 5 | 2 | `s14Aes128Ecb` | - | `lib.jdk` | - | `"AES"` | - |
| JV-166 | S14 | `op:encrypt` | `aes-128-ecb` | 261:42 | 261:74 | [11378, 11410) | [11378, 11410) | 32 | 0 | `s14Aes128Ecb` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(ECB_PLAINTEXT)` | - |
| JV-167 | S15 | `ctor` | `aes-256-ctr` | 266:28 | 266:59 | [11522, 11553) | [11522, 11553) | 31 | 0 | `s15Aes256Ctr` | `javax.crypto.KeyGenerator.getInstance` | `lib.jdk` | - | `KeyGenerator.getInstance("AES")` | - |
| JV-168 | S15 | `alg` | `aes-256-ctr` | 266:53 | 266:58 | [11547, 11552) | [11547, 11552) | 5 | 1 | `s15Aes256Ctr` | - | `lib.jdk` | - | `"AES"` | aes-keygen-label |
| JV-169 | S15 | `init` | `aes-256-ctr` | 267:9 | 267:31 | [11563, 11585) | [11563, 11585) | 22 | 0 | `s15Aes256Ctr` | `javax.crypto.KeyGenerator.init` | `lib.jdk` | - | `keyGenerator.init(256)` | - |
| JV-170 | S15 | `prm:key-size-bits` | `aes-256-ctr` | 267:27 | 267:30 | [11581, 11584) | [11581, 11584) | 3 | 1 | `s15Aes256Ctr` | - | `lib.jdk` | - | `256` | - |
| JV-171 | S15 | `op:keygen` | `aes-256-ctr` | 268:19 | 268:45 | [11605, 11631) | [11605, 11631) | 26 | 0 | `s15Aes256Ctr` | `javax.crypto.KeyGenerator.generateKey` | `lib.jdk` | `m.ctr-key` | `keyGenerator.generateKey()` | keygen-default-random |
| JV-172 | S15 | `prm:length-bytes` | `m.ctr-iv` | 269:37 | 269:39 | [11669, 11671) | [11669, 11671) | 2 | 0 | `s15Aes256Ctr` | - | `lib.jdk` | - | `16` | - |
| JV-173 | S15 | `op:generate` | `csprng` | 270:9 | 270:36 | [11682, 11709) | [11682, 11709) | 27 | 0 | `s15Aes256Ctr` | `java.security.SecureRandom.nextBytes` | `lib.jdk` | `m.ctr-iv` | `RNG.nextBytes(counterBlock)` | - |
| JV-174 | S15 | `ctor` | `aes-256-ctr` | 271:25 | 271:64 | [11735, 11774) | [11735, 11774) | 39 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/CTR/NoPadding")` | - |
| JV-175 | S15 | `alg` | `aes-256-ctr` | 271:44 | 271:63 | [11754, 11773) | [11754, 11773) | 19 | 1 | `s15Aes256Ctr` | - | `lib.jdk` | - | `"AES/CTR/NoPadding"` | - |
| JV-176 | S15 | `init:encrypt` | `aes-256-ctr` | 272:9 | 272:84 | [11784, 11859) | [11784, 11859) | 75 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(counterBlock))` | - |
| JV-177 | S15 | `spec` | `aes-256-ctr` | 272:50 | 272:83 | [11825, 11858) | [11825, 11858) | 33 | 1 | `s15Aes256Ctr` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(counterBlock)` | - |
| JV-178 | S15 | `op:encrypt` | `aes-256-ctr` | 273:26 | 273:52 | [11886, 11912) | [11886, 11912) | 26 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(MESSAGE)` | - |
| JV-179 | S15 | `ctor` | `aes-256-ctr` | 274:25 | 274:64 | [11938, 11977) | [11938, 11977) | 39 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("AES/CTR/NoPadding")` | - |
| JV-180 | S15 | `alg` | `aes-256-ctr` | 274:44 | 274:63 | [11957, 11976) | [11957, 11976) | 19 | 1 | `s15Aes256Ctr` | - | `lib.jdk` | - | `"AES/CTR/NoPadding"` | - |
| JV-181 | S15 | `init:decrypt` | `aes-256-ctr` | 275:9 | 275:84 | [11987, 12062) | [11987, 12062) | 75 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(counterBlock))` | - |
| JV-182 | S15 | `spec` | `aes-256-ctr` | 275:50 | 275:83 | [12028, 12061) | [12028, 12061) | 33 | 1 | `s15Aes256Ctr` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(counterBlock)` | - |
| JV-183 | S15 | `op:decrypt` | `aes-256-ctr` | 276:25 | 276:54 | [12088, 12117) | [12088, 12117) | 29 | 0 | `s15Aes256Ctr` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(ciphertext)` | - |
| JV-184 | S16 | `ctor` | `3des-cbc` | 282:28 | 282:62 | [12337, 12371) | [12337, 12371) | 34 | 0 | `s16TdeaCbc` | `javax.crypto.KeyGenerator.getInstance` | `lib.jdk` | - | `KeyGenerator.getInstance("DESede")` | - |
| JV-185 | S16 | `alg` | `3des-cbc` | 282:53 | 282:61 | [12362, 12370) | [12362, 12370) | 8 | 1 | `s16TdeaCbc` | - | `lib.jdk` | - | `"DESede"` | - |
| JV-186 | S16 | `op:keygen` | `3des-cbc` | 283:19 | 283:45 | [12391, 12417) | [12391, 12417) | 26 | 0 | `s16TdeaCbc` | `javax.crypto.KeyGenerator.generateKey` | `lib.jdk` | `m.tdes-key` | `keyGenerator.generateKey()` | desede-default-size |
| JV-187 | S16 | `prm:length-bytes` | `m.tdes-iv` | 284:27 | 284:28 | [12445, 12446) | [12445, 12446) | 1 | 0 | `s16TdeaCbc` | - | `lib.jdk` | - | `8` | - |
| JV-188 | S16 | `op:generate` | `csprng` | 285:9 | 285:26 | [12457, 12474) | [12457, 12474) | 17 | 0 | `s16TdeaCbc` | `java.security.SecureRandom.nextBytes` | `lib.jdk` | `m.tdes-iv` | `RNG.nextBytes(iv)` | - |
| JV-189 | S16 | `ctor` | `3des-cbc` | 286:25 | 286:70 | [12500, 12545) | [12500, 12545) | 45 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("DESede/CBC/PKCS5Padding")` | - |
| JV-190 | S16 | `alg` | `3des-cbc` | 286:44 | 286:69 | [12519, 12544) | [12519, 12544) | 25 | 1 | `s16TdeaCbc` | - | `lib.jdk` | - | `"DESede/CBC/PKCS5Padding"` | pkcs5-is-pkcs7 |
| JV-191 | S16 | `init:encrypt` | `3des-cbc` | 287:9 | 287:74 | [12555, 12620) | [12555, 12620) | 65 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv))` | - |
| JV-192 | S16 | `spec` | `3des-cbc` | 287:50 | 287:73 | [12596, 12619) | [12596, 12619) | 23 | 1 | `s16TdeaCbc` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(iv)` | - |
| JV-193 | S16 | `op:encrypt` | `3des-cbc` | 288:26 | 288:52 | [12647, 12673) | [12647, 12673) | 26 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(MESSAGE)` | - |
| JV-194 | S16 | `ctor` | `3des-cbc` | 289:25 | 289:70 | [12699, 12744) | [12699, 12744) | 45 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("DESede/CBC/PKCS5Padding")` | - |
| JV-195 | S16 | `alg` | `3des-cbc` | 289:44 | 289:69 | [12718, 12743) | [12718, 12743) | 25 | 1 | `s16TdeaCbc` | - | `lib.jdk` | - | `"DESede/CBC/PKCS5Padding"` | pkcs5-is-pkcs7 |
| JV-196 | S16 | `init:decrypt` | `3des-cbc` | 290:9 | 290:74 | [12754, 12819) | [12754, 12819) | 65 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv))` | - |
| JV-197 | S16 | `spec` | `3des-cbc` | 290:50 | 290:73 | [12795, 12818) | [12795, 12818) | 23 | 1 | `s16TdeaCbc` | `javax.crypto.spec.IvParameterSpec.<init>` | `lib.jdk` | - | `new IvParameterSpec(iv)` | - |
| JV-198 | S16 | `op:decrypt` | `3des-cbc` | 291:25 | 291:54 | [12845, 12874) | [12845, 12874) | 29 | 0 | `s16TdeaCbc` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(ciphertext)` | - |
| JV-199 | S17 | `ctor` | `rsa-3072` | 297:25 | 297:60 | [13105, 13140) | [13105, 13140) | 35 | 0 | `s17Rsa3072` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("RSA")` | - |
| JV-200 | S17 | `alg` | `rsa-3072` | 297:54 | 297:59 | [13134, 13139) | [13134, 13139) | 5 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"RSA"` | - |
| JV-201 | S17 | `init` | `rsa-3072` | 298:9 | 298:90 | [13150, 13231) | [13150, 13231) | 81 | 0 | `s17Rsa3072` | `java.security.KeyPairGenerator.initialize` | `lib.jdk` | - | `generator.initialize(new RSAKeyGenParameterSpec(3072, RSAKeyGenParameterSpec.F4))` | - |
| JV-202 | S17 | `spec` | `rsa-3072` | 298:30 | 298:89 | [13171, 13230) | [13171, 13230) | 59 | 1 | `s17Rsa3072` | `java.security.spec.RSAKeyGenParameterSpec.<init>` | `lib.jdk` | - | `new RSAKeyGenParameterSpec(3072, RSAKeyGenParameterSpec.F4)` | - |
| JV-203 | S17 | `prm:key-size-bits` | `rsa-3072` | 298:57 | 298:61 | [13198, 13202) | [13198, 13202) | 4 | 2 | `s17Rsa3072` | - | `lib.jdk` | - | `3072` | - |
| JV-204 | S17 | `prm:public-exponent` | `rsa-3072` | 298:63 | 298:88 | [13204, 13229) | [13204, 13229) | 25 | 2 | `s17Rsa3072` | `java.security.spec.RSAKeyGenParameterSpec.F4` | `lib.jdk` | - | `RSAKeyGenParameterSpec.F4` | - |
| JV-205 | S17 | `op:keygen` | `rsa-3072` | 299:23 | 299:50 | [13255, 13282) | [13255, 13282) | 27 | 0 | `s17Rsa3072` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.rsa-private-key`, `m.rsa-public-key` | `generator.generateKeyPair()` | - |
| JV-206 | S17 | `spec` | `rsa-oaep-sha256` | 301:20 | 302:89 | [13304, 13415) | [13304, 13415) | 111 | 0 | `s17Rsa3072` | `javax.crypto.spec.OAEPParameterSpec.<init>` | `lib.jdk` | - | `new OAEPParameterSpec( … (+1 lines)` | oaep-explicit |
| JV-207 | S17 | `alg` | `sha-256` ^`rsa-oaep-sha256` | 302:17 | 302:26 | [13343, 13352) | [13343, 13352) | 9 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"SHA-256"` | - |
| JV-208 | S17 | `alg` | `mgf1-sha256` ^`rsa-oaep-sha256` | 302:28 | 302:34 | [13354, 13360) | [13354, 13360) | 6 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"MGF1"` | - |
| JV-209 | S17 | `alg` | `sha-256` ^`mgf1-sha256` | 302:36 | 302:60 | [13362, 13386) | [13362, 13386) | 24 | 1 | `s17Rsa3072` | `java.security.spec.MGF1ParameterSpec.SHA256` | `lib.jdk` | - | `MGF1ParameterSpec.SHA256` | - |
| JV-210 | S17 | `ctor` | `rsa-oaep-sha256` | 303:25 | 303:66 | [13441, 13482) | [13441, 13482) | 41 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("RSA/ECB/OAEPPadding")` | - |
| JV-211 | S17 | `alg` | `rsa-oaep-sha256` | 303:44 | 303:65 | [13460, 13481) | [13460, 13481) | 21 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"RSA/ECB/OAEPPadding"` | - |
| JV-212 | S17 | `init:encrypt` | `rsa-oaep-sha256` | 304:9 | 304:71 | [13492, 13554) | [13492, 13554) | 62 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `encryptor.init(Cipher.ENCRYPT_MODE, keyPair.getPublic(), oaep)` | - |
| JV-213 | S17 | `op:encrypt` | `rsa-oaep-sha256` | 305:26 | 305:52 | [13581, 13607) | [13581, 13607) | 26 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `encryptor.doFinal(MESSAGE)` | - |
| JV-214 | S17 | `ctor` | `rsa-oaep-sha256` | 306:25 | 306:66 | [13633, 13674) | [13633, 13674) | 41 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.getInstance` | `lib.jdk` | - | `Cipher.getInstance("RSA/ECB/OAEPPadding")` | - |
| JV-215 | S17 | `alg` | `rsa-oaep-sha256` | 306:44 | 306:65 | [13652, 13673) | [13652, 13673) | 21 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"RSA/ECB/OAEPPadding"` | - |
| JV-216 | S17 | `init:decrypt` | `rsa-oaep-sha256` | 307:9 | 307:72 | [13684, 13747) | [13684, 13747) | 63 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.init` | `lib.jdk` | - | `decryptor.init(Cipher.DECRYPT_MODE, keyPair.getPrivate(), oaep)` | - |
| JV-217 | S17 | `op:decrypt` | `rsa-oaep-sha256` | 308:25 | 308:54 | [13773, 13802) | [13773, 13802) | 29 | 0 | `s17Rsa3072` | `javax.crypto.Cipher.doFinal` | `lib.jdk` | - | `decryptor.doFinal(ciphertext)` | - |
| JV-218 | S17 | `spec` | `rsassa-pss-sha256` | 311:19 | 313:55 | [13911, 14048) | [13911, 14048) | 137 | 0 | `s17Rsa3072` | `java.security.spec.PSSParameterSpec.<init>` | `lib.jdk` | - | `new PSSParameterSpec( … (+2 lines)` | - |
| JV-219 | S17 | `alg` | `sha-256` ^`rsassa-pss-sha256` | 312:17 | 312:26 | [13949, 13958) | [13949, 13958) | 9 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"SHA-256"` | - |
| JV-220 | S17 | `alg` | `mgf1-sha256` ^`rsassa-pss-sha256` | 312:28 | 312:34 | [13960, 13966) | [13960, 13966) | 6 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"MGF1"` | - |
| JV-221 | S17 | `alg` | `sha-256` ^`mgf1-sha256` | 312:36 | 312:60 | [13968, 13992) | [13968, 13992) | 24 | 1 | `s17Rsa3072` | `java.security.spec.MGF1ParameterSpec.SHA256` | `lib.jdk` | - | `MGF1ParameterSpec.SHA256` | - |
| JV-222 | S17 | `prm:salt-length-bytes` | `rsassa-pss-sha256` | 313:17 | 313:19 | [14010, 14012) | [14010, 14012) | 2 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `32` | - |
| JV-223 | S17 | `prm:trailer-field` | `rsassa-pss-sha256` | 313:21 | 313:54 | [14014, 14047) | [14014, 14047) | 33 | 1 | `s17Rsa3072` | `java.security.spec.PSSParameterSpec.TRAILER_FIELD_BC` | `lib.jdk` | - | `PSSParameterSpec.TRAILER_FIELD_BC` | - |
| JV-224 | S17 | `ctor` | `rsassa-pss-sha256` | 314:25 | 314:60 | [14074, 14109) | [14074, 14109) | 35 | 0 | `s17Rsa3072` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("RSASSA-PSS")` | - |
| JV-225 | S17 | `alg` | `rsassa-pss-sha256` | 314:47 | 314:59 | [14096, 14108) | [14096, 14108) | 12 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"RSASSA-PSS"` | - |
| JV-226 | S17 | `init` | `rsassa-pss-sha256` | 315:9 | 315:36 | [14119, 14146) | [14119, 14146) | 27 | 0 | `s17Rsa3072` | `java.security.Signature.setParameter` | `lib.jdk` | - | `pssSigner.setParameter(pss)` | - |
| JV-227 | S17 | `init:sign` | `rsassa-pss-sha256` | 316:9 | 316:49 | [14156, 14196) | [14156, 14196) | 40 | 0 | `s17Rsa3072` | `java.security.Signature.initSign` | `lib.jdk` | - | `pssSigner.initSign(keyPair.getPrivate())` | - |
| JV-228 | S17 | `op:sign` | `rsassa-pss-sha256` | 318:28 | 318:44 | [14260, 14276) | [14260, 14276) | 16 | 0 | `s17Rsa3072` | `java.security.Signature.sign` | `lib.jdk` | - | `pssSigner.sign()` | - |
| JV-229 | S17 | `ctor` | `rsassa-pss-sha256` | 319:27 | 319:62 | [14304, 14339) | [14304, 14339) | 35 | 0 | `s17Rsa3072` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("RSASSA-PSS")` | - |
| JV-230 | S17 | `alg` | `rsassa-pss-sha256` | 319:49 | 319:61 | [14326, 14338) | [14326, 14338) | 12 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"RSASSA-PSS"` | - |
| JV-231 | S17 | `init` | `rsassa-pss-sha256` | 320:9 | 320:38 | [14349, 14378) | [14349, 14378) | 29 | 0 | `s17Rsa3072` | `java.security.Signature.setParameter` | `lib.jdk` | - | `pssVerifier.setParameter(pss)` | - |
| JV-232 | S17 | `init:verify` | `rsassa-pss-sha256` | 321:9 | 321:52 | [14388, 14431) | [14388, 14431) | 43 | 0 | `s17Rsa3072` | `java.security.Signature.initVerify` | `lib.jdk` | - | `pssVerifier.initVerify(keyPair.getPublic())` | - |
| JV-233 | S17 | `op:verify` | `rsassa-pss-sha256` | 323:49 | 323:81 | [14518, 14550) | [14518, 14550) | 32 | 0 | `s17Rsa3072` | `java.security.Signature.verify` | `lib.jdk` | - | `pssVerifier.verify(pssSignature)` | - |
| JV-234 | S17 | `ctor` | `rsassa-pkcs1v15-sha256` | 325:27 | 325:65 | [14580, 14618) | [14580, 14618) | 38 | 0 | `s17Rsa3072` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("SHA256withRSA")` | - |
| JV-235 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 325:49 | 325:64 | [14602, 14617) | [14602, 14617) | 15 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"SHA256withRSA"` | - |
| JV-236 | S17 | `init:sign` | `rsassa-pkcs1v15-sha256` | 326:9 | 326:51 | [14628, 14670) | [14628, 14670) | 42 | 0 | `s17Rsa3072` | `java.security.Signature.initSign` | `lib.jdk` | - | `pkcs1Signer.initSign(keyPair.getPrivate())` | - |
| JV-237 | S17 | `op:sign` | `rsassa-pkcs1v15-sha256` | 328:30 | 328:48 | [14738, 14756) | [14738, 14756) | 18 | 0 | `s17Rsa3072` | `java.security.Signature.sign` | `lib.jdk` | - | `pkcs1Signer.sign()` | - |
| JV-238 | S17 | `ctor` | `rsassa-pkcs1v15-sha256` | 329:29 | 329:67 | [14786, 14824) | [14786, 14824) | 38 | 0 | `s17Rsa3072` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("SHA256withRSA")` | - |
| JV-239 | S17 | `alg` | `rsassa-pkcs1v15-sha256` | 329:51 | 329:66 | [14808, 14823) | [14808, 14823) | 15 | 1 | `s17Rsa3072` | - | `lib.jdk` | - | `"SHA256withRSA"` | - |
| JV-240 | S17 | `init:verify` | `rsassa-pkcs1v15-sha256` | 330:9 | 330:54 | [14834, 14879) | [14834, 14879) | 45 | 0 | `s17Rsa3072` | `java.security.Signature.initVerify` | `lib.jdk` | - | `pkcs1Verifier.initVerify(keyPair.getPublic())` | - |
| JV-241 | S17 | `op:verify` | `rsassa-pkcs1v15-sha256` | 332:54 | 332:90 | [14973, 15009) | [14973, 15009) | 36 | 0 | `s17Rsa3072` | `java.security.Signature.verify` | `lib.jdk` | - | `pkcs1Verifier.verify(pkcs1Signature)` | - |
| JV-242 | S18 | `ctor` | `ecdsa-p256-sha256` | 337:25 | 337:59 | [15130, 15164) | [15130, 15164) | 34 | 0 | `s18EcdsaP256` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("EC")` | - |
| JV-243 | S18 | `alg` | `ecdsa-p256-sha256` | 337:54 | 337:58 | [15159, 15163) | [15159, 15163) | 4 | 1 | `s18EcdsaP256` | - | `lib.jdk` | - | `"EC"` | ec-keygen-label |
| JV-244 | S18 | `init` | `ecdsa-p256-sha256` | 338:9 | 338:66 | [15174, 15231) | [15174, 15231) | 57 | 0 | `s18EcdsaP256` | `java.security.KeyPairGenerator.initialize` | `lib.jdk` | - | `generator.initialize(new ECGenParameterSpec("secp256r1"))` | - |
| JV-245 | S18 | `spec` | `ecdsa-p256-sha256` | 338:30 | 338:65 | [15195, 15230) | [15195, 15230) | 35 | 1 | `s18EcdsaP256` | `java.security.spec.ECGenParameterSpec.<init>` | `lib.jdk` | - | `new ECGenParameterSpec("secp256r1")` | - |
| JV-246 | S18 | `alg` | `ecdsa-p256-sha256` | 338:53 | 338:64 | [15218, 15229) | [15218, 15229) | 11 | 2 | `s18EcdsaP256` | - | `lib.jdk` | - | `"secp256r1"` | curve-alias |
| JV-247 | S18 | `op:keygen` | `ecdsa-p256-sha256` | 339:23 | 339:50 | [15255, 15282) | [15255, 15282) | 27 | 0 | `s18EcdsaP256` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.ecdsa-private-key`, `m.ecdsa-public-key` | `generator.generateKeyPair()` | - |
| JV-248 | S18 | `ctor` | `ecdsa-p256-sha256` | 340:22 | 340:62 | [15305, 15345) | [15305, 15345) | 40 | 0 | `s18EcdsaP256` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("SHA256withECDSA")` | - |
| JV-249 | S18 | `alg` | `ecdsa-p256-sha256` | 340:44 | 340:61 | [15327, 15344) | [15327, 15344) | 17 | 1 | `s18EcdsaP256` | - | `lib.jdk` | - | `"SHA256withECDSA"` | - |
| JV-250 | S18 | `init:sign` | `ecdsa-p256-sha256` | 341:9 | 341:46 | [15355, 15392) | [15355, 15392) | 37 | 0 | `s18EcdsaP256` | `java.security.Signature.initSign` | `lib.jdk` | - | `signer.initSign(keyPair.getPrivate())` | - |
| JV-251 | S18 | `op:sign` | `ecdsa-p256-sha256` | 343:25 | 343:38 | [15450, 15463) | [15450, 15463) | 13 | 0 | `s18EcdsaP256` | `java.security.Signature.sign` | `lib.jdk` | - | `signer.sign()` | - |
| JV-252 | S18 | `ctor` | `ecdsa-p256-sha256` | 344:24 | 344:64 | [15488, 15528) | [15488, 15528) | 40 | 0 | `s18EcdsaP256` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("SHA256withECDSA")` | - |
| JV-253 | S18 | `alg` | `ecdsa-p256-sha256` | 344:46 | 344:63 | [15510, 15527) | [15510, 15527) | 17 | 1 | `s18EcdsaP256` | - | `lib.jdk` | - | `"SHA256withECDSA"` | - |
| JV-254 | S18 | `init:verify` | `ecdsa-p256-sha256` | 345:9 | 345:49 | [15538, 15578) | [15538, 15578) | 40 | 0 | `s18EcdsaP256` | `java.security.Signature.initVerify` | `lib.jdk` | - | `verifier.initVerify(keyPair.getPublic())` | - |
| JV-255 | S18 | `op:verify` | `ecdsa-p256-sha256` | 347:48 | 347:74 | [15661, 15687) | [15661, 15687) | 26 | 0 | `s18EcdsaP256` | `java.security.Signature.verify` | `lib.jdk` | - | `verifier.verify(signature)` | - |
| JV-256 | S19 | `ctor` | `ed25519` | 352:26 | 352:74 | [15802, 15850) | [15802, 15850) | 48 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.params.Ed25519PrivateKeyParameters.<init>` | `lib.bcprov` | - | `new Ed25519PrivateKeyParameters(ED25519_SEED, 0)` | seed-ctor |
| JV-257 | S19 | `op:keygen` | `ed25519` | 353:25 | 353:55 | [15876, 15906) | [15876, 15906) | 30 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.params.Ed25519PrivateKeyParameters.generatePublicKey` | `lib.bcprov` | `m.ed25519-public-key` | `privateKey.generatePublicKey()` | - |
| JV-258 | S19 | `ctor` | `ed25519` | 354:22 | 354:41 | [15929, 15948) | [15929, 15948) | 19 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.<init>` | `lib.bcprov` | - | `new Ed25519Signer()` | - |
| JV-259 | S19 | `init:sign` | `ed25519` | 355:9 | 355:38 | [15958, 15987) | [15958, 15987) | 29 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.init` | `lib.bcprov` | - | `signer.init(true, privateKey)` | - |
| JV-260 | S19 | `op:sign` | `ed25519` | 357:25 | 357:51 | [16064, 16090) | [16064, 16090) | 26 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.generateSignature` | `lib.bcprov` | - | `signer.generateSignature()` | - |
| JV-261 | S19 | `ctor` | `ed25519` | 358:24 | 358:43 | [16115, 16134) | [16115, 16134) | 19 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.<init>` | `lib.bcprov` | - | `new Ed25519Signer()` | - |
| JV-262 | S19 | `init:verify` | `ed25519` | 359:9 | 359:40 | [16144, 16175) | [16144, 16175) | 31 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.init` | `lib.bcprov` | - | `verifier.init(false, publicKey)` | - |
| JV-263 | S19 | `op:verify` | `ed25519` | 361:18 | 361:53 | [16247, 16282) | [16247, 16282) | 35 | 0 | `s19Ed25519` | `org.bouncycastle.crypto.signers.Ed25519Signer.verifySignature` | `lib.bcprov` | - | `verifier.verifySignature(signature)` | - |
| JV-264 | S20 | `ctor` | `x25519` | 366:25 | 366:60 | [16536, 16571) | [16536, 16571) | 35 | 0 | `agree` | `javax.crypto.KeyAgreement.getInstance` | `lib.jdk` | - | `KeyAgreement.getInstance(algorithm)` | polymorphic-site |
| JV-265 | S20 | `ctor` | `ecdh-p256` | 366:25 | 366:60 | [16536, 16571) | [16536, 16571) | 35 | 1 | `agree` | `javax.crypto.KeyAgreement.getInstance` | `lib.jdk` | - | `KeyAgreement.getInstance(algorithm)` | polymorphic-site |
| JV-266 | S20 | `init` | `x25519` | 367:9 | 367:35 | [16581, 16607) | [16581, 16607) | 26 | 0 | `agree` | `javax.crypto.KeyAgreement.init` | `lib.jdk` | - | `agreement.init(privateKey)` | - |
| JV-267 | S20 | `init` | `ecdh-p256` | 367:9 | 367:35 | [16581, 16607) | [16581, 16607) | 26 | 1 | `agree` | `javax.crypto.KeyAgreement.init` | `lib.jdk` | - | `agreement.init(privateKey)` | - |
| JV-268 | S20 | `op:agree` | `x25519` | 369:16 | 369:42 | [16666, 16692) | [16666, 16692) | 26 | 0 | `agree` | `javax.crypto.KeyAgreement.generateSecret` | `lib.jdk` | `m.x25519-shared-secret` | `agreement.generateSecret()` | polymorphic-site |
| JV-269 | S20 | `op:agree` | `ecdh-p256` | 369:16 | 369:42 | [16666, 16692) | [16666, 16692) | 26 | 1 | `agree` | `javax.crypto.KeyAgreement.generateSecret` | `lib.jdk` | `m.ecdh-shared-secret` | `agreement.generateSecret()` | polymorphic-site |
| JV-270 | S20 | `ctor` | `hkdf-sha256` | 373:20 | 373:50 | [16795, 16825) | [16795, 16825) | 30 | 0 | `deriveSessionKey` | `javax.crypto.KDF.getInstance` | `lib.jdk` | - | `KDF.getInstance("HKDF-SHA256")` | - |
| JV-271 | S20 | `alg` | `hkdf-sha256` | 373:36 | 373:49 | [16811, 16824) | [16811, 16824) | 13 | 1 | `deriveSessionKey` | - | `lib.jdk` | - | `"HKDF-SHA256"` | - |
| JV-272 | S20 | `spec` | `hkdf-sha256` | 374:22 | 374:101 | [16848, 16927) | [16848, 16927) | 79 | 0 | `deriveSessionKey` | `javax.crypto.spec.HKDFParameterSpec.ofExtract` | `lib.jdk` | - | `HKDFParameterSpec.ofExtract().addIKM(sharedSecret).thenExpand(SESSION_INFO, 32)` | - |
| JV-273 | S20 | `prm:output-length-bytes` | `hkdf-sha256` | 374:98 | 374:100 | [16924, 16926) | [16924, 16926) | 2 | 1 | `deriveSessionKey` | - | `lib.jdk` | - | `32` | - |
| JV-274 | S20 | `op:keyderive` | `hkdf-sha256` | 375:16 | 375:39 | [16944, 16967) | [16944, 16967) | 23 | 0 | `deriveSessionKey` | `javax.crypto.KDF.deriveData` | `lib.jdk` | `m.session-key` | `hkdf.deriveData(params)` | - |
| JV-275 | S20 | `ctor` | `x25519` | 380:22 | 380:60 | [17114, 17152) | [17114, 17152) | 38 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("X25519")` | - |
| JV-276 | S20 | `alg` | `x25519` | 380:51 | 380:59 | [17143, 17151) | [17143, 17151) | 8 | 1 | `s20KeyAgreement` | - | `lib.jdk` | - | `"X25519"` | - |
| JV-277 | S20 | `op:keygen` | `x25519` | 381:21 | 381:45 | [17174, 17198) | [17174, 17198) | 24 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.x25519-private-key-a` | `x25519.generateKeyPair()` | - |
| JV-278 | S20 | `op:keygen` | `x25519` | 382:19 | 382:43 | [17218, 17242) | [17218, 17242) | 24 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.x25519-private-key-b` | `x25519.generateKeyPair()` | - |
| JV-279 | S20 | `alg` | `x25519` | 383:28 | 383:36 | [17271, 17279) | [17271, 17279) | 8 | 0 | `s20KeyAgreement` | - | `lib.jdk` | - | `"X25519"` | interprocedural |
| JV-280 | S20 | `alg` | `x25519` | 384:26 | 384:34 | [17344, 17352) | [17344, 17352) | 8 | 0 | `s20KeyAgreement` | - | `lib.jdk` | - | `"X25519"` | interprocedural |
| JV-281 | S20 | `ctor` | `ecdh-p256` | 387:18 | 387:52 | [17481, 17515) | [17481, 17515) | 34 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("EC")` | - |
| JV-282 | S20 | `alg` | `ecdh-p256` | 387:47 | 387:51 | [17510, 17514) | [17510, 17514) | 4 | 1 | `s20KeyAgreement` | - | `lib.jdk` | - | `"EC"` | ec-keygen-label |
| JV-283 | S20 | `init` | `ecdh-p256` | 388:9 | 388:59 | [17525, 17575) | [17525, 17575) | 50 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.initialize` | `lib.jdk` | - | `ec.initialize(new ECGenParameterSpec("secp256r1"))` | - |
| JV-284 | S20 | `spec` | `ecdh-p256` | 388:23 | 388:58 | [17539, 17574) | [17539, 17574) | 35 | 1 | `s20KeyAgreement` | `java.security.spec.ECGenParameterSpec.<init>` | `lib.jdk` | - | `new ECGenParameterSpec("secp256r1")` | - |
| JV-285 | S20 | `alg` | `ecdh-p256` | 388:46 | 388:57 | [17562, 17573) | [17562, 17573) | 11 | 2 | `s20KeyAgreement` | - | `lib.jdk` | - | `"secp256r1"` | curve-alias |
| JV-286 | S20 | `op:keygen` | `ecdh-p256` | 389:23 | 389:43 | [17599, 17619) | [17599, 17619) | 20 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.ecdh-private-key-a` | `ec.generateKeyPair()` | - |
| JV-287 | S20 | `op:keygen` | `ecdh-p256` | 390:21 | 390:41 | [17641, 17661) | [17641, 17661) | 20 | 0 | `s20KeyAgreement` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.ecdh-private-key-b` | `ec.generateKeyPair()` | - |
| JV-288 | S20 | `alg` | `ecdh-p256` | 391:28 | 391:34 | [17690, 17696) | [17690, 17696) | 6 | 0 | `s20KeyAgreement` | - | `lib.jdk` | - | `"ECDH"` | interprocedural |
| JV-289 | S20 | `alg` | `ecdh-p256` | 392:26 | 392:32 | [17765, 17771) | [17765, 17771) | 6 | 0 | `s20KeyAgreement` | - | `lib.jdk` | - | `"ECDH"` | interprocedural |
| JV-290 | S21 | `ctor` | `ml-kem-768` | 402:25 | 402:67 | [18230, 18272) | [18230, 18272) | 42 | 0 | `s21MlKem768` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("ML-KEM-768")` | - |
| JV-291 | S21 | `alg` | `ml-kem-768` | 402:54 | 402:66 | [18259, 18271) | [18259, 18271) | 12 | 1 | `s21MlKem768` | - | `lib.jdk` | - | `"ML-KEM-768"` | - |
| JV-292 | S21 | `op:keygen` | `ml-kem-768` | 403:23 | 403:50 | [18296, 18323) | [18296, 18323) | 27 | 0 | `s21MlKem768` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.mlkem-decapsulation-key`, `m.mlkem-encapsulation-key` | `generator.generateKeyPair()` | - |
| JV-293 | S21 | `ctor` | `ml-kem-768` | 404:19 | 404:44 | [18343, 18368) | [18343, 18368) | 25 | 0 | `s21MlKem768` | `javax.crypto.KEM.getInstance` | `lib.jdk` | - | `KEM.getInstance("ML-KEM")` | - |
| JV-294 | S21 | `alg` | `ml-kem-768` | 404:35 | 404:43 | [18359, 18367) | [18359, 18367) | 8 | 1 | `s21MlKem768` | - | `lib.jdk` | - | `"ML-KEM"` | kem-family-name |
| JV-295 | S21 | `op:encapsulate` | `ml-kem-768` | 405:28 | 405:82 | [18397, 18451) | [18397, 18451) | 54 | 0 | `s21MlKem768` | `javax.crypto.KEM.Encapsulator.encapsulate` | `lib.jdk` | `m.mlkem-shared-secret` | `kem.newEncapsulator(keyPair.getPublic()).encapsulate()` | - |
| JV-296 | S21 | `ctor` | `ml-kem-768` | 405:28 | 405:68 | [18397, 18437) | [18397, 18437) | 40 | 1 | `s21MlKem768` | `javax.crypto.KEM.newEncapsulator` | `lib.jdk` | - | `kem.newEncapsulator(keyPair.getPublic())` | - |
| JV-297 | S21 | `op:decapsulate` | `ml-kem-768` | 408:25 | 408:90 | [18592, 18657) | [18592, 18657) | 65 | 0 | `s21MlKem768` | `javax.crypto.KEM.Decapsulator.decapsulate` | `lib.jdk` | `m.mlkem-shared-secret` | `kem.newDecapsulator(keyPair.getPrivate()).decapsulate(ciphertext)` | - |
| JV-298 | S21 | `ctor` | `ml-kem-768` | 408:25 | 408:66 | [18592, 18633) | [18592, 18633) | 41 | 1 | `s21MlKem768` | `javax.crypto.KEM.newDecapsulator` | `lib.jdk` | - | `kem.newDecapsulator(keyPair.getPrivate())` | - |
| JV-299 | S22 | `ctor` | `ml-dsa-65` | 415:25 | 415:66 | [18946, 18987) | [18946, 18987) | 41 | 0 | `s22MlDsa65` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("ML-DSA-65")` | - |
| JV-300 | S22 | `alg` | `ml-dsa-65` | 415:54 | 415:65 | [18975, 18986) | [18975, 18986) | 11 | 1 | `s22MlDsa65` | - | `lib.jdk` | - | `"ML-DSA-65"` | - |
| JV-301 | S22 | `op:keygen` | `ml-dsa-65` | 416:23 | 416:50 | [19011, 19038) | [19011, 19038) | 27 | 0 | `s22MlDsa65` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.mldsa-private-key`, `m.mldsa-public-key` | `generator.generateKeyPair()` | - |
| JV-302 | S22 | `ctor` | `ml-dsa-65` | 417:22 | 417:56 | [19061, 19095) | [19061, 19095) | 34 | 0 | `s22MlDsa65` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("ML-DSA-65")` | - |
| JV-303 | S22 | `alg` | `ml-dsa-65` | 417:44 | 417:55 | [19083, 19094) | [19083, 19094) | 11 | 1 | `s22MlDsa65` | - | `lib.jdk` | - | `"ML-DSA-65"` | - |
| JV-304 | S22 | `init:sign` | `ml-dsa-65` | 418:9 | 418:46 | [19105, 19142) | [19105, 19142) | 37 | 0 | `s22MlDsa65` | `java.security.Signature.initSign` | `lib.jdk` | - | `signer.initSign(keyPair.getPrivate())` | - |
| JV-305 | S22 | `op:sign` | `ml-dsa-65` | 420:25 | 420:38 | [19200, 19213) | [19200, 19213) | 13 | 0 | `s22MlDsa65` | `java.security.Signature.sign` | `lib.jdk` | - | `signer.sign()` | - |
| JV-306 | S22 | `ctor` | `ml-dsa-65` | 421:24 | 421:58 | [19238, 19272) | [19238, 19272) | 34 | 0 | `s22MlDsa65` | `java.security.Signature.getInstance` | `lib.jdk` | - | `Signature.getInstance("ML-DSA-65")` | - |
| JV-307 | S22 | `alg` | `ml-dsa-65` | 421:46 | 421:57 | [19260, 19271) | [19260, 19271) | 11 | 1 | `s22MlDsa65` | - | `lib.jdk` | - | `"ML-DSA-65"` | - |
| JV-308 | S22 | `init:verify` | `ml-dsa-65` | 422:9 | 422:49 | [19282, 19322) | [19282, 19322) | 40 | 0 | `s22MlDsa65` | `java.security.Signature.initVerify` | `lib.jdk` | - | `verifier.initVerify(keyPair.getPublic())` | - |
| JV-309 | S22 | `op:verify` | `ml-dsa-65` | 424:18 | 424:44 | [19375, 19401) | [19375, 19401) | 26 | 0 | `s22MlDsa65` | `java.security.Signature.verify` | `lib.jdk` | - | `verifier.verify(signature)` | - |
| JV-310 | S23 | `ctor` | `ecdsa-p256-sha256` | 430:25 | 430:59 | [19659, 19693) | [19659, 19693) | 34 | 0 | `s23X509SelfSigned` | `java.security.KeyPairGenerator.getInstance` | `lib.jdk` | - | `KeyPairGenerator.getInstance("EC")` | - |
| JV-311 | S23 | `alg` | `ecdsa-p256-sha256` | 430:54 | 430:58 | [19688, 19692) | [19688, 19692) | 4 | 1 | `s23X509SelfSigned` | - | `lib.jdk` | - | `"EC"` | ec-keygen-label |
| JV-312 | S23 | `init` | `ecdsa-p256-sha256` | 431:9 | 431:66 | [19703, 19760) | [19703, 19760) | 57 | 0 | `s23X509SelfSigned` | `java.security.KeyPairGenerator.initialize` | `lib.jdk` | - | `generator.initialize(new ECGenParameterSpec("secp256r1"))` | - |
| JV-313 | S23 | `spec` | `ecdsa-p256-sha256` | 431:30 | 431:65 | [19724, 19759) | [19724, 19759) | 35 | 1 | `s23X509SelfSigned` | `java.security.spec.ECGenParameterSpec.<init>` | `lib.jdk` | - | `new ECGenParameterSpec("secp256r1")` | - |
| JV-314 | S23 | `alg` | `ecdsa-p256-sha256` | 431:53 | 431:64 | [19747, 19758) | [19747, 19758) | 11 | 2 | `s23X509SelfSigned` | - | `lib.jdk` | - | `"secp256r1"` | curve-alias |
| JV-315 | S23 | `op:keygen` | `ecdsa-p256-sha256` | 432:23 | 432:50 | [19784, 19811) | [19784, 19811) | 27 | 0 | `s23X509SelfSigned` | `java.security.KeyPairGenerator.generateKeyPair` | `lib.jdk` | `m.cert-private-key`, `m.cert-public-key` | `generator.generateKeyPair()` | - |
| JV-316 | S23 | `ctor` | `cert.self-signed` | 435:23 | 441:37 | [19926, 20200) | [19926, 20200) | 274 | 0 | `s23X509SelfSigned` | `org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder.<init>` | `lib.bcpkix` | - | `new JcaX509v3CertificateBuilder( … (+6 lines)` | - |
| JV-317 | S23 | `op:generate` | `csprng` | 437:17 | 437:40 | [19997, 20020) | [19997, 20020) | 23 | 1 | `s23X509SelfSigned` | `java.math.BigInteger.<init>` | `lib.jdk` | - | `new BigInteger(64, RNG)` | serial |
| JV-318 | S23 | `prm:validity-days` | `cert.self-signed` | 439:52 | 439:55 | [20134, 20137) | [20134, 20137) | 3 | 1 | `s23X509SelfSigned` | - | `lib.bcpkix` | - | `365` | - |
| JV-319 | S23 | `ctor` | `ecdsa-p256-sha256` | 442:29 | 442:103 | [20230, 20304) | [20230, 20304) | 74 | 0 | `s23X509SelfSigned` | `org.bouncycastle.operator.jcajce.JcaContentSignerBuilder.build` | `lib.bcpkix` | - | `new JcaContentSignerBuilder("SHA256withECDSA").build(keyPair.getPrivate())` | - |
| JV-320 | S23 | `alg` | `ecdsa-p256-sha256` | 442:57 | 442:74 | [20258, 20275) | [20258, 20275) | 17 | 1 | `s23X509SelfSigned` | - | `lib.bcpkix` | - | `"SHA256withECDSA"` | - |
| JV-321 | S23 | `op:encode` | `cert.self-signed` | 443:27 | 443:105 | [20332, 20410) | [20332, 20410) | 78 | 0 | `s23X509SelfSigned` | `org.bouncycastle.cert.jcajce.JcaX509CertificateConverter.getCertificate` | `lib.bcpkix` | - | `new JcaX509CertificateConverter().getCertificate(builder.build(contentSigner))` | - |
| JV-322 | S23 | `op:sign` | `cert.self-signed` | 443:76 | 443:104 | [20381, 20409) | [20381, 20409) | 28 | 1 | `s23X509SelfSigned` | `org.bouncycastle.cert.X509v3CertificateBuilder.build` | `lib.bcpkix` | - | `builder.build(contentSigner)` | - |
| JV-323 | S23 | `op:verify` | `ecdsa-p256-sha256` | 446:13 | 446:59 | [20458, 20504) | [20458, 20504) | 46 | 0 | `s23X509SelfSigned` | `java.security.cert.X509Certificate.verify` | `lib.jdk` | - | `certificate.verify(certificate.getPublicKey())` | - |
| JV-324 | S24 | `ctor` | `tls13-client` | 456:23 | 456:56 | [20833, 20866) | [20833, 20866) | 33 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLContext.getInstance` | `lib.jdk` | - | `SSLContext.getInstance("TLSv1.3")` | - |
| JV-325 | S24 | `alg` | `tls13-client` | 456:46 | 456:55 | [20856, 20865) | [20856, 20865) | 9 | 1 | `s24Tls13Client` | - | `lib.jdk` | - | `"TLSv1.3"` | tls-context-name |
| JV-326 | S24 | `init` | `tls13-client` | 457:9 | 457:39 | [20876, 20906) | [20876, 20906) | 30 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLContext.init` | `lib.jdk` | - | `context.init(null, null, null)` | default-managers |
| JV-327 | S24 | `cfg:versions` | `tls13-client` | 459:9 | 459:58 | [20962, 21011) | [20962, 21011) | 49 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLParameters.setProtocols` | `lib.jdk` | - | `parameters.setProtocols(new String[] {"TLSv1.3"})` | - |
| JV-328 | S24 | `cfg:cipher-suites` | `tls13-client` | 460:9 | 461:97 | [21021, 21159) | [21021, 21159) | 138 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLParameters.setCipherSuites` | `lib.jdk` | - | `parameters.setCipherSuites(new String[] { … (+1 lines)` | - |
| JV-329 | S24 | `ctor` | `tls13-client` | 462:22 | 462:67 | [21182, 21227) | [21182, 21227) | 45 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLContext.createSSLEngine` | `lib.jdk` | - | `context.createSSLEngine(TLS_SERVER_NAME, 443)` | - |
| JV-330 | S24 | `cfg:client-mode` | `tls13-client` | 463:9 | 463:38 | [21237, 21266) | [21237, 21266) | 29 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLEngine.setUseClientMode` | `lib.jdk` | - | `engine.setUseClientMode(true)` | - |
| JV-331 | S24 | `cfg:apply` | `tls13-client` | 464:9 | 464:44 | [21276, 21311) | [21276, 21311) | 35 | 0 | `s24Tls13Client` | `javax.net.ssl.SSLEngine.setSSLParameters` | `lib.jdk` | - | `engine.setSSLParameters(parameters)` | - |

## Full text of multi-line evidence

**JV-087** (`hkdf-sha256`, 162:22 to 165:43):

```text
HKDFParameterSpec.ofExtract()
                .addIKM(HKDF_IKM)
                .addSalt(HKDF_SALT)
                .thenExpand(HKDF_INFO, 42)
```

**JV-101** (`argon2id`, 185:22 to 191:25):

```text
new Argon2Parameters.Builder(Argon2Parameters.ARGON2_id)
                .withVersion(Argon2Parameters.ARGON2_VERSION_13)
                .withIterations(2)
                .withMemoryAsKB(19_456)
                .withParallelism(1)
                .withSalt(ARGON2_SALT)
                .build()
```

**JV-206** (`rsa-oaep-sha256`, 301:20 to 302:89):

```text
new OAEPParameterSpec(
                "SHA-256", "MGF1", MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT)
```

**JV-218** (`rsassa-pss-sha256`, 311:19 to 313:55):

```text
new PSSParameterSpec(
                "SHA-256", "MGF1", MGF1ParameterSpec.SHA256,
                32, PSSParameterSpec.TRAILER_FIELD_BC)
```

**JV-316** (`cert.self-signed`, 435:23 to 441:37):

```text
new JcaX509v3CertificateBuilder(
                name,
                new BigInteger(64, RNG),
                Date.from(now.minus(Duration.ofMinutes(1))),
                Date.from(now.plus(Duration.ofDays(365))),
                name,
                keyPair.getPublic())
```

**JV-328** (`tls13-client`, 460:9 to 461:97):

```text
parameters.setCipherSuites(new String[] {
            "TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"})
```

## Non-asset mentions (negative ground truth)

Every case-insensitive match of the algorithm-name lexicon (see `_tooling/spec.py`, `DECOY_PATTERN`) that lies outside all occurrence spans. A scanner that reports any of these as a cryptographic asset produces a false positive.

| ID | L:C | Bytes | Match | Context | Containing token / line | Why it is not an asset |
|---|---|---|---|---|---|---|
| JV-N001 | 61:18 | [2388, 2392) | `HMAC` | comment | `// Wikipedia HMAC example key` | Comment text; documentation only |
| JV-N002 | 74:8 | [3169, 3172) | `GCM` | comment | `// GCM specification test case 16` | Comment text; documentation only |
| JV-N003 | 78:33 | [3524, 3527) | `GCM` | identifier | `GCM_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N004 | 83:33 | [3859, 3862) | `ECB` | identifier | `ECB_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N005 | 87:33 | [4196, 4199) | `TLS` | identifier | `TLS_SERVER_NAME` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N006 | 116:13 | [5074, 5081) | `SHA-256` | comment | `// S01: SHA-256 (FIPS 180-4)` | Comment text; documentation only |
| JV-N007 | 119:22 | [5218, 5225) | `SHA-256` | string | `"SHA-256"` | Output label passed to emit(); printed text only |
| JV-N008 | 122:13 | [5275, 5282) | `SHA-512` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| JV-N009 | 122:22 | [5284, 5292) | `SHA3-256` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| JV-N010 | 122:32 | [5294, 5301) | `BLAKE2b` | comment | `// S02: SHA-512, SHA3-256, BLAKE2b-512` | Comment text; documentation only |
| JV-N011 | 124:13 | [5373, 5379) | `sha512` | identifier | `sha512` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N012 | 125:22 | [5441, 5448) | `SHA-512` | string | `"SHA-512"` | Output label passed to emit(); printed text only |
| JV-N013 | 126:13 | [5495, 5499) | `sha3` | identifier | `sha3` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N014 | 127:22 | [5562, 5570) | `SHA3-256` | string | `"SHA3-256"` | Output label passed to emit(); printed text only |
| JV-N015 | 132:22 | [5800, 5807) | `BLAKE2b` | string | `"BLAKE2b-512"` | Output label passed to emit(); printed text only |
| JV-N016 | 137:13 | [5946, 5949) | `md5` | identifier | `md5` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N017 | 138:22 | [6007, 6010) | `MD5` | string | `"MD5"` | Output label passed to emit(); printed text only |
| JV-N018 | 139:13 | [6054, 6058) | `sha1` | identifier | `sha1` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N019 | 140:22 | [6118, 6123) | `SHA-1` | string | `"SHA-1"` | Output label passed to emit(); printed text only |
| JV-N020 | 143:13 | [6175, 6183) | `SHAKE128` | comment | `// S04: SHAKE128 extendable-output function` | Comment text; documentation only |
| JV-N021 | 145:13 | [6255, 6260) | `shake` | identifier | `shake` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N022 | 146:9 | [6293, 6298) | `shake` | identifier | `shake` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N023 | 149:22 | [6431, 6439) | `SHAKE128` | string | `"SHAKE128"` | Output label passed to emit(); printed text only |
| JV-N024 | 152:13 | [6474, 6478) | `HMAC` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| JV-N025 | 152:18 | [6479, 6485) | `SHA256` | comment | `// S05: HMAC-SHA256` | Comment text; documentation only |
| JV-N026 | 156:22 | [6668, 6672) | `HMAC` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| JV-N027 | 156:27 | [6673, 6679) | `SHA256` | string | `"HMAC-SHA256"` | Output label passed to emit(); printed text only |
| JV-N028 | 159:13 | [6731, 6735) | `HKDF` | comment | `// S06: HKDF-SHA256 (RFC 5869) through the JDK 25 KDF API` | Comment text; documentation only |
| JV-N029 | 159:18 | [6736, 6742) | `SHA256` | comment | `// S06: HKDF-SHA256 (RFC 5869) through the JDK 25 KDF API` | Comment text; documentation only |
| JV-N030 | 161:13 | [6844, 6848) | `hkdf` | identifier | `hkdf` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N031 | 166:22 | [7069, 7073) | `HKDF` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| JV-N032 | 166:27 | [7074, 7080) | `SHA256` | string | `"HKDF-SHA256"` | Output label passed to emit(); printed text only |
| JV-N033 | 169:13 | [7135, 7141) | `PBKDF2` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| JV-N034 | 169:20 | [7142, 7146) | `HMAC` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| JV-N035 | 169:25 | [7147, 7153) | `SHA256` | comment | `// S07: PBKDF2-HMAC-SHA256` | Comment text; documentation only |
| JV-N036 | 174:22 | [7455, 7461) | `PBKDF2` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| JV-N037 | 174:29 | [7462, 7468) | `SHA256` | string | `"PBKDF2-SHA256"` | Output label passed to emit(); printed text only |
| JV-N038 | 177:13 | [7507, 7513) | `scrypt` | comment | `// S08: scrypt` | Comment text; documentation only |
| JV-N039 | 180:22 | [7653, 7659) | `scrypt` | string | `"scrypt"` | Output label passed to emit(); printed text only |
| JV-N040 | 183:13 | [7698, 7706) | `Argon2id` | comment | `// S09: Argon2id` | Comment text; documentation only |
| JV-N041 | 196:22 | [8250, 8258) | `Argon2id` | string | `"Argon2id"` | Output label passed to emit(); printed text only |
| JV-N042 | 199:13 | [8293, 8299) | `bcrypt` | comment | `// S10: bcrypt` | Comment text; documentation only |
| JV-N043 | 205:22 | [8572, 8578) | `bcrypt` | string | `"bcrypt"` | Output label passed to emit(); printed text only |
| JV-N044 | 208:13 | [8617, 8624) | `AES-256` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| JV-N045 | 208:21 | [8625, 8628) | `GCM` | comment | `// S11: AES-256-GCM known-answer test` | Comment text; documentation only |
| JV-N046 | 211:13 | [8762, 8765) | `gcm` | identifier | `gcm` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N047 | 214:29 | [8951, 8954) | `GCM` | identifier | `GCM_AAD` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N048 | 218:29 | [9164, 9167) | `GCM` | identifier | `GCM_AAD` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N049 | 222:22 | [9400, 9407) | `AES-256` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| JV-N050 | 222:30 | [9408, 9411) | `GCM` | string | `"AES-256-GCM"` | Output label passed to emit(); printed text only |
| JV-N051 | 223:57 | [9519, 9522) | `GCM` | identifier | `GCM_PLAINTEXT` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N052 | 226:13 | [9555, 9572) | `ChaCha20-Poly1305` | comment | `// S12: ChaCha20-Poly1305 (RFC 8439)` | Comment text; documentation only |
| JV-N053 | 238:22 | [10220, 10237) | `ChaCha20-Poly1305` | string | `"ChaCha20-Poly1305"` | Output label passed to emit(); printed text only |
| JV-N054 | 241:13 | [10307, 10314) | `AES-256` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| JV-N055 | 241:21 | [10315, 10318) | `CBC` | comment | `// S13: AES-256-CBC with PKCS#7 padding` | Comment text; documentation only |
| JV-N056 | 254:22 | [11000, 11007) | `AES-256` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| JV-N057 | 254:30 | [11008, 11011) | `CBC` | string | `"AES-256-CBC"` | Output label passed to emit(); printed text only |
| JV-N058 | 257:13 | [11084, 11091) | `AES-128` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| JV-N059 | 257:21 | [11092, 11095) | `ECB` | comment | `// S14: AES-128-ECB known-answer test - deliberately weak mode` | Comment text; documentation only |
| JV-N060 | 261:22 | [11358, 11365) | `AES-128` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| JV-N061 | 261:30 | [11366, 11369) | `ECB` | string | `"AES-128-ECB"` | Output label passed to emit(); printed text only |
| JV-N062 | 264:13 | [11433, 11440) | `AES-256` | comment | `// S15: AES-256-CTR` | Comment text; documentation only |
| JV-N063 | 264:21 | [11441, 11444) | `CTR` | comment | `// S15: AES-256-CTR` | Comment text; documentation only |
| JV-N064 | 277:22 | [12140, 12147) | `AES-256` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| JV-N065 | 277:30 | [12148, 12151) | `CTR` | string | `"AES-256-CTR"` | Output label passed to emit(); printed text only |
| JV-N066 | 280:13 | [12224, 12228) | `3DES` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| JV-N067 | 280:19 | [12230, 12234) | `TDEA` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| JV-N068 | 280:25 | [12236, 12239) | `CBC` | comment | `// S16: 3DES (TDEA) CBC - deliberately legacy` | Comment text; documentation only |
| JV-N069 | 292:22 | [12897, 12901) | `3DES` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| JV-N070 | 292:27 | [12902, 12905) | `CBC` | string | `"3DES-CBC"` | Output label passed to emit(); printed text only |
| JV-N071 | 295:13 | [12978, 12981) | `RSA` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| JV-N072 | 295:24 | [12989, 12993) | `OAEP` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| JV-N073 | 295:30 | [12995, 12998) | `PSS` | comment | `// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair` | Comment text; documentation only |
| JV-N074 | 301:13 | [13297, 13301) | `oaep` | identifier | `oaep` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N075 | 309:22 | [13825, 13828) | `RSA` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| JV-N076 | 309:31 | [13834, 13838) | `OAEP` | string | `"RSA-3072 OAEP"` | Output label passed to emit(); printed text only |
| JV-N077 | 311:13 | [13905, 13908) | `pss` | identifier | `pss` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N078 | 323:22 | [14491, 14494) | `RSA` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| JV-N079 | 323:31 | [14500, 14503) | `PSS` | string | `"RSA-3072 PSS"` | Output label passed to emit(); printed text only |
| JV-N080 | 332:22 | [14941, 14944) | `RSA` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| JV-N081 | 332:31 | [14950, 14958) | `PKCS1v15` | string | `"RSA-3072 PKCS1v15"` | Output label passed to emit(); printed text only |
| JV-N082 | 335:13 | [15031, 15036) | `ECDSA` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| JV-N083 | 335:19 | [15037, 15042) | `P-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| JV-N084 | 335:30 | [15048, 15055) | `SHA-256` | comment | `// S18: ECDSA P-256 with SHA-256` | Comment text; documentation only |
| JV-N085 | 347:22 | [15635, 15640) | `ECDSA` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| JV-N086 | 347:28 | [15641, 15646) | `P-256` | string | `"ECDSA P-256"` | Output label passed to emit(); printed text only |
| JV-N087 | 350:13 | [15709, 15716) | `Ed25519` | comment | `// S19: Ed25519 from a fixed seed (RFC 8032)` | Comment text; documentation only |
| JV-N088 | 362:22 | [16305, 16312) | `Ed25519` | string | `"Ed25519"` | Output label passed to emit(); printed text only |
| JV-N089 | 373:13 | [16788, 16792) | `hkdf` | identifier | `hkdf` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N090 | 378:13 | [16988, 16994) | `X25519` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| JV-N091 | 378:22 | [16997, 17001) | `ECDH` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| JV-N092 | 378:27 | [17002, 17007) | `P-256` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| JV-N093 | 378:48 | [17023, 17027) | `HKDF` | comment | `// S20: X25519 + ECDH P-256 key agreement, HKDF session key` | Comment text; documentation only |
| JV-N094 | 380:13 | [17105, 17111) | `x25519` | identifier | `x25519` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N095 | 385:22 | [17413, 17419) | `X25519` | string | `"X25519"` | Output label passed to emit(); printed text only |
| JV-N096 | 393:22 | [17836, 17840) | `ECDH` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| JV-N097 | 393:27 | [17841, 17846) | `P-256` | string | `"ECDH P-256"` | Output label passed to emit(); printed text only |
| JV-N098 | 397:22 | [18032, 18036) | `HKDF` | string | `"HKDF session key"` | Output label passed to emit(); printed text only |
| JV-N099 | 400:13 | [18111, 18121) | `ML-KEM-768` | comment | `// S21: ML-KEM-768 (FIPS 203) through the JDK KEM API` | Comment text; documentation only |
| JV-N100 | 409:22 | [18693, 18703) | `ML-KEM-768` | string | `"ML-KEM-768"` | Output label passed to emit(); printed text only |
| JV-N101 | 413:13 | [18853, 18862) | `ML-DSA-65` | comment | `// S22: ML-DSA-65 (FIPS 204)` | Comment text; documentation only |
| JV-N102 | 425:22 | [19424, 19433) | `ML-DSA-65` | string | `"ML-DSA-65"` | Output label passed to emit(); printed text only |
| JV-N103 | 428:25 | [19513, 19518) | `X.509` | comment | `// S23: self-signed X.509 certificate (Bouncy Castle builder, JDK signer and ve…` | Comment text; documentation only |
| JV-N104 | 433:41 | [19853, 19856) | `TLS` | identifier | `TLS_SERVER_NAME` | Program identifier (function, variable or constant name); names an algorithm but is not a crypto asset |
| JV-N105 | 451:22 | [20645, 20650) | `X.509` | string | `"X.509 self-signed"` | Output label passed to emit(); printed text only |
| JV-N106 | 454:13 | [20701, 20704) | `TLS` | comment | `// S24: TLS 1.3-only client configuration (no connection is made)` | Comment text; documentation only |
| JV-N107 | 465:22 | [21334, 21337) | `TLS` | string | `"TLS 1.3 client"` | Output label passed to emit(); printed text only |

## Implicit and runtime-dependent cryptography

Behaviour that is fixed by the runtime or library rather than visible in the source. These are the places where source-level ground truth and the cryptography that actually executes can diverge.

| Asset | What happens |
|---|---|
| `csprng` | new SecureRandom() and every KeyGenerator/KeyPairGenerator/Signature without an explicit random use the default SecureRandom; on Linux that is NativePRNG (SUN), backed by /dev/urandom. |
| `chacha20-poly1305` | KeyGenerator 'ChaCha20' always produces 256-bit keys (implicit). |
| `3des-cbc` | KeyGenerator 'DESede' defaults to 168-bit keys (implicit). |
| `rsassa-pkcs1v15-sha256` | 'SHA256withRSA' and 'SHA256withECDSA' each name a hash and a scheme in one token. |
| `ecdsa-p256-sha256` | JCA ECDSA signatures are DER-encoded. |
| `ml-dsa-65` | JDK ML-DSA signing is hedged with an empty context by default. |
| `tls13-client` | SSLContext.init(null, null, null) uses the default trust store and SecureRandom. Named groups are the JDK 25 defaults (see Provider resolution); none is post-quantum. |
| `sha-512` | Ed25519 (Bouncy Castle) uses SHA-512 internally. |

Provider resolution observed on OpenJDK 25.0.4.1 with the default `java.security` (Bouncy Castle is used only through its lightweight API and is not registered as a JCA provider):

| Engine | Algorithm | Resolved provider |
|---|---|---|
| MessageDigest | SHA-256 | SUN |
| MessageDigest | SHA-512 | SUN |
| MessageDigest | SHA3-256 | SUN |
| MessageDigest | MD5 | SUN |
| MessageDigest | SHA-1 | SUN |
| Mac | HmacSHA256 | SunJCE |
| KDF | HKDF-SHA256 | SunJCE |
| SecretKeyFactory | PBKDF2WithHmacSHA256 | SunJCE |
| Cipher | AES/GCM/NoPadding | SunJCE |
| Cipher | ChaCha20-Poly1305 | SunJCE |
| Cipher | AES/CBC/PKCS5Padding | SunJCE |
| Cipher | AES/ECB/PKCS5Padding | SunJCE |
| Cipher | AES/CTR/NoPadding | SunJCE |
| Cipher | DESede/CBC/PKCS5Padding | SunJCE |
| Cipher | RSA/ECB/OAEPPadding | SunJCE |
| KeyGenerator | ChaCha20 | SunJCE (uninitialised default: 256-bit keys incl. parity) |
| KeyGenerator | AES | SunJCE (uninitialised default: 256-bit keys incl. parity) |
| KeyGenerator | DESede | SunJCE (uninitialised default: 192-bit keys incl. parity) |
| KeyPairGenerator | RSA | SunRsaSign |
| KeyPairGenerator | EC | SunEC |
| KeyPairGenerator | X25519 | SunEC |
| KeyPairGenerator | ML-KEM-768 | SunJCE |
| KeyPairGenerator | ML-DSA-65 | SUN |
| Signature | RSASSA-PSS | SunRsaSign |
| Signature | SHA256withRSA | SunRsaSign |
| Signature | SHA256withECDSA | SunEC |
| Signature | ML-DSA-65 | SUN |
| KeyAgreement | X25519 | SunEC |
| KeyAgreement | ECDH | SunEC |
| KEM | ML-KEM | SunJCE |
| SecureRandom | new SecureRandom() | SUN / NativePRNG |
| SSLContext | TLSv1.3 | SunJSSE |
| SSLParameters | default named groups | x25519, secp256r1, secp384r1, secp521r1, x448, ffdhe2048, ffdhe3072, ffdhe4096, ffdhe6144, ffdhe8192 |

## Detection notes

Notes referenced from the ledger. Together they describe what makes each occurrence hard (or easy) to recognise statically.

| Note | Explanation | Occurrences |
|---|---|---|
| `securerandom-default` | On Linux, new SecureRandom() resolves to NativePRNG (SUN provider). | JV-056 |
| `key-label` | Key-algorithm label inside a key spec; informational for HMAC keys. | JV-083 |
| `computed` | Parameter is a constant expression, not a literal (evaluates to 16384). | JV-097 |
| `bcrypt-version` | Explicit bcrypt version prefix ($2b$). | JV-114 |
| `keysize-from-key` | Key size is not named in code; it follows from the length of the key bytes (data-flow dependent). | JV-117, JV-164 |
| `keygen-default-random` | Key generator draws from the provider's default SecureRandom (implicit CSPRNG). | JV-131, JV-148, JV-171 |
| `aes-keygen-label` | Mode-agnostic 'AES' key generator; the mode is only visible in the later transformation string. | JV-145, JV-168 |
| `pkcs5-is-pkcs7` | JCA name 'PKCS5Padding' denotes PKCS#7 padding for 16-byte blocks; normalise to pkcs7. | JV-152, JV-157, JV-162, JV-190, JV-195 |
| `desede-default-size` | Key size is implicit: SunJCE's DESede KeyGenerator defaults to 168 bits (3-key TDEA). | JV-186 |
| `oaep-explicit` | OAEP parameters are explicit; the bare transformation 'RSA/ECB/OAEPWithSHA-256AndMGF1Padding' would make SunJCE use SHA-1 for MGF1. | JV-206 |
| `ec-keygen-label` | Generic 'EC' generator; the curve comes from a separate parameter spec. | JV-243, JV-282, JV-311 |
| `curve-alias` | Curve alias; normalise to P-256 (secp256r1 = prime256v1 = P-256). | JV-246, JV-285, JV-314 |
| `seed-ctor` | Key pair is derived deterministically from the hard-coded 32-byte seed. | JV-256 |
| `polymorphic-site` | One call site serves two assets depending on the caller; recorded once per asset (context-sensitive). | JV-264, JV-265, JV-268, JV-269 |
| `interprocedural` | Algorithm literal reaches the API through a helper-method parameter (inter-procedural constant). | JV-279, JV-280, JV-288, JV-289 |
| `kem-family-name` | KEM API takes the family name; the parameter set comes from the key (ML-KEM-768). | JV-294 |
| `serial` | CSPRNG output used for the certificate serial number (not key material). | JV-317 |
| `tls-context-name` | SSLContext protocol name; enabled versions are set separately via SSLParameters. | JV-325 |
| `default-managers` | null arguments select the default key/trust managers and SecureRandom. | JV-326 |

## Machine-readable files

`ground-truth.json` holds every field shown above, including the full evidence text of each span. `cbom.cdx.json` is a CycloneDX 1.6 BOM: one `library` component per library, one `cryptographic-asset` component per asset (with `evidence.occurrences`), library `provides` relations and algorithm `dependsOn` relations. Corpus-specific facts (NIST status, CNSA 2.0, implicit flags, provenance) are carried as `cbom-corpus:*` properties.
