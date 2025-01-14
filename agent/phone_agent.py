import openai
from typing import Dict, Any
import json
import time
import os

class PhoneAgent:
    def __init__(self, voice_handler, conversation_manager, logger):
        self.voice_handler = voice_handler
        self.conversation_manager = conversation_manager
        self.logger = logger
        
        # Initialize OpenAI client with API key
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Load agent configuration
        self.load_config()
        
    def load_config(self):
        """Load agent configuration and prompts"""
        try:
            with open('config/agent_config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.error("Agent configuration file not found")
            raise
            
    def start(self):
        """Start the phone agent"""
        self.logger.info("Starting phone agent...")
        while True:
            try:
                # Get next customer to call
                customer = self.get_next_customer()
                if customer:
                    self.make_call(customer)
                time.sleep(self.config.get('call_delay', 60))
            except Exception as e:
                self.logger.error(f"Error in phone agent: {str(e)}")
                
    def get_next_customer(self) -> Dict[str, Any]:
        """Get the next customer to call from the queue"""
        # Implementation for customer selection logic
        pass
        
    def make_call(self, customer: Dict[str, Any]):
        """Make a phone call to a customer"""
        try:
            # Initialize call
            call = self.voice_handler.initiate_call(customer['phone_number'])
            
            # Start conversation loop
            while True:
                # Get customer input
                customer_input = self.voice_handler.listen()
                
                # Process through conversation manager
                response = self.conversation_manager.process_input(
                    customer_input,
                    customer_context=customer
                )
                
                # Convert response to speech and send
                self.voice_handler.speak(response)
                
                # Check if conversation should end
                if self.conversation_manager.should_end_call():
                    break
                    
        except Exception as e:
            self.logger.error(f"Error during call: {str(e)}")
        finally:
            self.voice_handler.end_call()
            
    def generate_response(self, context: Dict[str, Any]) -> str:
        """Generate AI response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.config['system_prompt']},
                    {"role": "user", "content": self._format_context(context)}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error generating AI response: {str(e)}")
            return self.config['fallback_response']
            
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context for AI prompt"""
        return f"""
        Customer Name: {context.get('name', 'Unknown')}
        Previous Interaction: {context.get('history', 'None')}
        Current Topic: {context.get('current_topic', 'Introduction')}
        Customer Profile: {context.get('profile', {})}
        """
