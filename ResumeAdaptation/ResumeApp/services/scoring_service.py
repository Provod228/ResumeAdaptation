class ScoringService:

    @staticmethod
    def calculate_score(
        resume_skills: list,
        vacancy_skills: list
    ):

        if not vacancy_skills:
            return 0

        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        vacancy_set = {
            skill.lower()
            for skill in vacancy_skills
        }

        matched_skills = resume_set.intersection(
            vacancy_set
        )

        score = int(
            (len(matched_skills) / len(vacancy_set)) * 100
        )

        return min(score, 100)

    @staticmethod
    def get_missing_skills(
        resume_skills: list,
        vacancy_skills: list
    ):

        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        vacancy_set = {
            skill.lower()
            for skill in vacancy_skills
        }

        missing_skills = vacancy_set.difference(
            resume_set
        )

        return list(missing_skills)