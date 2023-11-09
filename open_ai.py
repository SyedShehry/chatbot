import openai
import os
openai.api_key = ""
def chat_bot(question, info):
    chat = openai.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "you are a AI assistant  how will answer the question of user based on the data provided. if you dont find the answer return a response thaat data doesnot  have answer for this question"},
        {
            "role": "user",
            "content": f"""answer the question based on the question, using the information provided
            '''question: {question}'''
            '''information: {info}'''
            """
        }
    ],
    temperature=0
    )
    return chat.choices[0].message.content