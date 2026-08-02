import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Karachi Service Agent (KSA)", page_icon="🛠️", layout="wide")

st.title("🏙️ Karachi Service Agent (KSA)")
st.caption("Team KSA Orchestrator | #AISeekho Google Antigravity Hackathon 2026")

st.markdown("""
کراچی میں اپنے قریب ترین **پلمبر، الیکٹریشن، میمکینک** اور دیگر ماہرین تلاش کریں۔ 
نیچے دی گئی سروس منتخب کریں یا اپنی ضرورت ٹائپ کریں۔
""")

# Google Places API Key Setup
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY" # اپنا گوگل میپس API کی یہاں درج کریں

# Service Selection UI
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("سروس تلاش کریں (مثال: Plumber, Electrician, Carpenter)", placeholder="مثال: Electrician in Gulshan-e-Iqbal")

with col2:
    selected_category = st.selectbox("یا کیٹیگری منتخب کریں:", [
        "کوئی نہیں",
        "Electrician (الیکٹریشن)",
        "Plumber (پلمبر)",
        "AC Mechanic (اے سی مکینک)",
        "Home Cleaner (صفائی ستھرائی)",
        "Car Mechanic (گاڑی کا مکینک)"
    ])

# Determine final search prompt
final_search = ""
if search_query:
    final_search = f"{search_query} Karachi"
elif selected_category != "کوئی نہیں":
    service_name = selected_category.split(" (")[0]
    final_search = f"{service_name} in Karachi"

# Search Function using Google Places API
def fetch_karachi_services(query):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

# Fetch Details (Phone Number) for a specific place
def fetch_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,international_phone_number,website&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result', {})
    return {}

# Action Button
if st.button("🔍 سروس تلاش کریں", type="primary"):
    if not final_search:
        st.warning("برائے مہربانی سروس کا نام درج کریں یا کیٹیگری منتخب کریں۔")
    else:
        st.info(f"کراچی میں **'{final_search}'** کے نتائج تلاش کیے جا رہے ہیں...")
        
        # NOTE: If API_KEY is not configured yet, showing a clean Demo View
        if API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
            st.error("⚠️ Google Maps API Key شامل نہیں کی گئی۔ فل حال ڈیمو ڈیٹا دکھایا جا رہا ہے:")
            
            # Dummy Data to show concept
            mock_results = [
                {"name": "Karachi Expert Electrician", "formatted_address": "Block 13, Gulshan-e-Iqbal, Karachi", "rating": 4.8, "phone": "+92 300 1234567"},
                {"name": "Ali Plumber & Sanitary Store", "formatted_address": "DHA Phase 2, Karachi", "rating": 4.5, "phone": "+92 321 9876543"},
                {"name": "Master AC & Home Services", "formatted_address": "PECHS Block 2, Karachi", "rating": 4.7, "phone": "+92 333 5554433"}
            ]
            
            for res in mock_results:
                with st.expander(f"📌 {res['name']} — ⭐ {res['rating']}"):
                    st.write(f"📍 **ایڈریس:** {res['formatted_address']}")
                    st.write(f"📞 **فون نمبر:** `{res['phone']}`")
                    st.markdown(f"[📲 کال کریں / رابطہ کریں](tel:{res['phone']})")
        else:
            # Real Google Maps API Results
            results = fetch_karachi_services(final_search)
            if results:
                for place in results[:10]:
                    name = place.get('name')
                    address = place.get('formatted_address', 'Address not available')
                    rating = place.get('rating', 'N/A')
                    place_id = place.get('place_id')
                    
                    details = fetch_place_details(place_id)
                    phone = details.get('formatted_phone_number', 'فون نمبر دستیاب نہیں')
                    
                    with st.expander(f"📌 {name} — ⭐ {rating}"):
                        st.write(f"📍 **ایڈریس:** {address}")
                        st.write(f"📞 **رابطہ نمبر:** `{phone}`")
                        if phone != 'فون نمبر دستیاب نہیں':
                            st.markdown(f"[📲 براہِ راست کال کریں](tel:{phone})")
            else:
                st.error("کوئی نتائج نہیں ملے۔ برائے مہربانی دوبارہ کوشش کریں۔")
