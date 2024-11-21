from flask import Flask, request
from openai import OpenAI
from creds import openai_key

# Enter your OpenAI API key here
client = OpenAI(openai_key)
app = Flask(__name__)

# Initialize conversation history
conversation_history = []

@app.route('/sms', methods=['POST'])
def sms():
    global conversation_history
    message = request.form.get('message')

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer with max 160 characters and use only simple language."}
        ] + conversation_history,
        max_tokens=160
    )

    response = completion.choices[0].message.content

    # Add assistant response to conversation history
    conversation_history.append({"role": "assistant", "content": response})

    print(response)
    return (str(response), 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5163)

