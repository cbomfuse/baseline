// Command cryptoshowcase is the Go implementation of the CBOM ground-truth corpus.
//
// It runs scenarios S01-S24 in the same order, with the same inputs and the same
// output lines as the Python, Java, TypeScript and C# implementations. All
// hard-coded keys, IVs, salts and passwords are published test vectors.
package main

import (
	"bytes"
	"crypto"
	"crypto/aes"
	"crypto/cipher"
	"crypto/des"
	"crypto/ecdh"
	"crypto/ecdsa"
	"crypto/ed25519"
	"crypto/elliptic"
	"crypto/hkdf"
	"crypto/hmac"
	"crypto/md5"
	"crypto/mlkem"
	"crypto/pbkdf2"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha3"
	"crypto/sha512"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/hex"
	"fmt"
	"math/big"
	"time"

	"github.com/cloudflare/circl/sign/mldsa/mldsa65"
	"golang.org/x/crypto/argon2"
	"golang.org/x/crypto/bcrypt"
	"golang.org/x/crypto/blake2b"
	"golang.org/x/crypto/chacha20poly1305"
	"golang.org/x/crypto/scrypt"
)

var message = []byte("The quick brown fox jumps over the lazy dog")

// Hard-coded material (public test vectors only): Wikipedia HMAC example key,
// RFC 5869 A.1, RFC 7914 sections 11 and 12, GCM specification test case 16,
// FIPS 197 appendix C.1 and RFC 8032 section 7.1 TEST 1.
var hmacKey = []byte("key")
var hkdfIKM = bytes.Repeat([]byte{0x0b}, 22)
var hkdfSalt = mustHex("000102030405060708090a0b0c")
var hkdfInfo = mustHex("f0f1f2f3f4f5f6f7f8f9")
var pbkdf2Password = "Password"
var pbkdf2Salt = []byte("NaCl")
var scryptPassword = []byte("pleaseletmein")
var scryptSalt = []byte("SodiumChloride")
var password = []byte("correct horse battery staple")
var argon2Salt = []byte("cbom-corpus-salt")
var gcmKey = mustHex("feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308")
var gcmIV = mustHex("cafebabefacedbaddecaf888")
var gcmAAD = mustHex("feedfacedeadbeeffeedfacedeadbeefabaddad2")
var gcmPlaintext = mustHex("d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72" +
	"1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39")
var ecbKey = mustHex("000102030405060708090a0b0c0d0e0f")
var ecbPlaintext = mustHex("00112233445566778899aabbccddeeff")
var ed25519Seed = mustHex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
var sessionInfo = "cbom-corpus session key v1"

const tlsServerName = "cbom-corpus.example"

