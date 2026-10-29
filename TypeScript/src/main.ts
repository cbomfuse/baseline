/**
 * CBOM ground-truth corpus - TypeScript (Node.js) implementation.
 *
 * Runs scenarios S01-S24 in the same order, with the same inputs and the same
 * output lines as the Python, Java, Go and C# implementations. All hard-coded
 * keys, IVs, salts and passwords are published test vectors - never reuse them.
 */
// reflect-metadata is a runtime polyfill required by @peculiar/x509 (tsyringe).
import "reflect-metadata";
import * as crypto from "node:crypto";
import * as tls from "node:tls";
import { chacha20poly1305 } from "@noble/ciphers/chacha.js";
import { randomBytes } from "@noble/ciphers/utils.js";
import { ed25519 } from "@noble/curves/ed25519.js";
import { argon2id } from "@noble/hashes/argon2.js";
import { blake2b } from "@noble/hashes/blake2.js";
import { sha3_256 } from "@noble/hashes/sha3.js";
import { ml_dsa65 } from "@noble/post-quantum/ml-dsa.js";
import { ml_kem768 } from "@noble/post-quantum/ml-kem.js";
import * as x509 from "@peculiar/x509";
import bcrypt from "bcryptjs";

type Bytes = Uint8Array<ArrayBuffer>;

// The W3C Web Cryptography API as implemented by Node.js (distinct from node:crypto).
const subtle = globalThis.crypto.subtle;

const MESSAGE = utf8("The quick brown fox jumps over the lazy dog");

// --- Hard-coded material (public test vectors only) ---
// Wikipedia HMAC example key
const HMAC_KEY = utf8("key");
// RFC 5869 A.1
const HKDF_IKM = new Uint8Array(22).fill(0x0b);
const HKDF_SALT = fromHex("000102030405060708090a0b0c");
const HKDF_INFO = fromHex("f0f1f2f3f4f5f6f7f8f9");
// RFC 7914 sections 11 and 12
const PBKDF2_PASSWORD = utf8("Password");
const PBKDF2_SALT = utf8("NaCl");
const SCRYPT_PASSWORD = utf8("pleaseletmein");
const SCRYPT_SALT = utf8("SodiumChloride");
const PASSWORD = "correct horse battery staple";
const ARGON2_SALT = utf8("cbom-corpus-salt");
// GCM specification test case 16
const GCM_KEY = fromHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308");
const GCM_IV = fromHex("cafebabefacedbaddecaf888");
const GCM_AAD = fromHex("feedfacedeadbeeffeedfacedeadbeefabaddad2");
const GCM_PLAINTEXT = fromHex(
  "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72" +
    "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39",
);
// FIPS 197 appendix C.1
const ECB_KEY = fromHex("000102030405060708090a0b0c0d0e0f");
const ECB_PLAINTEXT = fromHex("00112233445566778899aabbccddeeff");
// RFC 8032 section 7.1, TEST 1
const ED25519_SEED = fromHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60");
const SESSION_INFO = utf8("cbom-corpus session key v1");
const TLS_SERVER_NAME = "cbom-corpus.example";

function utf8(text: string): Bytes {
  return new TextEncoder().encode(text);
}

function fromHex(hex: string): Bytes {
  return new Uint8Array(Buffer.from(hex, "hex"));
}

function toHex(bytes: Uint8Array | ArrayBuffer): string {
  return Buffer.from(bytes instanceof ArrayBuffer ? new Uint8Array(bytes) : bytes).toString("hex");
}

function equal(a: Uint8Array | ArrayBuffer, b: Uint8Array): boolean {
  return Buffer.compare(Buffer.from(a instanceof ArrayBuffer ? new Uint8Array(a) : a), Buffer.from(b)) === 0;
}

function emit(scenario: string, label: string, value: string): void {
  console.log(`[${scenario}] ${label.padEnd(18)} ${value}`);
}

// S01: SHA-256 (FIPS 180-4)
function s01Sha256(): void {
  emit("S01", "SHA-256", crypto.createHash("sha256").update(MESSAGE).digest("hex"));
}

