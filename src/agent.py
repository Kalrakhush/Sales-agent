import google.generativeai as genai
from config import Config
from database import PhoneDatabase
from safety_filter import SafetyFilter
from prompt_handler import PromptHandler


class ShoppingAgent:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)

        # Init helpers
        self.db = PhoneDatabase()
        self.safety = SafetyFilter()
        self.prompt_handler = PromptHandler()
        self.conversation_history = []

    def chat(self, user_query: str) -> tuple[str, list]:
        """Main chat method (LLM-driven, no manual intent logic)"""
        print(f"\n🧠 Received query: {user_query}")

        # Safety check
        is_safe, reason = self.safety.is_safe_query(user_query)
        if not is_safe:
            print("⚠️ Unsafe query blocked.")
            return reason, []

        # Save query
        self.conversation_history.append({"role": "user", "content": user_query})

        # Load database phones (LLM decides relevance)
        all_phones = self.db.get_all_phones()

        # Build prompt
        prompt = self.prompt_handler.create_query_prompt(user_query, all_phones)
        full_prompt = self.prompt_handler.get_system_prompt() + "\n\n" + prompt

        try:
            print("🤖 Sending request to Gemini...")
            response = self.model.generate_content(full_prompt)
            response_text = ""

            # ✅ Safely extract Gemini output (different SDK versions vary)
            if hasattr(response, "text") and response.text:
                response_text = response.text.strip()
            elif hasattr(response, "candidates") and len(response.candidates) > 0:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    response_text = parts[0].text.strip()

            if not response_text:
                response_text = "I couldn’t generate a valid response. Please try again."

            print("✅ Gemini response received successfully.")
            print("📝 Response Preview:\n", response_text[:500], "..." if len(response_text) > 500 else "")

            # Save assistant response
            self.conversation_history.append({"role": "assistant", "content": response_text})

            # Return clean output
            return self.safety.sanitize_output(response_text)

        except Exception as e:
            print(f"❌ LLM Runtime Error: {e}")
            error_msg = (
                "I apologize, but I encountered an error while processing your request. "
                "Please try again or rephrase your question."
            )
            return error_msg, all_phones
