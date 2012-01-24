import os
import re
import stat
from optparse import OptionParser
from datetime import datetime

ret_code = '\n'

class Processor(object):
    def metric(self, f):
        code = open(f).read()
        code_no_comment = self.remove_comment(code)
        # print code_no_comment
        return dict([('loc', len(code.split(ret_code))),
                     ('loc_no_comment', len(code_no_comment.split(ret_code)))] + 
                    [(k, len(re.findall(r'\b%s\b' % k, code_no_comment))) for k in self.keywords])
    def remove_comment(self, code):
        s = re.sub(r'%s(?:.|%s)*?%s' % (re.escape(self.comment_region_start), ret_code, re.escape(self.comment_region_end)),
                   r'', code, flags=re.M)
        if self.comment_line:
            s = re.sub(r'^\s*%s.*%s' % (re.escape(self.comment_line), ret_code), r'', s, flags=re.M)
            s = re.sub(r'%s.*' % re.escape(self.comment_line), r'', s)
        return s

class Java(Processor):
    """Processor class for Java"""
    keywords = ['if', 'else', 'try', 'catch', 'finally']
    comment_region_start = '/*'
    comment_region_end   = '/*'
    comment_line         = '//'

class CPP(Processor):
    """Processor class for C++"""
    keywords = ['if', 'else', 'try', 'catch']
    comment_region_start = '/*'
    comment_region_end   = '/*'
    comment_line         = '//'

class C(Processor):
    """Processor class for C"""
    keywords = ['if', 'else']
    comment_region_start = '/*'
    comment_region_end   = '/*'
    comment_line         = None

processors = { ".java" : Java(),
               ".cpp" : CPP(),
               ".cc" : CPP(),
               ".c" : C()}

if __name__ == '__main__':
    parser = OptionParser("usage: %prog [options] dir")
    (options, args) = parser.parse_args()
    dir = args[0]
    data = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for path in [os.path.join(root, f) for f in files]:
            ext = os.path.splitext(path)[1]
            if not ext in processors:
                continue
            d = processors[ext].metric(path)
            d['path'] = path
            mod_dt = datetime.fromtimestamp(os.stat(path).st_mtime)
            d['mod_date'] = mod_dt.date()
            d['mod_time'] = mod_dt.time()
            data.append(d)

    colnames = ['loc', 'loc_no_comment'] + list(reduce(set.union, [set(x.keywords) for x in processors.values()]))
    keys = ['path', 'mod_date', 'mod_time'] + colnames
    print ",".join(keys)
    for d in data:
        print ",".join([str(d.get(k, 0)) for k in keys])

