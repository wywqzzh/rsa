from my_rsa import RSA
import base64
from gmpy2 import mpz
import gmpy2
import io

import operator


class CBC:
    def __init__(self):
        self.rsa = RSA()
        self.M = bytearray()
        self.C = bytearray()

    def getFile(self, file):
        self.file = file

    def to_Bytes(self, p):
        # x=[]
        # while(p!=0):
        #     x.append(str(gmpy2.mod(p,2)))
        #     p//=2
        # x.append('0')
        # x.reverse()
        s= bin(p)
        z=''
        for i in range(2050-len(s)):
            z+='0'
        z+=s[2:]
        L = []
        for i in range(0, 256):
            temp = z[i * 8:i * 8 + 8]
            temp = int(temp, base=2)
            L.append(temp)
        return L

    def padding(self,B):
        Final_Results=bytearray()
        Final_Results += b'\x00'
        Final_Results+=b'\x01'
        for i in range(128-len(B)-3):
            Final_Results+=b'\xFF'
        Final_Results += b'\x00'
        Final_Results+=B
        return Final_Results
    def encrypt(self):
        f = open(self.file, 'rb')
        temp = bytearray()
        cunt = 0
        C = []
        while True:
            ch = f.read(1)
            if not ch:
                break
            temp += ch
            cunt += 1
            if cunt == 117:
                temp=self.padding(temp)
                c = self.rsa.encrypt(temp)
                C.append(c)
                cunt = 0
                temp = bytearray()
        if len(temp)!=0:
            temp=temp=self.padding(temp)
            c = self.rsa.encrypt(temp)
            C.append(c)
        f = open('C:/Users/76774/Desktop/b', 'wb')
        S = []
        for i in C:
            y = self.to_Bytes(i)
            S.append(y)
            for j in y:
                f.write(j.to_bytes(1, byteorder='big'))
        f.close()
        return C, S

    def to_binary(self, n):
        s = []
        for i in range(8):
            s.append(str(n % 2))
            n //= 2
        s.reverse()
        return ''.join(s)

    def Dpadding(self, B):
        x = 0
        for i in range(1, len(B)):
            print(B[i])
            if B[i] == 0:
                x = i
                break
        print(x)
        return B[x + 1:]
    def decrypt(self):
        pass
        f = open('C:/Users/76774/Desktop/b', 'rb')
        cunt = 0
        temp = []
        C = []
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
                C.append(mpz('0b' + ''.join(temp)))
                temp = []
        message=[]
        for i in C:
            message.append(self.rsa.decrypt(i))
        Final=bytearray()
        for m in message:
            Final+=self.Dpadding(m)
        print(len(Final))
        print(Final.decode('gbk'))
cbc = CBC()
cbc.getFile('C:/Users/76774/Desktop/a.txt')
C, S = cbc.encrypt()
cbc.decrypt()
flag = True
