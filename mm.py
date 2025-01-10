import requests
from flask import Flask, request

app = Flask(__name__)

# إعداد متغيرات API
API_KEY = "67daafd60774c736da43970e78d889cb"
API_URL = "https://mandovd.com/api/v2"

# الصفحة الرئيسية (واجهة لإضافة 10 روابط منفصلة)
@app.route('/')
def home():
    return """
    <h1>إضافة طلبات جديدة</h1>
    <form action="/send_orders" method="post">
        <label>رقم الخدمة:</label><br>
        <input type="text" name="service" value="7726"><br>
        <label>الكمية لكل طلب:</label><br>
        <input type="text" name="quantity" value="10"><br>
        <h3>الروابط:</h3>
        <label>رابط 1:</label><br>
        <input type="text" name="link1"><br>
        <label>رابط 2:</label><br>
        <input type="text" name="link2"><br>
        <label>رابط 3:</label><br>
        <input type="text" name="link3"><br>
        <label>رابط 4:</label><br>
        <input type="text" name="link4"><br>
        <label>رابط 5:</label><br>
        <input type="text" name="link5"><br>
        <label>رابط 6:</label><br>
        <input type="text" name="link6"><br>
        <label>رابط 7:</label><br>
        <input type="text" name="link7"><br>
        <label>رابط 8:</label><br>
        <input type="text" name="link8"><br>
        <label>رابط 9:</label><br>
        <input type="text" name="link9"><br>
        <label>رابط 10:</label><br>
        <input type="text" name="link10"><br><br>
        <button type="submit">إرسال الطلبات</button>
    </form>
    """

# دالة لإرسال الطلبات باستخدام 10 روابط منفصلة
@app.route('/send_orders', methods=['POST'])
def send_orders():
    # الحصول على القيم المدخلة من المستخدم
    service = request.form.get('service')
    quantity = request.form.get('quantity')

    # جمع الروابط من النموذج
    links = [
        request.form.get(f'link{i}') for i in range(1, 11)
    ]

    # التأكد من وجود روابط صالحة
    valid_links = [link for link in links if link]  # حذف الروابط الفارغة
    if len(valid_links) < 1:
        return "<h2>يرجى إدخال رابط واحد على الأقل.</h2>"

    # قائمة لتخزين نتائج الطلبات
    orders = []

    try:
        # إرسال الطلبات باستخدام الروابط المدخلة
        for i, link in enumerate(valid_links):
            payload = {
                "key": API_KEY,
                "action": "add",
                "service": service,
                "link": link.strip(),
                "quantity": quantity
            }
            response = requests.post(API_URL, data=payload)
            if response.ok:
                result = response.json()
                if "order" in result:
                    orders.append(f"طلب {i + 1}: تم بنجاح! رقم الطلب: {result['order']}")
                else:
                    orders.append(f"طلب {i + 1}: فشل. استجابة API: {result}")
            else:
                orders.append(f"طلب {i + 1}: خطأ HTTP - {response.status_code}: {response.text}")

        # عرض النتائج بعد الانتهاء
        orders_html = "<br>".join(orders)
        return f"<h2>تم إرسال الطلبات</h2><p>{orders_html}</p>"

    except Exception as e:
        # عرض رسالة خطأ في حالة حدوث استثناء
        return f"<h2>حدث خطأ أثناء معالجة الطلبات: {e}</h2>"

if __name__ == "__main__":
    # تشغيل التطبيق
    app.run(host="0.0.0.0", port=5000)
