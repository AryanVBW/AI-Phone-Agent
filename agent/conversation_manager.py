from typing import Dict, Any, List
import json
import time

class ConversationManager:
    def __init__(self):
        self.conversation_history = []
        self.current_state = "initial"
        self.load_conversation_flows()
        
    def load_conversation_flows(self):
        """Load conversation flows and scripts"""
        try:
            with open('config/conversation_flows.json', 'r') as f:
                self.flows = json.load(f)
        except FileNotFoundError:
            raise Exception("Conversation flows configuration not found")
            
    def process_input(self, user_input: str, customer_context: Dict[str, Any]) -> str:
        """Process user input and generate appropriate response"""
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": time.time()
        })
        
        # Analyze intent and sentiment
        intent = self.analyze_intent(user_input)
        sentiment = self.analyze_sentiment(user_input)
        
        # Get next response based on current state and analysis
        response = self.get_next_response(intent, sentiment, customer_context)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": time.time()
        })
        
        return response
        
    def analyze_intent(self, text: str) -> str:
        """Analyze the intent of user input"""
        # Implementation for intent analysis
        pass
        
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze the sentiment of user input"""
        # Implementation for sentiment analysis
        pass
        
    def get_next_response(self, intent: str, sentiment: Dict[str, float], 
                         context: Dict[str, Any]) -> str:
        """Get next response based on conversation state and analysis"""
        try:
            # Get appropriate flow based on current state
            current_flow = self.flows[self.current_state]
            
            # Determine next state
            self.current_state = self.determine_next_state(
                current_flow, intent, sentiment
            )
            
            # Get response template
            response_template = current_flow['responses'].get(
                intent, current_flow['default_response']
            )
            
            # Personalize response
            return self.personalize_response(response_template, context)
            
        except Exception as e:
            return self.flows['fallback']['default_response']
            
    def determine_next_state(self, current_flow: Dict[str, Any], 
                           intent: str, sentiment: Dict[str, float]) -> str:
        """Determine the next conversation state"""
        transitions = current_flow.get('transitions', {})
        
        # Check for intent-based transitions
        if intent in transitions:
            return transitions[intent]
            
        # Check for sentiment-based transitions
        if sentiment['negative'] > 0.7:
            return 'handling_objection'
        
        return self.current_state
        
    def personalize_response(self, template: str, context: Dict[str, Any]) -> str:
        """Personalize response template with customer context"""
        try:
            return template.format(**context)
        except KeyError:
            return template
            
    def should_end_call(self) -> bool:
        """Determine if the conversation should end"""
        # Check if we've reached a terminal state
        if self.current_state in ['call_completed', 'sale_closed', 'call_rejected']:
            return True
            
        # Check conversation duration
        if self.get_conversation_duration() > 900:  # 15 minutes
            return True
            
        return False
        
    def get_conversation_duration(self) -> float:
        """Get the duration of the conversation in seconds"""
        if not self.conversation_history:
            return 0
            
        start_time = self.conversation_history[0]['timestamp']
        end_time = self.conversation_history[-1]['timestamp']
        return end_time - start_time
