
import streamlit as st
import pandas as pd
from io import BytesIO

def generate_pricing_table(product_name, base_price, quantity, years, increase_rate):
    data = []
    for year in range(1, years + 1):
        unit_price = base_price * ((1 + increase_rate / 100) ** (year - 1))
        total_price = unit_price * quantity
        data.append({
            "Product Name": product_name,
            "Year": year,
            "Unit Price": round(unit_price, 2),
            "Quantity": quantity,
            "Total Price": round(total_price, 2)
        })
    return pd.DataFrame(data)

st.title("Multi-Year Pricing Table Generator")

product_name = st.text_input("Product Name")
base_price = st.number_input("Base Price", min_value=0.0, value=100.0)
quantity = st.number_input("Quantity", min_value=1, value=10)
years = st.selectbox("Number of Years", [3, 5])
increase_rate = st.number_input("Annual Increase Rate (%)", min_value=0.0, value=5.0)

if st.button("Generate Pricing Table"):
    df = generate_pricing_table(product_name, base_price, quantity, years, increase_rate)
    st.dataframe(df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Pricing')
    output.seek(0)

    st.download_button(
        label="Download Excel File",
        data=output,
        file_name="pricing_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
