// CBOM ground-truth corpus - C# (.NET) implementation.
//
// Runs scenarios S01-S24 in the same order, with the same inputs and the same
// output lines as the Python, Java, Go and TypeScript implementations. All
// hard-coded keys, IVs, salts and passwords are published test vectors.

using System.Formats.Asn1;
using System.Net.Security;
using System.Security.Authentication;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using Org.BouncyCastle.Crypto.Agreement;
using Org.BouncyCastle.Crypto.Digests;
using Org.BouncyCastle.Crypto.Generators;
using Org.BouncyCastle.Crypto.Kems;
using Org.BouncyCastle.Crypto.Parameters;
using Org.BouncyCastle.Crypto.Signers;
using Org.BouncyCastle.Security;

namespace CbomCorpus;

internal static class CryptoShowcase
{
    private static readonly byte[] Message = Encoding.ASCII.GetBytes("The quick brown fox jumps over the lazy dog");

    // --- Hard-coded material (public test vectors only) ---
    // Wikipedia HMAC example key
    private static readonly byte[] HmacKey = Encoding.ASCII.GetBytes("key");
    // RFC 5869 A.1
    private static readonly byte[] HkdfIkm = Enumerable.Repeat((byte)0x0b, 22).ToArray();
    private static readonly byte[] HkdfSalt = Convert.FromHexString("000102030405060708090a0b0c");
    private static readonly byte[] HkdfInfo = Convert.FromHexString("f0f1f2f3f4f5f6f7f8f9");
    // RFC 7914 sections 11 and 12
    private static readonly byte[] Pbkdf2Password = Encoding.ASCII.GetBytes("Password");
    private static readonly byte[] Pbkdf2Salt = Encoding.ASCII.GetBytes("NaCl");
    private static readonly byte[] ScryptPassword = Encoding.ASCII.GetBytes("pleaseletmein");
    private static readonly byte[] ScryptSalt = Encoding.ASCII.GetBytes("SodiumChloride");
    private const string Password = "correct horse battery staple";
    private static readonly byte[] Argon2Salt = Encoding.ASCII.GetBytes("cbom-corpus-salt");
    // GCM specification test case 16
    private static readonly byte[] GcmKey = Convert.FromHexString("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308");
    private static readonly byte[] GcmIv = Convert.FromHexString("cafebabefacedbaddecaf888");
    private static readonly byte[] GcmAad = Convert.FromHexString("feedfacedeadbeeffeedfacedeadbeefabaddad2");
    private static readonly byte[] GcmPlaintext = Convert.FromHexString(
        "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72" +
        "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39");
    // FIPS 197 appendix C.1
    private static readonly byte[] EcbKey = Convert.FromHexString("000102030405060708090a0b0c0d0e0f");
    private static readonly byte[] EcbPlaintext = Convert.FromHexString("00112233445566778899aabbccddeeff");
    // RFC 8032 section 7.1, TEST 1
    private static readonly byte[] Ed25519Seed = Convert.FromHexString("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60");
    private static readonly byte[] SessionInfo = Encoding.ASCII.GetBytes("cbom-corpus session key v1");
    private const string TlsServerName = "cbom-corpus.example";

    private static readonly SecureRandom BcRandom = new SecureRandom();

    private static string Hex(ReadOnlySpan<byte> bytes) => Convert.ToHexStringLower(bytes);

    private static string Flag(bool ok) => ok ? "true" : "false";

    private static void Emit(string scenario, string label, string value) =>
        Console.Write($"[{scenario}] {label,-18} {value}\n");

    // S01: SHA-256 (FIPS 180-4)
    private static void S01Sha256()
    {
        Emit("S01", "SHA-256", Hex(SHA256.HashData(Message)));
    }

