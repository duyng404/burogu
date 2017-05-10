from flask import render_template, flash, Markup
from app import app
import os
import markdown
import frontmatter

# Helper functions
def showfile(file):
    with open(file) as f:
        raw = f.read()
    meta = frontmatter.loads(raw)
    content = Markup(markdown.markdown(raw,['markdown.extensions.extra','markdown.extensions.meta']))
    return render_template('singlepost.html',
            meta=meta,
            content=content)

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
        if os.path.isfile(app.config['CONTENT_DIR']+'/'+path+'.md'):
            return showfile(app.config['CONTENT_DIR']+'/'+path+'.md')
        # If theres a folder
        elif os.path.isdir(app.config['CONTENT_DIR']+'/'+path):
            if os.path.isfile(app.config['CONTENT_DIR']+'/'+path+'/index.md'):
                return showfile(app.config['CONTENT_DIR']+'/'+path+'/index.md')
        # 404
        else:
            return showfile(app.config['CONTENT_DIR']+'/404.md')

    # Else they are asking for the homepage
    else:
        return showfile(app.config['CONTENT_DIR']+'/index.md')
