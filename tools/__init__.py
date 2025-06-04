# This file marks the directory as a Python package and can be used to expose tools.
from tools.content_converters import CONTENT_CONVERTER_TOOLS
#from tools.web import WEB_TOOLS
from tools.space_calculator import SPACE_CALCULATOR_TOOLS
from tools.stellar_locator import STELLAR_LOCATOR_TOOLS
from tools.signal_decoder import SIGNAL_DECODER_TOOLS
from tools.vector_search import VECTOR_SEARCH_TOOLS
# Combine all tools into a single dictionary
TOOLS = {
    **CONTENT_CONVERTER_TOOLS,
    #**WEB_TOOLS,
    **SPACE_CALCULATOR_TOOLS,
    **STELLAR_LOCATOR_TOOLS,
    **SIGNAL_DECODER_TOOLS,
    **VECTOR_SEARCH_TOOLS
}