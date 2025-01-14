import os
from elevenlabs import generate, play
import speech_recognition as sr
from twilio.rest import Client
from typing import Optional
import logging

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Initialize Twilio client with better error handling
        twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if twilio_sid and twilio_token:
            try:
                self.twilio_client = Client(twilio_sid, twilio_token)
            except Exception as e:
                logging.error(f"Failed to initialize Twilio client: {str(e)}")
                self.twilio_client = None
        else:
            logging.warning("Twilio credentials not found in environment variables")
            self.twilio_client = None
            
        self.current_call = None
        
    def initiate_call(self, phone_number: str) -> Optional[str]:
        """Initiate a phone call using Twilio"""
        if not self.twilio_client:
            logging.error("Cannot initiate call: Twilio client not initialized")
            return None
            
        try:
            call = self.twilio_client.calls.create(
                url='http://your-webhook-url/voice',  # Webhook for call handling
                to=phone_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER')
            )
            self.current_call = call.sid
            return call.sid
        except Exception as e:
            logging.error(f"Error initiating call: {str(e)}")
            return None
            
    def listen(self) -> str:
        """Listen and convert speech to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {str(e)}")
            return ""
            
    def speak(self, text: str) -> None:
        """Convert text to speech and play it"""
        try:
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice="Josh",  # Can be configured based on agent personality
                model="eleven_monolingual_v1"
            )
            
            # Play the audio
            play(audio)
            
            # If in a call, send audio through Twilio
            if self.current_call:
                self._send_audio_to_call(audio)
                
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            
    def _send_audio_to_call(self, audio_data: bytes) -> None:
        """Send audio data to active Twilio call"""
        if not self.current_call:
            return
            
        try:
            # Implementation for sending audio to Twilio call
            pass
        except Exception as e:
            print(f"Error sending audio to call: {str(e)}")
            
    def end_call(self) -> None:
        """End the current call"""
        if self.current_call:
            try:
                self.twilio_client.calls(self.current_call).update(status="completed")
                self.current_call = None
            except Exception as e:
                print(f"Error ending call: {str(e)}")
                
    def is_call_active(self) -> bool:
        """Check if there is an active call"""
        if not self.current_call:
            return False
            
        try:
            call = self.twilio_client.calls(self.current_call).fetch()
            return call.status in ['queued', 'ringing', 'in-progress']
        except Exception:
            return False
