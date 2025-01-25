import streamlit as st
from bs4 import BeautifulSoup
import requests
import re

class JewelryPriceCalculator:
    def __init__(self):
        self.product = None
        self.unit = None
        self.weight = 0.0
        self.making_charges = 0
        self.gst = 0
        self.Gold24k = 0
        self.Gold22k = 0
        self.Gold18k = 0
        self.Silvergm = 0
        self.Silverkg = 0
        self.Platinumgm = 0
        self.Platinumkg = 0

# jewellary price scraping
    def scrap(self):
        url=r"https://www.vaibhavjewellers.com/gold-rate"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_elements = soup.find_all("tr")
        for price_element in price_elements:
            if 'INR' in price_element.text:
                match = re.search(r'(\d+\.\d+|\d+)\s*INR', price_element.text)
                if match:
                    value = float(match.group(1))
                    if '24 KT' in price_element.text:
                        self.Gold24k = value
                    elif '22 KT' in price_element.text:
                        self.Gold22k = value
                    elif '18 KT' in price_element.text:
                        self.Gold18k = value
                    elif '100%' in price_element.text:
                        self.Silvergm = value
                        self.Silverkg = self.Silvergm * 1000
                    elif '99.5' in price_element.text:
                        self.Platinumgm = value
                        self.Platinumkg = self.Platinumgm * 1000

# Price Calculator
    def choose_product(self):
        self.product = st.selectbox("Select Product", ["Silver", "Gold", "Platinum"])

    def get_product_icon(self):
        if self.product == 'Gold':
            return 'gold.png'
        elif self.product == 'Silver':
            return 'silver.png'
        elif self.product == 'Platinum':
            return 'platinum.png'

    def choose_unit(self):
        if self.product == "Silver":
            self.unit = st.selectbox("Select Unit for Silver", ["gm", "kg"])
        elif self.product == "Gold":
            self.unit = st.selectbox("Select Type of Gold", ["18K Gold", "22K Gold", "24K Gold"])
        else:
            self.unit = st.selectbox("Select Unit for Platinum", ["gm", "kg"])

    def get_weight(self):
        self.weight = st.number_input(f"Weight ({self.unit})", min_value=0.0)

    def choose_making_charges(self):
        making_charges_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]
        self.making_charges = st.selectbox("Making Charges in %", making_charges_options)

    def choose_gst(self):
        gst_options = [0, 3, 5, 12, 18, 28]
        self.gst = st.selectbox("GST in %", gst_options)

    def product_price(self):
        if self.product == "Silver":
            return self.silver_price()
        elif self.product == "Gold":
            return self.gold_price()
        else:
            return self.platinum_price()

    def silver_price(self):
        return self.Silvergm if self.unit == "gm" else self.Silverkg

    def gold_price(self):
        if self.unit == "18K Gold":
            return self.Gold18k
        elif self.unit == "22K Gold":
            return self.Gold22k
        else:
            return self.Gold24k

    def platinum_price(self):
        return self.Platinumgm if self.unit == "gm" else self.Platinumkg

    def calculate_total_price(self):
        price_per_gram = self.product_price()
        
        # Convert weight to grams if the unit is kg
        weight_in_grams = self.weight * 1000 if self.unit == "kg" else self.weight
        
        # Calculate prices
        total_weight_price = price_per_gram * weight_in_grams
        total_making_charges = total_weight_price * (self.making_charges / 100)
        total_gst = (total_weight_price + total_making_charges) * (self.gst / 100)

        total_price = total_weight_price + total_making_charges + total_gst
        return total_price

# Streamlit UI
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
        text-align: center;
    }
    .highlight {
        color: white;
    }
    .stSelectbox label, .stNumberInput label {
        color: white;
    }
    a {
        color: white;
    }
    .stButton>button {
        background-color: white;
        color: black;
    }
    .separator {
        border-top: 2px solid white;
        margin: 05px 0; /* Adjust this value to control spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.image("image2.jpg")
#st.header("Jewelry Price Calculator")

calculator = JewelryPriceCalculator()
calculator.scrap()
calculator.choose_product()
# Display the product icon
product_icon = calculator.get_product_icon()
if product_icon:
    st.image(product_icon, width=50)

calculator.choose_unit()
calculator.get_weight()
calculator.choose_making_charges()
calculator.choose_gst()

st.write(f"Today Price per {calculator.unit}: {calculator.product_price()}")

if st.button("Calculate Total Price"):
    total_price = calculator.calculate_total_price()
    st.write(f"Total Price is: {total_price:.2f}")
st.markdown("---")
st.header("Note")

st.write("Calculates the price of Gold, Silver, and Platinum Jewellery based on the current market price.")
st.write("To stay updated with the latest market prices, the app retrieves the current prices directly from [Vaibhav Jewellers](https://www.vaibhavjewellers.com/gold-rate).")

st.markdown("___")
st.write("Created & Published by © 2025 [Nishant]()")
st.write("[Linkdin](https://www.linkedin.com/in/nishant-kumar-data-analyst/) | [Github](https://github.com/Nishant6020) | [Portfolio](https://www.datascienceportfol.io/nishant575051)")