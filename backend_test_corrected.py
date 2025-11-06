#!/usr/bin/env python3
"""
Corrected Backend API Testing for Budget Wedding Planner
Verifies exact budget calculations based on actual service prices
"""

import requests
import json

BACKEND_URL = "http://localhost:8001"

def test_exact_budget_calculations():
    """Test budget calculations with exact expected values"""
    
    print("🧮 Testing Exact Budget Calculations")
    print("=" * 50)
    
    # Test Scenario 1: Budget wedding
    payload1 = {
        "guest_count": 200,
        "venue_id": "v1",  # Garden Paradise ₹150,000
        "cuisine_ids": ["c5"],  # Simple Vegetarian ₹250/plate
        "service_ids": ["s1", "s3", "s7", "s9"]  # Basic services: 30k+40k+20k+15k = 105k
    }
    
    expected1 = 150000 + (250 * 200) + 105000  # ₹305,000
    
    response1 = requests.post(f"{BACKEND_URL}/api/calculate-budget", json=payload1)
    if response1.status_code == 200:
        actual1 = response1.json()["total_cost"]
        status1 = "✅ PASS" if actual1 == expected1 else "❌ FAIL"
        print(f"{status1}: Budget Wedding - Expected: ₹{expected1:,}, Got: ₹{actual1:,}")
    
    # Test Scenario 2: Mid-range wedding
    payload2 = {
        "guest_count": 350,
        "venue_id": "v2",  # Royal Banquet Hall ₹300,000
        "cuisine_ids": ["c3"],  # Mixed Cuisine ₹600/plate
        "service_ids": ["s2", "s4", "s5", "s7", "s9", "s11"]  # 80k+100k+25k+20k+15k+15k = 255k
    }
    
    expected2 = 300000 + (600 * 350) + 255000  # ₹765,000
    
    response2 = requests.post(f"{BACKEND_URL}/api/calculate-budget", json=payload2)
    if response2.status_code == 200:
        actual2 = response2.json()["total_cost"]
        status2 = "✅ PASS" if actual2 == expected2 else "❌ FAIL"
        print(f"{status2}: Mid-range Wedding - Expected: ₹{expected2:,}, Got: ₹{actual2:,}")
    
    # Test Scenario 3: Premium wedding
    payload3 = {
        "guest_count": 500,
        "venue_id": "v3",  # Heritage Palace ₹500,000
        "cuisine_ids": ["c4"],  # Premium Royal Feast ₹800/plate
        "service_ids": ["s2", "s4", "s6", "s8", "s10", "s11", "s12"]  # 80k+100k+50k+40k+30k+15k+10k = 325k
    }
    
    expected3 = 500000 + (800 * 500) + 325000  # ₹1,225,000
    
    response3 = requests.post(f"{BACKEND_URL}/api/calculate-budget", json=payload3)
    if response3.status_code == 200:
        actual3 = response3.json()["total_cost"]
        status3 = "✅ PASS" if actual3 == expected3 else "❌ FAIL"
        print(f"{status3}: Premium Wedding - Expected: ₹{expected3:,}, Got: ₹{actual3:,}")
    
    print("\n📋 Breakdown Verification:")
    
    # Test breakdown structure for scenario 1
    if response1.status_code == 200:
        breakdown = response1.json().get("breakdown", [])
        print(f"Budget Wedding Breakdown ({len(breakdown)} items):")
        for item in breakdown:
            print(f"  - {item['category']}: {item['item']} = ₹{item['cost']:,}")
            if 'details' in item:
                print(f"    ({item['details']})")

if __name__ == "__main__":
    test_exact_budget_calculations()