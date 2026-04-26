import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    user_text = ""
    summary_type = "short"

    if request.method == "POST":
        user_text = request.form["text"]
        summary_type = request.form["summary_type"]

        if summary_type == "short":
            system_prompt = "Summarize the text into exactly 3 short bullet points. Do not add any introduction. Return only bullet points starting with '-'."

        elif summary_type == "detailed":
            system_prompt = "Summarize the text into exactly 5 detailed bullet points. Do not add any introduction. Return only bullet points starting with '-'."

        elif summary_type == "actions":
            system_prompt = "Extract exactly 5 action points from the text. Do not add any introduction. Return only bullet points starting with '-'."

        else:
            system_prompt = "Summarize the text into exactly 3 bullet points. Do not add any introduction. Return only bullet points starting with '-'."

        if user_text.strip() == "":
            user_text = ""
            summary = "Please enter some text to summarize."

        elif len(user_text) > 1000:
            user_text = user_text[:1000] + "..."
            summary = "Please enter text with less than 1000 characters."

        else:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            )

            summary = response.choices[0].message.content

    points = [p.lstrip("- ").strip() for p in summary.split("\n") if p.strip()]

    return render_template(
        "index.html",
        summary=points,
        user_text=user_text,
        summary_type=summary_type
    )

if __name__ == "__main__":
    app.run(debug=True)
