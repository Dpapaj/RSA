from tkinter import *
from tkinter.ttk import Combobox

import random

window = Tk()



def rabinMiller(n,d):
    a = random.randint (2,(n - 2) - 2)
    x = pow (a,int (d),n)  # a^d%n
    if x == 1 or x == n - 1:
        return True

    # čtverec x
    while d != n - 1:
        x = pow (x,2,n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True

    # není prvočíslo
    return False


def isPrime(n):
    """
        návrat True, pokud n je prvočíslo,jinak vrácení k rabinMillerovi
    """

    # 0, 1, -čísla nejsou prvočísla
    if n < 2:
        return False

    # malá prvočísla pro rychlejší zpracování
    lowPrimes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
                 139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,
                 277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,
                 433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,
                 599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                 757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,
                 937,941,947,953,967,971,977,983,991,997]

    # jestli je malé prvočísla
    if n in lowPrimes:
        return True

    # malé prvočísla dělíme na n
    for prime in lowPrimes:
        if n % prime == 0:
            return False

    # nacházení čísla c, jako c * 2 ^ r = n - 1
    c = n - 1  # c jako c n nedělitelná 2
    while c % 2 == 0:
        c /= 2  # udělání c liché

    # test jestli čísla nejsou prvočísla
    for i in range (128):
        if not rabinMiller (n,c):
            return False

    return True


def generateKeys(keysize=1024):
    e = d = N = 0

    # prvočísla nums, p & q
    p = generateLargePrime (keysize)
    q = generateLargePrime (keysize)

    p_text.set(p)
    q_text.set(q)

    N = p * q  # RSA Modul
    N_text.set(N)
    phiN = (p - 1) * (q - 1)

    # vybrání e
    # e je coprime s phiN & 1 < e <= phiN
    while True:
        e = random.randrange (2 ** (keysize - 1),2 ** keysize - 1)
        e_text.set(e)
        if (isCoPrime (e,phiN)):
            break

    # vybrání d
    # d je mod inv z e s phiN, e * d (mod phiN) = 1
    d = modularInv (e,phiN)
    d_text.set(d)

    return e,d,N


def generateLargePrime(keysize):
    """
        vrátit náhodně velké prvočíslo bitů velikosti klíče
    """

    while True:
        num = random.randrange (2 ** (keysize - 1),2 ** keysize - 1)
        if (isPrime (num)):
            return num


def isCoPrime(p,q):
    """
        return True, pokud je gcd(p, q) 1 relativně prvočíslo
    """

    return gcd (p,q) == 1


def gcd(p,q):
    """
        euklidovský algoritmus k nalezení gcd p a q
    """

    while q:
        p,q = q,p % q
    return p


def egcd(a,b):
    s = 0;
    old_s = 1
    t = 1;
    old_t = 0
    r = b;
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r,r = r,old_r - quotient * r
        old_s,s = s,old_s - quotient * s
        old_t,t = t,old_t - quotient * t

    # vrácení gcd, x, y
    return old_r,old_s,old_t


def modularInv(a,b):
    gcd,x,y = egcd (a,b)

    if x < 0:
        x += b

    return x


def encrypt(e,N,msg):
    cipher = ""

    for c in msg:
        m = ord (c)
        cipher += str (pow (m,e,N)) + " "

    return cipher


def decrypt(d,N,cipher):
    msg = ""

    parts = cipher.split ()
    for part in parts:
        if part:
            c = int (part)
            msg += chr (pow (c,d,N))

    return msg

def type_change(event):
    if combobox1.get() == "Šifrovat":
        before_entry.configure(state='normal')
        after_entry.configure(state='readonly')
        encrypt_button.configure(text="Šifrovat")

    elif combobox1.get() == "Dešifrovat":
        after_entry.configure(state='normal')
        before_entry.configure(state='readonly')
        encrypt_button.configure (text="Dešifrovat")


window.title('RSA šifra')
window.geometry("500x250")

combobox1 = Combobox (window,
                      values=(
                          'Šifrovat','Dešifrovat'
                      ),state='readonly',width=10)
combobox1.grid (row=6,column=0,sticky="w",pady=5,padx=10,columnspan=2)
combobox1.set ("Šifrovat")
combobox1.bind('<<ComboboxSelected>>', type_change)

Label(window, text='e').place(x=50,y=7)
e_text = IntVar()
e_entry = Entry(window, textvariable=e_text, state='readonly', width=21)
e_entry.grid(row=0, column=1, sticky="w")

Label(window, text='d').place(x=50,y=37)
d_text = IntVar()
d_entry = Entry(window, textvariable=d_text, state='readonly', width=21)
d_entry.grid(row=1, column=1, sticky="w")

Label(window, text='N').place(x=50,y=62)
N_text = IntVar()
N_entry = Entry(window, textvariable=N_text, state='readonly', width=21)
N_entry.grid(row=2, column=1, sticky="w")

Label(window, text='p').grid(row=0, column=2, padx=10, pady=5, sticky="w")
p_text = IntVar()
p_entry = Entry(window, textvariable=p_text, state='readonly', width=13)
#p_entry.grid(row=0, column=3, sticky="w")
p_entry.place(x=230,y=5)

Label(window, text='q').grid(row=1, column=2, padx=10, pady=5, sticky="w")
q_text = IntVar()
q_entry = Entry(window, textvariable=q_text, state='readonly', width=13)
#q_entry.grid(row=1, column=3,sticky="w")
q_entry.place(x=230,y=37)

Label(window, text='Šířka klíče').grid(row=3, column=0, padx=7, pady=5, sticky="w")
key_text = IntVar()
key_entry = Entry(window, textvariable=key_text, width=13)
key_entry.grid(row=3, column=1, sticky="w")
key_text.set(30)

first_label = Label(window, text='Text')
first_label.grid(row=4, column=0, padx=0, pady=5, columnspan=2, sticky="w")
before_text = StringVar()
before_entry = Entry(window, textvariable=before_text,width=28)
before_entry.grid(row=5, column=0, columnspan=2, padx=10, sticky="w")


second_label = Label(window, text='Zašifrovaný text')
second_label.grid(row=4, column=2, padx=0, pady=5, columnspan=2, sticky="w")
after_text = StringVar()
after_entry = Entry(window, textvariable=after_text, state='readonly', width=40)
after_entry.grid(row=5, column=2, columnspan=2, sticky="w")



def onclick_crypt():
    after_entry.configure(state='readonly')

    if combobox1.get() == "Šifrovat":
        after_text.set (encrypt (e_text.get(),N_text.get(),before_text.get()))
    elif combobox1.get()=="Dešifrovat":
        before_text.set (decrypt (d_text.get (),N_text.get(),after_text.get()))




def onclick_numgen():
    keysize=key_text.get()
    generateKeys(keysize)


encrypt_button = Button(window, text='Šifrovat', command=onclick_crypt)
encrypt_button.grid(row=6, column=2, padx=5, pady=5, columnspan=2, sticky="w")

decrypt_button = Button(window, text='Vygenerovat klíč', command=onclick_numgen)
decrypt_button.grid(row=3, column=2, padx=0, pady=10, columnspan=2, sticky="w")

window.mainloop()
