# Testing with DeepEval

This guide explains how to test the Restaurant AI Assistant using **DeepEval** - a framework for evaluating LLM outputs.

## 🎯 What is DeepEval?

DeepEval is an open-source framework for testing LLM applications. It helps you:
- Evaluate the quality of LLM responses
- Test factual accuracy
- Measure relevance and coherence
- Automate LLM testing

## 📦 Installation

```bash
pip install deepeval
```

## 🧪 Test Scenarios

This application should pass these evaluation tests:

### 1. **Understanding Reservation Requests**
- **Test Name**: `test_understands_reservation_requests`
- **Purpose**: Verify the AI understands when users want to make reservations
- **Example Inputs**:
  - "I need a table for 4 tomorrow at 7 PM"
  - "Book me a reservation for 2 people tonight at 6"
  - "Can you reserve a table for 6 this Saturday?"

### 2. **Respecting Business Hours**
- **Test Name**: `test_respects_business_hours`
- **Purpose**: Verify the AI doesn't accept reservations outside 11 AM - 10 PM
- **Example Inputs**:
  - "I want a table at 10:30 PM"
  - "Can we book at 11 PM?"
  - "What about 10 AM tomorrow?"

### 3. **Table Capacity Matching**
- **Test Name**: `test_matches_party_size_to_table`
- **Purpose**: Verify the AI suggests appropriate tables for party size
- **Example Inputs**:
  - "I need a table for 8 people" (should suggest largest table: 6, and recommend split)
  - "2 people" (should suggest Table 1 or 2)
  - "5 people" (should suggest Table 5)

### 4. **Response Politeness**
- **Test Name**: `test_response_politeness`
- **Purpose**: Verify responses are always polite and professional
- **Example Inputs**:
  - Any request (responses should be friendly)
  - Impossible requests (should apologize and offer alternatives)

### 5. **Factual Accuracy**
- **Test Name**: `test_factual_accuracy`
- **Purpose**: Verify the AI provides correct restaurant information
- **Example Inputs**:
  - "What time does the restaurant open?"
  - "How many tables do you have?"
  - "What's the maximum party size?"

## 🔧 Sample Test Implementation

### Setup

```python
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FactualConsistency, Relevancy, Toxicity
import requests

# API endpoint
API_URL = "http://localhost:8000/chat"

def send_message(message: str) -> str:
    """Send message to the chatbot and get response"""
    response = requests.post(API_URL, json={"message": message})
    return response.json()["reply"]
```

### Example Test 1: Business Hours

```python
from deepeval import assert_test

def test_respects_business_hours():
    """Test that AI doesn't accept reservations outside business hours"""
    
    test_case = LLMTestCase(
        input="I want to book a table at 11 PM",
        expected_output="closed"  # Should mention we're closed
    )
    
    actual_output = send_message(test_case.input)
    test_case.actual_output = actual_output
    
    # Check if response mentions being closed or suggests earlier time
    assert any(phrase in actual_output.lower() for phrase in [
        "closed", "10 pm", "earlier", "business hours"
    ]), f"Response should mention business hours. Got: {actual_output}"
    
    print("✅ Business hours test passed")

test_respects_business_hours()
```

### Example Test 2: Politeness

```python
from deepeval.metrics import Toxicity

def test_response_politeness():
    """Test that all responses are polite"""
    
    messages = [
        "I need a table for 100 people",
        "Can I have a table at 5 AM?",
        "Do you have any tables?",
    ]
    
    for message in messages:
        response = send_message(message)
        
        # Check for politeness markers
        assert any(word in response.lower() for word in [
            "please", "thank you", "happy", "welcome", "appreciate",
            "sorry", "apologies", "unfortunately"
        ]), f"Response lacks politeness: {response}"
    
    print("✅ Politeness test passed")

test_response_politeness()
```

### Example Test 3: Factual Accuracy

