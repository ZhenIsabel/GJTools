import time
from cv2 import threshold

import pytesseract
import cv2
from PIL import Image
import numpy as np
import imutils
import math
import re
import pyautogui
import role_move
import test
import struct
import socket
import select
import sys

current_ping_area = [539, 173, 51, 19]
# current_ping_area = [389, 173, 51, 19]
bin_threshold = 180
re_cmp = re.compile('[1-9]\d*')

# 通过检测延迟减少旋转方向误差


def get_current_ping(try_times=5):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(
        region=current_ping_area)), cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(image, bin_threshold, 255, cv2.THRESH_BINARY)
    cv2.bitwise_not(binary, binary)
    # binary = cv2.resize(
    #     binary, [current_ping_area[2]*10, current_ping_area[3]*10])
    # binary = cv2.blur(binary, (3, 3))
    test.show_imag('bin', binary)
    test_message = Image.fromarray(binary)
    # text = pytesseract.image_to_string(test_message)
    text = pytesseract.image_to_string(binary)
    print(text)
    text = text.replace('B', '8')
    # print(f'位置：{text}')
    ping_str = re_cmp.findall(text)
    # print(ping_str)
    if len(ping_str) >= 1 and abs(int(ping_str[0])) > 5:
        return int(ping_str[0])
    if try_times > 0:
        return get_current_ping(try_times-1)
    return None


def chesksum(data):
  """
  校验
  """
  n = len(data)
  m = n % 2
  sum = 0
  for i in range(0, n - m, 2):
    sum += (data[i]) + ((data[i + 1]) << 8) # 传入data以每两个字节（十六进制）通过ord转十进制，第一字节在低位，第二个字节在高位
  if m:
    sum += (data[-1])
  # 将高于16位与低16位相加
  sum = (sum >> 16) + (sum & 0xffff)
  sum += (sum >> 16) # 如果还有高于16位，将继续与低16位相加
  answer = ~sum & 0xffff
  # 主机字节序转网络字节序列（参考小端序转大端序）
  answer = answer >> 8 | (answer << 8 & 0xff00)
  return answer
 
  '''
  连接套接字,并将数据发送到套接字
  '''
 
 
def raw_socket(dst_addr, imcp_packet):
  rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
  send_request_ping_time = time.time()
  # send data to the socket
  rawsocket.sendto(imcp_packet, (dst_addr, 80))
  return send_request_ping_time, rawsocket, dst_addr

def request_ping(data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body):
  # 把字节打包成二进制数据
  imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body)
  icmp_chesksum = chesksum(imcp_packet) # 获取校验和
  imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, icmp_chesksum, data_ID, data_Sequence, payload_body)
  return imcp_packet

def reply_ping(send_request_ping_time, rawsocket, data_Sequence, timeout=2):
  while True:
    started_select = time.time()
    what_ready = select.select([rawsocket], [], [], timeout)
    wait_for_time = (time.time() - started_select)
    if what_ready[0] == []: # Timeout
      return -1
    time_received = time.time()
    received_packet, addr = rawsocket.recvfrom(1024)
    icmpHeader = received_packet[20:28]
    type, code, checksum, packet_id, sequence = struct.unpack(
      ">BBHHH", icmpHeader
    )
    if type == 0 and sequence == data_Sequence:
      return time_received - send_request_ping_time
    timeout = timeout - wait_for_time
    if timeout <= 0:
      return -1
 
  '''
  实现 ping 主机/ip
  '''


def check_ping(host='121.5.96.160',try_times=3):
    data_type = 8  # ICMP Echo Request
    data_code = 0  # must be zero
    data_checksum = 0  # "...with value 0 substituted for this field..."
    data_ID = 0  # Identifier
    data_Sequence = 1  # Sequence number
    payload_body = b'abcdefghijklmnopqrstuvwabcdefghi'  # data
    # 将主机名转ipv4地址格式，返回以ipv4地址格式的字符串，如果主机名称是ipv4地址，则它将保持不变
    dst_addr = socket.gethostbyname(host)
    for i in range(0, 1):
      for j in range(0,try_times):
        icmp_packet = request_ping(
            data_type, data_code, data_checksum, data_ID, data_Sequence + i, payload_body)
        send_request_ping_time, rawsocket, addr = raw_socket(
            dst_addr, icmp_packet)
        times = reply_ping(send_request_ping_time,
                           rawsocket, data_Sequence + i)
      if times > 0:
          # print("来自 {0} 的回复: 字节=32 时间={1}ms".format(addr, int(times * 1000)))
          # time.sleep(0.7)
          return times
      else:
          # print("请求超时。")
          return 0