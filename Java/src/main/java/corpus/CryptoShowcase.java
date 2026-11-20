package corpus;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;
import java.security.spec.MGF1ParameterSpec;
import java.security.spec.PSSParameterSpec;
import java.security.spec.RSAKeyGenParameterSpec;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.Date;
import java.util.HexFormat;
import javax.crypto.Cipher;
import javax.crypto.KDF;
import javax.crypto.KEM;
import javax.crypto.KeyAgreement;
import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.HKDFParameterSpec;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PSource;
import javax.crypto.spec.SecretKeySpec;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder;
import org.bouncycastle.crypto.digests.Blake2bDigest;
import org.bouncycastle.crypto.digests.SHAKEDigest;
import org.bouncycastle.crypto.generators.Argon2BytesGenerator;
import org.bouncycastle.crypto.generators.OpenBSDBCrypt;
import org.bouncycastle.crypto.generators.SCrypt;
import org.bouncycastle.crypto.params.Argon2Parameters;
import org.bouncycastle.crypto.params.Ed25519PrivateKeyParameters;
import org.bouncycastle.crypto.signers.Ed25519Signer;
import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;

/**
 * CBOM ground-truth corpus - Java implementation.
 *
 * <p>Runs scenarios S01-S24 in the same order, with the same inputs and the same
 * output lines as the Python, Go, TypeScript and C# implementations. All hard-coded
 * keys, IVs, salts and passwords are published test vectors - never reuse them.
 */
public final class CryptoShowcase {

    private static final byte[] MESSAGE = ascii("The quick brown fox jumps over the lazy dog");

    // --- Hard-coded material (public test vectors only) ---
    // Wikipedia HMAC example key
    private static final byte[] HMAC_KEY = ascii("key");
    // RFC 5869 A.1
    private static final byte[] HKDF_IKM = fromHex("0b".repeat(22));
    private static final byte[] HKDF_SALT = fromHex("000102030405060708090a0b0c");
    private static final byte[] HKDF_INFO = fromHex("f0f1f2f3f4f5f6f7f8f9");
    // RFC 7914 sections 11 and 12
    private static final String PBKDF2_PASSWORD = "Password";
    private static final byte[] PBKDF2_SALT = ascii("NaCl");
    private static final byte[] SCRYPT_PASSWORD = ascii("pleaseletmein");
    private static final byte[] SCRYPT_SALT = ascii("SodiumChloride");
    private static final String PASSWORD = "correct horse battery staple";
    private static final byte[] ARGON2_SALT = ascii("cbom-corpus-salt");
    // GCM specification test case 16
    private static final byte[] GCM_KEY = fromHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308");
    private static final byte[] GCM_IV = fromHex("cafebabefacedbaddecaf888");
    private static final byte[] GCM_AAD = fromHex("feedfacedeadbeeffeedfacedeadbeefabaddad2");
    private static final byte[] GCM_PLAINTEXT = fromHex(
            "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
                    + "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39");
    // FIPS 197 appendix C.1
    private static final byte[] ECB_KEY = fromHex("000102030405060708090a0b0c0d0e0f");
    private static final byte[] ECB_PLAINTEXT = fromHex("00112233445566778899aabbccddeeff");
    // RFC 8032 section 7.1, TEST 1
    private static final byte[] ED25519_SEED = fromHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60");
    private static final byte[] SESSION_INFO = ascii("cbom-corpus session key v1");
    private static final String TLS_SERVER_NAME = "cbom-corpus.example";

    private static final SecureRandom RNG = new SecureRandom();

    private CryptoShowcase() {
    }

    private static byte[] ascii(String text) {
        return text.getBytes(StandardCharsets.US_ASCII);
    }

    private static byte[] fromHex(String hex) {
        return HexFormat.of().parseHex(hex);
    }

    private static String toHex(byte[] bytes) {
        return HexFormat.of().formatHex(bytes);
    }

    private static byte[] concat(byte[] first, byte[] second) {
        byte[] out = Arrays.copyOf(first, first.length + second.length);
        System.arraycopy(second, 0, out, first.length, second.length);
        return out;
    }

    private static void emit(String scenario, String label, String value) {
        System.out.print(String.format("[%s] %-18s %s", scenario, label, value) + "\n");
    }

    // S01: SHA-256 (FIPS 180-4)
    static void s01Sha256() throws Exception {
        var md = MessageDigest.getInstance("SHA-256");
        emit("S01", "SHA-256", toHex(md.digest(MESSAGE)));
    }

