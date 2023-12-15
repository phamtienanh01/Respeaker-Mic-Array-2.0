const mongoClient = require('mongodb').MongoClient;

mongoClient.connect('mongodb+srv://Phamtienanh0:Phamtienanh0@cluster0.o3w7mgf.mongodb.net/?retryWrites=true&w=majority', function (err, db) {
  if (err) throw err;

  const products = db.collection('products');

  products.findOne({ name: 'ao-thun' }, function (err, res) {
    if (err) throw err;

    console.log(res);

    db.close();
  });
});