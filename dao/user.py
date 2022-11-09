from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one()

    def update_profile(self, user_d):
        user = self.get_one(user_d.get("id"))
        if user_d.get("name") is not None:
            user.name = user_d.get("name")
        if user_d.get("surname") is not None:
            user.surname = user_d.get("surname")
        if user_d.get("favorite_genre") is not None:
            user.favorite_genre = user_d.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def update_password(self, user_d):
        user = self.get_one(user_d.get("id"))
        if user_d.get("password") is not None:
            user.password = user_d.get("password")

        self.session.add(user)
        self.session.commit()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