// S02: SHA-512, SHA3-256, BLAKE2b-512
function s02Sha2Sha3Blake2(): void {
  emit("S02", "SHA-512", crypto.createHash("sha512").update(MESSAGE).digest("hex"));
  emit("S02", "SHA3-256", toHex(sha3_256(MESSAGE)));
  emit("S02", "BLAKE2b-512", toHex(blake2b(MESSAGE, { dkLen: 64 })));
}

// S03: legacy digests - deliberately weak
function s03LegacyHashes(): void {
  emit("S03", "MD5", crypto.createHash("md5").update(MESSAGE).digest("hex"));
  emit("S03", "SHA-1", crypto.createHash("sha1").update(MESSAGE).digest("hex"));
}

// S04: SHAKE128 extendable-output function
function s04Shake128(): void {
  const xof = crypto.createHash("shake128", { outputLength: 32 });
  emit("S04", "SHAKE128", xof.update(MESSAGE).digest("hex"));
}

// S05: HMAC-SHA256
function s05HmacSha256(): void {
  const mac = crypto.createHmac("sha256", HMAC_KEY);
  emit("S05", "HMAC-SHA256", mac.update(MESSAGE).digest("hex"));
}

// S06: HKDF-SHA256 (RFC 5869)
function s06HkdfSha256(): void {
  const okm = crypto.hkdfSync("sha256", HKDF_IKM, HKDF_SALT, HKDF_INFO, 42);
  emit("S06", "HKDF-SHA256", toHex(okm));
}

// S07: PBKDF2-HMAC-SHA256 through WebCrypto
async function s07Pbkdf2(): Promise<void> {
  const baseKey = await subtle.importKey("raw", PBKDF2_PASSWORD, "PBKDF2", false, ["deriveBits"]);
  const bits = await subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt: PBKDF2_SALT, iterations: 80_000 },
    baseKey,
    512,
  );
  emit("S07", "PBKDF2-SHA256", toHex(bits));
}

// S08: scrypt
function s08Scrypt(): void {
  const derived = crypto.scryptSync(SCRYPT_PASSWORD, SCRYPT_SALT, 64, { N: 2 ** 14, r: 8, p: 1 });
  emit("S08", "scrypt", toHex(derived));
}

// S09: Argon2id
function s09Argon2id(): void {
  const raw = argon2id(utf8(PASSWORD), ARGON2_SALT, { t: 2, m: 19_456, p: 1, dkLen: 32 });
  emit("S09", "Argon2id", toHex(raw));
}

// S10: bcrypt
function s10Bcrypt(): void {
  const salt = bcrypt.genSaltSync(12);
  const hash = bcrypt.hashSync(PASSWORD, salt);
  const ok = bcrypt.compareSync(PASSWORD, hash);
  emit("S10", "bcrypt", `verify=${ok}`);
}

// S11: AES-256-GCM known-answer test
function s11Aes256Gcm(): void {
  const encryptor = crypto.createCipheriv("aes-256-gcm", GCM_KEY, GCM_IV, { authTagLength: 16 });
  encryptor.setAAD(GCM_AAD);
  const ciphertext = Buffer.concat([encryptor.update(GCM_PLAINTEXT), encryptor.final()]);
  const tag = encryptor.getAuthTag();
  const decryptor = crypto.createDecipheriv("aes-256-gcm", GCM_KEY, GCM_IV, { authTagLength: 16 });
  decryptor.setAAD(GCM_AAD);
  decryptor.setAuthTag(tag);
  const plaintext = Buffer.concat([decryptor.update(ciphertext), decryptor.final()]);
  emit("S11", "AES-256-GCM", `ct=${toHex(ciphertext)} tag=${toHex(tag)} roundtrip=${equal(plaintext, GCM_PLAINTEXT)}`);
}

// S12: ChaCha20-Poly1305 (RFC 8439)
function s12ChaCha20Poly1305(): void {
  const key = randomBytes(32);
  const nonce = randomBytes(12);
  const sealed = chacha20poly1305(key, nonce).encrypt(MESSAGE);
  const opened = chacha20poly1305(key, nonce).decrypt(sealed);
  emit("S12", "ChaCha20-Poly1305", `roundtrip=${equal(opened, MESSAGE)}`);
}

