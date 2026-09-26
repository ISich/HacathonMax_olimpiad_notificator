from app.models.user import UserSelectedLevel

class UserService:

    def __init__(
        self,
        user_repository,
        subject_repository,
    ):
        self.user_repository = user_repository
        self.subject_repository = subject_repository

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

    def toggle_subject(self, user_id: int, subject_code: str):
        user = self.get_or_create_user(user_id)

        subject = self.subject_repository.get_by_code(
            subject_code
        )

        if subject is None:
            raise ValueError(
                f"Предмет {subject_code} не найден"
            )

        existing = next(
            (
                item
                for item in user.subjects
                if item.code == subject_code
            ),
            None,
        )

        if existing is not None:
            user.subjects.remove(existing)
        else:
            user.subjects.append(subject)

        self.user_repository.save(user)

    def get_subjects(self, user_id: int) -> set[str]:
        user = self.get_or_create_user(user_id)

        return {
            subject.code
            for subject in user.subjects
        }

    def toggle_level(self, user_id: int, level: int):
        user = self.get_or_create_user(user_id)

        existing = next(
            (
                item
                for item in user.selected_levels
                if item.level == level
            ),
            None
        )

        if existing is not None:
            user.selected_levels.remove(existing)
        else:
            user.selected_levels.append(
                UserSelectedLevel(level=level)
            )

        self.user_repository.save(user)

    def get_selected_levels(self, user_id: int) -> set[int]:
        user = self.get_or_create_user(user_id)

        return {
            item.level
            for item in user.selected_levels
        }

    def start_grade_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = "grade"

        self.user_repository.save(user)

    def start_subjects_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = "subjects"

        self.user_repository.save(user)

    def finish_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = None

        self.user_repository.save(user)

    def finish_subjects_edit(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.edit_mode = None

        self.user_repository.save(user)

    def clear_olympiads(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.olympiads.clear()

        self.user_repository.save(user)

    def set_olympiads(self, user_id: int, olympiads):
        user = self.get_or_create_user(user_id)

        user.olympiads.clear()
        user.olympiads.extend(olympiads)

        self.user_repository.save(user)

    def remove_olympiad(self, user_id: int, olympiad_id):
        user = self.get_or_create_user(user_id)

        olympiad = next(
            (
                item
                for item in user.olympiads
                if str(item.id) == str(olympiad_id)
            ),
            None
        )

        if olympiad is not None:
            user.olympiads.remove(olympiad)
            self.user_repository.save(user)

        return olympiad

    def toggle_olympiad(self, user_id: int, olympiad):
        user = self.get_or_create_user(user_id)

        existing = next(
            (
                item
                for item in user.olympiads
                if item.id == olympiad.id
            ),
            None
        )

        if existing is not None:
            user.olympiads.remove(existing)
        else:
            user.olympiads.append(olympiad)

        self.user_repository.save(user)

    def reset_user(self, user_id: int):
        user = self.get_or_create_user(user_id)

        user.grade = None
        user.subjects.clear()
        user.selected_levels.clear()
        user.olympiads.clear()
        user.edit_mode = None

        self.user_repository.save(user)