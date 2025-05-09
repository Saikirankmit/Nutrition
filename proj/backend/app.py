from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import PIL.Image
import io

app = Flask(__name__)
CORS(app)

genai.configure(api_key="")  
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        image = PIL.Image.open(io.BytesIO(image_bytes))

        prompt = """
You are a food recognition and calorie estimation expert.

Given an image of food, identify and list:
1. Each food item
2. Estimated portion size
3. Estimated calorie content
4. Estimated protein content

Return the result in this exact format (no extra comments):

<Food Item 1>
Portion: <Size>
Calories: <kcal>
Protein: <g>
Fat:<g>
Carbohydrates:<g>

<Food Item 2>
Portion: <Size>
Calories: <kcal>
Protein: <g>
Fat:<g>
Carbohydrates:<g>

...

Total Estimated Calories: <kcal>
Total Estimated Protein: <g>
Total Estimated Fats: <g>
Total Estimated Carbohydrates: <g>
"""
        response = model.generate_content([prompt, image])
        result = response.text

        html_output = "<div style='line-height:1.6em;'>"
        for line in result.splitlines():
            if line.strip() == "":
                html_output += "<br>"
            else:
                html_output += f"{line}<br>"
        html_output += "</div>"

        return jsonify({"result": html_output})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Analysis failed", "details": str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        user_message = request.json.get('message', '')

        chat_model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        convo = chat_model.start_chat()
        convo.send_message("You are a nutrition assistant. Help users with food facts, diet tips, or explain calorie estimates.")
        response = convo.send_message(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        error_message = str(e)
        print("Chatbot error:", error_message)

        # Check for quota exceeded message
        if "quota" in error_message.lower() or "429" in error_message:
            return jsonify({
                "reply": "🚫 Daily limit for chatbot requests has been reached. Please try again tomorrow or upgrade your plan."
            }), 429
        
        return jsonify({
            "reply": "⚠️ Oops! I had trouble responding. Please try again later."
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
