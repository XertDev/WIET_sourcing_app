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

    @staticmethod
    @abstractmethod
    def get_create_answer_mutation(screen, question_id):
        pass

    @staticmethod
    @abstractmethod
    def set_screen_view(screen, question):
        """
        :description: Sets screen according to question
        :return:
        """
        pass