func mustHex(s string) []byte {
	b, err := hex.DecodeString(s)
	if err != nil {
		panic(err)
	}
	return b
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func emit(scenario, label, value string) {
	fmt.Printf("[%s] %-18s %s\n", scenario, label, value)
}

func pkcs7Pad(data []byte, blockSize int) []byte {
	n := blockSize - len(data)%blockSize
	return append(bytes.Clone(data), bytes.Repeat([]byte{byte(n)}, n)...)
}

func pkcs7Unpad(data []byte) []byte {
	n := int(data[len(data)-1])
	if n == 0 || n > len(data) {
		panic("invalid padding")
	}
	return data[:len(data)-n]
}

// S01: SHA-256 (FIPS 180-4)
func s01SHA256() {
	digest := sha256.Sum256(message)
	emit("S01", "SHA-256", hex.EncodeToString(digest[:]))
}

// S02: SHA-512, SHA3-256, BLAKE2b-512
func s02SHA2SHA3BLAKE2() {
	sha512Digest := sha512.Sum512(message)
	emit("S02", "SHA-512", hex.EncodeToString(sha512Digest[:]))
	sha3Digest := sha3.Sum256(message)
	emit("S02", "SHA3-256", hex.EncodeToString(sha3Digest[:]))
	blakeDigest := blake2b.Sum512(message)
	emit("S02", "BLAKE2b-512", hex.EncodeToString(blakeDigest[:]))
}

// S03: legacy digests - deliberately weak
func s03LegacyHashes() {
	md5Digest := md5.Sum(message)
	emit("S03", "MD5", hex.EncodeToString(md5Digest[:]))
	sha1Digest := sha1.Sum(message)
	emit("S03", "SHA-1", hex.EncodeToString(sha1Digest[:]))
}

// S04: SHAKE128 extendable-output function
func s04SHAKE128() {
	out := sha3.SumSHAKE128(message, 32)
	emit("S04", "SHAKE128", hex.EncodeToString(out))
}

// S05: HMAC-SHA256
func s05HMACSHA256() {
	mac := hmac.New(sha256.New, hmacKey)
	mac.Write(message)
	emit("S05", "HMAC-SHA256", hex.EncodeToString(mac.Sum(nil)))
}

// S06: HKDF-SHA256 (RFC 5869)
func s06HKDFSHA256() {
	okm, err := hkdf.Key(sha256.New, hkdfIKM, hkdfSalt, string(hkdfInfo), 42)
	check(err)
	emit("S06", "HKDF-SHA256", hex.EncodeToString(okm))
}

// S07: PBKDF2-HMAC-SHA256
func s07PBKDF2() {
	derived, err := pbkdf2.Key(sha256.New, pbkdf2Password, pbkdf2Salt, 80_000, 64)
	check(err)
	emit("S07", "PBKDF2-SHA256", hex.EncodeToString(derived))
}

// S08: scrypt
func s08Scrypt() {
	derived, err := scrypt.Key(scryptPassword, scryptSalt, 1<<14, 8, 1, 64)
	check(err)
	emit("S08", "scrypt", hex.EncodeToString(derived))
}

// S09: Argon2id
func s09Argon2id() {
	raw := argon2.IDKey(password, argon2Salt, 2, 19_456, 1, 32)
	emit("S09", "Argon2id", hex.EncodeToString(raw))
}

// S10: bcrypt
func s10Bcrypt() {
	hash, err := bcrypt.GenerateFromPassword(password, 12)
	check(err)
	ok := bcrypt.CompareHashAndPassword(hash, password) == nil
	emit("S10", "bcrypt", fmt.Sprintf("verify=%t", ok))
}

// S11: AES-256-GCM known-answer test
func s11AES256GCM() {
	block, err := aes.NewCipher(gcmKey)
	check(err)
	aead, err := cipher.NewGCM(block)
	check(err)
	sealed := aead.Seal(nil, gcmIV, gcmPlaintext, gcmAAD)
	opened, err := aead.Open(nil, gcmIV, sealed, gcmAAD)
	check(err)
	tagStart := len(sealed) - aead.Overhead()
	emit("S11", "AES-256-GCM", fmt.Sprintf("ct=%x tag=%x roundtrip=%t", sealed[:tagStart], sealed[tagStart:], bytes.Equal(opened, gcmPlaintext)))
}

// S12: ChaCha20-Poly1305 (RFC 8439)
func s12ChaCha20Poly1305() {
	key := make([]byte, chacha20poly1305.KeySize)
	rand.Read(key)
	nonce := make([]byte, chacha20poly1305.NonceSize)
	rand.Read(nonce)
	aead, err := chacha20poly1305.New(key)
	check(err)
	sealed := aead.Seal(nil, nonce, message, nil)
	opened, err := aead.Open(nil, nonce, sealed, nil)
	check(err)
	emit("S12", "ChaCha20-Poly1305", fmt.Sprintf("roundtrip=%t", bytes.Equal(opened, message)))
}

// S13: AES-256-CBC with PKCS#7 padding
func s13AES256CBC() {
	key := make([]byte, 32)
	rand.Read(key)
	iv := make([]byte, aes.BlockSize)
	rand.Read(iv)
	block, err := aes.NewCipher(key)
	check(err)
	padded := pkcs7Pad(message, aes.BlockSize)
	ciphertext := make([]byte, len(padded))
	cipher.NewCBCEncrypter(block, iv).CryptBlocks(ciphertext, padded)
	plaintext := make([]byte, len(ciphertext))
	cipher.NewCBCDecrypter(block, iv).CryptBlocks(plaintext, ciphertext)
	emit("S13", "AES-256-CBC", fmt.Sprintf("roundtrip=%t", bytes.Equal(pkcs7Unpad(plaintext), message)))
}

// S14: AES-128-ECB known-answer test - deliberately weak mode
func s14AES128ECB() {
	block, err := aes.NewCipher(ecbKey)
	check(err)
	padded := pkcs7Pad(ecbPlaintext, aes.BlockSize)
	ciphertext := make([]byte, len(padded))
	for i := 0; i < len(padded); i += aes.BlockSize {
		block.Encrypt(ciphertext[i:i+aes.BlockSize], padded[i:i+aes.BlockSize])
	}
	emit("S14", "AES-128-ECB", hex.EncodeToString(ciphertext))
}

// S15: AES-256-CTR
func s15AES256CTR() {
	key := make([]byte, 32)
	rand.Read(key)
	counterBlock := make([]byte, aes.BlockSize)
	rand.Read(counterBlock)
	block, err := aes.NewCipher(key)
	check(err)
	ciphertext := make([]byte, len(message))
	cipher.NewCTR(block, counterBlock).XORKeyStream(ciphertext, message)
	plaintext := make([]byte, len(ciphertext))
	cipher.NewCTR(block, counterBlock).XORKeyStream(plaintext, ciphertext)
	emit("S15", "AES-256-CTR", fmt.Sprintf("roundtrip=%t", bytes.Equal(plaintext, message)))
}

// S16: 3DES (TDEA) CBC - deliberately legacy
func s16TDEACBC() {
	key := make([]byte, 24)
	rand.Read(key)
	iv := make([]byte, des.BlockSize)
	rand.Read(iv)
	block, err := des.NewTripleDESCipher(key)
	check(err)
	padded := pkcs7Pad(message, des.BlockSize)
	ciphertext := make([]byte, len(padded))
	cipher.NewCBCEncrypter(block, iv).CryptBlocks(ciphertext, padded)
	plaintext := make([]byte, len(ciphertext))
	cipher.NewCBCDecrypter(block, iv).CryptBlocks(plaintext, ciphertext)
	emit("S16", "3DES-CBC", fmt.Sprintf("roundtrip=%t", bytes.Equal(pkcs7Unpad(plaintext), message)))
}

// S17: RSA-3072 - OAEP, PSS and PKCS#1 v1.5 with one key pair
func s17RSA3072() {
	privateKey, err := rsa.GenerateKey(rand.Reader, 3072)
	check(err)
	publicKey := &privateKey.PublicKey

	ciphertext, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, publicKey, message, nil)
	check(err)
	plaintext, err := rsa.DecryptOAEP(sha256.New(), nil, privateKey, ciphertext, nil)
	check(err)
	emit("S17", "RSA-3072 OAEP", fmt.Sprintf("roundtrip=%t", bytes.Equal(plaintext, message)))

	digest := sha256.Sum256(message)
	pssOptions := &rsa.PSSOptions{SaltLength: rsa.PSSSaltLengthEqualsHash}
	pssSignature, err := rsa.SignPSS(rand.Reader, privateKey, crypto.SHA256, digest[:], pssOptions)
	check(err)
	pssOK := rsa.VerifyPSS(publicKey, crypto.SHA256, digest[:], pssSignature, pssOptions) == nil
	emit("S17", "RSA-3072 PSS", fmt.Sprintf("verify=%t", pssOK))

	pkcs1Signature, err := rsa.SignPKCS1v15(nil, privateKey, crypto.SHA256, digest[:])
	check(err)
	pkcs1OK := rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, digest[:], pkcs1Signature) == nil
	emit("S17", "RSA-3072 PKCS1v15", fmt.Sprintf("verify=%t", pkcs1OK))
}

