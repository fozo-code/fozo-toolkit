#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import secrets
import shutil
import socket
import string
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime

VERSION = "1.0.0"
APP_NAME = "FOZO Toolkit"

def clear():
    os.system("clear")

def pause():
    input("\nاضغط Enter للرجوع للقائمة...")

def banner():
    print("\033[1;36m")
    print("  ███████╗ ██████╗ ███████╗ ██████╗ ")
    print("  ██╔════╝██╔═══██╗╚══███╔╝██╔═══██╗")
    print("  █████╗  ██║   ██║  ███╔╝ ██║   ██║")
    print("  ██╔══╝  ██║   ██║ ███╔╝  ██║   ██║")
    print("  ██║    ╚██████╔╝███████╗╚██████╔╝")
    print("  ╚═╝     ╚═════╝ ╚══════╝ ╚═════╝ ")
    print("\033[0m")
    print(f"  {APP_NAME} v{VERSION} | Termux toolkit\n")

def system_info():
    clear()
    banner()
    print("=== معلومات النظام ===")
    print("النظام:", sys.platform)
    print("Python:", sys.version.split()[0])
    print("المجلد الحالي:", os.getcwd())
    print("المساحة:")
    try:
        usage = shutil.disk_usage(os.path.expanduser("~"))
        print(f"  الإجمالي: {usage.total // (1024**3)} GB")
        print(f"  المستخدم: {usage.used // (1024**3)} GB")
        print(f"  المتاح:   {usage.free // (1024**3)} GB")
    except OSError:
        print("  تعذر قراءة المساحة.")
    print("اسم الجهاز:", socket.gethostname())
    pause()

def password_generator():
    clear()
    banner()
    try:
        length = int(input("طول كلمة المرور (8-128): ").strip())
        if not 8 <= length <= 128:
            print("اختار طولًا من 8 إلى 128.")
            pause()
            return
    except ValueError:
        print("اكتب رقمًا صحيحًا.")
        pause()
        return
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    print("\nكلمة المرور:", password)
    print("نصيحة: استخدم كلمة مختلفة لكل حساب واحفظها في مدير كلمات مرور.")
    pause()

def text_tools():
    clear()
    banner()
    print("1) Base64 ترميز")
    print("2) Base64 فك الترميز")
    print("3) SHA-256 بصمة النص")
    choice = input("\nاختيارك: ").strip()
    value = input("اكتب النص: ")
    try:
        if choice == "1":
            print("\nالنتيجة:", base64.b64encode(value.encode()).decode())
        elif choice == "2":
            print("\nالنتيجة:", base64.b64decode(value.encode(), validate=True).decode())
        elif choice == "3":
            print("\nSHA-256:", hashlib.sha256(value.encode()).hexdigest())
        else:
            print("اختيار غير صحيح.")
    except (ValueError, UnicodeDecodeError):
        print("تعذر التحويل؛ تأكد من النص.")
    pause()

def make_qr():
    clear()
    banner()
    try:
        import qrcode
    except ImportError:
        print("مكتبة QR غير مثبتة.")
        print("نفّذ: pip install qrcode[pil]")
        pause()
        return
    value = input("اكتب نصًا أو رابطًا: ").strip()
    if not value:
        print("النص فارغ.")
        pause()
        return
    filename = "fozo-qr.png"
    qrcode.make(value).save(filename)
    print(f"تم حفظ QR في: {os.path.abspath(filename)}")
    print("تقدر تلاقيه في المجلد الحالي.")
    pause()

def install_qr():
    clear()
    banner()
    print("سيتم تثبيت مكتبة إنشاء QR باستخدام pip.")
    if input("متأكد؟ (y/N): ").strip().lower() == "y":
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode[pil]"], check=False)
    pause()

def git_status():
    clear()
    banner()
    if not shutil.which("git"):
        print("Git غير مثبت. نفّذ: pkg install git")
        pause()
        return
    path = input("مسار المشروع (Enter للمجلد الحالي): ").strip() or "."
    result = subprocess.run(["git", "-C", os.path.expanduser(path), "status", "--short", "--branch],
                            text=True, capture_output=True)
    if result.returncode:
        print("تعذر قراءة حالة Git:")
        print(result.stderr.strip() or "تأكد أن المسار مشروع Git.")
    else:
        print(result.stdout.strip() or "المشروع نظيف ولا توجد تغييرات.")
    pause()

def dns_lookup():
    clear()
    banner()
    host = input("اسم النطاق (مثال: example.com): ").strip()
    if not host or "/" in host or " " in host:
        print("اكتب اسم نطاق صحيحًا.")
        pause()
        return
    try:
        records = socket.getaddrinfo(host, None)
        addresses = sorted({item[4][0] for item in records})
        print("\nعناوين IP:")
        for address in addresses:
            print(" -", address)
    except socket.gaierror as exc:
        print("فشل DNS:", exc)
    pause()

def public_ip():
    clear()
    banner()
    print("جاري محاولة معرفة عنوان IP العام من خدمة خارجية...")
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=8) as response:
            ip = response.read(100).decode().strip()
        print("عنوان IP العام:", ip)
    except Exception:
        print("تعذر الاتصال بالخدمة. تحقق من الإنترنت وحاول لاحقًا.")
    pause()

def help_menu():
    clear()
    banner()
    print("الأوامر:")
    print("  fozo        تشغيل القائمة التفاعلية")
    print("  fozo --help عرض هذه المساعدة")
    print("\nالأدوات تعمل محليًا ما عدا الاستعلام عن IP العام الذي يتصل بخدمة خارجية.")
    print("لا تستخدم فحوص الشبكات إلا على أنظمة تملكها أو لديك إذن بفحصها.")
    pause()

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(f"{APP_NAME} v{VERSION}")
        print("Run: fozo")
        return
    while True:
        clear()
        banner()
        print("  1) معلومات النظام")
        print("  2) توليد كلمة مرور قوية")
        print("  3) أدوات النصوص (Base64 / SHA-256)")
        print("  4) إنشاء QR Code")
        print("  5) حالة مشروع Git")
        print("  6) فحص DNS لنطاق")
        print("  7) معرفة IP العام")
        print("  0) خروج")
        choice = input("\n  اختر رقمًا: ").strip()
        if choice == "1":
            system_info()
        elif choice == "2":
            password_generator()
        elif choice == "3":
            text_tools()
        elif choice == "4":
            make_qr()
        elif choice == "5":
            git_status()
        elif choice == "6":
            dns_lookup()
        elif choice == "7":
            public_ip()
        elif choice == "0":
            print("مع السلامة!")
            break
        else:
            print("اختيار غير صحيح.")
            input("اضغط Enter...")

if __name__ == "__main__":
    main()
