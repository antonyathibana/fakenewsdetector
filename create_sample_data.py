"""
Generate Sample Fake and Real News Datasets
This script creates proper CSV files with title, text, subject, and date columns.
The format matches the Kaggle Fake and Real News dataset.
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Project root
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'

# Sample news data
FAKE_NEWS_TITLES = [
    "BREAKING: Scientists Discover New Planet That Shouldn't Exist",
    "SHOCKING: Government Hiding Alien Contact Evidence",
    "EXPOSED: Big Pharma's Secret Cure for Cancer Revealed",
    "INCREDIBLE: Woman Lives Without Food for 300 Days",
    "WARNING: Your Food Is Being Poisoned By...",
    "MUST SEE: Celebrity Caught in Massive Scandal",
    "UNBELIEVABLE: Scientists Say Earth Is Actually Flat",
    "SECRET: What They Don't Want You To Know About 5G",
    "AMAZING: This One Trick Will Make You Rich",
    "ALERT: Nuclear War Starting Next Week",
    "SCANDAL: Politician Involved in Massive Fraud",
    "REVEALED: The Truth About the Moon Landing",
    "SHOCKER: Technology That Can Read Your Mind",
    "WARNING: Massive Earthquake Coming This Month",
    "SECRET: Underground Cities Discovered",
    "INCREDIBLE: New Energy Source Could Replace Oil",
    "MUST READ: What Happened to This Family Will Shock You",
    "EXPOSED: Media Lying About This Important Story",
    "UNBELIEVABLE: Man Claims to Be Time Traveler",
    "ALERT: New Disease spreading Across the World"
]

FAKE_NEWS_TEXTS = [
    """In a shocking development that has left the scientific community baffled, researchers at an unnamed 
    institute have discovered a new planet in our solar system that according to all known physics 
    shouldn't exist. The planet appears to be made entirely of dark matter and emits no light whatsoever.

    Experts are struggling to explain how such a celestial body could have formed without being 
    detected until now. Some are calling this the most significant astronomical discovery in history.

    The discovery was made using a new type of telescope that can detect dark matter emissions. 
    Government officials have refused to comment on whether they knew about this discovery beforehand.

    Sources close to the research team say that the planet's orbit suggests it may have been placed 
    there artificially. This has led to speculation about intelligent design or even alien involvement.

    More details will be revealed in the upcoming documentary 'The Planet That Shouldn't Exist' 
    airing next week on alternative media channels.""",
    
    """Whistleblowers have come forward with explosive allegations that the government has been 
    hiding evidence of alien contact for decades. Documents obtained by investigative journalists 
    show that multiple UFO sightings have been confirmed as extraterrestrial craft.

    The documents reveal that at least 15 separate contact events have occurred since 1947, 
    with the most recent happening just last month. Despite this, government officials continue 
    to deny any knowledge of extraterrestrial life.

    Former military personnel have sworn under oath that they were present during alien encounters 
    and were ordered to keep silent. Many of these witnesses are now coming forward before they die.

    Experts believe this could be the biggest story in human history if verified. The implications 
    would be profound for religion, science, and human understanding of our place in the universe.

    The government has yet to respond to these allegations.""",
    
    """A revolutionary new treatment for cancer has been discovered but is being suppressed by 
    pharmaceutical companies who profit from expensive chemotherapy treatments. The treatment, 
    derived from a rare plant found only in the Amazon rainforest, has shown 100% effectiveness 
    in early trials.

    Big Pharma allegedly paid researchers to falsify results and bury the discovery. Sources 
    inside the pharmaceutical industry confirm that potential cures are regularly suppressed 
    to protect market profits.

    The treatment consists of a simple compound that can be synthesized for less than $10 per dose. 
    Pharmaceutical companies would lose billions if this treatment were to become widely available.

    Several patients who have tried the treatment report complete remission with no side effects. 
    They are now fighting to make the treatment available to others.

    The FDA has refused to comment on why this treatment has not been fast-tracked for approval.""",
    
    """A woman in a remote village has stunned medical experts by claiming to have lived without 
    food for 300 days. Doctors who examined her say they cannot explain how she is still alive.

    The woman says she survives on water and 'universal energy' that she absorbs through meditation. 
    Scientists are baffled but cannot find any evidence of deception.

    If verified, this would completely revolutionize our understanding of human biology and nutrition. 
    The implications for solving world hunger would be enormous.

    Skeptics say this is likely another hoax, but the woman's doctors insist all tests show she is 
    in perfect health despite consuming no food.

    More tests are planned to verify this extraordinary claim.""",
    
    """Sources inside the food industry have revealed that major corporations have been knowingly 
    adding harmful chemicals to common food products. These additives are hidden under confusing 
    names that consumers cannot understand.

    The chemicals have been linked to cancer, obesity, and various other health problems. Despite 
    this, the FDA continues to allow their use in food products.

    Internal documents show that company executives were aware of the health risks but chose to 
    prioritize profits over consumer safety.

    Consumers are advised to avoid any food products containing ingredients you cannot pronounce. 
    Organic and locally sourced foods are the safest option.

    Class action lawsuits are being prepared against the companies involved."""
]

REAL_NEWS_TITLES = [
    "Federal Reserve Announces Interest Rate Decision",
    "Tech Companies Report Quarterly Earnings",
    "Climate Summit Reaches Agreement on Emissions",
    "New Study Shows Benefits of Exercise",
    "Stock Market Closes Higher Today",
    "Scientists Discover New Species in Ocean",
    "Economic Report Shows Job Growth",
    "Health Officials Recommend Vaccination",
    "International Trade Agreement Signed",
    "Technology Conference Highlights AI Advances",
    "Weather Service Issues Winter Storm Warning",
    "Researchers Publish Findings on Renewable Energy",
    "Central Bank Updates Economic Forecast",
    "Education Department Announces Policy Changes",
    "Sports Team Wins Championship Title",
    "Local Community Holds Charity Event",
    "City Council Approves New Infrastructure Project",
    "Medical Researchers Report Breakthrough",
    "Transportation Department Reports on Safety",
    "Environmental Agency Releases Study Results"
]

REAL_NEWS_TEXTS = [
    """The Federal Reserve announced its latest interest rate decision today, maintaining the 
    current rate amid ongoing discussions about inflation and economic growth. Fed Chair stated 
    that the decision reflects careful consideration of current economic conditions.

    Analysts had mixed predictions about potential rate changes. The decision to hold steady 
    comes after months of rate increases aimed at combating inflation.

    The Fed's statement emphasized commitment to achieving maximum employment while maintaining 
    price stability. Markets reacted with modest gains following the announcement.

    Economic indicators suggest inflation is gradually cooling, though it remains above the 
    Fed's 2% target. Officials will continue monitoring data before making future decisions.

    The next Fed meeting is scheduled for next month when officials will review updated 
    economic projections.""",
    
    """Major technology companies reported their quarterly earnings this week, showing varied 
    results across the sector. While some companies exceeded expectations, others faced 
    challenges in the current economic environment.

    Revenue growth was driven by cloud computing and artificial intelligence services. 
    Companies that invested early in AI technologies reported particularly strong performance.

    Stock prices fluctuated in response to the earnings reports. Some analysts remain 
    optimistic about the sector's long-term prospects despite short-term volatility.

    Employment in the technology sector continued to grow, with companies adding thousands 
    of new positions. However, some firms announced layoffs amid restructuring efforts.

    Industry experts predict continued growth in technology spending, particularly in 
    enterprise solutions and digital transformation initiatives.""",
    
    """World leaders at the international climate summit announced a new agreement to reduce 
    carbon emissions. The deal includes commitments from major economies to transition to 
    renewable energy sources.

    The agreement sets ambitious targets for reducing greenhouse gas emissions over the 
    next decade. Environmental advocates called it an important step forward though 
    more action is needed.

    Participating countries agreed to increase adaptation funding for climate and 
    mitigation efforts. Financial commitments total billions of dollars over the 
    implementation period.

    Scientists have emphasized the importance of immediate action to address climate change. 
    The agreement includes provisions for regular progress reviews and accountability measures.

    Critics argue the commitments don't go far enough, while supporters say it represents 
    meaningful progress in international cooperation on climate issues.""",
    
    """A comprehensive study published in a leading medical journal confirms the numerous 
    health benefits of regular exercise. Researchers followed thousands of participants 
    over several decades to reach their conclusions.

    The study found that regular physical activity significantly reduces the risk of 
    heart disease, diabetes, and certain cancers. Even moderate exercise provided 
    substantial health benefits.

    Experts recommend at least 150 minutes of moderate aerobic activity per week, 
    combined with strength training exercises. The benefits extend beyond physical 
    health to include improved mental wellbeing.

    The research highlights the importance of incorporating physical activity into 
    daily routines. Simple changes like walking more and taking stairs can make 
    a significant difference in overall health.

    Health officials are using these findings to update exercise recommendations 
    and promote public health initiatives.""",
    
    """The stock market closed higher today, driven by positive economic data and 
    corporate earnings reports. The major indices posted gains of more than 1%.

    Technology and financial sectors led the advance. Investors responded favorably 
    to news of strong job growth and easing inflation concerns.

    Trading volume was above average as market participants adjusted positions ahead 
    of the weekend. Options expiration contributed to increased activity.

    Bond yields remained stable, providing support for equity valuations. The 
    yield curve showed slight steepening in response to economic data.

    Analysts suggest market sentiment remains cautiously optimistic despite ongoing 
    concerns about economic headwinds. Earnings season continues next week with 
    more major companies reporting results."""
]


def generate_date():
    """Generate a random date within the past 2 years"""
    start_date = datetime.now() - timedelta(days=730)
    random_days = random.randint(0, 730)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


def create_fake_news_dataset(num_samples=500):
    """Create Fake.csv dataset"""
    data = []
    for i in range(num_samples):
        title = random.choice(FAKE_NEWS_TITLES)
        text = random.choice(FAKE_NEWS_TEXTS)
        # Add some variation
        text = f"{title}. {text}" if i % 3 == 0 else text
        
        data.append({
            'title': title,
            'text': text,
            'subject': random.choice(['news', 'politics', 'world news', 'US news']),
            'date': generate_date()
        })
    
    df = pd.DataFrame(data)
    return df


def create_true_news_dataset(num_samples=500):
    """Create True.csv dataset"""
    data = []
    for i in range(num_samples):
        title = random.choice(REAL_NEWS_TITLES)
        text = random.choice(REAL_NEWS_TEXTS)
        # Add some variation
        text = f"{title}. {text}" if i % 3 == 0 else text
        
        data.append({
            'title': title,
            'text': text,
            'subject': random.choice(['politics', 'world', 'business', 'technology']),
            'date': generate_date()
        })
    
    df = pd.DataFrame(data)
    return df


def main():
    print("=" * 60)
    print("📊 Generating Sample News Datasets")
    print("=" * 60)
    
    # Create datasets
    print("\n📝 Creating Fake news dataset...")
    fake_df = create_fake_news_dataset(500)
    fake_path = DATA_DIR / 'Fake.csv'
    fake_df.to_csv(fake_path, index=False)
    print(f"   ✓ Saved: {fake_path} ({len(fake_df)} samples)")
    
    print("\n📝 Creating True news dataset...")
    true_df = create_true_news_dataset(500)
    true_path = DATA_DIR / 'True.csv'
    true_df.to_csv(true_path, index=False)
    print(f"   ✓ Saved: {true_path} ({len(true_df)} samples)")
    
    print("\n" + "=" * 60)
    print("✅ Dataset Generation Complete!")
    print("=" * 60)
    
    # Verify datasets
    print("\n🔍 Verifying datasets...")
    print(f"\nFake.csv columns: {list(fake_df.columns)}")
    print(f"True.csv columns: {list(true_df.columns)}")
    print(f"\nSample Fake.csv entry:")
    print(f"  Title: {fake_df.iloc[0]['title']}")
    print(f"  Subject: {fake_df.iloc[0]['subject']}")
    print(f"  Date: {fake_df.iloc[0]['date']}")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Run: python train_model.py")
    print("2. Run: python app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

