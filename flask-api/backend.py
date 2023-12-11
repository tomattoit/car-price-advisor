from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_config = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_SERVICE": os.environ["POSTGRES_SERVICE"],
    "POSTGRES_DB": os.environ["POSTGRES_DB"],
}
print(db_config)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'postgresql://{db_config["POSTGRES_USER"]}:{db_config["POSTGRES_PASSWORD"]}@{db_config["POSTGRES_SERVICE"]}:5432/{db_config["POSTGRES_DB"]}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<People {self.name}>"


@app.route("/", methods=["GET"])
def get_people():
    people = People.query.all()
    return {"people": [person.name for person in people]}


if __name__ == "__main__":
    app.run(debug=True)
