import pytest
from tools.signal_decoder import decode_signal


def test_decode_alien_signal():
    """Test decoding an alien signal."""
    encoded = "§Ω§¥ßΩ π∆∆µ §λπΩµ !+! ß¥§π¥Φß *^* §¥ ¥∞π§Ω"
    result = decode_signal(encoded_signal=encoded, signal_type="alien")
    
    assert result.success is True
    assert "decoded_message" in result.data
    assert result.data["signal_type"] == "alien"
    assert "aeatse ioon alien please staitus warning at tmiae" in result.data["decoded_message"]


def test_decode_satellite_signal():
    """Test decoding a satellite signal."""
    encoded = "CMD:NAV:UPDATE:coordinates\nCMD:COMM:BROADCAST\n01100001 01101100 01100101 01110010 01110100"
    result = decode_signal(encoded_signal=encoded, signal_type="satellite")
    
    assert result.success is True
    assert "decoded_message" in result.data
    assert result.data["signal_type"] == "satellite"
    assert "NAV system: UPDATE operation coordinates" in result.data["decoded_message"]
    assert "COMM system: BROADCAST operation" in result.data["decoded_message"]
    assert "alert" in result.data["decoded_message"]


def test_decode_unknown_signal():
    """Test decoding an unknown signal type."""
    encoded = "§¥¥Ω∆µ¥π∆∆µ###§λπΩµ ∞Ωßß§ΦΩ###"
    result = decode_signal(encoded_signal=encoded)
    
    assert result.success is True
    assert "decoded_message" in result.data
    assert result.data["signal_type"] == "unknown"
    assert result.data["confidence"] == 0.7
    assert "Possible alien message:" in result.data["decoded_message"]


def test_invalid_signal_type():
    """Test providing an invalid signal type."""
    result = decode_signal(encoded_signal="test", signal_type="invalid")
    
    assert result.success is False
    assert "Error: Signal type must be 'alien', 'satellite', or 'unknown'" in result.error


def test_empty_signal():
    """Test providing an empty signal."""
    result = decode_signal(encoded_signal="")
    
    assert result.success is False
    assert "Error: Encoded signal must be a non-empty string" in result.error