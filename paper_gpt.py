import gradio as gr
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_APIKEY')

def get_gpt_response_json(comment=""):
    completion = openai.chat.completions.create(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "user", "content": comment+' return in json format, Please fill in your answer, don’t leave anything out, don’t use ... to omit content.'}
        ]
    )

    response_str = completion.choices[0].message.content
    response_str = response_str.replace('\\\\','\\')
    return response_str

def process(latex, comment, line):
    line_start = 0
    if line:
        line_offset = 10
        line_num = int(line)
        latex = latex.split('\n')
        line_start = line_num-line_offset-1 if line_num-line_offset-1 > 0 else 0
        latex = '\n'.join(latex[line_start:line_num+line_offset-1])

    prompt = 'You are a scientist who is good at writing papers. Please modify the following LaTex according to the suggestions.'
    prompt += '\n---------------------------------------------------'
    prompt += 'Example 1: '
    prompt += 'Latex: '
    prompt += '$x^2 + 2x + 1 = 0$'
    prompt += '\nSuggestions: Please change the equation to $x^2 + 2x = 0$ Output: {"origin":"$x^2 + 2x + 1 = 0$", change:"$x^2 + 2x = 0$", "line":1}'
    prompt += '\n---------------------------------------------------'
    prompt += f'Now you have the following LaTex : {latex}. Please modify LaTex according to the following suggestions : {comment}'
    
    response_json = get_gpt_response_json(comment=prompt)
    return str(response_json)
	
with gr.Blocks(title='Paper GPT') as demo:
    gr.Markdown('# Paper GPT')
    with gr.Row():
        textbox1 = gr.Textbox(lines=29, label="LaTex", show_label=True, show_copy_button=True)
        with gr.Column():
            textbox2 = gr.Textbox(lines=5, label="Comment", show_label=True)
            textbox_line = gr.Textbox(lines=1, label="Line", show_label=True)
            btn = gr.Button(value="Submit", variant="primary")
            textbox3 = gr.Textbox(lines=11, label="Change", show_label=True)

    btn.click(process, [textbox1, textbox2, textbox_line], textbox3)

demo.launch()