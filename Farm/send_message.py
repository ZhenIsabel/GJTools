from smtplib import SMTP_SSL
from email.mime.text import MIMEText

import config_model
import log_message
import traceback

def send_message(message):
     try:
        # 填写真实的发邮件服务器用户名、密码
        receive_addr = config_model.config['email_add']
        user = 'code_test_message@163.com'
        password = 'RYXVVTELHMNPHJUY'
        # 邮件内容
        msg = MIMEText(message, 'plain', _charset="utf-8")
        msg["Subject"] = "GJTool"
        msg["from"] = user
        msg["to"] = receive_addr
        msg["Cc"] = ""
        with SMTP_SSL(host="smtp.163.com") as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr=user, to_addrs=receive_addr,
                          msg=msg.as_string())
     except:
        log_message.log_error(message)
        error_log=traceback.format_exc()
        log_message.log_error(error_log)


def send_procedure_report(message: dict, index=0):
    send_text = '简报第{0}次：'.format(index)+'\n'
    for index, key in enumerate(message):
        send_text = send_text+str(key)+':'+str(message[key])+'\n'
    send_message(send_text)
