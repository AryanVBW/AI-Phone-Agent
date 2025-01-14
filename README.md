# AI Phone Agent

An intelligent, AI-powered phone agent system capable of making cold calls, engaging in natural conversations, and closing sales using OpenAI's GPT models and voice synthesis.

## Features

- 🤖 Natural language understanding and generation using OpenAI GPT-4
- 🗣️ High-quality voice synthesis using ElevenLabs
- 📞 Phone call handling through Twilio integration
- 🔄 Dynamic response personalization
- 📊 Conversation state management and analytics
- 📝 Detailed logging and monitoring
- ⚙️ Configurable conversation flows and responses

## Prerequisites

- Python 3.8+
- OpenAI API account
- ElevenLabs API account
- Twilio account with a phone number

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-phone-agent.git
cd ai-phone-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Set up your API credentials in `.env`:
```plaintext
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

3. Configure conversation flows in `config/conversation_flows.json`
4. Adjust agent settings in `config/agent_config.json`

## Usage

Run the agent:
```bash
python main.py
```

The agent will:
1. Initialize all necessary components
2. Load conversation flows and configurations
3. Begin making calls according to the configured schedule
4. Handle conversations using AI-powered natural language processing
5. Log all interactions for monitoring and analysis

## Project Structure

```
.
├── agent/
│   ├── phone_agent.py      # Main agent implementation
│   └── conversation_manager.py  # Conversation flow management
├── voice/
│   └── voice_handler.py    # Voice processing and call handling
├── config/
│   ├── agent_config.json   # Agent configuration
│   └── conversation_flows.json  # Conversation flow definitions
├── utils/
│   └── logger.py          # Logging utilities
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for their powerful GPT models
- ElevenLabs for voice synthesis
- Twilio for telephony services
