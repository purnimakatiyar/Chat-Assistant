import { useState } from "react";
import InputBox from "./InputBox";
import MessageList from "./MessageList";

export default function ChatContainer() {
  // Each message: { id, role: "user"|"assistant", content, insights? }
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (text) => {
    const userMessage = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsLoading(true);
    setError(null);

    try {
      // Build history for context (exclude current message — it's in `message` field)
      const history = messages.map(({ role, content }) => ({ role, content }));

      const API_BASE = import.meta.env.VITE_API_URL ?? "";
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history }),
      });

      if (!res.ok) {
        let errorMsg = `Server error (${res.status})`;
        try {
          const err = await res.json();
          errorMsg = err.detail || errorMsg;
        } catch {
          const text = await res.text();
          if (text) errorMsg = text;
        }
        throw new Error(errorMsg);
      }

      const data = await res.json();

      const aiMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.response,
        insights: data.insights,
      };

      setMessages([...updatedMessages, aiMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="chat-header-left">
          <div className="chat-avatar">AI</div>
          <div>
            <h1>AI Chat Assistant</h1>
            <p className="chat-subtitle">Powered by Groq · LLaMA 3.1</p>
          </div>
        </div>
        {messages.length > 0 && (
          <button className="clear-btn" onClick={clearChat} title="Clear chat">
            Clear
          </button>
        )}
      </header>

      <MessageList messages={messages} isLoading={isLoading} />

      {error && (
        <div className="error-bar">
          <span>⚠ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <InputBox onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
}