// S13: AES-256-CBC with PKCS#7 padding
function s13Aes256Cbc(): void {
  const key = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);
  const encryptor = crypto.createCipheriv("aes-256-cbc", key, iv);
  const ciphertext = Buffer.concat([encryptor.update(MESSAGE), encryptor.final()]);
  const decryptor = crypto.createDecipheriv("aes-256-cbc", key, iv);
  const plaintext = Buffer.concat([decryptor.update(ciphertext), decryptor.final()]);
  emit("S13", "AES-256-CBC", `roundtrip=${equal(plaintext, MESSAGE)}`);
}

// S14: AES-128-ECB known-answer test - deliberately weak mode
function s14Aes128Ecb(): void {
  const encryptor = crypto.createCipheriv("aes-128-ecb", ECB_KEY, null);
  const ciphertext = Buffer.concat([encryptor.update(ECB_PLAINTEXT), encryptor.final()]);
  emit("S14", "AES-128-ECB", toHex(ciphertext));
}

// S15: AES-256-CTR through WebCrypto
async function s15Aes256Ctr(): Promise<void> {
  const key = await subtle.generateKey({ name: "AES-CTR", length: 256 }, false, ["encrypt", "decrypt"]);
  const counter = globalThis.crypto.getRandomValues(new Uint8Array(16));
  const params = { name: "AES-CTR", counter, length: 128 };
  const ciphertext = await subtle.encrypt(params, key, MESSAGE);
  const plaintext = await subtle.decrypt(params, key, ciphertext);
  emit("S15", "AES-256-CTR", `roundtrip=${equal(plaintext, MESSAGE)}`);
}

// S16: 3DES (TDEA) CBC - deliberately legacy
function s16TdeaCbc(): void {
  const key = crypto.randomBytes(24);
  const iv = crypto.randomBytes(8);
  const encryptor = crypto.createCipheriv("des-ede3-cbc", key, iv);
  const ciphertext = Buffer.concat([encryptor.update(MESSAGE), encryptor.final()]);
  const decryptor = crypto.createDecipheriv("des-ede3-cbc", key, iv);
  const plaintext = Buffer.concat([decryptor.update(ciphertext), decryptor.final()]);
  emit("S16", "3DES-CBC", `roundtrip=${equal(plaintext, MESSAGE)}`);
}

// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair
function s17Rsa3072(): void {
  const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", { modulusLength: 3072, publicExponent: 0x10001 });

  const ciphertext = crypto.publicEncrypt(
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" },
    MESSAGE,
  );
  const plaintext = crypto.privateDecrypt(
    { key: privateKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" },
    ciphertext,
  );
  emit("S17", "RSA-3072 OAEP", `roundtrip=${equal(plaintext, MESSAGE)}`);

  const pssSignature = crypto.sign("sha256", MESSAGE, {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: 32,
  });
  const pssOk = crypto.verify(
    "sha256",
    MESSAGE,
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_PSS_PADDING, saltLength: 32 },
    pssSignature,
  );
  emit("S17", "RSA-3072 PSS", `verify=${pssOk}`);

  const pkcs1Signature = crypto.sign("sha256", MESSAGE, {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PADDING,
  });
  const pkcs1Ok = crypto.verify(
    "sha256",
    MESSAGE,
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_PADDING },
    pkcs1Signature,
  );
  emit("S17", "RSA-3072 PKCS1v15", `verify=${pkcs1Ok}`);
}

// S18: ECDSA P-256 with SHA-256 through WebCrypto
async function s18EcdsaP256(): Promise<void> {
  const keys = await subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, false, ["sign", "verify"]);
  const algorithm = { name: "ECDSA", hash: "SHA-256" };
  const signature = await subtle.sign(algorithm, keys.privateKey, MESSAGE);
  const ok = await subtle.verify(algorithm, keys.publicKey, signature, MESSAGE);
  emit("S18", "ECDSA P-256", `verify=${ok}`);
}

// S19: Ed25519 from a fixed seed (RFC 8032)
function s19Ed25519(): void {
  const publicKey = ed25519.getPublicKey(ED25519_SEED);
  const signature = ed25519.sign(MESSAGE, ED25519_SEED);
  const ok = ed25519.verify(signature, MESSAGE, publicKey);
  emit("S19", "Ed25519", `pk=${toHex(publicKey)} sig=${toHex(signature)} verify=${ok}`);
}

function deriveSessionKey(sharedSecret: Uint8Array): Uint8Array {
  const key = crypto.hkdfSync("sha256", sharedSecret, new Uint8Array(0), SESSION_INFO, 32);
  return new Uint8Array(key);
}

