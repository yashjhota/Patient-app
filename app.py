import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Patient Management", page_icon="🏥", layout="centered")
st.title("🏥 Patient Management System")

menu = ["Home", "View All Patients", "View Patient by ID", "Create Patient", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------ Home ------------------
if choice == "Home":
    st.write("Welcome to the **Patient Management System** Streamlit Frontend!")
    st.info("Use the sidebar to navigate between options.")

# ------------------ View All Patients ------------------
elif choice == "View All Patients":
    res = requests.get(f"{BASE_URL}/view")
    if res.status_code == 200:
        data = res.json()
        if data:
            st.subheader("All Patients")
            for pid, patient in data.items():
                st.json({pid: patient})
        else:
            st.warning("No patient records found!")
    else:
        st.error("Failed to fetch patient data")

# ------------------ View Patient by ID ------------------
elif choice == "View Patient by ID":
    patient_id = st.text_input("Enter Patient ID (e.g., P001)")
    if st.button("Search"):
        res = requests.get(f"{BASE_URL}/patient/{patient_id}")
        if res.status_code == 200:
            st.subheader("Patient Details")
            st.json(res.json())
        else:
            st.error("Patient not found!")

# ------------------ Create Patient ------------------
elif choice == "Create Patient":
    st.subheader("Create New Patient")

    patient_id = st.text_input("ID (e.g., P001)")
    name = st.text_input("Name")
    city = st.text_input("City")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["male", "female", "others"])
    height = st.number_input("Height (in meters)", min_value=0.1, format="%.2f")
    weight = st.number_input("Weight (in kgs)", min_value=0.1, format="%.2f")

    if st.button("Create Patient"):
        data = {
            "id": patient_id,
            "name": name,
            "city": city,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight
        }
        res = requests.post(f"{BASE_URL}/create", json=data)
        if res.status_code == 201:
            st.success("✅ Patient created successfully!")
        else:
            st.error(res.json().get("detail", "Error creating patient"))

# ------------------ Update Patient ------------------
elif choice == "Update Patient":
    st.subheader("Update Patient Details")

    patient_id = st.text_input("Enter Patient ID to Update")
    name = st.text_input("New Name (optional)")
    city = st.text_input("New City (optional)")
    age = st.number_input("New Age (optional)", min_value=0, max_value=120, step=1)
    gender = st.selectbox("New Gender (optional)", ["", "male", "female", "others"])
    height = st.number_input("New Height (optional)", min_value=0.0, step=0.01, format="%.2f")
    weight = st.number_input("New Weight (optional)", min_value=0.0, step=0.01, format="%.2f")

    if st.button("Update Patient"):
        update_data = {}
        if name: update_data["name"] = name
        if city: update_data["city"] = city
        if age > 0: update_data["age"] = age
        if gender: update_data["gender"] = gender
        if height > 0: update_data["height"] = height
        if weight > 0: update_data["weight"] = weight

        res = requests.put(f"{BASE_URL}/edit/{patient_id}", json=update_data)
        if res.status_code == 200:
            st.success("✅ Patient updated successfully!")
        else:
            st.error(res.json().get("detail", "Error updating patient"))

# ------------------ Delete Patient ------------------
elif choice == "Delete Patient":
    st.subheader("Delete Patient")
    patient_id = st.text_input("Enter Patient ID to Delete")
    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/delete/{patient_id}")
        if res.status_code == 200:
            st.success("🗑️ Patient deleted successfully!")
        else:
            st.error("Patient not found!")
