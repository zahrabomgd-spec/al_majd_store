const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 3000;

// كلمة سر لوحة التحكم (يمكنك تغييرها هنا متى شئت)
const ADMIN_PASSWORD = "123"; 

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null, Date.now() + path.extname(file.originalname))
});
const upload = multer({ storage: storage });

const dataFile = path.join(__dirname, 'products.json');

function getProducts() {
    if (!fs.existsSync(dataFile)) return [];
    try {
        const data = fs.readFileSync(dataFile, 'utf8');
        return JSON.parse(data);
    } catch (e) {
        return [];
    }
}

function saveProducts(products) {
    fs.writeFileSync(dataFile, JSON.stringify(products, null, 2));
}

// جلب المنتجات
app.get('/products', (req, res) => {
    res.json(getProducts());
});

// التحقق من كلمة السر
app.post('/verify-admin', (req, res) => {
    const { password } = req.body;
    if (password === ADMIN_PASSWORD) {
        res.json({ success: true });
    } else {
        res.json({ success: false });
    }
});

// إضافة منتج
app.post('/add', upload.single('image'), (req, res) => {
    const products = getProducts();
    const newProduct = {
        id: Date.now().toString(),
        name: req.body.name,
        category: req.body.category || 'أخرى',
        price: req.body.price,
        image: req.file ? `/uploads/${req.file.filename}` : ''
    };
    products.push(newProduct);
    saveProducts(products);
    res.redirect('/');
});

// تعديل منتج
app.post('/update/:id', upload.single('image'), (req, res) => {
    const products = getProducts();
    const index = products.findIndex(p => p.id === req.params.id);
    if (index !== -1) {
        products[index].name = req.body.name;
        products[index].category = req.body.category || 'أخرى';
        products[index].price = req.body.price;
        if (req.file) {
            products[index].image = `/uploads/${req.file.filename}`;
        }
        saveProducts(products);
    }
    res.redirect('/');
});

// حذف منتج
app.post('/delete/:id', (req, res) => {
    let products = getProducts();
    products = products.filter(p => p.id !== req.params.id);
    saveProducts(products);
    res.redirect('/');
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
