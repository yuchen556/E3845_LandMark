import smtplib
import ssl
def mail_Hydar_UI():
    # Mail result
    smtp_server = "smtp.sina.com"
    port = 465
    sender = "yuchen556@sina.com"
    receiver = ['556wangzhen@163.com', 'jiandong_bao@163.com']
    message = "Subject:Passed_Hydra_UI_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format("spinel_sn", sender, receiver)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, 'cd443ab65c8e8431')
        print('Mail_sent')
        server.sendmail(sender, receiver, message)

mail_Hydar_UI()

