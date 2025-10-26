# 🌐 دليل النشر على الإنترنت
# Deployment Guide

---

## 📌 ملخص الخيارات

| المنصة | التكلفة | الموثوقية | سهولة الاستخدام |
|--------|--------|----------|-----------------|
| **Render** | مجاني | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Railway** | مجاني (محدود) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Replit** | مجاني | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **VPS (DigitalOcean)** | $4/شهر | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 الطريقة الأولى: Render (الأفضل والأسهل)

### المميزات:
- ✅ مجاني تماماً
- ✅ لا يتطلب بطاقة ائتمان
- ✅ يعمل 24/7
- ✅ سهل جداً

### الخطوات:

#### 1. إعداد GitHub

**أ) إنشاء حساب GitHub:**
- اذهب إلى [github.com](https://github.com)
- اضغط "Sign up"
- أكمل التسجيل

**ب) إنشاء مستودع جديد:**
- انقر على "+" في الزاوية العلوية اليمنى
- اختر "New repository"
- اسم المستودع: `telegram-bot`
- اختر "Public"
- اضغط "Create repository"

**ج) رفع الملفات:**

```bash
# انتقل إلى مجلد البوت
cd /home/ubuntu/telegram_bot

# هيّئ git
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"

# أضف جميع الملفات
git add .

# أنشئ commit
git commit -m "Initial commit - Telegram Customer Service Bot"

# غيّر اسم الفرع إلى main
git branch -M main

# أضف الـ remote (استبدل YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git

# ارفع الملفات
git push -u origin main
```

#### 2. إعداد Render

**أ) إنشاء حساب Render:**
- اذهب إلى [render.com](https://render.com)
- اضغط "Get Started"
- اختر "Sign up with GitHub"
- وافق على الأذونات

**ب) نشر البوت:**
- انقر على "New +"
- اختر "Web Service"
- اختر مستودع `telegram-bot`
- اضغط "Connect"

**ج) إعدادات الخدمة:**

| الحقل | القيمة |
|------|--------|
| **Name** | `telegram-bot` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python3 bot.py` |
| **Instance Type** | `Free` |

**د) إضافة متغيرات البيئة:**
- انقر على "Environment"
- أضف متغير جديد:
  - **Key:** `BOT_TOKEN`
  - **Value:** `7968719347:AAEUloIBy_gvD2cmE9vrdiHcZwClldYZ-Xk`

**هـ) النشر:**
- اضغط "Create Web Service"
- انتظر حتى تظهر رسالة "Your service is live"

✅ **تم! البوت الآن يعمل على الإنترنت!**

---

## 🚂 الطريقة الثانية: Railway

### الخطوات:

1. **إنشاء حساب:**
   - اذهب إلى [railway.app](https://railway.app)
   - اضغط "Login with GitHub"

2. **نشر المشروع:**
   - اضغط "New Project"
   - اختر "Deploy from GitHub repo"
   - اختر مستودع `telegram-bot`

3. **إضافة متغيرات البيئة:**
   - اذهب إلى "Variables"
   - أضف: `BOT_TOKEN=your_token_here`

4. **النشر:**
   - سيبدأ Railway في النشر تلقائياً

---

## 🔄 الطريقة الثالثة: Replit

### الخطوات:

1. **إنشاء حساب:**
   - اذهب إلى [replit.com](https://replit.com)
   - اضغط "Sign up"

2. **استيراد المشروع:**
   - اضغط "Create"
   - اختر "Import from GitHub"
   - ألصق رابط مستودعك

3. **تشغيل البوت:**
   - اضغط "Run"
   - سيبدأ البوت في التشغيل

---

## 💻 الطريقة الرابعة: VPS (DigitalOcean)

### المميزات:
- ✅ تحكم كامل
- ✅ أداء عالي
- ✅ رخيص ($4/شهر)

### الخطوات:

#### 1. إنشاء droplet:

- اذهب إلى [digitalocean.com](https://digitalocean.com)
- اضغط "Create" ثم "Droplets"
- اختر:
  - **Image:** Ubuntu 22.04
  - **Size:** Basic ($4/month)
  - **Region:** الأقرب لك
- اضغط "Create Droplet"

#### 2. الاتصال بالـ Droplet:

```bash
# استبدل IP_ADDRESS برقم IP الخاص بك
ssh root@IP_ADDRESS
```

#### 3. تثبيت المتطلبات:

```bash
# تحديث النظام
apt update && apt upgrade -y

# تثبيت Python و pip
apt install -y python3 python3-pip git

# استنساخ المستودع
git clone https://github.com/YOUR_USERNAME/telegram-bot.git
cd telegram-bot

# تثبيت المكتبات
pip install -r requirements.txt
```

#### 4. تشغيل البوت في الخلفية:

**الطريقة الأولى: استخدام screen:**

```bash
screen -S telegram_bot
python3 bot.py

# للخروج: Ctrl+A ثم D
```

**الطريقة الثانية: استخدام systemd (أفضل):**

```bash
# إنشاء ملف الخدمة
sudo nano /etc/systemd/system/telegram-bot.service
```

أضف المحتوى التالي:

```ini
[Unit]
Description=Telegram Customer Service Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram-bot
ExecStart=/usr/bin/python3 /root/telegram-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

ثم شغّل:

```bash
# تفعيل الخدمة
sudo systemctl enable telegram-bot

# بدء الخدمة
sudo systemctl start telegram-bot

# التحقق من الحالة
sudo systemctl status telegram-bot
```

---

## 🔄 تحديث البوت

### على Render:

1. عدّل الملفات في مستودع GitHub
2. ارفع التغييرات:
   ```bash
   git add .
   git commit -m "Update bot"
   git push
   ```
3. Render سيعيد النشر تلقائياً

### على VPS:

```bash
cd telegram-bot
git pull
# أعد تشغيل الخدمة إذا لزم الأمر
sudo systemctl restart telegram-bot
```

---

## 📊 مراقبة البوت

### على Render:

- اذهب إلى لوحة التحكم
- اختر خدمتك
- اعرض السجلات (Logs)

### على VPS:

```bash
# عرض السجلات
sudo journalctl -u telegram-bot -f

# أو استخدم screen
screen -r telegram_bot
```

---

## 🆘 استكشاف الأخطاء

### المشكلة: "Failed to connect"

**الحل:**
1. تحقق من Token
2. تحقق من الإنترنت
3. أعد النشر

### المشكلة: "ModuleNotFoundError"

**الحل:**
```bash
pip install -r requirements.txt
```

### المشكلة: البوت يتوقف بعد فترة

**الحل:**
- تأكد من أن الخدمة مفعلة
- استخدم `Restart=always` في systemd
- تحقق من السجلات

---

## 💡 نصائح مهمة

✅ **افعل:**
- استخدم `.env` لمتغيرات البيئة
- احفظ Token في متغيرات البيئة فقط
- راقب السجلات بانتظام
- أعد النشر بعد التحديثات

❌ **لا تفعل:**
- لا تكتب Token في الكود
- لا تشارك Token مع أحد
- لا تستخدم أجهزة ضعيفة

---

## 📞 الدعم

- 📖 [توثيق Render](https://render.com/docs)
- 📖 [توثيق Railway](https://docs.railway.app)
- 📖 [توثيق DigitalOcean](https://docs.digitalocean.com)

---

**اختر الطريقة التي تناسبك وابدأ الآن!** 🚀

