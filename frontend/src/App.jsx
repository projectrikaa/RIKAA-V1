import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);

  async function send() {
    if (sending || !message.trim()) return;
    setSending(true);

    const text = message;
    setMessage("");
    setMessages((prev) => [...prev, { user: text, ai: null }]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await res.json();

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          user: text,
          ai: data.reply,
          code: data.code || "",
          file: data.file || "",
          run: data.run || null,
          build: data.build || null,
        };
        return updated;
      });
    } catch {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { user: text, ai: "(Error)" };
        return updated;
      });
    } finally {
      setSending(false);
    }
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>RIKAA</h1>

      <textarea
        rows={1}
        style={{ width: 400, padding: 10, resize: "vertical" }}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (message.trim()) {
              send();
            }
          }
        }}
        placeholder="Ask RIKAA..."
        disabled={sending}
      />

      <button onClick={send} disabled={sending}>Send</button>

      <hr />

{[...messages].reverse().map((m, index) => (
  <div key={index} style={{ marginTop: 20 }}>
    <b>You</b>
    <p>{m.user}</p>

    <b>RIKAA</b>
    <p>{m.ai}</p>

    {m.file && (
      <div style={{ marginTop: 8, fontSize: 13, color: "#555" }}>
        <div><b>File:</b> {m.file}</div>
      </div>
    )}

    {m.run && (
      <div style={{ marginTop: 4, fontSize: 13 }}>
        <div>
          <b>Run:</b>{" "}
          <span style={{ color: m.run.success ? "green" : "red" }}>
            {m.run.success ? "Success" : "Failed"}
          </span>
        </div>
        {m.run.output && (
          <pre style={{ background: "#f5f5f5", padding: 8, fontSize: 12, whiteSpace: "pre-wrap" }}>
            {m.run.output}
          </pre>
        )}
        {m.run.error && (
          <pre style={{ background: "#ffe0e0", padding: 8, fontSize: 12, whiteSpace: "pre-wrap" }}>
            {m.run.error}
          </pre>
        )}
      </div>
    )}

    {m.build && (
      <div style={{ marginTop: 4, fontSize: 13 }}>
        <b>Build:</b>{" "}
        <span style={{ color: m.build.success ? "green" : "red" }}>
          {m.build.message}
        </span>
      </div>
    )}

    <hr />
  </div>
))}
    </div>
  );
}

export default App;