// S18: ECDSA P-256 with SHA-256
func s18ECDSAP256() {
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	check(err)
	digest := sha256.Sum256(message)
	signature, err := ecdsa.SignASN1(rand.Reader, privateKey, digest[:])
	check(err)
	ok := ecdsa.VerifyASN1(&privateKey.PublicKey, digest[:], signature)
	emit("S18", "ECDSA P-256", fmt.Sprintf("verify=%t", ok))
}

// S19: Ed25519 from a fixed seed (RFC 8032)
func s19Ed25519() {
	privateKey := ed25519.NewKeyFromSeed(ed25519Seed)
	publicKey := privateKey.Public().(ed25519.PublicKey)
	signature := ed25519.Sign(privateKey, message)
	ok := ed25519.Verify(publicKey, message, signature)
	emit("S19", "Ed25519", fmt.Sprintf("pk=%x sig=%x verify=%t", []byte(publicKey), signature, ok))
}

func deriveSessionKey(sharedSecret []byte) []byte {
	key, err := hkdf.Key(sha256.New, sharedSecret, nil, sessionInfo, 32)
	check(err)
	return key
}

// S20: X25519 + ECDH P-256 key agreement, HKDF session key
func s20KeyAgreement() {
	x25519 := ecdh.X25519()
	alice, err := x25519.GenerateKey(rand.Reader)
	check(err)
	bob, err := x25519.GenerateKey(rand.Reader)
	check(err)
	xAlice, err := alice.ECDH(bob.PublicKey())
	check(err)
	xBob, err := bob.ECDH(alice.PublicKey())
	check(err)
	emit("S20", "X25519", fmt.Sprintf("agree=%t", bytes.Equal(xAlice, xBob)))

	p256 := ecdh.P256()
	aliceEC, err := p256.GenerateKey(rand.Reader)
	check(err)
	bobEC, err := p256.GenerateKey(rand.Reader)
	check(err)
	zAlice, err := aliceEC.ECDH(bobEC.PublicKey())
	check(err)
	zBob, err := bobEC.ECDH(aliceEC.PublicKey())
	check(err)
	emit("S20", "ECDH P-256", fmt.Sprintf("agree=%t", bytes.Equal(zAlice, zBob)))

	kAlice := deriveSessionKey(append(bytes.Clone(xAlice), zAlice...))
	kBob := deriveSessionKey(append(bytes.Clone(xBob), zBob...))
	emit("S20", "HKDF session key", fmt.Sprintf("match=%t", bytes.Equal(kAlice, kBob)))
}

