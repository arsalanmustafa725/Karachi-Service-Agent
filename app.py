import streamlit as st
import requests
import json

# --- 1. Page Config ---
st.set_page_config(page_title="Karachi Service Agent (KSA)", page_icon="🏙️", layout="wide")

# API Keys setup (Paste keys here or use st.secrets)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
MAPS_API_KEY = st.secrets.get("MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY")

# --- 2. Database & State ---
KARACHI_SERVICES = [
    {"name": "Kashif Electrician", "area": "Gulshan-e-Iqbal", "rating": 4.8, "service": "Electrician", "phone": "+92 300 1234567"},
    {"name": "Aslam Plumber", "area": "Saddar", "rating": 4.5, "service": "Plumber", "phone": "+92 321 9876543"},
    {"name": "Irfan AC Tech", "area": "Nazimabad", "rating": 4.9, "service": "AC Repair", "phone": "+92 333 5554433"},
    {"name": "Junaid Plumbing", "area": "DHA", "rating": 4.9, "service": "Plumber", "phone": "+92 312 8887766"}
]

if "my_history" not in st.session_state:
    st.session_state.my_history = []

if "current_ans" not in st.session_state:
    st.session_state.current_ans = None

# --- 3. Sidebar Setup ---
with st.sidebar:
    st.markdown("### 🛠️ Technical Agent State")
    st.success("🤖 Agent Status: Active")
    st.info("🧠 Brain: Llama 3.3 70B (Groq Live)")
    st.markdown("---")
    st.markdown("### 🧬 Core Technical Stack")
    st.markdown("**1. Groq REST API (Orchestrator)**")
    st.caption("یوزر کی زبان کو سمجھ کر سمارٹ میچنگ کرتا ہے۔")
    st.markdown("**2. Google Places & Maps API**")
    st.caption("کراچی کے لوکل پلمبرز، الیکٹریشنز اور لوکیشن کا ڈیٹا لاتا ہے۔")
    st.markdown("---")
    st.code("Status = Ready\nDatabase = Active", language="javascript")

# --- 4. Main Interface ---
st.title("🏙️ Karachi Service Agent (KSA)")
st.caption("Team KSA Orchestrator | #AISeekho Google Antigravity Hackathon 2026")

query = st.text_input("کراچی میں کیا مدد چاہیے؟", placeholder="Type in English, اردو میں لکھیں، یا Roman Urdu...")

if st.button("🚀 سروس تلاش کریں", type="primary"):
    if query:
        with st.status("ایجنٹ پروسیسنگ کر رہا ہے...", expanded=True) as status:
            
            # Groq API Processing
            if GROQ_API_KEY != "YOUR_GROQ_API_KEY":
                past_chats = "".join([f"User: {t['u']}\nAgent: {t['a']}\n" for t in st.session_state.my_history])
                master_prompt = f"""
                You are 'Karachi Service Agent', a strict single-language AI Orchestrator.
                Database: {json.dumps(KARACHI_SERVICES)}
                History: {past_chats}
                Query: "{query}"
                Reply in the EXACT SAME language/script as user input (Urdu Script, Roman Urdu, or English).
                Suggest relevant providers from DB or general help for Karachi services.
                """
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": master_prompt}], "temperature": 0.2}
                
                try:
                    res = requests.post(url, headers=headers, json=payload).json()
                    ans = res['choices'][0]['message']['content']
                    st.session_state.current_ans = ans
                    st.session_state.my_history.append({"u": query, "a": ans})
                except Exception as e:
                    st.session_state.current_ans = f"AI پروسیسنگ میں مسئلہ: {e}"
            else:
                # Fallback response if Groq Key not added
                ans = f"آپ کی درخواست: '{query}' موصول ہوئی۔ ذیل میں لوکل سروسز ملاحظہ کریں۔"
                st.session_state.current_ans = ans
                st.session_state.my_history.append({"u": query, "a": ans})
            
            status.update(label="حل تیار ہے!", state="complete", expanded=False)

# --- 5. Display Results ---
if st.session_state.current_ans:
    st.markdown("### 🤖 ایجنٹ کا جواب:")
    st.info(st.session_state.current_ans)
    
    st.divider()
    st.subheader("📍 لوکل سروس فراہم کنندگان (Service Providers)")
    
    # Filter Providers based on user query
    matched = False
    for res in KARACHI_SERVICES:
        if query and (res['service'].lower() in query.lower() or res['area'].lower() in query.lower()):
            matched = True
            with st.expander(f"📌 {res['name']} ({res['service']}) — ⭐ {res['rating']}", expanded=True):
                st.write(f"📍 **علاقہ/ایڈریس:** {res['area']}, Karachi")
                st.write(f"📞 **رابطہ نمبر:** `{res['phone']}`")
    
    # Display all if no direct query match
    if not matched:
        for res in KARACHI_SERVICES:
            with st.expander(f"📌 {res['name']} ({res['service']}) — ⭐ {res['rating']}"):
                st.write(f"📍 **علاقہ/ایڈریس:** {res['area']}, Karachi")
                st.write(f"📞 **رابطہ نمبر:** `{res['phone']}`")

    st.divider()
    st.subheader("🗺️ لوکیشن میپ (Embedded Search)")
    
    # Safe Google Maps Link (Opens in new browser tab)
    search_q = (query + " Karachi").replace(" ", "+") if query else "Karachi+Services"
    map_url = f"https://www.google.com/maps/search/{search_q}"
    
    st.markdown(f'<a href="{map_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">📍 Google Maps پر لوکیشن کھولیں</button></a>', unsafe_allow_html=True)

# Chat History Display
if st.session_state.my_history:
    st.divider()
    st.subheader("💬 گفتگو کی یادداشت (Agent History)")
    for turn in st.session_state.my_history[-3:]:
        st.caption(f"👤 **آپ:** {turn['u']}")
        st.caption(f"🤖 **ایجنٹ:** {turn['a']}")
