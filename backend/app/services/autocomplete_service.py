from sqlalchemy.orm import Session
from app.models import CodeEdit, Room

class AutocompleteService:
    """Service for providing autocomplete suggestions."""
    
    # Common programming keywords and snippets
    KEYWORDS = {
        "python": [
            "def", "class", "if", "else", "elif", "for", "while", "try", "except",
            "import", "from", "return", "yield", "lambda", "async", "await", "with"
        ],
        "javascript": [
            "function", "const", "let", "var", "if", "else", "for", "while", "try", "catch",
            "import", "export", "return", "async", "await", "class", "extends", "super"
        ],
        "typescript": [
            "function", "const", "let", "var", "if", "else", "for", "while", "try", "catch",
            "import", "export", "return", "async", "await", "class", "interface", "type"
        ],
        "java": [
            "public", "private", "class", "interface", "if", "else", "for", "while", "try", "catch",
            "import", "return", "new", "static", "final", "abstract", "extends", "implements"
        ]
    }
    
    # Common function/method patterns
    SNIPPETS = {
        "python": {
            "def": "def ${1:function_name}(${2:args}):\n    ${3:pass}",
            "class": "class ${1:ClassName}:\n    def __init__(self):\n        ${2:pass}",
        },
        "javascript": {
            "function": "function ${1:name}(${2:params}) {\n    ${3:}\n}",
            "const": "const ${1:name} = ${2:value};",
            "arrow": "const ${1:name} = (${2:params}) => {\n    ${3:}\n};",
        },
        "typescript": {
            "function": "function ${1:name}(${2:params}): ${3:ReturnType} {\n    ${4:}\n}",
            "interface": "interface ${1:Name} {\n    ${2:properties}\n}",
        }
    }
    
    @staticmethod
    def get_suggestions(language: str, prefix: str, db: Session = None) -> list:
        """Get autocomplete suggestions based on language and prefix."""
        suggestions = []
        
        # Get keywords for the language
        keywords = AutocompleteService.KEYWORDS.get(language.lower(), [])
        
        # Filter keywords by prefix
        for keyword in keywords:
            if keyword.startswith(prefix.lower()):
                suggestions.append({
                    "label": keyword,
                    "kind": "keyword",
                    "detail": f"{language} keyword"
                })
        
        # Get snippets for the language
        snippets = AutocompleteService.SNIPPETS.get(language.lower(), {})
        
        # Filter snippets by prefix
        for snippet_key, snippet_value in snippets.items():
            if snippet_key.startswith(prefix.lower()):
                suggestions.append({
                    "label": snippet_key,
                    "kind": "snippet",
                    "detail": "code snippet",
                    "insertText": snippet_value
                })
        
        return suggestions
    
    @staticmethod
    def get_code_context(db: Session, room_id: str, line_number: int) -> str:
        """Get code context for autocomplete from a specific line."""
        room = db.query(Room).filter(Room.room_id == room_id).first()
        if not room:
            return ""
        
        lines = room.code_content.split('\n')
        if line_number < len(lines):
            return lines[line_number]
        return ""
