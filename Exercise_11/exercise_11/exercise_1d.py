constraint='''
 exists <Return> r:
    exists <integer> i:
        (inside(i, r) and 995 < str.to.int(i) and str.to.int(i) < 1005)
'''