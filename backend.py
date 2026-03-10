"""
backend.py
BrandCraft: Generative AI-Powered Branding Automation System
Main application with Gradio web interface
"""

import os
import gradio as gr
from branding_assistant import BrandingAssistant
from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')


# ==================== CONFIGURATION ====================

# API Configuration - Use environment variable or direct key
API_KEY = os.getenv("GROQ_API_KEY", "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")

# Initialize the branding assistant
assistant = None


def initialize_assistant(api_key: str = None):
    """Initialize or reinitialize the branding assistant"""
    global assistant
    key = api_key if api_key else API_KEY
    if not key or key == "your-api-key-here":
        return None
    try:
        assistant = BrandingAssistant(key)
        return assistant
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        return None


# Initialize on startup
assistant = initialize_assistant()


# ==================== BRAND NAME GENERATION ====================

def generate_brand_names_ui(industry: str, style: str, keywords: str, count: int):
    """UI wrapper for brand name generation"""
    if not assistant:
        return "Please configure a valid API key first."
    
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    if not keyword_list:
        keyword_list = ["innovative", "modern", "quality"]
    
    result = assistant.generate_brand_names(
        industry=industry,
        style=style,
        keywords=keyword_list,
        count=count
    )
    
    output = f"## Brand Name Suggestions for {industry}\n\n"
    output += f"**Style:** {style}\n**Keywords:** {', '.join(keyword_list)}\n\n---\n\n"
    output += result["suggestions"]
    
    return output


# ==================== LOGO CONCEPT GENERATION ====================

def generate_logo_concept_ui(brand_name: str, industry: str, style: str, colors: str):
    """UI wrapper for logo concept generation"""
    if not assistant:
        return "Please configure a valid API key first."
    
    color_list = [c.strip() for c in colors.split(",") if c.strip()]
    if not color_list:
        color_list = ["Blue", "White"]
    
    result = assistant.generate_logo_concept(
        brand_name=brand_name,
        industry=industry,
        style=style,
        colors=color_list
    )
    
    output = f"## Logo Design Concept for {brand_name}\n\n"
    output += f"**Industry:** {industry}\n**Style:** {style}\n**Colors:** {', '.join(color_list)}\n\n---\n\n"
    output += result["concept"]
    
    return output


# ==================== CONTENT AUTOMATION ====================

def generate_content_ui(brand_name: str, content_type: str, industry: str, 
                        tone: str, key_points: str, length: str):
    """UI wrapper for content generation"""
    if not assistant:
        return "Please configure a valid API key first."
    
    points_list = [p.strip() for p in key_points.split(",") if p.strip()]
    if not points_list:
        points_list = ["Quality", "Innovation", "Customer Focus"]
    
    result = assistant.generate_content(
        brand_name=brand_name,
        content_type=content_type,
        industry=industry,
        tone=tone,
        key_points=points_list,
        length=length
    )
    
    output = f"## {content_type} for {brand_name}\n\n"
    output += f"**Industry:** {industry}\n**Tone:** {tone}\n\n---\n\n"
    output += result["content"]
    
    return output


# ==================== SENTIMENT ANALYSIS ====================

def analyze_sentiment_ui(text: str):
    """UI wrapper for sentiment analysis"""
    if not assistant:
        return "Please configure a valid API key first."
    
    if not text.strip():
        return "Please enter some text to analyze."
    
    result = assistant.analyze_sentiment(text)
    
    output = "## Sentiment Analysis Results\n\n"
    
    # Quantitative metrics
    quant = result["quantitative"]
    polarity = quant["polarity"]
    subjectivity = quant["subjectivity"]
    
    # Determine sentiment label
    if polarity > 0.3:
        sentiment_label = "Positive"
        sentiment_emoji = "🟢"
    elif polarity < -0.3:
        sentiment_label = "Negative"
        sentiment_emoji = "🔴"
    else:
        sentiment_label = "Neutral"
        sentiment_emoji = "🟡"
    
    output += f"### Quantitative Metrics\n\n"
    output += f"| Metric | Value | Indicator |\n"
    output += f"|--------|-------|----------|\n"
    output += f"| **Polarity** | {polarity} | {sentiment_emoji} {sentiment_label} |\n"
    output += f"| **Subjectivity** | {subjectivity} | {'💡 Opinionated' if subjectivity > 0.5 else '📋 Factual'} |\n\n"
    
    output += "---\n\n### Detailed Analysis\n\n"
    output += result["analysis"]
    
    return output


