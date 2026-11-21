# Deploying the reporting service

The service reads its certificate from `pki/server.crt` and the matching key from `pki/server.key`.
On a new host, paste the certificate issued for that host into `examples/placeholder.crt`; the file in
this folder only shows the expected shape.

Never commit a private key. This is what the start of one looks like (shortened, not a usable key):

```text
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7...
...(the remaining lines are deliberately left out)...
-----END PRIVATE KEY-----
```

Plan: move the RSA-2048 server key to ECDSA P-384 or ML-DSA-65 once every client supports it, and stop
accepting SHA-1 signatures.
