from flask import render_template, flash, Markup, request, redirect, url_for, g, session
from flask_login import login_user, login_required, current_user, UserMixin, logout_user
from app import app, logman
from .forms import AuthForm, EditForm
import os
import markdown
import frontmatter
from operator import itemgetter
from werkzeug.security import check_password_hash

@app.before_request
def before_request():
    g.user = current_user

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

def listfolder(origpath,page):
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
            meta, content = frontmatter.parse(f.read())
        # turn all meta tags to lowercase
        meta = dict((k.lower(), v) for k,v in meta.items())
        # if date tag doesn't exist, add it as empty string. same with title
        if 'date' not in meta: meta['date']=''
        if 'title' not in meta: meta['title']='Untitled'
        # add link to individual post in meta
        meta['url']=os.path.join(origpath,filename)
        # get the intro text from each post
        meta['intro']=getintro(content)
        # append it to the list
        listofdata.append(meta)
    # sort the list of posts by date
    listofdata = sorted(listofdata, key=lambda k: k['date'], reverse=True)
    # check page number
    if len(listofdata)-1 < (page-1)*app.config['PER_PAGE']:
        flash('Invalid page number')
        page = len(listofdata) // app.config['PER_PAGE']
    # set up link for next and prev page
    pagenav = (page-1, page, page+1 if page*app.config['PER_PAGE'] <= len(listofdata)-1 else 0)
    # trim the data list to only contain current page
    listofdata = listofdata[(page-1)*app.config['PER_PAGE']:(page-1)*app.config['PER_PAGE']+app.config['PER_PAGE']]
    return render_template('listposts.html',
            posts=listofdata,
            folder=origpath.split('/')[-1].title(),
            pagenav=pagenav)

class User(UserMixin):
    def __init__(self,id):
        self.id = id

theonlyuser = User('onlyuser')

@logman.user_loader
def load_user(id):
    if id == 'onlyuser':
        return theonlyuser
    else:
        return None

def verify_password(password):
    with open('pass.txt','r') as f:
        hashedpass = f.read().rstrip()
    return check_password_hash(hashedpass,password)

@app.route('/auth',methods=['GET','POST'], strict_slashes=False)
def auth():
    form = AuthForm()
    if form.validate_on_submit():
        if verify_password(form.password.data):
            login_user(theonlyuser,form.remember.data)
            return redirect(request.args.get('next') or url_for('himitsu'))
        flash('Invalid Password')
    return render_template('auth.html',form=form)

@app.route('/deauth', strict_slashes=False)
def deauth():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('catch_all'))

@app.route('/himitsu', strict_slashes=False)
@app.route('/journal', strict_slashes=False)
@login_required
def himitsu():
    # getting page number
    page = request.args.get('p')
    try:
        if page != None: page = int(page)
    except ValueError:
        page = 1
        flash('Something wrong with your url...')
    if page == None: page = 1
    return listfolder('journal',page)

@app.route('/edit',defaults={'path':''}, strict_slashes=False)
@app.route('/edit/<path:path>',methods=['GET','POST'], strict_slashes=False)
@login_required
def edit(path):
    # if no file specified, list all files
    if path=='':
        data={}
        for root,dirs,files in os.walk(app.config['CONTENT_DIR'], followlinks=True):
            for ff in files:
                if not os.path.isdir(os.path.join(root,ff)) and not ff[-3:]==".md" and not ff[-7:]=='.hidden':
                    continue
                with open(os.path.join(root,ff)) as f:
                    meta, content = frontmatter.parse(f.read())
                    # turn all meta tags to lowercase
                    meta = dict((k.lower(), v) for k,v in meta.items())
                    # if date tag doesn't exist, add it as empty string
                    if 'date' not in meta: meta['date']=''
                    if 'title' not in meta: meta['title']='Untitled'
                    # add link to individual post in meta
                    meta['url']=os.path.join(os.path.relpath(root,app.config['CONTENT_DIR']),ff)
                    data[meta['url']] = meta
        return render_template('editlist.html',data=data)
    else:
        trupath=os.path.join(app.config['CONTENT_DIR'],path)
        if 'file_in_process' in session and session['file_in_process']!='':
            form = EditForm(session['file_in_process'])
        else: form = EditForm()
        if form.validate_on_submit():
            data = form.editor.data
            newfile = os.path.join(app.config['CONTENT_DIR'],form.filepath.data)
            if 'file_in_process' in session and session['file_in_process']!='':
                os.remove(os.path.join(app.config['CONTENT_DIR'],session['file_in_process']))
            with open(newfile,'w') as f:
                f.write(data)
            flash('Changes saved')
            return redirect(url_for('edit'))
        else:
            if os.path.isfile(trupath) and (trupath[-3:]=='.md' or trupath[-7:]=='.hidden'):
                with open(trupath) as f:
                    raw = f.read()
                form.editor.data=raw
                form.filepath.data=path
                session['file_in_process']=path
                return render_template('editpost.html',form=form,title=path)
            else:
                flash('Invalid URL')
                return render_template('singlepost.html')

@app.route('/add',methods=['GET','POST'], strict_slashes=False)
@login_required
def add():
    form = EditForm()
    if form.validate_on_submit():
        data = form.editor.data
        filepath = form.filepath.data
        trupath = os.path.join(app.config['CONTENT_DIR'],filepath)
        with open(trupath,'w') as f:
            f.write(data)
        flash('Changes saved')
        return redirect(url_for('edit'))
    session['file_in_process']=''
    return render_template('editpost.html',form=form,title='Add Post')

# The only function that matters
@app.route('/', defaults={'path': ''}, strict_slashes=False)
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

    # getting page number
    page = request.args.get('p')
    try:
        if page != None: page = int(page)
    except ValueError:
        page = 1
        flash('Something wrong with your url...')
    if page == None: page = 1

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
                return listfolder(path,page)
        # 404
        else:
            return showfile(os.path.join(app.config['CONTENT_DIR'],'404.md'))

    # Else they are asking for the homepage
    else:
        return showfile(os.path.join(app.config['CONTENT_DIR'],'index.md'))
