import os
from dotenv import load_dotenv
from agent.phone_agent import PhoneAgent
from agent.conversation_manager import ConversationManager
from voice.voice_handler import VoiceHandler
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

def main():
    # Setup logging
    logger = setup_logger()
    
    try:
        # Initialize components
        voice_handler = VoiceHandler()
        conversation_manager = ConversationManager()
        
        # Initialize the phone agent
        phone_agent = PhoneAgent(
            voice_handler=voice_handler,
            conversation_manager=conversation_manager,
            logger=logger
        )
        
        # Start the agent
        phone_agent.start()
        
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        raise

if __name__ == "__main__":
    main()
