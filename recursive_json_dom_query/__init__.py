
from lxml import html
import json
import re
import jsonpath_rw_ext as jp

with open("index.html", 'rb') as f:
    data = f.read()


def js_comment_clean(js):
    js = re.sub("<!--[\\s\\S]*?(?:-->)?","",js)
    js = re.sub("<!--[\\s\\S]*?-->?","",js)
    js = re.sub('<!---+>?','',js)
    js = re.sub("|<!(?![dD][oO][cC][tT][yY][pP][eE]|\\[CDATA\\[)[^>]*>?","",js)
    js = re.sub("|<[?][^>]*>?","",js)
    return js

root = html.fromstring(js_comment_clean(data))

def dom_recurse(node,tags):

    temp_obj = []
    i=0
    for childnode in node:
        child_obj = []

        if  childnode.tag  not in tags:

            attr={}
            for key,value in childnode.attrib.iteritems():
                attr[key]=value

            child_obj.append({"child":dom_recurse(childnode,tags),"tag":childnode.tag,"text": childnode.text,"attr": attr})
        i = i + 1
        temp_obj.append(child_obj[0])
    return temp_obj

print json.dumps(dom_recurse(root,['']))
print jp.match('$.[0].child.[*].text',dom_recurse(root,['']))