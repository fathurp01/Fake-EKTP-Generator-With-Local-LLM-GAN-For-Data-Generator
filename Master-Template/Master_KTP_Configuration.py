import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# ==========================================
# ALAT TUNING KORDINAT FINAL (DENGAN TRANSPARANSI SEMI-BOLD)
# ==========================================
TEMPLATE_PATH = "Master-Template\Master-ktp.png"

test_items = [
    {"key": "provinsi", "label": "PROVINSI", "text": "PROVINSI JAWA BARAT", "anchor": "ms", "size": 22, "font": "font/Arrial.ttf", "x": 312, "y": 30, "type": "text"},
    {"key": "kota", "label": "KOTA", "text": "KABUPATEN CIANJUR", "anchor": "mt", "size": 22, "font": "font/Arrial.ttf", "x": 311, "y": 36, "type": "text"},
    {"key": "nik", "label": "NIK", "text": "3203012503770011", "anchor": "lt", "size": 26, "font": "font/Ocr.ttf", "x": 156, "y": 92, "type": "text", "is_bold": True},
    {"key": "nama", "label": "NAMA", "text": "GUOHUI CHEN", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 124, "type": "text"},
    {"key": "ttl", "label": "TEMPAT/TGL LAHIR", "text": "FUJIAN, 25-03-1977", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 142, "type": "text"},
    {"key": "jenis_kelamin", "label": "JENIS KELAMIN", "text": "MALE", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 160, "type": "text"},
    {"key": "golongan_darah", "label": "GOLONGAN DARAH", "text": "Gol. Darah : B", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 313, "y": 160, "type": "text"},
    {"key": "alamat", "label": "ALAMAT", "text": "JL SELAMET PERUMAHAN RANCABALI", "anchor": "lt", "size": 14, "font": "font/Arrial.ttf", "x": 170, "y": 179, "type": "text"},
    {"key": "rt_rw", "label": "RT/RW", "text": "002/004", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 197, "type": "text"},
    {"key": "kel_desa", "label": "KEL/DESA", "text": "MUKA", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 216, "type": "text"},
    {"key": "kecamatan", "label": "KECAMATAN", "text": "CIANJUR", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 234, "type": "text"},
    {"key": "agama", "label": "AGAMA", "text": "CHRISTIAN", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 252, "type": "text"},
    {"key": "status", "label": "STATUS KAWIN", "text": "MARRIED", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 270, "type": "text"},
    {"key": "pekerjaan", "label": "PEKERJAAN", "text": "OTHERS", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 289, "type": "text"},
    {"key": "kewarganegaraan", "label": "KEWARGANEGARAAN", "text": "CHINA", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 307, "type": "text"},
    {"key": "masa_berlaku", "label": "BERLAKU HINGGA", "text": "12-12-2023", "anchor": "lt", "size": 16, "font": "font/Arrial.ttf", "x": 170, "y": 325, "type": "text"},
    {"key": "kota_footer", "label": "KOTA (Footer)", "text": "KOTA CIANJUR", "anchor": "mt", "size": 16, "font": "font/Arrial.ttf", "x": 525, "y": 299, "type": "text"},
    {"key": "terbuat", "label": "TGL TERBUAT", "text": "17-09-2018", "anchor": "mt", "size": 16, "font": "font/Arrial.ttf", "x": 525, "y": 317, "type": "text"},
    {"key": "sign", "label": "TANDA TANGAN", "text": "GUOHUI", "anchor": "mt", "size": 16, "font": "font/Sign.ttf", "x": 525, "y": 341, "type": "text"},
    {"key": "pas_photo", "label": "PAS FOTO", "text": "FOTO", "anchor": "lt", "size": 155, "font": "font/Arrial.ttf", "x": 444, "y": 93, "type": "photo", "height": 199}
]

current_idx = 2 
text_gray_level = 64  
nik_bold_alpha = 104 # Level transparansi stroke (0=Tipis, 255=Full Bold)
nik_stroke_width = 0.4  # Ketebalan outline (px)

