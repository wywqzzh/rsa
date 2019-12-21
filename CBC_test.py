from my_rsa import RSA
import base64
from gmpy2 import mpz
import gmpy2
import random


class CBC:
    def __init__(self):
        self.rsa = RSA()
        self.M = bytearray()
        self.C = bytearray()

    def getFile(self, filename1, filename2):
        # 明文路径
        self.PlainTextFile = filename1
        # 密文路径
        self.CiphertextFile = filename2

    # 保存密钥
    def gen_keys(self, filename):
        n = str(self.rsa.n).encode('utf-8')
        e = str(self.rsa.e).encode('utf-8')
        d = str(self.rsa.d).encode('utf-8')
        public_filename = filename + '.pub'
        private_filename = filename + '.key'
        f = open(public_filename, 'wb')
        f.write(n)
        f.write('\n'.encode('utf-8'))
        f.write(e)
        f.close()
        f = open(private_filename, 'wb')
        f.write(n)
        f.write('\n'.encode('utf-8'))
        f.write(d)
        f.close()

    # 获取私钥(解密)
    def set_private_keys(self, filename):
        f = open(filename, 'r')
        x = f.read().split('\n')
        f.close()
        n = mpz(x[0])
        d = mpz(x[1])
        self.rsa.set_private_keys(n, d)

    # 获取公钥(加密)
    def set_public_keys(self, filename):
        f = open(filename, 'r')
        x = f.read().split('\n')
        f.close()
        n = mpz(x[0])
        e = mpz(x[1])
        self.rsa.set_private_keys(n, e)

    # 将mpz大整数转化为256个int,每个int一个字节
    def to_ListBytes(self, p):
        s = bin(p)
        z = ''
        for i in range(2050 - len(s)):
            z += '0'
        z += s[2:]
        L = []
        for i in range(0, 256):
            temp = z[i * 8:i * 8 + 8]
            temp = int(temp, base=2)
            L.append(temp)
        return L

    # 填充
    def padding(self, B):
        Final_Results = bytearray()
        Final_Results += b'\x00'
        Final_Results += b'\x01'
        for i in range(128 - len(B) - 3):
            Final_Results += b'\xFF'
        Final_Results += b'\x00'
        Final_Results += B
        return Final_Results

    # 生成随机初始化向量
    def gen_IV(self):
        s = '0b' + '0'
        for i in range(2047):
            x = random.randint(0, 1)
            s += str(x)
        return mpz(s)

    # 读取明文
    def load_PlainText(self):
        f = open(self.PlainTextFile, 'rb')
        temp = bytearray()
        cunt = 0
        PlainText = []
        while True:
            ch = f.read(1)
            if not ch:
                break
            temp += ch
            cunt += 1
            if cunt == 117:
                temp = self.padding(temp)
                PlainText.append(temp)
                cunt = 0
                temp = bytearray()
        if len(temp) != 0:
            temp = self.padding(temp)
            PlainText.append(temp)
        return PlainText

    # 根据明文加密成密文
    def get_Ciphertext(self, PlainText):
        Initialization_vector = self.gen_IV()
        Ciphertext = [Initialization_vector]
        for i, plaintext in enumerate(PlainText):
            plaintext_mpz = mpz(int.from_bytes(plaintext, byteorder='big'))
            C0 = Ciphertext[i]
            Encrypted_plaintext = plaintext_mpz ^ C0
            Ciphertext.append(self.rsa.encrypt(Encrypted_plaintext))
        return Ciphertext

    # 保存密文
    def save_Ciphertext(self, Ciphertext):
        f = open(self.CiphertextFile, 'wb')
        for i in Ciphertext:
            y = self.to_ListBytes(i)
            for j in y:
                f.write(j.to_bytes(1, byteorder='big'))
        f.close()

    # 加密主函数
    def encrypt(self, PlaintextFile, CiphertextFile, keysFile):
        self.getFile(PlaintextFile, CiphertextFile)
        self.set_public_keys(keysFile)
        PlainText = self.load_PlainText()
        Ciphertext = self.get_Ciphertext(PlainText)
        self.save_Ciphertext(Ciphertext)

    # 将int转为Binary(0-255)
    def to_binary(self, n):
        s = []
        for i in range(8):
            s.append(str(n % 2))
            n //= 2
        s.reverse()
        return ''.join(s)

    # 消除填充
    def Dpadding(self, B):
        x = 0
        for i in range(1, len(B)):
            if B[i] == 0:
                x = i
                break
        return B[x + 1:]

    # 保存解密出的明文
    def save_PlainText(self, PlainText):
        f = open(self.PlainTextFile, 'wb')
        f.write(PlainText)
        f.close()

    # 根据路径加载密文
    def load_Ciphertext(self):
        f = open(self.CiphertextFile, 'rb')
        cunt = 0
        temp = []
        Ciphertext = []
        while True:
            ch = f.read(1)
            if not ch:
                break
            cunt += 1
            ch = int.from_bytes(ch, byteorder='big')
            ch = self.to_binary(ch)
            temp.append(ch)
            if cunt == 256:
                cunt = 0
                Ciphertext.append(mpz('0b' + ''.join(temp)))
                temp = []
        f.close()
        return Ciphertext

    def Binary_byters(self, s):
        Z = bytearray()
        for i in range(len(s) // 8):
            temp = s[i * 8:i * 8 + 8]
            x = int(temp, base=2)
            x = x.to_bytes(1, byteorder='big')
            Z += x
        return Z

    # mpz大整数转化为bytes
    def to_Bytes(self, M):
        s = bin(M)[2:]
        z = ''
        for i in range(1024 - len(s)):
            z += '0'
        z += s
        x = self.Binary_byters(z)
        return x

    # 根据密文解密明文
    def get_PlainText(self, Ciphertext):
        PlainText = []
        for i in range(1, len(Ciphertext)):
            Decrypted_plaintext = self.rsa.decrypt(Ciphertext[i], 1)
            C0 = Ciphertext[i - 1]
            plaintext_mpz = Decrypted_plaintext ^ C0
            PlainText.append(self.to_Bytes(plaintext_mpz))
        return PlainText

    # 解密主函数
    def decrypt(self, PlaintextFile, CiphertextFile, keysFile):
        self.getFile(PlaintextFile, CiphertextFile)
        self.set_private_keys(keysFile)
        Ciphertext = self.load_Ciphertext()
        PlainText = self.get_PlainText(Ciphertext)
        MS = bytearray()
        for m in PlainText:
            MS += self.Dpadding(m)
        self.save_PlainText(MS)


cbc = CBC()
Pfile = 'C:/Users/76774/Desktop/b.jpg'
Cfile = 'C:/Users/76774/Desktop/b'
keysFile = 'C:/Users/76774/Desktop/c.key'
cbc.decrypt(Pfile, Cfile, keysFile)
