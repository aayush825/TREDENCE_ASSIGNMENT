import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface AutocompleteProps {
  language: string;
  prefix: string;
  roomId: string;
}

interface Suggestion {
  label: string;
  kind: string;
  detail: string;
  insertText?: string;
}

const Autocomplete: React.FC<AutocompleteProps> = ({ language, prefix, roomId }) => {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!prefix || prefix.length < 1) {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      setIsLoading(true);
      try {
        const response = await axios.post('http://localhost:8000/api/autocomplete/suggestions', {
          language,
          prefix,
          room_id: roomId,
        });
        setSuggestions(response.data);
      } catch (error) {
        console.error('Failed to fetch autocomplete suggestions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const debounceTimer = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(debounceTimer);
  }, [language, prefix, roomId]);

  return (
    <div style={{ position: 'absolute', background: '#fff', border: '1px solid #ccc', maxHeight: '200px', overflowY: 'auto' }}>
      {isLoading && <div>Loading...</div>}
      {suggestions.map((suggestion, index) => (
        <div key={index} style={{ padding: '5px', borderBottom: '1px solid #eee' }}>
          <strong>{suggestion.label}</strong> <span style={{ color: '#666' }}>({suggestion.kind})</span>
          <div style={{ fontSize: '12px', color: '#999' }}>{suggestion.detail}</div>
        </div>
      ))}
    </div>
  );
};

export default Autocomplete;
