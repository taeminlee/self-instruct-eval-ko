# python
from abc import ABC
import os
# 비동기
import asyncio
from tqdm.asyncio import tqdm_asyncio
# jsonl 파일 핸들링
import jsonlines
from aiofile import async_open
import json
# 유틸리티 함수
from termcolor import colored


class Evaluate(ABC):
    def __init__(self):
        pass

    async def __call__(self, instruction, input) -> str:
        pass
    

    def get_answer(self, obj: dict) -> dict:
        if 'instances' in obj.keys():
            # only use first instance
            obj['input'] = obj['instances'][0]['input']
        return asyncio.run(self.__call__(obj['instruction'], obj['input']))

    async def arun(self, obj: dict) -> dict:
        if 'instances' in obj.keys():
            # only use first instance
            obj['input'] = obj['instances'][0]['input']
        obj['answer'] = await self.__call__(obj['instruction'], obj['input'])
        return obj
    
    async def aeval_jsonl(self, in_filepath: str, out_filepath: str, max_concurrency=10, verbose=True, dev=False, increment=True):
        """이 함수는 입력 파일 경로와 출력 파일 경로를 받아서, 입력 파일에서 모든 객체들을 가져와 각 객체에 대해서 비동기 처리를 해주고, 결과를 출력 파일에 저장하는 함수입니다.

        Args:
            in_filepath (str): 입력 파일 경로
            out_filepath (str): 출력 파일 경로
            max_concurrency (int, optional): 최대 동시성 개수. Defaults to 10.
            verbose (bool, optional): verbose 여부. Defaults to True.
            dev (bool, optional): 개발자 모드 여부. Defaults to False.
            increment (bool, optional): 증분 모드 여부. Defaults to True.
        """
        async def run_task(sem, afp, obj):
            async with sem:  # semaphore lock을 사용하여 동시에 실행되는 coroutine의 개수를 제한합니다.
                result = await self.arun(obj)  # __call__ 함수를 실행하여 결과를 반환합니다.
                await afp.write(json.dumps(result, ensure_ascii=False)+'\n')

        with jsonlines.open(in_filepath) as reader:
            data = [obj for obj in reader]  # 입력 파일에서 모든 객체들을 리스트에 저장합니다.
        
        if increment and os.path.exists(out_filepath):  # increment 가 True 이고 out_filepath 가 존재하는 경우
            afp = await async_open(out_filepath, 'a')  # 파일을 추가 모드로 열기 (이어서 쓰기 가능)
            with jsonlines.open(out_filepath) as reader:  # jsonlines 로 읽기
                processed_ids = [obj['id'] for obj in reader]  # 이미 처리한 id 들을 processed_ids 리스트에 저장
            data = [obj for obj in data if obj['id'] not in processed_ids]  # data 의 id 가 이미 processed_ids 리스트에 있는 경우 제외한 데이터만 data 리스트에 저장
        else:
            afp = await async_open(out_filepath, "w")

        if dev:
            data = data[:5]  # 개발자 모드인 경우, 데이터의 일부만 변환하도록 하여 테스트할 수 있습니다.

        semaphore = asyncio.Semaphore(max_concurrency)  # 최대 max_concurrency 수만큼의 태스크가 동시에 실행됩니다.

        tasks = [asyncio.ensure_future(run_task(semaphore, afp, obj)) for obj in data]  # 모든 객체들에 대해서 비동기 태스크를 생성합니다.

        if verbose:
            print(colored(f"in_filepath: {in_filepath}", 'yellow'))  # 입력 파일 경로 출력
            print(colored(f"out_filepath: {out_filepath}", 'yellow'))  # 출력 파일 경로 출력
            print(colored(f"max_concurrency: {max_concurrency}", 'yellow'))  # 최대 max_concurrency 수 출력
            await tqdm_asyncio.gather(*tasks)  # 결과값들을 모아서 반환합니다.
        else:
            await asyncio.gather(*tasks)  # 결과값들을 모아서 반환합니다.

        await afp.close()


# 현재 모듈의 이름이 __main__일 경우, 아래 코드를 실행합니다.
if __name__ == '__main__':
    from chatgpt import ChatGPTEval

    # ChatGPT API를 사용하여 'user_oriented_instructions_deepl_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl' 파일에 저장합니다.
    # dev 모드를 활성화하여 디버그 정보도 출력합니다.
    asyncio.run(ChatGPTEval().aeval_jsonl(in_filepath='user_oriented_instructions_deepl_ko.jsonl',
                        out_filepath='user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl',
                        max_concurrency=100,
                        dev=True))

