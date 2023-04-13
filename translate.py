# python
import os
from abc import ABC, abstractmethod
from typing import Callable
# jsonl 파일 핸들링
import jsonlines
# DeepL 라이브러리를 이용하여 번역
import deepl
# OpenAI ChatGPT를 langchain 라이브러리를 이용하여 번역
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
# 유틸리티 함수
from termcolor import colored
import tqdm


class Translate(ABC):
    """
    추상 클래스로, 문자열 번역에 필요한 메소드들을 정의합니다.

    Args:
        없음

    Attributes:
        없음

    Methods:
        __call__(original_text (str)): 문자열을 매개변수로 받아 번역된 결과를 반환하는 메소드입니다.
    """

    def __init__(self):
        pass

    def __call__(self, original_text):
        """
        문자열을 매개변수로 받아 번역된 결과를 반환하는 메소드입니다.

        Args:
            original_text (str): 번역할 대상이 되는 문자열입니다.

        Returns:
            str: 번역된 결과물 문자열입니다.
        """
        pass

    def translate(self, in_filepath: str, out_filepath: str, translate_func: Callable[[dict, Callable[[str], str]], dict], verbose=True, dev=False):
        """
        JSON 파일에서 데이터를 읽어 번역 함수(translate_func)로 변환한 후 새로운 JSON 파일로 저장하는 메서드입니다.
    
        Args:
            in_filepath (str): 입력할 JSON 파일의 경로와 이름. 확장자는 반드시 .jsonl 이어야 합니다.
            out_filepath (str): 출력할 JSON 파일의 경로와 이름. 확장자는 반드시 .jsonl 이어야 합니다.
            translate_func (Callable[[dict], dict]): 각각의 객체를 번역하는데 사용될 함수
            verbose (bool): 진행 상황 메시지 출력 여부 (기본값: True)
            dev (bool): 개발자 모드 사용 여부 (기본값: False)
    
        Returns:
            None
        """
      
        # 입력 및 출력 파일을 처리하기 위해 jsonl 라이브러리 사용
        with jsonlines.open(in_filepath) as reader:
            with jsonlines.open(out_filepath, mode='w') as writer:
                if dev:
                    print(colored("DEV MODE IS ON, only 5 objs are converted", 'red'))
                # verbose 옵션이 True인 경우 for loop에서 tqdm 라이브러리를 사용하여 진행 상황을 표시
                if verbose:
                    print(colored(f"in_filepath: {in_filepath}", 'yellow'))
                    print(colored(f"out_filepath: {out_filepath}", 'yellow'))
                    iterator = tqdm.tqdm(reader)
                # verbose가 False인 경우, 진행 상황 메시지를 출력하지 않고 원래의 iterable한 객체를 반환
                else:
                    iterator = reader
                  
                # JSON 파일 안의 모든 객체에 대해 입력받은 번역 함수(translate_func)로 번역 작업을 수행하고, 새로운 JSON 파일에 쓰기
                for idx, obj in enumerate(iterator):
                    if dev:
                        print(colored(f"\nORIGINAL: {obj}", 'blue'))
                    t_obj = translate_func(obj, self.__call__) # 입력으로 받은 번역 함수(translate_func)를 이용해 번역 작업 수행
                    if dev:
                        print(colored(f"TRANSLATED: {t_obj}", 'green'))
                        if idx > 4:
                            break # 개발자 모드(dev=True)일 때, 5개 이상 객체가 변환되면 break
                    writer.write(t_obj) # 새로운 JSON 파일에 변환된 객체 쓰기


# deepl 번역
class DeepL(Translate):
    def __init__(self):
        # DeepL API Key를 가져와 Translator 객체를 생성합니다.
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

    def __call__(self, original_text: str, target_lang: str = 'KO') -> str:
        """
        입력된 original_text를 target_lang으로 번역하는 함수입니다.

        Args:
          original_text (str): 번역할 텍스트
          target_lang (str): 번역될 언어 코드 (default: 'KO')

        Returns:
          str: 번역된 텍스트
        """
        # original_text가 빈 문자열인 경우 바로 반환합니다.
        if not original_text:
            return original_text

        # DeepL 라이브러리의 translate_text 메소드를 사용하여 번역한 후, 결과를 반환합니다.
        return self.translator.translate_text(text=original_text, target_lang=target_lang).text


