import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# كود إرسال الطلب لتيليجرام من المتصفح مباشرة
tg_script = f'''
async function sendOrderToTelegram(orderData) {{
    const token = "{BOT_TOKEN}";
    const chatId = "{CHAT_ID}";
    
    let itemsText = orderData.items.map(i => `• ${{i.name}} (${{i.qty}}x)`).join('\\n');
    let message = `🛒 *طلب جديد من المجد إكسبرس*\\n\\n` +
                  `👤 *الزبون:* ${{orderData.name}}\\n` +
                  `📞 *الهاتف:* ${{orderData.phone}}\\n` +
                  `📍 *العنوان:* ${{orderData.address}}\\n` +
                  (orderData.notes ? `📝 *ملاحظات:* ${{orderData.notes}}\\n` : '') +
                  `\\n📦 *الطلبات:*\\n${{itemsText}}\\n\\n` +
                  `💰 *الإجمالي:* ${{orderData.total}} ل.س`;

    try {{
        const response = await fetch(`https://api.telegram.org/bot${{token}}/sendMessage`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                chat_id: chatId,
                text: message,
                parse_mode: 'Markdown'
            }})
        }});
        return response.ok;
    }} catch (e) {{
        console.error("Telegram send error:", e);
        return false;
    }}
}}
'''

print("✅ تم تجهيز كود الربط الفوري لـ GitHub Pages!")
