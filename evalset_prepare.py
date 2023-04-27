import asyncio
from chatgpt import ChatGPTEval


# ChatGPT 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_chatgpt_ko.jsonl 파일에 저장
asyncio.run(ChatGPTEval().aeval_jsonl(in_filepath='user_oriented_instructions_deepl_ko.jsonl',
                    out_filepath='user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl',
                    max_concurrency=100,
                    dev=False))
