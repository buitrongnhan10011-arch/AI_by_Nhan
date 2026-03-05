from flask import Flask, render_template, request, jsonify
import re
import unicodedata
import random

app = Flask(__name__)

# ==============================
# Hàm bỏ dấu tiếng Việt
# ==============================
def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# ==============================
# REGEX
# ==============================

pattern_beo = re.compile(r"\bbiet\s*danh(\s*cua)?\s*(beo|bell)\b")
pattern_tuan = re.compile(r"\bbiet\s*danh(\s*cua)?\s*(tuan|turkey|ga\s*tay|gatay)\b")
pattern_bin = re.compile(r"\bbiet\s*danh(\s*cua)?\s*(bin|binsa|pansa|binsa\s*hevibom|pansa\s*hevibom)\b")

pattern_song_bat_on = re.compile(r"\bbai\s*hat.*bat\s*on\b")
pattern_event_bin = re.compile(r"\b(su\s*kien).*(bin|binsa)\b")

pattern_img_tuan = re.compile(r"\banh(\s*cua)?\s*tuan\b")
pattern_img_beo = re.compile(r"\banh(\s*cua)?\s*beo\b")
pattern_img_hoang = re.compile(r"\banh(\s*cua)?\s*(hoang|lalang|la\s*lang)\b")

# ====== BỔ SUNG ẢNH BIN/BINSA (KHÔNG ẢNH HƯỞNG LOGIC CŨ) ======
pattern_img_bin = re.compile(r"\banh(\s*cua)?\s*(bin|binsa)\b")

pattern_img_money = re.compile(r"\banh(\s*cua)?\s*money\b")

pattern_video_bin = re.compile(r"\bvideo(\s*cua)?\s*(bin|binsa)\b")

pattern_video_turkey = re.compile(
    r"\bvideo(\s*cua)?\s*(tuan|turkey|tuantay|tuan\s*tay|tuan\s*ga\s*tay)\b"
)

pattern_video_beovatuan = re.compile(r"\bbeo\s*va\s*tuan\s*thich\b")

pattern_video_ringbell = re.compile(r"\bvideo\s*ring\s*the\s*golden\s*bell\b")

pattern_video_khilo = re.compile(
    r"\bvideo(\s*cua)?\s*(khi|hoang|lalang|la\s*lang)\b"
)

pattern_quote_baton = re.compile(r"\bnhung\s*cau\s*noi\s*noi\s*tieng\s*trong\s*nhom\s*bat\s*on\b")

pattern_thanksgiving = re.compile(
    r"\ble\s*(ta\s*on|tuan|tuan\s*tay|ga\s*tay|thanksgiving)\b"
)

pattern_top_banchim = re.compile(r"\btop\s*ban\s*chim\b")

pattern_random_song = re.compile(r"\bchon\s*ngau\s*nhien\s*1\s*bai\s*hat\b")

pattern_bin_giong = re.compile(
    r"\b(bin|binsa)\s*giong\s*cau\s*thu\s*nao\b"
)

# ==============================
# Chatbot xử lý
# ==============================