    // S02: SHA-512, SHA3-256, BLAKE2b-512
    private static void S02Sha2Sha3Blake2()
    {
        Emit("S02", "SHA-512", Hex(SHA512.HashData(Message)));
        Emit("S02", "SHA3-256", Hex(DigestUtilities.CalculateDigest("SHA3-256", Message)));
        var blake = new Blake2bDigest(512);
        blake.BlockUpdate(Message, 0, Message.Length);
        var output = new byte[blake.GetDigestSize()];
        blake.DoFinal(output, 0);
        Emit("S02", "BLAKE2b-512", Hex(output));
    }

    // S03: legacy digests - deliberately weak
    private static void S03LegacyHashes()
    {
        Emit("S03", "MD5", Hex(MD5.HashData(Message)));
        Emit("S03", "SHA-1", Hex(SHA1.HashData(Message)));
    }

    // S04: SHAKE128 extendable-output function
    private static void S04Shake128()
    {
        var shake = new ShakeDigest(128);
        shake.BlockUpdate(Message, 0, Message.Length);
        var output = new byte[32];
        shake.OutputFinal(output, 0, output.Length);
        Emit("S04", "SHAKE128", Hex(output));
    }

    // S05: HMAC-SHA256
    private static void S05HmacSha256()
    {
        Emit("S05", "HMAC-SHA256", Hex(HMACSHA256.HashData(HmacKey, Message)));
    }

    // S06: HKDF-SHA256 (RFC 5869)
    private static void S06HkdfSha256()
    {
        var okm = HKDF.DeriveKey(HashAlgorithmName.SHA256, HkdfIkm, 42, HkdfSalt, HkdfInfo);
        Emit("S06", "HKDF-SHA256", Hex(okm));
    }

    // S07: PBKDF2-HMAC-SHA256
    private static void S07Pbkdf2()
    {
        var derived = Rfc2898DeriveBytes.Pbkdf2(Pbkdf2Password, Pbkdf2Salt, 80_000, HashAlgorithmName.SHA256, 64);
        Emit("S07", "PBKDF2-SHA256", Hex(derived));
    }

    // S08: scrypt
    private static void S08Scrypt()
    {
        var derived = SCrypt.Generate(ScryptPassword, ScryptSalt, 1 << 14, 8, 1, 64);
        Emit("S08", "scrypt", Hex(derived));
    }

    // S09: Argon2id
    private static void S09Argon2id()
    {
        var parameters = new Argon2Parameters.Builder(Argon2Parameters.Argon2id)
            .WithVersion(Argon2Parameters.Version13)
            .WithIterations(2)
            .WithMemoryAsKB(19_456)
            .WithParallelism(1)
            .WithSalt(Argon2Salt)
            .Build();
        var generator = new Argon2BytesGenerator();
        generator.Init(parameters);
        var output = new byte[32];
        generator.GenerateBytes(Encoding.ASCII.GetBytes(Password), output);
        Emit("S09", "Argon2id", Hex(output));
    }

    // S10: bcrypt
    private static void S10Bcrypt()
    {
        var salt = RandomNumberGenerator.GetBytes(16);
        var hash = OpenBsdBCrypt.Generate("2b", Password.ToCharArray(), salt, 12);
        var ok = OpenBsdBCrypt.CheckPassword(hash, Password.ToCharArray());
        Emit("S10", "bcrypt", $"verify={Flag(ok)}");
    }

    // S11: AES-256-GCM known-answer test
    private static void S11Aes256Gcm()
    {
        using var aead = new AesGcm(GcmKey, 16);
        var ciphertext = new byte[GcmPlaintext.Length];
        var tag = new byte[16];
        aead.Encrypt(GcmIv, GcmPlaintext, ciphertext, tag, GcmAad);
        var plaintext = new byte[ciphertext.Length];
        aead.Decrypt(GcmIv, ciphertext, tag, plaintext, GcmAad);
        Emit("S11", "AES-256-GCM", $"ct={Hex(ciphertext)} tag={Hex(tag)} roundtrip={Flag(plaintext.AsSpan().SequenceEqual(GcmPlaintext))}");
    }

