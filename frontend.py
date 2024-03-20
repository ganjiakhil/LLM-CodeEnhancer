import streamlit as st
import openai

openai.api_key = "EMPTY"
openai.api_base = "http://localhost:8000/v1"

models = openai.Model.list()

st.markdown(
    """
    <style>
    .my-textarea {
        height: auto;
        min-height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("CodeEnhancer - Make your code follow PEP standards")

user_input = st.text_area("Enter Input:", placeholder="Insert your python code here...")

system="""\
  You are a Software Engineer whose work is to work on a codebase consisting of Python and other language code,\
  your responsibility is to beautify the Python code by adding proper indentation,\
  adding typing and adhering to the PEP standards, you can also add Typing,\
  docstrings on each classes and functions, also at the top of the scripts,\
  you are NOT ALLOWED to work on languages other than python.
  You should also ONLY respond with the code,\
  do NOT start with your response like 'SOLUTION',\
  'Here is the code with proper indentation, typing, and adherence to PEP standards:',\
  'Here's the corrected code with proper indentation and syntax',\
  'Sure! Here's the corrected code:'.
  you MUST and MUST REPLY ONLY WITH THE CODE AND MUST NOT PROVIDE EXPLANATION. \n
"""

example='''
def calculate_average(numbers):
		total = 0
	for num in numbers:
total+=num
		return total / len(numbers)
'''

formatted_code='''
def calculate_average(numbers):
	"""
	Calculate the average of a list of numbers.
	"""
	total = 0
	for num in numbers:
		total += num
	return total / len(numbers)
'''

user_message = {
    "input": example,
    "output": formatted_code
}

prompt =f"<<SYS>>\\n{system}\\n<</SYS>>\\n\\n{user_message['input']}"
prompt += f"<s>[INST] {prompt} [/INST] {user_message['output']} </s>"
prompt += f"<s>[INST] {user_input} [/INST]"

if st.button("Submit"):
    # processed_output = f"You entered: {user_input}"
    model = models["data"][0]["id"]
    completion = openai.Completion.create(model="codellama/CodeLlama-7b-Instruct-hf",
                                          prompt=prompt,
                                          max_tokens=6000, 
                                          temperature=0)
    # st.write("Corrected code:")
    st.write(completion["choices"][0]["text"])

