#!/usr/bin/env python3
"""
Advanced AI-Powered Financial Chatbot for Global Finance Corp (GFC)
Task 2: Enhanced Version with NLP Principles

This chatbot incorporates:
- Rule-based logic with intent matching
- Conversation state management
- Robust error handling
- Accessible financial insight communication
- Interactive dialogue design
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, List, Tuple, Optional

class ConversationState:
    """Manages conversation context and history"""
    def __init__(self):
        self.history = []
        self.current_context = {
            'last_company': None,
            'last_metric': None,
            'last_year': None
        }
        self.user_expertise_level = 'beginner'  # beginner, intermediate, advanced
    
    def add_turn(self, user_input: str, bot_response: str):
        """Add conversation turn to history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'bot': bot_response
        })
    
    def update_context(self, **kwargs):
        """Update conversation context"""
        self.current_context.update(kwargs)
    
    def get_context(self):
        """Get current context"""
        return self.current_context
    
    def infer_expertise(self, user_input: str):
        """Infer user's financial knowledge level"""
        advanced_terms = ['cagr', 'leverage', 'ebitda', 'roi', 'pe ratio', 'debt-to-equity']
        beginner_terms = ['revenue', 'profit', 'money', 'earnings']
        
        user_lower = user_input.lower()
        advanced_count = sum(1 for term in advanced_terms if term in user_lower)
        
        if advanced_count > 0:
            self.user_expertise_level = 'advanced'
        elif any(term in user_lower for term in beginner_terms):
            if self.user_expertise_level == 'beginner':
                self.user_expertise_level = 'intermediate'


class FinancialDataStore:
    """Centralized financial data store"""
    def __init__(self):
        self.data = self.load_financial_data()
        self.companies = self.data['Company'].unique().tolist()
        self.years = sorted(self.data['Year'].unique().tolist())
        self.metrics = ['Total Revenue', 'Net Income', 'Total Assets', 
                       'Total Liabilities', 'Operating Cash Flow']
        self._build_indexes()
    
    def load_financial_data(self):
        """Load financial data"""
        data = {
            'Company': [
                'Microsoft', 'Microsoft', 'Microsoft',
                'Tesla', 'Tesla', 'Tesla',
                'Apple', 'Apple', 'Apple'
            ],
            'Year': [2025, 2024, 2023, 2025, 2024, 2023, 2025, 2024, 2023],
            'Total Revenue': [281724, 245122, 211915, 94827, 97690, 96773, 416161, 391035, 383285],
            'Net Income': [101832, 88136, 72361, 3855, 7153, 14974, 112010, 93736, 96995],
            'Total Assets': [619003, 512163, 411975, 137806, 122070, 82338, 359241, 364980, 352583],
            'Total Liabilities': [275524, 243686, 205753, 54941, 48390, 36440, 285508, 308030, 290437],
            'Operating Cash Flow': [136162, 118548, 87582, 14747, 14923, 13256, 111482, 118254, 110543]
        }
        return pd.DataFrame(data)
    
    def _build_indexes(self):
        """Build efficient data indexes"""
        self.company_index = {c: self.data[self.data['Company'] == c] for c in self.companies}
        self.year_index = {y: self.data[self.data['Year'] == y] for y in self.years}
    
    def get_value(self, company: str, year: int, metric: str) -> Optional[float]:
        """Get specific data value"""
        try:
            result = self.data[
                (self.data['Company'] == company) & 
                (self.data['Year'] == year)
            ][metric].values
            return result[0] if len(result) > 0 else None
        except:
            return None
    
    def get_company_data(self, company: str, year: Optional[int] = None):
        """Get company data with optional year filter"""
        data = self.company_index.get(company)
        if data is None:
            return None
        if year:
            return data[data['Year'] == year]
        return data


