# توثيق API شريان

العنوان المحلي: `http://127.0.0.1:8000`

يمكن فتح التوثيق التفاعلي من `/docs` أو `/redoc`.

## المصادقة

أرسل JWT في كل مسار محمي:

```http
Authorization: Bearer <access_token>
```

### الحسابات

| الطريقة | المسار | الحماية | الوصف |
|---|---|---|---|
| POST | `/api/auth/register` | عامة | إنشاء حساب |
| POST | `/api/auth/login` | عامة | تسجيل الدخول بصيغة form: `username`, `password` |
| GET | `/api/auth/me` | JWT | بيانات المستخدم الحالي |
| POST | `/api/auth/bootstrap-admin` | header سري | ترقية أول مستخدم إلى مشرف |

## المتبرعون والطلبات

| الطريقة | المسار | الحماية | الوصف |
|---|---|---|---|
| POST | `/api/donors/me` | JWT | إنشاء أو تحديث ملف المتبرع |
| GET | `/api/donors?blood_type=O%2B&city=كسلا` | عامة | البحث عن المتبرعين |
| POST | `/api/requests` | JWT | إنشاء طلب دم |
| GET | `/api/requests` | عامة | عرض الطلبات المفتوحة |
| PATCH | `/api/requests/{id}/cancel` | JWT | إلغاء طلب المستخدم |

## الرسائل والإشعارات

| الطريقة | المسار | الحماية | الوصف |
|---|---|---|---|
| POST | `/api/messages` | JWT | إرسال رسالة داخلية |
| GET | `/api/messages/{user_id}` | JWT | عرض المحادثة |
| GET | `/api/notifications` | JWT | آخر 50 إشعارًا |
| PATCH | `/api/notifications/{id}/read` | JWT | تحديد الإشعار كمقروء |

## المشرف والتقارير

كل المسارات التالية تتطلب JWT لمستخدم `is_admin=true`:

| الطريقة | المسار | الوصف |
|---|---|---|
| GET | `/api/admin/stats` | أرقام مختصرة |
| GET | `/api/admin/reports/overview` | تقرير حسب الحالة والفصيلة والمدينة |
| GET | `/api/admin/users` | قائمة المستخدمين |
| GET | `/api/admin/requests` | كل الطلبات |
| PATCH | `/api/admin/requests/{id}/status?status=fulfilled` | تحديث حالة الطلب |
| PATCH | `/api/admin/donors/{id}/availability?available=false` | تعطيل متبرع |
| DELETE | `/api/admin/users/{id}` | حذف مستخدم |
| DELETE | `/api/admin/donors/{id}` | حذف ملف متبرع |

## أمثلة

إنشاء طلب:

```json
{
  "patient_name": "Sara",
  "blood_type": "O+",
  "city": "Riyadh",
  "hospital": "Central Hospital",
  "units": 2,
  "urgent": true,
  "notes": "يرجى الحضور خلال ساعتين"
}
```

الردود المهمة: `201` للإنشاء، `401` لمصادقة غير صالحة، `403` لصلاحية ناقصة، `404` للمورد غير الموجود، و`422` لبيانات التحقق غير الصالحة.
