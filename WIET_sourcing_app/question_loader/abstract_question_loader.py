from abc import ABC, abstractmethod


class AbstractQuestionLoader(ABC):
    @staticmethod
    @abstractmethod
    def get_typename() -> str:
        """
        :return: question type name
        """
        pass
