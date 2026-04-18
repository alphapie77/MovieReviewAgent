import streamlit as st

st.title("Test Example Buttons")

# Examples
examples = {
    "Romantic": "একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক বাধা পেরিয়ে মিলিত হয়।",
    "Thriller": "শহরটার নাম নীলপুর। শান্ত শহরে হঠাৎ রহস্যজনক ঘটনা ঘটতে শুরু করে।",
    "Action": "একজন সাধারণ মানুষ যখন তার পরিবারকে বাঁচাতে গিয়ে অপরাধীদের বিরুদ্ধে লড়াই করে।"
}

# Initialize
if 'test_plot' not in st.session_state:
    st.session_state.test_plot = ""

st.write("Current value in session state:", st.session_state.test_plot[:50] if st.session_state.test_plot else "Empty")

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Romantic", key="test_rom"):
        st.session_state.test_plot = examples["Romantic"]
        st.write("✓ Romantic clicked!")
        st.rerun()

with col2:
    if st.button("Thriller", key="test_thr"):
        st.session_state.test_plot = examples["Thriller"]
        st.write("✓ Thriller clicked!")
        st.rerun()

with col3:
    if st.button("Action", key="test_act"):
        st.session_state.test_plot = examples["Action"]
        st.write("✓ Action clicked!")
        st.rerun()

# Text area
plot = st.text_area(
    "Plot",
    value=st.session_state.test_plot,
    height=150,
    key="test_textarea"
)

# Sync back
if plot != st.session_state.test_plot:
    st.session_state.test_plot = plot

st.write("---")
st.write("Debug - Session state value:", st.session_state.test_plot[:100] if st.session_state.test_plot else "Empty")
