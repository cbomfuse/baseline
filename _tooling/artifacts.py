"""The Artifacts case: cryptography that lives in files rather than in program code.

``python3 artifacts.py generate`` creates the artifact files under ``../Artifacts``: an RSA/ECDSA test PKI
(PEM, DER and PKCS#7 certificates, PKCS#1, SEC 1, PKCS#8 and encrypted PKCS#8 keys, a CSR and a CRL), a
legacy SHA-1 certificate, an Ed25519 device certificate, an OpenSSH key pair, PKCS#12 and JKS keystores,
application secrets, an OpenSSL TLS 1.3 configuration, ML-DSA-65 / ML-KEM-768 certificates and keys, and two
decoy files.  Keys are random, so it refuses to overwrite an existing case unless ``--force`` is given.

``python3 artifacts.py`` (no argument) parses the committed files, checks every object against the registry
below (names, serials, validity, algorithms, key matches, signatures, passwords) and writes
``Artifacts/README.md``, ``Artifacts/cbom.cdx.json`` and ``Artifacts/ground-truth.json`` plus the corpus
``README.md``.  Every occurrence is found by parsing the files, so fingerprints and coordinates are exact.

Needs the ``cryptography`` package with ML-DSA and ML-KEM support (tested with 50.0.1 and its bundled
OpenSSL 4.0.2).  Every key, certificate, password and token in the case was generated for the corpus and
protects nothing.
"""
import argparse
import base64
import datetime
import hashlib
import hmac
import json
import re
import secrets
import string
import struct
import sys
import uuid
from collections import Counter, OrderedDict

from cryptography import __version__ as CRYPTOGRAPHY_VERSION
from cryptography import x509
from cryptography.hazmat.backends import openssl as _openssl_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, mldsa, mlkem, padding, rsa
from cryptography.hazmat.primitives.serialization import pkcs7, pkcs12
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

import markers
import spec
from build_sources import OUT

CASE_DIR = "Artifacts"
CASE = OUT / CASE_DIR
GENERATED_DOCS = ("README.md", "cbom.cdx.json", "ground-truth.json")
ID_PREFIX = "AR"
UTC = datetime.timezone.utc
GEN_TIME = datetime.datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def T(y, m, d):
    return datetime.datetime(y, m, d, tzinfo=UTC)


ORG = "CBOMFuse Baseline"
KEYSTORE_PASSWORD = "changeit"           # the JDK default; CBOM-Lens and keytool users try it first
JKS_ENTRY_TIME = T(2026, 1, 1)
JWT_PAYLOAD = OrderedDict([("iss", "https://auth.cbom-corpus.example"), ("sub", "svc-reporting"),
                           ("aud", "reports-api"), ("scope", "reports:read"),
                           ("iat", int(T(2026, 1, 1).timestamp())), ("exp", int(T(2027, 1, 1).timestamp()))])

# ---------------------------------------------------------------------------------------------- registry
SCENARIOS = [
    ("A01", "Certificates and keys", "RSA/ECDSA test PKI: RSA-4096 root CA, ECDSA P-384 issuing CA with its SEC 1 key, "
                                     "and a chain bundle whose blocks are preceded by subject=/issuer= lines"),
    ("A02", "Certificates and keys", "TLS server: PEM certificate (RSA-2048 key, signed ecdsa-with-SHA384), PKCS#1 key, "
                                     "PKCS#10 CSR and a PKCS#7 full chain"),
    ("A03", "Certificates and keys", "API endpoint: DER certificate (ECDSA P-256 key) and its PKCS#8 key"),
    ("A04", "Certificates and keys", "Certificate revocation list from the issuing CA (one revoked serial)"),
    ("A05", "Certificates and keys", "Legacy self-signed certificate: RSA-1024 key, sha1WithRSAEncryption, DER"),
    ("A06", "Certificates and keys", "Ed25519 device certificate and its PKCS#8 key"),
    ("A07", "Certificates and keys", "RSA-3072 backup key as encrypted PKCS#8 (PBES2) plus its SPKI public key"),
    ("A08", "Certificates and keys", "OpenSSH Ed25519 deploy key pair"),
    ("A09", "Keystores", "PKCS#12 client keystore: ECDSA P-256 key, client certificate and issuing CA certificate"),
    ("A10", "Keystores", "JKS truststore: the root CA and a partner root CA that occurs nowhere else"),
    ("A11", "Secrets and TLS configuration", "dotenv file: HS256 signing key, a JWT signed with it, the keystore "
                                             "password and the backup-key passphrase"),
    ("A12", "Secrets and TLS configuration", "Terraform resource with a database password"),
    ("A13", "Secrets and TLS configuration", "OpenSSL configuration: TLS 1.3 only, two cipher suites, a hybrid "
                                             "post-quantum key-exchange group"),
    ("A14", "Post-quantum artifacts", "ML-DSA-65 root CA and an ML-KEM-768 endpoint certificate it signed, with both "
                                      "PKCS#8 keys"),
]
SCENARIO_FAMILY = {sid: fam for sid, fam, _ in SCENARIOS}

FILES = OrderedDict([
    ("pki/root-ca.crt", dict(scn="A01", kind="pem", fmt="PEM certificate", desc="Root CA certificate")),
    ("pki/issuing-ca.crt", dict(scn="A01", kind="pem", fmt="PEM certificate", desc="Issuing CA certificate")),
    ("pki/issuing-ca.key", dict(scn="A01", kind="pem", fmt="SEC 1 EC PRIVATE KEY", desc="Issuing CA private key",
                                key="issuing-ca")),
    ("pki/ca-chain.pem", dict(scn="A01", kind="pem", fmt="PEM bundle (2 certificates)",
                              desc="Issuing CA and root CA, each preceded by subject=/issuer= lines")),
    ("pki/server.crt", dict(scn="A02", kind="pem", fmt="PEM certificate", desc="TLS server certificate")),
    ("pki/server.key", dict(scn="A02", kind="pem", fmt="PKCS#1 RSA PRIVATE KEY", desc="TLS server private key",
                            key="server")),
    ("pki/server.csr", dict(scn="A02", kind="pem", fmt="PKCS#10 CERTIFICATE REQUEST",
                            desc="Certificate signing request for the server key")),
    ("pki/fullchain.p7b", dict(scn="A02", kind="pkcs7", fmt="PKCS#7 certs-only, DER",
                               desc="Server certificate, issuing CA and root CA")),
    ("pki/api.der", dict(scn="A03", kind="der-cert", fmt="DER certificate", desc="API endpoint certificate")),
    ("pki/api.key", dict(scn="A03", kind="pem", fmt="PKCS#8 PRIVATE KEY", desc="API endpoint private key",
                         key="api")),
    ("pki/issuing-ca.crl", dict(scn="A04", kind="pem", fmt="PEM X509 CRL", desc="CRL of the issuing CA")),
    ("pki/legacy-sha1.cer", dict(scn="A05", kind="der-cert", fmt="DER certificate",
                                 desc="Legacy self-signed SHA-1 certificate")),
    ("pki/device-ed25519.crt", dict(scn="A06", kind="pem", fmt="PEM certificate",
                                    desc="Self-signed Ed25519 device certificate")),
    ("keys/device-ed25519.pem", dict(scn="A06", kind="pem", fmt="PKCS#8 PRIVATE KEY", desc="Device private key",
                                     key="device")),
    ("keys/backup-rsa3072.enc.pem", dict(scn="A07", kind="pem", fmt="PKCS#8 ENCRYPTED PRIVATE KEY (PBES2)",
                                         desc="Backup private key, passphrase in secrets/app.env", key="backup")),
    ("keys/backup-rsa3072.pub.pem", dict(scn="A07", kind="pem", fmt="SPKI PUBLIC KEY", desc="Backup public key",
                                         key="backup")),
    ("keys/deploy_ed25519", dict(scn="A08", kind="pem", fmt="OPENSSH PRIVATE KEY", desc="Deploy private key",
                                 key="deploy")),
    ("keys/deploy_ed25519.pub", dict(scn="A08", kind="openssh-pub", fmt="OpenSSH public key line",
                                     desc="Deploy public key", key="deploy")),
    ("keystores/client.p12", dict(scn="A09", kind="pkcs12", fmt="PKCS#12 (password changeit)",
                                  desc="Client key, client certificate and issuing CA")),
    ("keystores/truststore.jks", dict(scn="A10", kind="jks", fmt="JKS (password changeit)",
                                      desc="Root CA and partner root CA as trusted certificate entries")),
    ("secrets/app.env", dict(scn="A11", kind="env", fmt="dotenv", desc="Reporting service settings")),
    ("secrets/main.tf", dict(scn="A12", kind="terraform", fmt="Terraform (HCL)", desc="Reporting database resource")),
    ("tls/openssl.cnf", dict(scn="A13", kind="openssl-cnf", fmt="OpenSSL configuration",
                             desc="System-wide TLS defaults")),
    ("pqc/pq-root-ca.crt", dict(scn="A14", kind="pem", fmt="PEM certificate", desc="ML-DSA-65 root CA certificate")),
    ("pqc/pq-root-ca.key", dict(scn="A14", kind="pem", fmt="PKCS#8 PRIVATE KEY (seed form)",
                                desc="ML-DSA-65 root CA private key", key="pq-root")),
    ("pqc/kem-endpoint.crt", dict(scn="A14", kind="pem", fmt="PEM certificate",
                                  desc="ML-KEM-768 endpoint certificate")),
    ("pqc/kem-endpoint.key", dict(scn="A14", kind="pem", fmt="PKCS#8 PRIVATE KEY (seed form)",
                                  desc="ML-KEM-768 endpoint private key", key="kem-endpoint")),
    ("examples/placeholder.crt", dict(scn="-", kind="decoy", fmt="PEM armour, no certificate",
                                      desc="Placeholder telling an operator where to paste a certificate")),
    ("examples/deploy-notes.md", dict(scn="-", kind="decoy", fmt="Markdown",
                                      desc="Deployment notes quoting a shortened (unusable) private key")),
])

# key id -> algorithm, holder, whether the private key is stored anywhere in the case
KEYS = OrderedDict([
    ("root-ca", dict(alg="rsa-4096", holder="Root CA", private=False)),
    ("issuing-ca", dict(alg="ecdsa-p384", holder="Issuing CA", private=True)),
    ("server", dict(alg="rsa-2048", holder="TLS server", private=True)),
    ("api", dict(alg="ecdsa-p256", holder="API endpoint", private=True)),
    ("client", dict(alg="ecdsa-p256", holder="client svc-reporting", private=True)),
    ("device", dict(alg="ed25519", holder="device-42", private=True)),
    ("legacy", dict(alg="rsa-1024", holder="legacy service", private=False)),
    ("partner-ca", dict(alg="rsa-2048", holder="partner root CA", private=False)),
    ("backup", dict(alg="rsa-3072", holder="backup", private=True)),
    ("deploy", dict(alg="ed25519", holder="OpenSSH deploy key", private=True)),
    ("pq-root", dict(alg="ml-dsa-65", holder="PQC root CA", private=True)),
    ("kem-endpoint", dict(alg="ml-kem-768", holder="KEM endpoint", private=True)),
])
KEY_SCENARIO = {"root-ca": "A01", "issuing-ca": "A01", "server": "A02", "api": "A03", "client": "A09",
                "device": "A06", "legacy": "A05", "partner-ca": "A10", "backup": "A07", "deploy": "A08",
                "pq-root": "A14", "kem-endpoint": "A14"}


def _dn(cn, ou=None, org=ORG, c="CA"):
    rdns = [("C", c), ("O", org)] + ([("OU", ou)] if ou else []) + [("CN", cn)]
    return rdns


CA_USAGE = dict(digital_signature=False, key_cert_sign=True, crl_sign=True)
CERTS = OrderedDict([
    ("cert.root-ca", dict(name="CBOMFuse Test Root CA", dn=_dn("CBOMFuse Test Root CA"), issuer="cert.root-ca",
                          key="root-ca", sig="sha256-with-rsa", serial=0x01, nb=T(2026, 1, 1), na=T(2046, 1, 1),
                          ca=True, pathlen=None, ku=CA_USAGE, scn="A01")),
    ("cert.issuing-ca", dict(name="CBOMFuse Test Issuing CA", dn=_dn("CBOMFuse Test Issuing CA"),
                             issuer="cert.root-ca", key="issuing-ca", sig="sha256-with-rsa", serial=0x1000,
                             nb=T(2026, 1, 1), na=T(2036, 1, 1), ca=True, pathlen=0, ku=CA_USAGE, scn="A01")),
    ("cert.server", dict(name="server.cbom-corpus.example", dn=_dn("server.cbom-corpus.example"),
                         issuer="cert.issuing-ca", key="server", sig="ecdsa-with-sha384", serial=0x2001,
                         nb=T(2026, 1, 1), na=T(2028, 1, 1), ca=False,
                         ku=dict(digital_signature=True, key_encipherment=True), eku=["serverAuth"],
                         san=["server.cbom-corpus.example"], scn="A02")),
    ("cert.api", dict(name="api.cbom-corpus.example", dn=_dn("api.cbom-corpus.example"), issuer="cert.issuing-ca",
                      key="api", sig="ecdsa-with-sha384", serial=0x2002, nb=T(2026, 1, 1), na=T(2028, 1, 1),
                      ca=False, ku=dict(digital_signature=True), eku=["serverAuth"],
                      san=["api.cbom-corpus.example"], scn="A03")),
    ("cert.client", dict(name="svc-reporting", dn=_dn("svc-reporting", ou="Service Accounts"),
                         issuer="cert.issuing-ca", key="client", sig="ecdsa-with-sha384", serial=0x2003,
                         nb=T(2026, 1, 1), na=T(2028, 1, 1), ca=False, ku=dict(digital_signature=True),
                         eku=["clientAuth"], scn="A09")),
    ("cert.device", dict(name="device-42.cbom-corpus.example", dn=_dn("device-42.cbom-corpus.example"),
                         issuer="cert.device", key="device", sig="ed25519", serial=0x3001, nb=T(2026, 1, 1),
                         na=T(2031, 1, 1), ca=False, ku=dict(digital_signature=True),
                         san=["device-42.cbom-corpus.example"], scn="A06")),
    ("cert.legacy", dict(name="legacy.cbom-corpus.example", dn=_dn("legacy.cbom-corpus.example"),
                         issuer="cert.legacy", key="legacy", sig="sha1-with-rsa", serial=0x1999, nb=T(2016, 1, 1),
                         na=T(2036, 1, 1), ca=False, ku=dict(digital_signature=True, key_encipherment=True),
                         scn="A05")),
    ("cert.partner-ca", dict(name="CBOMFuse Partner Root CA", dn=_dn("CBOMFuse Partner Root CA", org="CBOMFuse Partner"),
                             issuer="cert.partner-ca", key="partner-ca", sig="sha256-with-rsa", serial=0x50,
                             nb=T(2026, 1, 1), na=T(2041, 1, 1), ca=True, pathlen=None, ku=CA_USAGE, scn="A10")),
    ("cert.pq-root-ca", dict(name="CBOMFuse PQC Test Root CA", dn=_dn("CBOMFuse PQC Test Root CA"),
                             issuer="cert.pq-root-ca", key="pq-root", sig="ml-dsa-65", serial=0x7001,
                             nb=T(2026, 1, 1), na=T(2041, 1, 1), ca=True, pathlen=None, ku=CA_USAGE, scn="A14")),
    ("cert.kem-endpoint", dict(name="kem.cbom-corpus.example", dn=_dn("kem.cbom-corpus.example"),
                               issuer="cert.pq-root-ca", key="kem-endpoint", sig="ml-dsa-65", serial=0x7002,
                               nb=T(2026, 1, 1), na=T(2028, 1, 1), ca=False,
                               ku=dict(digital_signature=False, key_encipherment=True),
                               san=["kem.cbom-corpus.example"], scn="A14")),
])
CRL_SPEC = dict(issuer="cert.issuing-ca", sig="ecdsa-with-sha384", this_update=T(2026, 1, 15),
                next_update=T(2027, 1, 15), number=1, revoked=[(0x2000, T(2026, 1, 10))])