// S20: X25519 + ECDH P-256 key agreement, HKDF session key
function s20KeyAgreement(): void {
  const alice = crypto.generateKeyPairSync("x25519");
  const bob = crypto.generateKeyPairSync("x25519");
  const xAlice = crypto.diffieHellman({ privateKey: alice.privateKey, publicKey: bob.publicKey });
  const xBob = crypto.diffieHellman({ privateKey: bob.privateKey, publicKey: alice.publicKey });
  emit("S20", "X25519", `agree=${equal(xAlice, xBob)}`);

  const aliceEc = crypto.createECDH("prime256v1");
  const bobEc = crypto.createECDH("prime256v1");
  const alicePublic = aliceEc.generateKeys();
  const bobPublic = bobEc.generateKeys();
  const zAlice = aliceEc.computeSecret(bobPublic);
  const zBob = bobEc.computeSecret(alicePublic);
  emit("S20", "ECDH P-256", `agree=${equal(zAlice, zBob)}`);

  const kAlice = deriveSessionKey(Buffer.concat([xAlice, zAlice]));
  const kBob = deriveSessionKey(Buffer.concat([xBob, zBob]));
  emit("S20", "HKDF session key", `match=${equal(kAlice, kBob)}`);
}

// S21: ML-KEM-768 (FIPS 203)
function s21MlKem768(): void {
  const { publicKey, secretKey } = ml_kem768.keygen();
  const { cipherText, sharedSecret } = ml_kem768.encapsulate(publicKey);
  const recovered = ml_kem768.decapsulate(cipherText, secretKey);
  emit("S21", "ML-KEM-768", `agree=${equal(sharedSecret, recovered)} ct=${cipherText.length} ss=${sharedSecret.length}`);
}

// S22: ML-DSA-65 (FIPS 204)
function s22MlDsa65(): void {
  const { publicKey, secretKey } = ml_dsa65.keygen();
  const signature = ml_dsa65.sign(MESSAGE, secretKey);
  const ok = ml_dsa65.verify(signature, MESSAGE, publicKey);
  emit("S22", "ML-DSA-65", `verify=${ok} sig=${signature.length}`);
}

// S23: self-signed X.509 certificate (@peculiar/x509 on WebCrypto)
async function s23X509SelfSigned(): Promise<void> {
  x509.cryptoProvider.set(globalThis.crypto);
  const algorithm = { name: "ECDSA", namedCurve: "P-256", hash: "SHA-256" };
  const keys = await subtle.generateKey(algorithm, false, ["sign", "verify"]);
  const now = Date.now();
  const certificate = await x509.X509CertificateGenerator.createSelfSigned({
    serialNumber: toHex(crypto.randomBytes(8)),
    name: `CN=${TLS_SERVER_NAME}`,
    notBefore: new Date(now - 60_000),
    notAfter: new Date(now + 365 * 86_400_000),
    signingAlgorithm: algorithm,
    keys,
  });
  const ok = await certificate.verify({ publicKey: keys.publicKey, signatureOnly: true });
  emit("S23", "X.509 self-signed", `verify=${ok}`);
}

// S24: TLS 1.3-only client configuration (no connection is made)
function s24Tls13Client(): void {
  const context = tls.createSecureContext({
    minVersion: "TLSv1.3",
    maxVersion: "TLSv1.3",
    ciphers: "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
  });
  emit("S24", "TLS 1.3 client", `configured=${context !== undefined}`);
}

async function main(): Promise<void> {
  s01Sha256();
  s02Sha2Sha3Blake2();
  s03LegacyHashes();
  s04Shake128();
  s05HmacSha256();
  s06HkdfSha256();
  await s07Pbkdf2();
  s08Scrypt();
  s09Argon2id();
  s10Bcrypt();
  s11Aes256Gcm();
  s12ChaCha20Poly1305();
  s13Aes256Cbc();
  s14Aes128Ecb();
  await s15Aes256Ctr();
  s16TdeaCbc();
  s17Rsa3072();
  await s18EcdsaP256();
  s19Ed25519();
  s20KeyAgreement();
  s21MlKem768();
  s22MlDsa65();
  await s23X509SelfSigned();
  s24Tls13Client();
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
