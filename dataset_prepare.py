import asyncio
from translate import DeepL, ChatGPT, GPT4 # 번역 모델을 사용하기 위한 라이브러리

# instruction 및 instances 안에 있는 내용들을 번역하는 함수 
async def translate_func(translate, obj):
    obj['instruction'] = await translate(obj['instruction']) # instruction 번역
    # instances에 있는 input과 output을 번역 후 dict로 저장하여 리스트로 만듦
    obj['instances'] = [{'input': await translate(instance['input']), 'output': instance['output']} for instance in obj['instances']]
    return obj # 번역된 결과 반환

# DeepL 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_deepl_ko.jsonl 파일에 저장
asyncio.run(DeepL().atranslate_jsonl(in_filepath='user_oriented_instructions.jsonl',
                    out_filepath='user_oriented_instructions_deepl_ko.jsonl',
                    translate_func=translate_func,
                    max_concurrency=100))

# ChatGPT 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_chatgpt_ko.jsonl 파일에 저장
asyncio.run(ChatGPT().atranslate_jsonl(in_filepath='user_oriented_instructions.jsonl',
                    out_filepath='user_oriented_instructions_chatgpt_ko.jsonl',
                    translate_func=translate_func,
                    max_concurrency=100))

# GPT4 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_gpt4_ko.jsonl 파일에 저장
asyncio.run(GPT4().atranslate_jsonl(in_filepath='user_oriented_instructions.jsonl',
                    out_filepath='user_oriented_instructions_gpt4_ko.jsonl',
                    translate_func=translate_func,
                    max_concurrency=50))