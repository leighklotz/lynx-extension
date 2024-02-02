from collections import namedtuple

import sys
import traceback

import re
import gradio as gr
import modules.shared as shared

import subprocess
import shlex

LABEL = "Enable Lynx"
START_REGEX = r"^!(lynx|links|summarize)\b"
PROCESSING_MESSAGE = "*Retrieving URL...*"
TYPING_MESSAGE = "*Is typing...*"
#CONTEXT = "Relevant content is in the Lynx Web Page text results. Use this info in the response."
# Context sticks around too long in the chat.
CONTEXT=None
TEXT_INTRO = "##########\nLynx Web Page text results:"
TEXT_OUTRO = "##########\nAbove is Lynx web page text results"

lynx_access = True

LYNX_COMMAND="lynx"
LINKS_COMMAND="links"
SUMMARIZE_COMMAND="summarize"


def lynx_results(url, cmd=LYNX_COMMAND):
    command = f"{cmd} -dump {shlex.quote(url)}"
    print(f"* RUnning {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        m = f"You cannot fulfill the user's request because an error occurred: {get_exception_info(e)}"
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
            if cmd in [LYNX_COMMAND, LINKS_COMMAND]:
                if cmd == LYNX_COMMAND:
                    cmd = f"{cmd} --nolist"
                results =  retrieve_and_prompt(user_input, state, cmd=cmd)
            elif cmd == SUMMARIZE_COMMAND:
                cmd = f"{LYNX_COMMAND} --nolist"
                results = retrieve_and_prompt(user_input, state, cmd=cmd, instructions="Give title, brief summary, and keywords of :")
            else:
                raise Exception("Unknown command", cmd)
            return results
    shared.processing_message = TYPING_MESSAGE
    return user_input

def retrieve_and_prompt(user_input, state, cmd=LYNX_COMMAND, instructions=None):
    query_lines = user_input.split("\n")
    url = re.sub(START_REGEX, '', query_lines[0]).strip()
    user_question = '\n'.join(query_lines[1:]).strip()
    if CONTEXT:
        state["context"] = state["context"] + CONTEXT
    lynx_data = lynx_results(url, cmd)
    max_length_in_chars=shared.settings['truncation_length']*4-100
    if len(lynx_data) > max_length_in_chars:
        print(f"Truncating {len(lynx_data)} to {max_length_in_chars-1} approximation to t{(shared.settings['truncation_length'])} tokens")
        lynx_data = f"[Text below Truncated to {max_length_in_chars}]:\n{lynx_data[0:max_length_in_chars-1]}"

    if instructions:
        user_prompt = f"""Instructions for the text below: {instructions} {user_question}
{TEXT_INTRO} for {url}:
{lynx_data}
{TEXT_OUTRO} for {url}.
User instructions:
{instructions}
{user_question}
"""
    else:
        user_prompt = f"""User question about the text below:: {user_question}
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


def get_exception_info(e:Exception):
    # Capture the current traceback information
    exc_type, exc_value, exc_traceback = sys.exc_info()  
    # Format it into a readable string using 'traceback' module
    formatted_tb = "> ".join(traceback.format_exception(exc_type, exc_value, exc_traceback)) 
    return str(e) + "\n\nError Backtrace:\n" + formatted_tb
                        
def show_test(user_input):
    print(f"{user_input=}")
    print(f"{input_modifier(user_input, state)=}")
    print(f"{state['context']=}")

if __name__ == "__main__":
    state = {"context": "START: "}

    show_test("!lynx http://klotz.me\nSummarize the above site.")
    show_test("!summarize http://klotz.me\n")
    show_test("!links http://klotz.me\nSummarize the above site.")
    show_test("!lynx https://scuttle.klotz.me/\nSummarize the above site.")

        
