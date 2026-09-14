import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [convId,setConvId]=useState("");

  async function sendMessage() {
    if (!question.trim()) {
      return;
    }

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        conversation_id:convId
      }),
    });

    const data = await response.json();

    setAnswer(data.answer);
  }

  return (
    <div>
      <h1>AI Support Agent</h1>
      <div>

      
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      </div>
      <div>
        
      </div>
      <input
        type="text"
        value={convId}
        onChange={(e) => setConvId(e.target.value)}
        placeholder="Enter conv Id okay"
      />

      <button onClick={sendMessage}>
        Send
      </button>

      <h2>Answer:</h2>

      <p>{answer}</p>
    </div>
  );
}

export default App;