    // S12: ChaCha20-Poly1305 (RFC 8439)
    private static void S12ChaCha20Poly1305()
    {
        var key = RandomNumberGenerator.GetBytes(32);
        var nonce = RandomNumberGenerator.GetBytes(12);
        using var aead = new ChaCha20Poly1305(key);
        var ciphertext = new byte[Message.Length];
        var tag = new byte[16];
        aead.Encrypt(nonce, Message, ciphertext, tag);
        var plaintext = new byte[ciphertext.Length];
        aead.Decrypt(nonce, ciphertext, tag, plaintext);
        Emit("S12", "ChaCha20-Poly1305", $"roundtrip={Flag(plaintext.AsSpan().SequenceEqual(Message))}");
    }

    // S13: AES-256-CBC with PKCS#7 padding
    private static void S13Aes256Cbc()
    {
        using var aes = Aes.Create();
        aes.KeySize = 256;
        aes.GenerateKey();
        var iv = RandomNumberGenerator.GetBytes(16);
        var ciphertext = aes.EncryptCbc(Message, iv, PaddingMode.PKCS7);
        var plaintext = aes.DecryptCbc(ciphertext, iv, PaddingMode.PKCS7);
        Emit("S13", "AES-256-CBC", $"roundtrip={Flag(plaintext.AsSpan().SequenceEqual(Message))}");
    }

    // S14: AES-128-ECB known-answer test - deliberately weak mode
    private static void S14Aes128Ecb()
    {
        using var aes = Aes.Create();
        aes.Key = EcbKey;
        var ciphertext = aes.EncryptEcb(EcbPlaintext, PaddingMode.PKCS7);
        Emit("S14", "AES-128-ECB", Hex(ciphertext));
    }

    // S15: AES-256-CTR (Bouncy Castle; .NET has no CTR mode)
    private static void S15Aes256Ctr()
    {
        var key = RandomNumberGenerator.GetBytes(32);
        var counterBlock = RandomNumberGenerator.GetBytes(16);
        var encryptor = CipherUtilities.GetCipher("AES/CTR/NoPadding");
        encryptor.Init(true, new ParametersWithIV(new KeyParameter(key), counterBlock));
        var ciphertext = encryptor.DoFinal(Message);
        var decryptor = CipherUtilities.GetCipher("AES/CTR/NoPadding");
        decryptor.Init(false, new ParametersWithIV(new KeyParameter(key), counterBlock));
        var plaintext = decryptor.DoFinal(ciphertext);
        Emit("S15", "AES-256-CTR", $"roundtrip={Flag(plaintext.AsSpan().SequenceEqual(Message))}");
    }

    // S16: 3DES (TDEA) CBC - deliberately legacy
    private static void S16TdeaCbc()
    {
        using var tdes = TripleDES.Create();
        tdes.GenerateKey();
        var iv = RandomNumberGenerator.GetBytes(8);
        var ciphertext = tdes.EncryptCbc(Message, iv, PaddingMode.PKCS7);
        var plaintext = tdes.DecryptCbc(ciphertext, iv, PaddingMode.PKCS7);
        Emit("S16", "3DES-CBC", $"roundtrip={Flag(plaintext.AsSpan().SequenceEqual(Message))}");
    }

