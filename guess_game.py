# -*- coding: utf-8 -*-
"""
پروژه ۱ کارگاه کامپیوتر: گسترش بازی حدس اعداد

امکانات:
  ۱) عدد مخفی تصادفی بین ۱ تا ۱۰۰ و حداکثر ۵ فرصت
  ۲) نمایش شماره تلاش و جان باقی‌مانده
  ۳) راهنمای هوشمند (خیلی نزدیک / نزدیک / خیلی دور) همراه با جهت
  ۴) رتبه‌بندی بر اساس تعداد تلاش در صورت برد
  ۵) نمایش عدد مخفی در صورت باخت
  ۶) امکان بازی مجدد
  ۷) اعتبارسنجی ورودی (ورودی نامعتبر فرصتی کم نمی‌کند)
"""

import random

# ---------------- تنظیمات بازی ----------------
MIN_NUMBER = 1        # کمترین عدد ممکن
MAX_NUMBER = 100      # بیشترین عدد ممکن
MAX_ATTEMPTS = 5      # تعداد فرصت‌ها

NEAR_LIMIT = 5        # اختلاف تا ۵  ← «خیلی نزدیکی!»
MEDIUM_LIMIT = 15     # اختلاف تا ۱۵ ← «نزدیکی، ولی هنوز فاصله داری!»
                      # اختلاف بیشتر از ۱۵ ← «خیلی دوری!»

# رتبه بر اساس شماره تلاشی که در آن عدد درست حدس زده شده
RANKS = {
    1: "نمونه‌ای!",
    2: "بسیار خوبی!",
    3: "خوب",
    4: "قبول",
    5: "با شانس بردی!",
}

# برای نمایش اعداد با ارقام فارسی
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(number):
    """عدد را با ارقام فارسی برمی‌گرداند (فقط برای نمایش)."""
    return str(number).translate(PERSIAN_DIGITS)


def normalize_text(text):
    """حذف فاصله‌های اضافه و یکسان‌سازی حروف عربی (ي، ك) با فارسی (ی، ک)."""
    return text.strip().lower().replace("ي", "ی").replace("ك", "ک")


def get_guess():
    """
    تا وقتی کاربر یک عدد صحیح معتبر بین ۱ تا ۱۰۰ وارد نکرده، دوباره می‌پرسد.
    ورودی نامعتبر به‌عنوان حدس حساب نمی‌شود و فرصتی کم نمی‌کند.
    """
    while True:
        text = input(f"یک عدد بین {fa(MIN_NUMBER)} تا {fa(MAX_NUMBER)} وارد کن: ").strip()

        if text == "":
            print("خطا: چیزی وارد نکردی! لطفاً یک عدد وارد کن.")
            continue

        try:
            # int() ارقام فارسی مثل «۴۲» را هم درست می‌خواند
            guess = int(text)
        except ValueError:
            print("خطا: ورودی نامعتبر است! فقط عدد صحیح وارد کن (حروف و متن قبول نیست).")
            continue

        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            print(f"خطا: عدد باید بین {fa(MIN_NUMBER)} تا {fa(MAX_NUMBER)} باشد!")
            continue

        return guess


def closeness_hint(guess, secret):
    """بر اساس اختلاف حدس با عدد مخفی، میزان نزدیکی را برمی‌گرداند."""
    difference = abs(guess - secret)
    if difference <= NEAR_LIMIT:
        return "خیلی نزدیکی!"
    elif difference <= MEDIUM_LIMIT:
        return "نزدیکی، ولی هنوز فاصله داری!"
    else:
        return "خیلی دوری!"


def direction_hint(guess, secret):
    """جهت درست حدس بعدی را مشخص می‌کند."""
    if guess > secret:
        return "کوچک‌تر وارد کن."
    else:
        return "بزرگ‌تر وارد کن."


def play_round():
    """یک دور کامل بازی را اجرا می‌کند."""
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)

    print("\n" + "-" * 40)
    print(f"یک عدد بین {fa(MIN_NUMBER)} تا {fa(MAX_NUMBER)} انتخاب کردم.")
    print(f"تو {fa(MAX_ATTEMPTS)} فرصت داری تا آن را حدس بزنی.")
    print("-" * 40)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        lives_left = MAX_ATTEMPTS - attempt + 1

        print(f"\nتلاش {fa(attempt)} از {fa(MAX_ATTEMPTS)}")
        print(f"جان باقی‌مانده: {fa(lives_left)}")

        guess = get_guess()

        # حدس درست ← برد و نمایش رتبه
        if guess == secret:
            print(f"\nآفرین! عدد {fa(secret)} را در تلاش {fa(attempt)} درست حدس زدی. برنده شدی!")
            print(f"رتبه تو: {RANKS[attempt]}")
            return

        # حدس غلط ← راهنمای نزدیکی + جهت
        if attempt < MAX_ATTEMPTS:
            print(f"{closeness_hint(guess, secret)} {direction_hint(guess, secret)}")

    # اگر حلقه تمام شد یعنی هر ۵ حدس غلط بوده ← باخت (بدون رتبه)
    print("\nمتأسفانه فرصت‌هایت تمام شد و باختی!")
    print(f"عدد مخفی {fa(secret)} بود.")


def ask_play_again():
    """از کاربر می‌پرسد که می‌خواهد دوباره بازی کند یا نه."""
    yes_answers = ("بله", "بلی", "آره", "اره", "ب", "y", "yes")
    no_answers = ("خیر", "نه", "نخیر", "خ", "n", "no")

    while True:
        answer = normalize_text(input("\nمی‌خواهی دوباره بازی کنی؟ (بله/خیر): "))
        if answer in yes_answers:
            return True
        if answer in no_answers:
            return False
        print("لطفاً فقط «بله» یا «خیر» وارد کن.")


def main():
    print("=" * 40)
    print("        بازی حدس اعداد")
    print("=" * 40)

    while True:
        play_round()
        if not ask_play_again():
            print("\nممنون که بازی کردی! خداحافظ.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # اگر کاربر با Ctrl+C برنامه را ببندد، بدون پیام خطا خارج می‌شویم
        print("\n\nبازی متوقف شد. خداحافظ!")
