from config import Config

class SafetyFilter:
    def __init__(self):
        self.blocked_keywords = Config.BLOCKED_KEYWORDS
    
    def is_safe_query(self, query: str) -> tuple[bool, str]:
        """Check if query is safe. Returns (is_safe, reason)"""
        
        query_lower = query.lower()
        
        # Check for adversarial prompts
        for keyword in self.blocked_keywords:
            if keyword in query_lower:
                return False, "I'm here to help you find the perfect mobile phone. I cannot respond to requests about my internal workings or system configuration."
        
        # Check for attempts to reveal API keys
        if any(word in query_lower for word in ['api', 'key', 'token', 'password', 'secret']):
            return False, "I cannot share any system credentials or configuration details. How can I help you find a mobile phone?"
        
        # Check for toxic/defamatory content
        toxic_words = ['trash', 'garbage', 'worst', 'terrible', 'hate', 'stupid']
        if any(word in query_lower for word in toxic_words) and any(brand in query_lower for brand in ['samsung', 'apple', 'xiaomi', 'oneplus', 'google']):
            return False, "I maintain a neutral, factual stance on all brands. I'd be happy to provide objective comparisons based on specifications and features."
        
        # Check if query is about phones
        phone_keywords = ['phone', 'mobile', 'smartphone', 'device', 'camera', 'battery', 
                         'display', 'processor', 'ram', 'storage', 'charging', 'brand',
                         'samsung', 'apple', 'xiaomi', 'oneplus', 'google', 'pixel',
                         'iphone', 'galaxy', 'redmi', 'poco', 'realme', 'vivo', 'oppo',
                         'ois', 'eis', 'amoled', 'oled', 'price', 'budget', 'compare',
                         'recommend', 'best', 'cheap', 'flagship', 'gaming']
        
        if not any(keyword in query_lower for keyword in phone_keywords):
            return False, "I specialize in helping you find mobile phones. Please ask me about phone recommendations, comparisons, or specifications."
        
        return True, ""
    
    def sanitize_output(self, output: str) -> str:
        """Remove any potential sensitive information from output"""
        # Remove any accidental API key patterns
        import re
        output = re.sub(r'[A-Za-z0-9]{32,}', '[REDACTED]', output)
        return output