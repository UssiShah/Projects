# SMS Chatbot with OpenAI and Flask

This project demonstrates how to build a simple SMS chatbot using **Flask**, **OpenAI's API**, and a conversational memory feature. The chatbot remembers the last few messages in a conversation and responds with concise, simple answers. The project was developed during a workshop conducted by [46elks](https://46elks.com/pycon).

---

## **Features**
- Creates a chatbot accessible via SMS.
- Uses OpenAI's conversational models for intelligent responses.
- Maintains a conversation history for context-aware replies.
- Configurable to run on any server or local environment.

---

## **Prerequisites**
Before running the application, make sure you have:
- Python 3.7 or higher installed.
- An [OpenAI API key](https://platform.openai.com/signup).
- Flask and the OpenAI Python library installed.
- Access to an SMS API service (like [46elks](https://46elks.com/)) to route incoming SMS messages to the Flask server.

---

## **Setup Instructions**

### **1. Clone the Repository**
Clone this project or copy the code into your development environment.

### **2. Install Dependencies**
Install the necessary Python libraries:
```bash
pip install flask openai
```

### **3. Configure Your API Key**
Create a `creds.py` file and add your OpenAI API key:
```python
# creds.py
openai_key = "your_openai_api_key_here"
```

### **4. Run the Application**
Start the Flask application:
```bash
python app.py
```
By default, the app will run on `http://0.0.0.0:5163`.

---

## **Code Overview**

### **1. Application Setup**
The code initializes a Flask app and sets up a POST endpoint `/sms` to handle incoming SMS messages.

### **2. Conversation History**
A global variable, `conversation_history`, is used to store the last few messages exchanged between the user and the chatbot. This enables context-aware responses.

### **3. OpenAI Integration**
The application uses the OpenAI Python library to generate responses:
- It combines the conversation history with a system prompt for concise and simple replies.
- Responses are limited to **160 characters**, making them SMS-friendly.

### **4. SMS Endpoint (`/sms`)**
When an SMS message is received:
1. The user's message is added to the conversation history.
2. OpenAI generates a response based on the conversation context.
3. The chatbot's response is added to the conversation history and returned to the SMS sender.

---

## **How It Works**
1. Incoming SMS messages are sent to the Flask server.
2. The `/sms` endpoint processes the message and sends it to OpenAI for response generation.
3. The chatbot's reply is returned to the sender.

---

## **Deployment**

### **1. Using ngrok for Local Testing**
Use [ngrok](https://ngrok.com/) to expose your local server to the internet:
```bash
ngrok http 5163
```
Ngrok will provide a public URL that can be used to route incoming SMS messages.

### **2. Integrating with 46elks**
46elks provides an easy-to-use SMS API that can forward incoming messages to your server. Configure 46elks to route SMS messages to your ngrok or server URL.

Learn more about setting up SMS with 46elks at their [PyCon workshop page](https://46elks.com/pycon).

---

## **Sample Usage**
1. Send an SMS to the number connected to your 46elks account.
2. The chatbot will reply intelligently, remembering the last few messages for context.

---

## **About the Workshop**
This project was created during a workshop hosted by [46elks](https://46elks.com/) at **PyCon**. The workshop focused on:
- Setting up SMS services using the 46elks API.
- Creating conversational bots using OpenAI's models.
- Integrating local servers with ngrok for public accessibility.

Explore more about 46elks and their developer-friendly tools [here](https://46elks.com/).

---

## **Contributors**
This project is a collaborative effort from the workshop participants. Special thanks to **46elks** for providing resources and guidance.

---

Feel free to extend or modify this project for your use cases. For any questions or feedback, visit [46elks support](https://46elks.com/support).