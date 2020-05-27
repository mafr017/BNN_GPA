import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def kirimEmail(eemail, namaAdmin, idadmin, pswd):
    email = 'ipkbnn.donotreply@gmail.com'
    password = 'ipkPrediksi'
    send_to_email = 'madityafr3@gmail.com'
    subject = 'Bantuan Id dan Password'
    messageHTML = f'<h2>Hallo admin {namaAdmin},</h2><p>Sistem aplikasi menerima permintaan untuk mengirimkan bantuan permasalahan <em>Login</em>.<br>Berikut ini merupakan Id dan Password akun aplikasi <strong>Prediksi IPK BNN Sistem Komputer UNIKOM.</strong></p><p style="margin-left: 40px;">Id : <strong>{idadmin}</strong><br>Password : <strong>{pswd}</strong></p><p>Jangan sebarkan pesan ini kepada orang lain!</p><hr><p>Email ini dikirim secara otomatis. Mohon untuk tidak membalas email ini.</p>'
    messagePlain = 'wuubla  lublaa dub dub!!'

    msg = MIMEMultipart('alternative')
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach both plain and HTML versions
    msg.attach(MIMEText(messagePlain, 'plain'))
    msg.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()