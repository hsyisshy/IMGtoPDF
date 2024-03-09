import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
from io import BytesIO

def convert_to_pdf():
    image_urls = entry_urls.get("1.0", tk.END).splitlines()
    if not image_urls:
        messagebox.showerror("Error", "Please enter image URLs.")
        return

    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_pdf:
        return

    # Call your function to convert images to PDF
    try:
        images_to_pdf(image_urls, output_pdf)
        messagebox.showinfo("Success", "PDF file created successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def download_images(image_urls, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download each image and save it to the output folder
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            with Image.open(image_data) as img:
                img.save(os.path.join(output_folder, f'image_{i+1}.jpg'))
        else:
            print(f"Failed to download image {i+1} from URL: {url}")

def images_to_pdf(image_urls, pdf_file):
    output_folder = "./temp_images"
    download_images(image_urls, output_folder)

    # Get all image files from the specified folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))]
    image_files.sort()  # Sort image files

    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Get the page dimensions
    page_width, page_height = letter

    for image_file in image_files:
        image_path = os.path.join(output_folder, image_file)

        with Image.open(image_path) as img:
            aspect_ratio = img.width / img.height

            # Calculate the width and height to fit the page
            max_width, max_height = letter
            width = min(img.width, max_width)
            height = width / aspect_ratio

            # Calculate the position to center the image on the page
            x = (page_width - width) / 2
            y = (page_height - height) / 2

            c.drawImage(image_path, x, y, width=width, height=height, preserveAspectRatio=True)
            c.showPage()

    c.save()

# Create the main window
root = tk.Tk()
root.title("Image to PDF Converter")

# Create widgets
label_urls = tk.Label(root, text="Enter Image URLs (one per line):")
label_urls.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

entry_urls = tk.Text(root, width=50, height=10)
entry_urls.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

button_convert = tk.Button(root, text="Convert to PDF", command=convert_to_pdf)
button_convert.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Run the application
root.mainloop()
