import os

from backend.auth import hash_password
from backend.database import SessionLocal
from backend.models import BloodRequest, BloodType, Donor, RequestStatus, User


def create_demo_data():
    if os.getenv("APP_ENV", "development").strip().lower() == "production":
        raise RuntimeError("Demo data seeding is disabled in production.")

    db = SessionLocal()

    demo_users = [
        {"full_name": "أحمد محمد علي", "email": "ahmed1@example.com", "password": "demo12345", "phone": "0910000001", "city": "المربعات الشعبي"},
        {"full_name": "صالح المرغني", "email": "saleh2@example.com", "password": "demo12345", "phone": "0910000002", "city": "المرغني"},
        {"full_name": "نبيل مكرم", "email": "nabil3@example.com", "password": "demo12345", "phone": "0910000003", "city": "مكرم"},
        {"full_name": "عمر بانت", "email": "omar4@example.com", "password": "demo12345", "phone": "0910000004", "city": "حي العرب"},
        {"full_name": "خالد سكة حديد", "email": "khalid5@example.com", "password": "demo12345", "phone": "0910000005", "city": "سكة حديد"},
        {"full_name": "فهد عبد الله", "email": "fahad6@example.com", "password": "demo12345", "phone": "0910000006", "city": "حي العمال"},
        {"full_name": "مصطفى حسن", "email": "mostafa7@example.com", "password": "demo12345", "phone": "0910000007", "city": "حي النور"},
        {"full_name": "ياسر آدم", "email": "yasser8@example.com", "password": "demo12345", "phone": "0910000008", "city": "حي السلام"},
        {"full_name": "طارق عثمان", "email": "tarek9@example.com", "password": "demo12345", "phone": "0910000009", "city": "حي الضباط"},
        {"full_name": "سامر النور", "email": "samer10@example.com", "password": "demo12345", "phone": "0910000010", "city": "كسلا"},
    ]

    donor_names = [u["full_name"] for u in demo_users]
    db.query(BloodRequest).delete()
    db.query(Donor).delete()
    db.query(User).delete()

    for item in demo_users:
        user = User(
            full_name=item["full_name"],
            email=item["email"],
            password_hash=hash_password(item["password"]),
            phone=item["phone"],
            city=item["city"],
            is_admin=item["email"] == "ahmed1@example.com",
            email_verified=True,
        )
        db.add(user)
    db.flush()

    users = db.query(User).order_by(User.id).all()
    donor_specs = [
        (users[0].id, BloodType.O_POSITIVE),
        (users[1].id, BloodType.A_NEGATIVE),
        (users[2].id, BloodType.B_POSITIVE),
        (users[3].id, BloodType.AB_POSITIVE),
        (users[4].id, BloodType.O_NEGATIVE),
        (users[5].id, BloodType.A_POSITIVE),
        (users[6].id, BloodType.B_NEGATIVE),
        (users[7].id, BloodType.AB_NEGATIVE),
        (users[8].id, BloodType.O_POSITIVE),
        (users[9].id, BloodType.B_POSITIVE),
    ]

    for user_id, blood in donor_specs:
        db.add(Donor(user_id=user_id, blood_type=blood, available=True))

    request_specs = [
        (users[5].id, "علي", BloodType.O_POSITIVE, "حي العمال", "مستشفى كسلا المركزي", 2, True, "حالة طارئة تحتاج إلى فصيلة O+ في حي العمال"),
        (users[0].id, "سارة", BloodType.A_NEGATIVE, "المربعات الشعبي", "مستشفى البشير", 1, False, "مطلوب متبرع فصيلة A- في المربعات الشعبي"),
        (users[1].id, "حسن", BloodType.B_POSITIVE, "المرغني", "مستشفى المدينة", 3, True, "تحتاج إلى 3 وحدات في المرغني"),
        (users[2].id, "لين", BloodType.AB_POSITIVE, "مكرم", "مستشفى النيل", 1, False, "مطلوب AB+ سريعًا في مكرم"),
        (users[3].id, "يوسف", BloodType.O_NEGATIVE, "حي العرب", "مستشفى وادي سبخ", 2, True, "فصيلة O- عاجلة جداً في حي العرب"),
    ]

    for requester_id, patient_name, blood_type, city, hospital, units, urgent, notes in request_specs:
        db.add(BloodRequest(
            requester_id=requester_id,
            patient_name=patient_name,
            blood_type=blood_type,
            city=city,
            hospital=hospital,
            units=units,
            urgent=urgent,
            notes=notes,
            status=RequestStatus.OPEN,
        ))

    db.commit()
    print("Demo data cleaned and rebuilt for KASSALA successfully.")
    print(f"Users: {db.query(User).count()}")
    print(f"Donors: {db.query(Donor).count()}")
    print(f"Requests: {db.query(BloodRequest).count()}")
    db.close()


if __name__ == "__main__":
    create_demo_data()
