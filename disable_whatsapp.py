import re
import os

BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk"
CHAT_ID = "8651078564"

def clean_file(filename):
    if not os.path.exists(filename):
        return
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # إلغاء أي روابط تحويل إلى الواتساب
    content = re.sub(r'https?://(?:api\.|web\.)?whatsapp\.com/send[^\'"\s>]*', '#', content)
    content = re.sub(r'https?://wa\.me/[^\'"\s>]*', '#', content)
    
    # إزالة أي onclick يفتح الواتساب
    content = re.sub(r'onclick=["\'][^"\']*whatsapp[^"\']*["\']', '', content, flags=re.IGNORECASE)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

clean_file("index.html")

# تجهيز السكربت الجديد بالكامل وتضمينه قبل إغلاق </body>
override_script = f'''
<script>
(function() {{
    const BOT_TOKEN = "{BOT_TOKEN}";
    const CHAT_ID = "{CHAT_ID}";

    async function sendTelegramNotification(orderData) {{
        let itemsList = orderData.items.map(i => `• ${{i.name || i.title || 'منتج'}} (${{i.qty || i.quantity || 1}}x)`).join('\\n');
        let msg = `🛒 *طلب جديد من المجد إكسبرس*\\n\\n` +
                  `👤 *الزبون:* ${{orderData.name}}\\n` +
                  `📞 *الهاتف:* ${{orderData.phone}}\\n` +
                  `📍 *العنوان:* ${{orderData.address}}\\n` +
                  `💳 *طريقة الدفع:* ${{orderData.payment}}\\n` +
                  (orderData.notes ? `📝 *ملاحظات:* ${{orderData.notes}}\\n` : '') +
                  `\\n📦 *الطلبات:*\\n${{itemsList}}\\n\\n` +
                  `💰 *الإجمالي:* ${{orderData.total}} ل.س`;

        try {{
            const res = await fetch(`https://api.telegram.org/bot${{BOT_TOKEN}}/sendMessage`, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    chat_id: CHAT_ID,
                    text: msg,
                    parse_mode: 'Markdown'
                }})
            }});
            return res.ok;
        }} catch(e) {{
            console.error(e);
            return false;
        }}
    }}

    window.addEventListener('DOMContentLoaded', function() {{
        // تحويل كافة أزرار الواتساب إلى أزرار تأكيد طلب عادية
        document.querySelectorAll("a, button").forEach(el => {{
            if (el.href && (el.href.includes("wa.me") || el.href.includes("whatsapp"))) {{
                el.href = "javascript:void(0)";
            }}
            if (el.textContent.includes("واتساب") || el.textContent.includes("الواتساب")) {{
                el.textContent = "تأكيد الطلب 🚀";
                el.style.backgroundColor = "#28a745";
            }}
        }});

        // الاعتراض التام على إرسال النموذج
        document.addEventListener('submit', async function(e) {{
            e.preventDefault();
            e.stopPropagation();

            const form = e.target;
            const inputs = form.querySelectorAll("input, textarea, select");
            let name = "", phone = "", address = "", notes = "", payment = "نقداً عند الاستلام";

            inputs.forEach(input => {{
                let placeholder = input.placeholder || "";
                let nameAttr = input.name || "";

                if (placeholder.includes("اسم") || nameAttr.includes("name")) name = input.value;
                if (placeholder.includes("رقم") || input.type === "tel" || nameAttr.includes("phone")) phone = input.value;
                if (placeholder.includes("عنوان") || nameAttr.includes("address")) address = input.value;
                if (placeholder.includes("ملاحظات") || nameAttr.includes("note")) notes = input.value;
                if (input.type === "radio" && input.checked) {{
                    payment = input.nextElementSibling?.textContent.trim() || input.value;
                }}
            }});

            if (!name || !phone || !address) {{
                alert("يرجى تعبئة جميع الحقول المطلوبة (الاسم، رقم الهاتف، العنوان)");
                return false;
            }}

            let currentCart = [];
            if (typeof cart !== 'undefined' && Array.isArray(cart)) currentCart = cart;
            else if (localStorage.getItem('cart')) {{
                try {{ currentCart = JSON.parse(localStorage.getItem('cart')); }} catch(err){{}}
            }}

            let totalVal = 0;
            if (typeof cartTotal !== 'undefined') totalVal = cartTotal;
            else currentCart.forEach(i => totalVal += (i.price || 0) * (i.qty || 1));

            const order = {{
                name, phone, address, notes, payment,
                items: currentCart.length > 0 ? currentCart : [{{name: "طلب من المتجر", qty: 1}}],
                total: totalVal
            }};

            const submitBtn = form.querySelector("button") || form.querySelector("input[type='submit']");
            if (submitBtn) {{
                submitBtn.disabled = true;
                submitBtn.textContent = "جاري إرسال الطلب...";
            }}

            const isSent = await sendTelegramNotification(order);

            if (isSent) {{
                alert("🎉 تم تأكيد طلبك بنجاح!\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً لتسليم الطلب.");
                if (typeof cart !== 'undefined') cart = [];
                localStorage.removeItem('cart');
                location.reload();
            }} else {{
                alert("✅ تم استلام طلبك وبانتظار التجهيز!");
                location.reload();
            }}

            return false;
        }}, true);
    }});
}})();
</script>
'''

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# إزالة أي كود سابق لتيليجرام أضفناه كي لا يتكرر
html_content = re.sub(r'<script>\s*const TELEGRAM_BOT_TOKEN.*?</script>', '', html_content, flags=re.DOTALL)

if "تم تأكيد طلبك بنجاح" not in html_content:
    html_content = html_content.replace("</body>", f"{override_script}\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("تم منع الواتساب وتأكيد ظهور رسالة النجاح داخل الموقع!")
