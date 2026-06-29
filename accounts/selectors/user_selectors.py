from accounts.models import CustomUser


# ==========================================
# GET USER BY EMAIL
# ==========================================
def get_user_by_email(email):
    return CustomUser.objects.filter(email=email).first()


# ==========================================
# CHECK EMAIL EXISTS
# ==========================================
def email_exists(email):
    return CustomUser.objects.filter(email=email).exists()


# ==========================================
# CHECK PHONE EXISTS
# ==========================================
def phone_exists(phone_number):
    return CustomUser.objects.filter(phone_number=phone_number).exists()