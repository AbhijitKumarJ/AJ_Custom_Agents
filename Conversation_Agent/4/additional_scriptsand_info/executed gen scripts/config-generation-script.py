import os
import json

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_json_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created file: {path}")

def create_config_files():
    config_dir = "aj_mas/config"
    create_directory(config_dir)

    # Main configuration
    config = {
        "system_name": "AJ_MAS",
        "version": "1.0.0",
        "log_level": "INFO",
        "max_concurrent_agents": 5,
        "default_model_provider": "ollama",
        "document_store": {
            "type": "fasttext_chroma",
            "storage_dir": "aj_mas/document_storage",
            "fasttext_model": "cc.en.300.bin"
        },
        "api_rate_limit": 100,
        "session_timeout": 3600
    }
    write_json_file(os.path.join(config_dir, "config.json"), config)

    # Agent configuration
    agent_config = {
        "travel_agent": {
            "name": "Alex Johnson",
            "gender": "Non-binary",
            "ethnicity": "Mixed Asian-European",
            "religious_inclination": "Agnostic",
            "skill_proficiencies": {
                "TRAVEL": 0.95,
                "ENTERTAINMENT": 0.7,
                "CULTURE": 0.8
            },
            "tool_proficiencies": {
                "FlightBookingTool": 0.95,
                "HotelRecommendationTool": 0.9,
                "ItineraryPlanningTool": 0.95
            },
            "language_proficiencies": {
                "English": "NATIVE",
                "Spanish": "ADVANCED",
                "French": "INTERMEDIATE"
            },
            "personality_traits": ["Enthusiastic", "Detail-oriented"],
            "communication_style": "Friendly and professional"
        },
        "financial_advisor": {
            "name": "Morgan Lee",
            "gender": "Female",
            "ethnicity": "African American",
            "religious_inclination": "Christian",
            "skill_proficiencies": {
                "FINANCE": 0.95,
                "BUSINESS": 0.85,
                "MATHEMATICS": 0.8
            },
            "tool_proficiencies": {
                "InvestmentAnalysisTool": 0.95,
                "TaxPlanningTool": 0.9,
                "RetirementPlanningTool": 0.95
            },
            "language_proficiencies": {
                "English": "NATIVE"
            },
            "personality_traits": ["Analytical", "Patient"],
            "communication_style": "Clear and reassuring"
        }
        # Add more agent configurations as needed
    }
    write_json_file(os.path.join(config_dir, "agent_config.json"), agent_config)

    # Skill configuration
    skill_config = {
        "travel": {
            "ItineraryPlanningSkill": {
                "enabled": True,
                "max_days": 30,
                "default_budget": 1000
            },
            "HotelRecommendationSkill": {
                "enabled": True,
                "max_price": 500,
                "min_rating": 3.5
            },
            "FlightBookingSkill": {
                "enabled": True,
                "preferred_airlines": ["Airline1", "Airline2"]
            }
        },
        "finance": {
            "InvestmentStrategySkill": {
                "enabled": True,
                "risk_levels": ["Low", "Medium", "High"],
                "min_investment": 1000
            },
            "TaxPlanningSkill": {
                "enabled": True,
                "supported_countries": ["USA", "Canada", "UK"]
            }
        }
        # Add more skill configurations as needed
    }
    write_json_file(os.path.join(config_dir, "skill_config.json"), skill_config)

    # Tool configuration
    tool_config = {
        "web_interaction": {
            "APIRequesterTool": {
                "enabled": True,
                "max_retries": 3,
                "timeout": 30
            },
            "WebScraperTool": {
                "enabled": True,
                "user_agent": "AJ_MAS Bot 1.0"
            }
        },
        "data_analysis": {
            "DataVisualizerTool": {
                "enabled": True,
                "max_data_points": 1000,
                "default_chart_type": "line"
            },
            "StatisticalAnalysisTool": {
                "enabled": True,
                "confidence_level": 0.95
            }
        },
        "nlp": {
            "TextSummarizationTool": {
                "enabled": True,
                "max_summary_length": 200
            },
            "SentimentAnalysisTool": {
                "enabled": True,
                "sentiment_levels": ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
            }
        }
        # Add more tool configurations as needed
    }
    write_json_file(os.path.join(config_dir, "tool_config.json"), tool_config)

if __name__ == "__main__":
    create_config_files()
    print("AJ_MAS configuration files created successfully!")
