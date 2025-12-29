import { useState, useEffect, useRef } from "react";
import api from "../api/axios";

function AIAssistant() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [inputText, setInputText] = useState("");
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        if (isOpen) {
            scrollToBottom();
        }
    }, [messages, isTyping, isOpen]);

    useEffect(() => {
        if (isOpen && messages.length === 0) {
            startConversation();
        }
    }, [isOpen]);

    const startConversation = async () => {
        addMessage({ text: "Hi! 👋 I'm your Smart Note Assistant. I'm ready to help you organize your thoughts.", sender: "ai" });
        setIsTyping(true);

        try {
            const summaryRes = await api.get("/ai/task-summary");
            setIsTyping(false);
            addMessage({ text: summaryRes.data.summary, sender: "ai" });
            addMessage({ text: "What's on your mind today?", sender: "ai" });
        } catch (error) {
            setIsTyping(false);
            addMessage({ text: "I'm in basic mode right now, but feel free to chat!", sender: "ai" });
        }
    };

    const addMessage = (msg) => {
        setMessages((prev) => [...prev, { ...msg, id: Date.now() }]);
    };

    const handleSend = async () => {
        if (!inputText.trim()) return;

        const textPayload = inputText;
        setInputText("");

        addMessage({ text: textPayload, sender: "user" });
        setIsTyping(true);

        try {
            const res = await api.post("/ai/chat", { message: textPayload });
            setIsTyping(false);
            addMessage({ text: res.data.reply, sender: "ai" });
        } catch (error) {
            setIsTyping(false);
            addMessage({ text: "Connection error. Ensure the server is running.", sender: "ai" });
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter") handleSend();
    };

    return (
        <div style={styles.container}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                style={{ ...styles.fab, transform: isOpen ? "rotate(90deg) scale(0.9)" : "rotate(0) scale(1)" }}
            >
                {isOpen ? "✕" : "🤖"}
            </button>

            {isOpen && (
                <div style={styles.chatWindow}>
                    <div style={styles.header}>
                        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                            <div style={styles.avatarMini}>AI</div>
                            <span style={{ fontWeight: "600", fontSize: "0.95rem" }}>Note Assistant</span>
                        </div>
                        <button
                            onClick={() => setMessages([])}
                            style={styles.resetBtn}
                        >
                            🗑️
                        </button>
                    </div>

                    <div style={styles.messageList}>
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                style={{
                                    ...styles.bubble,
                                    alignSelf: msg.sender === "ai" ? "flex-start" : "flex-end",
                                    background: msg.sender === "ai" ? "#f0f2f5" : "hsl(var(--primary))",
                                    color: msg.sender === "ai" ? "#1f2937" : "white",
                                }}
                            >
                                <div style={{ whiteSpace: "pre-line" }}>{msg.text}</div>
                            </div>
                        ))}
                        {isTyping && (
                            <div style={styles.typingIndicator}>
                                <span>●</span><span>●</span><span>●</span>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div style={styles.footer}>
                        <input
                            style={styles.input}
                            placeholder="Message..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button onClick={handleSend} style={styles.sendBtn}>
                            ➤
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

const styles = {
    container: { position: "fixed", bottom: "30px", right: "30px", zIndex: 1000 },
    fab: {
        width: "60px",
        height: "60px",
        borderRadius: "50%",
        backgroundColor: "hsl(var(--primary))",
        color: "white",
        fontSize: "24px",
        border: "none",
        boxShadow: "0 8px 16px rgba(0,0,0,0.15)",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "all 0.3s"
    },
    chatWindow: {
        position: "absolute",
        bottom: "75px",
        right: "0",
        width: "350px",
        height: "500px",
        backgroundColor: "white",
        borderRadius: "16px",
        boxShadow: "0 10px 40px rgba(0,0,0,0.15)",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
    },
    header: {
        padding: "16px",
        background: "hsl(var(--primary))",
        color: "white",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
    },
    avatarMini: { width: "24px", height: "24px", borderRadius: "12px", background: "rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "10px", fontWeight: "bold" },
    resetBtn: { background: "none", border: "none", cursor: "pointer", color: "white", fontSize: "14px" },
    messageList: { flex: 1, padding: "16px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "12px", backgroundColor: "#fff" },
    bubble: { maxWidth: "85%", padding: "12px 16px", borderRadius: "18px", fontSize: "0.9rem", lineHeight: "1.4" },
    typingIndicator: { alignSelf: "flex-start", padding: "12px 16px", color: "#888", display: "flex", gap: "4px", fontSize: "8px" },
    footer: { padding: "12px", borderTop: "1px solid #eee", display: "flex", gap: "10px", backgroundColor: "#fdfdfd" },
    input: { flex: 1, padding: "10px 15px", borderRadius: "20px", border: "1px solid #ddd", fontSize: "0.9rem", outline: "none" },
    sendBtn: { background: "hsl(var(--primary))", color: "white", border: "none", width: "36px", height: "36px", borderRadius: "50%", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }
};

export default AIAssistant;
