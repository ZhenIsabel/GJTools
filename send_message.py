from smtplib import SMTP_SSL
from email.mime.text import MIMEText

import log_message

receive_addr = "liangtianning@outlook.com"


def send_message(message):
    try:
        # 填写真实的发邮件服务器用户名、密码
        user = 'ltn1997@163.com'
        password = 'rd,jip_Ch57_q'
        # 邮件内容
        msg = MIMEText(message, 'plain', _charset="utf-8")
        msg["Subject"] = "GJTool"
        msg["from"] = "xilingyuli_test"
        msg["to"] = "GJTool"
        msg["Cc"] = ""
        with SMTP_SSL(host="smtp.163.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr=user, to_addrs=receive_addr, msg=msg.as_string())
    except:
        log_message.log_error(message)
