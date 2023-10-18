import requests
from pypdf import PdfMerger;
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
import json
from barcode import Code39
from barcode.writer import ImageWriter

IP = "192.168.10.102"
PORT = 5000

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def getUserList():
    res = requests.get(f"http://{IP}:{PORT}/manage/all-users")
    parsedRequest = json.loads(res.text)

    return parsedRequest['payload']

def getShiftTime(number):
    number = str(number)
    group = number[-1]

    shift_time = "SEE MANAGEMENT"
    
    match group:
        case "A":
            shift_time = "6:00 AM-1 AM"
        case "B":
            shift_time = "8:30 AM-1 AM"
        case "C":
            shift_time = "9:30 AM-1 AM"
        case "D":
            shift_time = "9:45 AM-1 AM"
        case "E":
            shift_time = "10:00 AM-1 AM"
        case "F":
            shift_time = "10:30 AM-1 AM"
        case "G":
            shift_time = "12:30 PM-1 AM"
        case "H":
            shift_time = "1 PM-1 AM"
        case "I":
            shift_time = "7 AM-1 AM"

    return shift_time

def createPdfPage(user):
    # Page size is 612 x 792
    c = canvas.Canvas(f"./Management/allPDFs/{user['number']}.pdf", pagesize=letter)
    w, h = letter

    c.drawString(50, 700, f"{user['name']}")
    c.drawString(50, 680, f"ID: {user['number']}")

    # Figure out shift
    shift_time = getShiftTime(user['number'])
    c.drawString(50, 660, f"Shift Time: {shift_time}")

    # Generate Barcode
    generateBarcode(user)
    image = ImageReader(f"./Management/allCodes/{user['number']}.png")

    c.drawImage(image, 50, h - 240, height=100, width=200)

    # Add Logo
    logo = ImageReader(f"./TNT Logo Color Horizontal.png")
    c.drawImage(logo, 50, h - 340, height=75, width=200, mask=[0, 0, 0, 0, 0, 0])

    c.save()

def generateBarcode(user):
    number = user['number']

    with open(f"./Management/allCodes/{user['number']}.png", "wb") as f:
        Code39(str(number), writer=ImageWriter(), add_checksum=False).write(f)

def mergeAllPdfs():
    x = [a for a in os.listdir("./management/allPDFs") if a.endswith(".pdf")]

    merger = PdfMerger()

    for pdf in x:
        merger.append(open(f"./management/allPDFs/{pdf}", 'rb'))

    with open("combinedIds.pdf", "wb") as fout:
        merger.write(fout)

if __name__ == "__main__":
    clear()

    user_list = getUserList()

    for user in user_list:
        createPdfPage(user)

    mergeAllPdfs()

