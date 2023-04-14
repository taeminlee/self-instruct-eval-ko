# OpenAI ChatGPT를 langchain 라이브러리를 이용하여 번역
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
# framework
from translate import Translate


# gpt4 번역
class GPT4(Translate):
    def __init__(self, model_name='gpt-4'):
        # ChatOpenAI 객체를 생성합니다.
        chat = ChatOpenAI(model_name=model_name, request_timeout=600)
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

    async def __call__(self, original_text: str, target_lang: str = 'Korean') -> str:
        """
        입력된 original_text를 GPT-4 모델을 이용하여 target_lang으로 번역하는 함수입니다. 

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
        return await self.translate_chain.arun({'text': '', 'original_text': original_text, 'target_lang': target_lang})


if __name__ == '__main__':
    text = 'hello world!'
    print(f'GPT4: {GPT4().translate(text)}')