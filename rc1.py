#
# rangecoder.py : (Range Coder)  Copyright (C) 2007 Makoto Hiroi
# rc0.py : Range coder           Copyright (C) 2007 Makoto Hiroi
# Carryless rangecoder (c) 1999 by Dmitry Subbotin 
#

# constant 
ENCODE = "encodemh"
DECODE = "decodemh"
ENCODEDS = "encodeds"
DECODEDS = "decodeds"
MAX_RANGE = 0x0100000000
MIN_RANGE = 0x0001000000
MASK      = 0x00ffffffff
SHIFT     = 24
TOP_VALUE = 0x01000000
BOT_VALUE = 0x00010000
MAX_VALUE = 0xFFFFFFFF

# Byte unit input / output 
def getc(f):
    c = list(f.read(1))
    if len(c)==0: return None
    return c[0]

def getw(f):
    w=getc(f)
    w=(w<<8)+getc(f)
    return w
    
def getl(f):
    l=getc(f)
    l=(l<<8)+getc(f)
    l=(l<<8)+getc(f)
    l=(l<<8)+getc(f)
    return l
    
def putc(f, x):
    f.write(bytearray([x & 0xff]))

def putw(f, w):
     putc(f, (w >> 8) & 0xff)
     putc(f, w & 0xff)

def putl(f, l):
     putc(f, (l >> 24) & 0xff)
     putc(f, (l >> 16) & 0xff)
     putc(f, (l >> 8) & 0xff)
     putc(f, l & 0xff)
    
#
class RangeCoder:
    def __init__(self, file, mode):
        self.file = file
        if mode == ENCODE:
            self.range = MAX_RANGE
            self.buff = 0
            self.cnt = 0
            self.low = 0
        elif mode == DECODE:
            self.range = MAX_RANGE
            self.buff = 0
            self.cnt = 0
            # buff Initial value of (0) Read away 
            getc(self.file)
            # 4 byte read
            self.low = getl(self.file)
        else:
            raise "RangeCoder mode error"

    def encode_normalize(self):
        if self.low >= MAX_RANGE:
            # Carry 
            self.buff += 1
            self.low &= MASK
            if self.cnt > 0:
                putc(self.file, self.buff)
                for _ in range(self.cnt - 1): putc(self.file, 0)
                self.buff = 0
                self.cnt = 0
        while self.range < MIN_RANGE:
            if self.low < (0xff << SHIFT):
                putc(self.file, self.buff)
                for _ in range(self.cnt): putc(self.file, 0xff)
                self.buff = (self.low >> SHIFT) & 0xff
                self.cnt = 0
            else:
                self.cnt += 1
            self.low = (self.low << 8) & MASK
            self.range <<= 8

    def decode_normalize(self):
        while self.range < MIN_RANGE:
            self.range <<= 8
            self.low = ((self.low << 8) + getc(self.file)) & MASK

    def finish(self):
        c = 0xff
        if self.low >= MAX_RANGE:
            # Carry 
            self.buff += 1
            c = 0
        putc(self.file, self.buff)
        for _ in range(self.cnt): putc(self.file, c)
        #
        putl(self.file, self.low)

    def fencode(self, cum_freq, freq, tot_freq):
        temp = self.range // tot_freq
        self.low += cum_freq * temp
        self.range = freq * temp
        self.encode_normalize()

    def freq_get(self, tot_freq): # range goes TEMP
        self.range //= tot_freq
        return self.low // self.range

    def fdecode(self, cum_freq, freq): # range is TEMP=range/tot_freq
        self.low -= self.range * cum_freq
        self.range *= freq
        self.decode_normalize()

class RangeCoderDS:
    def __init__(self, file, mode):
        self.file = file
        if mode == ENCODE:
            self.range = MAX_VALUE
            self.low = 0
        elif mode == DECODE:
            self.range = MAX_VALUE
            self.low = 0
            self.code = getl(self.file)
        else:
            raise "RangeCoder mode error"

    def encode_normalize(self):
        r=self.range
        l=self.low
        while (r < TOP_VALUE and ((l ^ (l+r)) < TOP_VALUE  or 
             r < BOT_VALUE and ((r:=-l & BOT_VALUE-1) or True))):
            putc(self.file,l>>24)
            r<<=8
            l<<=8
        self.range=r
        self.low=l

    def decode_normalize(self):
        r=self.range
        l=self.low
        code=self.code
        while (r < TOP_VALUE and ((l ^ l+r) < TOP_VALUE  or 
             r < BOT_VALUE and ((r:=-l & (BOT_VALUE-1)) or 1))):
            code=(code<<8)+getc(self.file)
            r<<=8
            l<<=8
        self.range=r
        self.low=l
        self.code=code

    def finish(self):
        putw(self.file, self.low)

    def fencode(self, cum_freq, freq, tot_freq):
        temp = self.range // tot_freq
        self.low += cum_freq * temp
        self.range = freq * temp
        self.encode_normalize()

    def freq_get(self, tot_freq): # range goes TEMP
        self.range //= tot_freq
        return (self.code-self.low) // self.range

    def fdecode(self, cum_freq, freq): # range is TEMP=range/tot_freq
        self.low -= self.range * cum_freq
        self.range *= freq
        self.decode_normalize()


