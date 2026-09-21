from app.models.user import User


class UserService:

    def __init__(self):
        self.users: dict[int, User] = {}

    def get_or_create_user(self, user_id: int) -> User:

        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)

        return self.users[user_id]

    def set_grade(self, user_id: int, grade: int):

        user = self.get_or_create_user(user_id)

        user.grade = grade

    def get_user(self, user_id: int) -> User | None:

        return self.users.get(user_id)