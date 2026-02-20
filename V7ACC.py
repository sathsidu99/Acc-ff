#!/usr/bin/env python3

# DON'T CHANGE MY CREDIT 💳 


"""
KNX ALL-IN-ONE ACCOUNT GENERATOR + AUTO ACTIVATOR
Version 7.1 – Final Stable Build | Auto Folder Creation Enabled
"""

import hmac
import hashlib
import requests
import string
import random
import json
import codecs
import time
from datetime import datetime
import os
import sys
import base64
import signal
import threading
import psutil
import re
import subprocess
import importlib
import logging
import warnings
import urllib3
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# Try to import protobuf
try:
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder

    _sym_db = _symbol_database.Default()
    DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
        b'\n\x13MajorLoginRes.proto"\x87\x05\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\x05\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0c \x01(\x03\x12\x32\n\tblacklist\x18\r \x01(\x0b\x32\x1f.MajorLoginRes.BlacklistInfoRes\x12\x31\n\nqueue_info\x18\x0f \x01(\x0b\x32\x1d.MajorLoginRes.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x10 \x01(\t\x12\x15\n\rapp_server_id\x18\x11 \x01(\x03\x12\x0f\n\x07\x61no_url\x18\x12 \x01(\t\x12\x0f\n\x07ip_city\x18\x13 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x14 \x01(\t\x12\x0b\n\x03kts\x18\x15 \x01(\x03\x12\n\n\x02\x61k\x18\x16 \x01(\x0c\x12\x0b\n\x03\x61iv\x18\x17 \x01(\x0c\x1aQ\n\x10\x42lacklistInfoRes\x12\x12\n\nban_reason\x18\x01 \x01(\x05\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\x03\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\x03\x1a\x66\n\x0eLoginQueueInfo\x12\r\n\x05\x41llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\x03\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\x03\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\x62\x06proto3'
    )
    _globals = globals()
    _builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
    _builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MajorLoginRes_pb2', _globals)
    PROTOBUF_OK = True
except Exception as e:
    print(f"⚠️ Protobuf setup: {e}")
    PROTOBUF_OK = False
#######MISSING PACKS
# ================= AUTO REQUIREMENTS INSTALLER =================
import sys
import subprocess

REQUIRED_PACKAGES = [
    "requests",
    "pycryptodome",
    "colorama",
    "urllib3",
    "psutil",
    "protobuf",
    "flask",
    "pyfiglet"
]

def install_missing():
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            print(f"📦 Installing missing package: {pkg}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_missing()
# ===============================================================
# Install requirements
def install_requirements():
    required_packages = ['requests', 'pycryptodome', 'colorama', 'urllib3', 'psutil', 'protobuf']
    for package in required_packages:
        try:
            if package == 'pycryptodome':
                import Crypto
            elif package == 'protobuf':
                import google.protobuf
            else:
                importlib.import_module(package)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            except:
                return False
    return True

if not install_requirements():
    sys.exit("Error installing dependencies.")

from colorama import Fore, Style, init
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

init(autoreset=True)

# =============================================================================
# CONFIGURATION
# =============================================================================

EXIT_FLAG = False
SUCCESS_COUNTER = 0
TARGET_ACCOUNTS = 0
RARE_COUNTER = 0
COUPLES_COUNTER = 0
ACTIVATED_COUNTER = 0
FAILED_ACTIVATION_COUNTER = 0
RARITY_SCORE_THRESHOLD = 3
LOCK = threading.Lock()
AUTO_ACTIVATION_ENABLED = True

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(CURRENT_DIR, "KNX")
TOKENS_FOLDER = os.path.join(BASE_FOLDER, "TOKENS")
ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "ACCOUNTS")
RARE_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "RARE_ACCOUNTS")
COUPLES_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "COUPLES_ACCOUNTS")
GHOST_FOLDER = os.path.join(BASE_FOLDER, "GHOST")
GHOST_ACCOUNTS_FOLDER = os.path.join(GHOST_FOLDER, "ACCOUNTS")
GHOST_RARE_FOLDER = os.path.join(GHOST_FOLDER, "RARE_ACCOUNTS")
GHOST_COUPLES_FOLDER = os.path.join(GHOST_FOLDER, "COUPLES_ACCOUNTS")
ACTIVATED_FOLDER = os.path.join(BASE_FOLDER, "ACTIVATED")
FAILED_ACTIVATION_FOLDER = os.path.join(BASE_FOLDER, "FAILED_ACTIVATION")

# =============================================================================
# FORCE FOLDER CREATION - FIXED!
# =============================================================================

def force_create_folder(folder_path):
    """Force create folder - works even if path exists as file"""
    try:
        if os.path.exists(folder_path):
            if os.path.isfile(folder_path):
                try:
                    os.remove(folder_path)
                    print(f"🗑️ Removed file: {folder_path}")
                except Exception as e:
                    print(f"⚠️ Cannot remove file {folder_path}: {e}")
                    return False

        os.makedirs(folder_path, exist_ok=True)
        return os.path.isdir(folder_path)
    except PermissionError as e:
        print(f"🚫 Permission denied: {folder_path} - {e}")
        return False
    except Exception as e:
        print(f"⚠️ Folder error: {folder_path} - {e}")
        return False

