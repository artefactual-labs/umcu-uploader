import os

from uploader import create_app

config_name = os.environ.get("FLASK_CONFIG", "default")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])
