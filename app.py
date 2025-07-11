from flask import Flask, request , render_template
import openai
app = Flask(__name__)

openai.api_key = "YourAPIKEY"
@app.route('/', methods=['GET', 'POST'])
def index():
    explanation =" "
    fixed_code =" "
    if request.method == 'POST':
        code = request.form['code']
        error = request.form['error']

        prompt= (f"Explain the error in this code without fixing it:"
                 f"\n\n{code}\n\n{error}")
        model_engine ="gpt-3.5-turbo"

        explanation_completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.8
        )

        explanation = explanation_completions['choices'][0]['message']['content'].strip()

        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\n{error}."
                             f"\nRespond only fixed code.")
        fixed_code_completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": fixed_code_prompt}
            ],
            max_tokens=1024,
            temperature=0.8
        )

        fixed_code = fixed_code_completions['choices'][0]['message']['content'].strip()
    return render_template("index.html", explanation=explanation,fixed_code=fixed_code)

if __name__ == '__main__':
    app.run(debug=True)