def setup_all_folders():
    """Create all required folders at startup"""
    folders = [
        BASE_FOLDER, TOKENS_FOLDER, ACCOUNTS_FOLDER, RARE_ACCOUNTS_FOLDER,
        COUPLES_ACCOUNTS_FOLDER, GHOST_FOLDER, GHOST_ACCOUNTS_FOLDER,
        GHOST_RARE_FOLDER, GHOST_COUPLES_FOLDER, ACTIVATED_FOLDER,
        FAILED_ACTIVATION_FOLDER
    ]

    print("🔧 Creating folders...")
    failed = []
    for folder in folders:
        if not force_create_folder(folder):
            failed.append(folder)

    if failed:
        print(f"⚠️ Failed: {len(failed)} folders")
    else:
        print("✅ All folders ready!")
    return len(failed) == 0

setup_all_folders()

# =============================================================================
# ROBUST FILE OPERATIONS - FIXED!
# =============================================================================

def safe_json_save(filepath, data):
    """Safely save JSON with automatic folder creation"""
    try:
        # Create parent folder if needed
        parent = os.path.dirname(filepath)
        if parent and not os.path.isdir(parent):
            if not force_create_folder(parent):
                return False

        # Write to temp file then rename (atomic)
        temp = filepath + '.tmp'
        with open(temp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        if os.path.exists(filepath):
            os.replace(temp, filepath)
        else:
            os.rename(temp, filepath)
        return True
    except Exception as e:
        print(f"❌ Save failed: {filepath} - {e}")
        return False

def safe_json_load(filepath, default=None):
    """Safely load JSON"""
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default if default is not None else []

REGION_LANG = {"ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th", "BD": "bn", "PK": "ur", "TW": "zh", "CIS": "ru", "SAC": "es", "BR": "pt"}

ACTIVATION_REGIONS = {
    'IND': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin', 'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData', 'client_host': 'client.ind.freefiremobile.com'},
    'BD': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'},
    'PK': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'},
    'ID': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'},
    'TH': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.common.ggbluefox.com/GetLoginData', 'client_host': 'clientbp.common.ggbluefox.com'},
    'VN': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'},
    'ME': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'},
    'BR': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant', 'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin', 'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData', 'client_host': 'clientbp.ggblueshark.com'}
}

MAIN_HEX_KEY = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
API_POOL = [{"id": "100067", "key": bytes.fromhex(MAIN_HEX_KEY), "label": f"API {i:02d} ⚡"} for i in range(1, 8)]
GARENA = "S05Y"
FILE_LOCKS = {}
POTENTIAL_COUPLES = {}
COUPLES_LOCK = threading.Lock()

def get_file_lock(filename):
    if filename not in FILE_LOCKS:
        FILE_LOCKS[filename] = threading.Lock()
    return FILE_LOCKS[filename]

def get_random_color():
    return random.choice([Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTBLUE_EX, Fore.CYAN])

class Colors:
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL

def safe_exit(signum=None, frame=None):
    global EXIT_FLAG
    EXIT_FLAG = True
    print(f"\n{get_random_color()}{Colors.BRIGHT}🚨 Exiting...{Colors.RESET}")
    sys.exit(0)

signal.signal(signal.SIGINT, safe_exit)
signal.signal(signal.SIGTERM, safe_exit)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    c = get_random_color()
    width = shutil.get_terminal_size().columns

    banner = f"""
██╗  ██╗███╗   ██╗██╗  ██╗
██║ ██╔╝████╗  ██║╚██╗██╔╝
█████╔╝ ██╔██╗ ██║ ╚███╔╝ 
██╔═██╗ ██║╚██╗██║ ██╔██╗ 
██║  ██╗██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

{Fore.RED}[ KNX GEN-ACT ENGINE v7.1 ]{Colors.RESET}
{Fore.GREEN}All-In-One Generator + Auto Activator{Colors.RESET}
{Fore.CYAN}Force Directory System: ENABLED{Colors.RESET}
"""

    centered_banner = "\n".join(line.center(width) for line in banner.splitlines())
    print(f"{c}{Colors.BRIGHT}{centered_banner}{Colors.RESET}")

def print_success(m): print(f"{get_random_color()}{Colors.BRIGHT}✅ {m}{Colors.RESET}")
def print_error(m): print(f"{Fore.RED}{Colors.BRIGHT}❌ {m}{Colors.RESET}")
def print_warning(m): print(f"{Fore.YELLOW}{Colors.BRIGHT}⚠️ {m}{Colors.RESET}")
def print_rare(m): print(f"{Fore.LIGHTMAGENTA_EX}{Colors.BRIGHT}💎 {m}{Colors.RESET}")
def print_activation(m): print(f"{Fore.GREEN}{Colors.BRIGHT}🔥 {m}{Colors.RESET}")

# =============================================================================
# CRYPTO FUNCTIONS
# =============================================================================

def EnC_Vr(N):
    if N < 0: 
        return b''
    H = []
    while True:
        BesTo = N & 0x7F 
        N >>= 7
        if N: 
            BesTo |= 0x80
        H.append(BesTo)
        if not N: 
            break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet

def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    K = AES.new(key , AES.MODE_CBC , iv)
    R = K.encrypt(pad(Z , AES.block_size))
    return R

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)
            account_id = data.get('account_id') or data.get('external_id')
            if account_id:
                return str(account_id)
    except:
        pass
    return "N/A"