# ==================== BRANDING ASSISTANT CHAT ====================

def chat_assistant_ui(message: str, history: List, context: str):
    """UI wrapper for interactive branding chat"""
    if not assistant:
        return "Please configure a valid API key first."
    
    response = assistant.chat_assistant(message, context if context else None)
    return response


# ==================== TAGLINE GENERATION ====================

def generate_tagline_ui(brand_name: str, industry: str, values: str, style: str):
    """UI wrapper for tagline generation"""
    if not assistant:
        return "Please configure a valid API key first."
    
    values_list = [v.strip() for v in values.split(",") if v.strip()]
    if not values_list:
        values_list = ["Innovation", "Trust", "Excellence"]
    
    result = assistant.generate_tagline(
        brand_name=brand_name,
        industry=industry,
        values=values_list,
        style=style
    )
    
    output = f"## Tagline Options for {brand_name}\n\n"
    output += f"**Industry:** {industry}\n**Values:** {', '.join(values_list)}\n\n---\n\n"
    output += result["taglines"]
    
    return output


# ==================== BRAND GUIDELINES ====================

def create_guidelines_ui(brand_name: str, industry: str, personality: str, target: str):
    """UI wrapper for brand guidelines generation"""
    if not assistant:
        return "Please configure a valid API key first."
    
    result = assistant.create_brand_guidelines(
        brand_name=brand_name,
        industry=industry,
        personality=personality,
        target_audience=target
    )
    
    output = f"# Brand Guidelines: {brand_name}\n\n"
    output += result["guidelines"]
    
    return output


# ==================== COMPETITOR ANALYSIS ====================

def competitor_analysis_ui(brand_name: str, industry: str, competitors: str):
    """UI wrapper for competitor analysis"""
    if not assistant:
        return "Please configure a valid API key first."
    
    comp_list = [c.strip() for c in competitors.split(",") if c.strip()]
    if not comp_list:
        return "Please enter at least one competitor."
    
    result = assistant.competitor_analysis(
        brand_name=brand_name,
        industry=industry,
        competitors=comp_list
    )
    
    output = f"# Competitive Analysis: {brand_name}\n\n"
    output += result["analysis"]
    
    return output


# ==================== API KEY CONFIGURATION ====================

def configure_api_key(api_key: str):
    """Configure a new API key"""
    global assistant
    try:
        assistant = initialize_assistant(api_key)
        if assistant:
            return "✅ API key configured successfully! All features are now available."
        else:
            return "❌ Failed to initialize. Please check your API key."
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ==================== CLEAR CHAT HISTORY ====================

def clear_chat():
    """Clear the chat conversation history"""
    if assistant:
        assistant.clear_history()
    return []


# ==================== GRADIO INTERFACE ====================

# Custom CSS for professional styling
custom_css = """
:root {
    --primary: #0a0a0a;
    --secondary: #1a1a2e;
    --accent: #e94560;
    --accent-secondary: #ff6b35;
    --text: #f5f5f5;
    --text-muted: #a0a0a0;
    --card-bg: #16162a;
    --border: #2a2a4a;
}

.gradio-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%) !important;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
}

.gradio-container .main {
    background: transparent !important;
}

h1, h2, h3 {
    color: var(--text) !important;
    font-weight: 600 !important;
}

.gr-box, .gr-panel {
    background: rgba(22, 22, 42, 0.8) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

.gr-input, .gr-textbox textarea, .gr-dropdown {
    background: rgba(10, 10, 26, 0.9) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.gr-button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3) !important;
}

.gr-button-secondary {
    background: var(--secondary) !important;
    border: 1px solid var(--border) !important;
}

.gr-tabs {
    border-bottom: 2px solid var(--border) !important;
}

.gr-tab {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}

.gr-tab.gr-tab--selected {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

.markdown-body {
    color: var(--text) !important;
    background: transparent !important;
}

.markdown-body h1, .markdown-body h2, .markdown-body h3 {
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 10px !important;
}

.markdown-body table {
    border-collapse: collapse !important;
}

.markdown-body th, .markdown-body td {
    border: 1px solid var(--border) !important;
    padding: 10px 15px !important;
}

.markdown-body th {
    background: var(--secondary) !important;
}

footer {
    display: none !important;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
"""


