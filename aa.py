from flask import Flask, request, render_template_string
from TikTokApi import TikTokApi

app = Flask(__name__)

def get_related_videos(video_url, num_videos=10):
    # قم بإنشاء كائن من API
    api = TikTokApi.get_instance()

    # استخراج معرف الفيديو من الرابط
    try:
        video_id = video_url.split("/video/")[1].split("?")[0]
    except IndexError:
        return "خطأ: الرابط غير صحيح."

    try:
        # جلب الفيديو الأصلي باستخدام الفيديو ID
        original_video = api.get_video_by_id(video_id)

        # استخراج الوسوم أو الكلمات المفتاحية المرتبطة بالفيديو
        hashtags = [hashtag['hashtagName'] for hashtag in original_video['itemInfo']['itemStruct']['textExtra']]

        # الآن استخدم هذه الوسوم للبحث عن مقاطع فيديو مشابهة
        related_videos = api.search_hashtags(hashtags, count=num_videos)

        # جمع روابط الفيديوهات الجديدة
        video_links = [f"https://www.tiktok.com/@{video['author']['uniqueId']}/video/{video['id']}" for video in related_videos]

        return video_links
    except Exception as e:
        return f"حدث خطأ: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        related_videos = get_related_videos(video_url)

        if isinstance(related_videos, str):  # إذا كانت النتيجة عبارة عن رسالة خطأ
            return render_template_string("""
                <h1>البحث عن فيديوهات مشابهة</h1>
                <form method="post">
                    <label for="video_url">أدخل رابط الفيديو:</label><br>
                    <input type="text" id="video_url" name="video_url" required><br><br>
                    <button type="submit">البحث</button>
                </form>
                <h2>{{ related_videos }}</h2>
            """, related_videos=related_videos)

        return render_template_string("""
            <h1>البحث عن فيديوهات مشابهة</h1>
            <form method="post">
                <label for="video_url">أدخل رابط الفيديو:</label><br>
                <input type="text" id="video_url" name="video_url" required><br><br>
                <button type="submit">البحث</button>
            </form>
            <h2>الفيديوهات المشابهة:</h2>
            <ul>
                {% for link in related_videos %}
                    <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
                {% endfor %}
            </ul>
        """, related_videos=related_videos)

    return render_template_string("""
        <h1>البحث عن فيديوهات مشابهة</h1>
        <form method="post">
            <label for="video_url">أدخل رابط الفيديو:</label><br>
            <input type="text" id="video_url" name="video_url" required><br><br>
            <button type="submit">البحث</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
