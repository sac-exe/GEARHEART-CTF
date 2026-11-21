# Project GEARHEART

**A Medium–Hard Web Exploitation CTF Challenge**

Project GEARHEART is a web-based Capture The Flag (CTF) challenge focused on chaining multiple vulnerabilities to compromise an application and recover a protected flag.

The challenge simulates a vulnerable administrative portal where players must investigate information leaks, hijack an administrator session, bypass a restrictive input filter, achieve server-side command execution, and recover an RSA-encrypted flag.

## Challenge Information

| Property | Details |
|---|---|
| Challenge Name | Project GEARHEART |
| Category | Web Exploitation |
| Difficulty | Medium–Hard |
| Platform | TryHackMe |
| Author | s_c.exe |
| Main Technologies | Python, Flask, Jinja2, Docker |
| Port | 5050 |

## Attack Chain

The challenge involves the following stages:

1. **Information Disclosure** – Discover hidden information in the application's page source.
2. **Session Hijacking** – Identify and exploit exposed administrator session information.
3. **Server-Side Template Injection (SSTI)** – Bypass a naive blacklist and exploit Jinja2 template rendering.
4. **Remote Code Execution (RCE)** – Abuse Python introspection to locate and execute a subprocess class.
5. **RSA Key Recovery** – Discover an exposed private key and decrypt the final flag.

## Features

- Flask-based vulnerable web application.
- Insecure session management.
- Information disclosure through a debug endpoint.
- Jinja2 SSTI with blacklist-based filtering.
- Python introspection and command execution.
- Exposed RSA private key.
- Base64-encoded encrypted flag.
- Docker-based deployment.

## Requirements

- Docker
- Git
- A web browser
- Basic knowledge of Linux and web exploitation

## Running Locally

Clone the repository:

```bash
git clone (https://github.com/sac-exe/GEARHEART-CTF.git)
cd GEARHEART-CTF
```

Build the Docker image:

```bash
docker build -t gearheart .
```

Run the container:

```bash
docker run -d \
  --name gearheart \
  -p 5050:5050 \
  gearheart
```

Access the application:

```text
http://localhost:5050
```

Check the container:

```bash
docker ps
```

Stop the container:

```bash
docker stop gearheart
```

Remove the container:

```bash
docker rm gearheart
```

## Initial Access

The application provides a guest account for initial access.

| Username | Password |
|---|---|
| guest | guest123 |

Use these credentials to explore the application and begin the challenge.

## Learning Objectives

By completing this challenge, players can practice:

- Identifying information disclosure vulnerabilities.
- Understanding insecure session handling.
- Exploiting session hijacking vulnerabilities.
- Understanding Jinja2 Server-Side Template Injection.
- Bypassing naive blacklist-based input validation.
- Exploring Python object introspection.
- Understanding remote command execution.
- Working with RSA private keys and encrypted data.
- Using CyberChef for data decoding and cryptographic operations.

## Tools

The following tools may be useful:

- Browser Developer Tools
- Burp Suite
- CyberChef
- Linux terminal
- Python

## Disclaimer

Project GEARHEART is intentionally vulnerable and designed exclusively for educational purposes and authorized CTF environments.

Do not deploy this application on a public production server or expose it to untrusted networks outside an authorized challenge environment.

The author is not responsible for misuse of this project.

## Author

**s_c.exe**

Project GEARHEART — A chained web exploitation challenge.

