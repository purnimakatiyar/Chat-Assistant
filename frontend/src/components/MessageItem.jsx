const SENTIMENT_CONFIG = {
  very_positive:     { emoji: "🤩", label: "Very Positive",     className: "sentiment-very-positive" },
  positive:          { emoji: "😊", label: "Positive",          className: "sentiment-positive" },
  slightly_positive: { emoji: "🙂", label: "Slightly Positive", className: "sentiment-slightly-positive" },
  neutral:           { emoji: "😐", label: "Neutral",           className: "sentiment-neutral" },
  slightly_negative: { emoji: "😕", label: "Slightly Negative", className: "sentiment-slightly-negative" },
  negative:          { emoji: "😟", label: "Negative",          className: "sentiment-negative" },
  very_negative:     { emoji: "😡", label: "Very Negative",     className: "sentiment-very-negative" },
};

const INTENT_ICONS = {
  greeting:       "👋",
  farewell:       "🚪",
  query:          "❓",
  request:        "📋",
  complaint:      "⚠️",
  praise:         "🌟",
  feedback:       "💬",
  clarification:  "🔍",
  confirmation:   "✅",
  denial:         "❌",
  troubleshooting:"🔧",
  small_talk:     "💭",
  opinion:        "🗣️",
  urgent:         "🚨",
  other:          "💡",
};

export default function MessageItem({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>
      {/* Bubble */}
      <div className="message-bubble">
        <p className="message-text">{message.content}</p>
      </div>

      {/* Insights badge — shown only on AI messages that have insights */}
      {!isUser && message.insights && (
        <InsightsBadge insights={message.insights} />
      )}
    </div>
  );
}

function InsightsBadge({ insights }) {
  const { intent, sentiment } = insights;
  const sentimentCfg = SENTIMENT_CONFIG[sentiment] ?? SENTIMENT_CONFIG.neutral;
  const intentIcon = INTENT_ICONS[intent] ?? INTENT_ICONS.other;

  return (
    <div className="insights-badge">
      <span className="insights-label">Insights:</span>
      <span className="insight-chip intent-chip">
        {intentIcon} {capitalise(intent)}
      </span>
      <span className={`insight-chip ${sentimentCfg.className}`}>
        {sentimentCfg.emoji} {sentimentCfg.label}
      </span>
    </div>
  );
}

function capitalise(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : str;
}
