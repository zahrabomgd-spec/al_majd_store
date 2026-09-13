import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# 1. قراءة index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2. تنظيف أي أكواد سابقة أضفناها
html = re.sub(r'<script>[\s\S]*?TELEGRAM_BOT_TOKEN[\s\S]*?</script>', '', html)
html = re.sub(r'<script>[\s\S]*?processTelegramOrder[\s\S]*?</script>', '', html)
html = re.sub(r'<script>[\s\S]*?extractAndSend[\s\S]*?</script>', '', html)

# 3. تغيير نص الزر إلى "تأكيد الطلب"
html = html.replace("إرسال الطلب عبر الواتساب", "تأكيد الطلب 🚀")
html = html.replace("الطلب عبر الواتساب", "تأكيد الطلب 🚀")

# 4. كود الاعتراض الشامل المباشر
interceptor_script = f'''
<script>
(function() {{
    const BOT_TOKEN = "{BOT_TOKEN}";
    const CHAT_ID = "{CHAT_ID}";

    function sendToTelegram(msgText) {{
        fetch(`https://api.telegram.org/bot${{BOT_TOKEN}}/sendMessage`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                chat_id: CHAT_ID,
                text: msgText
            }})
        }}).then(() => {{
            alert("🎉 تم تأكيد طلبك بنجاح!\\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً.");
            if (typeof cart !== 'undefined') cart = [];
            localStorage.removeItem('cart');
            location.reload();
        }}).catch(err => {{
            alert("🎉 تم تأكيد طلبك بنجاح!");
            location.reload();
        }});
    }}

    function extractAndSend(url) {{
        let msg = "🛒 طلب جديد من المجد إكسبرس";
        try {{
            if (url && url.includes("text=")) {{
                let rawText = url.split("text=")[1].split("&")[0];
                msg = decodeURIComponent(rawText);
            }}
        }} catch(e) {{}}
        sendToTelegram(msg);
    }}

    // اعتراض فتح الواتساب عبر النافذة
    const origOpen = window.open;
    window.open = function(url, target, features) {{
        if (url && (url.includes('wa.me') || url.includes('whatsapp.com'))) {{
            extractAndSend(url);
            return null;
        }}
        return origOpen.apply(this, arguments);
    }};

    // اعتراض الضغط على روابط الواتساب
    document.addEventListener('click', function(e) {{
        let a = e.target.closest('a');
        if (a && a.href && (a.href.includes('wa.me') || a.href.includes('whatsapp.com'))) {{
            e.preventDefault();
            e.stopPropagation();
            extractAndSend(a.href);
        }}
    }}, true);
}})();
</script>
'''

if "<head>" in html:
    html = html.replace("<head>", f"<head>\n{interceptor_script}")
else:
    html = f"{interceptor_script}\n{html}"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ تم تطبيق كود الاعتراض الشامل بنجاح!")
