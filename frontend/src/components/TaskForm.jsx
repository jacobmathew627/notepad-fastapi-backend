import { useState } from "react";
import api from "../api/axios";

function TaskForm({ setTasks, onTaskAdded }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [naturalLanguage, setNaturalLanguage] = useState("");
  const [isParsing, setIsParsing] = useState(false);
  const [showAIMode, setShowAIMode] = useState(false);

  // Use Case 3: Natural Language -> Draft
  const handleAIParse = async () => {
    if (!naturalLanguage.trim()) return;

    setIsParsing(true);
    try {
      const res = await api.post("/ai/task-draft", { text: naturalLanguage });

      setTitle(res.data.title || "");
      setDescription(res.data.description || "");

      if (res.data.due_date) {
        setDueDate(res.data.due_date.split("T")[0]);
      } else {
        setDueDate("");
      }

      setShowAIMode(false);
      setNaturalLanguage("");
    } catch (error) {
      console.error("Parse failed", error);
      alert("Could not parse note. Please enter manually.");
    } finally {
      setIsParsing(false);
    }
  };

  const handleAdd = async () => {
    if (!title || !title.trim()) {
      alert("Title cannot be empty");
      return;
    }

    try {
      const payload = {
        title: title.trim(),
        description: description.trim() || null,
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
      };

      const res = await api.post("/tasks/", payload);
      setTasks((prev) => [...prev, res.data]);
      if (onTaskAdded) onTaskAdded();

      setTitle("");
      setDescription("");
      setDueDate("");
    } catch (error) {
      console.error("Create failed", error);
      alert("Failed to create note.");
    }
  };

  return (
    <div className="task-form">
      <h3>Create Note</h3>

      {/* AI Toggle */}
      <div style={{ marginBottom: "15px", display: "flex", justifyContent: "flex-end" }}>
        <button
          onClick={() => setShowAIMode(!showAIMode)}
          className={showAIMode ? "secondary" : "secondary"}
          style={{ fontSize: "0.85rem", padding: "6px 12px" }}
        >
          {showAIMode ? "✕ Cancel AI" : "✨ Magic Draft"}
        </button>
      </div>

      {showAIMode ? (
        <div className="card-glass" style={{ marginBottom: "20px", background: "#f8fafc" }}>
          <p style={{ marginBottom: "8px", fontSize: "0.9rem", color: "#666" }}>
            Type naturally (e.g., "Buy groceries tomorrow") and I'll create the note.
          </p>
          <div style={{ display: "flex", gap: "10px" }}>
            <input
              placeholder='Describe your note...'
              value={naturalLanguage}
              onChange={(e) => setNaturalLanguage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleAIParse()}
              autoFocus
            />
            <button
              onClick={handleAIParse}
              disabled={isParsing || !naturalLanguage}
              className="primary"
            >
              {isParsing ? "Thinking..." : "Draft"}
            </button>
          </div>
        </div>
      ) : (
        <div className="form-group">
          <input
            placeholder="Note Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <textarea
            placeholder="Take a note..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{ minHeight: "80px", resize: "vertical" }}
          />
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
          />
        </div>
      )}

      {!showAIMode && (
        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: "15px" }}>
          <button onClick={handleAdd} disabled={!title.trim()} className="primary">
            + Add Note
          </button>
        </div>
      )}
    </div>
  );
}

export default TaskForm;
