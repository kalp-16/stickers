from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os

# Sticker layout constants
STICKER_WIDTH = 6.4 * cm
STICKER_HEIGHT = 3.4 * cm
SEPARATION = 0.3 * cm  # Horizontal space between stickers
LEFT_MARGIN = 0.6 * cm
RIGHT_MARGIN = 0.3 * cm
TOP_MARGIN = 1.2 * cm
BOTTOM_MARGIN = 1.2 * cm
PAGE_WIDTH, PAGE_HEIGHT = A4


def create_sticker_page(c, invoice_number, start_box, total_boxes):
    """
    Draws stickers on a single page, with no vertical separation between rows.
    """
    x_offset = LEFT_MARGIN
    y_offset = PAGE_HEIGHT - TOP_MARGIN

    # Calculate number of stickers per row and column
    stickers_per_row = int((PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN + SEPARATION) // (STICKER_WIDTH + SEPARATION))
    stickers_per_col = int((PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) // STICKER_HEIGHT)

    current_box = start_box
    for row in range(stickers_per_col):
        for col in range(stickers_per_row):
            if current_box > total_boxes:
                return current_box

            # Calculate sticker position
            x = x_offset + col * (STICKER_WIDTH + SEPARATION)
            y = y_offset - row * STICKER_HEIGHT - STICKER_HEIGHT

            # Draw rounded rectangle for the sticker
            c.roundRect(x, y, STICKER_WIDTH, STICKER_HEIGHT, 0.2 * cm)

            # Add text to the sticker
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x + STICKER_WIDTH / 2, y + STICKER_HEIGHT - 1 * cm, f"Invoice: {invoice_number}")
            c.setFont("Helvetica", 9)
            c.drawCentredString(x + STICKER_WIDTH / 2, y + STICKER_HEIGHT / 2, f"Box {current_box} of {total_boxes}")

            current_box += 1

    return current_box


def generate_stickers(invoice_number, total_boxes):
    """
    Generates a PDF with stickers.
    """
    output_file = f"static/stickers_{invoice_number}.pdf"
    c = canvas.Canvas(output_file, pagesize=A4)

    current_box = 1
    while current_box <= total_boxes:
        current_box = create_sticker_page(c, invoice_number, current_box, total_boxes)
        c.showPage()

    c.save()
    return output_file


# Flask App Routes
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    invoice_number = request.form.get('invoice')
    total_boxes = request.form.get('boxes')

    try:
        total_boxes = int(total_boxes)
        if total_boxes < 1:
            raise ValueError("Number of boxes must be at least 1.")
    except ValueError:
        return "Invalid number of boxes. Please enter a valid integer."

    pdf_file = generate_stickers(invoice_number, total_boxes)
    return send_file(pdf_file, as_attachment=True)


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)  # Ensure static directory exists
    app.run(debug=True)
