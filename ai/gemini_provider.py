import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_recommendation(row):

    prompt = f"""
You are an expert SEO consultant.

Analyze this SEO opportunity.

Page:
{row['page']}

Query:
{row['query']}

Impressions:
{row['impressions']}

CTR:
{row['ctr']}

Average Position:
{row['position']}

Intent:
{row['Intent']}

Opportunity Score:
{row['Opportunity Score']}

Provide:

1. Why this page is an opportunity.
2. Best optimization strategy.
3. Suggested SEO page title.
4. Suggested meta description.
5. Expected business impact.

Keep your response under 180 words.
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )

    return response.text