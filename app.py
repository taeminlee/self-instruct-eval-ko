import gradio as gr
import jsonlines

# 데이터 준비
with jsonlines.open('user_oriented_instructions_deepl_ko.jsonl') as reader:
    idxs = [obj['id'] for obj in reader]
with jsonlines.open('user_oriented_instructions_deepl_ko_eval_chatgpt.jsonl') as reader:
    chatgpt = {obj['id']: obj for obj in reader}
with jsonlines.open('user_oriented_instructions_deepl_ko_eval_gpt4.jsonl') as reader:
    gpt4 = {obj['id']: obj for obj in reader}


# 마크다운 변환
def extract_output(model:str, obj: dict):
        return f"""## {model}
{obj['instances'][0]['output']}"""

def extract_input_md(obj: dict):
        return f"""## Instruction
{obj['instruction']}
## Input
{obj['instances'][0]['input']}

---
"""

def update(idx):
    return [extract_input_md(chatgpt[idx]), extract_output('chatgpt', chatgpt[idx]), extract_output('gpt4', gpt4[idx])]

# 데이터 이동
def dec(idx):
    return move(idx, -1)

def inc(idx):
    return move(idx, 1)

def move(idx, step):
    selected_idx = idxs.index(idx)
    selected_idx += step
    selected_idx = max(0, selected_idx)
    selected_idx = min(selected_idx, len(idxs))
    return idxs[selected_idx]


with gr.Blocks() as demo:
    gr.Markdown("Select example from the following dropdown and see the results for LLMs.")
    # 드롭다운 리스트
    dd = gr.Dropdown(idxs, label="id", info="user oriented instruction task id", value=idxs[0])
    with gr.Row():
        # 아이템 이동 버튼
        lb = gr.Button("<-").style(full_width=True)
        rb = gr.Button("->").style(full_width=True)
    # 명령 및 입력 출력
    ins = gr.Markdown(extract_input_md(chatgpt[idxs[0]]))
    with gr.Row():
        # chatgpt 결과 출력
        out1 = gr.Markdown(extract_output('chatGPT', chatgpt[idxs[0]]))
        # gpt4 결과 출력
        out2 = gr.Markdown(extract_output('GPT4', gpt4[idxs[0]]))

    lb.click(dec, inputs=dd, outputs=dd)
    rb.click(inc, inputs=dd, outputs=dd)
    dd.change(update, dd, [ins, out1, out2])

demo.launch(share=True)