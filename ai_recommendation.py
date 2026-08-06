import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_recommendation(row):

    prompt = f"""
You are a senior SEO consultant working at FlyRank.

Analyze the following SEO opportunity and provide practical recommendations.

SEO DATA

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

Search Intent:
{row['Intent']}

Opportunity Score:
{row['Opportunity Score']:.2f}

Provide the following:

1. Why this page is an opportunity.
2. What SEO improvements should be made.
3. Suggest a better SEO page title.
4. Suggest a meta description (under 160 characters).
5. Estimate the expected business impact.

Keep the response under 180 words.
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )

    return response.text