# =============================================================================
# RARITY & COUPLES DETECTION
# =============================================================================

ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4": [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3": [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5": [r"(12345|23456|34567|45678|56789)", 4],
    "SEQUENTIAL_4": [r"(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "PALINDROME_6": [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4": [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH": [r"(69|420|1337|007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QUADRUPLE_DIGITS": [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MIRROR_PATTERN_HIGH": [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED": [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO": [r"1618|0618", 3]
}

def check_account_rarity(account_data):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None, 0

    rarity_score = 0
    detected_patterns = []

    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        pattern = pattern_data[0]
        score = pattern_data[1]
        if re.search(pattern, account_id):
            rarity_score += score
            detected_patterns.append(rarity_type)

    account_id_digits = [int(d) for d in account_id if d.isdigit()]

    if len(set(account_id_digits)) == 1 and len(account_id_digits) >= 4:
        rarity_score += 5
        detected_patterns.append("UNIFORM_DIGITS")

    if len(account_id_digits) >= 4:
        differences = [account_id_digits[i+1] - account_id_digits[i] for i in range(len(account_id_digits)-1)]
        if len(set(differences)) == 1:
            rarity_score += 4
            detected_patterns.append("ARITHMETIC_SEQUENCE")

    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3
        detected_patterns.append("LOW_ACCOUNT_ID")

    if rarity_score >= RARITY_SCORE_THRESHOLD:
        reason = f"Account ID {account_id} - Score: {rarity_score} - Patterns: {', '.join(detected_patterns)}"
        return True, "RARE_ACCOUNT", reason, rarity_score

    return False, None, None, rarity_score

def check_account_couples(account_data, thread_id):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None

    with COUPLES_LOCK:
        for stored_id, stored_data in POTENTIAL_COUPLES.items():
            stored_account_id = stored_data.get('account_id', '')
            couple_found, reason = check_account_couple_patterns(account_id, stored_account_id)
            if couple_found:
                partner_data = stored_data
                del POTENTIAL_COUPLES[stored_id]
                return True, reason, partner_data

        POTENTIAL_COUPLES[account_id] = {
            'uid': account_data.get('uid', ''),
            'account_id': account_id,
            'name': account_data.get('name', ''),
            'password': account_data.get('password', ''),
            'region': account_data.get('region', ''),
            'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }

    return False, None, None

def check_account_couple_patterns(account_id1, account_id2):
    if account_id1 and account_id2 and abs(int(account_id1) - int(account_id2)) == 1:
        return True, f"Sequential Account IDs: {account_id1} & {account_id2}"

    if account_id1 == account_id2[::-1]:
        return True, f"Mirror Account IDs: {account_id1} & {account_id2}"

    if account_id1 and account_id2:
        sum_acc = int(account_id1) + int(account_id2)
        if sum_acc % 1000 == 0 or sum_acc % 10000 == 0:
            return True, f"Complementary sum: {account_id1} + {account_id2} = {sum_acc}"

    love_numbers = ['520', '521', '1314', '3344']
    for love_num in love_numbers:
        if love_num in account_id1 and love_num in account_id2:
            return True, f"Both contain love number: {love_num}"

    return False, None

def print_rarity_found(account_data, rarity_type, reason, rarity_score):
    print(f"\n{Fore.LIGHTMAGENTA_EX}{Colors.BRIGHT}💎 RARE ACCOUNT FOUND!{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}🎯 Type: {rarity_type}{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}⭐ Rarity Score: {rarity_score}{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}👤 Name: {account_data['name']}{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}🆔 UID: {account_data['uid']}{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}🎮 Account ID: {account_data.get('account_id', 'N/A')}{Colors.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}📝 Reason: {reason}{Colors.RESET}\n")

def print_couples_found(account1, account2, reason):
    print(f"\n{Fore.LIGHTCYAN_EX}{Colors.BRIGHT}💑 COUPLES ACCOUNT FOUND!{Colors.RESET}")
    print(f"{Fore.LIGHTCYAN_EX}📝 Reason: {reason}{Colors.RESET}")
    print(f"{Fore.LIGHTCYAN_EX}👤 Account 1: {account1['name']} (ID: {account1.get('account_id', 'N/A')}){Colors.RESET}")
    print(f"{Fore.LIGHTCYAN_EX}👤 Account 2: {account2['name']} (ID: {account2.get('account_id', 'N/A')}){Colors.RESET}\n")

# =============================================================================
# ACCOUNT GENERATION HELPERS
# =============================================================================

def generate_exponent_number():
    exponent_digits = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
    number = random.randint(1, 99999)
    number_str = f"{number:05d}"
    return ''.join(exponent_digits[digit] for digit in number_str)

def generate_random_name(base_name):
    return f"{base_name[:7]}{generate_exponent_number()}"

def generate_custom_password(prefix):
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(5))
    return f"{prefix}_CODEX_{random_part}"

def encode_string(original):
    keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
                 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {"open_id": original, "field_14": encoded}

def to_unicode_escaped(s):
    return ''.join(c if 32 <= ord(c) <= 126 else '\\u{:04x}'.format(ord(c)) for c in s)

def smart_delay():
    time.sleep(random.uniform(0.1, 0.3))

# =============================================================================
# AUTO ACTIVATION CLASS
# =============================================================================

class AutoActivator:
    def __init__(self, max_workers=5, turbo_mode=True):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        self.max_workers = max_workers
        self.turbo_mode = turbo_mode
        self.session = requests.Session()
        self.successful = 0
        self.failed = 0
        self.stats_lock = threading.Lock()
        self.stop_execution = False

    def encrypt_api(self, plain_text):
        try:
            plain_text = bytes.fromhex(plain_text)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            return None

    def parse_my_message(self, serialized_data):
        try:
            text = serialized_data.decode('utf-8', errors='ignore')
            jwt_start = text.find("eyJ")
            if jwt_start != -1:
                jwt_token = text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    jwt_token = jwt_token[:second_dot + 44]
                    return jwt_token, None, None
            return None, None, None
        except:
            return None, None, None

    def guest_token(self, uid, password, region='IND'):
        if self.stop_execution:
            return None, None

        region_config = ACTIVATION_REGIONS.get(region, ACTIVATION_REGIONS['IND'])
        url = region_config['guest_url']
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        for attempt in range(3):
            try:
                timeout = 8 if self.turbo_mode else 15
                response = self.session.post(url, data=data, timeout=timeout, verify=False)
                if response.status_code == 200:
                    data_json = response.json()
                    return data_json.get('access_token'), data_json.get('open_id')
                elif response.status_code == 429:
                    time.sleep(2 ** attempt)
            except Exception as e:
                pass
            if attempt < 2:
                time.sleep(1)
        return None, None

    def major_login(self, access_token, open_id, region='IND'):
        if self.stop_execution:
            return None

        region_config = ACTIVATION_REGIONS.get(region, ACTIVATION_REGIONS['IND'])
        url = region_config['major_login_url']
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
        }
        payload_template = bytes.fromhex(
            '1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3132302e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134'
        )
        OLD_OPEN_ID = b"996a629dbcdb3964be6b6978f5d814db"
        OLD_ACCESS_TOKEN = b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        payload = payload_template.replace(OLD_OPEN_ID, open_id.encode())
        payload = payload.replace(OLD_ACCESS_TOKEN, access_token.encode())
        encrypted_payload = self.encrypt_api(payload.hex())
        if not encrypted_payload:
            return None
        final_payload = bytes.fromhex(encrypted_payload)
        for attempt in range(3):
            try:
                timeout = 12 if self.turbo_mode else 18
                response = self.session.post(url, headers=headers, data=final_payload, verify=False, timeout=timeout)
                if response.status_code == 200 and len(response.content) > 0:
                    return response.content
            except:
                pass
            if attempt < 2:
                time.sleep(1)
        return None

    def GET_LOGIN_DATA(self, JWT_TOKEN, access_token, region='IND'):
        if self.stop_execution:
            return False

        region_config = ACTIVATION_REGIONS.get(region, ACTIVATION_REGIONS['IND'])
        url = region_config['get_login_data_url']
        client_host = region_config['client_host']

        try:
            token_payload_base64 = JWT_TOKEN.split('.')[1]
            token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
            decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
            decoded_payload = json.loads(decoded_payload)
            NEW_EXTERNAL_ID = decoded_payload['external_id']
            SIGNATURE_MD5 = decoded_payload['signature_md5']
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            payload = bytes.fromhex("1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3132302e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134")
            payload = payload.replace(b"2025-07-30 11:02:51", now.encode())
            payload = payload.replace(b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a", access_token.encode("UTF-8"))
            payload = payload.replace(b"996a629dbcdb3964be6b6978f5d814db", NEW_EXTERNAL_ID.encode("UTF-8"))
            payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
            PAYLOAD = payload.hex()
            PAYLOAD = self.encrypt_api(PAYLOAD)
            if not PAYLOAD:
                return False
            final_payload = bytes.fromhex(PAYLOAD)
        except:
            return False

        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': client_host,
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        for attempt in range(2):
            try:
                timeout = 8 if self.turbo_mode else 12
                response = self.session.post(url, headers=headers, data=final_payload, verify=False, timeout=timeout)
                if response.status_code == 200:
                    return True
            except:
                pass
            if attempt < 1:
                time.sleep(1)
        return False

    def activate_account(self, account_data):
        """Activate a single account"""
        uid = account_data['uid']
        password = account_data['password']
        region = account_data.get('region', 'IND')

        if region not in ACTIVATION_REGIONS:
            region = 'IND'

        access_token, open_id = self.guest_token(uid, password, region)
        if not access_token or not open_id:
            return False

        major_login_response = self.major_login(access_token, open_id, region)
        if not major_login_response:
            return False

        jwt_token, key, iv = self.parse_my_message(major_login_response)
        if not jwt_token:
            return False

        activation_success = self.GET_LOGIN_DATA(jwt_token, access_token, region)
        return activation_success

# Global activator
auto_activator = AutoActivator(max_workers=5, turbo_mode=True)

# =============================================================================
# ACCOUNT CREATION FUNCTIONS
# =============================================================================

def create_acc(region, account_name, password_prefix, session, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        current_api = random.choice(API_POOL)
        app_id = current_api["id"]
        secret_key = current_api["key"]

        password = generate_custom_password(password_prefix)
        data = f"password={password}&client_type=2&source=2&app_id={app_id}"
        message = data.encode('utf-8')
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

        url = f"https://{app_id}.connect.garena.com/oauth/guest/register"
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
            "Authorization": "Signature " + signature,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        response = session.post(url, headers=headers, data=data, timeout=15, verify=False)
        response.raise_for_status()

        if 'uid' in response.json():
            uid = response.json()['uid']
            print_success(f"Guest created via {current_api['label']}: {uid}")
            smart_delay()
            return token(uid, password, region, account_name, password_prefix, current_api, session, is_ghost)
        return None
    except Exception as e:
        smart_delay()
        return None

def token(uid, password, region, account_name, password_prefix, api_config, session, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        app_id = api_config["id"]
        secret_key = api_config["key"]

        url = f"https://{app_id}.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": f"{app_id}.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        }
        body = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": secret_key,
            "client_id": app_id
        }

        response = session.post(url, headers=headers, data=body, timeout=15, verify=False)
        response.raise_for_status()

        if 'open_id' in response.json():
            open_id = response.json()['open_id']
            access_token = response.json()["access_token"]

            result = encode_string(open_id)
            field = to_unicode_escaped(result['field_14'])
            field = codecs.decode(field, 'unicode_escape').encode('latin1')
            print_success(f"Token granted for: {uid}")
            smart_delay()
            return Major_Regsiter(access_token, open_id, field, uid, password, region, account_name, password_prefix, api_config, session, is_ghost)
        return None
    except Exception as e:
        smart_delay()
        return None

def select_veteran(region, jwt_token, session):
    try:
        if region.upper() in ["ME", "TH"]:
            url = "https://clientbp.common.ggbluefox.com/ActiveBeginnerGuide"
        else:
            url = "https://clientbp.ggblueshark.com/ActiveBeginnerGuide"

        fields = {1: 3}
        proto_data = CrEaTe_ProTo(fields)
        encrypted_data = encrypt_api(proto_data.hex())
        payload = bytes.fromhex(encrypted_data)

        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'Authorization': f"Bearer {jwt_token}",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }

        response = session.post(url, data=payload, headers=headers, verify=False, timeout=15)
        return response.status_code == 200
    except:
        return False

def Major_Regsiter(access_token, open_id, field, uid, password, region, account_name, password_prefix, api_config, session, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorRegister"
        else:
            if region.upper() in ["ME", "TH"]:
                url = "https://loginbp.common.ggbluefox.com/MajorRegister"
            else:
                url = "https://loginbp.ggblueshark.com/MajorRegister"

        name = generate_random_name(account_name)

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",   
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME", "TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4."
        }

        lang_code = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")
        payload = {
            1: name,
            2: access_token,
            3: open_id,
            5: 102000007,
            6: 4,
            7: 1,
            13: 1,
            14: field,
            15: lang_code,
            16: 1,
            17: 1
        }

        payload_bytes = CrEaTe_ProTo(payload)
        encrypted_payload = E_AEs(payload_bytes.hex())

        response = session.post(url, headers=headers, data=encrypted_payload, verify=False, timeout=15)

        if response.status_code == 200:
            print_success(f"MajorRegister successful: {name}")

            login_result = perform_major_login(uid, password, access_token, open_id, region, session, is_ghost)
            account_id = login_result.get("account_id", "N/A")
            jwt_token = login_result.get("jwt_token", "")

            if not is_ghost and jwt_token and account_id != "N/A" and region.upper() != "BR":
                region_bound = force_region_binding(region, jwt_token, session)
                if region_bound:
                    print_success(f"Region {region} bound successfully!")

                veteran_selected = select_veteran(region, jwt_token, session)
                if veteran_selected:
                    print_success(f"🔥 Veteran Mode Selected (Tutorial Skipped)")

            return {
                "uid": uid, 
                "password": password, 
                "name": name, 
                "region": "GHOST" if is_ghost else region, 
                "status": "success",
                "account_id": account_id,
                "jwt_token": jwt_token,
                "api_label": api_config["label"]
            }
        return None
    except Exception as e:
        smart_delay()
        return None

def perform_major_login(uid, password, access_token, open_id, region, session, is_ghost=False):
    try:
        lang = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")

        payload_parts = [
            b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
            lang.encode("ascii"),
            b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        ]

        payload = b''.join(payload_parts)

        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
        elif region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/MajorLogin"
        else:
            url = "https://loginbp.ggblueshark.com/MajorLogin"

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME", "TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1"
        }

        data = payload
        data = data.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
        data = data.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())

        d = encrypt_api(data.hex())
        final_payload = bytes.fromhex(d)

        response = session.post(url, headers=headers, data=final_payload, verify=False, timeout=15)

        if response.status_code == 200 and len(response.text) > 10:
            jwt_start = response.text.find("eyJ")
            if jwt_start != -1:
                jwt_token = response.text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    jwt_token = jwt_token[:second_dot + 44]
                    account_id = decode_jwt_token(jwt_token)
                    return {"account_id": account_id, "jwt_token": jwt_token}

        return {"account_id": "N/A", "jwt_token": ""}
    except:
        return {"account_id": "N/A", "jwt_token": ""}

def force_region_binding(region, jwt_token, session):
    try:
        if region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/ChooseRegion"
        else:
            url = "https://loginbp.ggblueshark.com/ChooseRegion"

        region_code = "RU" if region.upper() == "CIS" else region.upper()

        fields = {1: region_code}
        proto_data = CrEaTe_ProTo(fields)
        encrypted_data = encrypt_api(proto_data.hex())
        payload = bytes.fromhex(encrypted_data)

        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'Authorization': f"Bearer {jwt_token}",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }

        response = session.post(url, data=payload, headers=headers, verify=False, timeout=15)
        return response.status_code == 200
    except:
        return False

# =============================================================================
# AUTO ACTIVATION INTEGRATION
# =============================================================================

def auto_activate_account(account_data):
    """Automatically activate account after generation"""
    global ACTIVATED_COUNTER, FAILED_ACTIVATION_COUNTER

    if not AUTO_ACTIVATION_ENABLED:
        return False

    try:
        print_activation(f"Auto-activating: {account_data['uid']}")

        activator = AutoActivator(max_workers=1, turbo_mode=True)
        success = activator.activate_account(account_data)

        with LOCK:
            if success:
                ACTIVATED_COUNTER += 1
                print_activation(f"✅ Activated! Total: {ACTIVATED_COUNTER}")
                save_activated_account(account_data)
            else:
                FAILED_ACTIVATION_COUNTER += 1
                print_error(f"❌ Failed! Total failed: {FAILED_ACTIVATION_COUNTER}")
                save_failed_activation(account_data)

        return success
    except Exception as e:
        print_error(f"Activation error: {e}")
        with LOCK:
            FAILED_ACTIVATION_COUNTER += 1
        return False

# =============================================================================
# FILE SAVING FUNCTIONS - FIXED WITH FORCE FOLDER CREATION
# =============================================================================

def save_activated_account(account_data):
    """Save successfully activated account"""
    try:
        region = account_data.get('region', 'UNKNOWN')
        filename = os.path.join(ACTIVATED_FOLDER, f"activated-{region}.json")

        entry = {
            'uid': account_data['uid'],
            'password': account_data['password'],
            'account_id': account_data.get('account_id', 'N/A'),
            'name': account_data['name'],
            'region': region,
            'activated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        file_lock = get_file_lock(filename)
        with file_lock:
            accounts_list = safe_json_load(filename, [])
            accounts_list.append(entry)
            safe_json_save(filename, accounts_list)
    except Exception as e:
        print_error(f"Error saving activated: {e}")

def save_failed_activation(account_data):
    """Save failed activation account"""
    try:
        region = account_data.get('region', 'UNKNOWN')
        filename = os.path.join(FAILED_ACTIVATION_FOLDER, f"failed-{region}.json")

        entry = {
            'uid': account_data['uid'],
            'password': account_data['password'],
            'account_id': account_data.get('account_id', 'N/A'),
            'name': account_data['name'],
            'region': region,
            'failed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        file_lock = get_file_lock(filename)
        with file_lock:
            accounts_list = safe_json_load(filename, [])
            accounts_list.append(entry)
            safe_json_save(filename, accounts_list)
    except Exception as e:
        print_error(f"Error saving failed: {e}")

def save_jwt_token(account_data, jwt_token, region, is_ghost=False):
    try:
        if is_ghost:
            token_filename = os.path.join(GHOST_FOLDER, "tokens-ghost.json")
        else:
            token_filename = os.path.join(TOKENS_FOLDER, f"tokens-{region}.json")

        token_entry = {
            'uid': account_data["uid"],
            'account_id': account_data.get("account_id", "N/A"),
            'jwt_token': jwt_token,
            'name': account_data["name"],
            'password': account_data["password"],
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': "KNX" if is_ghost else region,
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(token_filename)
        with file_lock:
            tokens_list = safe_json_load(token_filename, [])
            existing_ids = [t.get('account_id') for t in tokens_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                tokens_list.append(token_entry)
                safe_json_save(token_filename, tokens_list)
                return True
        return False
    except Exception as e:
        print_error(f"Error saving JWT: {e}")
        return False

def save_normal_account(account_data, region, is_ghost=False):
    try:
        if is_ghost:
            account_filename = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
        else:
            account_filename = os.path.join(ACCOUNTS_FOLDER, f"accounts-{region}.json")

        account_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "KNX" if is_ghost else region,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(account_filename)
        with file_lock:
            accounts_list = safe_json_load(account_filename, [])
            existing_ids = [acc.get('account_id') for acc in accounts_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                accounts_list.append(account_entry)
                safe_json_save(account_filename, accounts_list)
                return True
        return False
    except Exception as e:
        print_error(f"Error saving account: {e}")
        return False

def save_rare_account(account_data, rarity_type, reason, rarity_score, is_ghost=False):
    try:
        if is_ghost:
            rare_filename = os.path.join(GHOST_RARE_FOLDER, "rare-ghost.json")
        else:
            region = account_data.get('region', 'UNKNOWN')
            rare_filename = os.path.join(RARE_ACCOUNTS_FOLDER, f"rare-{region}.json")

        rare_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "KNX" if is_ghost else account_data.get('region', 'UNKNOWN'),
            'rarity_type': rarity_type,
            'rarity_score': rarity_score,
            'reason': reason,
            'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': account_data.get('jwt_token', ''),
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(rare_filename)
        with file_lock:
            rare_list = safe_json_load(rare_filename, [])
            existing_ids = [acc.get('account_id') for acc in rare_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                rare_list.append(rare_entry)
                safe_json_save(rare_filename, rare_list)
                return True
        return False
    except Exception as e:
        print_error(f"Error saving rare: {e}")
        return False

def save_couples_account(account1, account2, reason, is_ghost=False):
    try:
        if is_ghost:
            couples_filename = os.path.join(GHOST_COUPLES_FOLDER, "couples-ghost.json")
        else:
            region = account1.get('region', 'UNKNOWN')
            couples_filename = os.path.join(COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json")

        couples_entry = {
            'couple_id': f"{account1.get('account_id', 'N/A')}_{account2.get('account_id', 'N/A')}",
            'account1': {
                'uid': account1["uid"],
                'password': account1["password"],
                'account_id': account1.get("account_id", "N/A"),
                'name': account1["name"],
                'thread_id': account1.get('thread_id', 'N/A')
            },
            'account2': {
                'uid': account2["uid"],
                'password': account2["password"],
                'account_id': account2.get("account_id", "N/A"),
                'name': account2["name"],
                'thread_id': account2.get('thread_id', 'N/A')
            },
            'reason': reason,
            'region': "KNX" if is_ghost else account1.get('region', 'UNKNOWN'),
            'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        file_lock = get_file_lock(couples_filename)
        with file_lock:
            couples_list = safe_json_load(couples_filename, [])
            existing_couples = [c.get('couple_id') for c in couples_list]
            if couples_entry['couple_id'] not in existing_couples:
                couples_list.append(couples_entry)
                safe_json_save(couples_filename, couples_list)
                return True
        return False
    except Exception as e:
        print_error(f"Error saving couples: {e}")
        return False

# =============================================================================
# MAIN WORKER
# =============================================================================

def print_registration_status(count, total, name, uid, password, account_id, region, is_ghost=False, api_label="Unknown"):
    print(f"{get_random_color()}{Colors.BRIGHT}📝 Registration {count}/{total}{Colors.RESET}")
    print(f"{Fore.CYAN}🚀 {api_label}{Colors.RESET}")
    print(f"{get_random_color()}👤 Name: {name}{Colors.RESET}")
    print(f"{get_random_color()}🆔 UID: {uid}{Colors.RESET}")
    print(f"{get_random_color()}🎮 Account ID: {account_id}{Colors.RESET}")
    print(f"{get_random_color()}🔑 Password: {password}{Colors.RESET}")
    if is_ghost:
        print(f"{get_random_color()}🌍 Mode: {Fore.LIGHTMAGENTA_EX}GHOST Mode{Colors.RESET}")
    else:
        print(f"{get_random_color()}🌍 Region: {region}{Colors.RESET}")
    print()

def generate_single_account(region, account_name, password_prefix, total_accounts, thread_id, session, is_ghost=False):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER
    if EXIT_FLAG:
        return None

    with LOCK:
        if SUCCESS_COUNTER >= total_accounts:
            return None

    account_result = create_acc(region, account_name, password_prefix, session, is_ghost)
    if not account_result:
        return None

    account_id = account_result.get("account_id", "N/A")
    jwt_token = account_result.get("jwt_token", "")
    api_label = account_result.get("api_label", "Unknown")
    account_result['thread_id'] = thread_id

    with LOCK:
        SUCCESS_COUNTER += 1
        current_count = SUCCESS_COUNTER

    print_registration_status(current_count, total_accounts, account_result["name"], 
                            account_result["uid"], account_result["password"], account_id, region, is_ghost, api_label)

    is_rare, rarity_type, rarity_reason, rarity_score = check_account_rarity(account_result)
    if is_rare:
        with LOCK:
            RARE_COUNTER += 1
        print_rarity_found(account_result, rarity_type, rarity_reason, rarity_score)
        save_rare_account(account_result, rarity_type, rarity_reason, rarity_score, is_ghost)
        print_success(f"💎 Rare saved! (Total: {RARE_COUNTER})")

    is_couple, couple_reason, partner_data = check_account_couples(account_result, thread_id)
    if is_couple and partner_data:
        with LOCK:
            COUPLES_COUNTER += 1
        print_couples_found(account_result, partner_data, couple_reason)
        save_couples_account(account_result, partner_data, couple_reason, is_ghost)
        print_success(f"💑 Couples saved! (Total: {COUPLES_COUNTER})")

    if is_ghost:
        save_normal_account(account_result, "GHOST", is_ghost=True)
        if jwt_token:
            save_jwt_token(account_result, jwt_token, "GHOST", is_ghost=True)
    else:
        save_normal_account(account_result, region)
        if jwt_token:
            save_jwt_token(account_result, jwt_token, region)

        # AUTO ACTIVATION
        if AUTO_ACTIVATION_ENABLED:
            auto_activate_account(account_result)

    return {"account": account_result}

def worker(region, account_name, password_prefix, total_accounts, thread_id, is_ghost=False):
    thread_color = get_random_color()
    print(f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} started{Colors.RESET}")

    session = requests.Session()
    accounts_generated = 0

    while not EXIT_FLAG:
        with LOCK:
            if SUCCESS_COUNTER >= total_accounts:
                break

        result = generate_single_account(region, account_name, password_prefix, total_accounts, thread_id, session, is_ghost)
        if result:
            accounts_generated += 1

        time.sleep(random.uniform(0.1, 0.5))

    print(f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} finished: {accounts_generated} accounts{Colors.RESET}")

# =============================================================================
# MENU & MAIN
# =============================================================================

def generate_accounts_flow():
    global SUCCESS_COUNTER, TARGET_ACCOUNTS, RARE_COUNTER, COUPLES_COUNTER
    global ACTIVATED_COUNTER, FAILED_ACTIVATION_COUNTER, AUTO_ACTIVATION_ENABLED, RARITY_SCORE_THRESHOLD

    clear_screen()
    display_banner()

    cpu_count = psutil.cpu_count()
    recommended_threads = min(cpu_count * 2, 10) 

    print(f"{get_random_color()}{Colors.BRIGHT}🌍 Available Regions:{Colors.RESET}")

    regions_to_show = [r for r in REGION_LANG.keys() if r != "BR"]

    for i, region in enumerate(regions_to_show, 1):
        print(f"{get_random_color()}{i}) {region} ({REGION_LANG[region]}){Colors.RESET}")

    print(f"{get_random_color()}{len(regions_to_show)+1}) {Fore.LIGHTMAGENTA_EX}GHOST Mode{Colors.RESET}")
    print(f"{get_random_color()}00) {Fore.YELLOW}Back{Colors.RESET}")
    print(f"{get_random_color()}000) {Fore.RED}Exit{Colors.RESET}")

    while True:
        try:
            choice = input(f"\n{get_random_color()}{Colors.BRIGHT}🎯 Choose: {Colors.RESET}").strip().upper()

            if choice == "00":
                return
            elif choice == "000":
                print(f"\n{get_random_color()}{Colors.BRIGHT}👋 Goodbye!{Colors.RESET}")
                sys.exit(0)
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(regions_to_show):
                    selected_region = regions_to_show[choice_num - 1]
                    is_ghost = False
                    break
                elif choice_num == len(regions_to_show) + 1:
                    selected_region = "BR"
                    is_ghost = True
                    break
            elif choice in regions_to_show:
                selected_region = choice
                is_ghost = False
                break
            elif choice == "GHOST":
                selected_region = "BR"
                is_ghost = True
                break
            else:
                print_error("Invalid option")
        except KeyboardInterrupt:
            safe_exit()

    clear_screen()
    display_banner()

    if is_ghost:
        print(f"{Fore.LIGHTMAGENTA_EX}{Colors.BRIGHT}🌍 GHOST MODE{Colors.RESET}")
    else:
        print(f"{get_random_color()}{Colors.BRIGHT}🌍 Region: {selected_region}{Colors.RESET}")

    account_count = 999999999

    account_name = "KNX"

    password_prefix = "KNX"

    rarity_threshold = 4
     
    AUTO_ACTIVATION_ENABLED = True

    thread_count = 55

    clear_screen()
    display_banner()

    print(f"{get_random_color()}{Colors.BRIGHT}🚀 Starting...{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}🎯 Target: {account_count}{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}⚡ Speed Mode: ON{Colors.RESET}")
    if not is_ghost:
        print(f"{get_random_color()}{Colors.BRIGHT}🔥 Auto-Activation: {'ON' if AUTO_ACTIVATION_ENABLED else 'OFF'}{Colors.RESET}")
    print(f"\n{get_random_color()}{Colors.BRIGHT}⏳ Starting in 3 seconds...{Colors.RESET}")
    time.sleep(3)

    SUCCESS_COUNTER = 0
    TARGET_ACCOUNTS = account_count
    RARE_COUNTER = 0
    COUPLES_COUNTER = 0
    ACTIVATED_COUNTER = 0
    FAILED_ACTIVATION_COUNTER = 0
    start_time = time.time()
    threads = []

    print(f"\n{get_random_color()}{Colors.BRIGHT}🚀 Starting with {thread_count} threads...{Colors.RESET}\n")

    for i in range(thread_count):
        t = threading.Thread(target=worker, args=(selected_region, account_name, password_prefix, account_count, i+1, is_ghost))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(1)
            with LOCK:
                current_count = SUCCESS_COUNTER
                activated_count = ACTIVATED_COUNTER
                failed_act_count = FAILED_ACTIVATION_COUNTER

            percent = (current_count / account_count) if account_count > 0 else 0
            filled = int(25 * percent)
            bar = '█' * filled + '░' * (25 - filled)

            print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════╗")
            print(f"║ {Fore.YELLOW}⚡ KNX GENARATOR ✅{Fore.CYAN}                           ║")
            print(f"╠══════════════════════════════════════════════════╣")
            print(f"║ {Fore.YELLOW}📊 PROGRESS: {Fore.CYAN}[{bar}] {percent*100:.1f}%{Fore.CYAN}   ║")
            print(f"║ {Fore.MAGENTA}💎 RARE: {RARE_COUNTER:<5} {Fore.BLUE}💑 COUPLES: {COUPLES_COUNTER:<5}{Fore.CYAN}     ║")
            print(f"║ {Fore.GREEN}✅ GENERATED: {current_count}/{account_count}{Fore.CYAN}                    ║")
            if AUTO_ACTIVATION_ENABLED and not is_ghost:
                print(f"║ {Fore.GREEN}🔥 ACTIVATED: {activated_count:<5} {Fore.RED}❌ FAILED: {failed_act_count:<5}{Fore.CYAN}  ║")
            print(f"╚══════════════════════════════════════════════════╝\n")

            if current_count >= account_count:
                break
    except KeyboardInterrupt:
        print_warning("Interrupted!")
        EXIT_FLAG = True

    for t in threads:
        t.join(timeout=3)

    elapsed = time.time() - start_time

    print(f"\n{get_random_color()}{Colors.BRIGHT}🎉 Completed!{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}📊 Generated: {SUCCESS_COUNTER}/{account_count}{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}💎 Rare: {RARE_COUNTER}{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}💑 Couples: {COUPLES_COUNTER}{Colors.RESET}")
    if AUTO_ACTIVATION_ENABLED and not is_ghost:
        print(f"{Fore.GREEN}{Colors.BRIGHT}🔥 Activated: {ACTIVATED_COUNTER}{Colors.RESET}")
        print(f"{Fore.RED}{Colors.BRIGHT}❌ Failed: {FAILED_ACTIVATION_COUNTER}{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}⏱️ Time: {elapsed:.2f}s{Colors.RESET}")
    print(f"{get_random_color()}{Colors.BRIGHT}⚡ Speed: {SUCCESS_COUNTER/elapsed:.2f} acc/s{Colors.RESET}")

    input(f"\n{get_random_color()}{Colors.BRIGHT}⏎ Press Enter...{Colors.RESET}")

def view_saved_accounts():
    clear_screen()
    display_banner()
    print(f"{get_random_color()}{Colors.BRIGHT}📁 Saved Accounts{Colors.RESET}")

    folders = [ACCOUNTS_FOLDER, ACTIVATED_FOLDER, RARE_ACCOUNTS_FOLDER, COUPLES_ACCOUNTS_FOLDER]
    total = 0

    for folder in folders:
        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.endswith('.json')]
            for file in files:
                filepath = os.path.join(folder, file)
                try:
                    data = safe_json_load(filepath, [])
                    print(f"{get_random_color()}📄 {folder}/{file}: {len(data)} accounts{Colors.RESET}")
                    total += len(data)
                except:
                    pass

    print(f"\n{get_random_color()}{Colors.BRIGHT}📊 Total: {total} accounts{Colors.RESET}")
    input(f"\n{get_random_color()}{Colors.BRIGHT}⏎ Press Enter...{Colors.RESET}")

def main_menu():
    while True:
        clear_screen()
        display_banner()

        generate_accounts_flow()

        print(f"\n{get_random_color()}{Colors.BRIGHT}♻ Auto cycle complete! Restarting...{Colors.RESET}")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        safe_exit()
    except Exception as e:
        print_error(f"Error: {e}")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)