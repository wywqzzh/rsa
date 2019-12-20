#coding:utf-8
import random
__author__ = 'Kerne0'
class RSA:
    def __init__(self):
        self.p=0#大素数P
        self.q=0#大素数Q
        self.n=0#p*q
        self.nx=0#(p-1)*(q-1)
        self.e=0#公钥
        self.d=0#私钥

    #计算a*b%n
    def ModMul(self,a,b,n):
        res=0
        while(b):
            if(b&1):
                res=(res+a)%n
            a=(a+a)%n
            b=b>>1
        return res

    #a^b % n
    def ModExp(self,a,b,n):
        res=1
        a=int(a)
        b=int(b)
        n=int(n)
        while(b):
            if(b&int(1)):
                res=self.ModMul(res,a,n)
            a=self.ModMul(a,a,n)
            b=b>>1
        return res

    #MillersRabin素性测试
    def MillersRabin(self,n):
        for x in range(10):#可以自定义次数
            a=random.randint(2,n-1)
            if self.ModExp(a,n-1,n)!=1:
                return False
        return True

    #随机数产生
    def PrimeRandom(self,m=0):
        flag=True
        while(flag):
            for x in range(12):
                y=random.randint(0,9)
                m=m*10+y
            flag=not(self.MillersRabin(m))
            if flag==True:
                m=0
        return m

    #计算e,辗转相除法
    def CalculationE(self,nx):
        y=0
        while(True):
            for x in range(5):
                r=random.randint(1,9)
                y=y*10+r
            a=y
            while(nx%a!=0):
                a,nx=nx%a,a
            if a==1:
                break
            y=0
        return  y

    #扩展的欧几里德算法
    def EGcd(self,a,b,x,y):
        if b==0:
            x[0]=1
            y[0]=0
            return a
        ans=self.EGcd(b,a%b,x,y)
        temp=x[0]
        x[0]=y[0]
        y[0]=temp-a/b*y[0]
        return ans

    #计算d
    def Cal(self,a,m):
        x=[0]
        y=[0]
        gcd=self.EGcd(a,m,x,y)
        if 1%gcd!=0:
            return -1
        x[0]*=1/gcd
        m=abs(m)
        ans=x[0]%m
        if ans<=0:
            ans+=m
        return ans

    #生成公私钥
    def rsa(self):
        self.p=self.PrimeRandom()
        print("大素数P:     ",self.p)
        self.q=self.PrimeRandom()
        print ("大素数Q:     ",self.q)
        self.n=self.p*self.q
        print ("P与Q乘积:    ",self.n)
        self.nx=(self.p-1)*(self.q-1)
        print ("(p-1)*(q-1)  ",self.nx)
        self.e=self.CalculationE(self.nx)
        print ("e            ",self.e)
        self.d=self.Cal(self.e,self.nx)
        print ("d            ",self.d)

    #加解密测试
    def RSAT(self,stringM):
        print ('明文:',stringM)
        #将字符串stringM转换为列表lm
        lm=[]
        for x in stringM:
            lm.append(ord(x))
        #将每个字符的ASC值加密存入lc
        lc=[]
        stringC=''

        for m in lm:
            mx=self.ModExp(m,self.e,self.n)
            lc.append(mx)
            stringC+=str(mx)
        print ('密文:',stringC)
        #将密文解密,存入lx列表中
        lx=[]
        for c in lc:
            lx.append(self.ModExp(c,self.d,self.n))
        #将列表转换为字符串并输出
        string=''
        for ch in lx:
            string+=chr(ch)
        print ('解密:',string)
if __name__=="__main__":
    s=RSA()
    s.rsa()
    x='hello world'
    s.RSAT(x)