#!/usr/bin/env python3
"""
SIMPLIFIED VERSION - Beaminster Events Calendar Agent
Works with GitHub Actions - saves to current directory
"""

import json
import os
from datetime import datetime
import requests

class BeaminsterEventsAgent:
    def __init__(self):
        self.location = "Beaminster, West Dorset, UK"
        self.lat = 50.8110
        self.lon = -2.7430
        self.api_keys = {
            'OPENWEATHER_API_KEY': os.getenv('OPENWEATHER_API_KEY', ''),
        }
    
    def get_weather(self):
        """Get weather forecast for Beaminster"""
        weather_data = {
            "location": "Beaminster, Dorset",
            "coordinates": {"lat": self.lat, "lon": self.lon},
            "forecast": []
        }
        
        if not self.api_keys.get('OPENWEATHER_API_KEY'):
            print("⚠️  OpenWeather API key not provided")
            return weather_data
        
        try:
            api_key = self.api_keys['OPENWEATHER_API_KEY']
            url = f"https://api.openweathermap.org/data/2.5/forecast"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': api_key,
                'units': 'metric',
                'cnt': 40
            }
            
            print(f"Fetching weather from OpenWeather API...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('list', [])[:7]:
                    weather_data['forecast'].append({
                        'date': item['dt_txt'],
                        'temp': item['main']['temp'],
                        'feels_like': item['main']['feels_like'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    })
                
                print(f"✅ Weather forecast fetched: {len(weather_data['forecast'])} periods")
            else:
                print(f"❌ Weather API error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Weather fetch error: {str(e)}")
        
        return weather_data
    
    def get_sample_events(self):
        """Return sample events for Beaminster area"""
        return [
            {
                "title": "Bridport Farmers Market",
                "date": "Every Saturday",
                "category": "Market",
                "description": "Award-winning farmers market featuring local produce, artisan breads, and handmade crafts.",
                "distance": "7 miles",
                "location": "Bridport",
                "icon": "🥕",
                "url": "https://www.bridport-tc.gov.uk/market/"
            },
            {
                "title": "West Dorset Food & Drink Festival",
                "date": "Spring 2026",
                "category": "Food & Dining",
                "description": "Celebrate the finest food and drink that West Dorset has to offer.",
                "distance": "10 miles",
                "location": "Dorchester",
                "icon": "🍷",
                "url": ""
            },
            {
                "title": "Jurassic Coast Walking Tours",
                "date": "Daily",
                "category": "Outdoor Activity",
                "description": "Guided walks along the stunning UNESCO World Heritage Jurassic Coast.",
                "distance": "12 miles",
                "location": "Lyme Regis",
                "icon": "🌊",
                "url": ""
            },
            {
                "title": "Mapperton House & Gardens",
                "date": "Open daily (seasonal)",
                "category": "Attraction",
                "description": "Explore the stunning terraced gardens of this historic manor house.",
                "distance": "3 miles",
                "location": "Beaminster",
                "icon": "🏰",
                "url": ""
            }
        ]
    
    def generate_output(self):
        """Generate the complete output"""
        print("\n" + "="*60)
        print("BEAMINSTER EVENTS CALENDAR GENERATOR")
        print("="*60 + "\n")
        
        output = {
            "meta": {
                "generated": datetime.now().isoformat(),
                "location": self.location,
                "coordinates": {"latitude": self.lat, "longitude": self.lon},
                "search_radius_miles": 15,
                "for_website": "hugholidays.co.uk"
            },
            "weather": self.get_weather(),
            "events": {
                "upcoming": self.get_sample_events(),
                "categories": [
                    "Festivals & Markets",
                    "Outdoor Activities",
                    "Arts & Cultural Events",
                    "Food & Dining",
                    "Local Attractions"
                ]
            },
            "local_attractions": [
                {
                    "name": "Parnham House",
                    "distance_miles": 1.5,
                    "type": "Historic House"
                },
                {
                    "name": "Mapperton House & Gardens",
                    "distance_miles": 3,
                    "type": "Stately Home & Gardens"
                },
                {
                    "name": "Jurassic Coast",
                    "distance_miles": 12,
                    "type": "UNESCO World Heritage Site"
                },
                {
                    "name": "Bridport Market",
                    "distance_miles": 7,
                    "type": "Market (Wed & Sat)"
                }
            ]
        }
        
        return output
    
    def save_json(self, data, filename="hugholidays_events.json"):
        """Save to JSON file in current directory"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Data saved to: {filename}")
        return filename

def main():
    print("🏠 HUGHOLIDAYS.CO.UK - BEAMINSTER EVENTS AGENT\n")
    
    agent = BeaminsterEventsAgent()
    data = agent.generate_output()
    filename = agent.save_json(data)
    
    print("\n" + "="*60)
    print("✅ COMPLETE!")
    print("="*60)
    print(f"Generated: {filename}")
    print(f"Location: {data['meta']['location']}")
    print(f"Events: {len(data['events']['upcoming'])}")
    print(f"Weather periods: {len(data['weather']['forecast'])}")
    print("\nFiles ready for download in GitHub Actions artifacts!")

if __name__ == "__main__":
    main()
