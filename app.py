import streamlit as st
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import tempfile

st.set_page_config(page_title="Proposal Generator", layout="centered")

st.title("📄 Company Registration Proposal Maker")

# 🔹 Consultant Inputs
consultant_name = st.text_input("Startup Consultant Name")
consultant_mobile = st.text_input("Mobile Number")
consultant_email = st.text_input("Email ID")

# 🔹 Inputs
client_name = st.text_input("Client Name")

company_type = st.selectbox("Company Type", [
    "Private Limited", "LLP", "Section 8", "OPC", "Public Limited"
])

states = [
    "Bihar","Chandigarh","Delhi","Andhra Pradesh","Assam","Chhattisgarh",
    "Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Gujarat",
    "Madhya Pradesh","Maharashtra","Odisha","Punjab","Rajasthan",
    "Jammu & Kashmir","Uttarakhand","Uttar Pradesh","Tamil Nadu",
    "Andaman & Nicobar","Mizoram","Sikkim","Puducherry","Ladakh",
    "Nagaland","Daman & Diu","Lakshadweep","Meghalaya","Tripura",
    "Arunachal Pradesh","West Bengal","Dadra & Nagar Haveli"
]

state = st.selectbox("State", states)

dsc_count = st.number_input("No. of DSC", min_value=0, value=2, step=1)
compliance = st.selectbox("Compliance Commitment?", ["Yes", "No"])


# 🔹 Stamp Duty
def get_stamp_duty(state):
    mapping = {
        "Bihar":1520,"Chandigarh":1503,"Delhi":360,"Andhra Pradesh":1520,
        "Assam":525,"Chhattisgarh":1510,"Haryana":135,"Himachal Pradesh":123,
        "Jharkhand":173,"Karnataka":10020,"Kerala":3025,"Gujarat":620,
        "Madhya Pradesh":7550,"Maharashtra":1300,"Odisha":610,"Punjab":10025,
        "Rajasthan":5510,"Jammu & Kashmir":310,"Uttarakhand":1010,
        "Uttar Pradesh":1010,"Tamil Nadu":520,"Andaman & Nicobar":520,
        "Mizoram":260,"Sikkim":143,"Puducherry":510,"Ladakh":143,
        "Nagaland":260,"Daman & Diu":1170,"Lakshadweep":1525,
        "Meghalaya":410,"Tripura":260,"Arunachal Pradesh":710,
        "West Bengal":370,"Dadra & Nagar Haveli":184
    }
    return mapping.get(state, 1000)


# 🔹 Cost Calculation
def calculate_cost():
    run_fee = 1000 if company_type == "LLP" else 2000
    dsc_cost = dsc_count * 2000

    if company_type == "Section 8":
        prof_fee = 3500
    elif company_type == "Public Limited":
        prof_fee = 5000
    else:
        prof_fee = 2000 if compliance == "Yes" else 5000

    if company_type == "LLP":
        stamp = 500
        label = "FiLLiP Fee (LLP Filing)"
    else:
        stamp = get_stamp_duty(state)
        label = f"Stamp Duty (of {state})"

    subtotal_base = run_fee + dsc_cost + stamp
    subtotal = subtotal_base + prof_fee
    gst = subtotal * 0.18
    total = subtotal + gst

    return run_fee, dsc_cost, prof_fee, stamp, label, subtotal_base, subtotal, gst, total


# 🔹 Letterhead
def first_page(canvas, doc):
    canvas.drawImage("letterhead.png", 0, 0, width=595, height=842)

def later_pages(canvas, doc):
    pass


