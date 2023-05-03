import asyncio
from chatgpt import ChatGPTEval
from gpt4 import GPT4Eval


async def arun(self, obj: dict) -> dict:
    if 'instances' in obj.keys():
        for idx, instance in enumerate(obj['instances']):
            obj['instances'][idx]['output'] = await self.__call__(obj['instruction'], instance['input'])
    else:
        obj['answer'] = await self.__call__(obj['instruction'], obj['input'])
    return obj


# ChatGPT API를 사용하여 'user_oriented_instructions_deepl_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl' 파일에 저장합니다.
asyncio.run(ChatGPTEval().aeval_jsonl(in_filepath='user_oriented_instructions_deepl_ko.jsonl',
                    out_filepath='user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl',
                    run_func=arun,
                    max_concurrency=100,
                    dev=False))

# GPT4 API를 사용하여 'user_oriented_instructions_deepl_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_deepl_ko_eval_gpt4.jsonl' 파일에 저장합니다.
asyncio.run(GPT4Eval().aeval_jsonl(in_filepath='user_oriented_instructions_deepl_ko.jsonl',
                    out_filepath='user_oriented_instructions_deepl_ko_eval_gpt4.jsonl',
                    run_func=arun,
                    max_concurrency=50,
                    dev=False))

# ChatGPT API를 사용하여 'user_oriented_instructions_chatgpt_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_chatgpt_ko_eval_chatgpt.jsonl' 파일에 저장합니다.
asyncio.run(ChatGPTEval().aeval_jsonl(in_filepath='user_oriented_instructions_chatgpt_ko.jsonl',
                    out_filepath='user_oriented_instructions_chatgpt_ko_eval_chatgpt.jsonl',
                    run_func=arun,
                    max_concurrency=100,
                    dev=False))

# GPT4 API를 사용하여 'user_oriented_instructions_chatgpt_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_chatgpt_ko_eval_gpt4.jsonl' 파일에 저장합니다.
asyncio.run(GPT4Eval().aeval_jsonl(in_filepath='user_oriented_instructions_chatgpt_ko.jsonl',
                    out_filepath='user_oriented_instructions_chatgpt_ko_eval_gpt4.jsonl',
                    run_func=arun,
                    max_concurrency=50,
                    dev=False))

# ChatGPT API를 사용하여 'user_oriented_instructions_gpt4_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_gpt4_ko_eval_chatgpt.jsonl' 파일에 저장합니다.
asyncio.run(ChatGPTEval().aeval_jsonl(in_filepath='user_oriented_instructions_gpt4_ko.jsonl',
                    out_filepath='user_oriented_instructions_gpt4_ko_eval_chatgpt.jsonl',
                    run_func=arun,
                    max_concurrency=100,
                    dev=False))

# GPT4 API를 사용하여 'user_oriented_instructions_gpt4_ko.jsonl' 파일에 답변하고, 'user_oriented_instructions_gpt4_ko_eval_gpt4.jsonl' 파일에 저장합니다.
asyncio.run(GPT4Eval().aeval_jsonl(in_filepath='user_oriented_instructions_gpt4_ko.jsonl',
                    out_filepath='user_oriented_instructions_gpt4_ko_eval_gpt4.jsonl',
                    run_func=arun,
                    max_concurrency=50,
                    dev=False))
