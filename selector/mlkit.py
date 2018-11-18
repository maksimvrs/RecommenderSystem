from sklearn import linear_model
import numpy as np


class MLKit:
    def __init__(self, user_specs: object, mentor_specs: object) -> object:
        """
        :param user_specs: Список характеристик пользовтаеля (характеристика - число 0..1)
        :param mentor_specs: Список характеристик ментора (характеристика - число 0..1)
        """
        self.is_fitting = False
        self.user_specs = user_specs
        self.mentor_specs = mentor_specs
        self.models = [linear_model.LinearRegression()] * len(mentor_specs)

    def fit(self, user_specs: list, mentor_specs: list):
        self.is_fitting = True
        for i, model in enumerate(self.models):
            model.fit(user_specs, np.array(mentor_specs)[:, i])

    def predict(self, user_specs: object) -> object:
        """
        :param user_specs: Характеристики пользователя
        :return: Список желаемых характеристик ментора
        """
        if self.is_fitting:
            return [model.predict([user_specs])[0] for model in self.models]
        return None
