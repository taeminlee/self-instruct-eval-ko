# python
import os
from enum import Enum
# DeepL 라이브러리를 이용하여 번역
import deepl
# framework
from translate import Translate


class TargetLang(Enum):
    Bulgarian = 'BG'
    Czech = 'CS'
    Danish = 'DA'
    German = 'DE'
    Greek = 'EL'
    English = 'EN'
    English_GB = 'EN-GB'
    English_US = 'EN-US'
    Spanish = 'ES'
    Estonian = 'ET'
    Finnish = 'FI'
    French = 'FR'
    Hungarian = 'HU'
    Italian = 'IT'
    Japanese = 'JA'
    Lithuanian = 'LT'
    Latvian = 'LV'
    Dutch = 'NL'
    Polish = 'PL'
    Portuguese = 'PT-PT'
    Portuguese_BR = 'PT-BR'
    Portuguese_PT = 'PT'
    Romanian = 'RO'
    Russian = 'RU'
    Slovak = 'SK'
    Slovenian = 'SL'
    Swedish = 'SV'
    Chinese = 'ZH'
    Korean = 'KO'


# deepl 번역
class DeepL(Translate):
    def __init__(self):
        # DeepL API Key를 가져와 비동기 Translator 객체를 생성합니다.
        self.translator = deepl.Translator(deepl.AiohttpAdapter(os.getenv("DEEPL_API_KEY")))

    async def __call__(self, original_text: str, target_lang: str = 'KO') -> str:
        """
        입력된 original_text를 target_lang으로 번역하는 함수입니다.

        Args:
          original_text (str): 번역할 텍스트
          target_lang (str): 번역될 언어 코드 (default: 'KO')

        Returns:
          str: 번역된 텍스트
        """
        # original_text가 빈 문자열인 경우 바로 반환합니다.
        if not original_text or original_text.strip() == "":
            return original_text

        # DeepL 라이브러리의 translate_text 메소드를 사용하여 번역한 후, 결과를 반환합니다.
        return await self.translator.translate(original_text, target_lang=TargetLang.Korean)
    

if __name__ == '__main__':
    text = 'hello world!'
    print(f'DeepL: {DeepL().translate(text)}')