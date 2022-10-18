"""
MxRy - 2016 - Wiener's attack 
useful link : http://math.unice.fr/~walter/L1_Arith/cours2.pdf
"""
import math


def DevContinuedFraction(num, denum):
    partialQuotients = []
    divisionRests = []
    for i in range(int(math.log(denum, 2)/1)):
        divisionRests = num % denum
        partialQuotients.append(num / denum)
        num = denum
        denum = divisionRests
        if denum == 0:
            break
    return partialQuotients


""" (cf. useful link p.2) Theorem :
p_-2 = 0 p_-1 = 1   p_n = a_n.p_n-1 + p_n-2
q_-2 = 1 q_-1 = 0   q_n = a_n.q_n-1 + q_n-2 
"""


def DivergentsComputation(partialQuotients):
    (p1, p2, q1, q2) = (1, 0, 0, 1)
    convergentsList = []
    for q in partialQuotients:
        pn = q * p1 + p2
        qn = q * q1 + q2
        convergentsList.append([pn, qn])
        p2 = p1
        q2 = q1
        p1 = pn
        q1 = qn
    return convergentsList


"""  
https://dzone.com/articles/cryptographic-functions-python
Be careful to physical attacks see sections below
"""


def SquareAndMultiply(base, exponent, modulus):
    binaryExponent = []
    while exponent != 0:
        binaryExponent.append(exponent % 2)
        exponent = exponent/2
    result = 1
    binaryExponent.reverse()
    for i in binaryExponent:
        if i == 0:
            result = (result*result) % modulus
        else:
            result = (result*result*base) % modulus
    return result


def WienerAttack(e, N, C):
    testStr = 42
    C = SquareAndMultiply(testStr, e, N)
    for c in DivergentsComputation(DevContinuedFraction(e, N)):
        if SquareAndMultiply(C, c[1], N) == testStr:
            FullReverse(N, e, c)
            return c[1]
    return -1


"""
Credit for int2Text : 
https://jhafranco.com/2012/01/29/rsa-implementation-in-python/
"""


def GetTheFlag(C, N, d):
    p = pow(C, d, N)
    print p
    size = len("{:02x}".format(p)) // 2
    print "Flag = "+"".join([chr((p >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])


"""
http://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
"""


def find_invpow(x, n):
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1


"""
On reprend la demo on cherche (p, q), avec la recherche des racines du P
de scd degre : x^2 - (N - phi(N) + 1)x + N
"""


def FullReverse(N, e, c):
    phi = (e*c[1]-1)//c[0]
    a = 1
    b = -(N-phi+1)
    c = N
    delta = b*b - 4*a*c
    if delta > 0:
        x1 = (-b + find_invpow((b*b - 4*a*c), 2))/(2*a)
        x2 = (-b - find_invpow((b*b - 4*a*c), 2))/(2*a)
        if x1*x2 == N:
            print "p = "+str(x1)
            print "q = "+str(x2)
        else:
            print "** Error **"
    else:
        print "** ERROR : (p, q)**"


"""
Si N, e, C en hex ::> int("0x0123456789ABCDEF".strip("0x"), 16)
"""
if __name__ == "__main__":
    C = 803966748369093233867528670117833695673019045146866931674002529382581720466964038191118280233118778917693162909504749272637492591195155393830971306115662080454967101948208729181122662448033376455217412810428221150860739111744891956071056258413939565797976786982177166776259145668693871636782829074007793365982929885590007721015679407919307454597278784981674195161328092740619373294281239315918017584677709790325315202460959006049647790786848526319418345336115633228348623643747179118075155352279546884736186472718395207758873686387097911945774041633369812537580494436666655940958749843252996591801802720436045000085843967300119690956070340746966169967868549762159240374136639389419083565794256399400183300129021073200138882121476590630811020518868942385684725157562159316602749982901807520325564058116507232844541416904622352664641645136812679754528456915712750341861801262302690574858787275654591520414601305664500910787777
    e = 0xfc2e4d12eb69a42c074d9a0ddc6b84294f1e23d6eaa0ba53e9cb60ec0db203d31bdfb90eaca38189890ad26335ad6107cd234a415bfc73fc1bbd6c5d9da65249eebb57d889f91719cfdbd535ab19d2d317ffdf075870a62c6e05aac16c9b122e1c52d7dbeb2fb683514d0f463b58a4217f2e379e5a62be06e764e043a0eac5ac6af56816af926bcc4cd826ee1cfd4157496dc024042676503cec93de45c3c5e4dd9dcf85406a3cf93a9f784b9eef6e320cd9856aefff48df52127b98da8a0d207f588ce1c58e47419554590b1fa7fa3c38034f93a3a5112b6dd5e78c181abc2d972fbcb058575789c68c03f043bd4bf48d94fa7390c77f9fc033f3f01a5162d31056eb42a07397f3485b25396f93558466fc49ef80adea1e9d6c3d9edf529be5faf014669ae5f8e02433a2474d9c92fcc468d81aa0fd641a5647d55153713783a9e5d66fe70c9c2794325b28f20b751fb49359c4a8487bbfa7efc6270b7fa0ffe277276bba14027596d129fcbdef0a82aba24855bfd2155071b52c11da2d943
    N = 0x26553fbb7e4bd5bd48868a25f24d9cc5975aa8597f82110058e687dfa10dd0114c0d2011fa288dbd9d01c0a70dfa8212d5a218d513bdd8ebed9f75bc299e1461be8a23ed8ade96bc449d409fbbf5a328ee2ad3257e6c55a97641258730f74f4d3938f0df794546791ba2b1518b8d855e83f65f885d67aa000a01687ac605404e7bca681e51e6e195f77eb4785fcda0372e3d0fd90240f736243584677f89da4c6ab54d687897d5afb0801cc151c516b072aaa2d9aa8d39d34c230536cba077beaa88ff8e8940a5ba990cafd0b1326f209873a43a785d0c5477241fb6469b8c27c7d54908467a7525de18b2425901c0de3ed63472831c29818ce6efb0354c61f36b2e61146472e99209d198bc885ced0edb66eab62a968c9b98b49b756c689d69820ca1d97e1232c338084097078265ce79b25c1e37bc777247af3fee2ce7a87a697a120c0428327177cf6e934aa2d18e696474227d361a5c36992788c3b1aa8654b88852e897027d58b21576b25a5ffdcb9fbdc5167eb74f1c9082ae79ca0b89

    print "e : "+str(e)
    print "N : "+str(N)
    print "C : "+str(C)
    d = WienerAttack(e, N, C)
    if d != -1:
        print "d = "+str(d)
        # GetTheFlag(C, N, d)
    else:
        print "** ERROR : Wiener's attack Impossible**"
