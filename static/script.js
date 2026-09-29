const messages = document.getElementById("messages");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");

function addMessage(text, who, note) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  if (note) {
    const small = document.createElement("small");
    small.textContent = note;
    div.appendChild(small);
  }
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

async function send(question) {
  question = question.trim();
  if (!question) return;
  addMessage(question, "user");
  input.value = "";

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    const note = data.matched ? `Matched: "${data.matched}" (${Math.round(data.score * 100)}%)` : "";
    addMessage(data.answer, "bot", note);

    (data.suggestions || []).forEach(s => {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = s;
      b.onclick = () => send(s);
      messages.appendChild(b);
    });
    messages.scrollTop = messages.scrollHeight;
  } catch (e) {
    addMessage("Could not reach the server. Check that Flask is running and try again.", "bot");
  }
}

sendBtn.addEventListener("click", () => send(input.value));
input.addEventListener("keydown", e => { if (e.key === "Enter") send(input.value); });
document.querySelectorAll("#chips .chip").forEach(c => c.addEventListener("click", () => send(c.textContent)));
