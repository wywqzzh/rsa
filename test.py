import gmpy2
from gmpy2 import mpz
import binascii


def gen_prime(rs):
    """生成二进制位数为1024的随机素数"""
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p


def gen_key():
    """生成密钥"""
    rs = gmpy2.random_state()
    p = gen_prime(rs)
    q = gen_prime(rs)
    return p, q


def encrypt(e, n, message):
    """将输入消息转换成16进制数字并加密，支持utf-8字符串"""
    M = mpz(binascii.hexlify(message.encode('utf-8')), 16)
    C = gmpy2.powmod(M, e, n)
    return C


def decrypt(d, n, C):
    """对输入的密文进行解密并解码"""
    M = gmpy2.powmod(C, d, n)
    return binascii.unhexlify(format(M, 'x')).decode('utf-8')


def main():
    # 密钥生成
    p, q = gen_key()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = gmpy2.invert(e, phi)

    # 输入消息
    message = input('输入待加密的消息：\n')

    # 加密
    C = encrypt(e, n, message)
    print('16进制密文：', hex(C))

    # 解密
    print('解密后的消息：', decrypt(d, n, C))


if __name__ == '__main__':
    main()
