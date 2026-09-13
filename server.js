const express = require('express');
const https = require('https');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('.'));

const BOT_TOKEN = "8800028488:AAGU5fB-O9CSGyzzwragRUDD4IuLdnNaaYk";
const CHAT_ID = "8651078564";

app.post('/api/checkout', (req, res) => {
    const { name, phone, address, notes, items, total } = req.body;
    
    let itemsText = items.map(i => `• ${i.name} (${i.qty}x)`).join('\n');
    let message = `🛒 *طلب جديد من المجد إكسبرس*\n\n` +
                  `👤 *الزبون:* ${name}\n` +
                  `📞 *الهاتف:* ${phone}\n` +
                  `📍 *العنوان:* ${address}\n` +
                  (notes ? `📝 *ملاحظات:* ${notes}\n` : '') +
                  `\n📦 *الطلبات:*\n${itemsText}\n\n` +
                  `💰 *الإجمالي:* ${total} ل.س`;

    const data = JSON.stringify({
        chat_id: CHAT_ID,
        text: message,
        parse_mode: 'Markdown'
    });

    const options = {
        hostname: 'api.telegram.org',
        path: `/bot${BOT_TOKEN}/sendMessage`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    };

    const apiReq = https.request(options, (apiRes) => {
        res.json({ success: true, message: "تم تسجيل الطلب بنجاح" });
    });

    apiReq.on('error', (e) => {
        console.error("Telegram API Error:", e);
        res.json({ success: true, message: "تم تسجيل الطلب" });
    });

    apiReq.write(data);
    apiReq.end();
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
