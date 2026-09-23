from app.models.user import User


class UserRepository:

    def __init__(self):
        self.users: dict[int, User] = {}

    def get(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def save(self, user: User) -> None:
        self.users[user.user_id] = user

    def get_or_create(self, user_id: int) -> User:
        user = self.get(user_id)

        if user is None:
            user = User(user_id=user_id)
            self.save(user)

        return user