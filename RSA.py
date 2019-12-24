import gmpy2
from gmpy2 import mpz
import binascii
import os
import random
class RSA:
    def __init__(self):
        # 大素数
        self.p, self.q = self.gen_key()
        # 公钥
        self.n = self.p * self.q


        self.e = 65537
        # n的欧拉函数
        self.phi = (self.p - 1) * (self.q - 1)

        self.d = gmpy2.invert(self.e, self.phi)

    def set_private_keys(self, n, d):
        self.n = n
        self.d = d

    def set_public_keys(self, n, e):
        self.n = n
        self.e = e

    def gen_prime(self, rs):
        """生成二进制位数为1024的随机素数"""
        p = gmpy2.mpz_urandomb(rs, 1024)
        while not gmpy2.is_prime(p):
            p = p + 1
        return p

    def gen_key(self):
        """生成密钥"""
        seed = random.randint(0, 100000000000)
        rs = gmpy2.random_state(seed)
        p = self.gen_prime(rs)
        q = self.gen_prime(rs)
        return p, q

    def encrypt(self, message):
        """将输入消息转换成16进制数字并加密，支持utf-8字符串"""
        if not isinstance(message, mpz):
            M = mpz(int.from_bytes(message, byteorder='big'))
        else:
            M = message
        C = gmpy2.powmod(M, self.e, self.n)
        return C

    def Binary_byters(self, s):
        Z = bytearray()
        for i in range(len(s) // 8):
            temp = s[i * 8:i * 8 + 8]
            x = int(temp, base=2)
            x = x.to_bytes(1, byteorder='big')
            Z += x
        return Z

    def decrypt(self, C, type):
        """对输入的密文进行解密并解码"""
        M = gmpy2.powmod(C, self.d, self.n)
        s = bin(M)[2:]
        z = ''
        for i in range(1024 - len(s)):
            z += '0'
        z += s
        x = self.Binary_byters(z)
        if type == 1:
            return M
        else:
            return x

# def main():
#     # 密钥生成
#     rsa = RSA()
#     # 输入消息
#     message = input('输入待加密的消息：\n')
#     # 加密
#     C = rsa.encrypt(message)
#     print('16进制密文：', hex(C))
#     # 解密
#     print('解密后的消息：', rsa.decrypt(C))


# if __name__ == '__main__':
#     main()
