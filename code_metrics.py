import os
import re
from optparse import OptionParser

ret_code = '\n'

class Processor(object):
    def metric(self, f):
        code = open(f).read()
        code_no_comment = self.remove_comment(code)
        # print code_no_comment
        return dict([('loc', len(code.split(ret_code))),
                     ('loc_no_comment', len(code_no_comment.split(ret_code)))] + 
                    [(k, len(re.findall(r'\b%s\b' % k, code_no_comment))) for k in self.keywords])

class Java(Processor):
    keywords = ['if', 'else', 'try', 'catch']
    def remove_comment(self, code):
        s = re.sub(r'/\*(?:.|%s)*?\*/' % ret_code, r'', code, flags=re.M)
        s = re.sub(r'^\s*//.*%s' % ret_code, r'', s, flags=re.M)
        return re.sub(r'//.*', r'', s)


processors = { ".java" : Java() }

if __name__ == '__main__':
    parser = OptionParser("usage: %prog [options] dir")
    (options, args) = parser.parse_args()
    dir = args[0]
    ext = '.java'               # only java supported for now
    processor = processors[ext]
    colnames = ['loc', 'loc_no_comment'] + processor.keywords
    print ",".join(['path'] + colnames)
    for root, dirs, files in os.walk(dir, topdown=False):
        for path in [os.path.join(root, f) for f in files if os.path.splitext(f)[1] == ext]:
            data = processor.metric(path)
            print ",".join([path] + [str(data[k]) for k in colnames])

