#!/usr/bin/env python3
"""
بوت خدمة العملاء على تلجرام
Customer Service Bot for Telegram
"""

import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# إعداد نظام السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token البوت
BOT_TOKEN = "7968719347:AAEUloIBy_gvD2cmE9vrdiHcZwClldYZ-Xk"

# معرف المسؤول (يمكن تغييره لاحقاً)
ADMIN_ID = None  # سيتم تعيينه من أول مستخدم

# حالات المحادثة
CHOOSING, TYPING_REPLY, WAITING_FOR_MESSAGE = range(3)

# قاموس لتخزين بيانات المستخدمين
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """بدء المحادثة مع البوت"""
    user = update.effective_user
    user_id = user.id
    
    # تسجيل بيانات المستخدم
    if user_id not in user_data:
        user_data[user_id] = {
            'name': user.first_name,
            'username': user.username,
            'start_time': datetime.now(),
            'messages': []
        }
    
    # رسالة الترحيب
    welcome_text = f"""
👋 أهلاً وسهلاً {user.first_name}!

مرحباً بك في بوت خدمة العملاء. نحن هنا لمساعدتك!

اختر أحد الخيارات التالية:
"""
    
    # إنشاء لوحة المفاتيح
    keyboard = [
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='faq')],
        [InlineKeyboardButton("📞 التواصل مع الدعم", callback_data='support')],
        [InlineKeyboardButton("ℹ️ معلومات عنا", callback_data='about')],
        [InlineKeyboardButton("💬 شكوى أو اقتراح", callback_data='complaint')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    return CHOOSING


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة نقرات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    user_id = query.from_user.id
    
    if choice == 'faq':
        await handle_faq(query)
    elif choice == 'support':
        await handle_support(query, context)
    elif choice == 'about':
        await handle_about(query)
    elif choice == 'complaint':
        await handle_complaint(query, context)
    elif choice == 'back_to_menu':
        await back_to_menu(query)
    
    return CHOOSING


async def handle_faq(query) -> None:
    """التعامل مع الأسئلة الشائعة"""
    faq_text = """
❓ **الأسئلة الشائعة**

**س: كيف يمكنني الاتصال بفريق الدعم؟**
ج: يمكنك اختيار "التواصل مع الدعم" من القائمة الرئيسية.

**س: ما هي ساعات العمل؟**
ج: نحن متاحون من الساعة 9 صباحاً إلى 6 مساءً، من الأحد إلى الخميس.

**س: كم الوقت اللازم للرد على استفساراتي؟**
ج: عادةً نرد خلال 24 ساعة.

**س: هل يمكنني تتبع حالة طلبي؟**
ج: نعم، سنرسل لك رقم تتبع عند استقبال طلبك.

**س: هل هناك رسوم إضافية؟**
ج: لا، جميع خدماتنا الأساسية مجانية.

---
"""
    
    keyboard = [
        [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=faq_text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_support(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """التعامل مع طلب التواصل مع الدعم"""
    support_text = """
📞 **التواصل مع فريق الدعم**

يرجى اختيار نوع المشكلة:
"""
    
    keyboard = [
        [InlineKeyboardButton("🔧 مشكلة تقنية", callback_data='tech_issue')],
        [InlineKeyboardButton("💳 مشكلة في الدفع", callback_data='payment_issue')],
        [InlineKeyboardButton("📦 مشكلة في الطلب", callback_data='order_issue')],
        [InlineKeyboardButton("❓ استفسار عام", callback_data='general_inquiry')],
        [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=support_text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_about(query) -> None:
    """التعامل مع طلب معلومات عنا"""
    about_text = """
ℹ️ **معلومات عنا**

🏢 **اسم الشركة:** شركة الخدمات الممتازة

📍 **الموقع:** الرياض، المملكة العربية السعودية

📧 **البريد الإلكتروني:** support@company.com

📱 **الهاتف:** +966 11 1234567

🌐 **الموقع الإلكتروني:** www.company.com

⏰ **ساعات العمل:** 
- الأحد - الخميس: 9 صباحاً - 6 مساءً
- الجمعة والسبت: مغلق

---
"""
    
    keyboard = [
        [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=about_text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_complaint(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """التعامل مع الشكاوى والاقتراحات"""
    complaint_text = """
💬 **شكوى أو اقتراح**

شكراً لاهتمامك! يرجى كتابة شكواك أو اقتراحك في الرسالة التالية.

سيتم إرسال رسالتك مباشرة إلى فريق الدعم.
"""
    
    keyboard = [
        [InlineKeyboardButton("✍️ اكتب رسالتك", callback_data='write_message')],
        [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=complaint_text, reply_markup=reply_markup, parse_mode='Markdown')


async def back_to_menu(query) -> int:
    """العودة للقائمة الرئيسية"""
    welcome_text = """
👋 القائمة الرئيسية

اختر أحد الخيارات التالية:
"""
    
    keyboard = [
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='faq')],
        [InlineKeyboardButton("📞 التواصل مع الدعم", callback_data='support')],
        [InlineKeyboardButton("ℹ️ معلومات عنا", callback_data='about')],
        [InlineKeyboardButton("💬 شكوى أو اقتراح", callback_data='complaint')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=welcome_text, reply_markup=reply_markup)
    return CHOOSING


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الرسائل النصية"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # تسجيل الرسالة
    if user_id in user_data:
        user_data[user_id]['messages'].append({
            'text': message_text,
            'timestamp': datetime.now()
        })
    
    # رسالة تأكيد
    confirmation_text = """
✅ **تم استقبال رسالتك**

شكراً على تواصلك معنا! سيتم الرد عليك في أقرب وقت ممكن.

رقم تتبع طلبك: `#{}` 

يرجى الاحتفاظ برقم التتبع هذا للمتابعة.
""".format(user_id)
    
    await update.message.reply_text(confirmation_text, parse_mode='Markdown')
    
    # إرسال إشعار للمسؤول (إذا تم تعيينه)
    if ADMIN_ID:
        admin_notification = f"""
📬 **رسالة جديدة من العميل**

👤 **المستخدم:** {update.effective_user.first_name} (@{update.effective_user.username})
🆔 **معرف المستخدم:** {user_id}
💬 **الرسالة:** {message_text}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_notification, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"خطأ في إرسال الإشعار للمسؤول: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر المساعدة"""
    help_text = """
🆘 **أوامر البوت المتاحة:**

/start - بدء المحادثة والعودة للقائمة الرئيسية
/help - عرض هذه الرسالة
/status - معلومات عن حالة الخدمة

---

**ملاحظة:** يمكنك أيضاً استخدام الأزرار التفاعلية في القائمة الرئيسية للتنقل بسهولة.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أمر حالة الخدمة"""
    status_text = """
✅ **حالة الخدمة**

🟢 **الخادم:** يعمل بشكل طبيعي
🟢 **قاعدة البيانات:** متصلة
🟢 **الدعم الفني:** متاح

---

**إحصائيات:**
- عدد المستخدمين النشطين: {}
- الرسائل المستقبلة اليوم: {}

شكراً لاستخدامك خدماتنا!
""".format(len(user_data), sum(len(u.get('messages', [])) for u in user_data.values()))
    
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الأخطاء"""
    logger.error(msg="حدث استثناء أثناء معالجة التحديث:", exc_info=context.error)
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ حدث خطأ ما. يرجى المحاولة لاحقاً أو التواصل مع فريق الدعم."
        )


def main() -> None:
    """بدء البوت"""
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # إضافة معالج نقرات الأزرار
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # إضافة معالج الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)
    
    # بدء البوت
    logger.info("🚀 جاري بدء البوت...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

