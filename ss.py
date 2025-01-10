from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# إعداد متغيرات API
API_KEY = "67daafd60774c736da43970e78d889cb"
API_URL = "https://mandovd.com/api/v2"

# الصفحة الرئيسية (واجهة بسيطة لإضافة طلب جديد)
@app.route('/')
def home():
    return """
    <h1>طلب جديد</h1>
    <form action="/send_order" method="post">
        <label>رقم الخدمة:</label><br>
        <input type="text" name="service" value="7726"><br>
        <label>الرابط:</label><br>
        <input type="text" name="link" value=""><br>
        <label>الكمية:</label><br>
        <input type="text" name="quantity" value="10"><br>
        <button type="submit">إرسال الطلب</button>
    </form>
    """

# دالة لإرسال طلب جديد إلى الـ API
@app.route('/send_order', methods=['POST'])
def send_order():
    # الحصول على القيم المدخلة من المستخدم
    service = request.form.get('service')
    link = request.form.get('link')
    quantity = request.form.get('quantity')

    # إعداد البيانات لإرسالها إلى API
    payload = {
        "key": API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }

    try:
        # إرسال الطلب إلى API
        response = requests.post(API_URL, data=payload)

        # التحقق من نجاح الطلب
        if response.ok:
            result = response.json()
            if "order" in result:
                return f"<h2>تم إنشاء الطلب بنجاح! رقم الطلب: {result['order']}</h2>"
            else:
                return f"<h2>فشل إنشاء الطلب. استجابة API: {result}</h2>"
        else:
            # في حالة وجود خطأ HTTP
            return f"<h2>خطأ في الاتصال: {response.status_code}. التفاصيل: {response.text}</h2>"
    except Exception as e:
        # عرض رسالة خطأ في حالة حدوث استثناء
        return f"<h2>حدث خطأ أثناء معالجة الطلب: {e}</h2>"

if __name__ == "__main__":
    # تشغيل التطبيق
    app.run(host="0.0.0.0", port=5000)
