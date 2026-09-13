import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# تنظيف أي أكواد سابقة أُضيفت في الأسفل
if "<!-- كود إرسال تيليجرام المضاف بأمان -->" in html:
    html = html.split("<!-- كود إرسال تيليجرام المضاف بأمان -->")[0]

smart_script = '''
<!-- كود إرسال تيليجرام المضاف بأمان -->
<script>
(function() {
    const BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk";
    const CHAT_ID = "8651078564";

    async function sendOrderNotification(customText) {
        try {
            await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: CHAT_ID,
                    text: customText,
                    parse_mode: 'Markdown'
                })
            });
        } catch (e) {
            console.error("Telegram Send Error:", e);
        }
    }

    function buildOrderMessage() {
        let name = "", phone = "", address = "", payment = "نقداً عند الاستلام", notes = "";

        document.querySelectorAll('input, textarea, select').forEach(el => {
            let p = (el.placeholder || "").toLowerCase();
            let n = (el.name || "").toLowerCase();
            let val = el.value ? el.value.trim() : "";

            if (el.type === 'radio' || el.type === 'checkbox') {
                if (el.checked) {
                    let label = el.nextElementSibling ? el.nextElementSibling.textContent.trim() : el.value;
                    if (label.includes("شام") || el.value.includes("sham")) payment = "شام كاش (Sham Cash)";
                    else payment = "الدفع نقداً عند الاستلام";
                }
                return;
            }

            if (!val) return;

            if (p.includes("اسم") || n.includes("name")) name = val;
            else if (p.includes("09") || p.includes("رقم") || n.includes("phone") || el.type === 'tel') phone = val;
            else if (p.includes("منطقة") || p.includes("شارع") || p.includes("عنوان") || n.includes("address")) address = val;
            else if (p.includes("ملاحظ") || n.includes("note")) notes = val;
        });

        // استخراج قيم المدخلات في حال عدم مطابقة الـ placeholder
        if (!name || !phone || !address) {
            let textInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="tel"], textarea')).filter(i => i.value.trim() !== "");
            if (textInputs[0] && !name) name = textInputs[0].value;
            if (textInputs[1] && !phone) phone = textInputs[1].value;
            if (textInputs[2] && !address) address = textInputs[2].value;
        }

        // قراءة منتجات السلة
        let items = [];
        try {
            let localCart = localStorage.getItem('cart') || localStorage.getItem('shopping_cart') || localStorage.getItem('almajd_cart');
            if (localCart) {
                let parsed = JSON.parse(localCart);
                if (Array.isArray(parsed)) items = parsed;
            }
        } catch(e) {}

        if (items.length === 0 && typeof cart !== 'undefined' && Array.isArray(cart)) {
            items = cart;
        }

        let itemsText = "";
        let total = "";

        if (items.length > 0) {
            let sum = 0;
            itemsText = items.map(item => {
                let title = item.title || item.name || item.productName || "منتج";
                let qty = item.qty || item.quantity || item.count || 1;
                let price = item.price || 0;
                if (price) sum += (price * qty);
                return `• ${title} (الكمية: ${qty})`;
            }).join("\n");
            if (sum > 0) total = sum + " ل.س";
        }

        if (!itemsText) {
            let domItems = [];
            document.querySelectorAll('.cart-item, .cart-product, #cart-items div, .cart-list li').forEach(el => {
                let txt = el.textContent.replace(/\s+/g, ' ').trim();
                if (txt) domItems.push("• " + txt);
            });
            if (domItems.length > 0) itemsText = domItems.join("\n");
        }

        if (!itemsText) itemsText = "• طلب منتجات من المتجر";

        if (!total) {
            let totalEl = document.querySelector('.cart-total, #cart-total, .total-price, #total');
            if (totalEl) total = totalEl.textContent.trim();
        }

        let msg = `🛒 *طلب جديد من المجد إكسبرس*\n\n` +
                  `👤 *الزبون:* ${name || 'غير محدد'}\n` +
                  `📞 *الهاتف:* ${phone || 'غير محدد'}\n` +
                  `📍 *العنوان:* ${address || 'غير محدد'}\n` +
                  `💳 *طريقة الدفع:* ${payment}\n` +
                  (notes ? `📝 *ملاحظات:* ${notes}\n` : '') +
                  `\n📦 *تفاصيل الطلبات:*\n${itemsText}\n` +
                  (total ? `\n💰 *الإجمالي:* ${total}` : '');

        return { msg, name, phone, address };
    }

    document.addEventListener('DOMContentLoaded', function() {
        document.addEventListener('click', async function(e) {
            let btn = e.target.closest('button, a, input[type="submit"]');
            if (!btn) return;

            let txt = (btn.textContent || btn.value || "").trim();
            if (txt.includes('واتساب') || txt.includes('تأكيد') || txt.includes('إرسال') || txt.includes('طلب')) {
                e.preventDefault();
                e.stopPropagation();

                let { msg, name, phone, address } = buildOrderMessage();

                if (!name || !phone || !address) {
                    alert("يرجى تعبئة كافة البيانات (الاسم، رقم الهاتف، والعنوان) لإكمال الطلب.");
                    return false;
                }

                btn.disabled = true;
                let oldText = btn.textContent;
                btn.textContent = "جاري الإرسال...";

                await sendOrderNotification(msg);

                alert("🎉 تم تأكيد طلبك بنجاح!\nشكراً لتسوقك من المجد إكسبرس، سنتواصل معك قريباً لتسليم الطلب.");

                try {
                    localStorage.removeItem('cart');
                    localStorage.removeItem('shopping_cart');
                    if (typeof cart !== 'undefined') cart = [];
                } catch(e) {}

                location.reload();
            }
        }, true);
    });
})();
</script>
'''

if "</body>" in html:
    html = html.replace("</body>", f"{smart_script}\n</body>")
else:
    html += smart_script

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ تم تحديث كود الإرسال والتأكيد بنجاح!")
