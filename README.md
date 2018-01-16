# burogu

## Overview

burogu is a super simple blog system that uses markdown files instead of a database. Built on python and flask

## Features

- No databases. Nope.
- Simple & Fast.
- Markdown formatting. No weird WYSIWYG editor.
- Built-in webui backend to manage content.
- Open source! (lol)

## Shortcomings

Well uh, since I wrote this mostly just to serve as the backend for my website, a good part of the system is hard-coded in and only serve my use case. Doesn't mean it's hard to modify, though. See the sections below for more details.

Original inspiration was from the [Pico CMS](http://picocms.org/) which has similar (and better) features. Only they didn't have a webui backend.

## Installation & Setting up

So you are curious and want to explore this spaghetti code I wrote?

Note that this instruction is only applicable to Linux (and  macOS if you know what you're doing)

- Ensure requirements are installed: Python 3, pip, virtualenv.
- `git clone https://github.com/ferb96/burogu`
- cd into repo
- `./deploy.sh` (this script will try to make a virtualenv folder named `flask`, activate the virtualenv, and install all the required packages. If it fails, try doing those manually maybe)

Installation is basically complete, however you still need to add some files for it to work

- cd into repo
- `source flask/bin/activate`
- run `python`, and type in the following commands to generate your hashed password for the backend:
- `from werkzeug.security import generate_password_hash`
- `generate_password_hash('foobar')`. Replace `foobar` with your intended password. Then copy the generated string into a file named `pass.txt` in the repo's directory.
- This is a very primitive method, I know.
- Exit python. now `mkdir content`.
- `touch content/index.md content/404.md`. These two files will be your index page, and your 404 page, respectively.

That's it! Now run it using `python run.py`. To disable verbose logging, use `python runp.py`.

## General usage

- Let's say your `content` folder looks like this:

```
content/
    blog/
        one.md
        two.md
        index.md
    private/
        secret.md
        .restricted
    projects/
        project1.md
        project2.md
        index.md
        .nolist
    about.md
    index.md
    404.md
```

- `yourdomain.com` will show the root's `index.md`
- `yourdomain.com/blog` will list out all the content of the folder in a blog post listing fashion. A short summary of the first 250 words of each md file is included. The file `index.md` will serve as the "description". You can utilize this to make multiple categories for your site, like `/blog`, `/works`, etc
- `yourdomain.com/blog/one.md` will display only that article alone.
- `yourdomain.com/private` will ask for backend password before displaying post because of the file `.restricted`. Also because the folder doesn't have an `index.md`, it will only list out all the content without a "description".
- `yourdomain.com/projects` will only display the `index.md` without listing out the files in the folder, because of the file `.nolist`. You can use this to make a folder of just individual, non-related pages.
- `yourdomain.com/about.md` will display the root's `about.md`.
- Access the backend by logging in, using `yourdomain.com/auth`.

### How to theme?

- The static resource folder is located at `app/static/`.
- The html files are in `app/template/`. Put your CSS and JS file in the static folder.
- Read up on [Jinja docs](http://jinja.pocoo.org/docs/2.10/) on how to theme

## F.A.Q.

#### Q: Why the name?

A: It's from the Japanese pronunciation of 'Blog', ブログ

#### Q: So many hardcoded stuff I don't get it!!!

A: Sorry lol. Open up a github issue so I can help you

#### Q: This code is bad / insecure and you should feel bad

A: Please I need feedback! Tell me where I screwed up.

#### Q: Why make your own while there are others out there already better?

A: I learned a bunch while doing this. I'm master of HTML and CSS now, for one (not really, but u get the point)

#### Q: Do you plan to update / add more features?

A: Only if I need it. You are welcome to fork / contribute. Or open a github issue.

I felt like I wrote too much for such a minor unimportant piece of software. If you read this far you really did have interest in this. Thanks for that!
