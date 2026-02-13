"""
Test configuration and fixtures for pytest
"""

import pytest
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))


@pytest.fixture
def sample_rti_text():
    """Sample RTI request text"""
    return """
    I request information under Section 6 of the Right to Information Act, 2005.
    Please provide certified copies of all documents related to road construction 
    project in Delhi during 2023-2024. I am willing to pay the requisite fee.
    """


@pytest.fixture
def sample_complaint_text():
    """Sample complaint text"""
    return """
    I want to file a grievance regarding the poor condition of roads in my area.
    There are multiple potholes and the street lights are not working. 
    Despite several complaints to the municipal corporation, no action has been taken.
    This is causing harassment to residents.
    """


@pytest.fixture
def sample_appeal_text():
    """Sample appeal text"""
    return """
    I am filing a first appeal under Section 19 of RTI Act 2005.
    My original RTI application number was RTI/2024/0001234, submitted 45 days ago.
    The PIO has not responded within the stipulated time of 30 days.
    I request the appellate authority to direct the PIO to provide the information.
    """


@pytest.fixture
def sample_urgent_complaint():
    """Sample urgent complaint needing immediate action"""
    return """
    URGENT: There has been a complete power failure in our area for the past 3 days.
    The transformer exploded and there is a risk of fire. Lives are at risk.
    Multiple calls to the electricity board have been ignored. 
    This is an emergency situation requiring immediate action.
    """


@pytest.fixture
def sample_corruption_complaint():
    """Sample corruption complaint text"""
    return """
    I want to report corruption by officials in the Land Registry Office.
    They are demanding bribes of Rs. 50,000 to process my property registration.
    This is illegal and a violation of the Prevention of Corruption Act.
    I request immediate investigation and action against the corrupt officials.
    """


@pytest.fixture
def sample_water_issue():
    """Sample water supply issue text"""
    return """
    There is no water supply in our colony for the past week.
    The pipeline is broken and sewage is mixing with drinking water.
    The Jal Board has not responded to our complaints. This is a health hazard.
    """


@pytest.fixture
def sample_follow_up():
    """Sample follow-up text"""
    return """
    This is a follow up on my previous complaint number CPGRAMS/2024/12345.
    I had submitted the complaint 2 months ago but have not received any response.
    Please provide the current status of my application.
    """


@pytest.fixture
def sample_escalation():
    """Sample escalation request text"""
    return """
    I am escalating my complaint to the higher authority as the concerned department
    has failed to take action despite multiple reminders. My original complaint
    reference number is PG/2024/5678. I request the senior officer to intervene.
    """


@pytest.fixture
def empty_text():
    """Empty text input"""
    return ""


@pytest.fixture
def minimal_text():
    """Minimal ambiguous text"""
    return "I need some help."


@pytest.fixture
def mixed_signals_text():
    """Text with mixed RTI and complaint signals"""
    return """
    I want to file a complaint about the poor road conditions in Delhi.
    Also, I request information under RTI about the budget allocated for road repairs.
    """
