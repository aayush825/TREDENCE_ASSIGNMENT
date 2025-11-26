import React from 'react';

interface EditorProps {
  roomId: string;
  code: string;
  onChange: (code: string) => void;
}

const CodeEditor: React.FC<EditorProps> = ({ code, onChange }) => {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        style={{
          width: '100%',
          height: '100%',
          fontFamily: 'monospace',
          fontSize: '14px',
          padding: '10px',
          border: '1px solid #ccc',
        }}
        placeholder="Start coding..."
      />
    </div>
  );
};

export default CodeEditor;
