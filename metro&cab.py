import streamlit as st
import qrcode
from io import BytesIO
import uuid

# QR generation function
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

st.title("RIDE BOOKING")

stations = [
    "Hitech-city", "BalaNagar", "Kukkatpally", "KPHB",
    "JNTU", "Miyapur", "Panjagutta", "Ameerpet", "SRNagar"
]

name = st.text_input("Passenger Name")
source = st.selectbox("From Station", stations)
destination = st.selectbox("To Station", stations)

no_tickets = st.number_input("Tickets", min_value=1, max_value=10, value=1)
price_per_ticket = 30
total_amount = no_tickets * price_per_ticket

st.info(f"Total amount is ₹{total_amount}")

st.subheader("Do you need a cab?")
need_cab = st.radio("", ["NO", "YES"])

cab_loc_info = ""
if need_cab == "YES":
    cab_loc_info = st.text_input("Enter Drop Location")

if st.button("Book Ride"):
    if name.strip() == "":
        st.error("Please enter passenger name.")
    elif source == destination:
        st.error("Source and Destination cannot be the same.")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Amount: {total_amount}\n"
            f"Cab Drop: {cab_loc_info if cab_loc_info else 'No Cab'}"
        )

        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")

        st.success(" Ticket Booked Successfully!")
        st.write(f"**Booking ID:** {booking_id}")
        st.write(f"**Passenger:** {name}")
        st.write(f"**From:** {source}")
        st.write(f"**To:** {destination}")
        st.write(f"**Tickets:** {no_tickets}")
        st.write(f"**Amount Paid:** ₹{total_amount}")

        if cab_loc_info:
            st.write(f"**Cab Drop Location:** {cab_loc_info}")

        st.image(buf.getvalue(), width=250)
