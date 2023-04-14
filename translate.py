# python
from abc import ABC, abstractmethod
from typing import Callable
# 비동기
from functools import partial
import asyncio
from tqdm.asyncio import tqdm_asyncio
# jsonl 파일 핸들링
import jsonlines
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

    async def __call__(self, original_text):
        """
        문자열을 매개변수로 받아 번역된 결과를 반환하는 메소드입니다.

        Args:
            original_text (str): 번역할 대상이 되는 문자열입니다.

        Returns:
            str: 번역된 결과물 문자열입니다.
        """
        pass
    
    def translate(self, original_text):
        return asyncio.run(self.__call__(original_text))

    def translate_jsonl(self, in_filepath: str, out_filepath: str, translate_func: Callable[[Callable[[str], str], dict], dict], verbose=True, dev=False):
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
                    t_obj = translate_func(asyncio.run(self.__call__), obj) # 입력으로 받은 번역 함수(translate_func)를 이용해 번역 작업 수행
                    if dev:
                        print(colored(f"TRANSLATED: {t_obj}", 'green'))
                        if idx > 4:
                            break # 개발자 모드(dev=True)일 때, 5개 이상 객체가 변환되면 break
                    writer.write(t_obj) # 새로운 JSON 파일에 변환된 객체 쓰기
    

    async def atranslate_jsonl(self, in_filepath: str, out_filepath: str, translate_func: Callable[[Callable[[str], str], dict], dict], max_concurrency=10, verbose=True, dev=False):
        """
        JSON 파일에서 데이터를 읽어 번역 함수(translate_func)로 변환한 후 새로운 JSON 파일로 저장하는 비동기 메서드입니다.
    
        Args:
            in_filepath (str): 입력할 JSON 파일의 경로와 이름. 확장자는 반드시 .jsonl 이어야 합니다.
            out_filepath (str): 출력할 JSON 파일의 경로와 이름. 확장자는 반드시 .jsonl 이어야 합니다.
            translate_func (Callable[[dict], dict]): 각각의 객체를 번역하는데 사용될 함수
            max_concurrency (int): 동시에 실행될 태스크 수 (기본값: 10)
            verbose (bool): 진행 상황 메시지 출력 여부 (기본값: True)
            dev (bool): 개발자 모드 사용 여부 (기본값: False)
    
        Returns:
            None
        """

        translate_call = partial(translate_func, self.__call__)  # translate_func에 self.__call__ 함수를 인자로 고정하여 새로운 함수(translate_call)를 생성합니다. 

        async def run_task(sem, obj):
            async with sem:  # semaphore lock을 사용하여 동시에 실행되는 coroutine의 개수를 제한합니다.
                result = await translate_call(obj)  # translate_call 함수를 실행하여 결과를 반환합니다.
                return result

        with jsonlines.open(in_filepath) as reader:
            data = [obj for obj in reader]  # 입력 파일에서 모든 객체들을 리스트에 저장합니다.

        if dev:
            data = data[:5]  # 개발자 모드인 경우, 데이터의 일부만 변환하도록 하여 테스트할 수 있습니다.

        semaphore = asyncio.Semaphore(max_concurrency)  # 최대 max_concurrency 수만큼의 태스크가 동시에 실행됩니다.

        tasks = [asyncio.ensure_future(run_task(semaphore, obj)) for obj in data]  # 모든 객체들에 대해서 비동기 태스크를 생성합니다.

        if verbose:
            print(colored(f"in_filepath: {in_filepath}", 'yellow'))  # 입력 파일 경로 출력
            print(colored(f"out_filepath: {out_filepath}", 'yellow'))  # 출력 파일 경로 출력
            print(colored(f"max_concurrency: {max_concurrency}", 'yellow'))  # 최대 max_concurrency 수 출력
            results = await tqdm_asyncio.gather(*tasks)  # 결과값들을 모아서 반환합니다.
        else:
            results = await asyncio.gather(*tasks)  # 결과값들을 모아서 반환합니다.

        with jsonlines.open(out_filepath, mode='w') as writer:
            for t_obj in results:
                writer.write(t_obj)  # 번역된 결과물들을 출력 파일에 저장합니다.


# 현재 모듈의 이름이 __main__일 경우, 아래 코드를 실행합니다.
if __name__ == '__main__':
    from deepl_ import DeepL
    from chatgpt import ChatGPT
    from gpt4 import GPT4
    # 변수 text를 'hello world!'로 설정하고, 이를 출력합니다.
    text = 'hello world!'
    print(f'원문: {text}')
    # DEEPL API를 사용하여 텍스트를 번역한 결과를 출력합니다.
    print(f'DEEPL: {DeepL().translate(text)}')
    # ChatGPT 3.5 API를 사용하여 새로운 텍스트를 생성하고 출력합니다.
    print(f'ChatGPT 3.5: {ChatGPT().translate(text)}')
    # GPT-4 API를 사용하여 새로운 텍스트를 생성하고, 이를 출력합니다.
    print(f'GPT-4: {GPT4().translate(text)}')

    async def translate_func(translate, obj):
        # 'instruction' 필드와 'instances' 배열을 각각 번역 함수로 번역하고, 그 결과를 다시 대입합니다.
        obj['instruction'] = await translate(obj['instruction'])
        obj['instances'] = [{'input': await translate(instance['input']), 'output': instance['output']} for instance in obj['instances']]
        return obj
    
    # GPT4 API를 사용하여 'user_oriented_instructions.jsonl' 파일을 번역하고, 'user_oriented_instructions_ko.jsonl' 파일에 저장합니다.
    # 번역 작업은 'translate_func' 함수가 수행하며, dev 모드를 활성화하여 디버그 정보도 출력합니다.
    asyncio.run(DeepL().atranslate_jsonl(in_filepath='user_oriented_instructions.jsonl',
                        out_filepath='user_oriented_instructions_ko.jsonl',
                        translate_func=translate_func,
                        dev=True))

