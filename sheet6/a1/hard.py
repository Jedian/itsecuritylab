st = "abcdefghijklmnopqrstuvwxyz"
passs = ""
for local5 in range(8):
    local16 = 26
    local12 = local5**2
    passs += st[((local12^0x6f56df77)%local16)]

print passs