def chatbot_response(text):
    text = text.lower()
    text_no_accent = remove_accents(text)

    # ===== BIN GIỐNG CẦU THỦ NÀO =====
    if pattern_bin_giong.search(text_no_accent):
        return """
        <div>
            <p>1. Pansa Hevibom</p>
            <p>2. Video:</p>
            <div style="max-width:600px; margin-top:10px;">
                <video width="100%" controls>
                    <source src="/static/tienlinh.mp4" type="video/mp4">
                    Trình duyệt của bạn không hỗ trợ video.
                </video>
            </div>
        </div>
        """

    # ===== CHỌN NGẪU NHIÊN 1 BÀI HÁT =====
    if pattern_random_song.search(text_no_accent):
        rand = random.random()

        if rand < 0.6:
            return "🎵 Kết quả: Bài số 3 - Binsa Hevibom"
        elif rand < 0.7:
            return "🎵 Kết quả: Bài số 1 - No"
        elif rand < 0.8:
            return "🎵 Kết quả: Bài số 2 - Sợ Liền"
        elif rand < 0.9:
            return "🎵 Kết quả: Bài số 4 - No (Mở rộng)"
        else:
            return "🎵 Kết quả: Bài số 5 - Gà Không Biết Gáy"

    # ===== VIDEO KHI / HOANG / LALANG =====
    elif pattern_video_khilo.search(text_no_accent):
        return """
        <div style="max-width:600px; margin-top:10px;">
            <video width="100%" controls>
                <source src="/static/khilo.mp4" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>
        """

    # ===== ẢNH BIN/BINSA (PHẦN ĐƯỢC THÊM) =====
    elif pattern_img_bin.search(text_no_accent):
        return """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <img src="/static/bin1.jpg" width="150">
            <img src="/static/bin2.jpg" width="150">
            <img src="/static/bin3.jpg" width="150">
            <img src="/static/bin4.jpg" width="150">
        </div>
        """

    # ===== ẢNH TUẤN =====
    elif pattern_img_tuan.search(text_no_accent):
        return """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <img src="/static/tuan1.png" width="150">
            <img src="/static/tuan2.png" width="150">
            <img src="/static/tuan3.png" width="150">
            <img src="/static/tuan4.jpg" width="150">
        </div>
        """

    # ===== ẢNH BEO =====
    elif pattern_img_beo.search(text_no_accent):
        return """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <img src="/static/beo1.jpg" width="150">
            <img src="/static/beo2.jpg" width="150">
            <img src="/static/beo3.png" width="150">
        </div>
        """

    # ===== ẢNH HOÀNG =====
    elif pattern_img_hoang.search(text_no_accent):
        return """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <img src="/static/hoang1.jpg" width="150">
            <img src="/static/hoang2.jpg" width="150">
            <img src="/static/hoang3.jpg" width="150">
            <img src="/static/hoang4.png" width="150">
        </div>
        """

    # ===== ẢNH MONEY =====
    elif pattern_img_money.search(text_no_accent):
        return """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <img src="/static/money.png" width="400">
        </div>
        """

    # ===== VIDEO BINSA =====
    elif pattern_video_bin.search(text_no_accent):
        return """
        <div style="max-width:600px; margin-top:10px;">
            <video width="100%" controls>
                <source src="/static/binsa.mp4" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>
        """

    # ===== VIDEO TUẤN =====
    elif pattern_video_turkey.search(text_no_accent):
        return """
        <div style="max-width:600px; margin-top:10px;">
            <video width="100%" controls>
                <source src="/static/turkey.mp4" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>
        """

    # ===== VIDEO BEO VA TUAN =====
    elif pattern_video_beovatuan.search(text_no_accent):
        return """
        <div style="max-width:600px; margin-top:10px;">
            <video width="100%" controls>
                <source src="/static/beovatuan.mp4" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>
        """

    # ===== VIDEO RING THE GOLDEN BELL =====
    elif pattern_video_ringbell.search(text_no_accent):
        return """
        <div style="max-width:600px; margin-top:10px;">
            <video width="100%" controls>
                <source src="/static/ringbell.mp4" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>
        """

    # ===== CÂU NÓI NỔI TIẾNG =====
    elif pattern_quote_baton.search(text_no_accent):
        return (
            "Những câu nói nổi tiếng trong nhóm Bất Ổn:\n"
            "- No\n"
            "- Sợ liền\n"
            "- Ko thể nào tin tưởng đc\n"
            "- Sao m hài v"
        )

    # ===== BIỆT DANH BEO =====
    elif pattern_beo.search(text_no_accent):
        return (
            "Biệt danh của Beo:\n"
            "- Bạc Leo\n"
            "- Beo Lạc\n"
            "- Dog Beo\n"
            "- Beo Đồng\n"
            "- Beo Bạc\n"
            "- Beo Chì\n"
            "- Beo Kẽm\n"
            "- Beo Thiếc\n"
            "- Beo Than\n"
            "- Beo Lạc Xào\n"
            "- Bạc Leo Xào\n"
            "- Beo Sắt\n"
            "- Chuông\n"
            "- Bell\n"
            "- Ớt Beo\n"
            "- Ring The Golden Bell\n"
            "- Alexander Graham Bell\n"
            "- Santiago Bernabeu\n"
            "- Gareth Bale\n"
            "- Bellingham\n"
            "- Taco Bell\n"
            "- Bella Ciao\n"
            "- Ag Cucumber\n"
            "- Beo Nhôm"
        )

    # ===== BIỆT DANH TUẤN =====
    elif pattern_tuan.search(text_no_accent):
        return (
            "Biệt danh của Tuấn:\n"
            "- Tuấn Gà\n"
            "- Tuấn Khỉ\n"
            "- Tuấn Tây\n"
            "- Tuấn Cánh Cụt\n"
            "- Tuấn tép riêu\n"
            "- Tuấn Hấp\n"
            "- Tuấn Luộc\n"
            "- Tuấn Nướng\n"
            "- Tuấn Turkey\n"
            "- Tuấn cá chuồng\n"
            "- Tuấn Dê"
        )

    # ===== BIỆT DANH BIN =====
    elif pattern_bin.search(text_no_accent):
        return (
            "Biệt danh của Bin/Pansa:\n"
            "- Bin\n"
            "- Bin Sa\n"
            "- Bạc Lin\n"
            "- Bin Lạc\n"
            "- Dog Bin\n"
            "- Pansa\n"
            "- Pansa Hevibom\n"
            "- Binsa Hevibom\n"
            "- Bin lạc xào\n"
            "- Bin phản lưới nhà\n"
            "- Ba sa\n"
            "- Ba sin\n"
            "- Tam ca\n"
            "- Song ca\n"
            "- Bin Puskas\n"
            "- Bin Tiger\n"
            "- Bin Sài Gòn"
        )

    # ===== SỰ KIỆN BINSA =====
    elif pattern_event_bin.search(text_no_accent):
        return (
            "Sự kiện Bin/Binsa:\n\n"
            "- Nhiều năm trước đã xảy ra một sự kiện làm chấn động bóng đá thế giới. "
            "Bin đánh đầu phản lưới nhà với quỹ đạo cong tuyệt đẹp bay thẳng vào góc A.\n\n"
            "- Một số ý kiến cho rằng sự kiện này bị sắp đặt vì nó diễn ra khoảng hai tuần "
            "sau chung kết Asian Cup 2024, nơi Pansa Hevibom phản lưới nhà giúp đội tuyển "
            "Việt Nam vô địch sau 6 năm chờ đợi.\n\n"
            "- Sự trùng hợp giữa Bin và Pansa khiến dư luận đặt nhiều nghi vấn. "
            "Trước sự quan tâm lớn từ người hâm mộ, Bin đổi tên thành Binsa hoặc "
            "Binsa Hevibom và sử dụng nhiều biệt danh khác.\n\n"
            "- FIFA xem xét bàn thắng và đưa vào đề cử giải Puskás. "
            "Kỳ tích xảy ra khi Binsa giành giải Puskás danh giá. "
            "Bàn thắng còn xuất hiện trong intro World Cup 2026.\n\n"
            "- Tuy nhiên bàn thắng gây tranh cãi vì khiến CLB lỡ cơ hội vô địch C1. "
            "Mùa sau phong độ sa sút, chịu nhiều chỉ trích và quyết định giải nghệ.\n\n"
            "- Sau giải nghệ, Binsa bị bắt cóc và bán sang Campuchia. "
            "Bốn năm sau được giải cứu.\n\n"
            "- Dù không trở thành cầu thủ vĩ đại, bàn phản lưới đó được mệnh danh "
            "là bàn phản lưới đẹp nhất lịch sử."
        )

    # ===== BÀI HÁT BẤT ỔN =====
    elif pattern_song_bat_on.search(text_no_accent):
        return (
            "Các bài hát của nhóm Bất Ổn:\n"
            "1. No\n"
            "2. Sợ Liền\n"
            "3. Binsa Hevibom\n"
            "4. No (Mở rộng)\n"
            "5. Gà Không Biết Gáy"
        )

    # ===== LỄ TẠ ƠN =====
    elif pattern_thanksgiving.search(text_no_accent):
        return (
            "**Lễ Tạ Ơn (Thanksgiving)** tại Hoa Kỳ:\n\n"
            "Thời gian: Thứ Năm tuần thứ tư của tháng 11 \n"
            "Ý nghĩa:Bày tỏ lòng biết ơn, sum họp gia đình \n"
            "Món chính: Gà tây quay \n"
            "Ăn kèm: Khoai tây nghiền, stuffing, sốt nam việt quất \n"
            "Tráng miệng: Bánh bí đỏ \n\n"
            "→ Ngày lễ cảm ơn và đoàn tụ."
        )

    # ===== TOP BẮN CHIM =====
    elif pattern_top_banchim.search(text_no_accent):
        return (
            "1.Binsa ( 2-4/tran)\n"
            "2.Tuấn tây ( 0-2/trận)\n"
            "3.Hoàng khỉ ( 0-1/trận)\n"
            "4.Nhân ( 0-1/trận)\n"
            "5.Beo ( hiếm)\n"
            "6. Kiệt ( ko sút nổi)"
        )

    else:
        return "Không phát hiện từ khóa."

# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "")
    reply = chatbot_response(user_text)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run()