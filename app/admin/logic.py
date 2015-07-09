def get_vacancies():
    vacancies = Vacancy.query.all()
    return vacancies