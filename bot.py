from flask import Flask, render_template, request
import os
import google.generativeai as genai

# Configure the generative AI API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
                        """you are a chatbot / LLM that has been specially used for the domain of 
                        predicting fuel consumption in transport fleets so you have to be 
                        answer the questions that has been related to your domain only. 
                        You shouldn't answer for any unnecessary questions and you can 
                        answer any questions related to Vehicles, transportation, Vehicle details, etc...\n and give answers in short and detailed """,
    ),
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    bot_response = ""

    if request.method == "POST":
        user_input = request.form.get("user_input")

        # Avoid empty inputs
        if user_input.strip():
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            bot_response = response.text

    return render_template("index.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