    // S02: SHA-512, SHA3-256, BLAKE2b-512
    static void s02Sha2Sha3Blake2() throws Exception {
        var sha512 = MessageDigest.getInstance("SHA-512");
        emit("S02", "SHA-512", toHex(sha512.digest(MESSAGE)));
        var sha3 = MessageDigest.getInstance("SHA3-256");
        emit("S02", "SHA3-256", toHex(sha3.digest(MESSAGE)));
        var blake = new Blake2bDigest(512);
        blake.update(MESSAGE, 0, MESSAGE.length);
        var out = new byte[blake.getDigestSize()];
        blake.doFinal(out, 0);
        emit("S02", "BLAKE2b-512", toHex(out));
    }

    // S03: legacy digests - deliberately weak
    static void s03LegacyHashes() throws Exception {
        var md5 = MessageDigest.getInstance("MD5");
        emit("S03", "MD5", toHex(md5.digest(MESSAGE)));
        var sha1 = MessageDigest.getInstance("SHA-1");
        emit("S03", "SHA-1", toHex(sha1.digest(MESSAGE)));
    }

    // S04: SHAKE128 extendable-output function
    static void s04Shake128() {
        var shake = new SHAKEDigest(128);
        shake.update(MESSAGE, 0, MESSAGE.length);
        var out = new byte[32];
        shake.doFinal(out, 0, out.length);
        emit("S04", "SHAKE128", toHex(out));
    }

