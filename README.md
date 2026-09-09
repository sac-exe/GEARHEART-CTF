# GEARHEART — Web Exploitation CTF

GEARHEART is a multi-stage web exploitation Capture The Flag (CTF)
challenge built with Python, Flask, Jinja2, Docker and RSA cryptography.

The challenge is designed around a chained exploitation path where
each stage provides information or access required for the next stage.

## Challenge Overview

The intended attack chain is:

Information Disclosure
        ↓
Session Enumeration
        ↓
Admin Session Hijacking
        ↓
Broken Access Control
        ↓
SSTI
        ↓
Blacklist Bypass
        ↓
Remote Code Execution
        ↓
Key Recovery
        ↓
RSA Decryption
        ↓
Flag

## Technologies

- Python
- Flask
- Jinja2
- Docker
- RSA
- HTML/CSS

## Vulnerability Classes

- Information Disclosure
- Session Hijacking
- Broken Access Control
- Server-Side Template Injection (SSTI)
- Blacklist Bypass
- Remote Code Execution (RCE)
- Cryptography

## Running the Challenge

### Requirements

- Docker

### Build

```bash
docker build -t gearheart .