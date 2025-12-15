# Crypto Mental Models (Hashing, Encryption, Keys)

## Learning objectives
- Distinguish hashing from encryption
- Explain symmetric vs asymmetric encryption at a high level
- Understand what TLS does (and what it does not do)

## Hashing
- One-way transformation
- Used for integrity checks and (properly) for password storage

## Encryption
- Two-way transformation using a key
- Protects confidentiality

## Symmetric vs asymmetric (conceptual)
- Symmetric: same key encrypts/decrypts (fast)
- Asymmetric: public/private keys (identity + key exchange)

## TLS summary (beginner level)
TLS protects data **in transit**.
It does not automatically make a website “trustworthy” or “safe.”