# Appearance frequency table 
class Freq:
    def __init__(self, count):
        size = len(count)
        self.size = size
        m = max(count)
        # Fit in 2 bytes 
        if m > 0xffff:
            self.count = [0] * size
            n = 0
            while m > 0xffff:
                m >>= 1
                n += 1
            for x in range(size):
                if count[x] != 0:
                    self.count[x] = (count[x] >> n) | 1
        else:
            self.count = count[:]
        self.count_sum = [0] * (size + 1)
        # Cumulative frequency table 
        for x in range(size):
            self.count_sum[x + 1] = self.count_sum[x] + self.count[x]

    def get_table(self):
        return self.count

    def total(self):
        return self.count_sum[self.size]

    def get(self, c):
        return self.count_sum[c], self.count[c]
    
    def search(self,value):
        i=0
        j=self.size-1
        while i < j:
            k = (i + j) // 2
            if self.count_sum[k + 1] <= value:
                i = k + 1
            else:
                j = k
        return i


import time, sys, getopt, os.path

def write_count_table(fout,count):
        for x in count:
            putw(fout, x)
    
def read_count_table(fin):
    count = [0] * 256
    for x in range(256):
        count[x] = getw(fin)
    return count

def read_file(fin):
    while True:
        c = getc(fin)
        if c is None: break
        yield c

def encode(fin, fout):
    count = [0] * 256
    print("read input for table")
    for x in read_file(fin):
        count[x] += 1
    rc = RangeCoderDS(fout, ENCODE)
    freq = Freq(count)
    ftot = freq.total()
#    print("write freq table")
#    write_count_table(fout,freq.get_table())
    fin.seek(0)
    print("encode")
    for x in read_file(fin):
        cumf,fq=freq.get(x)
        rc.fencode(cumf,fq,ftot)
    print("write final code")
    rc.finish()

def decode(fin, fout, size):
    print("read freq table")
    freq = Freq(read_count_table(fin))
    print("read initial code")
    rc = RangeCoderDS(fin, DECODE)
    ftot=freq.total()
    print("decode, freqtot:",ftot)
    for _ in range(size):
        f=rc.freq_get(ftot)
        c=freq.search(f)
        cumf,fq=freq.get(c)
        rc.fdecode(cumf,fq)
        putc(fout,c)

def encode_file(name1, name2):
    size = os.path.getsize(name1)
    infile = open(name1, "rb")
    outfile = open(name2, "wb")
#    print("write size")
#    putl(outfile, size)
    if size > 0: encode(infile, outfile)
    infile.close()
    outfile.close()

def decode_file(name1, name2):
    infile = open(name1, "rb")
    outfile = open(name2, "wb")
    print("read size")
    size = getl(infile)
    print("decodesize",size)
    if size > 0: decode(infile, outfile, size)
    infile.close()
    outfile.close()

#
def main():
    eflag = False
    dflag = False
    opts, args = getopt.getopt(sys.argv[1:], 'ed')
    for x, y in opts:
        if x == '-e' or x == '-E':
            eflag = True
        elif x == '-d' or x == '-D':
            dflag = True
    if eflag and dflag:
        print('option error')
    elif eflag:
        encode_file(args[0], args[1])
    elif dflag:
        decode_file(args[0], args[1])
    else:
        print('option error')

#
#s = time.clock()
#main()rc0.py
#encode_file("Cbios_8x8.bin", "Cbios_8x8.rc0")
#decode_file("Cbios_8x8.rc0", "Cbios_8x8.bn")
encode_file("README.md", "README.rc0")
#decode_file("README.rc0", "README.dat")
#e = time.clock()
#print("{:.3f}".format(e - s))

