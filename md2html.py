import sys

import markdown
import os


def md2html(mdstr):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']

    html = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link rel="stylesheet" href="/static/css/style.css" type="text/css" charset="utf-8"/>
    <link rel="stylesheet" href="/static/css/github-markdown.css" type="text/css" charset="utf-8"/>
    <link rel="stylesheet" href="/static/css/prism.css" type="text/css" charset="utf-8"/>
    <script src="/static/js/prism.js" type="text/javascript"
            charset="utf-8"></script>
    <title>{{ title }}</title>
</head>
<body>
<div class="markdown-body">
    %s
</div>
</body>
</html>
    '''
    ret = markdown.markdown(mdstr, extensions=exts)
    return html % ret


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(f'usage: {sys.argv[0]} source_filename target_file')
        sys.exit()

    infile = open(sys.argv[1], 'r', encoding="utf-8")
    md = infile.read()
    infile.close()

    if os.path.exists(sys.argv[2]):
        os.remove(sys.argv[2])

    outfile = open(sys.argv[2], 'a', encoding="utf-8")
    outfile.write(md2html(md))
    outfile.close()

    print('convert %s to %s success!' % (sys.argv[1], sys.argv[2]))