# chatgpt 번역
class ChatGPT(Translate):
    def __init__(self, model_name='gpt-3.5-turbo'):
        # ChatOpenAI 객체를 생성합니다.
        chat = ChatOpenAI(model_name=model_name)
        # 사용자에게 보낼 시스템 메시지와 인간의 응답 메시지 템플릿을 정의합니다.
        template = "You are a helpful assistant that translates English to {target_lang}. Please paraphrase as much as possible when translating. Do not add expressions that are not in the source sentences. Do not add pronunciations for the target language."
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template)
        human_template = """Please provide the {target_lang} translation for these sentences: {original_text}"""
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt])

        # LLMChain 객체를 생성하여 prompt에 chat_prompt를 할당합니다.
        self.translate_chain = LLMChain(llm=chat, prompt=chat_prompt)

    def __call__(self, original_text: str, target_lang: str = 'Korean') -> str:
        """
        입력된 original_text를 GPT-3 모델을 이용하여 target_lang으로 번역하는 함수입니다. 

        Args:
          original_text (str): 번역할 영어 텍스트
          target_lang (str): 목표 언어 (default: 'Korean')

        Returns:
          str: 입력된 original_text가 target_lang으로 번역된 결과
        """
        # original_text가 빈 문자열인 경우 바로 반환합니다.
        if not original_text:
            return original_text

        # translate_chain 객체의 run 메소드를 사용하여 번역을 진행한 후, 반환합니다.
        return self.translate_chain.run({'text': '', 'original_text': original_text, 'target_lang': target_lang})


# gpt4 번역
class GPT4(Translate):
    def __init__(self, model_name='gpt-4'):
        # ChatOpenAI 객체를 생성합니다.
        chat = ChatOpenAI(model_name=model_name)
        # 사용자에게 보낼 시스템 메시지와 인간의 응답 메시지 템플릿을 정의합니다.
        template = "You are a helpful assistant that translates English to {target_lang}. Please paraphrase as much as possible when translating. Do not add expressions that are not in the source sentences. Do not add pronunciations for the target language. Please provide the {target_lang} translation for these sentences:"
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template)
        human_template = """{original_text}"""
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt])

        # LLMChain 객체를 생성하여 prompt에 chat_prompt를 할당합니다.
        self.translate_chain = LLMChain(llm=chat, prompt=chat_prompt)

    def __call__(self, original_text: str, target_lang: str = 'Korean') -> str:
        """
        입력된 original_text를 GPT-3 모델을 이용하여 target_lang으로 번역하는 함수입니다. 

        Args:
          original_text (str): 번역할 영어 텍스트
          target_lang (str): 목표 언어 (default: 'Korean')

        Returns:
          str: 입력된 original_text가 target_lang으로 번역된 결과
        """
        # original_text가 빈 문자열인 경우 바로 반환합니다.
        if not original_text:
            return original_text

        # translate_chain 객체의 run 메소드를 사용하여 번역을 진행한 후, 반환합니다.
        return self.translate_chain.run({'text': '', 'original_text': original_text, 'target_lang': target_lang})


# 현재 모듈의 이름이 __main__일 경우, 아래 코드를 실행합니다.
if __name__ == '__main__':
    # 변수 text를 'hello world!'로 설정하고, 이를 출력합니다.
    text = 'hello world!'
    print(f'원문: {text}')
    # DEEPL API를 사용하여 텍스트를 번역한 결과를 출력합니다.
    print(f'DEEPL: {DeepL()(text)}')
    # ChatGPT 3.5 API를 사용하여 새로운 텍스트를 생성하고 출력합니다.
    print(f'ChatGPT 3.5: {ChatGPT()(text)}')
    # GPT-4 API를 사용하여 새로운 텍스트를 생성하고, 이를 출력합니다.
    print(f'GPT-4: {GPT4()(text)}')

    def translate_func(obj, translate):
        # 'instruction' 필드와 'instances' 배열을 각각 번역 함수로 번역하고, 그 결과를 다시 대입합니다.
        obj['instruction'] = translate(obj['instruction'])
        obj['instances'] = [{'input': translate(instance['input']), 'output': translate(instance['output'])} for instance in obj['instances']]
        return obj
    
    # GPT4 API를 사용하여 'user_oriented_instructions.jsonl' 파일을 번역하고, 'user_oriented_instructions_ko.jsonl' 파일에 저장합니다.
    # 번역 작업은 'translate_func' 함수가 수행하며, dev 모드를 활성화하여 디버그 정보도 출력합니다.
    GPT4().translate(in_filepath='user_oriented_instructions.jsonl',
                      out_filepath='user_oriented_instructions_ko.jsonl',
                      translate_func=translate_func,
                      dev=True)

