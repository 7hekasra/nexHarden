#!/usr/bin/env python3

import os
import subprocess
import sys
import shutil
import re
import time
import json
from datetime import datetime

# ============================================
# Colors for terminal output
# ============================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

BANNER = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███╗   ██╗███████╗██╗  ██╗██╗  ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
║   ████╗  ██║██╔════╝╚██╗██╔╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ███████║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║
║   ██║ ╚████║███████╗██╔╝ ██╗██║  ██║██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
║                                                                  ║
║             Ubuntu Hardening Script - Version 1.0.0              ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   {Colors.BLUE}GitHub{Colors.END}   : github.com/7hekasra                                 {Colors.CYAN}║
║   {Colors.CYAN}Telegram{Colors.END} : t.me/linuxfarci                                     {Colors.CYAN}║
║   {Colors.BLUE}Website{Colors.END}  : linuxfarci.ir                                       {Colors.CYAN}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Colors.END}
"""

class SecurityScanner:
    def __init__(self):
        self.results = {}
        self.total_checks = 0
        self.passed_checks = 0
        
    def check(self, name, condition, weight=1):
        self.total_checks += weight
        if condition:
            self.passed_checks += weight
            self.results[name] = {"status": "PASS", "weight": weight}
        else:
            self.results[name] = {"status": "FAIL", "weight": weight}
        return condition
    
    def get_score(self):
        if self.total_checks == 0:
            return 0
        return int((self.passed_checks / self.total_checks) * 100)
    
    def get_failed_checks(self):
        failed = []
        for name, data in self.results.items():
            if data["status"] == "FAIL":
                failed.append(name)
        return failed
    
    def print_report(self, title="Security Scan Report"):
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.HEADER} {title}{Colors.END}")
        print(f"{Colors.BOLD}{'='*70}{Colors.END}")
        
        for name, data in self.results.items():
            if data["status"] == "PASS":
                print(f"  {Colors.GREEN}PASS{Colors.END}  {name}")
            else:
                print(f"  {Colors.RED}FAIL{Colors.END}  {name}")
        
        print(f"{Colors.BOLD}{'-'*70}{Colors.END}")
        score = self.get_score()
        print(f" {Colors.BOLD}SECURITY SCORE:{Colors.END} {self._colorize_score(score)}%")
        
        if score >= 90:
            print(f" {Colors.GREEN}STATUS: EXCELLENT{Colors.END}")
        elif score >= 70:
            print(f" {Colors.CYAN}STATUS: GOOD{Colors.END}")
        elif score >= 50:
            print(f" {Colors.YELLOW}STATUS: MODERATE{Colors.END}")
        else:
            print(f" {Colors.RED}STATUS: CRITICAL{Colors.END}")
        
        print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
        return score
    
    def _colorize_score(self, score):
        if score >= 90:
            return f"{Colors.GREEN}{score}{Colors.END}"
        elif score >= 70:
            return f"{Colors.CYAN}{score}{Colors.END}"
        elif score >= 50:
            return f"{Colors.YELLOW}{score}{Colors.END}"
        else:
            return f"{Colors.RED}{score}{Colors.END}"

def run_command(command, check=True, capture_output=False):
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        if check and result.returncode != 0:
            print(f"{Colors.RED}Error in command: {command}{Colors.END}")
            print(f"{Colors.RED}Error: {result.stderr if capture_output else ''}{Colors.END}")
        return result
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
        return None

def get_command_output(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def file_contains(file_path, pattern):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return re.search(pattern, content) is not None
    except:
        return False

def service_is_active(service_name):
    result = get_command_output(f"systemctl is-active {service_name}")
    return result == "active"

def service_is_enabled(service_name):
    result = get_command_output(f"systemctl is-enabled {service_name}")
    return result == "enabled"

def perform_security_scan():
    print(f"\n{Colors.BOLD} Performing security scan...{Colors.END}")
    scanner = SecurityScanner()
    
    update_check = get_command_output("apt list --upgradable 2>/dev/null | grep -c upgradable")
    if update_check and int(update_check) <= 10:
        scanner.check("System is up to date (<=10 updates pending)", True)
    else:
        scanner.check("System is up to date (<=10 updates pending)", False)
    
    ufw_status = get_command_output("ufw status | grep -q 'Status: active' && echo 'active'")
    scanner.check("UFW firewall is active", ufw_status == "active")
    
    open_ports = get_command_output("ss -tuln | grep -E ':(22|80|443)' | wc -l")
    if open_ports:
        scanner.check("Only essential ports open (SSH, HTTP, HTTPS)", int(open_ports) <= 3)
    else:
        scanner.check("Only essential ports open (SSH, HTTP, HTTPS)", False)
    
    ssh_config = "/etc/ssh/sshd_config"
    if os.path.exists(ssh_config):
        root_login = file_contains(ssh_config, r"^PermitRootLogin\s+no")
        scanner.check("Root login is disabled in SSH", root_login)
        
        pass_auth = file_contains(ssh_config, r"^PasswordAuthentication\s+no")
        scanner.check("Password authentication is disabled in SSH", pass_auth)
        
        pubkey_auth = file_contains(ssh_config, r"^PubkeyAuthentication\s+yes")
        scanner.check("Public key authentication is enabled in SSH", pubkey_auth)
        
        max_auth = file_contains(ssh_config, r"^MaxAuthTries\s+[0-5]")
        scanner.check("SSH MaxAuthTries <= 5", max_auth)
    else:
        scanner.check("SSH is configured", False)
    
    fail2ban_status = get_command_output("systemctl is-active fail2ban")
    scanner.check("Fail2ban is running", fail2ban_status == "active")
    
    unwanted_services = ["cups", "avahi-daemon", "bluetooth", "nfs-server", "rpcbind"]
    active_unwanted = 0
    for svc in unwanted_services:
        if service_is_active(svc):
            active_unwanted += 1
    scanner.check("No unnecessary services are running", active_unwanted == 0)
    
    sysctl_params = {
        "net.ipv4.conf.all.rp_filter": "1",
        "net.ipv4.icmp_echo_ignore_all": "1",
        "net.ipv4.tcp_syncookies": "1",
        "kernel.randomize_va_space": "2",
        "kernel.kptr_restrict": "2",
    }
    
    sysctl_passed = 0
    for param, expected in sysctl_params.items():
        actual = get_command_output(f"sysctl -n {param}")
        if actual == expected:
            sysctl_passed += 1
    scanner.check(f"Kernel hardening parameters applied ({sysctl_passed}/{len(sysctl_params)})", 
                  sysctl_passed >= 4)
    
    login_defs = "/etc/login.defs"
    if os.path.exists(login_defs):
        max_days = get_command_output("grep -E '^PASS_MAX_DAYS' /etc/login.defs | awk '{print $2}'")
        if max_days and int(max_days) <= 90:
            scanner.check("Password max age <= 90 days", True)
        else:
            scanner.check("Password max age <= 90 days", False)
        
        min_days = get_command_output("grep -E '^PASS_MIN_DAYS' /etc/login.defs | awk '{print $2}'")
        if min_days and int(min_days) >= 7:
            scanner.check("Password min age >= 7 days", True)
        else:
            scanner.check("Password min age >= 7 days", False)
    
    extra_users = ["games", "news", "uucp", "operator", "ftp", "gopher"]
    found_extra = 0
    for user in extra_users:
        if get_command_output(f"id {user} 2>/dev/null"):
            found_extra += 1
    scanner.check("No extra/unnecessary users exist", found_extra == 0)
    
    auditd_status = service_is_active("auditd")
    scanner.check("Auditd is running", auditd_status)
    
    unattended_status = service_is_active("unattended-upgrades")
    scanner.check("Unattended upgrades are enabled", unattended_status)
    
    scanner.print_report(" SECURITY SCAN REPORT")
    return scanner

def show_recommendations(scanner):
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER} RECOMMENDATIONS{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    failed = scanner.get_failed_checks()
    total_failed = len(failed)
    current_score = scanner.get_score()
    
    if total_failed == 0:
        print(f"{Colors.GREEN} Your system is already secure. No recommendations needed.{Colors.END}")
        return True
    
    print(f" Found {Colors.YELLOW}{total_failed}{Colors.END} security issues.")
    print(f" Current security score: {scanner._colorize_score(current_score)}%")
    
    potential_score = current_score
    fixed_items = 0
    
    for i, issue in enumerate(failed, 1):
        print(f"\n {Colors.BOLD}{i}.{Colors.END} {issue}")
        if "updates pending" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Run 'apt update && apt upgrade -y'")
            potential_score += 7
        elif "UFW firewall" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Enable UFW with 'ufw enable'")
            potential_score += 7
        elif "ports open" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Close unnecessary ports with UFW")
            potential_score += 6
        elif "Root login" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'PermitRootLogin no' in /etc/ssh/sshd_config")
            potential_score += 7
        elif "Password authentication" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'PasswordAuthentication no' in /etc/ssh/sshd_config")
            potential_score += 7
        elif "Public key authentication" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'PubkeyAuthentication yes' in /etc/ssh/sshd_config")
            potential_score += 5
        elif "MaxAuthTries" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'MaxAuthTries 3' in /etc/ssh/sshd_config")
            potential_score += 5
        elif "Fail2ban" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Install and enable Fail2ban")
            potential_score += 7
        elif "unnecessary services" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Disable unwanted services with systemctl")
            potential_score += 6
        elif "Kernel hardening" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Apply kernel parameters in /etc/sysctl.conf")
            potential_score += 7
        elif "Password max age" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'PASS_MAX_DAYS 90' in /etc/login.defs")
            potential_score += 5
        elif "Password min age" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Set 'PASS_MIN_DAYS 7' in /etc/login.defs")
            potential_score += 5
        elif "extra/unnecessary users" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Remove unused users with userdel")
            potential_score += 6
        elif "Auditd" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Install and enable auditd")
            potential_score += 5
        elif "Unattended upgrades" in issue:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Install and enable unattended-upgrades")
            potential_score += 5
        else:
            print(f"    {Colors.CYAN}-> Fix:{Colors.END} Review and apply appropriate security measures")
            potential_score += 3
    
    potential_score = min(potential_score, 100)
    
    print(f"\n{Colors.BOLD}{'-'*70}{Colors.END}")
    print(f" Potential security score after fixes: {scanner._colorize_score(potential_score)}%")
    print(f" Improvement: {Colors.GREEN}+{potential_score - current_score}%{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    return False

def get_user_confirmation():
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER} CONFIRMATION{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f" {Colors.GREEN}[1]{Colors.END} Yes, apply all fixes")
    print(f" {Colors.RED}[2]{Colors.END} No, skip hardening")
    print(f" {Colors.YELLOW}[3]{Colors.END} Exit")
    
    while True:
        choice = input(f"\n {Colors.BOLD}Enter your choice (1/2/3):{Colors.END} ").strip()
        if choice == "1":
            return True
        elif choice == "2":
            return False
        elif choice == "3":
            print(f"{Colors.YELLOW}Exiting...{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid choice. Please enter 1, 2, or 3.{Colors.END}")

def system_update():
    print(f"\n{Colors.BLUE}[1] Updating system and installing essential packages...{Colors.END}")
    run_command("apt update -y")
    run_command("apt upgrade -y")
    run_command("apt install -y wget curl gnupg2 ufw fail2ban unattended-upgrades auditd apt-listchanges")
    run_command("apt autoremove -y")
    print(f"{Colors.GREEN}System update completed.{Colors.END}\n")

def configure_firewall():
    print(f"{Colors.BLUE}[2] Configuring UFW firewall...{Colors.END}")
    run_command("ufw default deny incoming")
    run_command("ufw default allow outgoing")
    run_command("ufw allow ssh")
    run_command("ufw allow http")
    run_command("ufw allow https")
    run_command("ufw --force enable")
    print(f"{Colors.GREEN}Firewall configured.{Colors.END}\n")

def secure_ssh():
    print(f"{Colors.BLUE}[3] Securing SSH configuration...{Colors.END}")
    ssh_config = "/etc/ssh/sshd_config"
    if not os.path.exists(ssh_config):
        print(f"{Colors.RED}SSH config not found!{Colors.END}")
        return

    shutil.copy(ssh_config, ssh_config + ".backup")

    settings = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",
        "PubkeyAuthentication": "yes",
        "ChallengeResponseAuthentication": "no",
        "UsePAM": "yes",
        "X11Forwarding": "no",
        "MaxAuthTries": "3",
        "MaxSessions": "5",
        "ClientAliveInterval": "300",
        "ClientAliveCountMax": "2",
        "PermitEmptyPasswords": "no",
        "AllowAgentForwarding": "no",
        "TCPKeepAlive": "no",
        "Compression": "no",
        "LogLevel": "VERBOSE",
    }

    with open(ssh_config, "r") as f:
        lines = f.readlines()

    new_lines = []
    applied = set()
    for line in lines:
        if line.strip() and not line.startswith("#"):
            key = line.split()[0]
            if key in settings:
                new_lines.append(f"{key} {settings[key]}\n")
                applied.add(key)
                continue
        new_lines.append(line)

    for key, value in settings.items():
        if key not in applied:
            new_lines.append(f"\n{key} {value}\n")

    with open(ssh_config, "w") as f:
        f.writelines(new_lines)

    run_command("systemctl restart sshd")
    print(f"{Colors.GREEN}SSH secured.{Colors.END}\n")

def setup_fail2ban():
    print(f"{Colors.BLUE}[4] Setting up Fail2ban...{Colors.END}")
    run_command("systemctl enable fail2ban")
    run_command("systemctl start fail2ban")

    jail_local = "/etc/fail2ban/jail.local"
    if os.path.exists("/etc/fail2ban/jail.conf"):
        shutil.copy("/etc/fail2ban/jail.conf", jail_local)
    
    with open(jail_local, "a") as f:
        f.write("""
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
""")

    run_command("systemctl restart fail2ban")
    print(f"{Colors.GREEN}Fail2ban configured.{Colors.END}\n")

def disable_unnecessary_services():
    print(f"{Colors.BLUE}[5] Disabling unnecessary services...{Colors.END}")
    services_to_disable = [
        "cups", "avahi-daemon", "bluetooth", "nfs-server",
        "rpcbind", "vsftpd", "telnet", "dovecot", "samba"
    ]

    for service in services_to_disable:
        run_command(f"systemctl stop {service}", check=False)
        run_command(f"systemctl disable {service}", check=False)

    print(f"{Colors.GREEN}Unnecessary services disabled.{Colors.END}\n")

def kernel_hardening():
    print(f"{Colors.BLUE}[6] Applying kernel hardening parameters...{Colors.END}")
    sysctl_conf = "/etc/sysctl.conf"
    settings = {
        "net.ipv4.conf.all.rp_filter": "1",
        "net.ipv4.conf.default.rp_filter": "1",
        "net.ipv4.conf.all.accept_redirects": "0",
        "net.ipv4.conf.default.accept_redirects": "0",
        "net.ipv4.conf.all.secure_redirects": "0",
        "net.ipv4.conf.default.secure_redirects": "0",
        "net.ipv4.conf.all.accept_source_route": "0",
        "net.ipv4.conf.default.accept_source_route": "0",
        "net.ipv4.icmp_echo_ignore_all": "1",
        "net.ipv4.icmp_ignore_bogus_error_responses": "1",
        "net.ipv4.tcp_syncookies": "1",
        "net.ipv4.tcp_max_syn_backlog": "2048",
        "net.ipv4.tcp_synack_retries": "2",
        "net.ipv4.tcp_syn_retries": "5",
        "kernel.randomize_va_space": "2",
        "kernel.kptr_restrict": "2",
        "kernel.dmesg_restrict": "1",
        "kernel.printk": "3 3 3 3",
        "kernel.pid_max": "65536",
    }

    with open(sysctl_conf, "a") as f:
        for key, value in settings.items():
            f.write(f"{key} = {value}\n")

    run_command("sysctl -p")
    print(f"{Colors.GREEN}Kernel parameters applied.{Colors.END}\n")

def password_policy():
    print(f"{Colors.BLUE}[7] Setting up password policies...{Colors.END}")
    login_defs = "/etc/login.defs"
    with open(login_defs, "r+") as f:
        content = f.read()
        content = re.sub(r"PASS_MAX_DAYS\s+\d+", "PASS_MAX_DAYS 90", content)
        content = re.sub(r"PASS_MIN_DAYS\s+\d+", "PASS_MIN_DAYS 7", content)
        content = re.sub(r"PASS_WARN_AGE\s+\d+", "PASS_WARN_AGE 7", content)
        f.seek(0)
        f.write(content)
        f.truncate()

    pam_files = ["/etc/pam.d/common-auth", "/etc/pam.d/sshd"]
    for pam_file in pam_files:
        if os.path.exists(pam_file):
            with open(pam_file, "r") as f:
                content = f.read()
            if "pam_tally2.so" not in content:
                with open(pam_file, "a") as f:
                    f.write("auth required pam_tally2.so onerr=fail deny=5 unlock_time=1800\n")
            if "pam_pwquality.so" not in content:
                with open(pam_file, "a") as f:
                    f.write("password requisite pam_pwquality.so retry=3 minlen=12 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1\n")

    print(f"{Colors.GREEN}Password policies applied.{Colors.END}\n")

def remove_extra_users():
    print(f"{Colors.BLUE}[8] Removing extra users and groups...{Colors.END}")
    extra_users = ["games", "news", "uucp", "operator", "ftp", "nobody4", "gopher"]
    for user in extra_users:
        run_command(f"userdel {user}", check=False)

    extra_groups = ["games", "news", "uucp", "operator", "ftp", "gopher"]
    for group in extra_groups:
        run_command(f"groupdel {group}", check=False)

    print(f"{Colors.GREEN}Extra users/groups removed.{Colors.END}\n")

def setup_logging():
    print(f"{Colors.BLUE}[9] Setting up logging and monitoring...{Colors.END}")
    run_command("systemctl enable auditd")
    run_command("systemctl start auditd")

    logrotate_conf = "/etc/logrotate.conf"
    with open(logrotate_conf, "a") as f:
        f.write("""
