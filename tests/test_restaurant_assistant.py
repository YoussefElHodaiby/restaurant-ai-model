"""
Sample tests for the Restaurant AI Assistant using DeepEval
Run with: pytest test_restaurant_assistant.py -v
"""

import pytest
import requests
from typing import str

# API endpoint - adjust if running on different port
API_URL = "http://localhost:8000/chat"


def send_message(message: str) -> str:
    """
    Send a message to the chatbot and get the response.
    
    Args:
        message: User message to send
        
    Returns:
        Assistant's response
    """
    try:
        response = requests.post(API_URL, json={"message": message}, timeout=30)
        response.raise_for_status()
        return response.json()["reply"]
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend not running. Start backend with: python backend/main.py")
    except Exception as e:
        raise Exception(f"Failed to get response: {str(e)}")


class TestBusinessHours:
    """Tests for business hours validation"""

    def test_accepts_valid_time_within_hours(self):
        """Should accept reservations during business hours"""
        response = send_message("I need a table for 2 at 7 PM tomorrow")
        
        # Should NOT mention being closed
        assert "closed" not in response.lower(), \
            f"Should accept 7 PM reservation. Got: {response}"

    def test_rejects_time_after_closing(self):
        """Should reject reservations after 10 PM"""
        response = send_message("Can I book a table for 4 at 10:30 PM?")
        
        # Should mention we're closed or suggest earlier time
        assert any(phrase in response.lower() for phrase in [
            "closed", "10 pm", "10pm", "earlier", "business hours", "until 10"
        ]), f"Should reject 10:30 PM. Got: {response}"

    def test_rejects_time_before_opening(self):
        """Should reject reservations before 11 AM"""
        response = send_message("Can we have a table at 9 AM?")
        
        # Should mention we're not open or suggest later time
        assert any(phrase in response.lower() for phrase in [
            "closed", "11 am", "11am", "later", "business hours", "open"
        ]), f"Should reject 9 AM. Got: {response}"


class TestTableCapacity:
    """Tests for table capacity matching"""

    def test_suggests_small_table_for_small_party(self):
        """Should suggest Table 1 or 2 for 2 people"""
        response = send_message("I need a table for 2 people")
        response_lower = response.lower()
        
        # Should mention table capacity or specific table number
        has_reference = any(phrase in response_lower for phrase in [
            "table 1", "table 2", "capacity 2", "two people"
        ])
        assert has_reference, f"Should mention small table. Got: {response}"

    def test_suggests_large_table_for_large_party(self):
        """Should suggest Table 5 for 6 people"""
        response = send_message("I need a table for 6 people")
        response_lower = response.lower()
        
        # Should mention the largest table
        has_reference = any(phrase in response_lower for phrase in [
            "table 5", "capacity 6", "six people", "largest"
        ])
        assert has_reference, f"Should mention large table. Got: {response}"

    def test_handles_oversized_party(self):
        """Should handle requests larger than max capacity"""
        response = send_message("I need a table for 10 people")
        response_lower = response.lower()
        
        # Should NOT confirm the reservation
        assert "confirmed" not in response_lower and "reserved" not in response_lower, \
            f"Should not confirm oversized party. Got: {response}"
        
        # Should suggest alternatives
        has_alternative = any(phrase in response_lower for phrase in [
            "split", "largest", "6", "maximum", "alternative"
        ])
        assert has_alternative, f"Should suggest alternatives. Got: {response}"


class TestPoliteness:
    """Tests for response politeness and professionalism"""

    def test_polite_greeting(self):
        """Should respond with politeness"""
        response = send_message("Hi, can I make a reservation?")
        response_lower = response.lower()
        
        # Should have at least one polite marker
        polite_words = ["welcome", "happy", "please", "thank", "glad", "help"]
        has_politeness = any(word in response_lower for word in polite_words)
        assert has_politeness or len(response) > 50, \
            f"Response should be polite and detailed. Got: {response}"

    def test_apologizes_for_unavailability(self):
        """Should apologize when table is unavailable"""
        response = send_message("I need a table for 100 people at peak hours")
        response_lower = response.lower()
        
        # Should include apology or regret
        has_apology = any(phrase in response_lower for phrase in [
            "sorry", "apologize", "unfortunately", "regret", "unable"
        ])
        assert has_apology or "not available" in response_lower, \
            f"Should apologize for unavailability. Got: {response}"

    def test_offers_alternatives(self):
        """Should offer alternatives when primary request can't be met"""
        response = send_message("Can I get a table at 11 PM?")
        
        # Should NOT just say no, should offer alternatives
        assert len(response) > 50, f"Should offer alternatives. Got: {response}"


