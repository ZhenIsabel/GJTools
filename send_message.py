from smtplib import SMTP_SSL
from email.mime.text import MIMEText

import config_model
import log_message

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


def send_procedure_report_test(open_count, weather_code, map_count):
    weather = ['晴', '雨', '夜']
    send_text = '''任务简报：{0}
以下是本次执行的任务简报：
开盒次数: {0}
天气: {1}
买图数量:{2}
每天有个好心情~'''.format(open_count, weather[weather_code], map_count)
    send_message(send_text)


def send_procedure_report(message: dict, index=0):
    send_text = '简报第{0}次：'.format(index)+'\n'
    for index, key in enumerate(message):
        send_text = send_text+str(key)+':'+str(message[key])+'\n'
    send_message(send_text)
