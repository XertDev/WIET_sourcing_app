import asyncio
from asyncio import Task
import inspect
import pkgutil
from importlib import import_module
from typing import Dict, Type

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from .abstract_question_loader import AbstractQuestionLoader
from WIET_sourcing_app.libs.solve_set_mode import SolveSetMode


class QuestionLoaderManager:
    """
    Manager of loaded question loaders.
    Upon creation, this class will read all plugins in loaders directory
    """
    _loaders: Dict[str, Type[AbstractQuestionLoader]]
    loaders_package = "WIET_sourcing_app.question_loader.loaders"
    _loader_file = "loader"
    _task: Task

    def __init__(self):
        self._loaders = {}
        self._screens = []
        self.reload_loaders()
        Clock.schedule_once(self.after_init)

    def reload_loaders(self) -> None:
        """
        Reset list of loaded loaders. Load all available loaders from specified directory
        :return:
        """
        self._loaders = {}
        imported_package = import_module(self.loaders_package)

        for _, loader_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + "."):
            if is_pkg:
                try:
                    loader_module_package = import_module("{}.{}".format(loader_name, self._loader_file))
                except ModuleNotFoundError as e:
                    print("Plugin does not contain loader file")
                    continue

                cls_members = inspect.getmembers(loader_module_package, inspect.isclass)
                for (_, loader_class) in cls_members:
                    if issubclass(loader_class, AbstractQuestionLoader) and (
                            loader_class is not AbstractQuestionLoader):
                        typename = loader_class.get_typename()
                        print("Loaded question plugin: {}".format(typename))

                        if typename in self._loaders.keys():
                            raise RuntimeError("Duplicated loader! {}".format(typename))
                        self._loaders[typename] = loader_class

                        loader_class_name = loader_name.split('.')[-1]
                        screen_kv_path = imported_package.__path__[0]+'/'+loader_class_name\
                                         + '/' + loader_name.split('.')[-1] + '.kv'
                        Builder.load_file(screen_kv_path)

                        screen = getattr(import_module(loader_name + '.' + loader_class_name + '_screen'),
                                               loader_class.get_screen_name())
                        self._screens.append((screen, loader_class.get_screen_name()))

    def after_init(self, dt):
        app = App.get_running_app()
        for screen, loader_class_name in self._screens:
            app.root.ids.screen_manager.add_widget(screen(name=loader_class_name))

    async def async_set_questions_query(self, set_id):
        # print("Loading question set:", set_id)
        app = App.get_running_app()
        res = await app.question_set_service.get_set_questions(set_id)
        res = list(filter(lambda que: self.is_question_type_supported(que[1]), res))
        app.solve_set_mode.load_questions(res)
        app.solve_set_mode.show_next_question()

    def load_set_questions(self, button):
        set_id = button.set_id
        self._task = asyncio.create_task(self.async_set_questions_query(set_id))

    def is_question_type_supported(self, typename: str) -> bool:
        return typename in self._loaders.keys()

    def get_screen_by_typename(self, typename):
        return self._loaders[typename].get_screen_name()

    def get_on_query_by_typename(self, typename):
        return self._loaders[typename].get_on_query()