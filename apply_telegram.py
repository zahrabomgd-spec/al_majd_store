import os
import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# كود دالة الإرسال إلى تيليجرام مباشرة
telegram_js = f'''
<script>
async function sendOrderToTelegram(name, phone, address, notes, items, total) {{
    const token = "{BOT_TOKEN}";
    const chatId = "{CHAT_ID}";
    
    let itemsText = items.map(i => `• ${{i.name || i.title}} (${{i.qty || i.quantity || 1}}x)`).join('\\n');
    let message = `🛒 *طلب جديد من المجد إكسبرس*\\n\\n` +
                  `👤 *الزبون:* ${{name}}\\n` +
                  `📞 *الهاتف:* ${{phone}}\\n` +
                  `📍 *العنوان:* ${{address}}\\n` +
                  (notes ? `📝 *ملاحظات:* ${{notes}}\\n` : '') +
                  `\\n📦 *الطلبات:*\\n${{itemsText}}\\n\\n` +
                  `💰 *الإجمالي:* ${{total}} ل.س`;

    try {{
        const res = await fetch(`https://api.telegram.org/bot${{token}}/sendMessage`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                chat_id: chatId,
                text: message,
                parse_mode: 'Markdown'
            }})
        }});
        return res.ok;
    }} catch (e) {{
        console.error("Telegram send error:", e);
        return false;
    }}
}}
</script>
'''

# التعديل على index.html
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    if "sendOrderToTelegram" not in html:
        if "</body>" in html:
            html = html.replace("</body>", f"{telegram_js}\n</body>")
        else:
            html += telegram_js

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ تم إضافة كود تيليجرام إلى index.html")

print("جاهز للرفع إلى GitHub!")