class TestFactualAccuracy:
    """Tests for factual accuracy about restaurant info"""

    def test_knows_restaurant_name(self):
        """Should know the restaurant name"""
        response = send_message("What's your restaurant name?")
        response_lower = response.lower()
        
        assert "ai restaurant" in response_lower, \
            f"Should mention restaurant name. Got: {response}"

    def test_knows_business_hours(self):
        """Should know business hours"""
        response = send_message("What time are you open?")
        response_lower = response.lower()
        
        # Should mention both opening and closing times
        assert ("11" in response_lower or "11 am" in response_lower or "11am" in response_lower), \
            f"Should mention opening time (11 AM). Got: {response}"
        assert ("10" in response_lower or "10 pm" in response_lower or "10pm" in response_lower), \
            f"Should mention closing time (10 PM). Got: {response}"

    def test_knows_number_of_tables(self):
        """Should know how many tables we have"""
        response = send_message("How many tables do you have?")
        response_lower = response.lower()
        
        assert any(word in response_lower for word in ["5", "five"]), \
            f"Should mention 5 tables. Got: {response}"

    def test_knows_max_party_size(self):
        """Should know maximum party size"""
        response = send_message("What's the maximum party size?")
        response_lower = response.lower()
        
        assert any(word in response_lower for word in ["6", "six"]), \
            f"Should mention maximum of 6 people. Got: {response}"


class TestReservationUnderstanding:
    """Tests for understanding reservation requests"""

    def test_understands_party_size_extraction(self):
        """Should understand party size from natural language"""
        test_cases = [
            ("Table for two", "2"),
            ("Four people", "4"),
            ("Party of 6", "6"),
            ("Just me", "1"),
        ]
        
        for message, size in test_cases:
            response = send_message(f"I need {message}")
            response_lower = response.lower()
            
            # Should acknowledge the party size
            assert any(num in response_lower for num in [size, {
                "1": "one",
                "2": "two",
                "4": "four",
                "6": "six"
            }.get(size, "")]), f"Should understand '{message}'. Got: {response}"

    def test_understands_time_extraction(self):
        """Should understand time from natural language"""
        response = send_message("I need a table for 2 at 7 PM tomorrow")
        response_lower = response.lower()
        
        # Should acknowledge the time request
        assert any(time in response_lower for time in ["7", "pm", "evening"]), \
            f"Should understand time. Got: {response}"


class TestErrorHandling:
    """Tests for graceful error handling"""

    def test_handles_unclear_requests(self):
        """Should handle unclear requests gracefully"""
        response = send_message("xyz abc 123")
        
        # Should not crash, should provide helpful response
        assert len(response) > 0, "Should provide some response"
        assert response != "", "Should not return empty response"

    def test_handles_empty_request(self):
        """Should handle empty or very short requests"""
        response = send_message(" ")
        
        # Should not crash
        assert len(response) > 0, "Should provide some response"


class TestConversationFlow:
    """Tests for natural conversation flow"""

    def test_can_handle_follow_up_questions(self):
        """Should handle follow-up questions"""
        # First message
        response1 = send_message("I need a table for 4")
        assert len(response1) > 0, "Should respond to first message"
        
        # Follow-up
        response2 = send_message("At 7 PM tomorrow?")
        assert len(response2) > 0, "Should respond to follow-up"

    def test_responses_are_not_too_long(self):
        """Responses should be concise, not excessively long"""
        response = send_message("Can I make a reservation?")
        
        # Response should be reasonable length (not too short or long)
        assert 30 < len(response) < 500, \
            f"Response should be concise. Length: {len(response)}"


# Markers for different test categories
SLOW_TESTS = ["test_"]  # All tests are fast for this project


if __name__ == "__main__":
    # Quick test to verify API is working
    print("Testing API connection...")
    try:
        response = send_message("Hi")
        print(f"✅ API is working! Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ API is not responding: {e}")
        print("Make sure to start the backend with: python backend/main.py")