class IntentMatcher:
    """Advanced intent matching with confidence scores"""
    def __init__(self):
        self.intent_patterns = {
            'revenue': {
                'keywords': ['revenue', 'sales', 'income from', 'earnings from', 'generated'],
                'examples': ['What was the revenue?', 'How much did they sell?']
            },
            'profit': {
                'keywords': ['profit', 'net income', 'earnings', 'profitable', 'profitability'],
                'examples': ['How profitable is the company?', 'What was net income?']
            },
            'growth': {
                'keywords': ['growth', 'grew', 'increase', 'decline', 'cagr', 'trend', 'growing'],
                'examples': ["Is revenue growing?', 'What's the growth trend?"]
            },
            'comparison': {
                'keywords': ['compare', 'vs', 'versus', 'better', 'which', 'ranking', 'most', 'highest', 'lowest'],
                'examples': ['Which company is bigger?', 'Compare the three companies']
            },
            'health': {
                'keywords': ['health', 'healthy', 'leverage', 'debt', 'risk', 'financial health', 'stability'],
                'examples': ['Is the company financially healthy?', 'What about debt?']
            },
            'efficiency': {
                'keywords': ['efficient', 'efficiency', 'margin', 'margin analysis', 'productivity', 'turnover'],
                'examples': ['How efficient is the company?', 'What about profit margins?']
            },
            'cashflow': {
                'keywords': ['cash', 'cash flow', 'operating cash', 'liquidity', 'cash generation'],
                'examples': ['How much cash does it generate?', 'What about cash flow?']
            },
            'help': {
                'keywords': ['help', 'what can', 'how do', 'guide', 'example', 'question', 'ask'],
                'examples': ['What can I ask?', 'Help me understand']
            }
        }
    
    def match_intent(self, user_input: str) -> Tuple[str, float]:
        """Match user input to intent with confidence score"""
        user_lower = user_input.lower()
        intent_scores = {}
        
        for intent, pattern_data in self.intent_patterns.items():
            score = 0
            keyword_matches = sum(1 for kw in pattern_data['keywords'] if kw in user_lower)
            score += keyword_matches * 0.5
            
            # Bonus for exact phrase match
            for example in pattern_data['examples']:
                if example.lower() in user_lower:
                    score += 2
            
            intent_scores[intent] = score
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent] / max(sum(intent_scores.values()), 1)
        
        return best_intent, min(confidence, 1.0)
    
    def get_suggestions(self, failed_intent: str) -> List[str]:
        """Get helpful suggestions for failed queries"""
        suggestions = []
        for intent, pattern_data in self.intent_patterns.items():
            if intent != failed_intent and intent != 'help':
                suggestions.append(f"Try asking: '{pattern_data['examples'][0]}'")
        return suggestions[:3]


