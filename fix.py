import json

with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

rules = [
    ("ثوم", "https://images.unsplash.com/photo-1615485290382-441e4d049cb5"),
    ("بطاطا", "https://images.unsplash.com/photo-1518977676601-b53f82aba655"),
    ("ملفوف", "https://images.unsplash.com/photo-1595855759920-86582396756a"),
    ("كرمب", "https://images.unsplash.com/photo-1595855759920-86582396756a"),
    ("فليفلة", "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83"),
    ("فلفل", "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83"),
    ("زهرة", "https://images.unsplash.com/photo-1568584712275-8b135200b87b"),
    ("قرنبيط", "https://images.unsplash.com/photo-1568584712275-8b135200b87b"),
    ("بقدونس", "https://images.unsplash.com/photo-1587888637140-8f9f99f4305f"),
    ("نعناع", "https://images.unsplash.com/photo-1628556270448-4d6e4604e26e"),
    ("فراولة", "https://images.unsplash.com/photo-1464965911861-746a04b4bca6"),
    ("بصل", "https://images.unsplash.com/photo-1508747703725-719777637510"),
    ("بندورة", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea"),
    ("طماطم", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea"),
    ("خيار", "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6"),
    ("تفاح", "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6"),
    ("موز", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e"),
    ("برتقال", "https://images.unsplash.com/photo-1547514701-42782101795e"),
    ("ليمون", "https://images.unsplash.com/photo-1534706936160-d5ee6773357b"),
    ("جزر", "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37"),
    ("خس", "https://images.unsplash.com/photo-1550989460-0adf9ea622e2"),
    ("حليب", "https://images.unsplash.com/photo-1550583724-b2692b85b150"),
    ("لبن", "https://images.unsplash.com/photo-1550583724-b2692b85b150"),
    ("جبن", "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"),
    ("بيض", "https://images.unsplash.com/photo-1516448620398-c5f44bf9f441"),
    ("خبز", "https://images.unsplash.com/photo-1509440159596-0249088772ff"),
    ("زيت", "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5"),
    ("دجاج", "https://images.unsplash.com/photo-1587593810167-a84920ea0781"),
    ("لحم", "https://images.unsplash.com/photo-1603048588665-791ca8aea617"),
    ("أرز", "https://images.unsplash.com/photo-1586201375761-83865001e31c"),
    ("رز", "https://images.unsplash.com/photo-1586201375761-83865001e31c"),
    ("معكرونة", "https://images.unsplash.com/photo-1621996346565-e3d5d6281226"),
    ("شاي", "https://images.unsplash.com/photo-1576092768241-dec231879fc3"),
    ("قهوة", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd"),
    ("سكر", "https://images.unsplash.com/photo-1581441363689-1f3c3c55c2f5"),
]

for p in products:
    name = p.get("name", "")
    matched = False
    for word, url in rules:
        if word in name:
            p["img"] = url + "?w=400&auto=format&fit=crop&q=70"
            matched = True
            break
    if not matched:
        p["img"] = "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&auto=format&fit=crop&q=70"

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("تم مطابقة وتحديث كافة الصور بنجاح!")
