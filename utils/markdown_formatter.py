import json
from datetime import datetime
from typing import Dict, Any

class MarkdownFormatter:
    @staticmethod
    def format_document(content: Dict[str, Any], layout_info: Dict[str, Any]) -> str:
        try:
            # Extract content or error message
            searchable_text = (
                MarkdownFormatter._create_searchable_text(content)
                if isinstance(content.get('content'), dict)
                else str(content.get('content', ''))
            )
            
            # Handle error cases
            if not searchable_text.strip():
                searchable_text = "No content could be extracted from this document."
            elif "error" in content:
                searchable_text = f"Error: {content['error']}\n\nPartial content:\n{searchable_text}"
            
            # Create markdown structure
            md_parts = [
                "# " + content.get('title', 'Document Analysis'),
                "",
                "## Document Information",
                f"- Processed: {datetime.now().isoformat()}",
                f"- Provider: {content.get('metadata', {}).get('ocr_provider', 'unknown')}",
                f"- Status: {'Success' if searchable_text else 'Failed'}",
                "",
                "## Extracted Content",
                "",
                searchable_text,
                "",
                "## Technical Details",
                "```json",
                json.dumps(layout_info, indent=2, ensure_ascii=False),
                "```"
            ]
            
            return "\n".join(md_parts)
            
        except Exception as e:
            return f"""# Document Processing Error
            
Error: {str(e)}

Please check the document and try processing again."""

    @staticmethod
    def _create_searchable_text(content: Dict[str, Any]) -> str:
        """Create flattened, searchable text from content"""
        text_parts = []
        
        def flatten_dict(d: Dict, prefix=''):
            for k, v in d.items():
                if isinstance(v, dict):
                    flatten_dict(v, f"{k} - ")
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            flatten_dict(item, f"{k} - ")
                        else:
                            text_parts.append(f"{prefix}{k}: {item}")
                else:
                    text_parts.append(f"{prefix}{k}: {v}")
        
        flatten_dict(content.get('content', {}))
        return "\n".join(text_parts)
