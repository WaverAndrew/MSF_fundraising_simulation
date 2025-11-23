import qrcode
from PIL import Image, ImageDraw


def generate_rounded_qr_code(url: str, size: int = 500, border: int = 4, corner_radius: int = 20) -> Image.Image:
    """
    Generate a QR code with rounded square corners.
    
    Args:
        url: The URL to encode in the QR code
        size: The size of the output image in pixels (default: 500)
        border: The border size around the QR code (default: 4)
        corner_radius: The radius of the rounded corners in pixels (default: 20)
    
    Returns:
        PIL Image object with rounded square QR code
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=border,
    )
    
    # Add data to QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize to desired size
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create a mask for rounded corners
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw rounded rectangle on mask
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=255
    )
    
    # Convert QR code to RGBA to support transparency
    qr_rgba = qr_img.convert('RGBA')
    
    # Apply mask to alpha channel
    qr_rgba.putalpha(mask)
    
    # Create output image with white background
    final_img = Image.new('RGB', (size, size), (255, 255, 255))
    
    # Paste QR code onto output (mask is applied via alpha channel)
    final_img.paste(qr_rgba, (0, 0), qr_rgba)
    
    return final_img


def save_rounded_qr_code(url: str, output_path: str, size: int = 500, border: int = 4, corner_radius: int = 20) -> None:
    """
    Generate and save a rounded square QR code to a file.
    
    Args:
        url: The URL to encode in the QR code
        output_path: Path where to save the QR code image
        size: The size of the output image in pixels (default: 500)
        border: The border size around the QR code (default: 4)
        corner_radius: The radius of the rounded corners in pixels (default: 20)
    """
    qr_img = generate_rounded_qr_code(url, size, border, corner_radius)
    qr_img.save(output_path)


if __name__ == "__main__":
    # Example usage
    url = "https://msf-project-bocconi.streamlit.app"
    output_file = "rounded_qr_code.png"
    
    print(f"Generating rounded QR code for: {url}")
    save_rounded_qr_code(url, output_file, size=500, corner_radius=30)
    print(f"QR code saved to: {output_file}")

