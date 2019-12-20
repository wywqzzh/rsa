import gmpy2
from gmpy2 import mpz
import binascii


class RSA:
    def __init__(self):
        # 大素数
        self.p, self.q = self.gen_key()
        # 公钥
        self.n = self.p * self.q

        # 私钥
        self.e = 65537
        # n的欧拉函数
        self.phi = (self.p - 1) * (self.q - 1)

        self.d = gmpy2.invert(self.e, self.phi)

    def gen_prime(self,rs):
        """生成二进制位数为1024的随机素数"""
        p = gmpy2.mpz_urandomb(rs, 1024)
        while not gmpy2.is_prime(p):
            p = p + 1
        return p

    def gen_key(self):
        """生成密钥"""
        rs = gmpy2.random_state()
        p = self.gen_prime(rs)
        q = self.gen_prime(rs)
        return p, q

    def encrypt(self, message):
        """将输入消息转换成16进制数字并加密，支持utf-8字符串"""
        M = mpz(int.from_bytes(message, byteorder='big'))
        # M = mpz(binascii.hexlify(message.encode('utf-8')), 16)
        C = gmpy2.powmod(M, self.e, self.n)
        return C

    def Binary_byters(self,s):
        Z = bytearray()
        for i in range(len(s) // 8):
            temp = s[i * 8:i * 8 + 8]
            x = int(temp, base=2)
            x = x.to_bytes(1, byteorder='big')
            Z += x
        return Z

    def decrypt(self,C):
        """对输入的密文进行解密并解码"""
        M = gmpy2.powmod(C, self.d, self.n)
        s = bin(M)[2:]
        z = ''
        for i in range(1024 - len(s)):
            z += '0'
        z += s
        x = self.Binary_byters(z)
        # y=x.to_bytes(8,byteorder='big').decode('gbk')
        return x
        # return binascii.unhexlify(format(M, 'x')).decode('utf-8')



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