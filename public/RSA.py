import rsa

def encrypt(data):
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(b"""-----BEGIN PUBLIC KEY-----               
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC75wr1oiN8lZ+18GngYMzEejUv
    wIhqVrs3Ek15igModCkFozENLpWKfkvF9byG3XmFDO2QbV8WVLY/laFKo1yyS9DE
    XAoQLgUPwqyTJ9CaBEyLrYG+RkXpp/MYDgp7wO1/Oi+Oa0pRRWVAHco9sUz4RX4q
    wdYSa8fjeVt7TckkUQIDAQAB
    -----END PUBLIC KEY-----""")





    return rsa.encrypt(data, pubkey)
