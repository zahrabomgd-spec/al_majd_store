const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});
const upload = multer({ storage: storage });

const DATA_FILE = path.join(__dirname, 'products.json');

// قائمة منتجات البقالة والسوبرماركت - بالليرة السورية
const initialProducts = [
  {
    id: 1,
    name: "زيت زيتون بلدي (1 لتر)",
    category: "زيوت وألبان",
    price: 85000,
    image: "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 2,
    name: "جبنة حلوم بلدية (1 كغ)",
    category: "زيوت وألبان",
    price: 65000,
    image: "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 3,
    name: "رز كبسة طويل الحبة (5 كغ)",
    category: "مواد جافة",
    price: 110000,
    image: "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 4,
    name: "سكر أبيض ناعم (5 كغ)",
    category: "مواد جافة",
    price: 75000,
    image: "https://images.unsplash.com/photo-1622484210800-88849f578714?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 5,
    name: "شاي أسود فاخر (500 غرام)",
    category: "مشروبات",
    price: 45000,
    image: "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 6,
    name: "قهوة عربية مع هيل (250 غرام)",
    category: "مشروبات",
    price: 38000,
    image: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 7,
    name: "سمنة حموية فاخرة (1 كغ)",
    category: "زيوت وألبان",
    price: 120000,
    image: "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 8,
    name: "معجون طماطم - رب البندورة (800 غرام)",
    category: "معلبات",
    price: 18000,
    image: "https://images.unsplash.com/photo-1534483509719-3feaee7c30da?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 9,
    name: "علبة تون قطع بالزيت (180 غرام)",
    category: "معلبات",
    price: 16000,
    image: "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 10,
    name: "معكرونة مشكلة (3 أظرف x 400غ)",
    category: "مواد جافة",
    price: 22000,
    image: "https://images.unsplash.com/photo-1621996346565-e3d5d6281288?auto=format&fit=crop&w=600&q=80"
  }
];

function getProducts() {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(initialProducts, null, 2));
    return initialProducts;
  }
  const data = fs.readFileSync(DATA_FILE);
  return JSON.parse(data);
}

function saveProducts(products) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(products, null, 2));
}

app.get('/api/products', (req, res) => {
  res.json(getProducts());
});

app.post('/api/products', upload.single('image'), (req, res) => {
  const products = getProducts();
  const newProduct = {
    id: Date.now(),
    name: req.body.name,
    category: req.body.category,
    price: Number(req.body.price),
    image: req.file ? `/uploads/${req.file.filename}` : 'https://via.placeholder.com/300'
  };
  products.push(newProduct);
  saveProducts(products);
  res.status(201).json(newProduct);
});

app.delete('/api/products/:id', (req, res) => {
  let products = getProducts();
  const id = Number(req.params.id);
  products = products.filter(p => p.id !== id);
  saveProducts(products);
  res.json({ message: 'تم الحذف بنجاح' });
});

app.listen(PORT, () => {
  console.log(`بقالة المجد تعمل على المنفذ ${PORT}`);
});
