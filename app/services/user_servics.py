class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_or_create_user(self, user_id: int):
        return self.user_repository.get_or_create(user_id)

    def get_user(self, user_id: int):
        return self.user_repository.get(user_id)

    def set_grade(self, user_id: int, grade: int):
        user = self.get_or_create_user(user_id)
        user.grade = grade

        self.user_repository.save(user)

    def change_grade(self, user_id: int, grade: int):
        user = self.get_or_create_user(user_id)

        user.grade = grade
        user.olympiads.clear()
        user.edit_mode = None

        self.user_repository.save(user)

    def toggle_subject(self, user_id: int, subject: str):
        user = self.get_or_create_user(user_id)

        if subject in user.subjects:
            user.subjects.remove(subject)
        else:
            user.subjects.add(subject)

        self.user_repository.save(user)

    def get_subjects(self, user_id: int) -> set[str]:
        user = self.get_or_create_user(user_id)
        return user.subjects

    def toggle_level(self, user_id: int, level: int):
        user = self.get_or_create_user(user_id)

        if level in user.selected_levels:
            user.selected_levels.remove(level)
        else:
            user.selected_levels.add(level)

        self.user_repository.save(user)

    def start_grade_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = "grade"

        self.user_repository.save(user)

    def start_subjects_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = "subjects"
        user.original_subjects = user.subjects.copy()

        self.user_repository.save(user)

    def finish_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = None
        user.original_subjects.clear()

        self.user_repository.save(user)

    def finish_subjects_edit(self, user_id: int) -> set[str]:
        user = self.get_or_create_user(user_id)

        removed_subjects = user.original_subjects - user.subjects

        user.edit_mode = None
        user.original_subjects.clear()

        self.user_repository.save(user)

        return removed_subjects

    def clear_olympiads(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.olympiads.clear()

        self.user_repository.save(user)

    def get_removed_subjects(self, user_id: int) -> set[str]:
        user = self.get_or_create_user(user_id)

        return user.original_subjects - user.subjects