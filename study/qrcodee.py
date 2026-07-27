import qrcode

qr = qrcode.QRCode(version=5,box_size=5,border=5)
qr.add_data('hi hello')
qr.make_image(fill_color="blue",back_color="white").save('customQR.png')
# qrcode.make('mailto:nikishdaniel1@gmail.com?subject=Hello').save('qrImage.png')