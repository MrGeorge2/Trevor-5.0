import typing
from .data_analysis.scraper import Scraper
from .data_analysis.models.results import Results
from .data_analysis.models.indicators import Indicators
from .samples.samples import Samples
from .nn_model.train import TrainNN
from .nn_model.test_gpu import test_tf_gpu


"""
Scrape all symbols from config with result
"""
def full_fetch(*args):
    Scraper.scrape_all()
    Results.count_results()
    Results.divide_train_test()
    Indicators.count_indicators()


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
def help(*args) -> None:
    for registredMethod in MethodRegistrator.REGISTRED_FUNCTIONS:
        print(registredMethod)


class MethodRegistrator:
    REGISTRED_FUNCTIONS: typing.Dict[str, typing.Callable[[typing.List[str]], None]] = {
        help.__name__: help,
        testFunction.__name__: testFunction,
        Scraper.scrape.__name__: Scraper.scrape,
        Scraper.scrape_all.__name__: Scraper.scrape_all,
        Results.count_results.__name__: Results.count_results,
        Indicators.count_indicators.__name__: Indicators.count_indicators,
        full_fetch.__name__: full_fetch,
        Samples.create_samples.__name__: Samples.create_samples,
        Results.divide_train_test.__name__: Results.divide_train_test,
        Results.reverse_train_data.__name__: Results.reverse_train_data,
        TrainNN.train.__name__: TrainNN.train,
        test_tf_gpu.__name__: test_tf_gpu
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
            raise Exception(
                f"Function is not registred! You have entered: {self.__function_name}!" + self.APPEND_EXT_TEXT)

    """
    Spustí metody z spolu s parametry spolu s parametry pro metodu
    """

    def run(self: str):
        self._check_function_registred()
        self.REGISTRED_FUNCTIONS[self.__function_name](*self.__arguments)
        

