# CTF Challenge Authoring

Web Exploitation challenges I designed and authored. Each folder contains the challenge description, design notes, and a full solve writeup with screenshots.

> ⚠️ These challenges were built with intentional vulnerabilities for CTF purposes. Nothing here should be deployed or reused in production.

## Challenges

| Challenge | Category | Difficulty | Vulnerability | Context |
|---|---|---|---|---|
| [Registry](./Registry/writeup.md) | Web Exploitation | Medium | Python `eval()` blacklist bypass via `chr()` | CSC CTF Contest 2026 |
| [Furab](./Furab/README.md) | Web Exploitation | Medium | Unrestricted file upload — hidden header + `.htaccess` filter bypass | Trial challenge (author selection test) |

## About

**Registry** was contributed to the organizing team's challenge repository for CSC CTF Contest 2026 (now concluded).

**Furab** was a trial challenge I built when trying out as a challenge author — not part of the official contest lineup, but included here because the design (hidden header + Apache `.htaccess` filter bypass) was a solid showcase of the same skills.

This repo collects my own authored challenges and solve writeups separately, for portfolio purposes.
