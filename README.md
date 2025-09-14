# WAFEye
Plugin-based Web Application Firewall (WAF) detection tool with passive and active fingerprinting support.

 🔥 WAFEye 👁️


    ██╗    ██╗ █████╗ ███████╗███████╗██╗   ██╗███████╗
    ██║    ██║██╔══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
    ██║ █╗ ██║███████║█████╗  █████╗   ╚████╔╝ █████╗  
    ██║███╗██║██╔══██║██╔══╝  ██╔══╝    ╚██╔╝  ██╔══╝  
    ╚███╔███╔╝██║  ██║██║     ███████╗   ██║   ███████╗
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝
    
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ▓ > Web Application Firewall Detection Tool ▓
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

## ⚡ **THE EYE THAT NEVER BLINKS** ⚡

> *"In the shadows of cyberspace, WAFEye watches... detecting the guardians before they detect you."*

WAFEye is a next-generation **Web Application Firewall Detection Framework** designed for penetration testers, bug bounty hunters, and security researchers who need to identify WAF systems protecting their targets.


## 🚀 **DEPLOYMENT**


git clone https://github.com/yourusername/WAFEye.git
cd WAFEye
pip3 install -r requirements.txt
python3 WAFEye.py --url https://target.com


### Stealth Mode
bash
# Basic reconnaissance
python3 WAFEye.py --url https://example.com

# Full spectrum scan
python3 WAFEye.py --url https://example.com --findall

# Active payload testing
python3 WAFEye.py --url https://example.com --active --scope full

# Aggressive testing with custom timing
python3 WAFEye.py --url https://example.com --active --aggressive 2.0






## ⚙️ **COMMAND LINE ARSENAL**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--url`        | Target URL (required)   | `--url https://example.com` |
| `--findall`    | Detect all WAF types    | `--findall`                 |
| `--active`     | Enable active testing   | `--active`                  |
| `--scope`      | Payload scope (50/full) | `--scope full`              |
| `--aggressive` | Delay between requests  | `--aggressive 1.5`          |



## 🎨 **TERMINAL EYE CANDY**

bash
[~] Loaded 167 WAFEye plugins.

[~] Sending normal request to https://target.com
[+] Normal request completed.

[~] Plugin detection initiated...
[+] WAF detected: CloudFlare
[+] WAF detected: ModSecurity  

✓ Detection completed!

## 📊 **BATTLE STATISTICS**



| Metric | Count |
|--------|-------|
| 🎯 **Detection Plugins**      | 167+ |
| ⚡ **WAF Vendors Supported**   | 50+ |
| 🔍 **Detection Methods**      | 6 |
| 🌐 **Tested Platforms**       | 1000+ |
| ⭐ **Community Contributors** | Growing |



## 📜 **LICENSE & LEGAL**

MIT License - Use responsibly, hack ethically.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
USE AT YOUR OWN RISK. ALWAYS OBTAIN PROPER AUTHORIZATION.


<div align="center">

### 🎭 *"The eye sees all, but reveals only what is necessary"*

**Made with 💀 by Security Researchers, for Security Researchers**

*[⚡ Star this repo if it helped you in your security journey! ⚡]*

</div>

## 🔥 **RECENT UPDATES**

- **v2.1** - Added 15+ new WAF detection plugins
- **v2.0** - Complete engine rewrite with improved accuracy  
- **v1.9** - Active attack simulation module
- **v1.8** - Matrix-style terminal interface
- **v1.7** - Multi-threading support for faster scans

*Stay tuned for more updates... 👁️*
