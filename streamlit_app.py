import streamlit as st
import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8080")

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
    return None

def main():
    st.set_page_config(page_title="Retail Catalog", layout="wide")

    # Initialize navigation session state
    if "view" not in st.session_state:
        st.session_state.view = "list"
    if "selected_product_id" not in st.session_state:
        st.session_state.selected_product_id = None

    # --- LIST VIEW ---
    if st.session_state.view == "list":
        st.title("Retail Catalog - Product List")
        
        # Sidebar for filtering
        st.sidebar.header("Filters")
        categories = fetch_data("categories")
        selected_category = st.sidebar.selectbox("Category", ["All"] + (categories if categories else []))

        # Fetch limited inventory
        params = {"category": selected_category}
        products = fetch_data("inventory", params=params)

        if products:
            # Display stats
            st.write(f"Showing **{len(products)}** products")
            
            # 5xX grid
            cols = st.columns(5)
            for idx, product in enumerate(products):
                with cols[idx % 5]:
                    st.image(product.get("link", ""), use_container_width=True)
                    st.write(f"**{product.get('title', 'No Title')}**")
                    st.write(f"₹{product.get('price', 0)}")
                    if st.button("View Details", key=product["_id"]):
                        st.session_state.selected_product_id = product["_id"]
                        st.session_state.view = "detail"
                        st.rerun()

    # --- DETAIL VIEW ---
    elif st.session_state.view == "detail":
        product_id = st.session_state.selected_product_id
        product = fetch_data(f"product/{product_id}")

        if product:
            if st.button("⬅️ Back to List"):
                st.session_state.view = "list"
                st.rerun()

            st.title(f"📦 Product Detail: {product.get('title', 'No Title')}")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(product.get("link", ""), use_container_width=True)
                st.metric("Price", f"₹{product.get('price', 0)}")
                if "discountedPrice" in product:
                    st.write(f"**Discounted Price:** ₹{product['discountedPrice']}")
                st.write(f"**Category:** {product.get('masterCategory', 'N/A')}")
                st.write(f"**Sub Category:** {product.get('subCategory', 'N/A')}")
                st.write(f"**Brand:** {product.get('brandName', 'N/A')}")
                st.write(f"**Gender:** {product.get('gender', 'N/A')}")

            with col2:
                st.subheader("Description / Attributes")
                if 'productDisplayName' in product:
                    st.write(f"**Display Name:** {product['productDisplayName']}")
                st.write(f"**Base Colour:** {product.get('baseColour', 'N/A')}")
                st.write(f"**Season:** {product.get('season', 'N/A')}")
                st.write(f"**Article Type:** {product.get('articleType', 'N/A')}")
                
                st.divider()
                st.write("### Full Technical Details")
                st.json(product)
        else:
            st.error("Product not found.")
            if st.button("Back to List"):
                st.session_state.view = "list"
                st.rerun()

if __name__ == "__main__":
    main()
