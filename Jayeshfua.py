from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Sticker layout constants
STICKER_WIDTH = 6.4 * cm
STICKER_HEIGHT = 3.4 * cm
SEPARATION = 0.3 * cm
LEFT_MARGIN = 0.6 * cm
RIGHT_MARGIN = 0.3 * cm
TOP_MARGIN = 1.2 * cm
BOTTOM_MARGIN = 1.2 * cm
PAGE_WIDTH, PAGE_HEIGHT = A4


def create_sticker_page(c, invoice_number, start_box, total_boxes):
    """
    Draws the stickers on a single page of the PDF.
    
    Args:
        c: The canvas object for the PDF.
        invoice_number: The invoice number to display on the stickers.
        start_box: The starting box number for this page.
        total_boxes: The total number of boxes to print stickers for.
    """
    x_offset = LEFT_MARGIN
    y_offset = PAGE_HEIGHT - TOP_MARGIN - STICKER_HEIGHT

    stickers_per_row = int((PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN + SEPARATION) // (STICKER_WIDTH + SEPARATION))
    stickers_per_col = int((PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) // STICKER_HEIGHT)
    stickers_per_page = stickers_per_row * stickers_per_col
    
    current_box = start_box
    for row in range(stickers_per_col):
        for col in range(stickers_per_row):
            if current_box > total_boxes:
                return current_box
            
            x = x_offset + col * (STICKER_WIDTH + SEPARATION)
            y = y_offset - row * STICKER_HEIGHT  # No separation for top and bottom
            
            # Draw the border for the sticker with rounded corners
            c.roundRect(x, y, STICKER_WIDTH, STICKER_HEIGHT, 0.2 * cm)  # Reduced corner radius to 0.2 cm
            
            # Add text to the sticker
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(x + STICKER_WIDTH / 2, y + STICKER_HEIGHT - 1 * cm, f"Invoice: {invoice_number}")
            c.setFont("Helvetica", 10)
            c.drawCentredString(x + STICKER_WIDTH / 2, y + STICKER_HEIGHT / 2, f"Box {current_box} of {total_boxes}")
            
            current_box += 1
    
    return current_box


def generate_stickers(invoice_number, total_boxes):
    """
    Generates a PDF file with stickers for the given invoice number and number of boxes.
    
    Args:
        invoice_number: The invoice number to display on each sticker.
        total_boxes: The total number of boxes to create stickers for.
    """
    output_file = f"stickers_{invoice_number}.pdf"
    c = canvas.Canvas(output_file, pagesize=A4)
    
    current_box = 1
    while current_box <= total_boxes:
        current_box = create_sticker_page(c, invoice_number, current_box, total_boxes)
        c.showPage()  # Move to the next page
    
    c.save()
    print(f"Stickers have been saved to {output_file}")


def main():
    """
    Main function to get user input and generate stickers.
    """
    invoice_number = input("Enter the invoice number: ").strip()
    try:
        total_boxes = int(input("Enter the total number of boxes: ").strip())
        if total_boxes < 1:
            raise ValueError("The number of boxes must be at least 1.")
    except ValueError as e:
        print("Invalid input. Please enter a valid number of boxes.")
        return
    
    generate_stickers(invoice_number, total_boxes)


if __name__ == "__main__":
    main()
