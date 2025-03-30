from flask import Flask, request, render_template
import pytesseract
from PIL import Image
from transformers import pipeline
import sympy as sp

app = Flask(__name__)

# Betöltjük a nyelvi modellt
text_generator = pipeline("text-generation", model="gpt2")

# Szöveg generálás
@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form['input_text']
    output = text_generator(input_text, max_length=150, num_return_sequences=1)
    return render_template('index.html', result=output[0]['generated_text'])

# Matematikai feladat megoldás
@app.route('/solve_math', methods=['POST'])
def solve_math():
    equation = request.form['equation']
    x = sp.Symbol('x')
    try:
        egyenlet = sp.sympify(equation)
        megoldas = sp.solve(egyenlet, x)
        return render_template('index.html', math_result=str(megoldas))
    except Exception as e:
        return render_template('index.html', math_result="Hiba: " + str(e))

# Kép szövegfelismerés
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template('index.html', ocr_result="Nincs feltöltött fájl!")
    file = request.files['image']
    image = Image.open(file)
    text = pytesseract.image_to_string(image, lang="eng+hun+ron") # angol, magyar, román nyelv
    return render_template('index.html', ocr_result=text)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
