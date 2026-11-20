# CBOM ground-truth corpus: one cryptographic program in five languages

The same program is implemented in **Python, Java, Go, TypeScript and C#**. It runs 24 scenarios covering hashing, an XOF, MAC, KDFs and password hashing, AEAD and block-cipher modes, legacy ciphers, RSA, elliptic-curve signatures and key agreement, ML-KEM and ML-DSA, an X.509 certificate and a TLS 1.3 configuration, across 23 library components in total. Each language directory contains the program, its build manifest, and a README.md that records **every occurrence of every cryptographic asset** with exact coordinates, role, API symbol, library, scope, scenario and asset properties, plus a ground-truth CycloneDX 1.6 CBOM and a JSON ledger.

## Layout

```text
.
├── README.md               this file
├── expected_output.txt     stdout shared by all five programs
├── Python/                 crypto_showcase.py, requirements.txt, README.md, cbom.cdx.json, ground-truth.json
├── Java/                   src/main/java/corpus/CryptoShowcase.java, pom.xml, ...
├── Go/                     main.go, go.mod, ...
├── TypeScript/             src/main.ts, package.json, tsconfig.json, ...
├── CSharp/                 Program.cs, CryptoShowcase.csproj, ...
└── _tooling/               annotated templates and the generator that produced the ground truth
```

`CSharp/` is spelled out because `#` breaks some shells, URLs and build tools. Scan the five language directories, not the archive root: `_tooling/templates` contains annotated copies of every program (with `.tmpl` extensions) and would double-count.

## Verified equivalence

All five programs were built and run; their standard output is byte-identical (31 lines, see `expected_output.txt`). Deterministic scenarios reproduce published test vectors: SHA-256/512, SHA3-256, BLAKE2b-512, MD5, SHA-1, SHAKE128 and HMAC-SHA256 of the 'quick brown fox' message, RFC 5869 A.1 (HKDF), RFC 7914 sections 11 and 12 (PBKDF2, scrypt), GCM test case 16 (AES-256-GCM), FIPS 197 C.1 (first AES-128-ECB block) and the RFC 8032 TEST 1 public key (Ed25519).

| Language | Toolchain | How it was built and run | Result |
|---|---|---|---|
| Python | CPython 3.12.3 (Ubuntu 24.04, x86_64) | venv with requirements.txt, python3 crypto_showcase.py | identical |
| Java | OpenJDK 25.0.4.1 | javac/java against Bouncy Castle 1.86 compiled from the r1rv86 tag (also re-run against the 1.80 jars); javac -Xlint:all reported no warnings | identical |
| Go | Go 1.26.8 | go build with x/crypto v0.58.0, CIRCL v1.6.5 and x/sys v0.49.0 from tagged sources; gofmt and go vet clean | identical |
| TypeScript | Node.js 22.22.2 (bundled OpenSSL 3.5.5), TypeScript 7.0.2 | npm install, tsc with 0 diagnostics, node dist/main.js | identical |
| C# | .NET SDK 10.0.113 (runtime 10.0.13) | dotnet build -c Release against BouncyCastle.Cryptography 2.7.0 compiled from the release-2.7.0 tag; 0 warnings | identical |

## Corpus statistics

| Language | Program | Lines | Occurrences | Algorithms | Material | Implicit assets | Libraries | Non-asset mentions |
|---|---|---|---|---|---|---|---|---|
| Python | `Python/crypto_showcase.py` | 365 | 195 | 33 | 49 | 2 | 6 | 164 |
| Java | `Java/src/main/java/corpus/CryptoShowcase.java` | 494 | 331 | 33 | 49 | 2 | 4 | 107 |
| Go | `Go/main.go` | 418 | 181 | 33 | 49 | 3 | 4 | 90 |
| TypeScript | `TypeScript/src/main.ts` | 365 | 192 | 33 | 49 | 3 | 7 | 96 |
| C# | `CSharp/Program.cs` | 407 | 212 | 34 | 49 | 3 | 2 | 95 |

## Scenarios and the APIs that implement them

