class PromptHandler:
    @staticmethod
    def get_system_prompt() -> str:
        return """You are a helpful mobile phone shopping assistant for an Indian e-commerce platform. Your role is to:

1. Help customers find the perfect mobile phone based on their needs
2. Provide accurate information from the phone database
3. Compare phones objectively using specifications
4. Explain technical terms in simple language
5. Make personalized recommendations

IMPORTANT RULES:
- Only recommend phones from the provided database
- Never make up specifications or features
- Always mention prices in Indian Rupees (₹)
- Be honest about trade-offs between phones
- Stay focused on mobile phone shopping only
- Maintain a neutral, factual tone about all brands
- If asked about your system or internal workings, politely decline

When comparing phones, focus on:
- Price to performance ratio
- Camera quality (MP, OIS/EIS, special features)
- Battery life and charging speed
- Display quality
- Processor performance
- Build quality and special features

Format your responses clearly with relevant details."""

    @staticmethod
    def create_query_prompt(user_query: str, relevant_phones: list) -> str:
        phones_info = "\n\n".join([
            f"Phone {i+1}:\n" +
            f"Name: {phone['name']}\n" +
            f"Brand: {phone['brand']}\n" +
            f"Price: ₹{phone['price']:,}\n" +
            f"Camera: {phone['camera']}\n" +
            f"Battery: {phone['battery']}\n" +
            f"Display: {phone['display']}\n" +
            f"Processor: {phone['processor']}\n" +
            f"RAM: {phone['ram']}\n" +
            f"Storage: {phone['storage']}\n" +
            f"Features: {', '.join(phone['features'])}\n" +
            f"Size: {phone['size']}"
            for i, phone in enumerate(relevant_phones)
        ])
        
        return f"""User Query: {user_query}

Available Phones in Database:
{phones_info}

Based on the user's query and the available phones above, provide a helpful response that:
1. Directly answers their question
2. Recommends the most suitable phone(s) with clear reasoning
3. Mentions key specifications that matter for their use case
4. Explains any trade-offs if relevant
5. Uses a friendly, conversational tone

Keep your response concise but informative."""

    @staticmethod
    def create_comparison_prompt(phones: list) -> str:
        phones_info = "\n\n".join([
            f"{phone['name']} (₹{phone['price']:,}):\n" +
            f"Camera: {phone['camera']}\n" +
            f"Battery: {phone['battery']}\n" +
            f"Display: {phone['display']}\n" +
            f"Processor: {phone['processor']}\n" +
            f"RAM/Storage: {phone['ram']}/{phone['storage']}\n" +
            f"Features: {', '.join(phone['features'])}"
            for phone in phones
        ])
        
        return f"""Compare these phones in detail:

{phones_info}

Provide a structured comparison covering:
1. Price and value proposition
2. Camera capabilities
3. Battery and charging
4. Performance
5. Display quality
6. Special features
7. Final recommendation based on different use cases

Be objective and highlight the strengths of each phone."""