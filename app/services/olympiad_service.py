class OlympiadService:

    def __init__(self, olympiad_repository):
        self.olympiad_repository = olympiad_repository

    def find_for_user(
        self,
        grade: int,
        subject_codes: set[str],
        levels: set[int] | None = None
    ):
        return self.olympiad_repository.find_matching(
            grade=grade,
            subject_codes=subject_codes,
            levels=levels
        )

    def get_olympiad(self, olympiad_id):
        return self.olympiad_repository.get(olympiad_id)