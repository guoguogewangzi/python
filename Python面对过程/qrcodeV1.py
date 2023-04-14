import qrcode
img=qrcode.make('http://python123.io')
img.save("qr.png")