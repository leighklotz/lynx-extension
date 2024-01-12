from collections import namedtuple

import re
import gradio as gr
try:
    import modules.shared as shared
except ImportError:
    shared = namedtuple('shared', ['processing_message', { 'truncation_length': 7999 } ])

import subprocess
import shlex

MAX_LENGTH_IN_CHARS=shared.settings['truncation_length']*4-1000
LABEL = "Enable Lynx"
START_REGEX = r"^(!lynx|!links)\b"
PROCESSING_MESSAGE = "*Retrieving URL...*"
TYPING_MESSAGE = "*Is typing...*"
#CONTEXT = "Relevant content is in the Lynx Web Page text results. Use this info in the response."
# Context sticks around too long in the chat.
CONTEXT=None
TEXT_INTRO = "##########\nLynx Web Page text results:"
TEXT_OUTRO = "##########\nAbove is Lynx web page text results "

lynx_access = True

LYNX_COMMAND="lynx"
LINKS_COMMAND="links"


def lynx_results(url, cmd=LYNX_COMMAND):
    command = f"{cmd} -dump {shlex.quote(url)}"
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        m = f"An error occurred: {e}"
        print(m)
        return m

def ui():
    global lynx_access
    checkbox = gr.Checkbox(value=lynx_access, label=LABEL)
    checkbox.change(fn=update_lynx_access, inputs=checkbox)
    return checkbox, lynx_access


def update_lynx_access(checkbox_value):
    global lynx_access
    lynx_access = checkbox_value
    return lynx_access, checkbox_value


def input_modifier(user_input, state):
    global lynx_access
    if lynx_access:
        if re.match(START_REGEX, user_input):
            shared.processing_message = PROCESSING_MESSAGE
            cmd = re.search(START_REGEX, user_input).group(1).replace("!", "")
            if cmd in  [LYNX_COMMAND, LINKS_COMMAND]:
                results =  retrieve_and_prompt(user_input, state, cmd=LYNX_COMMAND)
            else:
                raise Exception("Unknown command", cmd)
            return results
    shared.processing_message = TYPING_MESSAGE
    return user_input

def retrieve_and_prompt(user_input, state, cmd=LYNX_COMMAND):
    query_lines = user_input.split("\n")
    url = re.sub(START_REGEX, '', query_lines[0]).strip()
    user_question = '\n'.join(query_lines[1:]).strip()
    if CONTEXT:
        state["context"] = state["context"] + CONTEXT
    lynx_data = lynx_results(url, cmd)
    if len(lynx_data) > MAX_LENGTH_IN_CHARS:
        lynx_data = f"[Text bwlow Truncated to {MAX_LENGTH_IN_CHARS}]:\n{lynx_data[0:MAX_LENGTH_IN_CHARS-1]}"
    user_prompt = f"""User question about the text: {user_question}
{TEXT_INTRO} for {url}:
{lynx_data}
{TEXT_OUTRO} for {url}.
User question:\n{user_question}
"""
    print(f"{user_prompt=}")
    return user_prompt


def output_modifier(output):
    return output


def bot_prefix_modifier(prefix):
    return prefix


def show_test(user_input):
    print(f"{user_input=}")
    print(f"{input_modifier(user_input, state)=}")
    print(f"{state['context']=}")
    

if __name__ == "__main__":
    state = {"context": "START: "}

    show_test("!lynx http://klotz.me\nSummarize the above site.")
    show_test("!links http://klotz.me\nSummarize the above site.")
    show_test("!lynx https://scuttle.klotz.me/\nSummarize the above site.")
        
