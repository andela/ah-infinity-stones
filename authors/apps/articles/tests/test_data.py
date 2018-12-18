from ..models import User, Tag, Article



def generate_test_data():
    generate_users()
    generate_tags()


def generate_users():

    users = [{
        "username": "domnick",
        "email": "domnick@email.com",
        "password": "domnick"
    }]

    for user in users:
        new_user = User(
            username=user['username'],
            email=user['email'],
            password=user['password'])

        new_user.save()


def generate_tags():

    tags = ["kenya", "nairobi", "Andela"]

    for tag in tags:
        Tag(tag=tag).save()
