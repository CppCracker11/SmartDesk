from PIL import Image

img = Image.open("assets/smartdesk_logo.png").convert("RGBA")

img.save(
    "assets/smartdesk.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ],
)

print("Created assets/smartdesk.ico")