

class TestConfig:

    test_type_list: list = ['time', 'words', 'custom']
    duration_list: list = [15, 30, 60, 120]
    language_list: list = ['english',
                           'english 1k',
                           'english 5k',
                           'english 10k',
                           'english 25k',
                           'english 450k']


    def __init__(self, _type:  str, _duration: int, _language: str, _wpm: int, _punctuation_toggle: bool =None, _numbers_toggle: bool =None)-> None:

        if _type not in TestConfig.test_type_list:
            raise ValueError(f'Invalid test type. Choose from: {TestConfig.test_type_list}')
        elif _duration not in TestConfig.duration_list:
            raise ValueError(f'Invalid duration. Choose from: {TestConfig.duration_list}')
        elif _language not in TestConfig.language_list:
            raise ValueError(f'Invalid language. Choose from: {TestConfig.language_list}')
        elif _wpm not in range(0,351):
            raise ValueError('Invalid WPM. Choose from between 0 and 350')
        elif _punctuation_toggle not in [True, False, None]:
            raise ValueError('Invalid Punctuation Toggle. Choose from [True, False]')
        elif _numbers_toggle not in [True, False, None]:
            raise ValueError('Invalid Numbers Toggle. Choose from [True, False]')
        else:
            self._wpm = _wpm # speed of test completion (words per minute)
            self._type = _type # test type
            self._duration = _duration # test duration
            self._language = _language # test language
            self._punctuation_toggle = _punctuation_toggle # test with punctuation in text (boolean)
            self._numbers_toggle = _numbers_toggle # test with numbers in text


    def __str__(self):
        output = (
            f'Type of test: {self._type}\n'
            f'Duration: {self._duration}\n'
            f'Language: {self._language}\n'
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


if __name__ == "__main__":

    obj = TestConfig('words', 30,'english 1k',150)
    obj2 = TestConfig('time', 30, 'english 5k', 323,True,True)

    print(obj)
    print(obj2)