Each cell lists the operations recorded for that scenario (library ID, then API). The logic is the same everywhere; the APIs, the libraries and the way algorithms are named are deliberately varied.

| Scenario | Python | Java | Go | TypeScript | C# |
|---|---|---|---|---|---|
| **S01** SHA-256 digest of MESSAGE | py-stdlib: `hashlib.sha256` | jdk: `MessageDigest.digest` | go-stdlib: `sha256.Sum256` | node: `Hash.digest` | dotnet: `SHA256.HashData` |
| **S02** SHA-512, SHA3-256 and BLAKE2b-512 digests of MESSAGE | py-stdlib: `hashlib.sha512`<br>pycryptodome: `SHA3_256.new`<br>pyca: `Hash.finalize` | jdk: `MessageDigest.digest`<br>bcprov: `Blake2bDigest.doFinal` | go-stdlib: `sha512.Sum512`, `sha3.Sum256`<br>xcrypto: `blake2b.Sum512` | node: `Hash.digest`<br>noble-hashes: `sha3_256`, `blake2b` | dotnet: `SHA512.HashData`<br>bccs: `DigestUtilities.CalculateDigest`, `Blake2bDigest.DoFinal` |
| **S03** Legacy MD5 and SHA-1 digests of MESSAGE | py-stdlib: `hashlib.md5`<br>pyca: `Hash.finalize` | jdk: `MessageDigest.digest` | go-stdlib: `md5.Sum`, `sha1.Sum` | node: `Hash.digest` | dotnet: `MD5.HashData`, `SHA1.HashData` |
| **S04** SHAKE128 XOF, 32-byte output | py-stdlib: `hashlib.shake_128` | bcprov: `SHAKEDigest.doFinal` | go-stdlib: `sha3.SumSHAKE128` | node: `Hash.digest` | bccs: `ShakeDigest.OutputFinal` |
| **S05** HMAC-SHA256 tag over MESSAGE with a 3-byte hard-coded key | py-stdlib: `hmac.new` | jdk: `Mac.doFinal` | go-stdlib: `Hash.Sum` | node: `Hmac.digest` | dotnet: `HMACSHA256.HashData` |
| **S06** HKDF-SHA256 extract-and-expand, L=42 | pyca: `HKDF.derive` | jdk: `KDF.deriveData` | go-stdlib: `hkdf.Key` | node: `crypto.hkdfSync` | dotnet: `HKDF.DeriveKey` |
| **S07** PBKDF2-HMAC-SHA256, c=80000, dkLen=64 | py-stdlib: `hashlib.pbkdf2_hmac` | jdk: `SecretKeyFactory.generateSecret` | go-stdlib: `pbkdf2.Key` | node: `subtle.deriveBits` | dotnet: `Rfc2898DeriveBytes.Pbkdf2` |
| **S08** scrypt N=16384 r=8 p=1, dkLen=64 | pyca: `Scrypt.derive` | bcprov: `SCrypt.generate` | xcrypto: `scrypt.Key` | node: `crypto.scryptSync` | bccs: `SCrypt.Generate` |
| **S09** Argon2id v1.3 t=2 m=19456 KiB p=1, 32-byte output, fixed salt | argon2-cffi: `low_level.hash_secret_raw` | bcprov: `Argon2BytesGenerator.generateBytes` | xcrypto: `argon2.IDKey` | noble-hashes: `argon2id` | bccs: `Argon2BytesGenerator.GenerateBytes` |
| **S10** bcrypt cost 12 with random salt, then verify | bcrypt: `bcrypt.gensalt`, `bcrypt.hashpw`, `bcrypt.checkpw` | jdk: `SecureRandom.nextBytes`<br>bcprov: `OpenBSDBCrypt.generate`, `OpenBSDBCrypt.checkPassword` | xcrypto: `bcrypt.GenerateFromPassword`, `bcrypt.CompareHashAndPassword` | bcryptjs: `bcryptjs.genSaltSync`, `bcryptjs.hashSync`, `bcryptjs.compareSync` | dotnet: `RandomNumberGenerator.GetBytes`<br>bccs: `OpenBsdBCrypt.Generate`, `OpenBsdBCrypt.CheckPassword` |
| **S11** AES-256-GCM encrypt/decrypt, hard-coded key/IV/AAD | pyca: `AESGCM.encrypt`, `AESGCM.decrypt` | jdk: `Cipher.doFinal` | go-stdlib: `AEAD.Seal`, `AEAD.Open` | node: `Cipheriv.final`, `Decipheriv.final` | dotnet: `AesGcm.Encrypt`, `AesGcm.Decrypt` |
| **S12** ChaCha20-Poly1305 encrypt/decrypt, random key and nonce | pycryptodome: `Random.get_random_bytes`, `ChaCha20Poly1305Cipher.encrypt_and_digest`, `ChaCha20Poly1305Cipher.decrypt_and_verify` | jdk: `KeyGenerator.generateKey`, `SecureRandom.nextBytes`, `Cipher.doFinal` | go-stdlib: `rand.Read`, `AEAD.Seal`, `AEAD.Open` | noble-ciphers: `randomBytes`, `chacha20poly1305.encrypt`, `chacha20poly1305.decrypt` | dotnet: `RandomNumberGenerator.GetBytes`, `ChaCha20Poly1305.Encrypt`, `ChaCha20Poly1305.Decrypt` |
| **S13** AES-256-CBC with PKCS#7 padding, random key and IV | py-stdlib: `os.urandom`<br>pyca: `Cipher.encryptor`, `Cipher.decryptor` | jdk: `KeyGenerator.generateKey`, `SecureRandom.nextBytes`, `Cipher.doFinal` | go-stdlib: `rand.Read`, `BlockMode.CryptBlocks` | node: `crypto.randomBytes`, `Cipheriv.final`, `Decipheriv.final` | dotnet: `SymmetricAlgorithm.GenerateKey`, `RandomNumberGenerator.GetBytes`, `SymmetricAlgorithm.EncryptCbc`, `SymmetricAlgorithm.DecryptCbc` |
| **S14** AES-128-ECB with PKCS#7 padding, hard-coded key | pyca: `Cipher.encryptor` | jdk: `Cipher.doFinal` | go-stdlib: `Block.Encrypt` | node: `Cipheriv.final` | dotnet: `SymmetricAlgorithm.EncryptEcb` |
| **S15** AES-256-CTR, random key and 128-bit initial counter block | py-stdlib: `secrets.token_bytes`<br>pycryptodome: `CtrMode.encrypt`, `CtrMode.decrypt` | jdk: `KeyGenerator.generateKey`, `SecureRandom.nextBytes`, `Cipher.doFinal` | go-stdlib: `rand.Read`, `Stream.XORKeyStream` | node: `subtle.generateKey`, `crypto.getRandomValues`, `subtle.encrypt`, `subtle.decrypt` | dotnet: `RandomNumberGenerator.GetBytes`<br>bccs: `IBufferedCipher.DoFinal` |
| **S16** 3DES (3-key TDEA) CBC with PKCS#7 padding, random key and IV | pycryptodome: `DES3.adjust_key_parity`, `Random.get_random_bytes`, `CbcMode.encrypt`, `CbcMode.decrypt` | jdk: `KeyGenerator.generateKey`, `SecureRandom.nextBytes`, `Cipher.doFinal` | go-stdlib: `rand.Read`, `BlockMode.CryptBlocks` | node: `crypto.randomBytes`, `Cipheriv.final`, `Decipheriv.final` | dotnet: `SymmetricAlgorithm.GenerateKey`, `RandomNumberGenerator.GetBytes`, `SymmetricAlgorithm.EncryptCbc`, `SymmetricAlgorithm.DecryptCbc` |
| **S17** RSA-3072 key pair; RSA-OAEP-SHA256, RSASSA-PSS-SHA256, RSASSA-PKCS1-v1_5-SHA256 | pyca: `rsa.generate_private_key`, `RSAPublicKey.encrypt`, `RSAPrivateKey.decrypt`, `RSAPrivateKey.sign`, `RSAPublicKey.verify` | jdk: `KeyPairGenerator.generateKeyPair`, `Cipher.doFinal`, `Signature.sign`, `Signature.verify` | go-stdlib: `rsa.GenerateKey`, `rsa.EncryptOAEP`, `rsa.DecryptOAEP`, `sha256.Sum256`, `rsa.SignPSS`, `rsa.VerifyPSS`, `rsa.SignPKCS1v15`, `rsa.VerifyPKCS1v15` | node: `crypto.generateKeyPairSync`, `crypto.publicEncrypt`, `crypto.privateDecrypt`, `crypto.sign`, `crypto.verify` | dotnet: `RSA.Create`, `RSA.Encrypt`, `RSA.Decrypt`, `RSA.SignData`, `RSA.VerifyData` |
| **S18** ECDSA P-256 / SHA-256 sign and verify | pyca: `ec.generate_private_key`, `EllipticCurvePrivateKey.sign`, `EllipticCurvePublicKey.verify` | jdk: `KeyPairGenerator.generateKeyPair`, `Signature.sign`, `Signature.verify` | go-stdlib: `ecdsa.GenerateKey`, `sha256.Sum256`, `ecdsa.SignASN1`, `ecdsa.VerifyASN1` | node: `subtle.generateKey`, `subtle.sign`, `subtle.verify` | dotnet: `ECDsa.Create`, `ECDsa.SignData`, `ECDsa.VerifyData` |
| **S19** Ed25519 from a hard-coded seed: public key, signature, verify | pynacl: `SigningKey.sign`, `VerifyKey.verify` | bcprov: `Ed25519PrivateKeyParameters.generatePublicKey`, `Ed25519Signer.generateSignature`, `Ed25519Signer.verifySignature` | go-stdlib: `ed25519.NewKeyFromSeed`, `ed25519.Sign`, `ed25519.Verify` | noble-curves: `ed25519.getPublicKey`, `ed25519.sign`, `ed25519.verify` | bccs: `Ed25519PrivateKeyParameters.GeneratePublicKey`, `Ed25519Signer.GenerateSignature`, `Ed25519Signer.VerifySignature` |
| **S20** X25519 and ECDH P-256 key agreement, HKDF-SHA256 session key over both secrets | pyca: `HKDF.derive`, `X25519PrivateKey.generate`, `X25519PrivateKey.exchange`, `ec.generate_private_key`, `EllipticCurvePrivateKey.exchange` | jdk: `KeyAgreement.generateSecret`, `KDF.deriveData`, `KeyPairGenerator.generateKeyPair` | go-stdlib: `hkdf.Key`, `Curve.GenerateKey`, `PrivateKey.ECDH` | node: `crypto.hkdfSync`, `crypto.generateKeyPairSync`, `crypto.diffieHellman`, `ECDH.generateKeys`, `ECDH.computeSecret` | bccs: `X25519Agreement.CalculateAgreement`, `.ctor`<br>dotnet: `HKDF.DeriveKey`, `ECDiffieHellman.Create`, `ECDiffieHellman.DeriveRawSecretAgreement` |
| **S21** ML-KEM-768 key generation, encapsulation, decapsulation | pyca: `MLKEM768PrivateKey.generate`, `MLKEM768PublicKey.encapsulate`, `MLKEM768PrivateKey.decapsulate` | jdk: `KeyPairGenerator.generateKeyPair`, `Encapsulator.encapsulate`, `Decapsulator.decapsulate` | go-stdlib: `mlkem.GenerateKey768`, `EncapsulationKey768.Encapsulate`, `DecapsulationKey768.Decapsulate` | noble-pq: `ml_kem768.keygen`, `ml_kem768.encapsulate`, `ml_kem768.decapsulate` | bccs: `MLKemKeyPairGenerator.GenerateKeyPair`, `MLKemEncapsulator.Encapsulate`, `MLKemDecapsulator.Decapsulate` |
| **S22** ML-DSA-65 key generation, signing, verification | pyca: `MLDSA65PrivateKey.generate`, `MLDSA65PrivateKey.sign`, `MLDSA65PublicKey.verify` | jdk: `KeyPairGenerator.generateKeyPair`, `Signature.sign`, `Signature.verify` | circl: `mldsa65.GenerateKey`, `mldsa65.SignTo`, `mldsa65.Verify` | noble-pq: `ml_dsa65.keygen`, `ml_dsa65.sign`, `ml_dsa65.verify` | bccs: `MLDsaKeyPairGenerator.GenerateKeyPair`, `MLDsaSigner.GenerateSignature`, `MLDsaSigner.VerifySignature` |
| **S23** Self-signed X.509 v3 certificate (ECDSA P-256 / SHA-256), signature verified | pyca: `ec.generate_private_key`, `CertificateBuilder.sign`, `EllipticCurvePublicKey.verify`<br>py-stdlib: `secrets.randbits` | jdk: `KeyPairGenerator.generateKeyPair`, `BigInteger.<init>`, `X509Certificate.verify`<br>bcpkix: `JcaX509CertificateConverter.getCertificate`, `X509v3CertificateBuilder.build` | go-stdlib: `ecdsa.GenerateKey`, `rand.Int`, `x509.CreateCertificate`, `x509.ParseCertificate`, `Certificate.CheckSignature` | node: `subtle.generateKey`, `crypto.randomBytes`<br>peculiar-x509: `X509CertificateGenerator.createSelfSigned`, `X509Certificate.verify` | dotnet: `ECDsa.Create`, `CertificateRequest.Create`, `RandomNumberGenerator.GetBytes`, `ECDsa.VerifyData` |
| **S24** TLS 1.3-only client configuration (no network I/O) | py-stdlib: `ssl.create_default_context`, `SSLContext.minimum_version`, `SSLContext.maximum_version` | jdk: `SSLContext.getInstance`, `SSLParameters.setProtocols`, `SSLParameters.setCipherSuites`, `SSLContext.createSSLEngine`, `SSLEngine.setUseClientMode`, `SSLEngine.setSSLParameters` | go-stdlib: `tls.Config`, `tls.VersionTLS13` | node: `tls.createSecureContext`, `?` | dotnet: `.ctor`, `SslProtocols.Tls13` |