    // S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair
    private static void S17Rsa3072()
    {
        using var rsa = RSA.Create(3072);

        var ciphertext = rsa.Encrypt(Message, RSAEncryptionPadding.OaepSHA256);
        var plaintext = rsa.Decrypt(ciphertext, RSAEncryptionPadding.OaepSHA256);
        Emit("S17", "RSA-3072 OAEP", $"roundtrip={Flag(plaintext.AsSpan().SequenceEqual(Message))}");

        var pssSignature = rsa.SignData(Message, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
        var pssOk = rsa.VerifyData(Message, pssSignature, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
        Emit("S17", "RSA-3072 PSS", $"verify={Flag(pssOk)}");

        var pkcs1Signature = rsa.SignData(Message, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        var pkcs1Ok = rsa.VerifyData(Message, pkcs1Signature, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        Emit("S17", "RSA-3072 PKCS1v15", $"verify={Flag(pkcs1Ok)}");
    }

    // S18: ECDSA P-256 with SHA-256
    private static void S18EcdsaP256()
    {
        using var ecdsa = ECDsa.Create(ECCurve.NamedCurves.nistP256);
        var signature = ecdsa.SignData(Message, HashAlgorithmName.SHA256);
        var ok = ecdsa.VerifyData(Message, signature, HashAlgorithmName.SHA256);
        Emit("S18", "ECDSA P-256", $"verify={Flag(ok)}");
    }

    // S19: Ed25519 from a fixed seed (RFC 8032)
    private static void S19Ed25519()
    {
        var privateKey = new Ed25519PrivateKeyParameters(Ed25519Seed);
        var publicKey = privateKey.GeneratePublicKey();
        var signer = new Ed25519Signer();
        signer.Init(true, privateKey);
        signer.BlockUpdate(Message, 0, Message.Length);
        var signature = signer.GenerateSignature();
        var verifier = new Ed25519Signer();
        verifier.Init(false, publicKey);
        verifier.BlockUpdate(Message, 0, Message.Length);
        var ok = verifier.VerifySignature(signature);
        Emit("S19", "Ed25519", $"pk={Hex(publicKey.GetEncoded())} sig={Hex(signature)} verify={Flag(ok)}");
    }

    private static byte[] X25519Agree(X25519PrivateKeyParameters privateKey, X25519PublicKeyParameters peerKey)
    {
        var agreement = new X25519Agreement();
        agreement.Init(privateKey);
        var secret = new byte[agreement.AgreementSize];
        agreement.CalculateAgreement(peerKey, secret, 0);
        return secret;
    }

    private static byte[] DeriveSessionKey(byte[] sharedSecret)
    {
        return HKDF.DeriveKey(HashAlgorithmName.SHA256, sharedSecret, 32, salt: null, info: SessionInfo);
    }

    // S20: X25519 + ECDH P-256 key agreement, HKDF session key
    private static void S20KeyAgreement()
    {
        var alice = new X25519PrivateKeyParameters(BcRandom);
        var bob = new X25519PrivateKeyParameters(BcRandom);
        var xAlice = X25519Agree(alice, bob.GeneratePublicKey());
        var xBob = X25519Agree(bob, alice.GeneratePublicKey());
        Emit("S20", "X25519", $"agree={Flag(xAlice.AsSpan().SequenceEqual(xBob))}");

        using var aliceEc = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256);
        using var bobEc = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256);
        var zAlice = aliceEc.DeriveRawSecretAgreement(bobEc.PublicKey);
        var zBob = bobEc.DeriveRawSecretAgreement(aliceEc.PublicKey);
        Emit("S20", "ECDH P-256", $"agree={Flag(zAlice.AsSpan().SequenceEqual(zBob))}");

        var kAlice = DeriveSessionKey([.. xAlice, .. zAlice]);
        var kBob = DeriveSessionKey([.. xBob, .. zBob]);
        Emit("S20", "HKDF session key", $"match={Flag(kAlice.AsSpan().SequenceEqual(kBob))}");
    }

    // S21: ML-KEM-768 (FIPS 203)
    private static void S21MlKem768()
    {
        var generator = new MLKemKeyPairGenerator();
        generator.Init(new MLKemKeyGenerationParameters(BcRandom, MLKemParameters.ml_kem_768));
        var keyPair = generator.GenerateKeyPair();
        var encapsulator = new MLKemEncapsulator(MLKemParameters.ml_kem_768);
        encapsulator.Init(keyPair.Public);
        var ciphertext = new byte[encapsulator.EncapsulationLength];
        var sharedSecret = new byte[encapsulator.SecretLength];
        encapsulator.Encapsulate(ciphertext, 0, ciphertext.Length, sharedSecret, 0, sharedSecret.Length);
        var decapsulator = new MLKemDecapsulator(MLKemParameters.ml_kem_768);
        decapsulator.Init(keyPair.Private);
        var recovered = new byte[decapsulator.SecretLength];
        decapsulator.Decapsulate(ciphertext, 0, ciphertext.Length, recovered, 0, recovered.Length);
        Emit("S21", "ML-KEM-768", $"agree={Flag(sharedSecret.AsSpan().SequenceEqual(recovered))} ct={ciphertext.Length} ss={sharedSecret.Length}");
    }

    // S22: ML-DSA-65 (FIPS 204)
    private static void S22MlDsa65()
    {
        var generator = new MLDsaKeyPairGenerator();
        generator.Init(new MLDsaKeyGenerationParameters(BcRandom, MLDsaParameters.ml_dsa_65));
        var keyPair = generator.GenerateKeyPair();
        var signer = new MLDsaSigner(MLDsaParameters.ml_dsa_65, deterministic: false);
        signer.Init(true, new ParametersWithRandom(keyPair.Private, BcRandom));
        signer.BlockUpdate(Message, 0, Message.Length);
        var signature = signer.GenerateSignature();
        var verifier = new MLDsaSigner(MLDsaParameters.ml_dsa_65, deterministic: false);
        verifier.Init(false, keyPair.Public);
        verifier.BlockUpdate(Message, 0, Message.Length);
        var ok = verifier.VerifySignature(signature);
        Emit("S22", "ML-DSA-65", $"verify={Flag(ok)} sig={signature.Length}");
    }

    // S23: self-signed X.509 certificate, signature checked at the ASN.1 level
    private static void S23X509SelfSigned()
    {
        using var key = ECDsa.Create(ECCurve.NamedCurves.nistP256);
        var request = new CertificateRequest($"CN={TlsServerName}", key, HashAlgorithmName.SHA256);
        var now = DateTimeOffset.UtcNow;
        using var certificate = request.Create(
            request.SubjectName,
            X509SignatureGenerator.CreateForECDsa(key),
            now.AddMinutes(-1),
            now.AddDays(365),
            RandomNumberGenerator.GetBytes(8));

        var reader = new AsnReader(certificate.RawData, AsnEncodingRules.DER).ReadSequence();
        var tbs = reader.ReadEncodedValue().ToArray();
        reader.ReadSequence();
        var signature = reader.ReadBitString(out _);
        using var publicKey = certificate.GetECDsaPublicKey()!;
        var ok = publicKey.VerifyData(tbs, signature, HashAlgorithmName.SHA256, DSASignatureFormat.Rfc3279DerSequence);
        Emit("S23", "X.509 self-signed", $"verify={Flag(ok)}");
    }

    // S24: TLS 1.3-only client configuration (no connection is made)
    private static void S24Tls13Client()
    {
        var options = new SslClientAuthenticationOptions
        {
            TargetHost = TlsServerName,
            EnabledSslProtocols = SslProtocols.Tls13,
        };
        if (!OperatingSystem.IsWindows())
        {
            options.CipherSuitesPolicy = new CipherSuitesPolicy(
            [
                TlsCipherSuite.TLS_AES_128_GCM_SHA256,
                TlsCipherSuite.TLS_AES_256_GCM_SHA384,
                TlsCipherSuite.TLS_CHACHA20_POLY1305_SHA256,
            ]);
        }

        Emit("S24", "TLS 1.3 client", "configured=true");
    }

    public static void Main()
    {
        S01Sha256();
        S02Sha2Sha3Blake2();
        S03LegacyHashes();
        S04Shake128();
        S05HmacSha256();
        S06HkdfSha256();
        S07Pbkdf2();
        S08Scrypt();
        S09Argon2id();
        S10Bcrypt();
        S11Aes256Gcm();
        S12ChaCha20Poly1305();
        S13Aes256Cbc();
        S14Aes128Ecb();
        S15Aes256Ctr();
        S16TdeaCbc();
        S17Rsa3072();
        S18EcdsaP256();
        S19Ed25519();
        S20KeyAgreement();
        S21MlKem768();
        S22MlDsa65();
        S23X509SelfSigned();
        S24Tls13Client();
    }
}