/var/log/auth.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root adm
}

/var/log/syslog {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root adm
}
""")

    print(f"{Colors.GREEN}Logging configured.{Colors.END}\n")

def final_report(before_score, after_score):
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.GREEN} HARDENING COMPLETED SUCCESSFULLY {Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"\n {Colors.BOLD}SECURITY SCORE COMPARISON:{Colors.END}")
    print(f"  Before hardening: {before_score}%")
    print(f"  After hardening:  {after_score}%")
    
    improvement = after_score - before_score
    if improvement > 0:
        print(f"  Improvement: {Colors.GREEN}+{improvement}%{Colors.END}")
    else:
        print(f"  {Colors.YELLOW}No improvement detected (check configuration){Colors.END}")
    
    print(f"\n{Colors.BOLD}{'-'*70}{Colors.END}")
    
    if after_score >= 90:
        print(f" {Colors.GREEN}STATUS: EXCELLENT{Colors.END}")
    elif after_score >= 70:
        print(f" {Colors.CYAN}STATUS: GOOD{Colors.END}")
    elif after_score >= 50:
        print(f" {Colors.YELLOW}STATUS: MODERATE{Colors.END}")
    else:
        print(f" {Colors.RED}STATUS: CRITICAL{Colors.END}")
    
    print(f"\n {Colors.BOLD}Applied hardening measures:{Colors.END}")
    print(f"  {Colors.GREEN}System updated and upgraded{Colors.END}")
    print(f"  {Colors.GREEN}UFW firewall configured (SSH, HTTP, HTTPS allowed){Colors.END}")
    print(f"  {Colors.GREEN}SSH secured (root login disabled, password auth disabled){Colors.END}")
    print(f"  {Colors.GREEN}Fail2ban enabled and configured{Colors.END}")
    print(f"  {Colors.GREEN}Unnecessary services disabled{Colors.END}")
    print(f"  {Colors.GREEN}Kernel hardening parameters applied{Colors.END}")
    print(f"  {Colors.GREEN}Password policies enforced{Colors.END}")
    print(f"  {Colors.GREEN}Extra users/groups removed{Colors.END}")
    print(f"  {Colors.GREEN}Logging and auditing enabled{Colors.END}")
    
    print(f"\n{Colors.YELLOW} IMPORTANT NOTES:{Colors.END}")
    print(f"  {Colors.YELLOW}- Make sure you have set up SSH keys before running this script!{Colors.END}")
    print(f"  {Colors.YELLOW}- Check UFW rules: sudo ufw status numbered{Colors.END}")
    print(f"  {Colors.YELLOW}- Check Fail2ban status: sudo fail2ban-client status sshd{Colors.END}")
    print(f"  {Colors.YELLOW}- Review SSH config: sudo nano /etc/ssh/sshd_config{Colors.END}")
    print(f"  {Colors.YELLOW}- To test, try SSH from a new connection.{Colors.END}")
    print(f"\n{Colors.GREEN} Your server is now hardened. Stay secure.{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")

def main():
    if os.geteuid() != 0:
        print(f"{Colors.RED}This script must be run as root (sudo).{Colors.END}")
        sys.exit(1)

    print(BANNER)

    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER} NEXHARDEN - UBUNTU HARDENING SCRIPT{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f" {Colors.CYAN}Date:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" {Colors.CYAN}Hostname:{Colors.END} {os.uname().nodename}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")

    print(f"\n{Colors.HEADER} PHASE 1: Pre-Hardening Security Scan{Colors.END}")
    print(f"{Colors.BOLD}{'-'*70}{Colors.END}")
    scanner = perform_security_scan()
    
    show_recommendations(scanner)
    
    if not get_user_confirmation():
        print(f"\n{Colors.YELLOW}Hardening skipped. Exiting...{Colors.END}")
        sys.exit(0)
    
    print(f"\n{Colors.HEADER} PHASE 2: Applying Hardening Measures{Colors.END}")
    print(f"{Colors.BOLD}{'-'*70}{Colors.END}")
    
    system_update()
    configure_firewall()
    secure_ssh()
    setup_fail2ban()
    disable_unnecessary_services()
    kernel_hardening()
    password_policy()
    remove_extra_users()
    setup_logging()

    print(f"\n{Colors.HEADER} PHASE 3: Post-Hardening Security Scan{Colors.END}")
    print(f"{Colors.BOLD}{'-'*70}{Colors.END}")
    after_scanner = perform_security_scan()

    final_report(scanner.get_score(), after_scanner.get_score())

if __name__ == "__main__":
    main()