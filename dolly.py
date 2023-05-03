import asyncio
from deepl_ import DeepL
from gpt4 import GPT4Eval

# instruction 및 instances 안에 있는 내용들을 번역하는 함수 
async def translate_func(translate, obj):
    obj['instruction'] = await translate(obj['instruction']) # instruction 번역
    obj['context'] = await translate(obj['context']) # instruction 번역
    return obj # 번역된 결과 반환

async def arun(self, obj: dict) -> dict:
    obj['response'] = await self.__call__(obj['instruction'], obj['context'])
    return obj

# DeepL 번역을 사용하여 instruction을 한국어로 번역
asyncio.run(DeepL().atranslate_jsonl(in_filepath='databricks-dolly-15k.jsonl',
                    out_filepath='databricks-dolly-15k_deepl_ko.jsonl',
                    translate_func=translate_func,
                    max_concurrency=100))

# GPT4 API를 사용하여 output을 생성
asyncio.run(GPT4Eval().aeval_jsonl(in_filepath='databricks-dolly-15k_deepl_ko.jsonl',
                    out_filepath='databricks-dolly-15k_deepl+gpt4_ko.jsonl',
                    run_func=arun,
                    max_concurrency=50))