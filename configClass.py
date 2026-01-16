# I should probably look more into DATACLASSES (@dataclass) but for now this class will do.


# Test Configuration class to define all properties for tests
class TestConfig:

    test_type_list: list = ['time', 'words', 'custom']
    time_options: list = [15, 30, 60, 120]
    word_options: list = [10,25,50,100]
    language_list: list = ['english',
                           'english 1k',
                           'english 5k',
                           'english 10k',
                           'english 25k',
                           'english 450k']


    def __init__(self, _type:  str, _amount: int, _language: str, _wpm: int, _punctuation_toggle: bool =None, _numbers_toggle: bool =None)-> None:

        # Validate Type
        if _type not in TestConfig.test_type_list:
            raise ValueError(f'Invalid test type. Choose from: {TestConfig.test_type_list}')

        # Validate Amount based on Type
        if _type == 'time' and _amount not in TestConfig.time_options:
            raise ValueError(f'Invalid duration. Choose from: {TestConfig.time_options}')
        elif _type == 'words' and _amount not in TestConfig.word_options:
            raise ValueError(f'Invalid word count. Choose from: {TestConfig.word_options}')

        # Validate Language
        if _language not in TestConfig.language_list:
            raise ValueError(f'Invalid language. Choose from: {TestConfig.language_list}')

        # Validate WPM and Toggles
        if _wpm not in range(0,351):
            raise ValueError('Invalid WPM. Choose from between 0 and 350')
        elif _punctuation_toggle not in [True, False, None]:
            raise ValueError('Invalid Punctuation Toggle. Choose from True, False, or None')
        elif _numbers_toggle not in [True, False, None]:
            raise ValueError('Invalid Numbers Toggle. Choose from True, False, or None')

        # Assignment after checks
        self._wpm = _wpm # speed of test completion (words per minute)
        self._type = _type # test type
        self._amount = _amount # test duration
        self._language = _language # test language
        self._punctuation_toggle = _punctuation_toggle # test with punctuation in text (boolean)
        self._numbers_toggle = _numbers_toggle # test with numbers in text


    def __str__(self):
        output = (
            f'Type of test: {self._type}\n'
            f'Duration: {self._amount}\n'
            f'Language: {self._language}\n'
            f'Target WPM: {self._wpm}\n'
        )

        if self._punctuation_toggle is True:
            output += f'Punctuation in text is enabled\n'
        elif self._punctuation_toggle is False:
            output += f'Punctuation in text is disabled\n'

        if self._numbers_toggle is True:
            output += f'Numbers in text enabled\n'
        elif self._numbers_toggle is False:
            output += f'Numbers in text is disabled\n'

        return output

    # apply @property decorator to access the variable values from outside the class
    @property
    def test_type(self):
        return self._type
    @property
    def amount(self):
        return self._amount
    @property
    def language(self):
        return self._language
    @property
    def wpm(self):
        return self._wpm
    @property
    def punctuation_toggle(self):
        return self._punctuation_toggle
    @property
    def numbers_toggle(self):
        return self._numbers_toggle


if __name__ == "__main__":

    obj = TestConfig('words', 50,'english 1k',150)
    obj2 = TestConfig('time', 30, 'english 5k', 323,True,True)

    print(f"{obj.test_type}\n{obj.amount}\n{obj.language}\n{obj.wpm}\n{obj.punctuation_toggle}\n{obj.numbers_toggle}")
    print(obj)

    print(f"{obj2.test_type}\n{obj2.amount}\n{obj2.language}\n{obj2.wpm}\n{obj2.punctuation_toggle}\n{obj2.numbers_toggle}")
    print(obj2)

