# self-instruct-eval-ko

[Self-Instruct](https://github.com/yizhongw/self-instruct)의 eval dataset을 한국어 모델에서 사용 가능하도록 번역한 데이터 모음입니다.

### Requires

- openai api
- deepl api

### Installation

- poetry 패키지를 이용해서 의존성을 관리합니다.

```bash
# poetry 설치
pip install poetry
# 의존성 패키지 설치
poetry install
# poetry dotenv 플러그인 설치
poetry self add poetry-dotenv-plugin
# OPENAI_API_KEY 환경변수 설정
poetry run dotenv set OPENAI_API_KEY {OPENAI_API_KEY}
# DEEPL_API_KEY
poetry run dotenv set DEEPL_API_KEY {DEEPL_API_KEY}
```

### Dataset preparation

- run

`poetry run python dataset_prepare.py`

- log

```bash
(base) persuade@nlp-server-10:/mnt/md0/persuade/self-instruct-eval-ko$ poetry run python dataset_prepare.py 
in_filepath: user_oriented_instructions.jsonl
out_filepath: user_oriented_instructions_deepl_ko.jsonl
252it [03:27,  1.21it/s]
in_filepath: user_oriented_instructions.jsonl
out_filepath: user_oriented_instructions_chatgpt_ko.jsonl
252it [27:44,  6.61s/it]
```

### Translate

- run example

`poetry run python translate.py`

- log

```bash
(base) persuade@nlp-server-10:/mnt/md0/persuade/self-instruct-eval-ko$ poetry run python translate.py
original text: hello world!
DEEPL: 안녕하세요!
ChatGPT 3.5: 안녕 세상!
DEV MODE IS ON, only 5 objs are converted
in_filepath: user_oriented_instructions.jsonl
out_filepath: user_oriented_instructions_ko.jsonl
0it [00:00, ?it/s]
ORIGINAL: {'id': 'user_oriented_task_0', 'motivation_app': 'Grammarly', 'instruction': 'The sentence you are given might be too wordy, complicated, or unclear. Rewrite the sentence and make your writing clearer by keeping it concise. Whenever possible, break complex sentences into multiple sentences and eliminate unnecessary words.', 'instances': [{'input': 'If you have any questions about my rate or if you find it necessary to increase or decrease the scope for this project, please let me know.', 'output': "If you have any questions about my rate or find it necessary to increase or decrease this project's scope, please let me know."}]}
TRANSLATED: {'id': 'user_oriented_task_0', 'motivation_app': 'Grammarly', 'instruction': '당신이 받은 문장은 너무 많은 단어로, 복잡하게 또는 불분명할 수 있습니다. 문장을 다시 작성하고, 필요 없는 단어를 제거하며 간결하게 작성하여 더욱 명확하게 만드세요. 가능한 경우 복잡한 문장을 여러 문장으로 나누어 작성하세요.', 'instances': [{'input': '만약 제 수입에 대해 궁금한 점이 있거나 이 프로젝트의 범위를 늘리거나 줄이는 것이 필요한 경우, 알려주세요.', 'output': "If you have any questions about my rate or find it necessary to increase or decrease this project's scope, please let me know."}]}
1it [00:08,  8.50s/it]
ORIGINAL: {'id': 'user_oriented_task_1', 'motivation_app': 'Grammarly', 'instruction': 'Analyze the word choice, phrasing, punctuation, and capitalization in the given email. How may the writer of this email sound to the reader? These tones include Disheartening, Accusatory, Worried, Curious, Surprised, Disapproving, Unassuming, Formal, Assertive, Confident, Appreciative, Concerned, Sad, Informal, Regretful, Encouraging, Egocentric, Joyful, Optimistic, and Excited.', 'instances': [{'input': "Hi Jen, \nI hope you're well. Can we catch up today? I'd appreciate your input on my presentation for tomorrow's meeting. I'd especially love it if you could double-check the sales numbers with me. There's a coffee in it for you!", 'output': 'Confident'}]}
TRANSLATED: {'id': 'user_oriented_task_1', 'motivation_app': 'Grammarly', 'instruction': '주어진 이메일에서 단어 선택, 구문, 문장부호 및 대문자 사용을 분석하십시오. 이 이메일의 작성자는 독자에게 어떤 느낌을 줄까요? 이러한 감정에는 낙담, 비난적, 걱정된, 호기심 있는, 놀란, 비난하는, 겸손한, 공식적인, 단호한, 자신감 있는, 감사하는, 걱정하는, 슬픈, 비공식적인, 유감스러운, 격려하는, 자기중심적인, 기쁜, 낙천적인 및 흥분된 감정이 포함됩니다.', 'instances': [{'input': '안녕 젠, \n잘 지내고 있길 바랍니다. 오늘 만나서 이야기할 수 있을까요? 내일 회의를 위한 발표 자료에 대해 당신의 의견을 듣고 싶습니다. 특히, 판매 숫자를 함께 다시 확인해 주시면 정말 고맙겠습니다. 커피 한 잔 사드릴게요!', 'output': 'Confident'}]}
2it [00:23, 12.50s/it]
ORIGINAL: {'id': 'user_oriented_task_2', 'motivation_app': 'Grammarly', 'instruction': 'Rewrite the given text and correct grammar, spelling, and punctuation errors.', 'instances': [{'input': "If you'd told me year ago that today I would finish a marathon, I would of laughed. Your support had a huge affect on me!", 'output': "If you'd told me a year ago that today I would finish a marathon, I would have laughed. Your support had a huge effect on me!"}]}
TRANSLATED: {'id': 'user_oriented_task_2', 'motivation_app': 'Grammarly', 'instruction': '주어진 텍스트를 다시 작성하고 문법, 철자 및 구두점 오류를 수정해주세요.', 'instances': [{'input': '만약 1년 전에 오늘 나가 마라톤을 완주할 거라고 말해줬더라면, 내가 웃고 있었을 거야. 네 지원은 나에게 큰 영향을 미쳤어!', 'output': "If you'd told me a year ago that today I would finish a marathon, I would have laughed. Your support had a huge effect on me!"}]}
3it [00:29,  9.51s/it]
ORIGINAL: {'id': 'user_oriented_task_3', 'motivation_app': 'Google Scholar', 'instruction': 'You are given a paper citation, convert it to the requested citation style.', 'instances': [{'input': 'Chicago: Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, and Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.\nMLA:', 'output': 'Vaswani, Ashish, et al. "Attention Is All You Need." arXiv, 2017,  https://doi.org/10.48550/arXiv.1706.03762.'}]}
TRANSLATED: {'id': 'user_oriented_task_3', 'motivation_app': 'Google Scholar', 'instruction': '당신은 논문 인용문을 받았습니다. 요청된 인용 양식으로 변환해주세요.', 'instances': [{'input': '시카고: Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, 및 Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.\nMLA:', 'output': 'Vaswani, Ashish, et al. "Attention Is All You Need." arXiv, 2017,  https://doi.org/10.48550/arXiv.1706.03762.'}]}
4it [00:36,  8.30s/it]
ORIGINAL: {'id': 'user_oriented_task_4', 'motivation_app': 'Grammarly', 'instruction': "Desk jobs require writing a lot of emails, so it isn't surprising we get tired of repeating ourselves. Come up with several synonyms for the given word.", 'instances': [{'input': 'Sincerely', 'output': 'Best regards, All the best, Cheers, Best'}]}
TRANSLATED: {'id': 'user_oriented_task_4', 'motivation_app': 'Grammarly', 'instruction': '책상에서 하는 일은 많은 이메일을 쓰기 때문에 우리가 자신의 말을 반복하는 것에 지쳐 있는 것은 놀랍지 않다. 주어진 단어의 여러 동의어를 생각해보세요.', 'instances': [{'input': '정말로 진심으로 (jeongmallo jinsimeuro)', 'output': 'Best regards, All the best, Cheers, Best'}]}
5it [00:41,  7.32s/it]
ORIGINAL: {'id': 'user_oriented_task_5', 'motivation_app': 'Gmail', 'instruction': 'If you could help me write an email to my friends inviting them to dinner on Friday, it would be greatly appreciated.', 'instances': [{'input': '', 'output': "Hi there,\n\nI hope you're all doing well. I'm inviting you over for dinner on Friday night. Please let me know if you can make it. I'll be cooking your favorite dishes!\n\nLooking forward to seeing you,"}]}
TRANSLATED: {'id': 'user_oriented_task_5', 'motivation_app': 'Gmail', 'instruction': '만약 금요일 저녁에 친구들을 초대하는 이메일을 쓰는 데 도움을 줄 수 있다면, 정말 감사하겠습니다.', 'instances': [{'input': '', 'output': "Hi there,\n\nI hope you're all doing well. I'm inviting you over for dinner on Friday night. Please let me know if you can make it. I'll be cooking your favorite dishes!\n\nLooking forward to seeing you,"}]}
5it [00:44,  8.91s/it]
```

### Eval

TBD