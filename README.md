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
원문: hello world!
DEEPL: 안녕하세요!
ChatGPT 3.5: 안녕, 세상!
GPT-4: 안녕하세요, 세상!
DEV MODE IS ON, only 5 objs are converted
in_filepath: user_oriented_instructions.jsonl
out_filepath: user_oriented_instructions_ko.jsonl
0it [00:00, ?it/s]
ORIGINAL: {'id': 'user_oriented_task_0', 'motivation_app': 'Grammarly', 'instruction': 'The sentence you are given might be too wordy, complicated, or unclear. Rewrite the sentence and make your writing clearer by keeping it concise. Whenever possible, break complex sentences into multiple sentences and eliminate unnecessary words.', 'instances': [{'input': 'If you have any questions about my rate or if you find it necessary to increase or decrease the scope for this project, please let me know.', 'output': "If you have any questions about my rate or find it necessary to increase or decrease this project's scope, please let me know."}]}
TRANSLATED: {'id': 'user_oriented_task_0', 'motivation_app': 'Grammarly', 'instruction': '주어진 문장이 너무 길거나 복잡하거나 불분명할 수 있습니다. 문장을 다시 쓰고 간결하게 유지하여 글을 명확하게 만드세요. 가능한 한 복잡한 문장을 여러 문장으로 나누고 불필요한 단어를 제거하세요.', 'instances': [{'input': '제 요금에 대해 궁금한 점이 있거나 이 프로젝트의 범위를 늘리거나 줄일 필요가 있다고 생각되면 알려주세요.', 'output': '제가 제시한 금액에 대한 질문이 있거나 이 프로젝트의 범위를 늘리거나 줄일 필요가 있다고 생각하시면 알려주세요.'}]}
1it [00:33, 33.88s/it]
ORIGINAL: {'id': 'user_oriented_task_1', 'motivation_app': 'Grammarly', 'instruction': 'Analyze the word choice, phrasing, punctuation, and capitalization in the given email. How may the writer of this email sound to the reader? These tones include Disheartening, Accusatory, Worried, Curious, Surprised, Disapproving, Unassuming, Formal, Assertive, Confident, Appreciative, Concerned, Sad, Informal, Regretful, Encouraging, Egocentric, Joyful, Optimistic, and Excited.', 'instances': [{'input': "Hi Jen, \nI hope you're well. Can we catch up today? I'd appreciate your input on my presentation for tomorrow's meeting. I'd especially love it if you could double-check the sales numbers with me. There's a coffee in it for you!", 'output': 'Confident'}]}
TRANSLATED: {'id': 'user_oriented_task_1', 'motivation_app': 'Grammarly', 'instruction': '주어진 이메일에서 단어 선택, 표현, 구두점, 대소문자 사용을 분석하세요. 이 이메일의 작성자가 독자에게 어떤 느낌을 줄 수 있나요? 이러한 느낌들은 낙심감, 비난적, 걱정스러운, 호기심, 놀람, 불승인, 겸손한, 공식적, 단호한, 자신감 있는, 감사하는, 우려하는, 슬픈, 비공식적, 후회하는, 격려적, 자기 중심적, 기쁜, 낙관적, 그리고 흥분한 것들이 포함됩니다.', 'instances': [{'input': '안녕 Jen,\n잘 지내고 있는지 궁금해. 오늘 만나서 얘기 좀 할 수 있을까? 내일 회의를 위한 발표자료에 대한 의견 좀 듣고 싶어. 특히나 매출 숫자를 같이 확인해줄 수 있다면 정말 좋겠어. 커피 한잔 사줄게!', 'output': '자신감 있는'}]}
2it [01:24, 43.92s/it]
ORIGINAL: {'id': 'user_oriented_task_2', 'motivation_app': 'Grammarly', 'instruction': 'Rewrite the given text and correct grammar, spelling, and punctuation errors.', 'instances': [{'input': "If you'd told me year ago that today I would finish a marathon, I would of laughed. Your support had a huge affect on me!", 'output': "If you'd told me a year ago that today I would finish a marathon, I would have laughed. Your support had a huge effect on me!"}]}
TRANSLATED: {'id': 'user_oriented_task_2', 'motivation_app': 'Grammarly', 'instruction': '주어진 텍스트를 다시 작성하고, 문법, 철자 및 구두점 오류를 수정하십시오.', 'instances': [{'input': '만약 작년에 오늘 마라톤을 완주할 거라고 말해줬다면, 웃었을 것이다. 너의 지지가 나에게 큰 영향을 미쳤어!', 'output': '만약 작년에 오늘 나는 마라톤을 완주할 거라고 말해줬다면, 웃었을 거예요. 당신의 지지가 저에게 엄청난 영향을 미쳤어요!'}]}
3it [01:55, 37.71s/it]
ORIGINAL: {'id': 'user_oriented_task_3', 'motivation_app': 'Google Scholar', 'instruction': 'You are given a paper citation, convert it to the requested citation style.', 'instances': [{'input': 'Chicago: Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, and Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.\nMLA:', 'output': 'Vaswani, Ashish, et al. "Attention Is All You Need." arXiv, 2017,  https://doi.org/10.48550/arXiv.1706.03762.'}]}
TRANSLATED: {'id': 'user_oriented_task_3', 'motivation_app': 'Google Scholar', 'instruction': '당신은 논문 인용문을 받았습니다. 요청된 인용 스타일로 변경해주세요.', 'instances': [{'input': '시카고: 바스와니, 아시시, 샤지어, 노암, 파마르, 니키, 우시코레이트, 야콥, 존스, 릴리온, 고메즈, 에이단 엔., 카이저, 루카시, 및 일리아 폴로수킨. "주목만 있으면 충분합니다." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.\nMLA:', 'output': '바스와니, 아시시 등. "주의가 전부입니다." arXiv, 2017, https://doi.org/10.48550/arXiv.1706.03762.'}]}
4it [02:34, 38.46s/it]
ORIGINAL: {'id': 'user_oriented_task_4', 'motivation_app': 'Grammarly', 'instruction': "Desk jobs require writing a lot of emails, so it isn't surprising we get tired of repeating ourselves. Come up with several synonyms for the given word.", 'instances': [{'input': 'Sincerely', 'output': 'Best regards, All the best, Cheers, Best'}]}
TRANSLATED: {'id': 'user_oriented_task_4', 'motivation_app': 'Grammarly', 'instruction': '책상 일은 많은 이메일을 작성해야 하기 때문에, 우리가 계속 반복해서 지치는 것은 놀랍지 않다. 주어진 단어에 대한 몇 가지 동의어를 생각해보세요.', 'instances': [{'input': '진심으로', 'output': '감사합니다, 모두 좋은 일 있으시길, 건배, 최고'}]}
5it [02:52, 31.04s/it]
ORIGINAL: {'id': 'user_oriented_task_5', 'motivation_app': 'Gmail', 'instruction': 'If you could help me write an email to my friends inviting them to dinner on Friday, it would be greatly appreciated.', 'instances': [{'input': '', 'output': "Hi there,\n\nI hope you're all doing well. I'm inviting you over for dinner on Friday night. Please let me know if you can make it. I'll be cooking your favorite dishes!\n\nLooking forward to seeing you,"}]}
TRANSLATED: {'id': 'user_oriented_task_5', 'motivation_app': 'Gmail', 'instruction': '만약 금요일 저녁 식사에 친구들을 초대하는 이메일을 작성하는 데 도와주신다면 정말 감사하겠습니다.', 'instances': [{'input': '', 'output': '안녕하세요,\n\n여러분 모두 잘 지내고 계시길 바랍니다. 금요일 밤에 저희 집에서 저녁식사를 위해 여러분을 초대하고 싶습니다. 가능하다면 알려주세요. 여러분이 좋아하는 음식을 만들어볼게요!\n\n뵙기를 기대하며,'}]}
5it [03:17, 39.56s/it]
```

### Eval

TBD