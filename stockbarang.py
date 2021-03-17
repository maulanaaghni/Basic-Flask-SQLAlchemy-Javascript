import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import csv

# konfigurasi file db
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "nyetok_barang.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)



# konfigurasi db 
class Stock(db.Model):
    namabarang = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    qytbarang = db.Column(db.Integer)
    hargabeli = db.Column(db.Integer)
    hargajual = db.Column(db.Integer)
    diskonbarang = db.Column(db.Integer)
    total = db.Column(db.Integer)
    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.namabarang,self.qytbarang,self.hargabeli,self.hargajual,self.diskonbarang,self.total)
     
#routing
#indeks - home.html
@app.route('/', methods=["GET", "POST"]) #index
def home():
    #nambah stock ke database
    csv_fileName = 'rekapBarang.csv'




    stocks = None
    if request.form:
        try:
            stock = Stock(namabarang = request.form["namabarang"],qytbarang = request.form["qytbarang"],hargabeli = int(request.form["hargabeli"]),hargajual = int(request.form["hargajual"]),diskonbarang = int(request.form["diskonbarang"]),total = int(request.form["hargajual"]) - (int(request.form["hargajual"])*(int(request.form["diskonbarang"])/100)))
            db.session.add(stock)
            db.session.commit()
            listData = []

            
            with open(csv_fileName, mode ='a') as csv_file:
                fieldnames = ['Nama','Jumlah']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                inputNamaBarang = request.form["namabarang"]
                inputJumlahBarang = request.form["qytbarang"]

                writer.writerow({'Nama':inputNamaBarang,'Jumlah':inputJumlahBarang})
            

            # with open(csv_filename, mode="r") as csv_file:
            #     csv_reader = csv.DictReader(csv_file)
            #     for row in csv_reader:
            #         listData.append(row)
            #     no = len(listData)+1
            #     indexx = 0
            #     for data in listData:
            #         if (data['Nama'] == no):
            #             listData.remove(listData[indexx])
            #         indexx = indexx + 1 






        except Exception as e:
            print("Gagal nambah Stock ")
            print(e)


    stocks = Stock.query.all()

  

    return render_template("home.html", stocks=stocks)

#Delete route 
#POST methods
@app.route("/delete", methods=["POST"]) #delete/hapus row
def delete():
    namabarang = request.form.get("namabarang")
    #commit penghapusan
    stock = Stock.query.filter_by(namabarang=namabarang).first()
    db.session.delete(stock)
    db.session.commit()
    return redirect("/")







if __name__ == "__main__":
    app.run(debug=True)