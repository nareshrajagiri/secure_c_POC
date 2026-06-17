import fitz

pdf = fitz.open("cert_c.pdf")

print("Pages:", len(pdf))

for i in range(20, 40):
    page = pdf[i]
    text = page.get_text()

    if "PRE30-C" in text:
        print(text[:5000])
        break