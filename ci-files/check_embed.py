import sys
img = open(sys.argv[1],'rb').read()
magic = b'\xd0\x0d\xfe\xed'
n = img.count(magic)
print('d00dfeed occurrences:', n)
best = 0; idx = 0
while True:
    i = img.find(magic, idx)
    if i < 0: break
    if i+8 <= len(img):
        size = int.from_bytes(img[i+4:i+8],'big')
        if 0 < size <= len(img)-i: best = max(best, size)
    idx = i+1
print('largest plausible fdt size:', best)
print('image size:', len(img))