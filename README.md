# umcu-uploader
UMCU Uploader


# Installation

UMCU Uploader is a web-based application that is built using the Python
[Flask](https://pypi.org/project/Flask/) micro-framework. Below are the
developer quickstart instructions. See [CONTRIBUTING](CONTRIBUTING.md) for
guidelines on how to contribute to the project.


## UMCU Uploader Flask server

* Clone files and cd to directory:  `git clone https://github.com/artefactual-labs/umcu-uploader.git && cd umcu-uploader`
* Clone submodules: `git submodule update --init --recursive`
* Set up virtualenv in the project root directory: `virtualenv -p python3 venv`
* Activate virtualenv: `source venv/bin/activate`
* Install requirements: `pip install -r requirements/base.txt`
* In a terminal window, start the Flask server: `python run.py`
* Confirm that the Flask server and AIPscan application are up and running at `localhost:5000` in your browser


## Configuration

System-level configuration can be changed in config.py.

Admin-level configuration can be specified in `/etc/umcu-uploader.yaml`.

Example admin-level configuration:

    ---
    divisions:
      ed:
        name: Example Division
        transfer_source_directory: /path/to/directory
      ...
