import os
import re
from optparse import OptionParser

parser = OptionParser("usage: %prog [options] dir")
(options, args) = parser.parse_args()

dir = args[0]
ext = ".java"
ret_code = '\n'
keywords = ['if', 'else']

def remove_comment(code):
    s = re.sub(r'/\*(?:.|%s)*?\*/' % ret_code, r'', code, flags=re.M)
    s = re.sub(r'^\s*//.*%s' % ret_code, r'', s, flags=re.M)
    return re.sub(r'//.*', r'', s)

def metric(f):
    code = open(f).read()
    code_no_comment = remove_comment(code)
    # print code_no_comment
    return dict([('loc', len(code.split(ret_code))),
                 ('loc_no_comment', len(code_no_comment.split(ret_code)))] + 
                [(k, len(re.findall(r'\b%s\b' % k, code_no_comment))) for k in keywords])

colnames = ['loc', 'loc_no_comment'] + keywords
print ",".join(['path'] + colnames)
for root, dirs, files in os.walk(dir, topdown=False):
    for path in [os.path.join(root, f) for f in files if os.path.splitext(f)[1] == ext]:
        data = metric(path)
        print ",".join([path] + [str(data[k]) for k in colnames])