# 🔹 PDF Generator
def generate_pdf():
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        file.name,
        pagesize=A4,
        topMargin=110,
        bottomMargin=70,
        leftMargin=50,
        rightMargin=50
    )

    styles = getSampleStyleSheet()
    heading = styles["Heading2"]
    normal = styles["Normal"]

    run_fee, dsc_cost, prof_fee, stamp, label, subtotal_base, subtotal, gst, total = calculate_cost()

    story = []

    # 🔹 Opening
    story.append(Paragraph(f"<b>Dear {client_name} Ji,</b>", normal))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "As per our telephonic conversation regarding your inquiry, "
        "<b>we are pleased to share our Company registration proposal with you.</b>",
        normal
    ))
    story.append(Spacer(1, 10))

    # 🔹 Client Table
    client_data = [
        ["Client Name", client_name],
        ["Company Type", company_type],
        ["State", state],
        ["Date", datetime.now().strftime("%d %B %Y")]
    ]

    table = Table(client_data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), "#D9EAF7"),
        ("GRID", (0,0), (-1,-1), 1, "#A6A6A6"),
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    # 🔹 Scope
    story.append(Paragraph("<b>Scope of Services:</b>", heading))

    scope = [
        "Name Approval (RUN-Filing once)",
        "Company Incorporation Certificate (COI)",
        "Article of Association (AOA)",
        "Memorandum of Association (MOA)",
        "Company PAN & TAN Registration",
        "Bank Account Opening Support (BR)"
    ]

    if dsc_count > 0:
        scope.insert(4, f"{dsc_count} Directors – Digital Signature Certificate (Class-3)")
        scope.insert(5, f"{dsc_count} Directors – Director Identification Number (DIN)")

    if company_type != "LLP":
        scope.append("PF Registration")
        scope.append("ESIC Registration")

    for s in scope:
        story.append(Paragraph(f"• {s}", normal))

    story.append(Spacer(1, 10))

    # 🔹 Complimentary
    story.append(Paragraph("<b>Complimentary Services:</b>", heading))
    story.append(Paragraph("<font color='green'><b>• MSME Registration (Complimentary)</b></font>", normal))
    story.append(Paragraph("<font color='green'><b>• GST Application Filing (Complimentary)</b></font>", normal))

    story.append(Spacer(1, 10))

    # 🔹 Documents
    story.append(Paragraph("<b>Required Documents for Company Registration:</b>", heading))

    docs = [
        "At least 2 Proposed Company Names",
        "Nature of Business",
        "Aadhar Card & PAN Card of All Directors",
        "Contact Number & Email ID of All Directors",
        "Passport Size Photograph of All Directors",
        "Business Premises Photos (Inside & Outside)",
        "Latest Bank Statement (with Name & Address)",
        "Latest Electricity Bill (Office Address Proof)",
        "Rent Agreement (if rented) along with Owner PAN & Contact Details"
    ]

    for d in docs:
        story.append(Paragraph(f"• {d}", normal))

    # 🔹 Page Break
    story.append(PageBreak())

    # 🔹 Pricing Table
    story.append(Paragraph("<b>Pricing Breakdown (Standard Authorised Capital of Rs 1.0 Lakh)</b>", heading))
    story.append(Spacer(1, 8))

    pricing = [
        ["Particulars","Amount (INR)"],
        ["RUN Fee",f"INR {run_fee}"]
    ]

    if dsc_count > 0:
        pricing.append([f"DSC Cost ({dsc_count} nos.)", f"INR {dsc_cost}"])

    pricing.extend([
        [label, f"INR {stamp}"],
        ["Subtotal",f"INR {subtotal_base}"],
        ["Professional Fees",f"INR {prof_fee}"],
        ["GST (18%)",f"INR {int(gst)}"],
        ["TOTAL",f"INR {int(total)}"]
    ])

    subtotal_index = 3 if dsc_count > 0 else 2

    ptable = Table(pricing, colWidths=[250,150])
    ptable.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),"#0B5394"),
        ("TEXTCOLOR",(0,0),(-1,0),"white"),
        ("GRID",(0,0),(-1,-1),1,"#A6A6A6"),
        ("BACKGROUND",(0,subtotal_index),(-1,subtotal_index),"#D9EAF7"),
        ("FONTNAME",(0,subtotal_index),(-1,subtotal_index),"Helvetica-Bold"),
        ("BACKGROUND",(0,-1),(-1,-1),"#0B5394"),
        ("TEXTCOLOR",(0,-1),(-1,-1),"white"),
    ]))

    story.append(ptable)

    # 🔹 Timeline
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Process Timelines:</b>", heading))

    timeline = [
        ["Step","Process","Time"],
        ["1","Name Approval(Run Filing)","7-8 days"],
        ["2","DSC Creation","3-4 days"],
        ["3","MOA & AOA Drafting","2-3 days"],
        ["4","Incorporation Filing (Spice+)","3-4 days"],
        ["5","COI Issuance+ DIN/PAN/TAN/CIN Allocation","8-10 days"],
        ["","Total","30 days"]
    ]

    ttable = Table(timeline, colWidths=[60,220,120])
    ttable.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),"#2E8B57"),
        ("TEXTCOLOR",(0,0),(-1,0),"white"),
        ("GRID",(0,0),(-1,-1),1,"#A6A6A6"),
        ("BACKGROUND",(0,-1),(-1,-1),"#F57C00"),
        ("TEXTCOLOR",(0,-1),(-1,-1),"white"),
    ]))

    story.append(ttable)

    # 🔹 Note
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Note:</b>", normal))
    story.append(Paragraph("TAT is on an approximate basis and depends on MCA approvals.", normal))

    # 🔹 Important Notes
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Important Notes:</b>", heading))
    story.append(Paragraph("• Payment must be cleared after RUN approval.", normal))
    story.append(Paragraph("• RUN does not guarantee name approval. Re-application will be charged separately.", normal))
    
    # 🔹 Closing
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Warm Regards,</b>", normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>{consultant_name}</b>", normal))
    story.append(Paragraph("Startup Consultant", normal))
    story.append(Paragraph(f"Mobile: {consultant_mobile}", normal))
    story.append(Paragraph(f"Email: {consultant_email}", normal))

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)

    return file.name


# 🔹 Button
if st.button("Generate Proposal"):
    pdf = generate_pdf()
    with open(pdf, "rb") as f:
        st.download_button("Download Proposal", f, file_name="proposal.pdf")