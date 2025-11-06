#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Budget Wedding Planner
Tests all API endpoints and budget calculation scenarios
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "http://localhost:8001"

class WeddingPlannerAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        self.venues_data = []
        self.cuisines_data = []
        self.services_data = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test GET /api/health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, "Backend is running and healthy")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_venues_api(self):
        """Test GET /api/venues endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/venues", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                venues = data.get("venues", [])
                
                if len(venues) == 4:
                    # Verify venue structure
                    required_fields = ["id", "name", "description", "price_range", "capacity", "price", "image", "amenities"]
                    all_valid = True
                    
                    for venue in venues:
                        for field in required_fields:
                            if field not in venue:
                                all_valid = False
                                self.log_test("Venues API", False, f"Missing field '{field}' in venue {venue.get('id', 'unknown')}")
                                return False
                    
                    if all_valid:
                        self.venues_data = venues
                        venue_names = [v["name"] for v in venues]
                        self.log_test("Venues API", True, f"Retrieved 4 venues: {', '.join(venue_names)}")
                        return True
                else:
                    self.log_test("Venues API", False, f"Expected 4 venues, got {len(venues)}")
                    return False
            else:
                self.log_test("Venues API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Venues API", False, f"Connection error: {str(e)}")
            return False
    
    def test_cuisine_options_api(self):
        """Test GET /api/cuisine-options endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/cuisine-options", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cuisines = data.get("cuisines", [])
                
                if len(cuisines) == 5:
                    # Verify cuisine structure
                    required_fields = ["id", "name", "description", "price_per_plate", "cuisine_type", "popular_dishes"]
                    all_valid = True
                    
                    for cuisine in cuisines:
                        for field in required_fields:
                            if field not in cuisine:
                                all_valid = False
                                self.log_test("Cuisine Options API", False, f"Missing field '{field}' in cuisine {cuisine.get('id', 'unknown')}")
                                return False
                    
                    if all_valid:
                        self.cuisines_data = cuisines
                        cuisine_names = [c["name"] for c in cuisines]
                        self.log_test("Cuisine Options API", True, f"Retrieved 5 cuisines: {', '.join(cuisine_names)}")
                        return True
                else:
                    self.log_test("Cuisine Options API", False, f"Expected 5 cuisines, got {len(cuisines)}")
                    return False
            else:
                self.log_test("Cuisine Options API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Cuisine Options API", False, f"Connection error: {str(e)}")
            return False
    
    def test_services_api(self):
        """Test GET /api/services endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/services", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                services_grouped = data.get("services", {})
                all_services = data.get("all_services", [])
                
                # Check if services are grouped by category
                expected_categories = ["Photography", "Decorations", "Entertainment", "Makeup", "Invitations", "Transportation", "Mehendi"]
                found_categories = list(services_grouped.keys())
                
                if len(all_services) >= 10:  # Should have at least 10 services
                    # Verify service structure
                    required_fields = ["id", "category", "name", "description", "price", "package_type"]
                    all_valid = True
                    
                    for service in all_services:
                        for field in required_fields:
                            if field not in service:
                                all_valid = False
                                self.log_test("Services API", False, f"Missing field '{field}' in service {service.get('id', 'unknown')}")
                                return False
                    
                    if all_valid:
                        self.services_data = all_services
                        self.log_test("Services API", True, f"Retrieved {len(all_services)} services grouped in {len(found_categories)} categories: {', '.join(found_categories)}")
                        return True
                else:
                    self.log_test("Services API", False, f"Expected at least 10 services, got {len(all_services)}")
                    return False
            else:
                self.log_test("Services API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Services API", False, f"Connection error: {str(e)}")
            return False
    
    def test_budget_calculation_scenarios(self):
        """Test POST /api/calculate-budget with various scenarios"""
        if not self.venues_data or not self.cuisines_data or not self.services_data:
            self.log_test("Budget Calculation Setup", False, "Cannot test budget calculation - missing venue/cuisine/service data")
            return False
        
        scenarios = [
            # Scenario 1: Budget wedding (₹5L) - 200 guests, Garden Paradise venue, Simple Vegetarian cuisine, Basic services
            {
                "name": "Budget Wedding Scenario",
                "guest_count": 200,
                "venue_id": "v1",  # Garden Paradise
                "cuisine_ids": ["c5"],  # Simple Vegetarian
                "service_ids": ["s1", "s3", "s7", "s9"],  # Basic services
                "expected_range": (400000, 600000)  # ₹4L-6L range
            },
            # Scenario 2: Mid-range wedding (₹10L) - 350 guests, Royal Banquet Hall, Mixed Cuisine, Standard services
            {
                "name": "Mid-range Wedding Scenario",
                "guest_count": 350,
                "venue_id": "v2",  # Royal Banquet Hall
                "cuisine_ids": ["c3"],  # Mixed Cuisine Buffet
                "service_ids": ["s2", "s4", "s5", "s7", "s9", "s11"],  # Standard services
                "expected_range": (800000, 1200000)  # ₹8L-12L range
            },
            # Scenario 3: Premium wedding (₹15L+) - 500 guests, Heritage Palace, Premium cuisine, Premium services
            {
                "name": "Premium Wedding Scenario",
                "guest_count": 500,
                "venue_id": "v3",  # Heritage Palace
                "cuisine_ids": ["c4"],  # Premium Royal Feast
                "service_ids": ["s2", "s4", "s6", "s8", "s10", "s11", "s12"],  # Premium services
                "expected_range": (1400000, 2000000)  # ₹14L-20L range
            },
            # Test with only venue
            {
                "name": "Venue Only Test",
                "guest_count": 100,
                "venue_id": "v1",
                "cuisine_ids": None,
                "service_ids": None,
                "expected_range": (150000, 150000)  # Exact venue price
            },
            # Test with venue + cuisine
            {
                "name": "Venue + Cuisine Test",
                "guest_count": 200,
                "venue_id": "v1",
                "cuisine_ids": ["c1"],  # Traditional North Indian ₹400/plate
                "service_ids": None,
                "expected_range": (230000, 230000)  # 150000 + (200 * 400)
            }
        ]
        
        all_passed = True
        
        for scenario in scenarios:
            success = self.test_single_budget_calculation(scenario)
            if not success:
                all_passed = False
        
        return all_passed
    
    def test_single_budget_calculation(self, scenario: Dict):
        """Test a single budget calculation scenario"""
        try:
            payload = {
                "guest_count": scenario["guest_count"],
                "venue_id": scenario["venue_id"],
                "cuisine_ids": scenario["cuisine_ids"],
                "service_ids": scenario["service_ids"]
            }
            
            response = requests.post(f"{self.base_url}/api/calculate-budget", 
                                   json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_cost = data.get("total_cost", 0)
                breakdown = data.get("breakdown", [])
                guest_count = data.get("guest_count", 0)
                
                # Verify guest count matches
                if guest_count != scenario["guest_count"]:
                    self.log_test(scenario["name"], False, f"Guest count mismatch: expected {scenario['guest_count']}, got {guest_count}")
                    return False
                
                # Verify total cost is in expected range
                min_expected, max_expected = scenario["expected_range"]
                if min_expected <= total_cost <= max_expected:
                    # Verify breakdown structure
                    if breakdown and isinstance(breakdown, list):
                        breakdown_total = sum(item.get("cost", 0) for item in breakdown)
                        if breakdown_total == total_cost:
                            self.log_test(scenario["name"], True, 
                                        f"Budget calculation correct: ₹{total_cost:,} for {guest_count} guests")
                            return True
                        else:
                            self.log_test(scenario["name"], False, 
                                        f"Breakdown total (₹{breakdown_total:,}) doesn't match total cost (₹{total_cost:,})")
                            return False
                    else:
                        self.log_test(scenario["name"], False, "Missing or invalid breakdown in response")
                        return False
                else:
                    self.log_test(scenario["name"], False, 
                                f"Total cost ₹{total_cost:,} outside expected range ₹{min_expected:,}-₹{max_expected:,}")
                    return False
            else:
                self.log_test(scenario["name"], False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(scenario["name"], False, f"Connection error: {str(e)}")
            return False
    
    def test_budget_calculation_edge_cases(self):
        """Test budget calculation with different guest counts"""
        if not self.venues_data or not self.cuisines_data:
            return False
        
        guest_counts = [50, 200, 500, 1000]
        venue_id = "v1"  # Garden Paradise
        cuisine_id = "c1"  # Traditional North Indian ₹400/plate
        
        all_passed = True
        
        for guest_count in guest_counts:
            try:
                payload = {
                    "guest_count": guest_count,
                    "venue_id": venue_id,
                    "cuisine_ids": [cuisine_id],
                    "service_ids": None
                }
                
                response = requests.post(f"{self.base_url}/api/calculate-budget", 
                                       json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    total_cost = data.get("total_cost", 0)
                    
                    # Expected: venue (150000) + cuisine (guest_count * 400)
                    expected_cost = 150000 + (guest_count * 400)
                    
                    if total_cost == expected_cost:
                        self.log_test(f"Guest Count {guest_count}", True, 
                                    f"Correct calculation: ₹{total_cost:,}")
                    else:
                        self.log_test(f"Guest Count {guest_count}", False, 
                                    f"Expected ₹{expected_cost:,}, got ₹{total_cost:,}")
                        all_passed = False
                else:
                    self.log_test(f"Guest Count {guest_count}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Guest Count {guest_count}", False, f"Connection error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Budget Wedding Planner Backend API Tests")
        print("=" * 60)
        
        # Test basic endpoints first
        health_ok = self.test_health_check()
        venues_ok = self.test_venues_api()
        cuisines_ok = self.test_cuisine_options_api()
        services_ok = self.test_services_api()
        
        # Only test budget calculation if basic endpoints work
        budget_ok = False
        edge_cases_ok = False
        
        if venues_ok and cuisines_ok and services_ok:
            budget_ok = self.test_budget_calculation_scenarios()
            edge_cases_ok = self.test_budget_calculation_edge_cases()
        else:
            self.log_test("Budget Calculation", False, "Skipped due to failed prerequisite tests")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        return passed == total

def main():
    """Main test execution"""
    tester = WeddingPlannerAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend API is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the details above.")
        sys.exit(1)

if __name__ == "__main__":
    main()