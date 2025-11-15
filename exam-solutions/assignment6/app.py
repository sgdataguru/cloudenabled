#!/usr/bin/env python3
"""
Assignment 6: Healthcare Assistant Chatbot
Duration: 30 minutes
Focus: Flask, OpenAI LLM, Web Development

This Flask application provides:
- A healthcare assistant chatbot with web interface
- Knowledge base covering diet tips and health practices
- OpenAI LLM integration for intelligent responses
- Medical disclaimers and safety redirects
- Chat history (last 5 messages)
- Responsive web design
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import re

# Try to import OpenAI, fallback to local responses if not available
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not available. Using local responses only.")

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'healthcare-assistant-secret-key-2024')

# Configuration
app.config['MAX_CHAT_HISTORY'] = 5
app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')

# Initialize OpenAI client if available and key is provided
openai_client = None
if OPENAI_AVAILABLE and app.config['OPENAI_API_KEY']:
    try:
        openai_client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        openai_client = None

class HealthcareKnowledgeBase:
    """Healthcare knowledge base for local responses"""
    
    def __init__(self, kb_file: str = 'kb.json'):
        """Initialize knowledge base from JSON file"""
        self.kb_path = kb_file
        self.kb_data = self.load_knowledge_base()
    
    def load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from JSON file"""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file {self.kb_path} not found. Using minimal fallback.")
            return self._get_fallback_kb()
        except json.JSONDecodeError:
            print(f"Error parsing knowledge base file {self.kb_path}. Using minimal fallback.")
            return self._get_fallback_kb()
    
    def _get_fallback_kb(self) -> Dict[str, Any]:
        """Minimal fallback knowledge base"""
        return {
            "dos": ["Aim for 7-9 hours of sleep", "Drink water regularly", "Include vegetables in meals"],
            "donts": ["Avoid skipping meals", "Limit sugary drinks", "Don't ignore symptoms"],
            "diet_tips": ["Balanced plate: 1/2 veggies, 1/4 protein, 1/4 grains"],
            "safety_keywords": ["chest pain", "emergency", "doctor", "medication", "symptoms"],
            "fallback": "I can help with general health tips. Try asking about daily do's or diet advice."
        }
    
    def is_medical_query(self, message: str) -> bool:
        """Check if message contains medical keywords requiring safety redirect"""
        message_lower = message.lower()
        safety_keywords = self.kb_data.get('safety_keywords', [])
        
        for keyword in safety_keywords:
            if keyword in message_lower:
                return True
        return False
    
    def get_safety_response(self) -> str:
        """Get safety redirect response for medical queries"""
        return """I can't help with medical issues, symptoms, or diagnoses. 

🏥 **Please consult a healthcare professional or emergency services for:**
- Any symptoms or health concerns
- Medical advice or diagnoses
- Medication questions
- Emergency situations

I'm here to help with general wellness tips, diet planning, and healthy lifestyle advice only."""
    
    def find_response(self, message: str) -> str:
        """Find appropriate response based on message content"""
        message_lower = message.lower()
        
        # Check for medical queries first
        if self.is_medical_query(message):
            return self.get_safety_response()
        
        # Check for specific topics
        if any(word in message_lower for word in ['do', 'dos', "do's", 'should do']):
            return self._format_list_response("Daily Health Do's", self.kb_data.get('dos', []))
        
        if any(word in message_lower for word in ['dont', "don't", 'donts', "don'ts", 'avoid', 'should not']):
            return self._format_list_response("Daily Health Don'ts", self.kb_data.get('donts', []))
        
        if any(word in message_lower for word in ['diet', 'nutrition', 'eating', 'food']):
            return self._format_list_response("Diet Tips", self.kb_data.get('diet_tips', []))
        
        if any(word in message_lower for word in ['hydration', 'water', 'drink']):
            return self._format_list_response("Hydration Tips", self.kb_data.get('hydration', []))
        
        if any(word in message_lower for word in ['exercise', 'workout', 'fitness', 'activity']):
            return self._format_list_response("Exercise Tips", self.kb_data.get('exercise', []))
        
        # Check for meal plans
        plans = self.kb_data.get('plans', {})
        for plan_name, plan_data in plans.items():
            if plan_name in message_lower or any(keyword in message_lower for keyword in plan_name.split()):
                return self._format_meal_plan(plan_name.title(), plan_data)
        
        # Fallback response
        return self.kb_data.get('fallback', "I can help with health tips, diet plans, and wellness advice. What would you like to know?")
    
    def _format_list_response(self, title: str, items: List[str]) -> str:
        """Format a list of items as a response"""
        if not items:
            return f"I don't have specific information about {title.lower()} right now."
        
        response = f"**{title}:**\n\n"
        for item in items:
            response += f"• {item}\n"
        
        response += f"\nRemember, these are general guidelines. For personalized advice, consult a healthcare professional."
        return response
    
    def _format_meal_plan(self, plan_name: str, plan_data: Dict[str, str]) -> str:
        """Format a meal plan as a response"""
        if not plan_data:
            return f"I don't have a {plan_name} plan available right now."
        
        response = f"**{plan_name} Plan:**\n\n"
        
        meals = ['breakfast', 'lunch', 'snack', 'dinner']
        for meal in meals:
            if meal in plan_data:
                response += f"**{meal.title()}:** {plan_data[meal]}\n"
        
        if 'tips' in plan_data:
            response += f"\n**Tips:** {plan_data['tips']}\n"
        
        response += f"\nThis is a general plan. For personalized nutrition advice, consult a registered dietitian."
        return response

