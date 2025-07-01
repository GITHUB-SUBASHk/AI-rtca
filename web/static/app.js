const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatBody = document.getElementById("chatBody");

function addMessage(content, sender = "user") {
  const msg = document.createElement("div");
  msg.className = `message ${sender === "user" ? "user-msg" : "bot-msg"}`;
  msg.innerHTML = marked.parse(content);
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  userInput.focus();

  addMessage("...", "bot");

  try {
    const res = await fetch("/generate-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    const lastBotMsg = chatBody.querySelector(".bot-msg:last-child");
    if (lastBotMsg) lastBotMsg.remove();

    addMessage(data.reply || "⚠️ No response.", "bot");
  } catch (error) {
    const lastBotMsg = chatBody.querySelector(".bot-msg:last-child");
    if (lastBotMsg) lastBotMsg.remove();
    addMessage("⚠️ Error: Could not connect to server.", "bot");
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
