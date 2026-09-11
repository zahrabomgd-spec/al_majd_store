const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const dir = './uploads';
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        cb(null, dir);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage });

app.get('/products', (req, res) => {
    fs.readFile('products.json', 'utf8', (err, data) => {
        if (err) return res.json([]);
        res.json(JSON.parse(data || '[]'));
    });
});

app.post('/add', upload.single('image'), (req, res) => {
    const { name, price, category } = req.body;
    const newProduct = {
        id: Date.now().toString(),
        name,
        price,
        category: category || 'عام',
        image: req.file ? '/uploads/' + req.file.filename : ''
    };

    fs.readFile('products.json', 'utf8', (err, data) => {
        let products = err ? [] : JSON.parse(data || '[]');
        products.push(newProduct);
        fs.writeFile('products.json', JSON.stringify(products, null, 2), () => {
            res.redirect('/');
        });
    });
});

app.post('/update/:id', upload.single('image'), (req, res) => {
    const productId = req.params.id;
    const { name, price, category } = req.body;

    fs.readFile('products.json', 'utf8', (err, data) => {
        if (err) return res.status(500).send('Error');
        let products = JSON.parse(data || '[]');
        const index = products.findIndex(p => p.id === productId);

        if (index !== -1) {
            products[index].name = name || products[index].name;
            products[index].price = price || products[index].price;
            products[index].category = category || products[index].category;
            if (req.file) {
                products[index].image = '/uploads/' + req.file.filename;
            }
            fs.writeFile('products.json', JSON.stringify(products, null, 2), () => {
                res.redirect('/');
            });
        } else {
            res.status(404).send('Product not found');
        }
    });
});

app.post('/delete/:id', (req, res) => {
    const productId = req.params.id;
    fs.readFile('products.json', 'utf8', (err, data) => {
        if (err) return res.status(500).send('Error');
        let products = JSON.parse(data || '[]');
        products = products.filter(p => p.id !== productId);
        fs.writeFile('products.json', JSON.stringify(products, null, 2), () => {
            res.redirect('/');
        });
    });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
