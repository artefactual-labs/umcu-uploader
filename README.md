# umcu-uploader

UMCU Uploader is a web-based application that is built using the Python
[Flask](https://pypi.org/project/Flask/) micro-framework. The app has been
tested on Python 3.6.9.

Below are the developer quickstart instructions. See [CONTRIBUTING](CONTRIBUTING.md)
for guidelines on how to contribute to the project.


## Installation

1. Clone files and cd to directory:

```
$ git clone https://github.com/artefactual-labs/umcu-uploader.git && cd umcu-uploader
```

2. Clone submodules:

```
$ git submodule update --init --recursive
```

3. Set up virtualenv in the project root directory:

```
$ virtualenv -p python3 venv
```

4. Activate virtualenv:

```
$ source venv/bin/activate
```

5. Install requirements:

```
$ pip install -r requirements/base.txt
```

6. In a terminal window, start the Flask server:

```
$ python run.py
```

7. The application runs on HTTP port 5000. Confirm that the Flask server and application are up and running at
`localhost:5000` in your browser.


## Configuration

System-level configuration can be changed in config.py.

Admin-level configuration can be specified in `/etc/umcu-uploader.yaml`.

Example admin-level configuration:

```
---
divisions:
  ed:
    name: Example Division
    transfer_source_directory: /path/to/directory
  ...
```


## Deployment

A fairly simple way of deploying the app is to proxy it through Nginx. This
allows the app to be accessed via TLS/SSL, basic access authentication, etc.

Instructions for deploying using uWSGI proxied through Nginx:

1. Add, to the server block of an Nginx configuration, directives to proxy to WSGI:

```
location = /uploader { rewrite ^ /uploader/; }
location /uploader { try_files $uri @uploader; }
location @uploader {
  uwsgi_pass unix:/tmp/uploader.sock;
  include uwsgi_params;
}
```

 2. Run the app using the included config file:

```
$ uwsgi uploader.ini
```
