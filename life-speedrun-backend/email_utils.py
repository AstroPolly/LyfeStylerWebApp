# email_utils.py
def send_verification_email(email: str, code: str):
    # В консоли покажем код (для разработки)
    print(f"\n📧 MOCK EMAIL to {email}")
    print(f"🔑 Your verification code: {code}")
    print("✅ In production, this would be sent via SMTP.\n")
    return True