CSR_SPEC = dict(key="server", subject="cert.server", sig="sha256-with-rsa")

# OIDs -> algorithm asset ids
SIG_ALG = {"1.2.840.113549.1.1.11": "sha256-with-rsa", "1.2.840.113549.1.1.5": "sha1-with-rsa",
           "1.2.840.10045.4.3.3": "ecdsa-with-sha384", "1.3.101.112": "ed25519",
           "2.16.840.1.101.3.4.3.18": "ml-dsa-65"}
SIG_HASH = {"sha256-with-rsa": "sha-256", "sha1-with-rsa": "sha-1", "ecdsa-with-sha384": "sha-384"}
OID = {"rsaEncryption": "1.2.840.113549.1.1.1", "id-ecPublicKey": "1.2.840.10045.2.1", "Ed25519": "1.3.101.112",
       "ML-DSA-65": "2.16.840.1.101.3.4.3.18", "ML-KEM-768": "2.16.840.1.101.3.4.4.2",
       "PBES2": "1.2.840.113549.1.5.13", "PBKDF2": "1.2.840.113549.1.5.12", "hmacWithSHA256": "1.2.840.113549.2.9",
       "aes256-CBC": "2.16.840.1.101.3.4.1.42", "sha256": "2.16.840.1.101.3.4.2.1", "data": "1.2.840.113549.1.7.1",
       "encryptedData": "1.2.840.113549.1.7.6", "pkcs8ShroudedKeyBag": "1.2.840.113549.1.12.10.1.2",
       "certBag": "1.2.840.113549.1.12.10.1.3", "secp384r1": "1.3.132.0.34", "prime256v1": "1.2.840.10045.3.1.7"}
KEY_ALG_OID = {"rsa": OID["rsaEncryption"], "ecdsa": OID["id-ecPublicKey"], "ed25519": OID["Ed25519"],
               "ml-dsa-65": OID["ML-DSA-65"], "ml-kem-768": OID["ML-KEM-768"]}
CIPHER_SUITES = {"TLS_AES_256_GCM_SHA384": (["0x13", "0x02"], ["aes-256-gcm", "sha-384"]),
                 "TLS_AES_128_GCM_SHA256": (["0x13", "0x01"], ["aes-128-gcm", "sha-256"]),
                 "TLS_CHACHA20_POLY1305_SHA256": (["0x13", "0x03"], ["chacha20-poly1305", "sha-256"])}
TLS_GROUPS = {"X25519MLKEM768": ("x25519mlkem768", ["ml-kem-768", "x25519"]), "X25519": ("x25519", [])}

# Notes that only make sense for this case; the spec entries stay as they are for the five programs.
ALG_OVERRIDES = {
    "sha-384": dict(note="Hash of ecdsa-with-SHA384 and of the TLS_AES_256_GCM_SHA384 cipher suite."),
    "ml-dsa-65": dict(note="One OID names both the subjectPublicKeyInfo algorithm and the signature algorithm."),
    "rsa-3072": dict(note="Backup key; stored only as encrypted PKCS#8 and as an SPKI public key."),
    "hmac-sha256": dict(nistStatus="Approved (FIPS 198-1)",
                        note="HS256 for the JWT (RFC 7518) and the PKCS#12 integrity MAC (key from the PKCS#12 "
                             "KDF of RFC 7292 appendix B.2)."),
    "pbkdf2-hmac-sha256": dict(nistStatus="Approved (SP 800-132); the iteration counts used here (2,048 and 20,000) "
                                          "are below the OWASP 2023 figure of 600,000",
                               note="PBES2 key derivation (RFC 8018) in the encrypted PKCS#8 key and the PKCS#12 "
                                    "keystore; PRF hmacWithSHA256."),
    "aes-256-cbc": dict(note="PBES2 encryption scheme aes256-CBC-PAD (RFC 8018)."),
    "aes-256-gcm": dict(note="Record protection of TLS_AES_256_GCM_SHA384."),
}

NOTES = OrderedDict([
    ("pem-bundle", "Several PEM blocks in one file; a parser that stops at the first block misses the rest"),
    ("pem-preamble", "Free text (subject=/issuer= lines as printed by openssl) precedes each PEM block"),
    ("der", "Binary DER without PEM armour; found only by file extension or content sniffing"),
    ("pkcs7", "PKCS#7 / CMS SignedData with certificates and no signers (.p7b)"),
    ("pkcs12", "Inside a password-protected PKCS#12 file; certificates and key are encrypted (PBES2) and readable "
               "only with the password (changeit)"),
    ("jks", "Inside a Java KeyStore; trusted certificate entries are stored in clear, the file is "
            "integrity-protected with the store password (changeit)"),
    ("pkcs1", "PKCS#1 RSAPrivateKey: the algorithm is implied by the PEM label; modulus and public exponent are "
              "stored with the private key"),
    ("sec1", "SEC 1 ECPrivateKey: the curve OID and the public point are stored with the private scalar"),
    ("pkcs8", "PKCS#8 PrivateKeyInfo with its algorithm identifier"),
    ("pkcs8-encrypted", "Encrypted PKCS#8 (PBES2): the key and its algorithm are inside the ciphertext; the "
                        "passphrase is in secrets/app.env"),
    ("pkcs8-seed", "PKCS#8 private key in seed form: the public key is not stored and must be derived"),
    ("openssh", "OpenSSH openssh-key-v1 container: key type string, public key and private key"),
    ("openssh-pub", "One-line OpenSSH public key (type, base64 blob, comment)"),
    ("spki", "Subject public key info"),
    ("pqc-oid", "Post-quantum algorithm identified only by its OID; libraries without ML-DSA / ML-KEM support "
                "reject the object"),
    ("nested-hash", "Hash named only as part of a composite signature algorithm identifier"),
    ("csr", "PKCS#10 certificate request: signed by the key it asks to have certified"),
    ("crl", "X.509 CRL: signed list of revoked serial numbers"),
    ("jwt", "JSON Web Token: the algorithm is named in its base64url-encoded header"),
    ("env-secret", "Secret assigned in a dotenv file"),
    ("low-entropy-secret", "Default or low-entropy value: entropy-based secret scanners do not report it"),
    ("tf-secret", "Secret in a Terraform resource; gitleaks applies its Terraform password rule only to *.tf and "
                  "*.hcl paths"),
    ("openssl-cnf", "OpenSSL configuration directive in the system default section"),
    ("suite-name", "Algorithms named inside a TLS cipher-suite name"),
    ("hybrid-group", "Hybrid post-quantum TLS key-exchange group (ML-KEM-768 + X25519)"),
])

# ---------------------------------------------------------------------------------------------- DER helpers
def der_tlv(buf, i):
    """(tag, content_start, content_end) of the DER element at offset i."""
    tag = buf[i]
    j = i + 1
    if tag & 0x1F == 0x1F:
        while buf[j] & 0x80:
            j += 1
        j += 1
    ln = buf[j]
    j += 1
    if ln & 0x80:
        n = ln & 0x7F
        if n == 0 or n > 4:
            raise ValueError("unsupported DER length")
        ln = int.from_bytes(buf[j:j + n], "big")
        j += n
    if j + ln > len(buf):
        raise ValueError("truncated DER element")
    return tag, j, j + ln


def der_children(buf, start, end):
    out, i = [], start
    while i < end:
        tag, cs, ce = der_tlv(buf, i)
        out.append((i, tag, cs, ce))
        i = ce
    if i != end:
        raise ValueError("DER children overrun")
    return out