## How the ground truth was produced

Each program was written once as an annotated template in which every cryptographic span is wrapped in a marker carrying its role, asset, parent asset, produced material, API symbol and a note key (`«ROLE ASSET^PARENT>PRODUCED#SYMBOL!NOTE|code»`). `_tooling/build_sources.py` strips the markers to produce the delivered source and `_tooling/docs.py` computes positions on the stripped text, so coordinates are exact by construction rather than found by searching. Asset properties live in one shared registry (`_tooling/spec.py`), so the same asset ID means the same thing in every language. To change a program, edit its template and run `python3 build_sources.py && python3 docs.py` inside `_tooling/`.

## Caveats

- The build sandbox could not reach Maven Central, NuGet or the Go module proxy. Java was compiled and run against Bouncy Castle 1.86 built from the `r1rv86` source tag (and re-run against the 1.80 jars), C# against BouncyCastle.Cryptography 2.7.0 built from the `release-2.7.0` tag, and Go against x/crypto v0.58.0, CIRCL v1.6.5 and x/sys v0.49.0 from their tagged sources. `pom.xml` and `CryptoShowcase.csproj` pin those same versions but were not themselves exercised through Maven or NuGet.
- `Go/` ships without `go.sum`; run `go mod tidy` once to record checksums.
- Asset-level security levels and compliance statements (`_tooling/spec.py`) are analyst judgements with stated sources (FIPS, SP 800-131A Rev. 2, NIST IR 8547, CNSA 2.0); review them against your own policy baseline.
- 'Implicit' assets (for example the TLS 1.3 cipher suites in Python and Go, or MGF1 in Go, TypeScript and C#) are part of the runtime CBOM but have no source occurrence by design.
