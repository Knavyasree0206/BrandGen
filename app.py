"""
app.py
BrandCraft: Generative AI-Powered Branding Automation System
Streamlit Frontend with Image Generation
"""

import streamlit as st
from branding_assistant import BrandingAssistant
from PIL import Image, ImageDraw, ImageFont
import io
import random
import math

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="BrandCraft AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== LOGO IMAGE GENERATOR ENGINE ====================
class LogoImageGenerator:
    """
    Generates logo images programmatically using Pillow.
    No external GPU or paid API required.
    """
    
    def __init__(self):
        # Try to load a font, fallback to default if not found
        try:
            self.font_large = ImageFont.truetype("arial.ttf", 80)
            self.font_medium = ImageFont.truetype("arial.ttf", 40)
            self.font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()

    def _parse_color(self, color_str):
        """Convert string color name to hex or return hex"""
        colors = {
            "red": "#E94560", "blue": "#0F4C75", "green": "#2D6A4F",
            "yellow": "#FCA311", "purple": "#7B2CBF", "orange": "#FF6B35",
            "black": "#1A1A2E", "white": "#FFFFFF", "gray": "#4A4A4A",
            "teal": "#2A9D8F", "pink": "#FF4D6D", "gold": "#D4AF37"
        }
        return colors.get(color_str.lower(), color_str if color_str.startswith("#") else "#333333")

    def _get_color_palette(self, primary_color):
        """Generate a complementary palette"""
        # Simple complementary logic
        return {
            "primary": primary_color,
            "secondary": "#1A1A2E",  # Dark background
            "accent": "#FFFFFF"      # White text
        }

    def generate_minimalist(self, brand_name, colors, size=(500, 500)):
        """Minimalist style logo"""
        img = Image.new('RGB', size, color=colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Draw a simple circle or ring
        center_x, center_y = size[0] // 2, size[1] // 2 - 50
        radius = 100
        
        # Draw ring
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=colors['primary'], width=8
        )
        
        # Draw brand initial in center
        initial = brand_name[0].upper() if brand_name else "B"
        bbox = draw.textbbox((0, 0), initial, font=self.font_large)
        text_w = bbox[2] - bbox[0]
        draw.text((center_x - text_w//2, center_y - 50), initial, fill=colors['accent'], font=self.font_large)
        
        # Draw brand name below
        name_bbox = draw.textbbox((0, 0), brand_name, font=self.font_medium)
        name_w = name_bbox[2] - name_bbox[0]
        draw.text((center_x - name_w//2, center_y + 100), brand_name, fill=colors['primary'], font=self.font_medium)
        
        return img

    def generate_geometric(self, brand_name, colors, size=(500, 500)):
        """Geometric style logo"""
        img = Image.new('RGB', size, color=colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = size[0] // 2, size[1] // 2 - 50
        
        # Draw geometric shapes (Triangle, Square, Circle overlay)
        # Triangle
        tri_points = [
            (center_x, center_y - 100),
            (center_x - 100, center_y + 50),
            (center_x + 100, center_y + 50)
        ]
        draw.polygon(tri_points, outline=colors['primary'], width=5)
        
        # Square
        draw.rectangle(
            [center_x - 50, center_y - 50, center_x + 50, center_y + 50],
            outline=colors['accent'], width=3
        )
        
        # Text
        name_bbox = draw.textbbox((0, 0), brand_name, font=self.font_medium)
        name_w = name_bbox[2] - name_bbox[0]
        draw.text((center_x - name_w//2, center_y + 120), brand_name, fill=colors['accent'], font=self.font_medium)
        
        return img

    def generate_abstract(self, brand_name, colors, size=(500, 500)):
        """Abstract style logo with lines"""
        img = Image.new('RGB', size, color=colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = size[0] // 2, size[1] // 2 - 50
        
        # Draw random abstract lines
        for i in range(5):
            offset = i * 15
            draw.arc(
                [center_x - 80 - offset, center_y - 80 - offset, 
                 center_x + 80 + offset, center_y + 80 + offset],
                start=0, end=180 + i*20, fill=colors['primary'], width=4
            )
            
        # Text
        name_bbox = draw.textbbox((0, 0), brand_name, font=self.font_medium)
        name_w = name_bbox[2] - name_bbox[0]
        draw.text((center_x - name_w//2, center_y + 120), brand_name, fill=colors['accent'], font=self.font_medium)
        
        return img

    def generate_wordmark(self, brand_name, colors, size=(500, 500)):
        """Text-based logo"""
        img = Image.new('RGB', size, color=colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Draw large brand name
        bbox = draw.textbbox((0, 0), brand_name, font=self.font_large)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        center_x = (size[0] - text_w) // 2
        center_y = (size[1] - text_h) // 2
        
        # Draw decorative line
        draw.line([(center_x, center_y + text_h + 10), (center_x + text_w, center_y + text_h + 10)], 
                  fill=colors['primary'], width=5)
        
        draw.text((center_x, center_y), brand_name, fill=colors['accent'], font=self.font_large)
        
        return img

    def generate_logo(self, brand_name, style, color_name):
        """Main generator function"""
        primary_color = self._parse_color(color_name)
        colors = self._get_color_palette(primary_color)
        
        style = style.lower()
        
        if "minimalist" in style:
            return self.generate_minimalist(brand_name, colors)
        elif "geometric" in style:
            return self.generate_geometric(brand_name, colors)
        elif "abstract" in style:
            return self.generate_abstract(brand_name, colors)
        else:
            return self.generate_wordmark(brand_name, colors)

# Initialize Image Generator
img_gen = LogoImageGenerator()

# ==================== CUSTOM STYLING ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%);
        color: #f5f5f5;
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 20, 0.95);
        border-right: 1px solid #2a2a4a;
    }
    h1, h2, h3 { color: #f5f5f5 !important; }
    .main-title {
        font-size: 3rem; font-weight: 800;
        background: linear-gradient(135deg, #e94560, #ff6b35, #f7931e);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(22, 22, 42, 0.6); border: 1px solid #2a2a4a;
        border-radius: 10px; padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #e94560 0%, #ff6b35 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3); }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(10, 10, 26, 0.9) !important; border: 1px solid #2a2a4a !important; color: #f5f5f5 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(26, 26, 46, 0.8); border-radius: 8px 8px 0 0;
        padding: 10px 20px; color: #a0a0a0; font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(233, 69, 96, 0.2) !important; color: #e94560 !important;
        border-bottom: 2px solid #e94560;
    }
    /* Custom success box for images */
    .success-box {
        background: rgba(46, 204, 113, 0.1); border: 1px solid #2ecc71;
        border-radius: 10px; padding: 20px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE MANAGEMENT ====================
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = "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"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://via.placeholder.com/150x150/1a1a2e/e94560?text=BC", width=80)
    st.title("BrandCraft AI")
    st.caption("Generative AI Branding Suite")
    st.divider()
    
    api_key_input = st.text_input("Groq API Key", type="password", value=st.session_state.api_key)
    
    if st.button("Initialize Assistant"):
        if api_key_input:
            try:
                st.session_state.assistant = BrandingAssistant(api_key_input)
                st.session_state.api_key = api_key_input
                st.success("✅ Assistant Connected!")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")
        else:
            st.warning("Please enter an API key")
    
    st.divider()
    st.caption("Features:")
    st.caption("• Brand Name Generation")
    st.caption("• Logo Concepts + Images")
    st.caption("• Content Automation")
    st.caption("• Sentiment Analysis")
    st.caption("• Brand Chat Assistant")
    st.divider()
    st.caption("Powered by Llama 3.3 (Groq)")

# ==================== MAIN CONTENT ====================
st.markdown('<h1 class="main-title">BrandCraft AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0;'>Automate your brand identity creation with Generative AI</p>", unsafe_allow_html=True)
st.write("")

if st.session_state.assistant is None:
    st.info("👋 Welcome! Please enter your Groq API Key in the sidebar and click 'Initialize Assistant' to begin.")
    st.stop()

assistant = st.session_state.assistant

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏷️ Brand Names", "🎨 Logo Generator", "📝 Content Studio", "📊 Sentiment", "💬 Brand Assistant", "📖 More Tools"
])

# ========== TAB 1: BRAND NAMES ==========
with tab1:
    st.subheader("Generate Unique Brand Names")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        bn_industry = st.text_input("Industry", value="Technology", placeholder="e.g., Technology, Fashion")
        bn_style = st.selectbox("Naming Style", ["Modern & Minimal", "Classic & Timeless", "Playful & Creative", "Professional & Corporate", "Tech & Futuristic", "Luxury & Premium"])
        bn_keywords = st.text_input("Keywords (comma-separated)", value="smart, innovative, future")
        bn_count = st.slider("Number of Suggestions", 5, 15, 8)
        
        if st.button("Generate Names", use_container_width=True):
            if bn_industry and bn_keywords:
                with st.spinner("Generating creative brand names..."):
                    keywords_list = [k.strip() for k in bn_keywords.split(",")]
                    result = assistant.generate_brand_names(bn_industry, bn_style, keywords_list, bn_count)
                    st.session_state['bn_result'] = result['suggestions']
            else:
                st.warning("Please fill in all fields")
    
    with col2:
        if 'bn_result' in st.session_state:
            st.markdown("### Suggested Brand Names")
            st.markdown(st.session_state['bn_result'])
        else:
            st.info("Results will appear here")

# ========== TAB 2: LOGO GENERATOR (UPDATED WITH IMAGES) ==========
with tab2:
    st.subheader("AI Logo Concept & Image Generator")
    st.markdown("_Generate detailed AI descriptions AND downloadable logo images._")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        logo_brand = st.text_input("Brand Name", value="TechNova", key="logo_brand")
        logo_industry = st.text_input("Industry", value="Technology", key="logo_industry")
        
        logo_style = st.selectbox("Logo Style", [
            "Minimalist", "Geometric", "Abstract", "Wordmark", 
            "Pictorial Mark", "Emblem", "Combination Mark"
        ], key="logo_style_select")
        
        logo_colors = st.text_input("Primary Color", value="Blue", help="Enter a color name (e.g., Blue, Red, Gold) or Hex code (#FFFFFF)")
        
        generate_btn = st.button("Generate Logo Package", use_container_width=True)

    with col2:
        if generate_btn:
            # 1. Generate AI Description
            with st.spinner("AI designing concept..."):
                colors_list = [logo_colors]
                ai_result = assistant.generate_logo_concept(logo_brand, logo_industry, logo_style, colors_list)
                st.session_state['logo_desc'] = ai_result['concept']
            
            # 2. Generate Actual Image
            with st.spinner("Rendering logo image..."):
                try:
                    logo_image = img_gen.generate_logo(logo_brand, logo_style, logo_colors)
                    st.session_state['logo_img'] = logo_image
                except Exception as e:
                    st.error(f"Image generation error: {e}")
        
        # Display Results
        if 'logo_desc' in st.session_state:
            st.markdown("#### AI Design Brief")
            st.markdown(st.session_state['logo_desc'])
            
            st.divider()
            
            if 'logo_img' in st.session_state:
                st.markdown("#### Generated Logo Preview")
                
                # Display Image
                st.image(st.session_state['logo_img'], caption=f"Logo Concept: {st.session_state.get('logo_brand', 'Brand')}", width=300)
                
                # Download Button
                buf = io.BytesIO()
                st.session_state['logo_img'].save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Download Logo (PNG)",
                    data=byte_im,
                    file_name=f"{st.session_state.get('logo_brand', 'logo')}_concept.png",
                    mime="image/png"
                )
        else:
            st.info("Your logo concept and image will appear here")

# ========== TAB 3: CONTENT STUDIO ==========
with tab3:
    st.subheader("Automated Content Generation")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        content_brand = st.text_input("Brand Name", value="BrandCraft", key="content_brand")
        content_industry = st.text_input("Industry", value="SaaS", key="content_industry")
        content_type = st.selectbox("Content Type", ["Website Copy", "Product Description", "About Us Page", "Social Media Post", "Email Newsletter", "Blog Article", "Ad Copy"])
        content_tone = st.selectbox("Tone", ["Professional", "Friendly", "Authoritative", "Playful", "Inspirational"])
        content_points = st.text_area("Key Points (comma-separated)", value="AI-powered, easy to use, affordable")
        
        if st.button("Generate Content", use_container_width=True):
            with st.spinner("Writing content..."):
                points_list = [p.strip() for p in content_points.split(",")]
                result = assistant.generate_content(content_brand, content_type, content_industry, content_tone, points_list, "medium")
                st.session_state['content_result'] = result['content']
    
    with col2:
        if 'content_result' in st.session_state:
            st.markdown("### Generated Content")
            st.markdown(st.session_state['content_result'])
        else:
            st.info("Generated content will appear here")

# ========== TAB 4: SENTIMENT ANALYSIS ==========
with tab4:
    st.subheader("Brand Sentiment Analysis")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        sentiment_text = st.text_area("Text to Analyze", height=200, placeholder="Paste customer reviews, brand content...")
        if st.button("Analyze Sentiment", use_container_width=True):
            if sentiment_text:
                with st.spinner("Analyzing sentiment..."):
                    result = assistant.analyze_sentiment(sentiment_text)
                    st.session_state['sentiment_result'] = result
    
    with col2:
        if 'sentiment_result' in st.session_state:
            res = st.session_state['sentiment_result']
            metric_col1, metric_col2 = st.columns(2)
            polarity = res.get('polarity', 0)
            subjectivity = res.get('subjectivity', 0)
            
            sentiment_label = "Positive" if polarity > 0.3 else "Negative" if polarity < -0.3 else "Neutral"
            sentiment_color = "green" if polarity > 0.3 else "red" if polarity < -0.3 else "gray"
            
            metric_col1.metric("Sentiment Score", f"{polarity:.2f}", f"{sentiment_label}")
            metric_col2.metric("Subjectivity", f"{subjectivity:.2f}", "Opinionated" if subjectivity > 0.5 else "Factual")
            
            st.divider()
            st.markdown("### Detailed Analysis")
            st.markdown(res.get('analysis', 'No analysis available'))
        else:
            st.info("Analysis results will appear here")

# ========== TAB 5: BRAND ASSISTANT (CHAT) ==========
with tab5:
    st.subheader("Interactive Branding Consultant")
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    if prompt := st.chat_input("Ask about branding strategy..."):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = assistant.chat_assistant(prompt)
                st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        assistant.clear_history()
        st.rerun()

# ========== TAB 6: MORE TOOLS ==========
with tab6:
    col_tools1, col_tools2 = st.columns(2)
    
    with col_tools1:
        st.markdown("### 💡 Tagline Generator")
        tag_brand = st.text_input("Brand Name", value="BrandCraft", key="tag_brand")
        tag_industry = st.text_input("Industry", value="Technology", key="tag_industry")
        tag_values = st.text_input("Brand Values", value="Innovation, Trust, Quality")
        
        if st.button("Generate Taglines"):
            with st.spinner("Creating taglines..."):
                values_list = [v.strip() for v in tag_values.split(",")]
                result = assistant.generate_tagline(tag_brand, tag_industry, values_list, "Aspirational")
                st.markdown(result['taglines'])
    
    with col_tools2:
        st.markdown("### 📖 Brand Guidelines")
        guide_brand = st.text_input("Brand Name", value="BrandCraft", key="guide_brand")
        guide_industry = st.text_input("Industry", value="Technology", key="guide_industry")
        guide_personality = st.text_input("Personality", value="Innovative, Friendly")
        
        if st.button("Generate Guidelines"):
            with st.spinner("Creating guidelines..."):
                result = assistant.create_brand_guidelines(guide_brand, guide_industry, guide_personality, "Startups and Entrepreneurs")
                st.markdown(result['guidelines'])
    
    st.divider()
    st.markdown("### 🔍 Competitor Analysis")
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    with col_comp1: comp_brand = st.text_input("Your Brand", value="BrandCraft")
    with col_comp2: comp_industry = st.text_input("Industry", value="AI Tools")
    with col_comp3: comp_list = st.text_input("Competitors", value="Canva, Looka, Figma")
    
    if st.button("Analyze Competition", use_container_width=True):
        with st.spinner("Analyzing competitive landscape..."):
            competitors = [c.strip() for c in comp_list.split(",")]
            result = assistant.competitor_analysis(comp_brand, comp_industry, competitors)
            st.markdown(result['analysis'])

# ==================== FOOTER ====================
st.markdown("""
<div style='text-align: center; padding: 20px; margin-top: 50px; border-top: 1px solid #2a2a4a;'>
    <p style='color: #666; font-size: 0.8rem;'>
        BrandCraft AI — Powered by Groq & Pillow | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