// S21: ML-KEM-768 (FIPS 203)
func s21MLKEM768() {
	decapsulationKey, err := mlkem.GenerateKey768()
	check(err)
	sharedSecret, ciphertext := decapsulationKey.EncapsulationKey().Encapsulate()
	recovered, err := decapsulationKey.Decapsulate(ciphertext)
	check(err)
	emit("S21", "ML-KEM-768", fmt.Sprintf("agree=%t ct=%d ss=%d", bytes.Equal(sharedSecret, recovered), len(ciphertext), len(sharedSecret)))
}

// S22: ML-DSA-65 (FIPS 204)
func s22MLDSA65() {
	publicKey, privateKey, err := mldsa65.GenerateKey(rand.Reader)
	check(err)
	signature := make([]byte, mldsa65.SignatureSize)
	check(mldsa65.SignTo(privateKey, message, nil, true, signature))
	ok := mldsa65.Verify(publicKey, message, nil, signature)
	emit("S22", "ML-DSA-65", fmt.Sprintf("verify=%t sig=%d", ok, len(signature)))
}

// S23: self-signed X.509 certificate
func s23X509SelfSigned() {
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	check(err)
	serial, err := rand.Int(rand.Reader, new(big.Int).Lsh(big.NewInt(1), 64))
	check(err)
	now := time.Now()
	template := &x509.Certificate{
		SerialNumber:       serial,
		Subject:            pkix.Name{CommonName: tlsServerName},
		NotBefore:          now.Add(-time.Minute),
		NotAfter:           now.Add(365 * 24 * time.Hour),
		SignatureAlgorithm: x509.ECDSAWithSHA256,
	}
	der, err := x509.CreateCertificate(rand.Reader, template, template, &key.PublicKey, key)
	check(err)
	certificate, err := x509.ParseCertificate(der)
	check(err)
	ok := certificate.CheckSignature(certificate.SignatureAlgorithm, certificate.RawTBSCertificate, certificate.Signature) == nil
	emit("S23", "X.509 self-signed", fmt.Sprintf("verify=%t", ok))
}

// S24: TLS 1.3-only client configuration (no connection is made)
func s24TLS13Client() {
	config := &tls.Config{
		MinVersion: tls.VersionTLS13,
		MaxVersion: tls.VersionTLS13,
		ServerName: tlsServerName,
	}
	emit("S24", "TLS 1.3 client", fmt.Sprintf("configured=%t", config != nil))
}

func main() {
	s01SHA256()
	s02SHA2SHA3BLAKE2()
	s03LegacyHashes()
	s04SHAKE128()
	s05HMACSHA256()
	s06HKDFSHA256()
	s07PBKDF2()
	s08Scrypt()
	s09Argon2id()
	s10Bcrypt()
	s11AES256GCM()
	s12ChaCha20Poly1305()
	s13AES256CBC()
	s14AES128ECB()
	s15AES256CTR()
	s16TDEACBC()
	s17RSA3072()
	s18ECDSAP256()
	s19Ed25519()
	s20KeyAgreement()
	s21MLKEM768()
	s22MLDSA65()
	s23X509SelfSigned()
	s24TLS13Client()
}
