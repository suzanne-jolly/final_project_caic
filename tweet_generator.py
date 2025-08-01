import random

class SimpleTweetGenerator:
    def __init__(self):
        self.positive_templates = [
            "{company} is making waves in {industry}! 🚀 {message}",
            "Big news from {company} today in {industry}: {message}"
        ]
        self.negative_templates = [
            "Rough patch for {company} in {industry} sector.{message} 😟",
            "{company} is facing criticism in the {industry} space.{message}"
        ]
        self.neutral_templates = [
            "{company} shares updates on {industry}.{message}",
            "Steady progress from {company} in {industry}.{message}"
        ]

    def generate_smart_tweet(self, company, industry, word_count, sentiment_target, has_media, message):
        
        if sentiment_target > 0.5:
            templates = self.positive_templates
        elif sentiment_target < -0.5:
            templates = self.negative_templates
        else:
            templates = self.neutral_templates

        
        base_tweet = random.choice(templates).format(company=company, industry=industry, message= message)
        words = base_tweet.split()

      
        tweet = " ".join(words)

       
        if has_media:
            tweet += " 📸"

        return tweet[:280] 
