import os
import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# كود إرسال تيليجرام
telegram_code = f'''
function sendOrderToTelegramDirect(msgText) {{
    var cleanMsg = msgText;
    try {{ cleanMsg = decodeURIComponent(msgText.replace(/\\+/g, ' ')); }} catch(e) {{}}
    
    // استخراج النص إذا كان الرابط يحتوي على text=
    if (cleanMsg.includes("text=")) {{
        cleanMsg = cleanMsg.split("text=")[1].split("&")[0];
        try {{ cleanMsg = decodeURIComponent(cleanMsg); }} catch(e) {{}}
    }}

    if (!cleanMsg || cleanMsg.trim().length === 0) {{
        cleanMsg = "🛒 طلب جديد من المجد إكسبرس";
    }}

    var url = "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage";
    fetch(url, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
            chat_id: "{CHAT_ID}",
            text: cleanMsg
        }})
    }}).then(function() {{
        alert("🎉 تم تأكيد طلبك بنجاح!\\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً.");
        try {{
            localStorage.removeItem('cart');
            localStorage.removeItem('shopping_cart');
            if (typeof cart !== 'undefined') cart = [];
        }} catch(e) {{}}
        location.reload();
    }}).catch(function() {{
        alert("🎉 تم تأكيد طلبك بنجاح!");
        location.reload();
    }});
}}
'''

# فحص كافّة ملفات الـ HTML و JS في المجلد
found_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") or file.endswith(".js"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if "wa.me" in content or "whatsapp.com" in content:
                    found_files.append(file_path)

                    # إضافة دالة تيليجرام
                    if "sendOrderToTelegramDirect" not in content:
                        content = f"<script>{telegram_code}</script>\n" + content if file.endswith(".html") else telegram_code + "\n" + content

                    # استبدال عمليات فتح الواتساب بإرسال تيليجرام
                    content = re.sub(r'window\.location\.href\s*=\s*(`[^`]*wa\.me[^`]*`|\'[^\']*wa\.me[^\']*\'|"[^"]*wa\.me[^"]*"|[^\s;]+);', r'sendOrderToTelegramDirect(\1);', content)
                    content = re.sub(r'window\.open\s*\(\s*(`[^`]*wa\.me[^`]*`|\'[^\']*wa\.me[^\']*\'|"[^"]*wa\.me[^"]*"|[^\s,\)]+)[^\)]*\);', r'sendOrderToTelegramDirect(\1);', content)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ تم تعديل الملف: {file_path}")
            except Exception as e:
                pass

# إضافة معترض احتياطي عام لو كانت الروابط ديناميكية
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

fallback_script = f'''
<script>
{telegram_code}

document.addEventListener('submit', function(e) {{
    e.preventDefault();
    e.stopPropagation();
    
    let inputs = e.target.querySelectorAll('input, textarea');
    let details = [];
    inputs.forEach(i => {{
        if (i.value && i.type !== 'hidden' && i.type !== 'submit') {{
            details.push((i.placeholder || i.name || 'حقل') + ": " + i.value);
        }
    }});

    let cartData = localStorage.getItem('cart') || "";
    let msg = "🛒 *طلب جديد من المجد إكسبرس*\\n\\n" + details.join("\\n");
    sendOrderToTelegramDirect(msg);
    return false;
}}, true);
</script>
'''

if "sendOrderToTelegramDirect" not in html:
    html = html.replace("</body>", f"{fallback_script}\n</body>")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

print("🚀 تم تحديث النظام بالكامل ورفعه جاهزاً!")