```python
def test_factual_accuracy():
    """Test that AI provides correct restaurant information"""
    
    test_cases = [
        ("What are your business hours?", ["11", "10 pm", "11 am"]),
        ("How many tables do you have?", ["5", "five"]),
        ("What's your restaurant name?", ["AI Restaurant"]),
        ("Maximum party size?", ["6", "six"]),
    ]
    
    for question, expected_phrases in test_cases:
        response = send_message(question)
        response_lower = response.lower()
        
        found = any(phrase.lower() in response_lower for phrase in expected_phrases)
        assert found, f"Question: {question}\nExpected one of: {expected_phrases}\nGot: {response}"
    
    print("✅ Factual accuracy test passed")

test_factual_accuracy()
```

### Example Test 4: Table Capacity Matching

```python
def test_table_capacity_matching():
    """Test that AI suggests appropriate tables for party size"""
    
    test_cases = [
        {
            "message": "I need a table for 2 people",
            "should_mention": ["Table 1", "Table 2", "capacity 2"],
            "description": "2 people should get small tables"
        },
        {
            "message": "I need a table for 6 people",
            "should_mention": ["Table 5", "capacity 6"],
            "description": "6 people should get largest table"
        },
        {
            "message": "I need a table for 8 people",
            "should_not_mention": ["confirmed", "reserved"],
            "should_mention": ["split", "largest", "6"],
            "description": "8 people should get alternative suggestions"
        },
    ]
    
    for test in test_cases:
        response = send_message(test["message"])
        response_lower = response.lower()
        
        for phrase in test.get("should_mention", []):
            assert phrase.lower() in response_lower, \
                f"{test['description']}\nExpected '{phrase}' in: {response}"
        
        for phrase in test.get("should_not_mention", []):
            assert phrase.lower() not in response_lower, \
                f"{test['description']}\nShould NOT have '{phrase}' in: {response}"
    
    print("✅ Table capacity matching test passed")

test_table_capacity_matching()
```

## 🚀 Running Tests

### Run Single Test
```bash
python -m pytest test_file.py::test_name -v
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run with Coverage
```bash
pytest --cov=backend tests/
```

## 📊 Using DeepEval Metrics

### Relevancy
```python
from deepeval.metrics import Relevancy

def evaluate_relevancy():
    metric = Relevancy()
    
    test_case = LLMTestCase(
        input="What's your best table for 4 people?",
        expected_output="Table 3 or 4 seats 4 people",
        actual_output=send_message("What's your best table for 4 people?")
    )
    
    score = metric.measure(test_case)
    print(f"Relevancy Score: {score}")
```

### Factual Consistency
```python
from deepeval.metrics import FactualConsistency

def evaluate_factual_consistency():
    metric = FactualConsistency()
    
    context = """
    Our restaurant is open 11 AM to 10 PM.
    We have 5 tables with capacities: 2, 2, 4, 4, 6.
    """
    
    test_case = LLMTestCase(
        input="What time do you open?",
        expected_output="We open at 11 AM",
        actual_output=send_message("What time do you open?"),
        context=[context]
    )
    
    score = metric.measure(test_case)
    print(f"Factual Consistency Score: {score}")
```

## 📝 Best Practices

1. **Test Early and Often** - Test during development, not just at the end
2. **Use Multiple Metrics** - Combine different evaluation metrics
3. **Test Edge Cases** - Test unusual inputs and boundary conditions
4. **Automate Tests** - Run tests in CI/CD pipeline
5. **Monitor in Production** - Track LLM quality over time
6. **Document Test Cases** - Explain what each test measures

## 🔗 Resources

- [DeepEval Official Docs](https://docs.confident-ai.com/)
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [LLM Testing Best Practices](https://docs.confident-ai.com/docs/metrics-introduction)

## 💡 Next Steps

1. Set up pytest and deepeval
2. Create test files in a `tests/` directory
3. Implement the test cases above
4. Run tests regularly
5. Integrate with GitHub Actions for CI/CD

---

**Happy Testing! 🧪**
