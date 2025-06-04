import weave
import re
from tools.return_type import ToolResult
from typing import Dict, Any

SIGNAL_DECODER_TOOLS = {
    "decode_signal": {
        "type": "function",
        "function": {
            "name": "signal_decoder-decode_signal",
            "description": """Decodes alien or satellite signals into human-readable messages.  Best used for:
            - Translating encoded alien transmissions into human language
            - Converting encoded satellite signals into instructions
            - Interpreting strange or unusual message patterns received from space
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "encoded_signal": {
                        "type": "string",
                        "description": "The encoded signal to decode"
                    },
                    "signal_type": {
                        "type": "string",
                        "description": "The type of signal (alien, satellite, or unknown)",
                        "enum": ["alien", "satellite", "unknown"]
                    }
                },
                "required": ["encoded_signal"]
            }
        }
    }
}

@weave.op(name="signal_decoder-decode_signal")
def decode_signal(*, encoded_signal: str, signal_type: str = "unknown") -> ToolResult[Dict[str, Any]]:
    """
    Decode an encoded signal and translate it into human-readable form.
    
    Args:
        encoded_signal: The encoded signal string to decode
        signal_type: The type of signal (alien, satellite, or unknown)
        
    Returns:
        A dictionary containing the decoded message and additional metadata
    """
    try:
        # Validate input
        if not encoded_signal or not isinstance(encoded_signal, str):
            return ToolResult.err("Encoded signal must be a non-empty string")
            
        if signal_type not in ["alien", "satellite", "unknown"]:
            return ToolResult.err("Signal type must be 'alien', 'satellite', or 'unknown'")
        
        # Simple decoding logic - can be enhanced as needed
        decoded_message = ""
        confidence = 0.0
        source_info = "Unknown source"
        
        # Different decoding strategies based on signal type
        if signal_type == "alien":
            # Simple substitution cipher for alien signals
            decoded_message = _decode_alien_signal(encoded_signal)
            confidence = 0.85
            source_info = "Extraterrestrial origin"
            
        elif signal_type == "satellite":
            # Pattern-based decoding for satellite signals
            decoded_message = _decode_satellite_signal(encoded_signal)
            confidence = 0.95
            source_info = "Earth satellite network"
            
        else:
            # Basic decoding for unknown signals
            decoded_message = _decode_unknown_signal(encoded_signal)
            confidence = 0.70
            source_info = "Unidentified source"
        
        # Return the decoded result with metadata
        result = {
            "decoded_message": decoded_message,
            "confidence": confidence,
            "source": source_info,
            "signal_type": signal_type
        }
        
        return ToolResult.ok(result)
        
    except Exception as e:
        return ToolResult.err(str(e))

def _decode_alien_signal(encoded_signal: str) -> str:
    """
    Decode an alien signal using simple substitution patterns.
    This is a basic implementation that can be enhanced.
    """
    # Simple transformation - replace characters with others
    # This is a placeholder implementation
    decoded = encoded_signal
    
    # Example substitution patterns
    substitutions = {
        "§": "a", "Ω": "e", "π": "i", "∆": "o", "Φ": "u",
        "¥": "t", "µ": "n", "ß": "s", "∞": "m", "λ": "l",
        "!+!": "please", "?-?": "urgent", "*^*": "warning",
        "<<": "begin", ">>": "end",
    }
    
    for code, translation in substitutions.items():
        decoded = decoded.replace(code, translation)
    
    # Check for special patterns
    if "###" in decoded:
        decoded = re.sub(r'###(.*?)###', r'IMPORTANT: \1', decoded)
    
    return decoded.strip()

def _decode_satellite_signal(encoded_signal: str) -> str:
    """
    Decode a satellite signal using command-based patterns.
    This is a basic implementation that can be enhanced.
    """
    # Look for command patterns
    command_pattern = r'CMD:(\w+):(\w+):?(.*)?'
    message_parts = []
    
    # Process line by line
    for line in encoded_signal.split('\n'):
        # Check for command patterns
        cmd_match = re.match(command_pattern, line)
        if cmd_match:
            system = cmd_match.group(1)
            action = cmd_match.group(2)
            params = cmd_match.group(3) or ""
            
            message_parts.append(f"{system} system: {action} operation {params}")
        else:
            # Basic binary to text conversion for non-command parts
            if set(line.strip()) <= set('01 '):
                try:
                    # Convert binary strings to ASCII
                    binary_parts = line.strip().split()
                    text_parts = []
                    for part in binary_parts:
                        if part and all(bit in '01' for bit in part):
                            char_code = int(part, 2)
                            if 32 <= char_code <= 126:  # Printable ASCII range
                                text_parts.append(chr(char_code))
                    
                    if text_parts:
                        message_parts.append("".join(text_parts))
                except ValueError:
                    # If not valid binary, keep as is
                    message_parts.append(line)
            else:
                # Default handling for other content
                message_parts.append(line)
    
    return " ".join(message_parts).strip()

def _decode_unknown_signal(encoded_signal: str) -> str:
    """
    Attempt to decode an unknown signal using multiple strategies.
    This is a basic implementation that can be enhanced.
    """
    # Try different decoding strategies and use the most likely one
    
    # First try alien decoding
    alien_decoded = _decode_alien_signal(encoded_signal)
    
    # Then try satellite decoding
    satellite_decoded = _decode_satellite_signal(encoded_signal)
    
    # Simple heuristic: choose the result with more alphabetic characters
    alien_alpha_count = sum(c.isalpha() for c in alien_decoded)
    satellite_alpha_count = sum(c.isalpha() for c in satellite_decoded)
    
    if alien_alpha_count > satellite_alpha_count:
        return f"Possible alien message: {alien_decoded}"
    elif satellite_alpha_count > alien_alpha_count:
        return f"Possible satellite message: {satellite_decoded}"
    else:
        # If both strategies yielded similar results, return a combined message
        return f"Unclear origin. Best translation attempt: {encoded_signal.replace('$', ' ').replace('#', '').replace('@', '')}"