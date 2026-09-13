import re

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

# قراءة index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# تنظيف الكود القديم إن وجد
html = re.sub(r'<script>[\s\S]*?processTelegramOrder[\s\S]*?</script>', '', html)

new_script = f'''
<script>
async function processTelegramOrder(e) {{
    if (e) e.preventDefault();

    // البحث عن البيانات داخل الشاشة
    let name = "", phone = "", address = "", notes = "", payment = "نقداً عند الاستلام";

    document.querySelectorAll("input, textarea").forEach(input => {{
        let p = (input.placeholder || "").toLowerCase();
        let n = (input.name || "").toLowerCase();
        let id = (input.id || "").toLowerCase();

        if (p.includes("اسم") || n.includes("name") || id.includes("name")) name = input.value;
        if (p.includes("رقم") || p.includes("هاتف") || input.type === "tel" || n.includes("phone") || id.includes("phone")) phone = input.value;
        if (p.includes("عنوان") || n.includes("address") || id.includes("address")) address = input.value;
        if (p.includes("ملاحظات") || n.includes("note") || id.includes("note")) notes = input.value;
        if (input.type === "radio" && input.checked) {{
            payment = input.nextElementSibling ? input.nextElementSibling.textContent.trim() : input.value;
        }}
    }});

    if (!name.trim() || !phone.trim() || !address.trim()) {{
        alert("يرجى تعبئة كافة الحقول (الاسم، رقم التواصل، والعنوان).");
        return false;
    }}

    // الحصول على السلة
    let currentCart = [];
    if (typeof cart !== 'undefined' && Array.isArray(cart) && cart.length > 0) {{
        currentCart = cart;
    }} else if (localStorage.getItem('cart')) {{
        try {{ currentCart = JSON.parse(localStorage.getItem('cart')); }} catch(err) {{}}
    }}

    let totalVal = 0;
    if (typeof cartTotal !== 'undefined' && cartTotal > 0) {{
        totalVal = cartTotal;
    }} else {{
        currentCart.forEach(i => totalVal += (i.price || 0) * (i.qty || i.quantity || 1));
    }}

    let itemsList = currentCart.map(i => `• ${{i.name || i.title || 'منتج'}} (${{i.qty || i.quantity || 1}}x)`).join('\\n');
    if (!itemsList) itemsList = "• طلب منتجات من المتجر";

    let message = `🛒 *طلب جديد من المجد إكسبرس*\\n\\n` +
                  `👤 *الزبون:* ${{name}}\\n` +
                  `📞 *الهاتف:* ${{phone}}\\n` +
                  `📍 *العنوان:* ${{address}}\\n` +
                  `💳 *طريقة الدفع:* ${{payment}}\\n` +
                  (notes ? `📝 *ملاحظات:* ${{notes}}\\n` : '') +
                  `\\n📦 *الطلبات:*\\n${{itemsList}}\\n\\n` +
                  `💰 *الإجمالي:* ${{totalVal}} ل.س`;

    // إرسال الإشعار إلى تيليجرام
    try {{
        await fetch(`https://api.telegram.org/bot{BOT_TOKEN}/sendMessage`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                chat_id: "{CHAT_ID}",
                text: message,
                parse_mode: 'Markdown'
            }})
        }});
    }} catch (err) {{
        console.error(err);
    }}

    alert("🎉 تم تأكيد طلبك بنجاح!\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً.");
    localStorage.removeItem('cart');
    if (typeof cart !== 'undefined') cart = [];
    location.reload();
    return false;
}}

// ربط جميع أزرار الطلب بالدالة تلقائياً
window.addEventListener('DOMContentLoaded', function() {{
    setInterval(function() {{
        document.querySelectorAll("button, a, input[type='submit']").forEach(el => {{
            let txt = el.textContent || el.value || "";
            if (txt.includes("تأكيد") || txt.includes("واتساب") || txt.includes("إرسال")) {{
                el.textContent = "تأكيد الطلب 🚀";
                el.style.backgroundColor = "#28a745";
                el.onclick = processTelegramOrder;
            }}
        }});
    }}, 500);
}});
</script>
'''

if "processTelegramOrder" not in html:
    html = html.replace("</body>", f"{new_script}\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("تم إصلاح الزر وربطه بالكامل!")
