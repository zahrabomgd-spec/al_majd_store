import subprocess
import os

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# 1. استرجاع index.html السليم لإصلاح أي خطأ برمجي
try:
    subprocess.run(["git", "checkout", "HEAD", "--", "index.html"], check=True)
except Exception as e:
    print("Git checkout status:", e)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

if "<!-- TELEGRAM_INTERCEPTOR_START -->" in html:
    html = html.split("<!-- TELEGRAM_INTERCEPTOR_START -->")[0]

interceptor = """<!-- TELEGRAM_INTERCEPTOR_START -->
<script>
(function() {
    var BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk";
    var CHAT_ID = "8651078564";

    function sendTelegram(textMsg) {
        var url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage";
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: CHAT_ID,
                text: textMsg
            })
        });
    }

    function processOrderMessage(msgText) {
        var cleanMsg = msgText;
        try {
            cleanMsg = decodeURIComponent(msgText.replace(/\\+/g, ' '));
        } catch(e) {}

        if (!cleanMsg || cleanMsg.trim().length === 0) {
            cleanMsg = "🛒 طلب جديد من المجد إكسبرس";
        }

        sendTelegram(cleanMsg).then(function() {
            alert("🎉 تم تأكيد طلبك بنجاح!\\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً.");
            try {
                localStorage.removeItem('cart');
                localStorage.removeItem('shopping_cart');
                if (typeof cart !== 'undefined') cart = [];
            } catch(e) {}
            location.reload();
        }).catch(function() {
            alert("🎉 تم تأكيد طلبك بنجاح!");
            location.reload();
        });
    }

    function handleWhatsAppUrl(url) {
        if (!url || typeof url !== 'string') return false;
        if (url.indexOf('wa.me') !== -1 || url.indexOf('whatsapp.com') !== -1) {
            var msgText = "";
            if (url.indexOf('text=') !== -1) {
                msgText = url.split('text=')[1].split('&')[0];
            } else if (url.indexOf('message=') !== -1) {
                msgText = url.split('message=')[1].split('&')[0];
            }
            processOrderMessage(msgText);
            return true;
        }
        return false;
    }

    // اعتراض فتح نافذة الواتساب
    var originalOpen = window.open;
    window.open = function(url, target, features) {
        if (handleWhatsAppUrl(url)) {
            return null;
        }
        return originalOpen.apply(this, arguments);
    };

    // اعتراض الضغط على روابط الواتساب
    document.addEventListener('click', function(e) {
        var target = e.target;
        while (target && target !== document) {
            if (target && target.tagName === 'A' && target.href) {
                if (handleWhatsAppUrl(target.href)) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            }
            target = target.parentNode;
        }
    }, true);

})();
</script>
"""

if "</body>" in html:
    html = html.replace("</body>", interceptor + "\n</body>")
else:
    html = html + "\n" + interceptor

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ تم إصلاح الملف وتركيب المعترض الذكي بنجاح!")