    // S05: HMAC-SHA256
    static void s05HmacSha256() throws Exception {
        var mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(HMAC_KEY, "HmacSHA256"));
        emit("S05", "HMAC-SHA256", toHex(mac.doFinal(MESSAGE)));
    }

    // S06: HKDF-SHA256 (RFC 5869) through the JDK 25 KDF API
    static void s06HkdfSha256() throws Exception {
        var hkdf = KDF.getInstance("HKDF-SHA256");
        var params = HKDFParameterSpec.ofExtract()
                .addIKM(HKDF_IKM)
                .addSalt(HKDF_SALT)
                .thenExpand(HKDF_INFO, 42);
        emit("S06", "HKDF-SHA256", toHex(hkdf.deriveData(params)));
    }

    // S07: PBKDF2-HMAC-SHA256
    static void s07Pbkdf2() throws Exception {
        var factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        var spec = new PBEKeySpec(PBKDF2_PASSWORD.toCharArray(), PBKDF2_SALT, 80_000, 512);
        var derived = factory.generateSecret(spec).getEncoded();
        emit("S07", "PBKDF2-SHA256", toHex(derived));
    }

    // S08: scrypt
    static void s08Scrypt() {
        var derived = SCrypt.generate(SCRYPT_PASSWORD, SCRYPT_SALT, 1 << 14, 8, 1, 64);
        emit("S08", "scrypt", toHex(derived));
    }

    // S09: Argon2id
    static void s09Argon2id() {
        var params = new Argon2Parameters.Builder(Argon2Parameters.ARGON2_id)
                .withVersion(Argon2Parameters.ARGON2_VERSION_13)
                .withIterations(2)
                .withMemoryAsKB(19_456)
                .withParallelism(1)
                .withSalt(ARGON2_SALT)
                .build();
        var generator = new Argon2BytesGenerator();
        generator.init(params);
        var out = new byte[32];
        generator.generateBytes(ascii(PASSWORD), out);
        emit("S09", "Argon2id", toHex(out));
    }

    // S10: bcrypt
    static void s10Bcrypt() {
        var salt = new byte[16];
        RNG.nextBytes(salt);
        var hash = OpenBSDBCrypt.generate("2b", PASSWORD.toCharArray(), salt, 12);
        var ok = OpenBSDBCrypt.checkPassword(hash, PASSWORD.toCharArray());
        emit("S10", "bcrypt", "verify=" + ok);
    }

    // S11: AES-256-GCM known-answer test
    static void s11Aes256Gcm() throws Exception {
        var key = new SecretKeySpec(GCM_KEY, "AES");
        var gcm = new GCMParameterSpec(128, GCM_IV);
        var encryptor = Cipher.getInstance("AES/GCM/NoPadding");
        encryptor.init(Cipher.ENCRYPT_MODE, key, gcm);
        encryptor.updateAAD(GCM_AAD);
        var sealed = encryptor.doFinal(GCM_PLAINTEXT);
        var decryptor = Cipher.getInstance("AES/GCM/NoPadding");
        decryptor.init(Cipher.DECRYPT_MODE, key, gcm);
        decryptor.updateAAD(GCM_AAD);
        var opened = decryptor.doFinal(sealed);
        var ciphertext = Arrays.copyOfRange(sealed, 0, sealed.length - 16);
        var tag = Arrays.copyOfRange(sealed, sealed.length - 16, sealed.length);
        emit("S11", "AES-256-GCM", "ct=" + toHex(ciphertext) + " tag=" + toHex(tag)
                + " roundtrip=" + Arrays.equals(opened, GCM_PLAINTEXT));
    }

    // S12: ChaCha20-Poly1305 (RFC 8439)
    static void s12ChaCha20Poly1305() throws Exception {
        var keyGenerator = KeyGenerator.getInstance("ChaCha20");
        var key = keyGenerator.generateKey();
        var nonce = new byte[12];
        RNG.nextBytes(nonce);
        var encryptor = Cipher.getInstance("ChaCha20-Poly1305");
        encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(nonce));
        var sealed = encryptor.doFinal(MESSAGE);
        var decryptor = Cipher.getInstance("ChaCha20-Poly1305");
        decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(nonce));
        var opened = decryptor.doFinal(sealed);
        emit("S12", "ChaCha20-Poly1305", "roundtrip=" + Arrays.equals(opened, MESSAGE));
    }

    // S13: AES-256-CBC with PKCS#7 padding
    static void s13Aes256Cbc() throws Exception {
        var keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        var key = keyGenerator.generateKey();
        var iv = new byte[16];
        RNG.nextBytes(iv);
        var encryptor = Cipher.getInstance("AES/CBC/PKCS5Padding");
        encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        var ciphertext = encryptor.doFinal(MESSAGE);
        var decryptor = Cipher.getInstance("AES/CBC/PKCS5Padding");
        decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
        var plaintext = decryptor.doFinal(ciphertext);
        emit("S13", "AES-256-CBC", "roundtrip=" + Arrays.equals(plaintext, MESSAGE));
    }

    // S14: AES-128-ECB known-answer test - deliberately weak mode
    static void s14Aes128Ecb() throws Exception {
        var encryptor = Cipher.getInstance("AES/ECB/PKCS5Padding");
        encryptor.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(ECB_KEY, "AES"));
        emit("S14", "AES-128-ECB", toHex(encryptor.doFinal(ECB_PLAINTEXT)));
    }

    // S15: AES-256-CTR
    static void s15Aes256Ctr() throws Exception {
        var keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        var key = keyGenerator.generateKey();
        var counterBlock = new byte[16];
        RNG.nextBytes(counterBlock);
        var encryptor = Cipher.getInstance("AES/CTR/NoPadding");
        encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(counterBlock));
        var ciphertext = encryptor.doFinal(MESSAGE);
        var decryptor = Cipher.getInstance("AES/CTR/NoPadding");
        decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(counterBlock));
        var plaintext = decryptor.doFinal(ciphertext);
        emit("S15", "AES-256-CTR", "roundtrip=" + Arrays.equals(plaintext, MESSAGE));
    }

    // S16: 3DES (TDEA) CBC - deliberately legacy
    static void s16TdeaCbc() throws Exception {
        var keyGenerator = KeyGenerator.getInstance("DESede");
        var key = keyGenerator.generateKey();
        var iv = new byte[8];
        RNG.nextBytes(iv);
        var encryptor = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        encryptor.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        var ciphertext = encryptor.doFinal(MESSAGE);
        var decryptor = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        decryptor.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
        var plaintext = decryptor.doFinal(ciphertext);
        emit("S16", "3DES-CBC", "roundtrip=" + Arrays.equals(plaintext, MESSAGE));
    }

    // S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair
    static void s17Rsa3072() throws Exception {
        var generator = KeyPairGenerator.getInstance("RSA");
        generator.initialize(new RSAKeyGenParameterSpec(3072, RSAKeyGenParameterSpec.F4));
        var keyPair = generator.generateKeyPair();

        var oaep = new OAEPParameterSpec(
                "SHA-256", "MGF1", MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT);
        var encryptor = Cipher.getInstance("RSA/ECB/OAEPPadding");
        encryptor.init(Cipher.ENCRYPT_MODE, keyPair.getPublic(), oaep);
        var ciphertext = encryptor.doFinal(MESSAGE);
        var decryptor = Cipher.getInstance("RSA/ECB/OAEPPadding");
        decryptor.init(Cipher.DECRYPT_MODE, keyPair.getPrivate(), oaep);
        var plaintext = decryptor.doFinal(ciphertext);
        emit("S17", "RSA-3072 OAEP", "roundtrip=" + Arrays.equals(plaintext, MESSAGE));

        var pss = new PSSParameterSpec(
                "SHA-256", "MGF1", MGF1ParameterSpec.SHA256,
                32, PSSParameterSpec.TRAILER_FIELD_BC);
        var pssSigner = Signature.getInstance("RSASSA-PSS");
        pssSigner.setParameter(pss);
        pssSigner.initSign(keyPair.getPrivate());
        pssSigner.update(MESSAGE);
        var pssSignature = pssSigner.sign();
        var pssVerifier = Signature.getInstance("RSASSA-PSS");
        pssVerifier.setParameter(pss);
        pssVerifier.initVerify(keyPair.getPublic());
        pssVerifier.update(MESSAGE);
        emit("S17", "RSA-3072 PSS", "verify=" + pssVerifier.verify(pssSignature));

        var pkcs1Signer = Signature.getInstance("SHA256withRSA");
        pkcs1Signer.initSign(keyPair.getPrivate());
        pkcs1Signer.update(MESSAGE);
        var pkcs1Signature = pkcs1Signer.sign();
        var pkcs1Verifier = Signature.getInstance("SHA256withRSA");
        pkcs1Verifier.initVerify(keyPair.getPublic());
        pkcs1Verifier.update(MESSAGE);
        emit("S17", "RSA-3072 PKCS1v15", "verify=" + pkcs1Verifier.verify(pkcs1Signature));
    }

    // S18: ECDSA P-256 with SHA-256
    static void s18EcdsaP256() throws Exception {
        var generator = KeyPairGenerator.getInstance("EC");
        generator.initialize(new ECGenParameterSpec("secp256r1"));
        var keyPair = generator.generateKeyPair();
        var signer = Signature.getInstance("SHA256withECDSA");
        signer.initSign(keyPair.getPrivate());
        signer.update(MESSAGE);
        var signature = signer.sign();
        var verifier = Signature.getInstance("SHA256withECDSA");
        verifier.initVerify(keyPair.getPublic());
        verifier.update(MESSAGE);
        emit("S18", "ECDSA P-256", "verify=" + verifier.verify(signature));
    }

    // S19: Ed25519 from a fixed seed (RFC 8032)
    static void s19Ed25519() {
        var privateKey = new Ed25519PrivateKeyParameters(ED25519_SEED, 0);
        var publicKey = privateKey.generatePublicKey();
        var signer = new Ed25519Signer();
        signer.init(true, privateKey);
        signer.update(MESSAGE, 0, MESSAGE.length);
        var signature = signer.generateSignature();
        var verifier = new Ed25519Signer();
        verifier.init(false, publicKey);
        verifier.update(MESSAGE, 0, MESSAGE.length);
        var ok = verifier.verifySignature(signature);
        emit("S19", "Ed25519", "pk=" + toHex(publicKey.getEncoded()) + " sig=" + toHex(signature) + " verify=" + ok);
    }

    static byte[] agree(String algorithm, PrivateKey privateKey, PublicKey peerKey) throws Exception {
        var agreement = KeyAgreement.getInstance(algorithm);
        agreement.init(privateKey);
        agreement.doPhase(peerKey, true);
        return agreement.generateSecret();
    }

    static byte[] deriveSessionKey(byte[] sharedSecret) throws Exception {
        var hkdf = KDF.getInstance("HKDF-SHA256");
        var params = HKDFParameterSpec.ofExtract().addIKM(sharedSecret).thenExpand(SESSION_INFO, 32);
        return hkdf.deriveData(params);
    }

    // S20: X25519 + ECDH P-256 key agreement, HKDF session key
    static void s20KeyAgreement() throws Exception {
        var x25519 = KeyPairGenerator.getInstance("X25519");
        var alice = x25519.generateKeyPair();
        var bob = x25519.generateKeyPair();
        var xAlice = agree("X25519", alice.getPrivate(), bob.getPublic());
        var xBob = agree("X25519", bob.getPrivate(), alice.getPublic());
        emit("S20", "X25519", "agree=" + Arrays.equals(xAlice, xBob));

        var ec = KeyPairGenerator.getInstance("EC");
        ec.initialize(new ECGenParameterSpec("secp256r1"));
        var aliceEc = ec.generateKeyPair();
        var bobEc = ec.generateKeyPair();
        var zAlice = agree("ECDH", aliceEc.getPrivate(), bobEc.getPublic());
        var zBob = agree("ECDH", bobEc.getPrivate(), aliceEc.getPublic());
        emit("S20", "ECDH P-256", "agree=" + Arrays.equals(zAlice, zBob));

        var kAlice = deriveSessionKey(concat(xAlice, zAlice));
        var kBob = deriveSessionKey(concat(xBob, zBob));
        emit("S20", "HKDF session key", "match=" + Arrays.equals(kAlice, kBob));
    }

    // S21: ML-KEM-768 (FIPS 203) through the JDK KEM API
    static void s21MlKem768() throws Exception {
        var generator = KeyPairGenerator.getInstance("ML-KEM-768");
        var keyPair = generator.generateKeyPair();
        var kem = KEM.getInstance("ML-KEM");
        var encapsulated = kem.newEncapsulator(keyPair.getPublic()).encapsulate();
        var sharedSecret = encapsulated.key().getEncoded();
        var ciphertext = encapsulated.encapsulation();
        var recovered = kem.newDecapsulator(keyPair.getPrivate()).decapsulate(ciphertext).getEncoded();
        emit("S21", "ML-KEM-768", "agree=" + Arrays.equals(sharedSecret, recovered)
                + " ct=" + ciphertext.length + " ss=" + sharedSecret.length);
    }

    // S22: ML-DSA-65 (FIPS 204)
    static void s22MlDsa65() throws Exception {
        var generator = KeyPairGenerator.getInstance("ML-DSA-65");
        var keyPair = generator.generateKeyPair();
        var signer = Signature.getInstance("ML-DSA-65");
        signer.initSign(keyPair.getPrivate());
        signer.update(MESSAGE);
        var signature = signer.sign();
        var verifier = Signature.getInstance("ML-DSA-65");
        verifier.initVerify(keyPair.getPublic());
        verifier.update(MESSAGE);
        var ok = verifier.verify(signature);
        emit("S22", "ML-DSA-65", "verify=" + ok + " sig=" + signature.length);
    }

    // S23: self-signed X.509 certificate (Bouncy Castle builder, JDK signer and verifier)
    static void s23X509SelfSigned() throws Exception {
        var generator = KeyPairGenerator.getInstance("EC");
        generator.initialize(new ECGenParameterSpec("secp256r1"));
        var keyPair = generator.generateKeyPair();
        var name = new X500Name("CN=" + TLS_SERVER_NAME);
        var now = Instant.now();
        var builder = new JcaX509v3CertificateBuilder(
                name,
                new BigInteger(64, RNG),
                Date.from(now.minus(Duration.ofMinutes(1))),
                Date.from(now.plus(Duration.ofDays(365))),
                name,
                keyPair.getPublic());
        var contentSigner = new JcaContentSignerBuilder("SHA256withECDSA").build(keyPair.getPrivate());
        var certificate = new JcaX509CertificateConverter().getCertificate(builder.build(contentSigner));
        boolean ok;
        try {
            certificate.verify(certificate.getPublicKey());
            ok = true;
        } catch (java.security.GeneralSecurityException e) {
            ok = false;
        }
        emit("S23", "X.509 self-signed", "verify=" + ok);
    }

    // S24: TLS 1.3-only client configuration (no connection is made)
    static void s24Tls13Client() throws Exception {
        var context = SSLContext.getInstance("TLSv1.3");
        context.init(null, null, null);
        var parameters = new SSLParameters();
        parameters.setProtocols(new String[] {"TLSv1.3"});
        parameters.setCipherSuites(new String[] {
            "TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"});
        var engine = context.createSSLEngine(TLS_SERVER_NAME, 443);
        engine.setUseClientMode(true);
        engine.setSSLParameters(parameters);
        emit("S24", "TLS 1.3 client", "configured=true");
    }

    public static void main(String[] args) throws Exception {
        s01Sha256();
        s02Sha2Sha3Blake2();
        s03LegacyHashes();
        s04Shake128();
        s05HmacSha256();
        s06HkdfSha256();
        s07Pbkdf2();
        s08Scrypt();
        s09Argon2id();
        s10Bcrypt();
        s11Aes256Gcm();
        s12ChaCha20Poly1305();
        s13Aes256Cbc();
        s14Aes128Ecb();
        s15Aes256Ctr();
        s16TdeaCbc();
        s17Rsa3072();
        s18EcdsaP256();
        s19Ed25519();
        s20KeyAgreement();
        s21MlKem768();
        s22MlDsa65();
        s23X509SelfSigned();
        s24Tls13Client();
    }
}