def mouse_event(event, x, y, flags, param):
    global test_items, current_idx
    if event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON)):
        test_items[current_idx]["x"] = x
        test_items[current_idx]["y"] = y

def update_width(val):
    global test_items, current_idx
    if val > 10: test_items[current_idx]["size"] = val

def update_height(val):
    global test_items, current_idx
    if val > 10 and test_items[current_idx]["type"] == "photo":
        test_items[current_idx]["height"] = val

def update_color(val):
    global text_gray_level
    text_gray_level = val

def update_bold(val):
    global nik_bold_alpha
    nik_bold_alpha = val

def update_stroke(val):
    global nik_stroke_width
    if val >= 0:
        nik_stroke_width = val / 100.0

def print_status():
    item = test_items[current_idx]
    print("\n" + "="*50)
    print(f"👉 MENGEDIT : {item['label']}")
    if item["type"] == "photo":
        print(f"   Posisi Kiri-Atas : X={item['x']}, Y={item['y']}")
        print(f"   Ukuran Tuned     : Lebar={item['size']}px, Tinggi={item['height']}px")
    else:
        print(f"   Posisi           : X={item['x']}, Y={item['y']} | Font Size={item['size']}")
    print(f"   Warna Teks Final : RGB({text_gray_level}, {text_gray_level}, {text_gray_level})")
    print(f"   Ketebalan NIK    : {nik_bold_alpha}/255 | Stroke={nik_stroke_width:.2f}px")
    print("="*50)