def create_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(css=custom_css, title="BrandCraft AI", theme=gr.themes.Base()) as demo:
        
        # Header
        gr.HTML("""
        <div style="text-align: center; padding: 20px 0 30px;">
            <h1 style="font-size: 2.8rem; font-weight: 800; 
                background: linear-gradient(135deg, #e94560, #ff6b35, #f7931e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;">
                BrandCraft AI
            </h1>
            <p style="font-size: 1.1rem; color: #a0a0a0; font-weight: 400;">
                Generative AI-Powered Branding Automation System
            </p>
            <p style="font-size: 0.9rem; color: #666; margin-top: 5px;">
                Create compelling brand identities, content, and strategies with AI
            </p>
        </div>
        """)
        
        # API Configuration (collapsible)
        with gr.Accordion("⚙️ API Configuration", open=False):
            api_input = gr.Textbox(
                label="Groq API Key",
                type="password",
                placeholder="Enter your Groq API key (gsk_...)",
                value=""
            )
            api_btn = gr.Button("Connect API", variant="primary")
            api_status = gr.Textbox(label="Status", interactive=False)
            
            api_btn.click(
                fn=configure_api_key,
                inputs=[api_input],
                outputs=[api_status]
            )
        
        # Main Tabs
        with gr.Tabs():
            
            # ===== BRAND NAME GENERATION TAB =====
            with gr.TabItem("🏷️ Brand Names"):
                gr.Markdown("""
                ### Generate Unique Brand Names
                Create memorable, brandable names tailored to your industry and style preferences.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        bn_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., Technology, Fashion, Food & Beverage",
                            value="Technology"
                        )
                        bn_style = gr.Dropdown(
                            label="Naming Style",
                            choices=[
                                "Modern & Minimal",
                                "Classic & Timeless",
                                "Playful & Creative",
                                "Professional & Corporate",
                                "Tech & Futuristic",
                                "Nature & Organic",
                                "Luxury & Premium",
                                "Bold & Edgy"
                            ],
                            value="Modern & Minimal"
                        )
                        bn_keywords = gr.Textbox(
                            label="Keywords (comma-separated)",
                            placeholder="e.g., innovation, speed, quality",
                            value="innovation, future, smart"
                        )
                        bn_count = gr.Slider(
                            label="Number of Suggestions",
                            minimum=5,
                            maximum=20,
                            value=10,
                            step=1
                        )
                        bn_btn = gr.Button("Generate Brand Names", variant="primary")
                    
                    with gr.Column(scale=2):
                        bn_output = gr.Markdown(label="Generated Brand Names")
                
                bn_btn.click(
                    fn=generate_brand_names_ui,
                    inputs=[bn_industry, bn_style, bn_keywords, bn_count],
                    outputs=[bn_output]
                )
            
            # ===== LOGO CONCEPT TAB =====
            with gr.TabItem("🎨 Logo Concepts"):
                gr.Markdown("""
                ### Generate Logo Design Concepts
                Get detailed logo design briefs including visual descriptions, typography, and color recommendations.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        logo_brand = gr.Textbox(
                            label="Brand Name",
                            placeholder="Enter your brand name",
                            value="TechNova"
                        )
                        logo_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., Technology, Healthcare",
                            value="Technology"
                        )
                        logo_style = gr.Dropdown(
                            label="Logo Style",
                            choices=[
                                "Minimalist",
                                "Geometric",
                                "Abstract",
                                "Wordmark",
                                "Pictorial Mark",
                                "Emblem",
                                "Mascot",
                                "Combination Mark"
                            ],
                            value="Minimalist"
                        )
                        logo_colors = gr.Textbox(
                            label="Preferred Colors (comma-separated)",
                            placeholder="e.g., Blue, Silver, White",
                            value="Blue, Silver, White"
                        )
                        logo_btn = gr.Button("Generate Logo Concept", variant="primary")
                    
                    with gr.Column(scale=2):
                        logo_output = gr.Markdown(label="Logo Concept")
                
                logo_btn.click(
                    fn=generate_logo_concept_ui,
                    inputs=[logo_brand, logo_industry, logo_style, logo_colors],
                    outputs=[logo_output]
                )
            
            # ===== CONTENT AUTOMATION TAB =====
            with gr.TabItem("📝 Content Studio"):
                gr.Markdown("""
                ### Automated Content Generation
                Generate various types of marketing and brand content instantly.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        content_brand = gr.Textbox(
                            label="Brand Name",
                            placeholder="Enter your brand name",
                            value="BrandCraft"
                        )
                        content_type = gr.Dropdown(
                            label="Content Type",
                            choices=[
                                "Website Copy",
                                "Product Description",
                                "About Us Page",
                                "Social Media Post",
                                "Email Newsletter",
                                "Press Release",
                                "Blog Article",
                                "Ad Copy",
                                "Landing Page",
                                "Brand Story"
                            ],
                            value="Website Copy"
                        )
                        content_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., SaaS, E-commerce",
                            value="SaaS"
                        )
                        content_tone = gr.Dropdown(
                            label="Tone",
                            choices=[
                                "Professional",
                                "Friendly",
                                "Authoritative",
                                "Playful",
                                "Inspirational",
                                "Technical",
                                "Conversational",
                                "Luxurious"
                            ],
                            value="Professional"
                        )
                        content_points = gr.Textbox(
                            label="Key Points (comma-separated)",
                            placeholder="e.g., quality, innovation, customer support",
                            value="AI-powered, easy to use, affordable"
                        )
                        content_length = gr.Radio(
                            label="Content Length",
                            choices=["short", "medium", "long"],
                            value="medium"
                        )
                        content_btn = gr.Button("Generate Content", variant="primary")
                    
                    with gr.Column(scale=2):
                        content_output = gr.Markdown(label="Generated Content")
                
                content_btn.click(
                    fn=generate_content_ui,
                    inputs=[content_brand, content_type, content_industry, 
                            content_tone, content_points, content_length],
                    outputs=[content_output]
                )
            
            # ===== SENTIMENT ANALYSIS TAB =====
            with gr.TabItem("📊 Sentiment Analysis"):
                gr.Markdown("""
                ### Brand Sentiment Analysis
                Analyze text for sentiment, emotional tone, and brand alignment insights.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        sentiment_text = gr.Textbox(
                            label="Text to Analyze",
                            placeholder="Enter brand content, customer reviews, or any text...",
                            lines=8
                        )
                        sentiment_btn = gr.Button("Analyze Sentiment", variant="primary")
                    
                    with gr.Column(scale=2):
                        sentiment_output = gr.Markdown(label="Analysis Results")
                
                sentiment_btn.click(
                    fn=analyze_sentiment_ui,
                    inputs=[sentiment_text],
                    outputs=[sentiment_output]
                )
            
            # ===== BRANDING ASSISTANT TAB =====
            with gr.TabItem("💬 Brand Assistant"):
                gr.Markdown("""
                ### Interactive Branding Consultant
                Chat with our AI branding expert for personalized advice and recommendations.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        chat_context = gr.Textbox(
                            label="Context (Optional)",
                            placeholder="Provide context about your brand...",
                            lines=3
                        )
                        clear_btn = gr.Button("Clear Conversation", variant="secondary")
                
                # FIXED: Removed 'bubble_full_width' argument
                chatbot = gr.Chatbot(
                    label="BrandCraft Assistant",
                    height=450
                )
                
                with gr.Row():
                    chat_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask about branding strategy, positioning, naming...",
                        scale=4
                    )
                    chat_btn = gr.Button("Send", variant="primary", scale=1)
                
                def chat_wrapper(message, history):
                    response = chat_assistant_ui(message, history, "")
                    history.append((message, response))
                    return history, ""
                
                chat_btn.click(
                    fn=chat_wrapper,
                    inputs=[chat_input, chatbot],
                    outputs=[chatbot, chat_input]
                )
                
                chat_input.submit(
                    fn=chat_wrapper,
                    inputs=[chat_input, chatbot],
                    outputs=[chatbot, chat_input]
                )
                
                clear_btn.click(
                    fn=clear_chat,
                    outputs=[chatbot]
                )
            
            # ===== TAGLINE GENERATION TAB =====
            with gr.TabItem("💡 Taglines"):
                gr.Markdown("""
                ### Brand Tagline Generator
                Create memorable, impactful taglines that capture your brand essence.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        tag_brand = gr.Textbox(
                            label="Brand Name",
                            placeholder="Enter your brand name",
                            value="BrandCraft"
                        )
                        tag_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., Technology, Retail",
                            value="Technology"
                        )
                        tag_values = gr.Textbox(
                            label="Brand Values (comma-separated)",
                            placeholder="e.g., innovation, trust, simplicity",
                            value="innovation, creativity, simplicity"
                        )
                        tag_style = gr.Dropdown(
                            label="Tagline Style",
                            choices=[
                                "Aspirational",
                                "Descriptive",
                                "Provocative",
                                "Emotional",
                                "Playful",
                                "Minimal",
                                "Bold"
                            ],
                            value="Aspirational"
                        )
                        tag_btn = gr.Button("Generate Taglines", variant="primary")
                    
                    with gr.Column(scale=2):
                        tag_output = gr.Markdown(label="Tagline Options")
                
                tag_btn.click(
                    fn=generate_tagline_ui,
                    inputs=[tag_brand, tag_industry, tag_values, tag_style],
                    outputs=[tag_output]
                )
            
            # ===== BRAND GUIDELINES TAB =====
            with gr.TabItem("📖 Brand Guidelines"):
                gr.Markdown("""
                ### Comprehensive Brand Guidelines
                Generate detailed brand guidelines covering mission, voice, visual identity, and more.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        guide_brand = gr.Textbox(
                            label="Brand Name",
                            placeholder="Enter your brand name",
                            value="BrandCraft"
                        )
                        guide_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., Technology, Fashion",
                            value="AI Technology"
                        )
                        guide_personality = gr.Textbox(
                            label="Brand Personality",
                            placeholder="e.g., Innovative, Friendly, Professional",
                            value="Innovative, Friendly, Professional"
                        )
                        guide_target = gr.Textbox(
                            label="Target Audience",
                            placeholder="e.g., Small business owners, entrepreneurs",
                            value="Startups and small business owners"
                        )
                        guide_btn = gr.Button("Generate Guidelines", variant="primary")
                    
                    with gr.Column(scale=2):
                        guide_output = gr.Markdown(label="Brand Guidelines")
                
                guide_btn.click(
                    fn=create_guidelines_ui,
                    inputs=[guide_brand, guide_industry, guide_personality, guide_target],
                    outputs=[guide_output]
                )
            
            # ===== COMPETITOR ANALYSIS TAB =====
            with gr.TabItem("🔍 Competitor Analysis"):
                gr.Markdown("""
                ### Competitive Brand Analysis
                Get insights on your competitive landscape and differentiation opportunities.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        comp_brand = gr.Textbox(
                            label="Your Brand Name",
                            placeholder="Enter your brand name",
                            value="BrandCraft"
                        )
                        comp_industry = gr.Textbox(
                            label="Industry",
                            placeholder="e.g., AI Tools, Marketing Software",
                            value="AI Branding Tools"
                        )
                        comp_competitors = gr.Textbox(
                            label="Competitors (comma-separated)",
                            placeholder="e.g., Canva, Figma, Looka",
                            value="Canva, Looka, Tailor Brands"
                        )
                        comp_btn = gr.Button("Analyze Competition", variant="primary")
                    
                    with gr.Column(scale=2):
                        comp_output = gr.Markdown(label="Competitive Analysis")
                
                comp_btn.click(
                    fn=competitor_analysis_ui,
                    inputs=[comp_brand, comp_industry, comp_competitors],
                    outputs=[comp_output]
                )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 30px 0 20px; margin-top: 20px; border-top: 1px solid #2a2a4a;">
            <p style="color: #666; font-size: 0.85rem;">
                BrandCraft AI — Powered by Groq & Llama 3.3 | Built with Gradio
            </p>
            <p style="color: #444; font-size: 0.75rem; margin-top: 5px;">
                © 2025 BrandCraft. All rights reserved.
            </p>
        </div>
        """)
    
    return demo


# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  BrandCraft: Generative AI-Powered Branding Automation")
    print("=" * 60)
    print("\nInitializing application...")
    
    # Create and launch the interface
    demo = create_interface()
    
    print("\n🚀 Launching BrandCraft AI...")
    print("📱 Opening web interface in your browser...\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )
