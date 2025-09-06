import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bayad mo BOI", layout="centered")

st.title("💸 BAYAD COURT BOI 💸")

# Total Contribution
total_amount = st.number_input("Enter the total amount needed (₱):", min_value=0, step=10, format="%d")

# Number of People
num_people = st.number_input("How many people will contribute?", min_value=1, step=1, format="%d")

# 🔹 Downpayment Section
st.subheader("💰 Downpayment Section")

downpayment_total = st.number_input("Enter total downpayment amount (₱):", min_value=0, step=10, format="%d")
down_contributors = st.number_input("How many people paid the downpayment?", min_value=0, step=1, format="%d")

downpayers = []
for i in range(int(down_contributors)):
    col1, col2 = st.columns([2, 1])
    with col1:
        d_name = st.text_input(f"Downpayer {i+1} Name", key=f"d_name_{i}")
    with col2:
        d_paid = st.number_input("Paid (₱)", min_value=0, step=10, format="%d", key=f"d_paid_{i}")

    if not d_name:
        d_name = f"Downpayer {i+1}"
    downpayers.append([d_name, d_paid])

# 🔹 Contribution Splitting Section
contributors = []
if total_amount > 0 and num_people > 0:
    st.subheader("✍ Enter Names and Additional Payments")

    # Ideal share for each person
    ideal_share = total_amount // num_people  # no decimals
    st.write(f"Each person should ideally contribute: **₱{ideal_share:,}**")

    for i in range(int(num_people)):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Kupal {i+1}", key=f"name_{i}")
        with col2:
            paid = st.number_input("Paid (₱)", min_value=0, step=10, format="%d", key=f"paid_{i}")

        if not name:
            name = f"Kopal {i+1}"

        contributors.append([name, paid])

    # 🔹 Merge Downpayment + Contributors
    results = []
    down_dict = {d[0]: d[1] for d in downpayers}  # convert list to dict

    for name, paid in contributors:
        total_paid = paid + down_dict.get(name, 0)  
        balance = ideal_share - total_paid

        if balance > 0:
            status = f"🔴 Under: -{balance}"
        elif balance < 0:
            status = f"🟡 Over: +{abs(balance)}"
        else:
            status = "🟢 Fully Paid"

        results.append([name, total_paid, status])

    # 🔹 Display Table
    st.subheader("📊 Contribution Summary")
    df = pd.DataFrame(results, columns=["Name", "Total Paid (₱)", "Status"])
    st.table(df)

    # 🔹 Total Collected vs Needed
    total_collected = df["Total Paid (₱)"].sum()
    st.info(f"💵 Total Collected: ₱{total_collected:,} / ₱{total_amount:,}")

    if total_collected < total_amount:
        st.warning(f"⚠ Still short of ₱{total_amount - total_collected:,}")
    elif total_collected > total_amount:
        st.success(f"🎉 Overfunded by ₱{total_collected - total_amount:,}")
    else:
        st.success("✅ Target reached exactly!")
