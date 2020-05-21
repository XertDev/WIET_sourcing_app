from abc import ABC, abstractmethod


class AbstractQuestionLoader(ABC):
    @staticmethod
    @abstractmethod
    def get_typename() -> str:
        """
        :return: question type name
        """
        pass

    @staticmethod
    @abstractmethod
    def get_screen_name():
        """
        :return: screen class name
        """
        pass

    @staticmethod
    @abstractmethod
    def get_on_query():
        """
        :return: query used to retrieve union from node
        """
        pass