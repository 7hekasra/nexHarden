# 🛡️ nexHardener

> A lightweight Linux system hardening tool designed to improve system security through automated checks and security recommendations.

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Security-purple?style=for-the-badge&logo=linux" alt="Linux Security">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Status-Development-orange?style=for-the-badge" alt="Status">
</p>

---

## 📖 About

**nexHardener** is a Linux security hardening tool that helps users identify common security weaknesses and improve the overall security posture of their systems.

The project is designed to make Linux hardening easier, faster, and more accessible without requiring users to manually inspect every security-related configuration.

---

## ✨ Features

* 🔍 Security configuration checks
* 🔐 SSH security checks
* 👤 User and permission checks
* 🔥 Firewall status checks
* ⚙️ System configuration checks
* 📦 Service inspection
* 🚨 Detection of potentially insecure configurations
* 📊 Security status overview
* 🛡️ Hardening recommendations
* ⚡ Lightweight and fast CLI-based design

---

## 🧰 Requirements

* Linux
* Python 3.x
* Root privileges for some checks

Depending on the Linux distribution, some checks may require additional system utilities.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/nexHardener.git
```

Enter the project directory:

```bash
cd nexHardener
```

Run nexHardener:

```bash
python3 nexHardener.py
```

For checks that require elevated privileges:

```bash
sudo python3 nexHardener.py
```

---

## 💻 Usage

Simply run the tool:

```bash
python3 nexHardener.py
```

nexHardener will inspect the system and report potential security issues and recommended improvements.

Example:

```text
╔══════════════════════════════════════╗
║              nexHardener             ║
║        Linux Security Hardener       ║
╚══════════════════════════════════════╝

[+] Checking system configuration...
[+] Checking SSH configuration...
[+] Checking firewall...
[+] Checking users and permissions...
[+] Checking active services...

Security checks completed.

[✓] SSH configuration
[✓] Firewall
[!] User configuration
[✓] System configuration
[!] Service configuration
```

---

## 🔎 Security Checks

### 🔐 SSH

Checks common SSH security configurations such as:

* Root login configuration
* Password authentication
* SSH configuration
* Potentially insecure settings

### 🔥 Firewall

Checks whether a firewall is enabled and attempts to identify commonly used firewall systems such as:

* UFW
* firewalld
* nftables
* iptables

### 👤 Users & Permissions

Checks system users and potentially sensitive configurations related to:

* User accounts
* Privileged users
* Shell access
* UID configuration
* Permissions

### ⚙️ Services

Inspects active services and helps identify potentially unnecessary services that could increase the system's attack surface.

### 🖥️ System Configuration

Checks selected system-level security configurations and provides recommendations where applicable.

---

## 🛡️ Hardening

The goal of nexHardener is not only to detect security issues, but also to provide practical recommendations for improving the system.

Future versions may include automated hardening capabilities with:

* Configuration backups
* Safe configuration changes
* Restore functionality
* Hardening profiles
* Interactive confirmation before applying changes

---

## ⚠️ Warning

**Use this tool carefully on production systems.**

Changing security configurations can potentially:

* Disable services
* Change system behavior
* Restrict user access
* Break existing configurations
* Lock you out of remote systems

Always create a backup before applying security-related changes.

---

## 🗺️ Roadmap

* [x] Initial project
* [x] Basic security checks
* [ ] SSH hardening
* [ ] Firewall hardening
* [ ] User & permission audit
* [ ] Service audit
* [ ] Security scoring
* [ ] Interactive CLI
* [ ] Automatic configuration backup
* [ ] Configuration restore
* [ ] JSON output
* [ ] Detailed reports
* [ ] Hardening profiles
* [ ] More Linux distributions
* [ ] Improved detection engine

---

## 🤝 Contributing

Contributions, ideas, bug reports, and improvements are welcome.

If you find a bug or have an idea that could make nexHardener better, feel free to open an issue or submit a pull request.

---

## 📄 License

This project currently does not include a license.

---

## ⭐ Support

If you find **nexHardener** useful, consider giving the project a ⭐ on GitHub.

---

<p align="center">
  Made for Linux security 🐧🛡️
</p>
