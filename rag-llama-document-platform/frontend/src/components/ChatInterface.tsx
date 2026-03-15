import React, { useState } from 'react';
import axios from 'axios';

interface ChatResponse {
  answer: string;
  context: string[];
}

const ChatInterface: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<
    { role: 'user' | 'assistant'; text: string }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) {
      return;
    }

    const currentQuestion = question;
    setMessages((prev) => [...prev, { role: 'user', text: currentQuestion }]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await axios.post<ChatResponse>('http://localhost:8000/chat', {
        question: currentQuestion,
      });

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: response.data.answer },
      ]);
    } catch (error) {
      console.error('Error chatting with documents:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Failed to get answer from backend.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <h2>Chat With Documents</h2>

      <div
        style={{
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '16px',
          minHeight: '220px',
          marginBottom: '12px',
        }}
      >
        {messages.length === 0 ? (
          <p>Ask a question about your uploaded documents.</p>
        ) : (
          messages.map((message, index) => (
            <p key={index}>
              <strong>{message.role === 'user' ? 'You' : 'Assistant'}:</strong>{' '}
              {message.text}
            </p>
          ))
        )}
      </div>

      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask something about the document"
          style={{ flex: 1, padding: '10px' }}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