def oid_str(b):
    first = b[0]
    parts = [first // 40, first % 40] if first < 80 else [2, first - 80]
    v = 0
    for x in b[1:]:
        v = (v << 7) | (x & 0x7F)
        if not x & 0x80:
            parts.append(v)
            v = 0
    return ".".join(str(p) for p in parts)


def der_int(buf, cs, ce):
    return int.from_bytes(buf[cs:ce], "big", signed=True)


def algid(buf, off):
    """OID string and parameter children of the AlgorithmIdentifier at off."""
    _, cs, ce = der_tlv(buf, off)
    kids = der_children(buf, cs, ce)
    if kids[0][1] != 0x06:
        raise ValueError("AlgorithmIdentifier without OID")
    return oid_str(buf[kids[0][2]:kids[0][3]]), kids[1:]


def pbes2_params(buf, off):
    """Parse the PBES2 AlgorithmIdentifier at off: KDF, PRF, iterations and encryption scheme with offsets."""
    oid, params = algid(buf, off)
    if oid != OID["PBES2"]:
        raise ValueError(f"expected PBES2, found {oid}")
    _, pcs, pce = params[0][1], params[0][2], params[0][3]
    kdf_off, enc_off = [k[0] for k in der_children(buf, pcs, pce)]
    kdf_oid, kdf_params = algid(buf, kdf_off)
    kp = der_children(buf, kdf_params[0][2], kdf_params[0][3])
    iterations = der_int(buf, kp[1][2], kp[1][3])
    prf = "1.2.840.113549.2.7"                 # RFC 8018 default PRF: hmacWithSHA1
    prf_off = None
    for k in kp[2:]:
        if k[1] == 0x30:
            prf_off = k[0]
            prf = algid(buf, k[0])[0]
    enc_oid, enc_params = algid(buf, enc_off)
    return dict(offset=off, end=der_tlv(buf, off)[2], kdf=kdf_oid, kdf_offset=kdf_off, prf=prf, prf_offset=prf_off,
                iterations=iterations, enc=enc_oid, enc_offset=enc_off, salt=bytes(buf[kp[0][2]:kp[0][3]]),
                iv=bytes(buf[enc_params[0][2]:enc_params[0][3]]))


def pbes2_decrypt(info, ciphertext, password):
    """Decrypt PBES2 (PBKDF2-HMAC-SHA256, AES-256-CBC) content; OpenSSL and keytool pass the password as UTF-8."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.padding import PKCS7
    key = PBKDF2HMAC(hashes.SHA256(), 32, info["salt"], info["iterations"]).derive(password.encode())
    dec = Cipher(algorithms.AES(key), modes.CBC(info["iv"])).decryptor()
    unpad = PKCS7(128).unpadder()
    return unpad.update(dec.update(ciphertext) + dec.finalize()) + unpad.finalize()


def spki_der(pub):
    return pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)


def key_identifier(pub):
    """RFC 5280 section 4.2.1.2 method 1 (SHA-1 over the subjectPublicKey bits)."""
    der = spki_der(pub)
    _, cs, ce = der_tlv(der, 0)
    bits = der_children(der, cs, ce)[1]
    return hashlib.sha1(der[bits[2] + 1:bits[3]]).digest()


def key_alg_id(pub):
    if isinstance(pub, rsa.RSAPublicKey):
        return f"rsa-{pub.key_size}"
    if isinstance(pub, ec.EllipticCurvePublicKey):
        return {"secp256r1": "ecdsa-p256", "secp384r1": "ecdsa-p384"}[pub.curve.name]
    if isinstance(pub, ed25519.Ed25519PublicKey):
        return "ed25519"
    if isinstance(pub, mldsa.MLDSA65PublicKey):
        return "ml-dsa-65"
    if isinstance(pub, mlkem.MLKEM768PublicKey):
        return "ml-kem-768"
    raise TypeError(f"unexpected public key type {type(pub).__name__}")


def key_alg_oid(alg):
    if alg.startswith("rsa-"):
        return KEY_ALG_OID["rsa"]
    if alg.startswith("ecdsa-"):
        return KEY_ALG_OID["ecdsa"]
    return KEY_ALG_OID[alg]


def b64url(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def b64url_dec(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def x509_name(rdns):
    attr = {"C": NameOID.COUNTRY_NAME, "O": NameOID.ORGANIZATION_NAME, "OU": NameOID.ORGANIZATIONAL_UNIT_NAME,
            "CN": NameOID.COMMON_NAME}
    return x509.Name([x509.NameAttribute(attr[k], v) for k, v in rdns])


def rfc3339(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------------------------- generation
def _new_key(alg):
    if alg.startswith("rsa-"):
        return rsa.generate_private_key(public_exponent=65537, key_size=int(alg.split("-")[1]))
    if alg == "ecdsa-p256":
        return ec.generate_private_key(ec.SECP256R1())
    if alg == "ecdsa-p384":
        return ec.generate_private_key(ec.SECP384R1())
    if alg == "ed25519":
        return ed25519.Ed25519PrivateKey.generate()
    if alg == "ml-dsa-65":
        return mldsa.MLDSA65PrivateKey.generate()
    if alg == "ml-kem-768":
        return mlkem.MLKEM768PrivateKey.generate()
    raise KeyError(alg)


SIGN_HASH = {"sha256-with-rsa": hashes.SHA256(), "ecdsa-with-sha384": hashes.SHA384(), "ed25519": None,
             "ml-dsa-65": None}


def _key_usage(ku):
    flags = dict(digital_signature=False, content_commitment=False, key_encipherment=False, data_encipherment=False,
                 key_agreement=False, key_cert_sign=False, crl_sign=False, encipher_only=False, decipher_only=False)
    flags.update(ku)
    return x509.KeyUsage(**flags)


def _resign_sha1(cert, key):
    """cryptography refuses SHA-1 signatures, so build with SHA-256, swap the two AlgorithmIdentifiers to
    sha1WithRSAEncryption (same encoded length) and sign the TBS again with SHA-1."""
    der = cert.public_bytes(serialization.Encoding.DER)
    old = bytes.fromhex("06092a864886f70d01010b")
    new = bytes.fromhex("06092a864886f70d010105")
    if der.count(old) != 2:
        raise RuntimeError("unexpected sha256WithRSAEncryption count in certificate")
    der = der.replace(old, new)
    _, cs, ce = der_tlv(der, 0)
    tbs_off, _, _ = der_children(der, cs, ce)[0][:3]
    _, tcs, tce = der_tlv(der, tbs_off)
    tbs = der[tbs_off:tce]
    sig = key.sign(tbs, padding.PKCS1v15(), hashes.SHA1())
    alg = bytes.fromhex("300d06092a864886f70d0101050500")
    bits = b"\x03" + _der_len(len(sig) + 1) + b"\x00" + sig
    body = tbs + alg + bits
    out = b"\x30" + _der_len(len(body)) + body
    c = x509.load_der_x509_certificate(out)
    key.public_key().verify(c.signature, c.tbs_certificate_bytes, padding.PKCS1v15(), hashes.SHA1())
    return c


def _der_len(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _build_cert(cid, keys):
    c = CERTS[cid]
    issuer = CERTS[c["issuer"]]
    pub = keys[c["key"]].public_key()
    ski = key_identifier(pub)
    b = (x509.CertificateBuilder().subject_name(x509_name(c["dn"])).issuer_name(x509_name(issuer["dn"]))
         .public_key(pub).serial_number(c["serial"]).not_valid_before(c["nb"]).not_valid_after(c["na"])
         .add_extension(x509.BasicConstraints(ca=c["ca"], path_length=c.get("pathlen") if c["ca"] else None),
                        critical=True)
         .add_extension(_key_usage(c["ku"]), critical=True)
         .add_extension(x509.SubjectKeyIdentifier(ski), critical=False))
    if c["issuer"] != cid:
        b = b.add_extension(x509.AuthorityKeyIdentifier(key_identifier(keys[issuer["key"]].public_key()), None, None),
                            critical=False)
    if c.get("eku"):
        b = b.add_extension(x509.ExtendedKeyUsage([getattr(ExtendedKeyUsageOID, {"serverAuth": "SERVER_AUTH",
                                                                                 "clientAuth": "CLIENT_AUTH"}[u])
                                                   for u in c["eku"]]), critical=False)
    if c.get("san"):
        b = b.add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in c["san"]]), critical=False)
    signer = keys[issuer["key"]]
    if c["sig"] == "sha1-with-rsa":
        return _resign_sha1(b.sign(signer, hashes.SHA256()), signer)
    return b.sign(signer, SIGN_HASH[c["sig"]])


def _pem(cert):
    return cert.public_bytes(serialization.Encoding.PEM)


def _jks(entries, password):
    """A JKS keystore holding trusted certificate entries only (tag 2), as written by keytool."""
    def utf(s):
        raw = s.encode("utf-8")
        return struct.pack(">H", len(raw)) + raw
    out = struct.pack(">III", 0xFEEDFEED, 2, len(entries))
    for alias, when, der in entries:
        out += struct.pack(">I", 2) + utf(alias) + struct.pack(">q", int(when.timestamp() * 1000))
        out += utf("X.509") + struct.pack(">I", len(der)) + der
    return out + hashlib.sha1(password.encode("utf-16-be") + b"Mighty Aphrodite" + out).digest()


def _secret(alphabet, n):
    return "".join(secrets.choice(alphabet) for _ in range(n))


def generate(force=False):
    existing = [p for p in CASE.rglob("*") if p.is_file()] if CASE.exists() else []
    if existing and not force:
        sys.exit(f"{CASE} already holds {len(existing)} files; rerun with --force to replace every key and certificate")
    keys = {kid: _new_key(k["alg"]) for kid, k in KEYS.items()}
    certs = OrderedDict()
    for cid in CERTS:
        certs[cid] = _build_cert(cid, keys)
    files = OrderedDict()
    pem_cert = {cid: _pem(c) for cid, c in certs.items()}
    files["pki/root-ca.crt"] = pem_cert["cert.root-ca"]
    files["pki/issuing-ca.crt"] = pem_cert["cert.issuing-ca"]
    files["pki/issuing-ca.key"] = keys["issuing-ca"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption())

    def preamble(cid):
        c = CERTS[cid]
        fmt = lambda rdns: ", ".join(f"{k}={v}" for k, v in rdns)  # noqa: E731  (openssl 3 default -nameopt)
        return f"subject={fmt(c['dn'])}\nissuer={fmt(CERTS[c['issuer']]['dn'])}\n".encode()
    files["pki/ca-chain.pem"] = (preamble("cert.issuing-ca") + pem_cert["cert.issuing-ca"] +
                                 preamble("cert.root-ca") + pem_cert["cert.root-ca"])
    files["pki/server.crt"] = pem_cert["cert.server"]
    files["pki/server.key"] = keys["server"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption())
    csr = (x509.CertificateSigningRequestBuilder().subject_name(x509_name(CERTS["cert.server"]["dn"]))
           .add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in CERTS["cert.server"]["san"]]),
                          critical=False)
           .sign(keys["server"], hashes.SHA256()))
    files["pki/server.csr"] = csr.public_bytes(serialization.Encoding.PEM)
    files["pki/fullchain.p7b"] = pkcs7.serialize_certificates(
        [certs["cert.server"], certs["cert.issuing-ca"], certs["cert.root-ca"]], serialization.Encoding.DER)
    files["pki/api.der"] = certs["cert.api"].public_bytes(serialization.Encoding.DER)
    files["pki/api.key"] = keys["api"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    crl_b = (x509.CertificateRevocationListBuilder().issuer_name(x509_name(CERTS["cert.issuing-ca"]["dn"]))
             .last_update(CRL_SPEC["this_update"]).next_update(CRL_SPEC["next_update"])
             .add_extension(x509.CRLNumber(CRL_SPEC["number"]), critical=False)
             .add_extension(x509.AuthorityKeyIdentifier(key_identifier(keys["issuing-ca"].public_key()), None, None),
                            critical=False))
    for serial, when in CRL_SPEC["revoked"]:
        crl_b = crl_b.add_revoked_certificate(
            x509.RevokedCertificateBuilder().serial_number(serial).revocation_date(when)
            .add_extension(x509.CRLReason(x509.ReasonFlags.key_compromise), critical=False).build())
    files["pki/issuing-ca.crl"] = crl_b.sign(keys["issuing-ca"], hashes.SHA384()).public_bytes(serialization.Encoding.PEM)
    files["pki/legacy-sha1.cer"] = certs["cert.legacy"].public_bytes(serialization.Encoding.DER)
    files["pki/device-ed25519.crt"] = pem_cert["cert.device"]
    files["keys/device-ed25519.pem"] = keys["device"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

    passphrase = _secret(string.ascii_letters + string.digits + "-_", 24)
    files["keys/backup-rsa3072.enc.pem"] = keys["backup"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(passphrase.encode()))
    files["keys/backup-rsa3072.pub.pem"] = keys["backup"].public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    files["keys/deploy_ed25519"] = keys["deploy"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.OpenSSH, serialization.NoEncryption())
    files["keys/deploy_ed25519.pub"] = keys["deploy"].public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH) + b" deploy@cbom-corpus.example\n"
    files["keystores/client.p12"] = pkcs12.serialize_key_and_certificates(
        b"svc-reporting", keys["client"], certs["cert.client"], [certs["cert.issuing-ca"]],
        serialization.BestAvailableEncryption(KEYSTORE_PASSWORD.encode()))
    files["keystores/truststore.jks"] = _jks(
        [("cbomfuse-test-root-ca", JKS_ENTRY_TIME, certs["cert.root-ca"].public_bytes(serialization.Encoding.DER)),
         ("cbomfuse-partner-root-ca", JKS_ENTRY_TIME,
          certs["cert.partner-ca"].public_bytes(serialization.Encoding.DER))], KEYSTORE_PASSWORD)

    signing_key = secrets.token_bytes(32)
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body = b64url(json.dumps(JWT_PAYLOAD, separators=(",", ":")).encode())
    sig = b64url(hmac.new(signing_key, f"{header}.{body}".encode(), hashlib.sha256).digest())
    files["secrets/app.env"] = "\n".join([
        "# Reporting service settings - test fixture for the CBOM ground-truth corpus.",
        "# Every value below was generated for the corpus and protects nothing real.",
        "APP_ENV=staging",
        "JWT_ALGORITHM=HS256",
        f"JWT_SIGNING_KEY={b64url(signing_key)}",
        f"SERVICE_TOKEN={header}.{body}.{sig}",
        "KEYSTORE_PATH=keystores/client.p12",
        "TRUSTSTORE_PATH=keystores/truststore.jks",
        f"KEYSTORE_PASSWORD={KEYSTORE_PASSWORD}",
        "BACKUP_KEY_FILE=keys/backup-rsa3072.enc.pem",
        f"BACKUP_KEY_PASSPHRASE={passphrase}",
        ""]).encode()
    db_password = _secret(string.ascii_letters + string.digits, 8) + "-" + _secret(string.ascii_letters + string.digits, 7)
    files["secrets/main.tf"] = "\n".join([
        "# Reporting database - test fixture for the CBOM ground-truth corpus; the password protects nothing real.",
        'resource "aws_db_instance" "reporting" {',
        '  identifier     = "reporting-db"',
        '  engine         = "postgres"',
        '  instance_class = "db.t3.micro"',
        '  username       = "reporting"',
        f'  password       = "{db_password}"',
        "}",
        ""]).encode()
    files["tls/openssl.cnf"] = "\n".join([
        "# OpenSSL configuration for the reporting service (test fixture for the CBOM ground-truth corpus).",
        "# Loaded through OPENSSL_CONF=tls/openssl.cnf; restricts every TLS context to version 1.3 and prefers",
        "# the hybrid post-quantum key exchange.",
        "openssl_conf = openssl_init",
        "",
        "[openssl_init]",
        "ssl_conf = ssl_sect",
        "",
        "[ssl_sect]",
        "system_default = system_default_sect",
        "",
        "[system_default_sect]",
        "MinProtocol = TLSv1.3",
        "MaxProtocol = TLSv1.3",
        "Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
        "Groups = X25519MLKEM768:X25519",
        ""]).encode()
    files["pqc/pq-root-ca.crt"] = pem_cert["cert.pq-root-ca"]
    files["pqc/pq-root-ca.key"] = keys["pq-root"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    files["pqc/kem-endpoint.crt"] = pem_cert["cert.kem-endpoint"]
    files["pqc/kem-endpoint.key"] = keys["kem-endpoint"].private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    files["examples/placeholder.crt"] = "\n".join([
        "-----BEGIN CERTIFICATE-----",
        "PASTE-THE-CERTIFICATE-ISSUED-FOR-YOUR-HOST-HERE",
        "-----END CERTIFICATE-----",
        ""]).encode()
    files["examples/deploy-notes.md"] = "\n".join([
        "# Deploying the reporting service",
        "",
        "The service reads its certificate from `pki/server.crt` and the matching key from `pki/server.key`.",
        "On a new host, paste the certificate issued for that host into `examples/placeholder.crt`; the file in",
        "this folder only shows the expected shape.",
        "",
        "Never commit a private key. This is what the start of one looks like (shortened, not a usable key):",
        "",
        "```text",
        "-----BEGIN PRIVATE KEY-----",
        "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7...",
        "...(the remaining lines are deliberately left out)...",
        "-----END PRIVATE KEY-----",
        "```",
        "",
        "Plan: move the RSA-2048 server key to ECDSA P-384 or ML-DSA-65 once every client supports it, and stop",
        "accepting SHA-1 signatures.",
        ""]).encode()
    if set(files) != set(FILES):
        raise RuntimeError(f"generator and FILES disagree: {sorted(set(files) ^ set(FILES))}")
    for rel in FILES:
        dest = CASE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(files[rel])
    for p in existing:
        if p.relative_to(CASE).as_posix() not in FILES and p.name not in GENERATED_DOCS:
            p.unlink()
    print(f"wrote {len(files)} artifact files to {CASE}")


# ---------------------------------------------------------------------------------------------- analysis
PEM_RE = re.compile(r"-----BEGIN ([A-Z0-9 ]+)-----\r?\n(.*?)-----END \1-----", re.S)
ARMOUR_RE = re.compile(r"-----BEGIN [A-Z0-9 ]+-----")


class Text:
    """A text file with exact coordinates for char offsets."""

    def __init__(self, raw):
        self.text = raw.decode("utf-8")
        self.pos = markers.positions(self.text)
        self.lines = self.text.split("\n")

    def span(self, s, e):
        l1, c1, b1 = self.pos(s)
        l2, c2, b2 = self.pos(e)
        return dict(start=OrderedDict(line=l1, column=c1, charOffset=s, byteOffset=b1),
                    end=OrderedDict(line=l2, column=c2, charOffset=e, byteOffset=b2),
                    length=OrderedDict(chars=e - s, bytes=b2 - b1))


def bspan(off, end):
    return dict(start=OrderedDict(line=None, column=None, charOffset=None, byteOffset=off),
                end=OrderedDict(line=None, column=None, charOffset=None, byteOffset=end),
                length=OrderedDict(chars=None, bytes=end - off))


class Analysis:
    def __init__(self):
        self.occs = []
        self.asset_occ = OrderedDict()           # asset id -> [(occ id, relation)]
        self.cert_der = {}                       # cert id -> DER (all copies must be identical)
        self.cert_obj = {}
        self.spki = {}                           # key id -> SPKI DER
        self.private_seen = set()
        self.material = OrderedDict()            # material id -> props
        self.protocol = None
        self.checks = []                         # verification log
        self.covered = {}                        # text file -> list of (s, e) char spans
        self.texts = {}
        self.file_info = OrderedDict()
        self.env = {}

    # -- bookkeeping ------------------------------------------------------------------------------
    def touch(self, aid, oid=None, rel=None):
        lst = self.asset_occ.setdefault(aid, [])
        if oid:
            lst.append((oid, rel))

    def add(self, asset, file, scope, role, span, *, parent=None, symbol=None, note=None, nesting=0, container=None,
            evidence="", encoding=None, encrypted=False):
        oid = f"{ID_PREFIX}-{len(self.occs) + 1:03d}"
        kind, _, qual = role.partition(":")
        o = OrderedDict(id=oid, file=file, scenario=FILES[file]["scn"], scope=scope, role=role, kind=kind,
                        qualifier=qual or None, asset=asset, parent=parent, produces=[], symbol=symbol, library=None,
                        note=note, start=span["start"], end=span["end"], length=span["length"], nesting=nesting,
                        evidence=evidence, fileLevel=True, container=container, encoding=encoding,
                        encrypted=encrypted)
        self.occs.append(o)
        self.touch(asset, oid, "direct")
        if parent:
            self.touch(parent, oid, f"parameter:{asset}")
        if span["start"]["charOffset"] is not None and nesting == 0:
            self.covered.setdefault(file, []).append((span["start"]["charOffset"], span["end"]["charOffset"]))
        return oid

    def check(self, ok, what):
        if not ok:
            raise AssertionError(f"artifact check failed: {what}")
        self.checks.append(what)

    # -- identities -------------------------------------------------------------------------------
    def cert_id(self, cert):
        cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        cid = next((k for k, c in CERTS.items() if c["name"] == cn), None)
        if cid is None:
            raise AssertionError(f"certificate {cn!r} is not in the registry")
        der = cert.public_bytes(serialization.Encoding.DER)
        if cid in self.cert_der:
            self.check(self.cert_der[cid] == der, f"{cid}: every copy is byte-identical")
            return cid
        c = CERTS[cid]
        self.cert_der[cid] = der
        self.cert_obj[cid] = cert
        self.check(cert.subject == x509_name(c["dn"]) and cert.issuer == x509_name(CERTS[c["issuer"]]["dn"]),
                   f"{cid}: subject and issuer DNs")
        self.check(cert.serial_number == c["serial"], f"{cid}: serial {c['serial']:#x}")
        self.check(cert.not_valid_before_utc == c["nb"] and cert.not_valid_after_utc == c["na"], f"{cid}: validity")
        sig = SIG_ALG.get(cert.signature_algorithm_oid.dotted_string)
        self.check(sig == c["sig"], f"{cid}: signature algorithm {c['sig']}")
        self.bind_key(c["key"], cert.public_key(), f"{cid} subjectPublicKeyInfo")
        return cid

    def bind_key(self, kid, pub, where):
        der = spki_der(pub)
        self.check(key_alg_id(pub) == KEYS[kid]["alg"], f"{where}: key algorithm {KEYS[kid]['alg']}")
        if kid in self.spki:
            self.check(self.spki[kid] == der, f"{where}: same public key as elsewhere for key {kid}")
        else:
            self.spki[kid] = der

    def verify_chain(self):
        for cid, cert in self.cert_obj.items():
            issuer = self.cert_obj[CERTS[cid]["issuer"]]
            pub = issuer.public_key()
            if CERTS[cid]["sig"] == "sha1-with-rsa":
                pub.verify(cert.signature, cert.tbs_certificate_bytes, padding.PKCS1v15(), hashes.SHA1())
            elif isinstance(pub, rsa.RSAPublicKey):
                pub.verify(cert.signature, cert.tbs_certificate_bytes, padding.PKCS1v15(),
                           cert.signature_hash_algorithm)
            elif isinstance(pub, ec.EllipticCurvePublicKey):
                pub.verify(cert.signature, cert.tbs_certificate_bytes, ec.ECDSA(cert.signature_hash_algorithm))
            else:
                pub.verify(cert.signature, cert.tbs_certificate_bytes)
            self.check(True, f"{cid}: signature verifies under {CERTS[cid]['issuer']}")

    # -- objects ---------------------------------------------------------------------------------
    def x509_cert(self, cert, file, scope, span, *, symbol, note, encoding, encrypted=False, evidence=""):
        cid = self.cert_id(cert)
        c = self.add(cid, file, scope, "obj:x509", span, symbol=symbol, note=note, encoding=encoding,
                     encrypted=encrypted, evidence=evidence)
        self.signature(cert.signature_algorithm_oid.dotted_string, file, scope, span, c, encoding, encrypted)
        kid = CERTS[cid]["key"]
        alg = KEYS[kid]["alg"]
        pq = "pqc-oid" if alg in ("ml-dsa-65", "ml-kem-768") else None
        self.add(alg, file, f"{scope} > subjectPublicKeyInfo", "alg:subjectPublicKeyInfo", span,
                 symbol=key_alg_oid(alg), note=pq, nesting=1, container=c, encoding=encoding, encrypted=encrypted,
                 evidence=f"subjectPublicKeyInfo.algorithm {key_alg_oid(alg)}")
        self.add(f"m.{kid}-public-key", file, f"{scope} > subjectPublicKeyInfo", "obj:spki", span,
                 symbol="subjectPublicKeyInfo", note=pq, nesting=1, container=c, encoding=encoding,
                 encrypted=encrypted, evidence="subjectPublicKeyInfo.subjectPublicKey")
        return cid

    def signature(self, oid, file, scope, span, container, encoding, encrypted=False, field="signatureAlgorithm"):
        sig = SIG_ALG[oid]
        note = "pqc-oid" if sig == "ml-dsa-65" else None
        self.add(sig, file, f"{scope} > {field}", f"alg:{field}", span, symbol=oid, note=note, nesting=1,
                 container=container, encoding=encoding, encrypted=encrypted, evidence=f"{field} {oid}")
        if sig in SIG_HASH:
            self.add(SIG_HASH[sig], file, f"{scope} > {field}", f"alg:{field}", span, parent=sig, symbol=oid,
                     note="nested-hash", nesting=2, container=container, encoding=encoding, encrypted=encrypted,
                     evidence=f"{field} {oid}")

    def private_key(self, key, kid, file, scope, span, *, form, symbol, note, encoding, public_stored, alg_symbol,
                    encrypted=False, evidence=""):
        self.check(KEYS[kid]["private"], f"{kid}: private key expected in the case")
        self.bind_key(kid, key.public_key(), f"{file} {scope}")
        self.private_seen.add(kid)
        p = self.add(f"m.{kid}-private-key", file, scope, f"obj:{form}", span, symbol=symbol, note=note,
                     encoding=encoding, encrypted=encrypted, evidence=evidence)
        alg = KEYS[kid]["alg"]
        self.add(alg, file, f"{scope} > algorithm", "alg:privateKeyAlgorithm", span, symbol=alg_symbol,
                 note="pqc-oid" if alg in ("ml-dsa-65", "ml-kem-768") else None, nesting=1, container=p,
                 encoding=encoding, encrypted=encrypted, evidence=f"key algorithm {alg_symbol}")
        if public_stored:
            self.add(f"m.{kid}-public-key", file, f"{scope} > public key", "obj:public-key", span,
                     symbol="publicKey", nesting=1, container=p, encoding=encoding, encrypted=encrypted,
                     evidence="public key stored with the private key")
        return p

    def pbes2(self, info, file, scope, data_span_fn, container, encoding, base=1):
        note = "pkcs12" if encoding == "PKCS#12" else "pkcs8-encrypted"
        kdf = self.add("pbkdf2-hmac-sha256", file, f"{scope} > PBES2 keyDerivationFunc", "alg:pbes2.kdf",
                       data_span_fn(info["kdf_offset"]), symbol=info["kdf"], note=note, nesting=base,
                       container=container, encoding=encoding, evidence=f"PBKDF2, {info['iterations']} iterations")
        prf_span = data_span_fn(info["prf_offset"] if info["prf_offset"] is not None else info["kdf_offset"])
        self.add("hmac-sha256", file, f"{scope} > PBKDF2 prf", "alg:pbkdf2.prf", prf_span, parent="pbkdf2-hmac-sha256",
                 symbol=info["prf"], nesting=base + 1, container=container, encoding=encoding,
                 evidence="prf hmacWithSHA256")
        self.add("sha-256", file, f"{scope} > PBKDF2 prf", "alg:pbkdf2.prf", prf_span, parent="hmac-sha256",
                 symbol=info["prf"], note="nested-hash", nesting=base + 2, container=container, encoding=encoding,
                 evidence="prf hmacWithSHA256")
        self.add("aes-256-cbc", file, f"{scope} > PBES2 encryptionScheme", "alg:pbes2.enc",
                 data_span_fn(info["enc_offset"]), symbol=info["enc"], note=note, nesting=base, container=container,
                 encoding=encoding, evidence="encryptionScheme aes256-CBC")
        self.check(info["kdf"] == OID["PBKDF2"] and info["prf"] == OID["hmacWithSHA256"] and
                   info["enc"] == OID["aes256-CBC"], f"{file} {scope}: PBES2 with PBKDF2-HMAC-SHA256 and AES-256-CBC")
        return kdf

    # -- file parsers -----------------------------------------------------------------------------
    def parse_pem_file(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        blocks = list(PEM_RE.finditer(t.text))
        meta = FILES[rel]
        multi = len(blocks) > 1
        for n, m in enumerate(blocks, 1):
            label = m.group(1)
            der = base64.b64decode("".join(m.group(2).split())) if label != "OPENSSH PRIVATE KEY" else None
            span = t.span(m.start(), m.end())
            scope = f"PEM block {n} ({label})"
            # no armour (five dashes) in evidence: the README is scanned by secret scanners, whose private-key rule
            # would join one cell's BEGIN line to a later cell's END line
            evidence = f"PEM {label} block, lines {span['start']['line']}-{span['end']['line']}"
            pre = t.text[:m.start()].rstrip("\n").split("\n")[-1] if m.start() else ""
            note = "pem-bundle" if multi else None
            if pre.startswith("issuer="):
                note = "pem-preamble"
            if label == "CERTIFICATE":
                cert = x509.load_der_x509_certificate(der)
                self.x509_cert(cert, rel, scope, span, symbol=label, note=note, encoding="PEM", evidence=evidence)
            elif label == "CERTIFICATE REQUEST":
                self.csr(x509.load_der_x509_csr(der), rel, scope, span, evidence)
            elif label == "X509 CRL":
                self.crl(x509.load_der_x509_crl(der), rel, scope, span, evidence)
            elif label == "RSA PRIVATE KEY":
                key = serialization.load_der_private_key(der, None)
                self.private_key(key, meta["key"], rel, scope, span, form="pkcs1", symbol=label, note="pkcs1",
                                 encoding="PEM", public_stored=True, alg_symbol="RSA PRIVATE KEY", evidence=evidence)
            elif label == "EC PRIVATE KEY":
                key = serialization.load_der_private_key(der, None)
                curve_oid = OID["secp384r1"] if key.curve.name == "secp384r1" else OID["prime256v1"]
                self.private_key(key, meta["key"], rel, scope, span, form="sec1", symbol=label, note="sec1",
                                 encoding="PEM", public_stored=self.sec1_has_public(der), alg_symbol=curve_oid,
                                 evidence=evidence)
            elif label == "PRIVATE KEY":
                key = serialization.load_der_private_key(der, None)
                alg_oid, stores_pub = self.pkcs8_info(der)
                seed = isinstance(key, (mldsa.MLDSA65PrivateKey, mlkem.MLKEM768PrivateKey))
                self.private_key(key, meta["key"], rel, scope, span, form="pkcs8", symbol=label,
                                 note="pkcs8-seed" if seed else "pkcs8", encoding="PEM", public_stored=stores_pub,
                                 alg_symbol=alg_oid, evidence=evidence)
                self.check(not seed or not stores_pub, f"{rel}: seed-form PKCS#8 stores no public key")
            elif label == "ENCRYPTED PRIVATE KEY":
                passphrase = self.env["BACKUP_KEY_PASSPHRASE"][0]
                key = serialization.load_der_private_key(der, passphrase.encode())
                self.check(True, f"{rel}: decrypts with BACKUP_KEY_PASSPHRASE from secrets/app.env")
                _, cs, ce = der_tlv(der, 0)
                alg, data = der_children(der, cs, ce)
                info = pbes2_params(der, alg[0])
                inner = pbes2_decrypt(info, der[data[2]:data[3]], passphrase)
                alg_oid, stores_pub = self.pkcs8_info(inner)
                p = self.private_key(key, meta["key"], rel, scope, span, form="pkcs8-encrypted", symbol=label,
                                     note="pkcs8-encrypted", encoding="PEM", public_stored=stores_pub,
                                     alg_symbol=alg_oid, encrypted=True, evidence=evidence)
                self.pbes2(info, rel, scope, lambda off: span, p, "PEM")
                self.check(info["iterations"] == 2048, f"{rel}: PBKDF2 iteration count recorded ({info['iterations']})")
                self.material_extra[f"m.{meta['key']}-private-key"] = dict(securedBy=dict(
                    mechanism=f"PBES2 (PBKDF2-HMAC-SHA256, {info['iterations']} iterations; AES-256-CBC)",
                    algorithmRef="aes-256-cbc"))
            elif label == "PUBLIC KEY":
                pub = serialization.load_der_public_key(der)
                kid = meta["key"]
                self.bind_key(kid, pub, f"{rel} {scope}")
                p = self.add(f"m.{kid}-public-key", rel, scope, "obj:spki", span, symbol=label, note="spki",
                             encoding="PEM", evidence=evidence)
                alg = KEYS[kid]["alg"]
                self.add(alg, rel, f"{scope} > algorithm", "alg:subjectPublicKeyInfo", span, symbol=key_alg_oid(alg),
                         nesting=1, container=p, encoding="PEM", evidence=f"subjectPublicKeyInfo.algorithm {key_alg_oid(alg)}")
            elif label == "OPENSSH PRIVATE KEY":
                key = serialization.load_ssh_private_key(t.text[m.start():m.end()].encode() + b"\n", None)
                self.private_key(key, meta["key"], rel, scope, span, form="openssh", symbol=label, note="openssh",
                                 encoding="PEM", public_stored=True, alg_symbol="ssh-ed25519", evidence=evidence)
            else:
                raise AssertionError(f"{rel}: unexpected PEM label {label}")

    @staticmethod
    def sec1_has_public(der):
        _, cs, ce = der_tlv(der, 0)
        return any(tag == 0xA1 for _, tag, _, _ in der_children(der, cs, ce))

    @staticmethod
    def pkcs8_info(der):
        """Algorithm OID of a PKCS#8 PrivateKeyInfo and whether the public key is stored with it."""
        _, cs, ce = der_tlv(der, 0)
        kids = der_children(der, cs, ce)
        alg_oid, _ = algid(der, kids[1][0])
        if any(tag == 0x81 or tag == 0xA1 for _, tag, _, _ in kids[3:]):
            return alg_oid, True
        if alg_oid == OID["rsaEncryption"]:
            return alg_oid, True                     # RSAPrivateKey carries n and e
        if alg_oid == OID["id-ecPublicKey"]:
            inner = der[kids[2][2]:kids[2][3]]
            return alg_oid, Analysis.sec1_has_public(inner)
        return alg_oid, False

    def csr(self, csr, rel, scope, span, evidence):
        self.check(csr.is_signature_valid, f"{rel}: CSR self-signature verifies")
        self.check(csr.subject == x509_name(CERTS[CSR_SPEC["subject"]]["dn"]), f"{rel}: CSR subject")
        kid = CSR_SPEC["key"]
        self.bind_key(kid, csr.public_key(), f"{rel} CSR")
        p = self.add("m.server-csr", rel, scope, "obj:pkcs10", span, symbol="CERTIFICATE REQUEST", note="csr",
                     encoding="PEM", evidence=evidence)
        self.signature(csr.signature_algorithm_oid.dotted_string, rel, scope, span, p, "PEM")
        alg = KEYS[kid]["alg"]
        self.add(alg, rel, f"{scope} > subjectPublicKeyInfo", "alg:subjectPublicKeyInfo", span, symbol=key_alg_oid(alg),
                 nesting=1, container=p, encoding="PEM", evidence=f"subjectPublicKeyInfo.algorithm {key_alg_oid(alg)}")
        self.add(f"m.{kid}-public-key", rel, f"{scope} > subjectPublicKeyInfo", "obj:spki", span,
                 symbol="subjectPublicKeyInfo", nesting=1, container=p, encoding="PEM",
                 evidence="subjectPublicKeyInfo.subjectPublicKey")
        self.material_extra["m.server-csr"] = dict(subject=csr.subject.rfc4514_string(),
                                                   sha256=hashlib.sha256(csr.public_bytes(serialization.Encoding.DER)).hexdigest())

    def crl(self, crl, rel, scope, span, evidence):
        issuer = self.cert_obj.get(CRL_SPEC["issuer"])
        self.check(issuer is not None and crl.is_signature_valid(issuer.public_key()), f"{rel}: CRL signature verifies")
        self.check(crl.last_update_utc == CRL_SPEC["this_update"] and crl.next_update_utc == CRL_SPEC["next_update"],
                   f"{rel}: thisUpdate / nextUpdate")
        self.check(sorted(r.serial_number for r in crl) == sorted(s for s, _ in CRL_SPEC["revoked"]),
                   f"{rel}: revoked serials")
        p = self.add("m.issuing-ca-crl", rel, scope, "obj:crl", span, symbol="X509 CRL", note="crl", encoding="PEM",
                     evidence=evidence)
        self.signature(crl.signature_algorithm_oid.dotted_string, rel, scope, span, p, "PEM")
        self.material_extra["m.issuing-ca-crl"] = dict(
            issuer=crl.issuer.rfc4514_string(), thisUpdate=rfc3339(crl.last_update_utc),
            nextUpdate=rfc3339(crl.next_update_utc), revoked=[f"{r.serial_number:#x}" for r in crl],
            sha256=hashlib.sha256(crl.public_bytes(serialization.Encoding.DER)).hexdigest())

    def parse_der_cert(self, rel, raw):
        cert = x509.load_der_x509_certificate(raw)
        self.x509_cert(cert, rel, "DER file", bspan(0, len(raw)), symbol="Certificate", note="der", encoding="DER",
                       evidence=f"<DER certificate, {len(raw)} bytes>")

    def parse_pkcs7(self, rel, raw):
        certs = pkcs7.load_der_pkcs7_certificates(raw)
        for n, cert in enumerate(certs, 1):
            der = cert.public_bytes(serialization.Encoding.DER)
            off = raw.find(der)
            self.check(off >= 0, f"{rel}: certificate {n} stored in clear")
            self.x509_cert(cert, rel, f"PKCS#7 certificate {n}", bspan(off, off + len(der)), symbol="certificates",
                           note="pkcs7", encoding="PKCS#7 DER",
                           evidence=f"<certificate {n} of {len(certs)}, bytes {off}-{off + len(der)}>")

    def parse_pkcs12(self, rel, raw):
        key, cert, extra = pkcs12.load_key_and_certificates(raw, KEYSTORE_PASSWORD.encode())
        self.check(True, f"{rel}: opens with password {KEYSTORE_PASSWORD}")
        _, cs, ce = der_tlv(raw, 0)
        version, auth_safe, mac_data = der_children(raw, cs, ce)
        # AuthenticatedSafe: ContentInfo(data) -> [0] -> OCTET STRING -> SEQUENCE OF ContentInfo
        ai = der_children(raw, auth_safe[2], auth_safe[3])
        self.check(oid_str(raw[ai[0][2]:ai[0][3]]) == OID["data"], f"{rel}: authSafe is data")
        octet = der_children(raw, ai[1][2], ai[1][3])[0]
        safes_seq = der_children(raw, octet[2], octet[3])[0]
        cert_blob, key_info = None, None
        for ci in der_children(raw, safes_seq[2], safes_seq[3]):
            kids = der_children(raw, ci[2], ci[3])
            ctype = oid_str(raw[kids[0][2]:kids[0][3]])
            content = der_children(raw, kids[1][2], kids[1][3])[0]
            if ctype == OID["encryptedData"]:
                eci = der_children(raw, content[2], content[3])[1]           # EncryptedContentInfo
                e_kids = der_children(raw, eci[2], eci[3])
                cert_blob = dict(pbes2=pbes2_params(raw, e_kids[1][0]), blob=(e_kids[2][0], e_kids[2][3]),
                                 content=(e_kids[2][2], e_kids[2][3]))
            elif ctype == OID["data"]:
                for bag in der_children(raw, *der_children(raw, content[2], content[3])[0][2:4]):
                    b_kids = der_children(raw, bag[2], bag[3])
                    if oid_str(raw[b_kids[0][2]:b_kids[0][3]]) == OID["pkcs8ShroudedKeyBag"]:
                        epki = der_children(raw, b_kids[1][2], b_kids[1][3])[0]
                        ep = der_children(raw, epki[2], epki[3])
                        key_info = dict(pbes2=pbes2_params(raw, ep[0][0]), blob=(ep[1][0], ep[1][3]))
        self.check(cert_blob is not None and key_info is not None, f"{rel}: one encrypted certificate safe and one "
                                                                    f"shrouded key bag")
        span_of = lambda off: bspan(off, der_tlv(raw, off)[2])  # noqa: E731
        # integrity MAC
        mac_kids = der_children(raw, mac_data[2], mac_data[3])
        digest_info = der_children(raw, mac_kids[0][2], mac_kids[0][3])
        mac_alg_off = digest_info[0][0]
        mac_oid, _ = algid(raw, mac_alg_off)
        iterations = der_int(raw, mac_kids[2][2], mac_kids[2][3]) if len(mac_kids) > 2 else 1
        self.check(mac_oid == OID["sha256"], f"{rel}: MacData digest SHA-256")
        mac = self.add("hmac-sha256", rel, "PKCS#12 MacData", "alg:mac", span_of(mac_data[0]), symbol=mac_oid,
                       note="pkcs12", encoding="PKCS#12",
                       evidence=f"MacData: HMAC with SHA-256, PKCS#12 KDF, {iterations} iterations")
        self.add("sha-256", rel, "PKCS#12 MacData > digestAlgorithm", "alg:mac", span_of(mac_alg_off),
                 parent="hmac-sha256", symbol=mac_oid, note="nested-hash", nesting=1, container=mac,
                 encoding="PKCS#12", evidence="digestAlgorithm sha256")
        # encrypted certificate safe: its PBES2 parameters are in clear, the certificates are not
        blob = bspan(*cert_blob["blob"])
        plain = pbes2_decrypt(cert_blob["pbes2"], raw[slice(*cert_blob["content"])], KEYSTORE_PASSWORD)
        self.check(all(c.public_bytes(serialization.Encoding.DER) in plain for c in [cert] + list(extra)),
                   f"{rel}: both certificates are inside the encrypted safe")
        self.pbes2(cert_blob["pbes2"], rel, "PKCS#12 encryptedData safe", span_of, None, "PKCS#12", base=0)
        for n, c in enumerate([cert] + list(extra), 1):
            self.x509_cert(c, rel, f"PKCS#12 encryptedData safe > certBag {n}", blob, symbol="certBag", note="pkcs12",
                           encoding="PKCS#12", encrypted=True, evidence=f"<encrypted certBag {n}>")
        # shrouded key bag
        kblob = bspan(*key_info["blob"])
        kid = FILES_P12_KEY
        _, ccs, cce = der_tlv(raw, key_info["blob"][0])
        inner = pbes2_decrypt(key_info["pbes2"], raw[ccs:cce], KEYSTORE_PASSWORD)
        alg_oid, stores_pub = self.pkcs8_info(inner)
        self.check(serialization.load_der_private_key(inner, None).private_numbers() == key.private_numbers(),
                   f"{rel}: the shrouded key bag decrypts to the client key")
        p = self.private_key(key, kid, rel, "PKCS#12 pkcs8ShroudedKeyBag", kblob, form="pkcs8-shrouded",
                             symbol="pkcs8ShroudedKeyBag", note="pkcs12", encoding="PKCS#12", public_stored=stores_pub,
                             alg_symbol=alg_oid, encrypted=True, evidence="<encrypted PKCS#8 key bag>")
        self.pbes2(key_info["pbes2"], rel, "PKCS#12 pkcs8ShroudedKeyBag", span_of, p, "PKCS#12")
        self.material_extra[f"m.{kid}-private-key"] = dict(securedBy=dict(
            mechanism=f"PKCS#12 shrouded key bag, PBES2 (PBKDF2-HMAC-SHA256, {key_info['pbes2']['iterations']} "
                      f"iterations; AES-256-CBC)", algorithmRef="aes-256-cbc"))
        self.p12_info = dict(mac_iterations=iterations, cert_iterations=cert_blob["pbes2"]["iterations"],
                             key_iterations=key_info["pbes2"]["iterations"])

    def parse_jks(self, rel, raw):
        magic, version, count = struct.unpack(">III", raw[:12])
        self.check(magic == 0xFEEDFEED and version == 2, f"{rel}: JKS version 2")
        body, digest = raw[:-20], raw[-20:]
        self.check(hashlib.sha1(KEYSTORE_PASSWORD.encode("utf-16-be") + b"Mighty Aphrodite" + body).digest() == digest,
                   f"{rel}: keystore digest verifies with password {KEYSTORE_PASSWORD}")
        i = 12
        aliases = []
        for _ in range(count):
            tag = struct.unpack(">I", raw[i:i + 4])[0]
            self.check(tag == 2, f"{rel}: trusted certificate entry")
            i += 4
            n = struct.unpack(">H", raw[i:i + 2])[0]
            alias = raw[i + 2:i + 2 + n].decode()
            i += 2 + n + 8
            n = struct.unpack(">H", raw[i:i + 2])[0]
            i += 2 + n
            ln = struct.unpack(">I", raw[i:i + 4])[0]
            i += 4
            cert = x509.load_der_x509_certificate(raw[i:i + ln])
            self.x509_cert(cert, rel, f"JKS trustedCertEntry '{alias}'", bspan(i, i + ln), symbol=alias, note="jks",
                           encoding="JKS", evidence=f"<trustedCertEntry '{alias}', bytes {i}-{i + ln}>")
            aliases.append(alias)
            i += ln
        self.check(i == len(body), f"{rel}: entries end where the digest starts")
        self.add("sha-1", rel, "JKS keystore digest", "alg:integrity", bspan(len(body), len(raw)),
                 symbol="SHA-1(password || 'Mighty Aphrodite' || entries)", note="jks", encoding="JKS",
                 evidence="<20-byte SHA-1 keystore digest>")
        self.jks_aliases = aliases

    def parse_openssh_pub(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        line = t.text.rstrip("\n")
        typ, blob, *comment = line.split(" ")
        pub = serialization.load_ssh_public_key(f"{typ} {blob}".encode())
        kid = FILES[rel]["key"]
        self.bind_key(kid, pub, rel)
        p = self.add(f"m.{kid}-public-key", rel, "OpenSSH public key line", "obj:openssh-pub", t.span(0, len(line)),
                     symbol=typ, note="openssh-pub", encoding="OpenSSH", evidence=f"{typ} AAAA… {' '.join(comment)}")
        self.add(KEYS[kid]["alg"], rel, "OpenSSH public key line > key type", "alg:key-type", t.span(0, len(typ)),
                 symbol=typ, nesting=1, container=p, encoding="OpenSSH", evidence=typ)

    def parse_env(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        for m in re.finditer(r"^([A-Z_]+)=(.*)$", t.text, re.M):
            self.env[m.group(1)] = (m.group(2), m.start(2), m.end(2))

    def record_env(self, rel):
        t = self.texts[rel]
        env = self.env

        def mat(var, asset, note, redact=True):
            val, s, e = env[var]
            shown = f"{var}=<{len(val)} characters>" if redact else f"{var}={val}"
            self.add(asset, rel, var, f"mat:{var}", t.span(s, e), symbol=var, note=note, encoding="dotenv",
                     evidence=shown)
            return val
        val, s, e = env["JWT_ALGORITHM"]
        self.check(val == "HS256", f"{rel}: JWT_ALGORITHM=HS256")
        self.add("hmac-sha256", rel, "JWT_ALGORITHM", "cfg:JWT_ALGORITHM", t.span(s, e), symbol="HS256", note="jwt",
                 encoding="dotenv", evidence="JWT_ALGORITHM=HS256")
        self.add("sha-256", rel, "JWT_ALGORITHM", "cfg:JWT_ALGORITHM", t.span(s, e), parent="hmac-sha256",
                 symbol="HS256", note="nested-hash", nesting=1, encoding="dotenv", evidence="JWT_ALGORITHM=HS256")
        key_b64 = mat("JWT_SIGNING_KEY", "m.jwt-signing-key", "env-secret")
        token = mat("SERVICE_TOKEN", "m.service-token", "jwt")
        header, body, sig = token.split(".")
        _, ts, _ = env["SERVICE_TOKEN"]
        hdr = json.loads(b64url_dec(header))
        self.check(hdr == {"alg": "HS256", "typ": "JWT"}, f"{rel}: JWT header names HS256")
        self.check(hmac.compare_digest(b64url_dec(sig), hmac.new(b64url_dec(key_b64), f"{header}.{body}".encode(),
                                                                 hashlib.sha256).digest()),
                   f"{rel}: SERVICE_TOKEN verifies with JWT_SIGNING_KEY (HS256)")
        self.check(json.loads(b64url_dec(body)) == JWT_PAYLOAD, f"{rel}: JWT claims")
        self.add("hmac-sha256", rel, "SERVICE_TOKEN > JOSE header", "alg:jwt.alg", t.span(ts, ts + len(header)),
                 symbol="HS256", note="jwt", nesting=1, encoding="base64url", evidence="JOSE header {\"alg\":\"HS256\",…}")
        pw = mat("KEYSTORE_PASSWORD", "m.keystore-password", "low-entropy-secret")
        self.check(pw == KEYSTORE_PASSWORD, f"{rel}: KEYSTORE_PASSWORD opens both keystores")
        mat("BACKUP_KEY_PASSPHRASE", "m.backup-passphrase", "env-secret")
        self.secret_values.update({"m.jwt-signing-key": key_b64, "m.service-token": token,
                                   "m.keystore-password": pw, "m.backup-passphrase": env["BACKUP_KEY_PASSPHRASE"][0]})

    def parse_terraform(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        m = re.search(r'^\s*password\s*=\s*"([^"]+)"', t.text, re.M)
        self.check(m is not None, f"{rel}: password attribute")
        self.add("m.db-password", rel, 'resource "aws_db_instance" "reporting" > password', "mat:password",
                 t.span(m.start(1), m.end(1)), symbol="aws_db_instance.reporting.password", note="tf-secret",
                 encoding="HCL", evidence=f'password = "<{len(m.group(1))} characters>"')
        self.secret_values["m.db-password"] = m.group(1)

    def parse_openssl_cnf(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        section = None
        settings = {}
        proto = "tls13-openssl"
        for m in re.finditer(r"^(?:\[\s*([^\]]+?)\s*\]|([A-Za-z_]+)\s*=\s*(.*?))\s*$", t.text, re.M):
            if m.group(1):
                section = m.group(1)
                continue
            key, val = m.group(2), m.group(3)
            settings[(section, key)] = val
            s, e = m.start(3), m.end(3)
            scope = f"[{section}] {key}" if section else key
            if section != "system_default_sect":
                continue
            if key in ("MinProtocol", "MaxProtocol"):
                self.check(val == "TLSv1.3", f"{rel}: {key} = TLSv1.3")
                self.add(proto, rel, scope, f"cfg:{key}", t.span(s, e), symbol=key, note="openssl-cnf",
                         encoding="text", evidence=f"{key} = {val}")
            elif key == "Ciphersuites":
                p = self.add(proto, rel, scope, "cfg:Ciphersuites", t.span(s, e), symbol=key, note="openssl-cnf",
                             encoding="text", evidence=f"{key} = {val}")
                pos = s
                for suite in val.split(":"):
                    ss = t.text.index(suite, pos)
                    pos = ss + len(suite)
                    for alg in CIPHER_SUITES[suite][1]:
                        self.add(alg, rel, f"{scope} > {suite}", "alg:cipher-suite", t.span(ss, pos), parent=proto,
                                 symbol=suite, note="suite-name", nesting=1, container=p, encoding="text",
                                 evidence=suite)
                self.suites = val.split(":")
            elif key == "Groups":
                p = self.add(proto, rel, scope, "cfg:Groups", t.span(s, e), symbol=key, note="openssl-cnf",
                             encoding="text", evidence=f"{key} = {val}")
                pos = s
                for group in val.split(":"):
                    gs = t.text.index(group, pos)
                    pos = gs + len(group)
                    aid, parts = TLS_GROUPS[group]
                    self.add(aid, rel, f"{scope} > {group}", "alg:group", t.span(gs, pos), parent=proto, symbol=group,
                             note="hybrid-group" if parts else None, nesting=1, container=p, encoding="text",
                             evidence=group)
                    for part in parts:
                        self.add(part, rel, f"{scope} > {group}", "alg:group", t.span(gs, pos), parent=aid,
                                 symbol=group, note="hybrid-group", nesting=2, container=p, encoding="text",
                                 evidence=group)
                self.groups = val.split(":")
        self.check(settings.get((None, "openssl_conf")) == "openssl_init" and
                   settings.get(("ssl_sect", "system_default")) == "system_default_sect",
                   f"{rel}: system_default_sect is reachable from openssl_conf")

    def parse_decoy(self, rel, raw):
        t = Text(raw)
        self.texts[rel] = t
        for m in PEM_RE.finditer(t.text):
            body = "".join(m.group(2).split())
            try:
                der = base64.b64decode(body, validate=True)
                ok = False
                for loader in (x509.load_der_x509_certificate, lambda d: serialization.load_der_private_key(d, None)):
                    try:
                        loader(der)
                        ok = True
                    except Exception:  # noqa: BLE001
                        pass
            except ValueError:
                ok = False
            self.check(not ok, f"{rel}: the PEM armour at offset {m.start()} does not decode to a usable object")


FILES_P12_KEY = "client"


def analyse():
    present = sorted(p.relative_to(CASE).as_posix() for p in CASE.rglob("*") if p.is_file()
                     and p.relative_to(CASE).as_posix() not in GENERATED_DOCS)
    missing = sorted(set(FILES) - set(present))
    extra = sorted(set(present) - set(FILES))
    if missing or extra:
        sys.exit(f"Artifacts/ does not match FILES (missing {missing}, unexpected {extra}); run "
                 f"'python3 artifacts.py generate' first")
    A = Analysis()
    A.material_extra = {}
    A.secret_values = {}
    raw = {rel: (CASE / rel).read_bytes() for rel in FILES}
    for rel, meta in FILES.items():
        A.file_info[rel] = OrderedDict(path=rel, scenario=meta["scn"], format=meta["fmt"], description=meta["desc"],
                                       bytes=len(raw[rel]), sha256=hashlib.sha256(raw[rel]).hexdigest())
    A.parse_env("secrets/app.env", raw["secrets/app.env"])   # passphrase needed by the encrypted key
    # certificates first so that key bindings and the CRL issuer are known
    order = sorted(FILES, key=lambda r: (FILES[r]["kind"] != "pem" or b"BEGIN CERTIFICATE" not in raw[r], 0))
    for rel in order:
        kind = FILES[rel]["kind"]
        if kind == "pem":
            A.parse_pem_file(rel, raw[rel])
        elif kind == "der-cert":
            A.parse_der_cert(rel, raw[rel])
        elif kind == "pkcs7":
            A.parse_pkcs7(rel, raw[rel])
        elif kind == "pkcs12":
            A.parse_pkcs12(rel, raw[rel])
        elif kind == "jks":
            A.parse_jks(rel, raw[rel])
        elif kind == "openssh-pub":
            A.parse_openssh_pub(rel, raw[rel])
        elif kind == "env":
            A.record_env(rel)
        elif kind == "terraform":
            A.parse_terraform(rel, raw[rel])
        elif kind == "openssl-cnf":
            A.parse_openssl_cnf(rel, raw[rel])
        elif kind == "decoy":
            A.parse_decoy(rel, raw[rel])
    A.verify_chain()
    A.check(set(A.cert_obj) == set(CERTS), "every registered certificate occurs")
    A.check(A.private_seen == {k for k, v in KEYS.items() if v["private"]}, "every stored private key occurs")
    # file order for the ledger: re-sort occurrences by file (FILES order), then by position, keep ids stable
    rank = {rel: i for i, rel in enumerate(FILES)}
    A.occs.sort(key=lambda o: (rank[o["file"]], o["start"]["byteOffset"] if o["start"]["byteOffset"] is not None else 0,
                               o["nesting"], int(o["id"].split("-")[1])))
    remap = {o["id"]: f"{ID_PREFIX}-{i:03d}" for i, o in enumerate(A.occs, 1)}
    for o in A.occs:
        o["id"] = remap[o["id"]]
        if o["container"]:
            o["container"] = remap[o["container"]]
    A.asset_occ = OrderedDict((aid, sorted(((remap[oid], rel) for oid, rel in lst), key=lambda x: x[0]))
                              for aid, lst in A.asset_occ.items())
    A.by_id = {o["id"]: o for o in A.occs}
    build_assets(A)
    A.mentions = non_asset_mentions(A)
    return A


# ---------------------------------------------------------------------------------------------- assets
def _alg_props(aid):
    d = dict(spec.ALGORITHMS[aid])
    o = ALG_OVERRIDES.get(aid, {})
    if "nistStatus" in o:
        d["nistStatus"] = o["nistStatus"]
    if "note" in o:
        d["note"] = o["note"]
    return d


def build_assets(A):
    assets = OrderedDict()
    # algorithms: every referenced one plus the dependency closure (implicit when it has no occurrence)
    algs = [aid for aid in A.asset_occ if aid in spec.ALGORITHMS]
    todo = list(algs)
    while todo:
        aid = todo.pop()
        for d in spec.ALGORITHMS[aid]["dependsOn"]:
            if d not in algs:
                algs.append(d)
                todo.append(d)
    order = {aid: i for i, aid in enumerate(spec.ALGORITHMS)}
    for aid in sorted(algs, key=lambda a: order[a]):
        props = _alg_props(aid)
        occ = A.asset_occ.get(aid, [])
        props["implicit"] = not occ
        assets[aid] = dict(id=aid, kind="algorithm", occ=occ, implicit=not occ, props=props)
    # certificates
    for cid, c in CERTS.items():
        cert = A.cert_obj[cid]
        der = A.cert_der[cid]
        exts = []
        for e in cert.extensions:
            exts.append(f"{e.oid._name}{' (critical)' if e.critical else ''}")
        props = OrderedDict(
            id=cid, name=c["name"], scenario=c["scn"], subjectName=cert.subject.rfc4514_string(),
            issuerName=cert.issuer.rfc4514_string(), notValidBefore=rfc3339(cert.not_valid_before_utc),
            notValidAfter=rfc3339(cert.not_valid_after_utc), signatureAlgorithmRef=c["sig"],
            subjectPublicKeyRef=f"m.{c['key']}-public-key", certificateFormat="X.509", version="v3",
            serial=f"{cert.serial_number:#x}", issuerRef=c["issuer"],
            fingerprintSha256=hashlib.sha256(der).hexdigest(), extensions=exts,
            files=sorted({A.by_id[o]["file"] for o, r in A.asset_occ[cid] if r == "direct"}, key=list(FILES).index))
        assets[cid] = dict(id=cid, kind="certificate", occ=A.asset_occ[cid], implicit=False, props=props)
    # protocol
    proto = "tls13-openssl"
    suites = [OrderedDict(name=s, identifiers=CIPHER_SUITES[s][0], algorithms=CIPHER_SUITES[s][1]) for s in A.suites]
    assets[proto] = dict(id=proto, kind="protocol", occ=A.asset_occ[proto], implicit=False, props=OrderedDict(
        id=proto, name="TLS 1.3 system defaults (OpenSSL configuration)", scenario="A13", type="tls", version="1.3",
        cipherSuites=suites, groups=[TLS_GROUPS[g][0] for g in A.groups],
        note="MinProtocol = MaxProtocol = TLSv1.3. Groups lists the hybrid X25519MLKEM768 first, then X25519; "
             "signature algorithms are left at the OpenSSL defaults and are not recorded."))
    # related crypto material
    mats = OrderedDict()
    for kid, k in KEYS.items():
        alg = k["alg"]
        a = spec.ALGORITHMS[alg]
        size = {"ml-dsa-65": 15616, "ml-kem-768": 9472}.get(alg) or _key_bits(alg)
        if k["private"]:
            psize = None if alg in ("ml-dsa-65", "ml-kem-768") else _key_bits(alg)
            mats[f"m.{kid}-private-key"] = dict(
                name=f"{k['holder']} private key ({a['name'].replace(' key pair', '')})", type="private-key",
                size=psize, provenance="keygen", algorithmRef=alg, scenario=KEY_SCENARIO[kid],
                note={"ml-dsa-65": "Seed form (32 bytes) in PKCS#8", "ml-kem-768": "Seed form (64 bytes) in PKCS#8"}.get(alg, ""))
        mats[f"m.{kid}-public-key"] = dict(
            name=f"{k['holder']} public key ({a['name'].replace(' key pair', '')})", type="public-key", size=size,
            provenance="keygen", algorithmRef=alg, scenario=KEY_SCENARIO[kid],
            note={"ml-dsa-65": "1952 bytes", "ml-kem-768": "Encapsulation key, 1184 bytes"}.get(alg, ""))
    mats["m.server-csr"] = dict(name="Certificate signing request for server.cbom-corpus.example", type="other",
                                size=None, provenance="keygen", algorithmRef="sha256-with-rsa", scenario="A02",
                                note="PKCS#10; CycloneDX has no material type for a CSR, so type is 'other'")
    mats["m.issuing-ca-crl"] = dict(name="CRL of the CBOMFuse Test Issuing CA", type="other", size=None,
                                    provenance="keygen", algorithmRef="ecdsa-with-sha384", scenario="A04",
                                    note="CycloneDX has no material type for a CRL, so type is 'other'")
    sv = A.secret_values
    mats["m.jwt-signing-key"] = dict(name="HS256 JWT signing key", type="secret-key",
                                     size=len(b64url_dec(sv["m.jwt-signing-key"])) * 8, provenance="csprng",
                                     algorithmRef="hmac-sha256", scenario="A11", note="base64url, 32 bytes")
    mats["m.service-token"] = dict(name="Service JWT (HS256)", type="token", size=None, provenance="derived",
                                   algorithmRef="hmac-sha256", scenario="A11",
                                   note="Signed with m.jwt-signing-key; expires 2027-01-01")
    mats["m.keystore-password"] = dict(name="Keystore password (client.p12 and truststore.jks)", type="password",
                                       size=len(sv["m.keystore-password"]) * 8, provenance="hardcoded",
                                       algorithmRef="pbkdf2-hmac-sha256", scenario="A11", value='"changeit"',
                                       note="JDK default store password")
    mats["m.backup-passphrase"] = dict(name="Passphrase of the encrypted backup key", type="password",
                                       size=len(sv["m.backup-passphrase"]) * 8, provenance="hardcoded",
                                       algorithmRef="pbkdf2-hmac-sha256", scenario="A11", note="")
    mats["m.db-password"] = dict(name="Reporting database password", type="password",
                                 size=len(sv["m.db-password"]) * 8, provenance="hardcoded", algorithmRef=None,
                                 scenario="A12", note="")
    for mid, d in mats.items():
        props = OrderedDict(id=mid, name=d["name"], type=d["type"], size=d["size"], provenance=d["provenance"],
                            algorithmRef=d["algorithmRef"], scenario=d["scenario"], value=d.get("value"),
                            note=d["note"])
        if mid in A.secret_values:
            props["valueSha256"] = hashlib.sha256(A.secret_values[mid].encode()).hexdigest()
        kid = mid[2:].rsplit("-", 2)[0] if mid.endswith("-key") and mid[2:].rsplit("-", 2)[0] in KEYS else None
        if kid and mid.endswith("public-key"):
            props["spkiSha256"] = hashlib.sha256(A.spki[kid]).hexdigest()
        if kid and mid.endswith("private-key"):
            props["publicKeySpkiSha256"] = hashlib.sha256(A.spki[kid]).hexdigest()
        props.update(A.material_extra.get(mid, {}))
        occ = A.asset_occ.get(mid, [])
        if not occ:
            raise AssertionError(f"{mid} has no occurrence")
        assets[mid] = dict(id=mid, kind="related-crypto-material", occ=occ, implicit=False, props=props)
    unknown = set(A.asset_occ) - set(assets)
    if unknown:
        raise AssertionError(f"occurrences for unregistered assets {sorted(unknown)}")
    A.assets = assets


def _key_bits(alg):
    if alg.startswith("rsa-"):
        return int(alg.split("-")[1])
    return {"ecdsa-p256": 256, "ecdsa-p384": 384, "ed25519": 256}[alg]


# ---------------------------------------------------------------------------------------------- mentions
def non_asset_mentions(A):
    out = []
    for rel, t in A.texts.items():
        covered = bytearray(len(t.text) + 1)
        for s, e in A.covered.get(rel, []):
            covered[s:e] = b"\x01" * (e - s)
        md = rel.endswith(".md")

        def ctx(off):
            line = t.lines[t.pos(off)[0] - 1]
            stripped = line.strip()
            if md:
                return "documentation", "Prose in a Markdown document; documentation only"
            if stripped.startswith("#"):
                return "comment", "Comment text; documentation only"
            if stripped.startswith(("subject=", "issuer=")):
                return "pem-preamble", "Subject/issuer label printed before a PEM block; descriptive text only"
            return "config-value", "Configuration value (a file path or label) that names an algorithm but is not a crypto asset"
        for m in ARMOUR_RE.finditer(t.text):
            if any(covered[m.start():m.end()]):
                continue
            # record the label without its dashes ("BEGIN PRIVATE KEY"): the ledger and README must not contain PEM
            # armour themselves, or secret scanners would report them
            s, e = m.start() + 5, m.end() - 5
            l1, c1, b1 = t.pos(s)
            out.append(OrderedDict(id=None, file=rel, line=l1, column=c1, charOffset=s, byteOffset=b1,
                                   length=e - s, text=t.text[s:e], context="pem-armour",
                                   token=t.lines[l1 - 1].strip().strip("-"),
                                   reason="PEM armour around a body that does not decode (placeholder or shortened "
                                          "example); not a cryptographic object"))
            covered[m.start():m.end()] = b"\x01" * (m.end() - m.start())
        for m in re.finditer(spec.DECOY_PATTERN, t.text):
            if any(covered[m.start():m.end()]):
                continue
            l1, c1, b1 = t.pos(m.start())
            context, why = ctx(m.start())
            out.append(OrderedDict(id=None, file=rel, line=l1, column=c1, charOffset=m.start(), byteOffset=b1,
                                   length=len(m.group(0)), text=m.group(0), context=context,
                                   token=t.lines[l1 - 1].strip(), reason=why))
    rank = {rel: i for i, rel in enumerate(FILES)}
    out.sort(key=lambda d: (rank[d["file"]], d["charOffset"]))
    for i, d in enumerate(out, 1):
        d["id"] = f"{ID_PREFIX}-N{i:03d}"
    return out


# ---------------------------------------------------------------------------------------------- outputs
def bom_ref(aid):
    if aid in spec.ALGORITHMS:
        return f"crypto/algorithm/{aid}"
    if aid.startswith("m."):
        return f"crypto/related-crypto-material/{aid[2:]}"
    if aid.startswith("cert."):
        return f"crypto/certificate/{aid[5:]}"
    return f"crypto/protocol/{aid}"


KIND_ORDER = {"algorithm": 0, "certificate": 1, "protocol": 2, "related-crypto-material": 3}


def ground_truth(A):
    return OrderedDict([
        ("corpus", "cbom-ground-truth"), ("language", "Artifacts"), ("file", None), ("generated", GEN_TIME),
        ("conventions", OrderedDict(
            line="1-based (text files only)", column="1-based Unicode code points (text files only)", end="exclusive",
            charOffset="0-based code-point offset from file start (text files only; null for binary files)",
            byteOffset="0-based byte offset from file start", cyclonedxOffset="column - 1",
            fileLevel="true on every occurrence of this case: the evidence is an artifact file, so a tool location "
                      "that names the file (with or without a line) points at it",
            nesting="0 = object or setting, 1+ = field inside it; container = id of the enclosing occurrence",
            encrypted="true when the object is stored encrypted (readable only with the documented password)")),
        ("verification", OrderedDict(
            generator="_tooling/artifacts.py", parser=f"cryptography {CRYPTOGRAPHY_VERSION} "
                                                      f"({_openssl_backend.backend.openssl_version_text()})",
            checks=len(A.checks), result="every check passed",
            details=A.checks)),
        ("scenarios", [OrderedDict(id=s, family=f, description=d) for s, f, d in SCENARIOS]),
        ("files", list(A.file_info.values())),
        ("libraries", []),
        ("assets", [OrderedDict([("id", aid), ("kind", a["kind"]), ("bomRef", bom_ref(aid)), ("implicit", a["implicit"]),
                                 ("functions", []),
                                 ("occurrences", [OrderedDict(id=oid, relation=rel) for oid, rel in a["occ"]]),
                                 ("properties", a["props"])])
                    for aid, a in sorted(A.assets.items(), key=lambda kv: KIND_ORDER[kv[1]["kind"]])]),
        ("occurrences", A.occs),
        ("nonAssetMentions", A.mentions),
        ("notes", OrderedDict((k, v) for k, v in NOTES.items() if any(o["note"] == k for o in A.occs))),
        ("runtimeNotes", []),
        ("expectedOutput", [])])


def cbom(A):
    app_ref = "application/cbom-corpus-artifacts"
    components = []
    for aid, a in sorted(A.assets.items(), key=lambda kv: KIND_ORDER[kv[1]["kind"]]):
        d = a["props"]
        comp = OrderedDict([("type", "cryptographic-asset"), ("bom-ref", bom_ref(aid)), ("name", d["name"])])
        props = [{"name": "cbom-corpus:asset-id", "value": aid},
                 {"name": "cbom-corpus:implicit", "value": "true" if a["implicit"] else "false"},
                 {"name": "cbom-corpus:occurrence-count", "value": str(len(a["occ"]))}]
        if a["kind"] == "algorithm":
            ap = OrderedDict([("primitive", d["primitive"])])
            if d["parameterSetIdentifier"]:
                ap["parameterSetIdentifier"] = d["parameterSetIdentifier"]
            if d["curve"]:
                ap["curve"] = d["curve"]
            ap["executionEnvironment"] = "software-plain-ram"
            ap["implementationPlatform"] = "generic"
            ap["certificationLevel"] = ["none"]
            if d["mode"]:
                ap["mode"] = d["mode"]
            if d["padding"]:
                ap["padding"] = d["padding"]
            if d["classicalSecurityLevel"] is not None:
                ap["classicalSecurityLevel"] = d["classicalSecurityLevel"]
            if d["nistQuantumSecurityLevel"] is not None:
                ap["nistQuantumSecurityLevel"] = d["nistQuantumSecurityLevel"]
            cp = OrderedDict([("assetType", "algorithm"), ("algorithmProperties", ap)])
            if d["oid"]:
                cp["oid"] = d["oid"]
            props += [{"name": "cbom-corpus:family", "value": d["family"]},
                      {"name": "cbom-corpus:standards", "value": "; ".join(d["standards"])},
                      {"name": "cbom-corpus:nist-status", "value": d["nistStatus"]},
                      {"name": "cbom-corpus:cnsa-2.0", "value": d["cnsa2"]},
                      {"name": "cbom-corpus:quantum", "value": d["quantum"]}]
            if d["note"]:
                props.append({"name": "cbom-corpus:note", "value": d["note"]})
        elif a["kind"] == "certificate":
            cp = OrderedDict([("assetType", "certificate"), ("certificateProperties", OrderedDict([
                ("subjectName", d["subjectName"]), ("issuerName", d["issuerName"]),
                ("notValidBefore", d["notValidBefore"]), ("notValidAfter", d["notValidAfter"]),
                ("signatureAlgorithmRef", bom_ref(d["signatureAlgorithmRef"])),
                ("subjectPublicKeyRef", bom_ref(d["subjectPublicKeyRef"])),
                ("certificateFormat", d["certificateFormat"])]))])
            props += [{"name": "cbom-corpus:serial", "value": d["serial"]},
                      {"name": "cbom-corpus:fingerprint-sha256", "value": d["fingerprintSha256"]},
                      {"name": "cbom-corpus:issuer", "value": bom_ref(d["issuerRef"])},
                      {"name": "cbom-corpus:extensions", "value": "; ".join(d["extensions"])}]
        elif a["kind"] == "protocol":
            cp = OrderedDict([("assetType", "protocol"), ("protocolProperties", OrderedDict([
                ("type", d["type"]), ("version", d["version"]),
                ("cipherSuites", [OrderedDict([("name", cs["name"]), ("algorithms", [bom_ref(x) for x in cs["algorithms"]]),
                                               ("identifiers", cs["identifiers"])]) for cs in d["cipherSuites"]]),
                ("cryptoRefArray", [bom_ref(g) for g in d["groups"]])]))])
            props.append({"name": "cbom-corpus:note", "value": d["note"]})
        else:
            rp = OrderedDict([("type", d["type"]), ("id", aid), ("state", "active")])
            if d["algorithmRef"]:
                rp["algorithmRef"] = bom_ref(d["algorithmRef"])
            if d["size"]:
                rp["size"] = d["size"]
            if d.get("securedBy"):
                rp["securedBy"] = OrderedDict([("mechanism", d["securedBy"]["mechanism"]),
                                               ("algorithmRef", bom_ref(d["securedBy"]["algorithmRef"]))])
            cp = OrderedDict([("assetType", "related-crypto-material"), ("relatedCryptoMaterialProperties", rp)])
            props.append({"name": "cbom-corpus:provenance", "value": d["provenance"]})
            if d.get("value"):
                props.append({"name": "cbom-corpus:test-vector-value", "value": d["value"]})
            for key in ("spkiSha256", "publicKeySpkiSha256", "valueSha256", "sha256"):
                if d.get(key):
                    props.append({"name": f"cbom-corpus:{re.sub(r'(?<!^)(?=[A-Z])', '-', key).lower()}",
                                  "value": d[key]})
            if d["note"]:
                props.append({"name": "cbom-corpus:note", "value": d["note"]})
        comp["cryptoProperties"] = cp
        if a["occ"]:
            occ_list = []
            for oid, rel in a["occ"]:
                o = A.by_id[oid]
                item = OrderedDict([("location", f"{o['file']}")])
                if o["start"]["line"] is not None:
                    item["line"] = o["start"]["line"]
                    item["offset"] = o["start"]["column"] - 1
                if o["symbol"]:
                    item["symbol"] = o["symbol"]
                rng = f"byteRange={o['start']['byteOffset']}-{o['end']['byteOffset']}"
                if o["start"]["line"] is not None:
                    rng = (f"end={o['end']['line']}:{o['end']['column']}; charRange={o['start']['charOffset']}-"
                           f"{o['end']['charOffset']}; " + rng)
                item["additionalContext"] = (f"id={oid}; relation={rel}; role={o['role']}; scenario={o['scenario']}; "
                                             f"scope={o['scope']}; encoding={o['encoding']}; "
                                             f"encrypted={'true' if o['encrypted'] else 'false'}; {rng}")
                occ_list.append(item)
            comp["evidence"] = {"occurrences": occ_list}
        comp["properties"] = props
        components.append(comp)
    deps = [OrderedDict([("ref", app_ref), ("dependsOn", [])])]
    for aid, a in A.assets.items():
        if a["kind"] == "algorithm" and spec.ALGORITHMS[aid]["dependsOn"]:
            deps.append(OrderedDict([("ref", bom_ref(aid)),
                                     ("dependsOn", [bom_ref(x) for x in spec.ALGORITHMS[aid]["dependsOn"]])]))
    return OrderedDict([
        ("$schema", "http://cyclonedx.org/schema/bom-1.6.schema.json"), ("bomFormat", "CycloneDX"),
        ("specVersion", "1.6"), ("serialNumber", "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "cbom-corpus/artifacts"))),
        ("version", 1),
        ("metadata", OrderedDict([
            ("timestamp", GEN_TIME),
            ("tools", {"components": [{"type": "application", "name": "cbom-corpus ground-truth generator "
                                                                      "(_tooling/artifacts.py)", "version": "1.0.0"}]}),
            ("component", OrderedDict([("type", "application"), ("bom-ref", app_ref), ("name", "cbom-corpus-artifacts"),
                                       ("version", "1.0.0"),
                                       ("description", "Ground-truth CBOM for the artifact files of the CBOM corpus; "
                                                       "every occurrence was found by parsing the files, not by a "
                                                       "scanner.")]))])),
        ("components", components), ("dependencies", deps)])


# ---------------------------------------------------------------------------------------------- README
def code(s):
    s = str(s).replace("|", "\\|")
    return f"`` {s} ``" if "`" in s else f"`{s}`"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def where(o):
    if o["start"]["line"] is not None:
        return f"{o['start']['line']}:{o['start']['column']}-{o['end']['line']}:{o['end']['column']}"
    return f"bytes {o['start']['byteOffset']}-{o['end']['byteOffset']}"


def readme(A):
    occs, assets = A.occs, A.assets
    kinds = Counter(a["kind"] for a in assets.values())
    L = []
    w = L.append
    w("# CBOM ground-truth corpus - Artifacts\n")
    w(f"This case holds cryptography that lives in **files** rather than in program code: {len(FILES)} artifact files "
      f"(certificates, keys, a CSR and a CRL, PKCS#7, PKCS#12 and JKS stores, application secrets, an OpenSSL TLS "
      f"configuration and post-quantum certificates and keys, plus two decoys). They contain **{len(assets)} assets** "
      f"({kinds['algorithm']} algorithms, {kinds['certificate']} certificates, {kinds['protocol']} protocol, "
      f"{kinds['related-crypto-material']} items of related crypto material) at **{len(occs)} occurrences**, and "
      f"**{len(A.mentions)} non-asset mentions** that a scanner should not report. The same data is available "
      f"machine-readably in `cbom.cdx.json` (CycloneDX 1.6) and `ground-truth.json`.\n")
    w("> Every key, certificate, password and token here was generated for this corpus with `_tooling/artifacts.py` "
      "and protects nothing. The weak items (an RSA-1024 / SHA-1 certificate, the `changeit` store password, low "
      "PBKDF2 iteration counts) are deliberate so that policy checks have something to find.\n")
    w("The case targets file and secret scanners such as CBOMKit-Theia and CBOM-Lens, but every tool that accepts "
      "any input is scored on it. It is a directory of files, not a program: there is nothing to build or run.\n")
    w("## Files\n")
    rows = [(code(f["path"]), f["scenario"], f["format"], f["description"], f["bytes"],
             sum(1 for o in occs if o["file"] == f["path"] and o["nesting"] == 0),
             sum(1 for m in A.mentions if m["file"] == f["path"])) for f in A.file_info.values()]
    w(table(["File", "Scenario", "Format", "Contents", "Bytes", "Objects / settings", "Non-asset mentions"], rows) + "\n")
    w("Also here: `README.md` (this document), `cbom.cdx.json` (ground-truth CycloneDX 1.6 CBOM) and "
      "`ground-truth.json` (occurrence ledger, asset inventory, non-asset mentions, file hashes and the verification "
      "log). The orchestrator keeps the last two out of a tool's workspace.\n")
    w("## Scenarios\n")
    rows = []
    for sid, fam, desc in SCENARIOS:
        so = [o for o in occs if o["scenario"] == sid]
        files = [f for f in FILES if FILES[f]["scn"] == sid]
        al = sorted({o["asset"] for o in so}, key=lambda a: (KIND_ORDER[A.assets[a]["kind"]], a))
        rows.append((sid, fam, desc, ", ".join(code(f) for f in files), len(so), ", ".join(f"`{x}`" for x in al)))
    w(table(["Scenario", "Family", "What it holds", "Files", "Occurrences", "Assets"], rows) + "\n")
    w("## How occurrences are recorded\n")
    w("An **occurrence** is one place where an asset is stored: a certificate in a PEM block, a key in a PKCS#12 bag, "
      "a signature algorithm inside a certificate, a secret on a configuration line. Every occurrence carries "
      "`fileLevel: true`: the artifact file is the unit of evidence, so a scanner location that names the file counts "
      "even without a line. Coordinates:\n")
    w(table(["Field", "Convention"], [
        ("Text files", "Line and column (1-based, end exclusive), char and byte offsets of the PEM block "
                       "(from its BEGIN line to the end of its END line) or of the configuration value"),
        ("Binary files", "Byte range only: the whole file for DER, the certificate's DER inside PKCS#7 and JKS, the "
                         "encrypted blob for PKCS#12 bags, the AlgorithmIdentifier for PBES2 and MAC parameters"),
        ("Nesting", "0 = object or setting; 1+ = a field inside it (signature algorithm, subject public key, PBES2 "
                    "parameters). Nested occurrences reuse their container's span and name it in `container`"),
        ("Encrypted", "`true` when the object is stored encrypted and is readable only with the documented password"),
        ("CycloneDX", "`location` is the path relative to this directory; `line` and `offset` (column - 1) only for "
                      "text files; ranges, scope and encoding are in `additionalContext`"),
    ]) + "\n")
    w("Roles:\n")
    w(table(["Role", "Meaning"], [
        ("`obj`", "A stored object: certificate, private or public key, CSR, CRL (qualifier = encoding, e.g. `x509`, "
                  "`pkcs1`, `sec1`, `pkcs8`, `spki`, `openssh`)"),
        ("`alg`", "An algorithm identifier inside an object or a configuration value (qualifier = field, e.g. "
                  "`signatureAlgorithm`, `subjectPublicKeyInfo`, `pbes2.kdf`, `mac`, `cipher-suite`)"),
        ("`cfg`", "A protocol configuration directive (qualifier = directive)"),
        ("`mat`", "A secret value assigned in a configuration file (qualifier = variable)"),
    ]) + "\n")
    w("Recording rules: a certificate occurrence brings occurrences of its signature algorithm (and that algorithm's "
      "hash, with the signature algorithm as parent), its subject public key algorithm and its public key; a private "
      "key occurrence brings its key algorithm and, where the encoding stores it (PKCS#1, SEC 1 with a public point, "
      "PKCS#8 for RSA and EC, OpenSSH), its public key. A PKCS#8 key in seed form (ML-DSA, ML-KEM) and an Ed25519 "
      "PKCS#8 v1 key do not store the public key. Subject and authority key identifiers are not recorded as SHA-1 "
      "uses (RFC 5280 leaves the method open and nothing recomputes them). Ed25519's SHA-512 and ML-KEM's SHA-3 / "
      "SHAKE are implicit, as in the program cases.\n")
    w("## Summary\n")
    roles = Counter(o["kind"] for o in occs)
    w(table(["Measure", "Count"], [("Files", len(FILES)), ("Occurrences", len(occs))] +
            [(f"Occurrences with role `{k}`", roles[k]) for k in ("obj", "alg", "cfg", "mat") if roles[k]] +
            [("Occurrences inside encrypted containers", sum(1 for o in occs if o["encrypted"])),
             ("Algorithm assets (incl. implicit)", kinds["algorithm"]),
             ("Implicit assets (no occurrence)", sum(1 for a in assets.values() if a["implicit"])),
             ("Certificates", kinds["certificate"]), ("Protocols", kinds["protocol"]),
             ("Related crypto material", kinds["related-crypto-material"]),
             ("Non-asset mentions", len(A.mentions)), ("Verification checks passed", len(A.checks))]) + "\n")
    w("## Certificates\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "certificate":
            continue
        d = a["props"]
        rows.append((f"`{aid}`", code(d["subjectName"]), code(d["issuerName"]), d["serial"],
                     f"{d['notValidBefore'][:10]} to {d['notValidAfter'][:10]}", f"`{d['signatureAlgorithmRef']}`",
                     f"`{d['subjectPublicKeyRef']}`", ", ".join(code(f) for f in d["files"]),
                     code(d["fingerprintSha256"][:16] + "…")))
    w(table(["Asset", "Subject", "Issuer", "Serial", "Validity", "Signature", "Public key", "Files", "SHA-256"],
            rows) + "\n")
    w("Extensions:\n")
    w(table(["Asset", "Extensions"], [(f"`{aid}`", "; ".join(a["props"]["extensions"]))
                                      for aid, a in assets.items() if a["kind"] == "certificate"]) + "\n")
    w("## Algorithm assets\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "algorithm":
            continue
        d = a["props"]
        files = sorted({A.by_id[oid]["file"] for oid, _ in a["occ"]}, key=list(FILES).index)
        rows.append((f"`{aid}`", d["name"], d["primitive"], d["family"], d["parameterSetIdentifier"] or "-",
                     d["curve"] or "-", d["oid"] or "-", "implicit" if a["implicit"] else len(a["occ"]),
                     ", ".join(code(f) for f in files) or "-", ", ".join(d["dependsOn"]) or "-"))
    w(table(["Asset", "Name", "Primitive", "Family", "Parameter set", "Curve", "OID", "Occurrences", "Files",
             "Depends on"], rows) + "\n")
    w("Security and compliance:\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "algorithm":
            continue
        d = a["props"]
        rows.append((f"`{aid}`", d["classicalSecurityLevel"] if d["classicalSecurityLevel"] is not None else "-",
                     d["nistQuantumSecurityLevel"] if d["nistQuantumSecurityLevel"] is not None else "-",
                     "; ".join(d["standards"]), d["nistStatus"], d["cnsa2"], d["quantum"], d["note"] or "-"))
    w(table(["Asset", "Classical bits", "NIST PQ category", "Standards", "NIST status", "CNSA 2.0", "Quantum", "Note"],
            rows) + "\n")
    w("## Protocol\n")
    p = assets["tls13-openssl"]["props"]
    w(table(["Property", "Value"], [
        ("Asset", "`tls13-openssl`"), ("Type / version", f"{p['type']} {p['version']}"),
        ("Cipher suites", "; ".join(f"{cs['name']} ({','.join(cs['identifiers'])}): {', '.join(cs['algorithms'])}"
                                    for cs in p["cipherSuites"])),
        ("Key-exchange groups", ", ".join(f"`{g}`" for g in p["groups"])), ("Note", p["note"]),
        ("Occurrences", ", ".join(oid for oid, rel in assets["tls13-openssl"]["occ"] if rel == "direct"))]) + "\n")
    w("## Related cryptographic material\n")
    rows = []
    for aid, a in assets.items():
        if a["kind"] != "related-crypto-material":
            continue
        d = a["props"]
        places = []
        for oid, rel in a["occ"]:
            o = A.by_id[oid]
            places.append(f"{o['file']} ({o['scope']}{', encrypted' if o['encrypted'] else ''})")
        secured = d.get("securedBy", {}).get("mechanism", "-")
        rows.append((f"`{aid}`", d["name"], d["type"], d["size"] or "-", f"`{d['algorithmRef']}`" if d["algorithmRef"]
                     else "-", d["scenario"], secured, "; ".join(places), d["note"] or "-"))
    w(table(["Asset", "Name", "Type", "Size (bits)", "Algorithm", "Scenario", "Protected by", "Stored in", "Note"],
            rows) + "\n")
    w("Secret values are not repeated in this README, the CBOM or the ledger; `ground-truth.json` gives their "
      "SHA-256 (`valueSha256`) so a reported value can be checked.\n")
    w("## Occurrence ledger\n")
    w("Every occurrence, in file order. Nested rows (signature algorithm, public key, PBES2 parameters) name their "
      "container.\n")
    rows = []
    for o in occs:
        rows.append((o["id"], code(o["file"]), o["scenario"], f"`{o['role']}`",
                     f"`{o['asset']}`" + (f" ^`{o['parent']}`" if o["parent"] else ""), where(o), o["nesting"],
                     o["container"] or "-", code(o["scope"]), code(o["symbol"]) if o["symbol"] else "-",
                     o["encoding"], "yes" if o["encrypted"] else "-", code(o["evidence"]) if o["evidence"] else "-",
                     o["note"] or "-"))
    w(table(["ID", "File", "Scn", "Role", "Asset (^parent)", "Location", "Nest", "Container", "Scope", "Symbol",
             "Encoding", "Encrypted", "Evidence", "Note"], rows) + "\n")
    w("## Non-asset mentions (negative ground truth)\n")
    w("Every PEM armour that does not enclose a decodable object, and every case-insensitive match of the "
      "algorithm-name lexicon (`_tooling/spec.py`, `DECOY_PATTERN`) outside all occurrence spans, in every text file "
      "of the case. A scanner that reports one of these as a cryptographic asset produces a false positive.\n")
    rows = [(d["id"], code(d["file"]), f"{d['line']}:{d['column']}", code(d["text"]), d["context"],
             code(d["token"][:80]), d["reason"]) for d in A.mentions]
    w(table(["ID", "File", "L:C", "Match", "Context", "Line", "Why it is not an asset"], rows) + "\n")
    w("## Detection notes\n")
    used = OrderedDict()
    for o in occs:
        if o["note"]:
            used.setdefault(o["note"], []).append(o["id"])
    w(table(["Note", "Explanation", "Occurrences"], [(f"`{k}`", NOTES[k], f"{len(v)} ({v[0]} …)" if len(v) > 3
                                                      else ", ".join(v)) for k, v in used.items()]) + "\n")
    w("## Verification\n")
    w(f"`_tooling/artifacts.py` parsed every file with cryptography {CRYPTOGRAPHY_VERSION} "
      f"({_openssl_backend.backend.openssl_version_text()}) and stopped on the first mismatch. {len(A.checks)} checks "
      "passed, among them: every certificate's subject, issuer, serial, validity, signature algorithm and key match the "
      "registry and its signature verifies under its issuer (including the SHA-1 and ML-DSA-65 signatures); every "
      "copy of a certificate is byte-identical; every private key matches its certificate or public key; the CSR and "
      "CRL signatures verify; the encrypted PKCS#8 key opens with the passphrase from `secrets/app.env`, the PKCS#12 "
      "file and the JKS digest with `changeit`; the JWT verifies with the HS256 key next to it; the two decoys do not "
      "decode. The full list is in `ground-truth.json` (`verification.details`).\n")
    w("To regenerate: `cd _tooling && python3 artifacts.py` rewrites this README, `cbom.cdx.json` and "
      "`ground-truth.json` from the files; `python3 artifacts.py generate --force` first replaces every key, "
      "certificate and secret with new random ones.\n")
    return "\n".join(L)


def write_docs():
    A = analyse()
    docs_out = {"README.md": readme(A),
                "cbom.cdx.json": json.dumps(cbom(A), indent=2, ensure_ascii=False) + "\n",
                "ground-truth.json": json.dumps(ground_truth(A), indent=2, ensure_ascii=False) + "\n"}
    for name, text in docs_out.items():
        # the README is copied into every tool workspace, and none of the three may carry key material or secrets
        if "-----BEGIN" in text or any(v in text for v in A.secret_values.values() if len(v) > 8):
            raise AssertionError(f"{name} would contain PEM armour or a secret value")
        (CASE / name).write_text(text, encoding="utf-8")
    print(f"artifacts   files={len(FILES)} occurrences={len(A.occs)} assets={len(A.assets)} "
          f"mentions={len(A.mentions)} checks={len(A.checks)}")
    import docs                                            # corpus README lists the case
    from languages import LANGS
    (OUT / "README.md").write_text(docs.root_readme([docs.analyse(lang) for lang in LANGS]), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", nargs="?", choices=["generate", "docs"], default="docs")
    ap.add_argument("--force", action="store_true", help="replace an existing case (new keys and certificates)")
    args = ap.parse_args()
    if args.command == "generate":
        generate(force=args.force)
    write_docs()