class FinancialChatbot:
    """Advanced Financial Chatbot with all principles implemented"""
    
    def __init__(self):
        self.data_store = FinancialDataStore()
        self.state = ConversationState()
        self.intent_matcher = IntentMatcher()
        self.fallback_responses = [
            "I'm not quite sure about that. Let me help you with something I know well.",
            "That's an interesting question, but I might need more context.",
            "Could you rephrase that? I want to make sure I understand correctly.",
        ]
        self.fallback_index = 0
    
    def simplify_number(self, value: float) -> str:
        """Convert large numbers to readable format"""
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}B"
        elif value >= 1_000:
            return f"${value/1_000:.1f}M"
        else:
            return f"${value:.0f}"
    
    def format_financial_insight(self, insight: Dict, expertise_level: str) -> str:
        """Format financial insight based on user expertise level"""
        if expertise_level == 'beginner':
            # Simple explanation with analogy
            return insight.get('simple', insight.get('full', ''))
        elif expertise_level == 'advanced':
            # Technical details
            return insight.get('technical', insight.get('full', ''))
        else:
            # Balanced explanation
            return insight.get('full', '')
    
    def calculate_and_explain_growth(self, company: str, metric: str = 'Total Revenue') -> Dict:
        """Calculate growth with explanation"""
        val_2025 = self.data_store.get_value(company, 2025, metric)
        val_2024 = self.data_store.get_value(company, 2024, metric)
        
        if not val_2025 or not val_2024:
            return None
        
        growth = ((val_2025 - val_2024) / val_2024) * 100
        direction = "📈 grew" if growth > 0 else "📉 declined"
        emoji = "📈" if growth > 0 else "📉"
        concern = " - This is concerning and requires monitoring." if company == 'Tesla' and growth < 0 else ""
        
        return {
            'simple': f"{company}'s {metric} {direction} by {abs(growth):.1f}% last year.{concern}",
            'full': f"{company}'s {metric} {direction} {abs(growth):.1f}% from {self.simplify_number(val_2024)} (2024) to {self.simplify_number(val_2025)} (2025).{concern}",
            'technical': f"YoY growth rate: {growth:+.2f}% | Absolute change: {self.simplify_number(val_2025 - val_2024)}",
            'value': growth
        }
    
    def handle_revenue_query(self, company: str, year: int = 2025) -> str:
        """Handle revenue-related queries"""
        if company not in self.data_store.companies:
            return f"I don't have data for {company}. I can help with: {', '.join(self.data_store.companies)}"
        
        if year not in self.data_store.years:
            return f"I have data for years: {', '.join(map(str, self.data_store.years))}"
        
        revenue = self.data_store.get_value(company, year, 'Total Revenue')
        
        if self.state.user_expertise_level == 'beginner':
            response = f"{company} made {self.simplify_number(revenue)} in total sales in {year}. "
            response += "That's the money they earned from selling their products and services."
        else:
            response = f"{company}'s total revenue in {year} was {self.simplify_number(revenue)}."
        
        self.state.update_context(last_company=company, last_year=year, last_metric='Total Revenue')
        return response
    
    def handle_profit_query(self, company: str, year: int = 2025) -> str:
        """Handle profitability queries with deeper insights"""
        if company not in self.data_store.companies:
            return f"Could you specify which company? I have data for: {', '.join(self.data_store.companies)}"
        
        net_income = self.data_store.get_value(company, year, 'Net Income')
        revenue = self.data_store.get_value(company, year, 'Total Revenue')
        
        if not net_income or not revenue:
            return f"I don't have complete data for {company} in {year}."
        
        margin = (net_income / revenue) * 100
        
        if self.state.user_expertise_level == 'beginner':
            response = f"In {year}, {company} made {self.simplify_number(net_income)} in profit. "
            response += f"That's {margin:.1f}% of their sales - meaning for every dollar earned, they kept {margin/100:.2f} cents as profit."
        else:
            response = f"{company} {year}: Net Income {self.simplify_number(net_income)} | Profit Margin {margin:.2f}%"
        
        # Add context-aware suggestion
        response += "\n\n💡 Would you like to know how this compares to other companies?"
        
        self.state.update_context(last_company=company, last_year=year, last_metric='Net Income')
        return response
    
    def handle_growth_query(self, company: str) -> str:
        """Handle growth analysis queries"""
        if company not in self.data_store.companies:
            return "Which company would you like to analyze? I can help with: " + ", ".join(self.data_store.companies)
        
        growth_data = self.calculate_and_explain_growth(company, 'Total Revenue')
        
        if not growth_data:
            return f"I couldn't calculate growth for {company}."
        
        response = growth_data[self.state.user_expertise_level]
        
        # Add risk assessment for Tesla
        if company == 'Tesla' and growth_data['value'] < -2:
            response += "\n\n⚠️ Alert: This negative trend combined with profitability concerns (46% net income decline) suggests operational challenges."
        
        return response
    
    def handle_comparison_query(self) -> str:
        """Handle company comparison queries"""
        year = self.state.current_context.get('last_year', 2025)
        
        response = f"**Financial Comparison ({year}):**\n\n"
        
        # Revenue comparison
        year_data = self.data_store.year_index.get(year)
        revenue_ranking = year_data.nlargest(3, 'Total Revenue')[['Company', 'Total Revenue']]
        
        response += "📊 **Revenue Ranking:**\n"
        for idx, (_, row) in enumerate(revenue_ranking.iterrows(), 1):
            response += f"  {idx}. {row['Company']}: {self.simplify_number(row['Total Revenue'])}\n"
        
        response += "\n💰 **Profitability Ranking:**\n"
        profit_ranking = year_data.nlargest(3, 'Net Income')[['Company', 'Net Income']]
        for idx, (_, row) in enumerate(profit_ranking.iterrows(), 1):
            response += f"  {idx}. {row['Company']}: {self.simplify_number(row['Net Income'])}\n"
        
        response += "\n💡 **Key Insight:** Apple leads in total revenue, but Microsoft has better profit margins (36% vs 27%)."
        
        return response
    
    def handle_health_query(self, company: str, year: int = 2025) -> str:
        """Handle financial health queries"""
        if company not in self.data_store.companies:
            return f"Which company? Available: {', '.join(self.data_store.companies)}"
        
        assets = self.data_store.get_value(company, year, 'Total Assets')
        liabilities = self.data_store.get_value(company, year, 'Total Liabilities')
        
        if not assets or not liabilities:
            return "I don't have complete data for that analysis."
        
        equity = assets - liabilities
        de_ratio = liabilities / equity if equity > 0 else float('inf')
        
        if de_ratio < 1:
            health_status = "✓ Excellent - Low leverage"
        elif de_ratio < 5:
            health_status = "⚠️ Moderate - Manageable debt"
        else:
            health_status = "✗ Concerning - High leverage"
        
        response = f"**{company} Financial Health ({year}):**\n"
        response += f"Debt-to-Equity Ratio: {de_ratio:.2f} | Status: {health_status}\n\n"
        
        if self.state.user_expertise_level == 'beginner':
            response += "💡 This ratio shows how much the company relies on borrowing. Lower is better - it means less financial risk."
        else:
            response += f"📊 Equity: {self.simplify_number(equity)} | Liabilities: {self.simplify_number(liabilities)}"
        
        return response
    
    def handle_help_query(self) -> str:
        """Provide interactive help with suggestions"""
        help_text = """
🤖 **Financial Chatbot Help Guide**

I can answer questions about Microsoft, Tesla, and Apple's finances (2023-2025).

📊 **Example Questions:**

*About Revenue:*
  • "What was Apple's revenue in 2025?"
  • "How much did Microsoft sell last year?"
  
*About Profitability:*
  • "Is Tesla profitable?"
  • "What's Apple's profit margin?"

*About Growth:*
  • "Is Microsoft's revenue growing?"
  • "Show me Tesla's growth trend"

*About Financial Health:*
  • "How healthy is Apple financially?"
  • "Which company has the best balance sheet?"

*Comparisons:*
  • "Which company is most profitable?"
  • "Compare the three companies"

**💡 Tip:** I'll adjust my explanations based on your questions. Ask about financial details and I'll use more technical language!

Ask away! 🎯
"""
        return help_text
    
    def handle_unknown_query(self, user_input: str, intent: str, confidence: float) -> str:
        """Handle queries the chatbot can't understand"""
        if confidence < 0.3:
            suggestions = self.intent_matcher.get_suggestions(intent)
            response = "I'm not sure I understood that correctly. "
            response += "Here are some things I can help with:\n"
            for suggestion in suggestions:
                response += f"• {suggestion}\n"
            response += "\nOr type 'help' to see all options!"
        else:
            response = self.fallback_responses[self.fallback_index]
            self.fallback_index = (self.fallback_index + 1) % len(self.fallback_responses)
        
        return response
    
    def extract_entities(self, user_input: str) -> Dict:
        """Extract companies, years, and metrics from user input"""
        entities = {
            'company': self.state.current_context.get('last_company'),
            'year': self.state.current_context.get('last_year', 2025),
            'metric': self.state.current_context.get('last_metric', 'Total Revenue')
        }
        
        user_lower = user_input.lower()
        
        # Extract company
        for company in self.data_store.companies:
            if company.lower() in user_lower:
                entities['company'] = company
                break
        
        # Extract year
        for year in self.data_store.years:
            if str(year) in user_input:
                entities['year'] = year
                break
        
        # Extract metric
        for metric in self.data_store.metrics:
            if metric.lower() in user_lower:
                entities['metric'] = metric
                break
        
        return entities
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        if not user_input.strip():
            return "I'm here to help! Ask me about Microsoft, Tesla, or Apple's finances. Type 'help' for examples."
        
        # Infer expertise level
        self.state.infer_expertise(user_input)
        
        # Match intent
        intent, confidence = self.intent_matcher.match_intent(user_input)
        
        # Extract entities
        entities = self.extract_entities(user_input)
        
        # Route to appropriate handler
        if intent == 'help':
            response = self.handle_help_query()
        
        elif intent == 'comparison':
            response = self.handle_comparison_query()
        
        elif intent == 'health':
            company = entities['company']
            if company:
                response = self.handle_health_query(company, entities['year'])
            else:
                response = "Which company would you like me to analyze?"
        
        elif intent == 'profit' or intent == 'efficiency':
            company = entities['company']
            if company:
                response = self.handle_profit_query(company, entities['year'])
            else:
                response = "Which company's profitability interests you? (Microsoft, Tesla, or Apple)"
        
        elif intent == 'growth':
            company = entities['company']
            if company:
                response = self.handle_growth_query(company)
            else:
                response = "Which company's growth would you like to explore?"
        
        elif intent == 'revenue' or intent == 'cashflow':
            company = entities['company']
            if company:
                response = self.handle_revenue_query(company, entities['year'])
            else:
                response = "Which company would you like to know about?"
        
        else:
            response = self.handle_unknown_query(user_input, intent, confidence)
        
        # Add conversation turn to history
        self.state.add_turn(user_input, response)
        
        return response
    
    def run(self):
        """Run chatbot in interactive mode"""
        print("\n" + "="*70)
        print("🤖 ADVANCED FINANCIAL CHATBOT - Global Finance Corp")
        print("="*70)
        print("\nWelcome! Ask me about financial data for Microsoft, Tesla, and Apple.")
        print("Type 'quit' to exit, or 'help' for examples.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using the Financial Chatbot! Goodbye!\n")
                    break
                
                if not user_input:
                    continue
                
                response = self.process_input(user_input)
                print(f"\nChatbot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session ended. Goodbye!\n")
                break
            except Exception as e:
                print(f"\nChatbot: An error occurred. Please try again.\n")


def main():
    """Main entry point"""
    chatbot = FinancialChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
