from translate import DeepL, ChatGPT # 번역 모델을 사용하기 위한 라이브러리

# instruction 및 instances 안에 있는 내용들을 번역하는 함수 
def translate_func(obj, translate):
    obj['instruction'] = translate(obj['instruction']) # instruction 번역
    # instances에 있는 input과 output을 번역 후 dict로 저장하여 리스트로 만듦
    obj['instances'] = [{'input': translate(instance['input']), 'output': instance['output']} for instance in obj['instances']]
    return obj # 번역된 결과 반환

# DeepL 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_deepl_ko.jsonl 파일에 저장
DeepL().translate(in_filepath='user_oriented_instructions.jsonl',
                    out_filepath='user_oriented_instructions_deepl_ko.jsonl',
                    translate_func=translate_func)

# ChatGPT 번역을 사용하여 user_oriented_instructions.jsonl 파일의 내용을 한국어로 번역한 후, user_oriented_instructions_chatgpt_ko.jsonl 파일에 저장
ChatGPT().translate(in_filepath='user_oriented_instructions.jsonl',
                    out_filepath='user_oriented_instructions_chatgpt_ko.jsonl',
                    translate_func=translate_func)