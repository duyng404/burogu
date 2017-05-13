from flask import render_template, flash, Markup
from app import app
import os
import markdown
import frontmatter
from operator import itemgetter

# Helper functions
def showfile(file):
    with open(file) as f:
        raw = f.read()
    meta = frontmatter.loads(raw)
    content = Markup(markdown.markdown(raw,['markdown.extensions.extra','markdown.extensions.meta']))
    meta.metadata = dict((k.lower(), v) for k,v in meta.metadata.items())
    return render_template('singlepost.html',
            meta=meta,
            content=content)

def mdfileexists(path):
    for filename in os.listdir(path):
        if filename[-3:]==".md":
            return True

def getintro(text):
    i=0
    res=[]
    for word in text.split():
        res.append(word)
        i+=1
        if i>app.config['INTRO_LENGTH']: break
    return ' '.join(res)


def listfolder(origpath):
    path=os.path.join(app.config['CONTENT_DIR'],origpath)
    # List of all the posts that will be sent to template
    listofdata = []
    # Loop through all md files in directory
    for filename in os.listdir(path):
        # If it's a dir or not a md file, then skip
        if os.path.isdir(os.path.join(path,filename)) or filename[-3:]!=".md":
            continue
        # open and parse through frontmatter
        with open(os.path.join(path,filename)) as f:
            raw = f.read()
        meta, content = frontmatter.parse(raw)
        # turn all meta tags to lowercase
        meta = dict((k.lower(), v) for k,v in meta.items())
        # if date tag doesn't exist, add it as empty string
        if 'date' not in meta: meta['date']=''
        # add link to individual post in meta
        meta['url']=os.path.join(origpath,filename)
        # get the intro text from each post
        meta['intro']=getintro(content)
        # append it to the list
        listofdata.append(meta)
    # sort the list of posts by date
    listofdata = sorted(listofdata, key=lambda k: k['date'], reverse=True)
    return render_template('listposts.html',
            posts=listofdata,
            folder=origpath.split('/')[-1].title())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Trim last '/' from path
    if path and path[-1]=='/':
        path=path[:-1]

    # Trim any file extension
    if len(path)>=3 and path[-3:]=='.md':
        path=path[:-3]
    if len(path)>=4 and path[-4:]=='.html':
        path=path[:-4]

    # Pages other than index
    if path and path!='index':
        # If theres a md file
        if os.path.isfile(os.path.join(app.config['CONTENT_DIR'],path+'.md')):
            return showfile(os.path.join(app.config['CONTENT_DIR'],path+'.md'))
        # If theres a folder
        elif os.path.isdir(os.path.join(app.config['CONTENT_DIR'],path)):
            # If there is an index.md in the folder
            if os.path.isfile(os.path.join(app.config['CONTENT_DIR'],path,'index.md')):
                return showfile(os.path.join(app.config['CONTENT_DIR'],path,'index.md'))
            # If not, are there any md file at all? If there is, list all the md files
            if mdfileexists(os.path.join(app.config['CONTENT_DIR'],path)):
                return listfolder(path)
        # 404
        else:
            return showfile(os.path.join(app.config['CONTENT_DIR'],'404.md'))

    # Else they are asking for the homepage
    else:
        return showfile(os.path.join(app.config['CONTENT_DIR'],'index.md'))
