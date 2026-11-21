# CBOM ground-truth corpus - Artifacts

This case holds cryptography that lives in **files** rather than in program code: 29 artifact files (certificates, keys, a CSR and a CRL, PKCS#7, PKCS#12 and JKS stores, application secrets, an OpenSSL TLS configuration and post-quantum certificates and keys, plus two decoys). They contain **64 assets** (25 algorithms, 10 certificates, 1 protocol, 28 items of related crypto material) at **153 occurrences**, and **9 non-asset mentions** that a scanner should not report. The same data is available machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.

> Every key, certificate, password and token here was generated for this corpus with `_tooling/artifacts.py` and protects nothing. The weak items (an RSA-1024 / SHA-1 certificate, the `changeit` store password, low PBKDF2 iteration counts) are deliberate so that policy checks have something to find.

The case targets file and secret scanners such as CBOMKit-Theia and CBOM-Lens, but every tool that accepts any input is scored on it. It is a directory of files, not a program: there is nothing to build or run.

## Files

| File | Scenario | Format | Contents | Bytes | Objects / settings | Non-asset mentions |
|---|---|---|---|---|---|---|
| `pki/root-ca.crt` | A01 | PEM certificate | Root CA certificate | 1903 | 1 | 0 |
| `pki/issuing-ca.crt` | A01 | PEM certificate | Issuing CA certificate | 1375 | 1 | 0 |
| `pki/issuing-ca.key` | A01 | SEC 1 EC PRIVATE KEY | Issuing CA private key | 288 | 1 | 0 |
| `pki/ca-chain.pem` | A01 | PEM bundle (2 certificates) | Issuing CA and root CA, each preceded by subject=/issuer= lines | 3519 | 2 | 0 |
| `pki/server.crt` | A02 | PEM certificate | TLS server certificate | 1127 | 1 | 0 |
| `pki/server.key` | A02 | PKCS#1 RSA PRIVATE KEY | TLS server private key | 1675 | 1 | 0 |
| `pki/server.csr` | A02 | PKCS#10 CERTIFICATE REQUEST | Certificate signing request for the server key | 1045 | 1 | 0 |
| `pki/fullchain.p7b` | A02 | PKCS#7 certs-only, DER | Server certificate, issuing CA and root CA | 3174 | 3 | 0 |
| `pki/api.der` | A03 | DER certificate | API endpoint certificate | 583 | 1 | 0 |
| `pki/api.key` | A03 | PKCS#8 PRIVATE KEY | API endpoint private key | 241 | 1 | 0 |
| `pki/issuing-ca.crl` | A04 | PEM X509 CRL | CRL of the issuing CA | 503 | 1 | 0 |
| `pki/legacy-sha1.cer` | A05 | DER certificate | Legacy self-signed SHA-1 certificate | 598 | 1 | 0 |
| `pki/device-ed25519.crt` | A06 | PEM certificate | Self-signed Ed25519 device certificate | 660 | 1 | 0 |
| `keys/device-ed25519.pem` | A06 | PKCS#8 PRIVATE KEY | Device private key | 119 | 1 | 0 |
| `keys/backup-rsa3072.enc.pem` | A07 | PKCS#8 ENCRYPTED PRIVATE KEY (PBES2) | Backup private key, passphrase in secrets/app.env | 2666 | 1 | 0 |
| `keys/backup-rsa3072.pub.pem` | A07 | SPKI PUBLIC KEY | Backup public key | 625 | 1 | 0 |
| `keys/deploy_ed25519` | A08 | OPENSSH PRIVATE KEY | Deploy private key | 387 | 1 | 0 |
| `keys/deploy_ed25519.pub` | A08 | OpenSSH public key line | Deploy public key | 108 | 1 | 0 |
| `keystores/client.p12` | A09 | PKCS#12 (password changeit) | Client key, client certificate and issuing CA | 2331 | 6 | 0 |
| `keystores/truststore.jks` | A10 | JKS (password changeit) | Root CA and partner root CA as trusted certificate entries | 2345 | 3 | 0 |
| `secrets/app.env` | A11 | dotenv | Reporting service settings | 728 | 5 | 1 |
| `secrets/main.tf` | A12 | Terraform (HCL) | Reporting database resource | 315 | 1 | 0 |
| `tls/openssl.cnf` | A13 | OpenSSL configuration | System-wide TLS defaults | 519 | 4 | 2 |
| `pqc/pq-root-ca.crt` | A14 | PEM certificate | ML-DSA-65 root CA certificate | 7623 | 1 | 0 |
| `pqc/pq-root-ca.key` | A14 | PKCS#8 PRIVATE KEY (seed form) | ML-DSA-65 root CA private key | 128 | 1 | 0 |
| `pqc/kem-endpoint.crt` | A14 | PEM certificate | ML-KEM-768 endpoint certificate | 6672 | 1 | 0 |
| `pqc/kem-endpoint.key` | A14 | PKCS#8 PRIVATE KEY (seed form) | ML-KEM-768 endpoint private key | 172 | 1 | 0 |
| `examples/placeholder.crt` | - | PEM armour, no certificate | Placeholder telling an operator where to paste a certificate | 102 | 0 | 1 |
| `examples/deploy-notes.md` | - | Markdown | Deployment notes quoting a shortened (unusable) private key | 691 | 0 | 5 |

Also here: `README.md` (this document), `cbom.cdx.json` (ground-truth CycloneDX 1.6 CBOM) and `ground-truth.json` (occurrence ledger, asset inventory, non-asset mentions, file hashes and the verification log). The orchestrator keeps the last two out of a tool's workspace.

## Scenarios

| Scenario | Family | What it holds | Files | Occurrences | Assets |
|---|---|---|---|---|---|
| A01 | Certificates and keys | RSA/ECDSA test PKI: RSA-4096 root CA, ECDSA P-384 issuing CA with its SEC 1 key, and a chain bundle whose blocks are preceded by subject=/issuer= lines | `pki/root-ca.crt`, `pki/issuing-ca.crt`, `pki/issuing-ca.key`, `pki/ca-chain.pem` | 23 | `ecdsa-p384`, `rsa-4096`, `sha-256`, `sha256-with-rsa`, `cert.issuing-ca`, `cert.root-ca`, `m.issuing-ca-private-key`, `m.issuing-ca-public-key`, `m.root-ca-public-key` |
| A02 | Certificates and keys | TLS server: PEM certificate (RSA-2048 key, signed ecdsa-with-SHA384), PKCS#1 key, PKCS#10 CSR and a PKCS#7 full chain | `pki/server.crt`, `pki/server.key`, `pki/server.csr`, `pki/fullchain.p7b` | 28 | `ecdsa-p384`, `ecdsa-with-sha384`, `rsa-2048`, `rsa-4096`, `sha-256`, `sha-384`, `sha256-with-rsa`, `cert.issuing-ca`, `cert.root-ca`, `cert.server`, `m.issuing-ca-public-key`, `m.root-ca-public-key`, `m.server-csr`, `m.server-private-key`, `m.server-public-key` |
| A03 | Certificates and keys | API endpoint: DER certificate (ECDSA P-256 key) and its PKCS#8 key | `pki/api.der`, `pki/api.key` | 8 | `ecdsa-p256`, `ecdsa-with-sha384`, `sha-384`, `cert.api`, `m.api-private-key`, `m.api-public-key` |
| A04 | Certificates and keys | Certificate revocation list from the issuing CA (one revoked serial) | `pki/issuing-ca.crl` | 3 | `ecdsa-with-sha384`, `sha-384`, `m.issuing-ca-crl` |
| A05 | Certificates and keys | Legacy self-signed certificate: RSA-1024 key, sha1WithRSAEncryption, DER | `pki/legacy-sha1.cer` | 5 | `rsa-1024`, `sha-1`, `sha1-with-rsa`, `cert.legacy`, `m.legacy-public-key` |
| A06 | Certificates and keys | Ed25519 device certificate and its PKCS#8 key | `pki/device-ed25519.crt`, `keys/device-ed25519.pem` | 6 | `ed25519`, `cert.device`, `m.device-private-key`, `m.device-public-key` |
| A07 | Certificates and keys | RSA-3072 backup key as encrypted PKCS#8 (PBES2) plus its SPKI public key | `keys/backup-rsa3072.enc.pem`, `keys/backup-rsa3072.pub.pem` | 9 | `aes-256-cbc`, `hmac-sha256`, `pbkdf2-hmac-sha256`, `rsa-3072`, `sha-256`, `m.backup-private-key`, `m.backup-public-key` |
| A08 | Certificates and keys | OpenSSH Ed25519 deploy key pair | `keys/deploy_ed25519`, `keys/deploy_ed25519.pub` | 5 | `ed25519`, `m.deploy-private-key`, `m.deploy-public-key` |
| A09 | Keystores | PKCS#12 client keystore: ECDSA P-256 key, client certificate and issuing CA certificate | `keystores/client.p12` | 23 | `aes-256-cbc`, `ecdsa-p256`, `ecdsa-p384`, `ecdsa-with-sha384`, `hmac-sha256`, `pbkdf2-hmac-sha256`, `sha-256`, `sha-384`, `sha256-with-rsa`, `cert.client`, `cert.issuing-ca`, `m.client-private-key`, `m.client-public-key`, `m.issuing-ca-public-key` |
| A10 | Keystores | JKS truststore: the root CA and a partner root CA that occurs nowhere else | `keystores/truststore.jks` | 11 | `rsa-2048`, `rsa-4096`, `sha-1`, `sha-256`, `sha256-with-rsa`, `cert.partner-ca`, `cert.root-ca`, `m.partner-ca-public-key`, `m.root-ca-public-key` |
| A11 | Secrets and TLS configuration | dotenv file: HS256 signing key, a JWT signed with it, the keystore password and the backup-key passphrase | `secrets/app.env` | 7 | `hmac-sha256`, `sha-256`, `m.backup-passphrase`, `m.jwt-signing-key`, `m.keystore-password`, `m.service-token` |
| A12 | Secrets and TLS configuration | Terraform resource with a database password | `secrets/main.tf` | 1 | `m.db-password` |
| A13 | Secrets and TLS configuration | OpenSSL configuration: TLS 1.3 only, two cipher suites, a hybrid post-quantum key-exchange group | `tls/openssl.cnf` | 12 | `aes-256-gcm`, `chacha20-poly1305`, `ml-kem-768`, `sha-256`, `sha-384`, `x25519`, `x25519mlkem768`, `tls13-openssl` |
| A14 | Post-quantum artifacts | ML-DSA-65 root CA and an ML-KEM-768 endpoint certificate it signed, with both PKCS#8 keys | `pqc/pq-root-ca.crt`, `pqc/pq-root-ca.key`, `pqc/kem-endpoint.crt`, `pqc/kem-endpoint.key` | 12 | `ml-dsa-65`, `ml-kem-768`, `cert.kem-endpoint`, `cert.pq-root-ca`, `m.kem-endpoint-private-key`, `m.kem-endpoint-public-key`, `m.pq-root-private-key`, `m.pq-root-public-key` |

## How occurrences are recorded

An **occurrence** is one place where an asset is stored: a certificate in a PEM block, a key in a PKCS#12 bag, a signature algorithm inside a certificate, a secret on a configuration line. Every occurrence carries `fileLevel: true`: the artifact file is the unit of evidence, so a scanner location that names the file counts even without a line. Coordinates:

| Field | Convention |
|---|---|
| Text files | Line and column (1-based, end exclusive), char and byte offsets of the PEM block (from its BEGIN line to the end of its END line) or of the configuration value |
| Binary files | Byte range only: the whole file for DER, the certificate's DER inside PKCS#7 and JKS, the encrypted blob for PKCS#12 bags, the AlgorithmIdentifier for PBES2 and MAC parameters |
| Nesting | 0 = object or setting; 1+ = a field inside it (signature algorithm, subject public key, PBES2 parameters). Nested occurrences reuse their container's span and name it in `container` |
| Encrypted | `true` when the object is stored encrypted and is readable only with the documented password |
| CycloneDX | `location` is the path relative to this directory; `line` and `offset` (column - 1) only for text files; ranges, scope and encoding are in `additionalContext` |

Roles:

| Role | Meaning |
|---|---|
| `obj` | A stored object: certificate, private or public key, CSR, CRL (qualifier = encoding, e.g. `x509`, `pkcs1`, `sec1`, `pkcs8`, `spki`, `openssh`) |
| `alg` | An algorithm identifier inside an object or a configuration value (qualifier = field, e.g. `signatureAlgorithm`, `subjectPublicKeyInfo`, `pbes2.kdf`, `mac`, `cipher-suite`) |
| `cfg` | A protocol configuration directive (qualifier = directive) |
| `mat` | A secret value assigned in a configuration file (qualifier = variable) |

Recording rules: a certificate occurrence brings occurrences of its signature algorithm (and that algorithm's hash, with the signature algorithm as parent), its subject public key algorithm and its public key; a private key occurrence brings its key algorithm and, where the encoding stores it (PKCS#1, SEC 1 with a public point, PKCS#8 for RSA and EC, OpenSSH), its public key. A PKCS#8 key in seed form (ML-DSA, ML-KEM) and an Ed25519 PKCS#8 v1 key do not store the public key. Subject and authority key identifiers are not recorded as SHA-1 uses (RFC 5280 leaves the method open and nothing recomputes them). Ed25519's SHA-512 and ML-KEM's SHA-3 / SHAKE are implicit, as in the program cases.

## Summary

| Measure | Count |
|---|---|
| Files | 29 |
| Occurrences | 153 |
| Occurrences with role `obj` | 54 |
| Occurrences with role `alg` | 88 |
| Occurrences with role `cfg` | 6 |
| Occurrences with role `mat` | 5 |
| Occurrences inside encrypted containers | 16 |
| Algorithm assets (incl. implicit) | 25 |
| Implicit assets (no occurrence) | 3 |
| Certificates | 10 |
| Protocols | 1 |
| Related crypto material | 28 |
| Non-asset mentions | 9 |
| Verification checks passed | 139 |

## Certificates

| Asset | Subject | Issuer | Serial | Validity | Signature | Public key | Files | SHA-256 |
|---|---|---|---|---|---|---|---|---|
| `cert.root-ca` | `CN=CBOMFuse Test Root CA,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse Test Root CA,O=CBOMFuse Baseline,C=CA` | 0x1 | 2026-01-01 to 2046-01-01 | `sha256-with-rsa` | `m.root-ca-public-key` | `pki/root-ca.crt`, `pki/ca-chain.pem`, `pki/fullchain.p7b`, `keystores/truststore.jks` | `1db0a2221276b4cf…` |
| `cert.issuing-ca` | `CN=CBOMFuse Test Issuing CA,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse Test Root CA,O=CBOMFuse Baseline,C=CA` | 0x1000 | 2026-01-01 to 2036-01-01 | `sha256-with-rsa` | `m.issuing-ca-public-key` | `pki/issuing-ca.crt`, `pki/ca-chain.pem`, `pki/fullchain.p7b`, `keystores/client.p12` | `3ed6a695fc0b52ee…` |
| `cert.server` | `CN=server.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse Test Issuing CA,O=CBOMFuse Baseline,C=CA` | 0x2001 | 2026-01-01 to 2028-01-01 | `ecdsa-with-sha384` | `m.server-public-key` | `pki/server.crt`, `pki/fullchain.p7b` | `2066b075bb3abd7f…` |
| `cert.api` | `CN=api.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse Test Issuing CA,O=CBOMFuse Baseline,C=CA` | 0x2002 | 2026-01-01 to 2028-01-01 | `ecdsa-with-sha384` | `m.api-public-key` | `pki/api.der` | `4829f6a35164c9ba…` |
| `cert.client` | `CN=svc-reporting,OU=Service Accounts,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse Test Issuing CA,O=CBOMFuse Baseline,C=CA` | 0x2003 | 2026-01-01 to 2028-01-01 | `ecdsa-with-sha384` | `m.client-public-key` | `keystores/client.p12` | `7e6bf9af004ae33e…` |
| `cert.device` | `CN=device-42.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | `CN=device-42.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | 0x3001 | 2026-01-01 to 2031-01-01 | `ed25519` | `m.device-public-key` | `pki/device-ed25519.crt` | `1c10c70220a903a5…` |
| `cert.legacy` | `CN=legacy.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | `CN=legacy.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | 0x1999 | 2016-01-01 to 2036-01-01 | `sha1-with-rsa` | `m.legacy-public-key` | `pki/legacy-sha1.cer` | `e0e6c46367192026…` |
| `cert.partner-ca` | `CN=CBOMFuse Partner Root CA,O=CBOMFuse Partner,C=CA` | `CN=CBOMFuse Partner Root CA,O=CBOMFuse Partner,C=CA` | 0x50 | 2026-01-01 to 2041-01-01 | `sha256-with-rsa` | `m.partner-ca-public-key` | `keystores/truststore.jks` | `9e35c02326726178…` |
| `cert.pq-root-ca` | `CN=CBOMFuse PQC Test Root CA,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse PQC Test Root CA,O=CBOMFuse Baseline,C=CA` | 0x7001 | 2026-01-01 to 2041-01-01 | `ml-dsa-65` | `m.pq-root-public-key` | `pqc/pq-root-ca.crt` | `11c12cdc794b1bac…` |
| `cert.kem-endpoint` | `CN=kem.cbom-corpus.example,O=CBOMFuse Baseline,C=CA` | `CN=CBOMFuse PQC Test Root CA,O=CBOMFuse Baseline,C=CA` | 0x7002 | 2026-01-01 to 2028-01-01 | `ml-dsa-65` | `m.kem-endpoint-public-key` | `pqc/kem-endpoint.crt` | `ef21269eb3a546b7…` |

Extensions:

| Asset | Extensions |
|---|---|
| `cert.root-ca` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier |
| `cert.issuing-ca` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; authorityKeyIdentifier |
| `cert.server` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; authorityKeyIdentifier; extendedKeyUsage; subjectAltName |
| `cert.api` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; authorityKeyIdentifier; extendedKeyUsage; subjectAltName |
| `cert.client` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; authorityKeyIdentifier; extendedKeyUsage |
| `cert.device` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; subjectAltName |
| `cert.legacy` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier |
| `cert.partner-ca` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier |
| `cert.pq-root-ca` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier |
| `cert.kem-endpoint` | basicConstraints (critical); keyUsage (critical); subjectKeyIdentifier; authorityKeyIdentifier; subjectAltName |

## Algorithm assets

| Asset | Name | Primitive | Family | Parameter set | Curve | OID | Occurrences | Files | Depends on |
|---|---|---|---|---|---|---|---|---|---|
| `sha-256` | SHA-256 | hash | SHA-2 | 256 | - | 2.16.840.1.101.3.4.2.1 | 16 | `pki/root-ca.crt`, `pki/issuing-ca.crt`, `pki/ca-chain.pem`, `pki/server.csr`, `pki/fullchain.p7b`, `keys/backup-rsa3072.enc.pem`, `keystores/client.p12`, `keystores/truststore.jks`, `secrets/app.env`, `tls/openssl.cnf` | - |
| `sha-384` | SHA-384 | hash | SHA-2 | 384 | - | 2.16.840.1.101.3.4.2.2 | 6 | `pki/server.crt`, `pki/fullchain.p7b`, `pki/api.der`, `pki/issuing-ca.crl`, `keystores/client.p12`, `tls/openssl.cnf` | - |
| `sha-512` | SHA-512 | hash | SHA-2 | 512 | - | 2.16.840.1.101.3.4.2.3 | implicit | - | - |
| `sha3-256` | SHA3-256 | hash | SHA-3 | 256 | - | 2.16.840.1.101.3.4.2.8 | implicit | - | - |
| `sha-1` | SHA-1 | hash | SHA-1 | 160 | - | 1.3.14.3.2.26 | 2 | `pki/legacy-sha1.cer`, `keystores/truststore.jks` | - |
| `shake128` | SHAKE128 | xof | SHA-3 | 128 | - | 2.16.840.1.101.3.4.2.11 | implicit | - | - |
| `hmac-sha256` | HMAC-SHA256 | mac | HMAC | 256 | - | 1.2.840.113549.2.9 | 11 | `keys/backup-rsa3072.enc.pem`, `keystores/client.p12`, `secrets/app.env` | sha-256 |
| `pbkdf2-hmac-sha256` | PBKDF2-HMAC-SHA256 | kdf | PBKDF2 | SHA-256 | - | 1.2.840.113549.1.5.12 | 6 | `keys/backup-rsa3072.enc.pem`, `keystores/client.p12` | hmac-sha256, sha-256 |
| `aes-256-gcm` | AES-256-GCM | ae | AES | 256 | - | 2.16.840.1.101.3.4.1.46 | 1 | `tls/openssl.cnf` | - |
| `chacha20-poly1305` | ChaCha20-Poly1305 | ae | ChaCha20 | 256 | - | 1.2.840.113549.1.9.16.3.18 | 1 | `tls/openssl.cnf` | - |
| `aes-256-cbc` | AES-256-CBC-PKCS7 | block-cipher | AES | 256 | - | 2.16.840.1.101.3.4.1.42 | 3 | `keys/backup-rsa3072.enc.pem`, `keystores/client.p12` | - |
| `rsa-3072` | RSA-3072 key pair | pke | RSA | 3072 | - | 1.2.840.113549.1.1.1 | 2 | `keys/backup-rsa3072.enc.pem`, `keys/backup-rsa3072.pub.pem` | - |
| `x25519` | X25519 | key-agree | ECDH | Curve25519 | curve25519 | 1.3.101.110 | 2 | `tls/openssl.cnf` | - |
| `ed25519` | Ed25519 | signature | EdDSA | Ed25519 | edwards25519 | 1.3.101.112 | 5 | `pki/device-ed25519.crt`, `keys/device-ed25519.pem`, `keys/deploy_ed25519`, `keys/deploy_ed25519.pub` | sha-512 |
| `ml-kem-768` | ML-KEM-768 | kem | ML-KEM | 768 | - | 2.16.840.1.101.3.4.4.2 | 3 | `tls/openssl.cnf`, `pqc/kem-endpoint.crt`, `pqc/kem-endpoint.key` | sha3-256, shake128 |
| `ml-dsa-65` | ML-DSA-65 | signature | ML-DSA | 65 | - | 2.16.840.1.101.3.4.3.18 | 4 | `pqc/pq-root-ca.crt`, `pqc/pq-root-ca.key`, `pqc/kem-endpoint.crt` | - |
| `rsa-1024` | RSA-1024 key pair | pke | RSA | 1024 | - | 1.2.840.113549.1.1.1 | 1 | `pki/legacy-sha1.cer` | - |
| `rsa-2048` | RSA-2048 key pair | pke | RSA | 2048 | - | 1.2.840.113549.1.1.1 | 5 | `pki/server.crt`, `pki/server.key`, `pki/server.csr`, `pki/fullchain.p7b`, `keystores/truststore.jks` | - |
| `rsa-4096` | RSA-4096 key pair | pke | RSA | 4096 | - | 1.2.840.113549.1.1.1 | 4 | `pki/root-ca.crt`, `pki/ca-chain.pem`, `pki/fullchain.p7b`, `keystores/truststore.jks` | - |
| `ecdsa-p256` | ECDSA P-256 key pair | signature | ECDSA | P-256 | secp256r1 | 1.2.840.10045.2.1 | 4 | `pki/api.der`, `pki/api.key`, `keystores/client.p12` | - |
| `ecdsa-p384` | ECDSA P-384 key pair | signature | ECDSA | P-384 | secp384r1 | 1.2.840.10045.2.1 | 5 | `pki/issuing-ca.crt`, `pki/issuing-ca.key`, `pki/ca-chain.pem`, `pki/fullchain.p7b`, `keystores/client.p12` | - |
| `sha256-with-rsa` | sha256WithRSAEncryption (RSASSA-PKCS1-v1_5 with SHA-256) | signature | RSA | - | - | 1.2.840.113549.1.1.11 | 20 | `pki/root-ca.crt`, `pki/issuing-ca.crt`, `pki/ca-chain.pem`, `pki/server.csr`, `pki/fullchain.p7b`, `keystores/client.p12`, `keystores/truststore.jks` | sha-256 |
| `sha1-with-rsa` | sha1WithRSAEncryption (RSASSA-PKCS1-v1_5 with SHA-1) | signature | RSA | - | - | 1.2.840.113549.1.1.5 | 2 | `pki/legacy-sha1.cer` | sha-1 |
| `ecdsa-with-sha384` | ecdsa-with-SHA384 | signature | ECDSA | - | - | 1.2.840.10045.4.3.3 | 10 | `pki/server.crt`, `pki/fullchain.p7b`, `pki/api.der`, `pki/issuing-ca.crl`, `keystores/client.p12` | sha-384 |
| `x25519mlkem768` | X25519MLKEM768 hybrid key exchange | kem | ML-KEM | 768 | curve25519 | - | 3 | `tls/openssl.cnf` | ml-kem-768, x25519 |

Security and compliance:

| Asset | Classical bits | NIST PQ category | Standards | NIST status | CNSA 2.0 | Quantum | Note |
|---|---|---|---|---|---|---|---|
| `sha-256` | 128 | 2 | FIPS 180-4 | Approved | Not CNSA 2.0 (requires SHA-384/SHA-512) | Generic quantum speed-up only (Grover/BHT) | Collision resistance 128 bits; reference point of NIST PQ category 2. |
| `sha-384` | 192 | 4 | FIPS 180-4 | Approved | CNSA 2.0 compliant | Generic quantum speed-up only (Grover/BHT) | Hash of ecdsa-with-SHA384 and of the TLS_AES_256_GCM_SHA384 cipher suite. |
| `sha-512` | 256 | 4 | FIPS 180-4 | Approved | CNSA 2.0 compliant | Generic quantum speed-up only (Grover/BHT) | Category >= 4 (SHA-384 collision is the highest hash-based NIST reference point). |
| `sha3-256` | 128 | 2 | FIPS 202 | Approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | - |
| `sha-1` | 63 | 0 | FIPS 180-4; RFC 3174 | Disallowed for signature generation (SP 800-131A r2); NIST retires SHA-1 by 2030-12-31 | Not CNSA 2.0 | Already broken classically (chosen-prefix collision ~2^63) | - |
| `shake128` | 128 | 2 | FIPS 202 | Approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Used with a 256-bit output (min(d/2,128) = 128-bit collision resistance). |
| `hmac-sha256` | 256 | 5 | FIPS 198-1; RFC 2104 | Approved (FIPS 198-1) | Not CNSA 2.0 (SHA-384+ required) | Generic quantum speed-up only (Grover/BHT) | HS256 for the JWT (RFC 7518) and the PKCS#12 integrity MAC (key from the PKCS#12 KDF of RFC 7292 appendix B.2). |
| `pbkdf2-hmac-sha256` | - | - | SP 800-132; RFC 8018 | Approved (SP 800-132); the iteration counts used here (2,048 and 20,000) are below the OWASP 2023 figure of 600,000 | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | PBES2 key derivation (RFC 8018) in the encrypted PKCS#8 key and the PKCS#12 keystore; PRF hmacWithSHA256. |
| `aes-256-gcm` | 256 | 5 | FIPS 197; SP 800-38D | Approved | CNSA 2.0 compliant (AES-256) | Generic quantum speed-up only (Grover/BHT) | Record protection of TLS_AES_256_GCM_SHA384. |
| `chacha20-poly1305` | 256 | 5 | RFC 8439 | Not NIST-approved | Not CNSA 2.0 | Generic quantum speed-up only (Grover/BHT) | Stream-cipher AEAD; mode reported as 'other'. |
| `aes-256-cbc` | 256 | 5 | FIPS 197; SP 800-38A | Approved mode; unauthenticated (padding-oracle risk without a MAC) | AES-256 meets CNSA 2.0 key size | Generic quantum speed-up only (Grover/BHT) | PBES2 encryption scheme aes256-CBC-PAD (RFC 8018). |
| `rsa-3072` | 128 | 0 | FIPS 186-5; RFC 8017 | Acceptable; quantum-vulnerable - disallowed after 2035 (NIST IR 8547) | CNSA 1.0 only (>=3072); not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | Backup key; stored only as encrypted PKCS#8 and as an SPKI public key. |
| `x25519` | 128 | 0 | RFC 7748 | Not listed in SP 800-56A r3 | Not CNSA | Broken by Shor's algorithm on a CRQC | - |
| `ed25519` | 128 | 0 | RFC 8032; FIPS 186-5 | Approved (FIPS 186-5); quantum-vulnerable (IR 8547) | Not CNSA | Broken by Shor's algorithm on a CRQC | SHA-512 is used internally (implicit). |
| `ml-kem-768` | 192 | 3 | FIPS 203 | Approved | Not CNSA 2.0 (ML-KEM-1024 required) | Designed to resist CRQC | Uses SHA3/SHAKE internally (implicit). |
| `ml-dsa-65` | 192 | 3 | FIPS 204 | Approved | Not CNSA 2.0 (ML-DSA-87 required) | Designed to resist CRQC | One OID names both the subjectPublicKeyInfo algorithm and the signature algorithm. |
| `rsa-1024` | 80 | 0 | FIPS 186-5; RFC 8017 | Disallowed (below 112 bits of security; SP 800-131A r2) | Not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | - |
| `rsa-2048` | 112 | 0 | FIPS 186-5; RFC 8017 | Acceptable (112 bits); quantum-vulnerable - deprecated after 2030, disallowed after 2035 (NIST IR 8547) | Not CNSA (CNSA 1.0 requires >= 3072 bits) | Broken by Shor's algorithm on a CRQC | - |
| `rsa-4096` | 128 | 0 | FIPS 186-5; RFC 8017 | Acceptable; quantum-vulnerable - disallowed after 2035 (NIST IR 8547) | CNSA 1.0 only; not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | SP 800-57 Pt 1 r5 places 4096-bit RSA in the 128-bit category (3072 <= k < 7680). |
| `ecdsa-p256` | 128 | 0 | FIPS 186-5; SP 800-186; RFC 5480 | Approved; quantum-vulnerable (IR 8547) | Not CNSA (P-384 required) | Broken by Shor's algorithm on a CRQC | subjectPublicKeyInfo algorithm id-ecPublicKey with namedCurve prime256v1 (1.2.840.10045.3.1.7). |
| `ecdsa-p384` | 192 | 0 | FIPS 186-5; SP 800-186; RFC 5480 | Approved; quantum-vulnerable (IR 8547) | CNSA 1.0 (P-384); not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | subjectPublicKeyInfo algorithm id-ecPublicKey with namedCurve secp384r1 (1.3.132.0.34). |
| `sha256-with-rsa` | - | - | RFC 8017; RFC 4055; FIPS 186-5 | Approved; quantum-vulnerable (IR 8547) | Not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | X.509 signature algorithm; its strength is that of the signer's RSA key. |
| `sha1-with-rsa` | 63 | 0 | RFC 8017; RFC 3279 | Disallowed for signature generation (SP 800-131A r2) | Not CNSA 2.0 | Already broken classically (SHA-1 chosen-prefix collisions) | - |
| `ecdsa-with-sha384` | - | - | FIPS 186-5; RFC 5758 | Approved; quantum-vulnerable (IR 8547) | CNSA 1.0 with P-384; not CNSA 2.0 | Broken by Shor's algorithm on a CRQC | X.509 signature algorithm; the curve is that of the signer's key. |
| `x25519mlkem768` | 192 | 3 | draft-ietf-tls-ecdhe-mlkem; FIPS 203; RFC 7748 | ML-KEM-768 Approved (FIPS 203); the X25519 component is not NIST-approved | Not CNSA 2.0 (ML-KEM-1024 required) | Resists a CRQC as long as ML-KEM-768 does (hybrid) | TLS NamedGroup 0x11EC: the ML-KEM-768 and X25519 shared secrets are concatenated. |

## Protocol

| Property | Value |
|---|---|
| Asset | `tls13-openssl` |
| Type / version | tls 1.3 |
| Cipher suites | TLS_AES_256_GCM_SHA384 (0x13,0x02): aes-256-gcm, sha-384; TLS_CHACHA20_POLY1305_SHA256 (0x13,0x03): chacha20-poly1305, sha-256 |
| Key-exchange groups | `x25519mlkem768`, `x25519` |
| Note | MinProtocol = MaxProtocol = TLSv1.3. Groups lists the hybrid X25519MLKEM768 first, then X25519; signature algorithms are left at the OpenSSL defaults and are not recorded. |
| Occurrences | AR-130, AR-131, AR-132, AR-137 |

## Related cryptographic material

| Asset | Name | Type | Size (bits) | Algorithm | Scenario | Protected by | Stored in | Note |
|---|---|---|---|---|---|---|---|---|
| `m.root-ca-public-key` | Root CA public key (RSA-4096) | public-key | 4096 | `rsa-4096` | A01 | - | pki/root-ca.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo); pki/ca-chain.pem (PEM block 2 (CERTIFICATE) > subjectPublicKeyInfo); pki/fullchain.p7b (PKCS#7 certificate 3 > subjectPublicKeyInfo); keystores/truststore.jks (JKS trustedCertEntry 'cbomfuse-test-root-ca' > subjectPublicKeyInfo) | - |
| `m.issuing-ca-private-key` | Issuing CA private key (ECDSA P-384) | private-key | 384 | `ecdsa-p384` | A01 | - | pki/issuing-ca.key (PEM block 1 (EC PRIVATE KEY)) | - |
| `m.issuing-ca-public-key` | Issuing CA public key (ECDSA P-384) | public-key | 384 | `ecdsa-p384` | A01 | - | pki/issuing-ca.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo); pki/issuing-ca.key (PEM block 1 (EC PRIVATE KEY) > public key); pki/ca-chain.pem (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo); pki/fullchain.p7b (PKCS#7 certificate 2 > subjectPublicKeyInfo); keystores/client.p12 (PKCS#12 encryptedData safe > certBag 2 > subjectPublicKeyInfo, encrypted) | - |
| `m.server-private-key` | TLS server private key (RSA-2048) | private-key | 2048 | `rsa-2048` | A02 | - | pki/server.key (PEM block 1 (RSA PRIVATE KEY)) | - |
| `m.server-public-key` | TLS server public key (RSA-2048) | public-key | 2048 | `rsa-2048` | A02 | - | pki/server.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo); pki/server.key (PEM block 1 (RSA PRIVATE KEY) > public key); pki/server.csr (PEM block 1 (CERTIFICATE REQUEST) > subjectPublicKeyInfo); pki/fullchain.p7b (PKCS#7 certificate 1 > subjectPublicKeyInfo) | - |
| `m.api-private-key` | API endpoint private key (ECDSA P-256) | private-key | 256 | `ecdsa-p256` | A03 | - | pki/api.key (PEM block 1 (PRIVATE KEY)) | - |
| `m.api-public-key` | API endpoint public key (ECDSA P-256) | public-key | 256 | `ecdsa-p256` | A03 | - | pki/api.der (DER file > subjectPublicKeyInfo); pki/api.key (PEM block 1 (PRIVATE KEY) > public key) | - |
| `m.client-private-key` | client svc-reporting private key (ECDSA P-256) | private-key | 256 | `ecdsa-p256` | A09 | PKCS#12 shrouded key bag, PBES2 (PBKDF2-HMAC-SHA256, 20000 iterations; AES-256-CBC) | keystores/client.p12 (PKCS#12 pkcs8ShroudedKeyBag, encrypted) | - |
| `m.client-public-key` | client svc-reporting public key (ECDSA P-256) | public-key | 256 | `ecdsa-p256` | A09 | - | keystores/client.p12 (PKCS#12 encryptedData safe > certBag 1 > subjectPublicKeyInfo, encrypted); keystores/client.p12 (PKCS#12 pkcs8ShroudedKeyBag > public key, encrypted) | - |
| `m.device-private-key` | device-42 private key (Ed25519) | private-key | 256 | `ed25519` | A06 | - | keys/device-ed25519.pem (PEM block 1 (PRIVATE KEY)) | - |
| `m.device-public-key` | device-42 public key (Ed25519) | public-key | 256 | `ed25519` | A06 | - | pki/device-ed25519.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo) | - |
| `m.legacy-public-key` | legacy service public key (RSA-1024) | public-key | 1024 | `rsa-1024` | A05 | - | pki/legacy-sha1.cer (DER file > subjectPublicKeyInfo) | - |
| `m.partner-ca-public-key` | partner root CA public key (RSA-2048) | public-key | 2048 | `rsa-2048` | A10 | - | keystores/truststore.jks (JKS trustedCertEntry 'cbomfuse-partner-root-ca' > subjectPublicKeyInfo) | - |
| `m.backup-private-key` | backup private key (RSA-3072) | private-key | 3072 | `rsa-3072` | A07 | PBES2 (PBKDF2-HMAC-SHA256, 2048 iterations; AES-256-CBC) | keys/backup-rsa3072.enc.pem (PEM block 1 (ENCRYPTED PRIVATE KEY), encrypted) | - |
| `m.backup-public-key` | backup public key (RSA-3072) | public-key | 3072 | `rsa-3072` | A07 | - | keys/backup-rsa3072.enc.pem (PEM block 1 (ENCRYPTED PRIVATE KEY) > public key, encrypted); keys/backup-rsa3072.pub.pem (PEM block 1 (PUBLIC KEY)) | - |
| `m.deploy-private-key` | OpenSSH deploy key private key (Ed25519) | private-key | 256 | `ed25519` | A08 | - | keys/deploy_ed25519 (PEM block 1 (OPENSSH PRIVATE KEY)) | - |
| `m.deploy-public-key` | OpenSSH deploy key public key (Ed25519) | public-key | 256 | `ed25519` | A08 | - | keys/deploy_ed25519 (PEM block 1 (OPENSSH PRIVATE KEY) > public key); keys/deploy_ed25519.pub (OpenSSH public key line) | - |
| `m.pq-root-private-key` | PQC root CA private key (ML-DSA-65) | private-key | - | `ml-dsa-65` | A14 | - | pqc/pq-root-ca.key (PEM block 1 (PRIVATE KEY)) | Seed form (32 bytes) in PKCS#8 |
| `m.pq-root-public-key` | PQC root CA public key (ML-DSA-65) | public-key | 15616 | `ml-dsa-65` | A14 | - | pqc/pq-root-ca.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo) | 1952 bytes |
| `m.kem-endpoint-private-key` | KEM endpoint private key (ML-KEM-768) | private-key | - | `ml-kem-768` | A14 | - | pqc/kem-endpoint.key (PEM block 1 (PRIVATE KEY)) | Seed form (64 bytes) in PKCS#8 |
| `m.kem-endpoint-public-key` | KEM endpoint public key (ML-KEM-768) | public-key | 9472 | `ml-kem-768` | A14 | - | pqc/kem-endpoint.crt (PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo) | Encapsulation key, 1184 bytes |
| `m.server-csr` | Certificate signing request for server.cbom-corpus.example | other | - | `sha256-with-rsa` | A02 | - | pki/server.csr (PEM block 1 (CERTIFICATE REQUEST)) | PKCS#10; CycloneDX has no material type for a CSR, so type is 'other' |
| `m.issuing-ca-crl` | CRL of the CBOMFuse Test Issuing CA | other | - | `ecdsa-with-sha384` | A04 | - | pki/issuing-ca.crl (PEM block 1 (X509 CRL)) | CycloneDX has no material type for a CRL, so type is 'other' |
| `m.jwt-signing-key` | HS256 JWT signing key | secret-key | 256 | `hmac-sha256` | A11 | - | secrets/app.env (JWT_SIGNING_KEY) | base64url, 32 bytes |
| `m.service-token` | Service JWT (HS256) | token | - | `hmac-sha256` | A11 | - | secrets/app.env (SERVICE_TOKEN) | Signed with m.jwt-signing-key; expires 2027-01-01 |
| `m.keystore-password` | Keystore password (client.p12 and truststore.jks) | password | 64 | `pbkdf2-hmac-sha256` | A11 | - | secrets/app.env (KEYSTORE_PASSWORD) | JDK default store password |
| `m.backup-passphrase` | Passphrase of the encrypted backup key | password | 192 | `pbkdf2-hmac-sha256` | A11 | - | secrets/app.env (BACKUP_KEY_PASSPHRASE) | - |
| `m.db-password` | Reporting database password | password | 128 | - | A12 | - | secrets/main.tf (resource "aws_db_instance" "reporting" > password) | - |

Secret values are not repeated in this README, the CBOM or the ledger; `ground-truth.json` gives their SHA-256 (`valueSha256`) so a reported value can be checked.

## Occurrence ledger

Every occurrence, in file order. Nested rows (signature algorithm, public key, PBES2 parameters) name their container.

| ID | File | Scn | Role | Asset (^parent) | Location | Nest | Container | Scope | Symbol | Encoding | Encrypted | Evidence | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AR-001 | `pki/root-ca.crt` | A01 | `obj:x509` | `cert.root-ca` | 1:1-31:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-31` | - |
| AR-002 | `pki/root-ca.crt` | A01 | `alg:signatureAlgorithm` | `sha256-with-rsa` | 1:1-31:26 | 1 | AR-001 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-003 | `pki/root-ca.crt` | A01 | `alg:subjectPublicKeyInfo` | `rsa-4096` | 1:1-31:26 | 1 | AR-001 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-004 | `pki/root-ca.crt` | A01 | `obj:spki` | `m.root-ca-public-key` | 1:1-31:26 | 1 | AR-001 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-005 | `pki/root-ca.crt` | A01 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | 1:1-31:26 | 2 | AR-001 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-006 | `pki/issuing-ca.crt` | A01 | `obj:x509` | `cert.issuing-ca` | 1:1-23:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-23` | - |
| AR-007 | `pki/issuing-ca.crt` | A01 | `alg:signatureAlgorithm` | `sha256-with-rsa` | 1:1-23:26 | 1 | AR-006 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-008 | `pki/issuing-ca.crt` | A01 | `alg:subjectPublicKeyInfo` | `ecdsa-p384` | 1:1-23:26 | 1 | AR-006 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-009 | `pki/issuing-ca.crt` | A01 | `obj:spki` | `m.issuing-ca-public-key` | 1:1-23:26 | 1 | AR-006 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-010 | `pki/issuing-ca.crt` | A01 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | 1:1-23:26 | 2 | AR-006 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-011 | `pki/issuing-ca.key` | A01 | `obj:sec1` | `m.issuing-ca-private-key` | 1:1-6:29 | 0 | - | `PEM block 1 (EC PRIVATE KEY)` | `EC PRIVATE KEY` | PEM | - | `PEM EC PRIVATE KEY block, lines 1-6` | sec1 |
| AR-012 | `pki/issuing-ca.key` | A01 | `alg:privateKeyAlgorithm` | `ecdsa-p384` | 1:1-6:29 | 1 | AR-011 | `PEM block 1 (EC PRIVATE KEY) > algorithm` | `1.3.132.0.34` | PEM | - | `key algorithm 1.3.132.0.34` | - |
| AR-013 | `pki/issuing-ca.key` | A01 | `obj:public-key` | `m.issuing-ca-public-key` | 1:1-6:29 | 1 | AR-011 | `PEM block 1 (EC PRIVATE KEY) > public key` | `publicKey` | PEM | - | `public key stored with the private key` | - |
| AR-014 | `pki/ca-chain.pem` | A01 | `obj:x509` | `cert.issuing-ca` | 3:1-25:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 3-25` | pem-preamble |
| AR-015 | `pki/ca-chain.pem` | A01 | `alg:signatureAlgorithm` | `sha256-with-rsa` | 3:1-25:26 | 1 | AR-014 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-016 | `pki/ca-chain.pem` | A01 | `alg:subjectPublicKeyInfo` | `ecdsa-p384` | 3:1-25:26 | 1 | AR-014 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-017 | `pki/ca-chain.pem` | A01 | `obj:spki` | `m.issuing-ca-public-key` | 3:1-25:26 | 1 | AR-014 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-018 | `pki/ca-chain.pem` | A01 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | 3:1-25:26 | 2 | AR-014 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-019 | `pki/ca-chain.pem` | A01 | `obj:x509` | `cert.root-ca` | 28:1-58:26 | 0 | - | `PEM block 2 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 28-58` | pem-preamble |
| AR-020 | `pki/ca-chain.pem` | A01 | `alg:signatureAlgorithm` | `sha256-with-rsa` | 28:1-58:26 | 1 | AR-019 | `PEM block 2 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-021 | `pki/ca-chain.pem` | A01 | `alg:subjectPublicKeyInfo` | `rsa-4096` | 28:1-58:26 | 1 | AR-019 | `PEM block 2 (CERTIFICATE) > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-022 | `pki/ca-chain.pem` | A01 | `obj:spki` | `m.root-ca-public-key` | 28:1-58:26 | 1 | AR-019 | `PEM block 2 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-023 | `pki/ca-chain.pem` | A01 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | 28:1-58:26 | 2 | AR-019 | `PEM block 2 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-024 | `pki/server.crt` | A02 | `obj:x509` | `cert.server` | 1:1-19:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-19` | - |
| AR-025 | `pki/server.crt` | A02 | `alg:signatureAlgorithm` | `ecdsa-with-sha384` | 1:1-19:26 | 1 | AR-024 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PEM | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | - |
| AR-026 | `pki/server.crt` | A02 | `alg:subjectPublicKeyInfo` | `rsa-2048` | 1:1-19:26 | 1 | AR-024 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-027 | `pki/server.crt` | A02 | `obj:spki` | `m.server-public-key` | 1:1-19:26 | 1 | AR-024 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-028 | `pki/server.crt` | A02 | `alg:signatureAlgorithm` | `sha-384` ^`ecdsa-with-sha384` | 1:1-19:26 | 2 | AR-024 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PEM | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | nested-hash |
| AR-029 | `pki/server.key` | A02 | `obj:pkcs1` | `m.server-private-key` | 1:1-27:30 | 0 | - | `PEM block 1 (RSA PRIVATE KEY)` | `RSA PRIVATE KEY` | PEM | - | `PEM RSA PRIVATE KEY block, lines 1-27` | pkcs1 |
| AR-030 | `pki/server.key` | A02 | `alg:privateKeyAlgorithm` | `rsa-2048` | 1:1-27:30 | 1 | AR-029 | `PEM block 1 (RSA PRIVATE KEY) > algorithm` | `RSA PRIVATE KEY` | PEM | - | `key algorithm RSA PRIVATE KEY` | - |
| AR-031 | `pki/server.key` | A02 | `obj:public-key` | `m.server-public-key` | 1:1-27:30 | 1 | AR-029 | `PEM block 1 (RSA PRIVATE KEY) > public key` | `publicKey` | PEM | - | `public key stored with the private key` | - |
| AR-032 | `pki/server.csr` | A02 | `obj:pkcs10` | `m.server-csr` | 1:1-17:34 | 0 | - | `PEM block 1 (CERTIFICATE REQUEST)` | `CERTIFICATE REQUEST` | PEM | - | `PEM CERTIFICATE REQUEST block, lines 1-17` | csr |
| AR-033 | `pki/server.csr` | A02 | `alg:signatureAlgorithm` | `sha256-with-rsa` | 1:1-17:34 | 1 | AR-032 | `PEM block 1 (CERTIFICATE REQUEST) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-034 | `pki/server.csr` | A02 | `alg:subjectPublicKeyInfo` | `rsa-2048` | 1:1-17:34 | 1 | AR-032 | `PEM block 1 (CERTIFICATE REQUEST) > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-035 | `pki/server.csr` | A02 | `obj:spki` | `m.server-public-key` | 1:1-17:34 | 1 | AR-032 | `PEM block 1 (CERTIFICATE REQUEST) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-036 | `pki/server.csr` | A02 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | 1:1-17:34 | 2 | AR-032 | `PEM block 1 (CERTIFICATE REQUEST) > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PEM | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-037 | `pki/fullchain.p7b` | A02 | `obj:x509` | `cert.server` | bytes 45-836 | 0 | - | `PKCS#7 certificate 1` | `certificates` | PKCS#7 DER | - | `<certificate 1 of 3, bytes 45-836>` | pkcs7 |
| AR-038 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `ecdsa-with-sha384` | bytes 45-836 | 1 | AR-037 | `PKCS#7 certificate 1 > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | - |
| AR-039 | `pki/fullchain.p7b` | A02 | `alg:subjectPublicKeyInfo` | `rsa-2048` | bytes 45-836 | 1 | AR-037 | `PKCS#7 certificate 1 > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PKCS#7 DER | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-040 | `pki/fullchain.p7b` | A02 | `obj:spki` | `m.server-public-key` | bytes 45-836 | 1 | AR-037 | `PKCS#7 certificate 1 > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PKCS#7 DER | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-041 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `sha-384` ^`ecdsa-with-sha384` | bytes 45-836 | 2 | AR-037 | `PKCS#7 certificate 1 > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | nested-hash |
| AR-042 | `pki/fullchain.p7b` | A02 | `obj:x509` | `cert.issuing-ca` | bytes 836-1809 | 0 | - | `PKCS#7 certificate 2` | `certificates` | PKCS#7 DER | - | `<certificate 2 of 3, bytes 836-1809>` | pkcs7 |
| AR-043 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `sha256-with-rsa` | bytes 836-1809 | 1 | AR-042 | `PKCS#7 certificate 2 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-044 | `pki/fullchain.p7b` | A02 | `alg:subjectPublicKeyInfo` | `ecdsa-p384` | bytes 836-1809 | 1 | AR-042 | `PKCS#7 certificate 2 > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | PKCS#7 DER | - | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-045 | `pki/fullchain.p7b` | A02 | `obj:spki` | `m.issuing-ca-public-key` | bytes 836-1809 | 1 | AR-042 | `PKCS#7 certificate 2 > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PKCS#7 DER | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-046 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | bytes 836-1809 | 2 | AR-042 | `PKCS#7 certificate 2 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-047 | `pki/fullchain.p7b` | A02 | `obj:x509` | `cert.root-ca` | bytes 1809-3172 | 0 | - | `PKCS#7 certificate 3` | `certificates` | PKCS#7 DER | - | `<certificate 3 of 3, bytes 1809-3172>` | pkcs7 |
| AR-048 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `sha256-with-rsa` | bytes 1809-3172 | 1 | AR-047 | `PKCS#7 certificate 3 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-049 | `pki/fullchain.p7b` | A02 | `alg:subjectPublicKeyInfo` | `rsa-4096` | bytes 1809-3172 | 1 | AR-047 | `PKCS#7 certificate 3 > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | PKCS#7 DER | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-050 | `pki/fullchain.p7b` | A02 | `obj:spki` | `m.root-ca-public-key` | bytes 1809-3172 | 1 | AR-047 | `PKCS#7 certificate 3 > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PKCS#7 DER | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-051 | `pki/fullchain.p7b` | A02 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | bytes 1809-3172 | 2 | AR-047 | `PKCS#7 certificate 3 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#7 DER | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-052 | `pki/api.der` | A03 | `obj:x509` | `cert.api` | bytes 0-583 | 0 | - | `DER file` | `Certificate` | DER | - | `<DER certificate, 583 bytes>` | der |
| AR-053 | `pki/api.der` | A03 | `alg:signatureAlgorithm` | `ecdsa-with-sha384` | bytes 0-583 | 1 | AR-052 | `DER file > signatureAlgorithm` | `1.2.840.10045.4.3.3` | DER | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | - |
| AR-054 | `pki/api.der` | A03 | `alg:subjectPublicKeyInfo` | `ecdsa-p256` | bytes 0-583 | 1 | AR-052 | `DER file > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | DER | - | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-055 | `pki/api.der` | A03 | `obj:spki` | `m.api-public-key` | bytes 0-583 | 1 | AR-052 | `DER file > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | DER | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-056 | `pki/api.der` | A03 | `alg:signatureAlgorithm` | `sha-384` ^`ecdsa-with-sha384` | bytes 0-583 | 2 | AR-052 | `DER file > signatureAlgorithm` | `1.2.840.10045.4.3.3` | DER | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | nested-hash |
| AR-057 | `pki/api.key` | A03 | `obj:pkcs8` | `m.api-private-key` | 1:1-5:26 | 0 | - | `PEM block 1 (PRIVATE KEY)` | `PRIVATE KEY` | PEM | - | `PEM PRIVATE KEY block, lines 1-5` | pkcs8 |
| AR-058 | `pki/api.key` | A03 | `alg:privateKeyAlgorithm` | `ecdsa-p256` | 1:1-5:26 | 1 | AR-057 | `PEM block 1 (PRIVATE KEY) > algorithm` | `1.2.840.10045.2.1` | PEM | - | `key algorithm 1.2.840.10045.2.1` | - |
| AR-059 | `pki/api.key` | A03 | `obj:public-key` | `m.api-public-key` | 1:1-5:26 | 1 | AR-057 | `PEM block 1 (PRIVATE KEY) > public key` | `publicKey` | PEM | - | `public key stored with the private key` | - |
| AR-060 | `pki/issuing-ca.crl` | A04 | `obj:crl` | `m.issuing-ca-crl` | 1:1-9:23 | 0 | - | `PEM block 1 (X509 CRL)` | `X509 CRL` | PEM | - | `PEM X509 CRL block, lines 1-9` | crl |
| AR-061 | `pki/issuing-ca.crl` | A04 | `alg:signatureAlgorithm` | `ecdsa-with-sha384` | 1:1-9:23 | 1 | AR-060 | `PEM block 1 (X509 CRL) > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PEM | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | - |
| AR-062 | `pki/issuing-ca.crl` | A04 | `alg:signatureAlgorithm` | `sha-384` ^`ecdsa-with-sha384` | 1:1-9:23 | 2 | AR-060 | `PEM block 1 (X509 CRL) > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PEM | - | `signatureAlgorithm 1.2.840.10045.4.3.3` | nested-hash |
| AR-063 | `pki/legacy-sha1.cer` | A05 | `obj:x509` | `cert.legacy` | bytes 0-598 | 0 | - | `DER file` | `Certificate` | DER | - | `<DER certificate, 598 bytes>` | der |
| AR-064 | `pki/legacy-sha1.cer` | A05 | `alg:signatureAlgorithm` | `sha1-with-rsa` | bytes 0-598 | 1 | AR-063 | `DER file > signatureAlgorithm` | `1.2.840.113549.1.1.5` | DER | - | `signatureAlgorithm 1.2.840.113549.1.1.5` | - |
| AR-065 | `pki/legacy-sha1.cer` | A05 | `alg:subjectPublicKeyInfo` | `rsa-1024` | bytes 0-598 | 1 | AR-063 | `DER file > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | DER | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-066 | `pki/legacy-sha1.cer` | A05 | `obj:spki` | `m.legacy-public-key` | bytes 0-598 | 1 | AR-063 | `DER file > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | DER | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-067 | `pki/legacy-sha1.cer` | A05 | `alg:signatureAlgorithm` | `sha-1` ^`sha1-with-rsa` | bytes 0-598 | 2 | AR-063 | `DER file > signatureAlgorithm` | `1.2.840.113549.1.1.5` | DER | - | `signatureAlgorithm 1.2.840.113549.1.1.5` | nested-hash |
| AR-068 | `pki/device-ed25519.crt` | A06 | `obj:x509` | `cert.device` | 1:1-12:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-12` | - |
| AR-069 | `pki/device-ed25519.crt` | A06 | `alg:signatureAlgorithm` | `ed25519` | 1:1-12:26 | 1 | AR-068 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `1.3.101.112` | PEM | - | `signatureAlgorithm 1.3.101.112` | - |
| AR-070 | `pki/device-ed25519.crt` | A06 | `alg:subjectPublicKeyInfo` | `ed25519` | 1:1-12:26 | 1 | AR-068 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `1.3.101.112` | PEM | - | `subjectPublicKeyInfo.algorithm 1.3.101.112` | - |
| AR-071 | `pki/device-ed25519.crt` | A06 | `obj:spki` | `m.device-public-key` | 1:1-12:26 | 1 | AR-068 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-072 | `keys/device-ed25519.pem` | A06 | `obj:pkcs8` | `m.device-private-key` | 1:1-3:26 | 0 | - | `PEM block 1 (PRIVATE KEY)` | `PRIVATE KEY` | PEM | - | `PEM PRIVATE KEY block, lines 1-3` | pkcs8 |
| AR-073 | `keys/device-ed25519.pem` | A06 | `alg:privateKeyAlgorithm` | `ed25519` | 1:1-3:26 | 1 | AR-072 | `PEM block 1 (PRIVATE KEY) > algorithm` | `1.3.101.112` | PEM | - | `key algorithm 1.3.101.112` | - |
| AR-074 | `keys/backup-rsa3072.enc.pem` | A07 | `obj:pkcs8-encrypted` | `m.backup-private-key` | 1:1-42:36 | 0 | - | `PEM block 1 (ENCRYPTED PRIVATE KEY)` | `ENCRYPTED PRIVATE KEY` | PEM | yes | `PEM ENCRYPTED PRIVATE KEY block, lines 1-42` | pkcs8-encrypted |
| AR-075 | `keys/backup-rsa3072.enc.pem` | A07 | `alg:privateKeyAlgorithm` | `rsa-3072` | 1:1-42:36 | 1 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > algorithm` | `1.2.840.113549.1.1.1` | PEM | yes | `key algorithm 1.2.840.113549.1.1.1` | - |
| AR-076 | `keys/backup-rsa3072.enc.pem` | A07 | `obj:public-key` | `m.backup-public-key` | 1:1-42:36 | 1 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > public key` | `publicKey` | PEM | yes | `public key stored with the private key` | - |
| AR-077 | `keys/backup-rsa3072.enc.pem` | A07 | `alg:pbes2.kdf` | `pbkdf2-hmac-sha256` | 1:1-42:36 | 1 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > PBES2 keyDerivationFunc` | `1.2.840.113549.1.5.12` | PEM | - | `PBKDF2, 2048 iterations` | pkcs8-encrypted |
| AR-078 | `keys/backup-rsa3072.enc.pem` | A07 | `alg:pbes2.enc` | `aes-256-cbc` | 1:1-42:36 | 1 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > PBES2 encryptionScheme` | `2.16.840.1.101.3.4.1.42` | PEM | - | `encryptionScheme aes256-CBC` | pkcs8-encrypted |
| AR-079 | `keys/backup-rsa3072.enc.pem` | A07 | `alg:pbkdf2.prf` | `hmac-sha256` ^`pbkdf2-hmac-sha256` | 1:1-42:36 | 2 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > PBKDF2 prf` | `1.2.840.113549.2.9` | PEM | - | `prf hmacWithSHA256` | - |
| AR-080 | `keys/backup-rsa3072.enc.pem` | A07 | `alg:pbkdf2.prf` | `sha-256` ^`hmac-sha256` | 1:1-42:36 | 3 | AR-074 | `PEM block 1 (ENCRYPTED PRIVATE KEY) > PBKDF2 prf` | `1.2.840.113549.2.9` | PEM | - | `prf hmacWithSHA256` | nested-hash |
| AR-081 | `keys/backup-rsa3072.pub.pem` | A07 | `obj:spki` | `m.backup-public-key` | 1:1-11:25 | 0 | - | `PEM block 1 (PUBLIC KEY)` | `PUBLIC KEY` | PEM | - | `PEM PUBLIC KEY block, lines 1-11` | spki |
| AR-082 | `keys/backup-rsa3072.pub.pem` | A07 | `alg:subjectPublicKeyInfo` | `rsa-3072` | 1:1-11:25 | 1 | AR-081 | `PEM block 1 (PUBLIC KEY) > algorithm` | `1.2.840.113549.1.1.1` | PEM | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-083 | `keys/deploy_ed25519` | A08 | `obj:openssh` | `m.deploy-private-key` | 1:1-7:34 | 0 | - | `PEM block 1 (OPENSSH PRIVATE KEY)` | `OPENSSH PRIVATE KEY` | PEM | - | `PEM OPENSSH PRIVATE KEY block, lines 1-7` | openssh |
| AR-084 | `keys/deploy_ed25519` | A08 | `alg:privateKeyAlgorithm` | `ed25519` | 1:1-7:34 | 1 | AR-083 | `PEM block 1 (OPENSSH PRIVATE KEY) > algorithm` | `ssh-ed25519` | PEM | - | `key algorithm ssh-ed25519` | - |
| AR-085 | `keys/deploy_ed25519` | A08 | `obj:public-key` | `m.deploy-public-key` | 1:1-7:34 | 1 | AR-083 | `PEM block 1 (OPENSSH PRIVATE KEY) > public key` | `publicKey` | PEM | - | `public key stored with the private key` | - |
| AR-086 | `keys/deploy_ed25519.pub` | A08 | `obj:openssh-pub` | `m.deploy-public-key` | 1:1-1:108 | 0 | - | `OpenSSH public key line` | `ssh-ed25519` | OpenSSH | - | `ssh-ed25519 AAAA… deploy@cbom-corpus.example` | openssh-pub |
| AR-087 | `keys/deploy_ed25519.pub` | A08 | `alg:key-type` | `ed25519` | 1:1-1:12 | 1 | AR-086 | `OpenSSH public key line > key type` | `ssh-ed25519` | OpenSSH | - | `ssh-ed25519` | - |
| AR-088 | `keystores/client.p12` | A09 | `alg:pbes2.kdf` | `pbkdf2-hmac-sha256` | bytes 90-141 | 0 | - | `PKCS#12 encryptedData safe > PBES2 keyDerivationFunc` | `1.2.840.113549.1.5.12` | PKCS#12 | - | `PBKDF2, 20000 iterations` | pkcs12 |
| AR-089 | `keystores/client.p12` | A09 | `alg:pbkdf2.prf` | `hmac-sha256` ^`pbkdf2-hmac-sha256` | bytes 127-141 | 1 | - | `PKCS#12 encryptedData safe > PBKDF2 prf` | `1.2.840.113549.2.9` | PKCS#12 | - | `prf hmacWithSHA256` | - |
| AR-090 | `keystores/client.p12` | A09 | `alg:pbkdf2.prf` | `sha-256` ^`hmac-sha256` | bytes 127-141 | 2 | - | `PKCS#12 encryptedData safe > PBKDF2 prf` | `1.2.840.113549.2.9` | PKCS#12 | - | `prf hmacWithSHA256` | nested-hash |
| AR-091 | `keystores/client.p12` | A09 | `alg:pbes2.enc` | `aes-256-cbc` | bytes 141-172 | 0 | - | `PKCS#12 encryptedData safe > PBES2 encryptionScheme` | `2.16.840.1.101.3.4.1.42` | PKCS#12 | - | `encryptionScheme aes256-CBC` | pkcs12 |
| AR-092 | `keystores/client.p12` | A09 | `obj:x509` | `cert.client` | bytes 172-1888 | 0 | - | `PKCS#12 encryptedData safe > certBag 1` | `certBag` | PKCS#12 | yes | `<encrypted certBag 1>` | pkcs12 |
| AR-093 | `keystores/client.p12` | A09 | `obj:x509` | `cert.issuing-ca` | bytes 172-1888 | 0 | - | `PKCS#12 encryptedData safe > certBag 2` | `certBag` | PKCS#12 | yes | `<encrypted certBag 2>` | pkcs12 |
| AR-094 | `keystores/client.p12` | A09 | `alg:signatureAlgorithm` | `ecdsa-with-sha384` | bytes 172-1888 | 1 | AR-092 | `PKCS#12 encryptedData safe > certBag 1 > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PKCS#12 | yes | `signatureAlgorithm 1.2.840.10045.4.3.3` | - |
| AR-095 | `keystores/client.p12` | A09 | `alg:subjectPublicKeyInfo` | `ecdsa-p256` | bytes 172-1888 | 1 | AR-092 | `PKCS#12 encryptedData safe > certBag 1 > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | PKCS#12 | yes | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-096 | `keystores/client.p12` | A09 | `obj:spki` | `m.client-public-key` | bytes 172-1888 | 1 | AR-092 | `PKCS#12 encryptedData safe > certBag 1 > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PKCS#12 | yes | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-097 | `keystores/client.p12` | A09 | `alg:signatureAlgorithm` | `sha256-with-rsa` | bytes 172-1888 | 1 | AR-093 | `PKCS#12 encryptedData safe > certBag 2 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#12 | yes | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-098 | `keystores/client.p12` | A09 | `alg:subjectPublicKeyInfo` | `ecdsa-p384` | bytes 172-1888 | 1 | AR-093 | `PKCS#12 encryptedData safe > certBag 2 > subjectPublicKeyInfo` | `1.2.840.10045.2.1` | PKCS#12 | yes | `subjectPublicKeyInfo.algorithm 1.2.840.10045.2.1` | - |
| AR-099 | `keystores/client.p12` | A09 | `obj:spki` | `m.issuing-ca-public-key` | bytes 172-1888 | 1 | AR-093 | `PKCS#12 encryptedData safe > certBag 2 > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PKCS#12 | yes | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-100 | `keystores/client.p12` | A09 | `alg:signatureAlgorithm` | `sha-384` ^`ecdsa-with-sha384` | bytes 172-1888 | 2 | AR-092 | `PKCS#12 encryptedData safe > certBag 1 > signatureAlgorithm` | `1.2.840.10045.4.3.3` | PKCS#12 | yes | `signatureAlgorithm 1.2.840.10045.4.3.3` | nested-hash |
| AR-101 | `keystores/client.p12` | A09 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | bytes 172-1888 | 2 | AR-093 | `PKCS#12 encryptedData safe > certBag 2 > signatureAlgorithm` | `1.2.840.113549.1.1.11` | PKCS#12 | yes | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-102 | `keystores/client.p12` | A09 | `alg:pbes2.kdf` | `pbkdf2-hmac-sha256` | bytes 1953-2004 | 1 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > PBES2 keyDerivationFunc` | `1.2.840.113549.1.5.12` | PKCS#12 | - | `PBKDF2, 20000 iterations` | pkcs12 |
| AR-103 | `keystores/client.p12` | A09 | `alg:pbkdf2.prf` | `hmac-sha256` ^`pbkdf2-hmac-sha256` | bytes 1990-2004 | 2 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > PBKDF2 prf` | `1.2.840.113549.2.9` | PKCS#12 | - | `prf hmacWithSHA256` | - |
| AR-104 | `keystores/client.p12` | A09 | `alg:pbkdf2.prf` | `sha-256` ^`hmac-sha256` | bytes 1990-2004 | 3 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > PBKDF2 prf` | `1.2.840.113549.2.9` | PKCS#12 | - | `prf hmacWithSHA256` | nested-hash |
| AR-105 | `keystores/client.p12` | A09 | `alg:pbes2.enc` | `aes-256-cbc` | bytes 2004-2035 | 1 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > PBES2 encryptionScheme` | `2.16.840.1.101.3.4.1.42` | PKCS#12 | - | `encryptionScheme aes256-CBC` | pkcs12 |
| AR-106 | `keystores/client.p12` | A09 | `obj:pkcs8-shrouded` | `m.client-private-key` | bytes 2035-2182 | 0 | - | `PKCS#12 pkcs8ShroudedKeyBag` | `pkcs8ShroudedKeyBag` | PKCS#12 | yes | `<encrypted PKCS#8 key bag>` | pkcs12 |
| AR-107 | `keystores/client.p12` | A09 | `alg:privateKeyAlgorithm` | `ecdsa-p256` | bytes 2035-2182 | 1 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > algorithm` | `1.2.840.10045.2.1` | PKCS#12 | yes | `key algorithm 1.2.840.10045.2.1` | - |
| AR-108 | `keystores/client.p12` | A09 | `obj:public-key` | `m.client-public-key` | bytes 2035-2182 | 1 | AR-106 | `PKCS#12 pkcs8ShroudedKeyBag > public key` | `publicKey` | PKCS#12 | yes | `public key stored with the private key` | - |
| AR-109 | `keystores/client.p12` | A09 | `alg:mac` | `hmac-sha256` | bytes 2264-2331 | 0 | - | `PKCS#12 MacData` | `2.16.840.1.101.3.4.2.1` | PKCS#12 | - | `MacData: HMAC with SHA-256, PKCS#12 KDF, 2048 iterations` | pkcs12 |
| AR-110 | `keystores/client.p12` | A09 | `alg:mac` | `sha-256` ^`hmac-sha256` | bytes 2268-2283 | 1 | AR-109 | `PKCS#12 MacData > digestAlgorithm` | `2.16.840.1.101.3.4.2.1` | PKCS#12 | - | `digestAlgorithm sha256` | nested-hash |
| AR-111 | `keystores/truststore.jks` | A10 | `obj:x509` | `cert.root-ca` | bytes 58-1421 | 0 | - | `JKS trustedCertEntry 'cbomfuse-test-root-ca'` | `cbomfuse-test-root-ca` | JKS | - | `<trustedCertEntry 'cbomfuse-test-root-ca', bytes 58-1421>` | jks |
| AR-112 | `keystores/truststore.jks` | A10 | `alg:signatureAlgorithm` | `sha256-with-rsa` | bytes 58-1421 | 1 | AR-111 | `JKS trustedCertEntry 'cbomfuse-test-root-ca' > signatureAlgorithm` | `1.2.840.113549.1.1.11` | JKS | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-113 | `keystores/truststore.jks` | A10 | `alg:subjectPublicKeyInfo` | `rsa-4096` | bytes 58-1421 | 1 | AR-111 | `JKS trustedCertEntry 'cbomfuse-test-root-ca' > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | JKS | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-114 | `keystores/truststore.jks` | A10 | `obj:spki` | `m.root-ca-public-key` | bytes 58-1421 | 1 | AR-111 | `JKS trustedCertEntry 'cbomfuse-test-root-ca' > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | JKS | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-115 | `keystores/truststore.jks` | A10 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | bytes 58-1421 | 2 | AR-111 | `JKS trustedCertEntry 'cbomfuse-test-root-ca' > signatureAlgorithm` | `1.2.840.113549.1.1.11` | JKS | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-116 | `keystores/truststore.jks` | A10 | `obj:x509` | `cert.partner-ca` | bytes 1470-2325 | 0 | - | `JKS trustedCertEntry 'cbomfuse-partner-root-ca'` | `cbomfuse-partner-root-ca` | JKS | - | `<trustedCertEntry 'cbomfuse-partner-root-ca', bytes 1470-2325>` | jks |
| AR-117 | `keystores/truststore.jks` | A10 | `alg:signatureAlgorithm` | `sha256-with-rsa` | bytes 1470-2325 | 1 | AR-116 | `JKS trustedCertEntry 'cbomfuse-partner-root-ca' > signatureAlgorithm` | `1.2.840.113549.1.1.11` | JKS | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | - |
| AR-118 | `keystores/truststore.jks` | A10 | `alg:subjectPublicKeyInfo` | `rsa-2048` | bytes 1470-2325 | 1 | AR-116 | `JKS trustedCertEntry 'cbomfuse-partner-root-ca' > subjectPublicKeyInfo` | `1.2.840.113549.1.1.1` | JKS | - | `subjectPublicKeyInfo.algorithm 1.2.840.113549.1.1.1` | - |
| AR-119 | `keystores/truststore.jks` | A10 | `obj:spki` | `m.partner-ca-public-key` | bytes 1470-2325 | 1 | AR-116 | `JKS trustedCertEntry 'cbomfuse-partner-root-ca' > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | JKS | - | `subjectPublicKeyInfo.subjectPublicKey` | - |
| AR-120 | `keystores/truststore.jks` | A10 | `alg:signatureAlgorithm` | `sha-256` ^`sha256-with-rsa` | bytes 1470-2325 | 2 | AR-116 | `JKS trustedCertEntry 'cbomfuse-partner-root-ca' > signatureAlgorithm` | `1.2.840.113549.1.1.11` | JKS | - | `signatureAlgorithm 1.2.840.113549.1.1.11` | nested-hash |
| AR-121 | `keystores/truststore.jks` | A10 | `alg:integrity` | `sha-1` | bytes 2325-2345 | 0 | - | `JKS keystore digest` | `SHA-1(password \|\| 'Mighty Aphrodite' \|\| entries)` | JKS | - | `<20-byte SHA-1 keystore digest>` | jks |
| AR-122 | `secrets/app.env` | A11 | `cfg:JWT_ALGORITHM` | `hmac-sha256` | 4:15-4:20 | 0 | - | `JWT_ALGORITHM` | `HS256` | dotenv | - | `JWT_ALGORITHM=HS256` | jwt |
| AR-123 | `secrets/app.env` | A11 | `cfg:JWT_ALGORITHM` | `sha-256` ^`hmac-sha256` | 4:15-4:20 | 1 | - | `JWT_ALGORITHM` | `HS256` | dotenv | - | `JWT_ALGORITHM=HS256` | nested-hash |
| AR-124 | `secrets/app.env` | A11 | `mat:JWT_SIGNING_KEY` | `m.jwt-signing-key` | 5:17-5:60 | 0 | - | `JWT_SIGNING_KEY` | `JWT_SIGNING_KEY` | dotenv | - | `JWT_SIGNING_KEY=<43 characters>` | env-secret |
| AR-125 | `secrets/app.env` | A11 | `mat:SERVICE_TOKEN` | `m.service-token` | 6:15-6:284 | 0 | - | `SERVICE_TOKEN` | `SERVICE_TOKEN` | dotenv | - | `SERVICE_TOKEN=<269 characters>` | jwt |
| AR-126 | `secrets/app.env` | A11 | `alg:jwt.alg` | `hmac-sha256` | 6:15-6:51 | 1 | - | `SERVICE_TOKEN > JOSE header` | `HS256` | base64url | - | `JOSE header {"alg":"HS256",…}` | jwt |
| AR-127 | `secrets/app.env` | A11 | `mat:KEYSTORE_PASSWORD` | `m.keystore-password` | 9:19-9:27 | 0 | - | `KEYSTORE_PASSWORD` | `KEYSTORE_PASSWORD` | dotenv | - | `KEYSTORE_PASSWORD=<8 characters>` | low-entropy-secret |
| AR-128 | `secrets/app.env` | A11 | `mat:BACKUP_KEY_PASSPHRASE` | `m.backup-passphrase` | 11:23-11:47 | 0 | - | `BACKUP_KEY_PASSPHRASE` | `BACKUP_KEY_PASSPHRASE` | dotenv | - | `BACKUP_KEY_PASSPHRASE=<24 characters>` | env-secret |
| AR-129 | `secrets/main.tf` | A12 | `mat:password` | `m.db-password` | 7:21-7:37 | 0 | - | `resource "aws_db_instance" "reporting" > password` | `aws_db_instance.reporting.password` | HCL | - | `password = "<16 characters>"` | tf-secret |
| AR-130 | `tls/openssl.cnf` | A13 | `cfg:MinProtocol` | `tls13-openssl` | 13:15-13:22 | 0 | - | `[system_default_sect] MinProtocol` | `MinProtocol` | text | - | `MinProtocol = TLSv1.3` | openssl-cnf |
| AR-131 | `tls/openssl.cnf` | A13 | `cfg:MaxProtocol` | `tls13-openssl` | 14:15-14:22 | 0 | - | `[system_default_sect] MaxProtocol` | `MaxProtocol` | text | - | `MaxProtocol = TLSv1.3` | openssl-cnf |
| AR-132 | `tls/openssl.cnf` | A13 | `cfg:Ciphersuites` | `tls13-openssl` | 15:16-15:67 | 0 | - | `[system_default_sect] Ciphersuites` | `Ciphersuites` | text | - | `Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256` | openssl-cnf |
| AR-133 | `tls/openssl.cnf` | A13 | `alg:cipher-suite` | `aes-256-gcm` ^`tls13-openssl` | 15:16-15:38 | 1 | AR-132 | `[system_default_sect] Ciphersuites > TLS_AES_256_GCM_SHA384` | `TLS_AES_256_GCM_SHA384` | text | - | `TLS_AES_256_GCM_SHA384` | suite-name |
| AR-134 | `tls/openssl.cnf` | A13 | `alg:cipher-suite` | `sha-384` ^`tls13-openssl` | 15:16-15:38 | 1 | AR-132 | `[system_default_sect] Ciphersuites > TLS_AES_256_GCM_SHA384` | `TLS_AES_256_GCM_SHA384` | text | - | `TLS_AES_256_GCM_SHA384` | suite-name |
| AR-135 | `tls/openssl.cnf` | A13 | `alg:cipher-suite` | `chacha20-poly1305` ^`tls13-openssl` | 15:39-15:67 | 1 | AR-132 | `[system_default_sect] Ciphersuites > TLS_CHACHA20_POLY1305_SHA256` | `TLS_CHACHA20_POLY1305_SHA256` | text | - | `TLS_CHACHA20_POLY1305_SHA256` | suite-name |
| AR-136 | `tls/openssl.cnf` | A13 | `alg:cipher-suite` | `sha-256` ^`tls13-openssl` | 15:39-15:67 | 1 | AR-132 | `[system_default_sect] Ciphersuites > TLS_CHACHA20_POLY1305_SHA256` | `TLS_CHACHA20_POLY1305_SHA256` | text | - | `TLS_CHACHA20_POLY1305_SHA256` | suite-name |
| AR-137 | `tls/openssl.cnf` | A13 | `cfg:Groups` | `tls13-openssl` | 16:10-16:31 | 0 | - | `[system_default_sect] Groups` | `Groups` | text | - | `Groups = X25519MLKEM768:X25519` | openssl-cnf |
| AR-138 | `tls/openssl.cnf` | A13 | `alg:group` | `x25519mlkem768` ^`tls13-openssl` | 16:10-16:24 | 1 | AR-137 | `[system_default_sect] Groups > X25519MLKEM768` | `X25519MLKEM768` | text | - | `X25519MLKEM768` | hybrid-group |
| AR-139 | `tls/openssl.cnf` | A13 | `alg:group` | `ml-kem-768` ^`x25519mlkem768` | 16:10-16:24 | 2 | AR-137 | `[system_default_sect] Groups > X25519MLKEM768` | `X25519MLKEM768` | text | - | `X25519MLKEM768` | hybrid-group |
| AR-140 | `tls/openssl.cnf` | A13 | `alg:group` | `x25519` ^`x25519mlkem768` | 16:10-16:24 | 2 | AR-137 | `[system_default_sect] Groups > X25519MLKEM768` | `X25519MLKEM768` | text | - | `X25519MLKEM768` | hybrid-group |
| AR-141 | `tls/openssl.cnf` | A13 | `alg:group` | `x25519` ^`tls13-openssl` | 16:25-16:31 | 1 | AR-137 | `[system_default_sect] Groups > X25519` | `X25519` | text | - | `X25519` | - |
| AR-142 | `pqc/pq-root-ca.crt` | A14 | `obj:x509` | `cert.pq-root-ca` | 1:1-119:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-119` | - |
| AR-143 | `pqc/pq-root-ca.crt` | A14 | `alg:signatureAlgorithm` | `ml-dsa-65` | 1:1-119:26 | 1 | AR-142 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `2.16.840.1.101.3.4.3.18` | PEM | - | `signatureAlgorithm 2.16.840.1.101.3.4.3.18` | pqc-oid |
| AR-144 | `pqc/pq-root-ca.crt` | A14 | `alg:subjectPublicKeyInfo` | `ml-dsa-65` | 1:1-119:26 | 1 | AR-142 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `2.16.840.1.101.3.4.3.18` | PEM | - | `subjectPublicKeyInfo.algorithm 2.16.840.1.101.3.4.3.18` | pqc-oid |
| AR-145 | `pqc/pq-root-ca.crt` | A14 | `obj:spki` | `m.pq-root-public-key` | 1:1-119:26 | 1 | AR-142 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | pqc-oid |
| AR-146 | `pqc/pq-root-ca.key` | A14 | `obj:pkcs8` | `m.pq-root-private-key` | 1:1-4:26 | 0 | - | `PEM block 1 (PRIVATE KEY)` | `PRIVATE KEY` | PEM | - | `PEM PRIVATE KEY block, lines 1-4` | pkcs8-seed |
| AR-147 | `pqc/pq-root-ca.key` | A14 | `alg:privateKeyAlgorithm` | `ml-dsa-65` | 1:1-4:26 | 1 | AR-146 | `PEM block 1 (PRIVATE KEY) > algorithm` | `2.16.840.1.101.3.4.3.18` | PEM | - | `key algorithm 2.16.840.1.101.3.4.3.18` | pqc-oid |
| AR-148 | `pqc/kem-endpoint.crt` | A14 | `obj:x509` | `cert.kem-endpoint` | 1:1-104:26 | 0 | - | `PEM block 1 (CERTIFICATE)` | `CERTIFICATE` | PEM | - | `PEM CERTIFICATE block, lines 1-104` | - |
| AR-149 | `pqc/kem-endpoint.crt` | A14 | `alg:signatureAlgorithm` | `ml-dsa-65` | 1:1-104:26 | 1 | AR-148 | `PEM block 1 (CERTIFICATE) > signatureAlgorithm` | `2.16.840.1.101.3.4.3.18` | PEM | - | `signatureAlgorithm 2.16.840.1.101.3.4.3.18` | pqc-oid |
| AR-150 | `pqc/kem-endpoint.crt` | A14 | `alg:subjectPublicKeyInfo` | `ml-kem-768` | 1:1-104:26 | 1 | AR-148 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `2.16.840.1.101.3.4.4.2` | PEM | - | `subjectPublicKeyInfo.algorithm 2.16.840.1.101.3.4.4.2` | pqc-oid |
| AR-151 | `pqc/kem-endpoint.crt` | A14 | `obj:spki` | `m.kem-endpoint-public-key` | 1:1-104:26 | 1 | AR-148 | `PEM block 1 (CERTIFICATE) > subjectPublicKeyInfo` | `subjectPublicKeyInfo` | PEM | - | `subjectPublicKeyInfo.subjectPublicKey` | pqc-oid |
| AR-152 | `pqc/kem-endpoint.key` | A14 | `obj:pkcs8` | `m.kem-endpoint-private-key` | 1:1-4:26 | 0 | - | `PEM block 1 (PRIVATE KEY)` | `PRIVATE KEY` | PEM | - | `PEM PRIVATE KEY block, lines 1-4` | pkcs8-seed |
| AR-153 | `pqc/kem-endpoint.key` | A14 | `alg:privateKeyAlgorithm` | `ml-kem-768` | 1:1-4:26 | 1 | AR-152 | `PEM block 1 (PRIVATE KEY) > algorithm` | `2.16.840.1.101.3.4.4.2` | PEM | - | `key algorithm 2.16.840.1.101.3.4.4.2` | pqc-oid |

## Non-asset mentions (negative ground truth)

Every PEM armour that does not enclose a decodable object, and every case-insensitive match of the algorithm-name lexicon (`_tooling/spec.py`, `DECOY_PATTERN`) outside all occurrence spans, in every text file of the case. A scanner that reports one of these as a cryptographic asset produces a false positive.

| ID | File | L:C | Match | Context | Line | Why it is not an asset |
|---|---|---|---|---|---|---|
| AR-N001 | `secrets/app.env` | 10:29 | `rsa` | config-value | `BACKUP_KEY_FILE=keys/backup-rsa3072.enc.pem` | Configuration value (a file path or label) that names an algorithm but is not a crypto asset |
| AR-N002 | `tls/openssl.cnf` | 2:31 | `tls` | comment | `# Loaded through OPENSSL_CONF=tls/openssl.cnf; restricts every TLS context to ve` | Comment text; documentation only |
| AR-N003 | `tls/openssl.cnf` | 2:64 | `TLS` | comment | `# Loaded through OPENSSL_CONF=tls/openssl.cnf; restricts every TLS context to ve` | Comment text; documentation only |
| AR-N004 | `examples/placeholder.crt` | 1:6 | `BEGIN CERTIFICATE` | pem-armour | `BEGIN CERTIFICATE` | PEM armour around a body that does not decode (placeholder or shortened example); not a cryptographic object |
| AR-N005 | `examples/deploy-notes.md` | 10:6 | `BEGIN PRIVATE KEY` | pem-armour | `BEGIN PRIVATE KEY` | PEM armour around a body that does not decode (placeholder or shortened example); not a cryptographic object |
| AR-N006 | `examples/deploy-notes.md` | 16:16 | `RSA` | documentation | `Plan: move the RSA-2048 server key to ECDSA P-384 or ML-DSA-65 once every client` | Prose in a Markdown document; documentation only |
| AR-N007 | `examples/deploy-notes.md` | 16:39 | `ECDSA` | documentation | `Plan: move the RSA-2048 server key to ECDSA P-384 or ML-DSA-65 once every client` | Prose in a Markdown document; documentation only |
| AR-N008 | `examples/deploy-notes.md` | 16:54 | `ML-DSA-65` | documentation | `Plan: move the RSA-2048 server key to ECDSA P-384 or ML-DSA-65 once every client` | Prose in a Markdown document; documentation only |
| AR-N009 | `examples/deploy-notes.md` | 17:11 | `SHA-1` | documentation | `accepting SHA-1 signatures.` | Prose in a Markdown document; documentation only |

## Detection notes

| Note | Explanation | Occurrences |
|---|---|---|
| `nested-hash` | Hash named only as part of a composite signature algorithm identifier | 21 (AR-005 …) |
| `sec1` | SEC 1 ECPrivateKey: the curve OID and the public point are stored with the private scalar | AR-011 |
| `pem-preamble` | Free text (subject=/issuer= lines as printed by openssl) precedes each PEM block | AR-014, AR-019 |
| `pkcs1` | PKCS#1 RSAPrivateKey: the algorithm is implied by the PEM label; modulus and public exponent are stored with the private key | AR-029 |
| `csr` | PKCS#10 certificate request: signed by the key it asks to have certified | AR-032 |
| `pkcs7` | PKCS#7 / CMS SignedData with certificates and no signers (.p7b) | AR-037, AR-042, AR-047 |
| `der` | Binary DER without PEM armour; found only by file extension or content sniffing | AR-052, AR-063 |
| `pkcs8` | PKCS#8 PrivateKeyInfo with its algorithm identifier | AR-057, AR-072 |
| `crl` | X.509 CRL: signed list of revoked serial numbers | AR-060 |
| `pkcs8-encrypted` | Encrypted PKCS#8 (PBES2): the key and its algorithm are inside the ciphertext; the passphrase is in secrets/app.env | AR-074, AR-077, AR-078 |
| `spki` | Subject public key info | AR-081 |
| `openssh` | OpenSSH openssh-key-v1 container: key type string, public key and private key | AR-083 |
| `openssh-pub` | One-line OpenSSH public key (type, base64 blob, comment) | AR-086 |
| `pkcs12` | Inside a password-protected PKCS#12 file; certificates and key are encrypted (PBES2) and readable only with the password (changeit) | 8 (AR-088 …) |
| `jks` | Inside a Java KeyStore; trusted certificate entries are stored in clear, the file is integrity-protected with the store password (changeit) | AR-111, AR-116, AR-121 |
| `jwt` | JSON Web Token: the algorithm is named in its base64url-encoded header | AR-122, AR-125, AR-126 |
| `env-secret` | Secret assigned in a dotenv file | AR-124, AR-128 |
| `low-entropy-secret` | Default or low-entropy value: entropy-based secret scanners do not report it | AR-127 |
| `tf-secret` | Secret in a Terraform resource; gitleaks applies its Terraform password rule only to *.tf and *.hcl paths | AR-129 |
| `openssl-cnf` | OpenSSL configuration directive in the system default section | 4 (AR-130 …) |
| `suite-name` | Algorithms named inside a TLS cipher-suite name | 4 (AR-133 …) |
| `hybrid-group` | Hybrid post-quantum TLS key-exchange group (ML-KEM-768 + X25519) | AR-138, AR-139, AR-140 |
| `pqc-oid` | Post-quantum algorithm identified only by its OID; libraries without ML-DSA / ML-KEM support reject the object | 8 (AR-143 …) |
| `pkcs8-seed` | PKCS#8 private key in seed form: the public key is not stored and must be derived | AR-146, AR-152 |

## Verification

`_tooling/artifacts.py` parsed every file with cryptography 50.0.1 (OpenSSL 4.0.2 25 Aug 2026) and stopped on the first mismatch. 139 checks passed, among them: every certificate's subject, issuer, serial, validity, signature algorithm and key match the registry and its signature verifies under its issuer (including the SHA-1 and ML-DSA-65 signatures); every copy of a certificate is byte-identical; every private key matches its certificate or public key; the CSR and CRL signatures verify; the encrypted PKCS#8 key opens with the passphrase from `secrets/app.env`, the PKCS#12 file and the JKS digest with `changeit`; the JWT verifies with the HS256 key next to it; the two decoys do not decode. The full list is in `ground-truth.json` (`verification.details`).

To regenerate: `cd _tooling && python3 artifacts.py` rewrites this README, `cbom.cdx.json` and `ground-truth.json` from the files; `python3 artifacts.py generate --force` first replaces every key, certificate and secret with new random ones.
