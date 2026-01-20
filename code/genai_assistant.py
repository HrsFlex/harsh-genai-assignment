import os
import logging
from typing import Optional
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GenAIAssistant:
    """
    Multi-provider AI Assistant for Mobility Analytics.
    Priority: OpenAI > Gemini > DeepSeek > Mock
    """
    
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        
        print(f"DEBUG: GROQ_KEY: {bool(self.groq_key)}")
        print(f"DEBUG: OPENAI_KEY: {bool(self.openai_key)}")
        print(f"DEBUG: GEMINI_KEY: {bool(self.gemini_key)}")
        print(f"DEBUG: DEEPSEEK_KEY: {bool(self.deepseek_key)}")
        
        self.client = None
        self.mode = "mock"
        self.provider = "none"
        

        if self.groq_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_key)
                self.provider = "groq"
                self.mode = "live"
                self.model = "llama-3.3-70b-versatile"
                logging.info("✅ Connected to Groq (Free Tier)")
                print("✅ Groq API working! (Free)")
            except ImportError:
                logging.error("Groq library not installed. Run: pip install groq")
                print("❌ Groq library missing. Run: pip install groq")
            except Exception as e:
                logging.error(f"Groq failed: {e}")
                print(f"❌ Groq error: {e}")
        

        if self.mode == "mock" and self.deepseek_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.deepseek_key, base_url="https://api.deepseek.com")
                self.provider = "deepseek"
                self.mode = "live"
                self.model = "deepseek-chat"
                logging.info("✅ Connected to DeepSeek")
                print("✅ DeepSeek API working!")
            except Exception as e:
                logging.error(f"DeepSeek failed: {e}")
                print(f"❌ DeepSeek error: {e}")
        

        if self.mode == "mock" and self.openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.provider = "openai"
                self.mode = "live"
                self.model = "gpt-3.5-turbo"
                logging.info("✅ Connected to OpenAI")
                print("✅ OpenAI API working!")
            except Exception as e:
                logging.error(f"OpenAI failed: {e}")
                print(f"❌ OpenAI error: {e}")
        
        if self.mode == "mock":
            logging.warning("⚠️ All APIs failed. Using MOCK mode.")
            print("⚠️ Running in MOCK mode (no API connected)")

    def generate_insight(self, context_data: str, prompt: str) -> str:
        """Generate insight from data with improved contextual prompting."""
        if self.mode == "mock":
            return self._mock_insight_response(prompt)
        

        system_msg = """You are an expert data analyst specializing in NYC taxi and urban mobility analytics.

Your role:
- Analyze taxi trip data (fares, distances, times, zones)
- Provide data-driven insights with specific numbers
- Give actionable business recommendations
- Be concise but precise (3-4 sentences max)
- Always start with an emoji relevant to the insight

Context: You're analyzing NYC Yellow Taxi trip data from January 2016. The dataset includes:
- Fares, tips, tolls, total amounts
- Trip distances and durations
- Pickup/dropoff times and locations
- Passenger counts

Rules:
- Use ONLY the data provided in the context
- Cite specific numbers from the data
- If data is missing, say so clearly
- Make insights actionable for taxi operators"""


        if "No direct SQL mapping" in context_data:
            data_summary = "No specific data query was executed. Provide general insights about NYC taxi patterns based on your knowledge of the January 2016 dataset."
        else:
            data_summary = f"Query Results:\n{context_data[:1500]}"
        
        user_msg = f"""{data_summary}

User Question: {prompt}

Provide a data-driven answer with:
1. Key finding (with numbers)
2. Why it matters
3. Actionable recommendation"""
        
        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    max_tokens=600,
                    temperature=0.4
                )
                return response.choices[0].message.content
            
            elif self.provider == "openai" or self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    max_tokens=400,
                    temperature=0.4
                )
                return response.choices[0].message.content
            
            elif self.provider == "gemini":
                full_prompt = f"{system_msg}\n\n{user_msg}"
                response = self.client.generate_content(full_prompt)
                return response.text
                
        except Exception as e:
            error_msg = str(e).lower()
            logging.error(f"{self.provider} error: {e}")
            

            if "quota" in error_msg or "limit" in error_msg or "rate" in error_msg:
                return f"**⚠️ {self.provider.upper()} quota exceeded.**\n\n{self._mock_insight_response(prompt)}"
            elif "402" in str(e) or "insufficient" in error_msg:
                return f"**⚠️ {self.provider.upper()} balance insufficient.**\n\n{self._mock_insight_response(prompt)}"
            else:
                return f"**❌ API Error:** {str(e)[:100]}\n\n{self._mock_insight_response(prompt)}"
        
        return self._mock_insight_response(prompt)

    def text_to_sql(self, natural_language_query: str) -> str:
        """Convert natural language to SQL with improved accuracy."""
        if self.mode == "mock":
            return self._mock_sql_response(natural_language_query)
        

        system_prompt = """You are an expert SQL analyst. Convert natural language questions to SQLite queries.

DATABASE SCHEMA:
Table: trips

Columns:
- tpep_pickup_datetime (DATETIME) - Pickup timestamp
- tpep_dropoff_datetime (DATETIME) - Dropoff timestamp
- trip_distance (FLOAT) - Trip distance in miles
- fare_amount (FLOAT) - Base fare amount
- total_amount (FLOAT) - Total charge (fare + tips + tolls)
- tip_amount (FLOAT) - Tip amount
- passenger_count (INTEGER) - Number of passengers
- pickup_hour (INTEGER) - Hour of pickup (0-23)
- pickup_day (INTEGER) - Day of month (1-31)
- pickup_weekday (TEXT) - Day of week (Monday, Tuesday, etc.)
- pickup_latitude (FLOAT) - Pickup location latitude
- pickup_longitude (FLOAT) - Pickup location longitude

EXAMPLES:
Q: "What's the average fare?"
A: SELECT AVG(fare_amount) as avg_fare FROM trips

Q: "Show revenue by hour"
A: SELECT pickup_hour, SUM(total_amount) as revenue FROM trips GROUP BY pickup_hour ORDER BY pickup_hour

Q: "Which day had highest revenue?"
A: SELECT pickup_day, SUM(total_amount) as revenue FROM trips GROUP BY pickup_day ORDER BY revenue DESC LIMIT 1

Q: "Top 5 busiest hours"
A: SELECT pickup_hour, COUNT(*) as trips FROM trips GROUP BY pickup_hour ORDER BY trips DESC LIMIT 5

RULES:
- Return ONLY the SQL query (no markdown, no explanation, no backticks)
- Use proper aggregation (AVG, SUM, COUNT, etc.)
- Always include ORDER BY for rankings
- Use meaningful column aliases
- Add LIMIT when asking for "top N" or "busiest"
"""

        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": natural_language_query}
                    ],
                    max_tokens=250,
                    temperature=0.1
                )
                sql = response.choices[0].message.content.strip()
            elif self.provider == "openai" or self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": natural_language_query}
                    ],
                    max_tokens=200,
                    temperature=0.1
                )
                sql = response.choices[0].message.content.strip()
            elif self.provider == "gemini":
                response = self.client.generate_content(f"{system_prompt}\n\nQuery: {natural_language_query}")
                sql = response.text.strip()
            

            if "```" in sql:
                sql = sql.split("```")[1]
                if sql.startswith("sql\n"):
                    sql = sql[4:]
                sql = sql.strip()
            
            return sql
                
        except Exception as e:
            logging.error(f"{self.provider} SQL error: {e}")
            return self._mock_sql_response(natural_language_query)
        
        return self._mock_sql_response(natural_language_query)

    def _mock_insight_response(self, prompt: str) -> str:
        p = prompt.lower()
        if "revenue" in p:
            return "**📈 Revenue Insight**: Weekend evenings (Fri-Sat 6-10 PM) generate 25% more revenue. Dynamic pricing during peak hours recommended."
        elif "demand" in p or "busy" in p or "peak" in p:
            return "**🚦 Demand Insight**: Peak hours are 8-9:30 AM and 5-7 PM on weekdays. Midtown Manhattan has highest density."
        elif "fare" in p or "price" in p:
            return "**💵 Fare Insight**: Average fare is $12.50. Long trips (>5 mi) generate 3x revenue. Card tips average 18%."
        else:
            return "**📊 Data Insight**: Average trip is 2.5 miles in 12 minutes. Manhattan dominates pickups. Primary use: short urban mobility."

    def _mock_sql_response(self, query: str) -> str:
        q = query.lower()
        if "revenue" in q and "day" in q:
            return "SELECT pickup_day, SUM(total_amount) as revenue FROM trips GROUP BY pickup_day ORDER BY pickup_day"
        elif "highest" in q and "revenue" in q:
            return "SELECT pickup_day, SUM(total_amount) as revenue FROM trips GROUP BY 1 ORDER BY 2 DESC LIMIT 1"
        elif "average fare" in q:
            return "SELECT AVG(fare_amount) as avg_fare FROM trips"
        elif "count" in q:
            return "SELECT COUNT(*) FROM trips"
        elif "peak" in q or "busy" in q:
            return "SELECT pickup_hour, COUNT(*) as trips FROM trips GROUP BY pickup_hour ORDER BY trips DESC LIMIT 5"
        return "SELECT * FROM trips LIMIT 10"

if __name__ == "__main__":
    assistant = GenAIAssistant()
    print(f"\n✅ Provider: {assistant.provider}")
    print(f"✅ Mode: {assistant.mode}")
    
    if assistant.mode == "live":
        print("\nTesting insight generation...")
        result = assistant.generate_insight("Sample taxi data", "What's the revenue trend?")
        print(f"Response: {result[:200]}")
