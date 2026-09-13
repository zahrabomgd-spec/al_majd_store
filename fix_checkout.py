import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. تغيير نص الزر من واتساب إلى تأكيد الطلب
html = html.replace("إرسال الطلب عبر الواتساب", "تأكيد الطلب 🚀")
html = html.replace("الطلب عبر الواتساب", "تأكيد الطلب 🚀")

# 2. كود إرسال الطلب المباشر لتيليجرام من المتصفح
telegram_script = f'''
<script>
const TELEGRAM_BOT_TOKEN = "{BOT_TOKEN}";
const TELEGRAM_CHAT_ID = "{CHAT_ID}";

async function sendOrderToTelegram(orderData) {{
    let itemsText = orderData.items.map(i => `• ${{i.name || i.title || 'منتج'}} (${{i.qty || i.quantity || 1}}x)`).join('\\n');
    let message = `🛒 *طلب جديد من المجد إكسبرس*\\n\\n` +
                  `👤 *الزبون:* ${{orderData.name}}\\n` +
                  `📞 *الهاتف:* ${{orderData.phone}}\\n` +
                  `📍 *العنوان:* ${{orderData.address}}\\n` +
                  `💳 *طريقة الدفع:* ${{orderData.payment}}\\n` +
                  (orderData.notes ? `📝 *ملاحظات:* ${{orderData.notes}}\\n` : '') +
                  `\\n📦 *الطلبات:*\\n${{itemsText}}\\n\\n` +
                  `💰 *الإجمالي:* ${{orderData.total}} ل.س`;

    try {{
        const response = await fetch(`https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/sendMessage`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                chat_id: TELEGRAM_CHAT_ID,
                text: message,
                parse_mode: 'Markdown'
            }})
        }});
        return response.ok;
    }} catch(e) {{
        console.error("Telegram Error:", e);
        return false;
    }}
}}

document.addEventListener("DOMContentLoaded", function() {{
    // البحث عن أزرار الواتساب وتغييرها إلى تأكيد الطلب
    document.querySelectorAll("button, a").forEach(el => {{
        if (el.textContent.includes("واتساب") || el.textContent.includes("الواتساب")) {{
            el.textContent = "تأكيد الطلب 🚀";
            el.style.backgroundColor = "#28a745";
        }}
    }});

    // الاعتراض على النموذج وإرساله إلى تيليجرام
    const form = document.querySelector("form");
    if (form) {{
        form.onsubmit = async function(e) {{
            e.preventDefault();
            
            const inputs = form.querySelectorAll("input, textarea");
            let name = "", phone = "", address = "", notes = "", payment = "نقداً عند الاستلام";

            inputs.forEach(input => {{
                if (input.placeholder?.includes("اسم") || input.name?.includes("name")) name = input.value;
                if (input.placeholder?.includes("رقم") || input.type === "tel") phone = input.value;
                if (input.placeholder?.includes("عنوان") || input.name?.includes("address")) address = input.value;
                if (input.type === "radio" && input.checked) {{
                    payment = input.nextElementSibling?.textContent.trim() || input.value;
                }}
            }});

            if (!name || !phone || !address) {{
                alert("يرجى تعبئة كافة البيانات (الاسم، الهاتف، العنوان)");
                return;
            }}

            let currentCart = [];
            if (typeof cart !== 'undefined' && Array.isArray(cart)) currentCart = cart;
            else if (localStorage.getItem('cart')) {{
                try {{ currentCart = JSON.parse(localStorage.getItem('cart')); }} catch(e){{}}
            }}

            let total = 0;
            if (typeof cartTotal !== 'undefined') total = cartTotal;
            else currentCart.forEach(item => total += (item.price || 0) * (item.qty || 1));

            const orderData = {{
                name, phone, address, payment, notes,
                items: currentCart.length > 0 ? currentCart : [{{name: "طلب من المتجر", qty: 1}}],
                total: total
            }};

            const btn = form.querySelector("button[type='submit']") || form.querySelector("button");
            if (btn) btn.disabled = true;

            const success = await sendOrderToTelegram(orderData);
            if (success) {{
                alert("✅ تم إرسال طلبك بنجاح! وسنتواصل معك قريباً.");
                localStorage.removeItem('cart');
                location.reload();
            }} else {{
                alert("حدث خطأ في الإرسال، يرجى المحاولة مرة أخرى.");
                if (btn) btn.disabled = false;
            }}
        }};
    }}
}});
</script>
'''

if "TELEGRAM_BOT_TOKEN" not in html:
    html = html.replace("</body>", f"{telegram_script}\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("تم تحديث index.html بنجاح!")
