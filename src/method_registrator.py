import typing
from .api_handler.api_handler import ApiHandler
from .data_analysis.scraper import Scraper

"""
Method for testing args
"""
def testFunction(*args) -> None:
    print()
    print("Malý krok pro člověka, ale velký krok pro lidstvo!!")
    print("Zadané parametry:")
    for par in args:
        print(par)

"""
Function for printing out registred methods
"""
def help() -> None:
    for registredMethod in MethodRegistrator.REGISTRED_FUNCTIONS:
        print(registredMethod)


class MethodRegistrator:

    REGISTRED_FUNCTIONS: typing.Dict[str, typing.Callable[[typing.List[str]], None]]= {
        help.__name__: help,
        testFunction.__name__: testFunction,
        Scraper.scrape.__name__: Scraper.scrape
        
    }
    APPEND_EXT_TEXT: str = "\n For getting all registred methods please use python3 main.py help"

    def __init__(self, arguments: typing.List[str]):
        self.__check_args_len(arguments)

        self.__function_name: str = arguments[1]
        self.__arguments: typing.List[str] = arguments[2:]

    def __str__(self):
        return f"Method registrator, {self.__function_name}"

    def __check_args_len(self, args: typing.List[str]):
        if len(args) < 2:
            raise Exception("At least 1 argument is reguired." + self.APPEND_EXT_TEXT)

    """
    Testuje zda je metoda zaregistrovana
    """
    def _check_function_registred(self):
        if self.__function_name in self.REGISTRED_FUNCTIONS:
            return True
        else:
            raise Exception(f"Function is not registred! You have entered: {self.__function_name}!" + self.APPEND_EXT_TEXT)

    """
    Spustí metody z spolu s parametry spolu s parametry pro metodu
    """
    def run(self: str):
        self._check_function_registred()
        self.REGISTRED_FUNCTIONS[self.__function_name](*self.__arguments)

            