def run_tuner():
    global current_idx, text_gray_level, nik_bold_alpha
    
    if not os.path.exists(TEMPLATE_PATH):
        return print(f"❌ Gambar '{TEMPLATE_PATH}' tidak ditemukan!")

    # Use RGBA so semi-transparent stroke_fill alpha is honored
    base_pil = Image.open(TEMPLATE_PATH).convert("RGBA")
    window_name = "KTP Master Pro Tuner (Alpha-Bold)"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(window_name, mouse_event)
    
    cv2.createTrackbar("Font Size/Lebar", window_name, test_items[current_idx]["size"], 400, update_width)
    initial_h = test_items[current_idx].get("height", 100)
    cv2.createTrackbar("Tinggi Foto", window_name, initial_h, 400, update_height)
    cv2.createTrackbar("Warna Teks (0=Hitam)", window_name, text_gray_level, 255, update_color)
    
    # Slider khusus untuk ketebalan/transparansi outline NIK
    cv2.createTrackbar("Tebal NIK (0=Tipis)", window_name, nik_bold_alpha, 255, update_bold)
    cv2.createTrackbar("Ketebalan Outline", window_name, int(nik_stroke_width * 100), 100, update_stroke)

    print_status()

    while True:
        temp_pil = base_pil.copy()
        draw = ImageDraw.Draw(temp_pil, "RGBA") 
        
        # Warna teks utama (dengan Alpha 255 penuh)
        global_text_color = (text_gray_level, text_gray_level, text_gray_level, 255)
        
        for i, item in enumerate(test_items):
            if item["type"] == "text":
                try:
                    font = ImageFont.truetype(item["font"], item["size"])
                except:
                    font = ImageFont.load_default()
                
                # Warna teks: Merah (255, 0, 0, 255) jika diedit, atau abu-abu standar
                color = (255, 0, 0, 255) if i == current_idx else global_text_color
                
                # Jika field bold (mis. NIK) -> outline khusus. NIK harus full black.
                if item.get("is_bold") and nik_bold_alpha > 0 and nik_stroke_width > 0:
                    if item.get("key") == "nik":
                        # NIK dirender pada layer terpisah agar stroke 0.4 px bisa disimulasikan.
                        scale_factor = 4
                        nik_layer = Image.new("RGBA", (base_pil.width * scale_factor, base_pil.height * scale_factor), (0, 0, 0, 0))
                        nik_draw = ImageDraw.Draw(nik_layer, "RGBA")
                        try:
                            scaled_font = ImageFont.truetype(item["font"], item["size"] * scale_factor)
                        except:
                            scaled_font = ImageFont.load_default()
                        nik_draw.text(
                            (item["x"] * scale_factor, item["y"] * scale_factor),
                            item["text"],
                            fill=color,
                            font=scaled_font,
                            anchor=item["anchor"],
                            stroke_width=max(1, int(round(nik_stroke_width * scale_factor))),
                            stroke_fill=(0, 0, 0, 255),
                        )
                        nik_layer_small = nik_layer.resize(base_pil.size, Image.LANCZOS)
                        temp_pil = Image.alpha_composite(temp_pil, nik_layer_small)
                        draw = ImageDraw.Draw(temp_pil, "RGBA")
                    else:
                        # Outline lainnya mengikuti slider alpha dengan warna abu-abu
                        s_width = max(1, int(round(nik_stroke_width)))
                        s_fill = (text_gray_level, text_gray_level, text_gray_level, nik_bold_alpha)
                        draw.text((item["x"], item["y"]), item["text"], fill=color, font=font, anchor=item["anchor"], stroke_width=s_width, stroke_fill=s_fill)
                else:
                    draw.text((item["x"], item["y"]), item["text"], fill=color, font=font, anchor=item["anchor"])
                
            elif item["type"] == "photo":
                x1, y1 = item["x"], item["y"]
                x2, y2 = x1 + item["size"], y1 + item["height"]
                
                if i == current_idx:
                    draw.rectangle([x1, y1, x2, y2], fill=(255, 0, 0, 90), outline="red", width=2)
                else:
                    draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 40), outline="black", width=1)

        # Composite RGBA result over white background for proper display in OpenCV
        display_pil = Image.new("RGB", temp_pil.size, (255, 255, 255))
        display_pil.paste(temp_pil, (0, 0), temp_pil)
        open_cv_image = np.array(display_pil)[:, :, ::-1].copy()
        cv2.imshow(window_name, open_cv_image)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        elif key == 32: 
            current_idx = (current_idx + 1) % len(test_items)
            cv2.setTrackbarPos("Font Size/Lebar", window_name, test_items[current_idx]["size"])
            if test_items[current_idx]["type"] == "photo":
                cv2.setTrackbarPos("Tinggi Foto", window_name, test_items[current_idx]["height"])
            print_status() 
        elif key == ord('c') or key == ord('C'):
            print("\n" + "🔥"*10 + " INJEKSI KE SCRIPT FASE 2 UTAMA " + "🔥"*10)
            item_photo = None
            
            print(f"warna_teks = ({text_gray_level}, {text_gray_level}, {text_gray_level}, 255)")
            print(f"warna_semi_bold = ({text_gray_level}, {text_gray_level}, {text_gray_level}, {nik_bold_alpha})\n")
            
            for item in test_items:
                if item["type"] == "text":
                    if item.get('is_bold'):
                        if item.get('key') == 'nik':
                            bold_param = f', stroke_width={nik_stroke_width:.2f}, stroke_fill=(0, 0, 0, 255)'
                        else:
                            bold_param = f', stroke_width={nik_stroke_width:.2f}, stroke_fill=warna_semi_bold'
                    else:
                        bold_param = ''
                    print(f"write.text(({item['x']},{item['y']}), ..., fill=warna_teks, anchor=\"{item['anchor']}\"{bold_param}) # {item['label']}")
                elif item["type"] == "photo":
                    item_photo = item
            
            if item_photo:
                print(f"\n# ==========================================")
                print(f"# KODE PASTE FOTO FINAL:")
                print(f"# ==========================================")
                print(f"target_w, target_h = {item_photo['size']}, {item_photo['height']}")
                print(f"pas_photo_final = pas_photo.resize((target_w, target_h))")
                print(f"tmp.paste(pas_photo_final, ({item_photo['x']}, {item_photo['y']}))")
            print("🔥"*38 + "\n")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_tuner()