# Initialize knowledge base
kb = HealthcareKnowledgeBase()

def get_chat_history() -> List[Dict[str, str]]:
    """Get chat history from session"""
    return session.get('chat_history', [])

def add_to_chat_history(message: str, message_type: str) -> None:
    """Add message to chat history, keeping only last 5 messages"""
    chat_history = get_chat_history()
    
    # Add new message
    chat_history.append({
        'content': message,
        'type': message_type,
        'timestamp': datetime.now().strftime('%H:%M')
    })
    
    # Keep only last 5 messages (excluding current)
    max_history = app.config['MAX_CHAT_HISTORY']
    if len(chat_history) > max_history:
        chat_history = chat_history[-max_history:]
    
    session['chat_history'] = chat_history

def get_openai_response(message: str) -> str:
    """Get response from OpenAI API"""
    if not openai_client:
        return kb.find_response(message)
    
    try:
        # Check for medical queries first
        if kb.is_medical_query(message):
            return kb.get_safety_response()
        
        # Prepare context for OpenAI
        system_prompt = """You are a helpful healthcare wellness assistant. You provide general health and wellness advice including:

- Daily health do's and don'ts
- Diet and nutrition tips
- Meal planning advice
- Hydration and exercise guidance
- General lifestyle recommendations

IMPORTANT SAFETY RULES:
1. NEVER provide medical advice, diagnoses, or treatment recommendations
2. If users ask about symptoms, medications, or medical conditions, redirect them to healthcare professionals
3. Always include disclaimers that your advice is general information only
4. Be supportive but emphasize the importance of professional medical care when needed

Keep responses helpful, friendly, and focused on general wellness. Use bullet points and clear formatting when listing tips or advice."""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback to knowledge base
        return kb.find_response(message)

@app.route('/')
def index():
    """Main chat page"""
    # Clear chat history on page reload for demo purposes
    if 'new_session' not in session:
        session['chat_history'] = []
        session['new_session'] = True
    
    return render_template('index.html', 
                         chat_history=get_chat_history(),
                         current_time=datetime.now().strftime('%H:%M'))

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Add user message to history
        add_to_chat_history(user_message, 'user')
        
        # Get bot response
        if openai_client and not kb.is_medical_query(user_message):
            bot_response = get_openai_response(user_message)
        else:
            bot_response = kb.find_response(user_message)
        
        # Add bot response to history
        add_to_chat_history(bot_response, 'bot')
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'An error occurred processing your message'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'openai_available': openai_client is not None,
        'knowledge_base_loaded': len(kb.kb_data) > 0
    })

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    session['chat_history'] = []
    return jsonify({'message': 'Chat history cleared'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', 
                         chat_history=get_chat_history(),
                         current_time=datetime.now().strftime('%H:%M')), 200

@app.errorhandler(500)
def internal_error(error):
    print(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Healthcare Assistant Chatbot...")
    print(f"OpenAI integration: {'Enabled' if openai_client else 'Disabled (using local KB only)'}")
    print(f"Knowledge base loaded: {len(kb.kb_data)} categories")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file template...")
        with open('.env', 'w') as f:
            f.write("# Healthcare Assistant Chatbot Environment Variables\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
        print("Please edit .env file with your OpenAI API key for enhanced responses.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
