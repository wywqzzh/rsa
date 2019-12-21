import gmpy2
from gmpy2 import mpz
import binascii
# def to_binary(n):
#     s = []
#     for i in range(8):
#         s.append(str(n % 2))
#         n //= 2
#     s.reverse()
#     return ''.join(s)
#
#
# x = 2
# y = x.to_bytes(1, byteorder='big')
# z = int.from_bytes(y, byteorder='big')
# print(z)
# z=255
# s = to_binary(z)
# print(s)
# x='\r\n\r\n\r\n\r\n'.encode('utf-8').hex()
# t=int(x,base=16)
# t=bin(t)
# z=t.to_bytes(8,byteorder='big').decode('utf-8')
# print(z)



# def Binary_byters(s):
#     Z=bytearray()
#     for i in range(len(s)//8):
#         temp=s[i*8:i*8+8]
#         x=int(temp,base=2)
#         x=x.to_bytes(1,byteorder='big')
#         Z+=x
#     return Z
# x='哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨达哈哈呵呵意义萨嗯'
# y=x.encode('gbk')
# M = gmpy2.mpz(int.from_bytes(y, byteorder='big'))
# s=bin(M)[2:]
# z=''
# for i in range(1024-len(s)):
#     z+='0'
# z+=s
# x=Binary_byters(z)
# print(x.decode('gbk'))
# print(y)





