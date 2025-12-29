import { useState } from "react";
import api from "../api/axios";

function TaskList({ tasks, setTasks }) {
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ title: "", description: "", due_date: "" });

  const startEdit = (task) => {
    setEditingId(task.id);
    let dueDateStr = "";
    if (task.due_date) {
      const dateStr = typeof task.due_date === 'string' ? task.due_date : new Date(task.due_date).toISOString();
      dueDateStr = dateStr.slice(0, 10);
    }
    setForm({ title: task.title, description: task.description || "", due_date: dueDateStr });
  };

  const saveEdit = async (id) => {
    if (!form.title.trim()) return alert("Title cannot be empty");
    try {
      const payload = { ...form, due_date: form.due_date ? new Date(form.due_date).toISOString() : null };
      const res = await api.patch(`/tasks/${id}`, payload);
      setTasks((prev) => prev.map((task) => (task.id === id ? res.data : task)));
      setEditingId(null);
    } catch (error) {
      console.error(error);
    }
  };

  const completeTask = async (id) => {
    try {
      const res = await api.patch(`/tasks/${id}/complete`);
      setTasks((prev) => prev.map((task) => (task.id === id ? res.data : task)));
    } catch (error) { console.error(error); }
  };

  const reopenTask = async (id) => {
    try {
      const res = await api.patch(`/tasks/${id}/reopen`);
      setTasks((prev) => prev.map((task) => (task.id === id ? res.data : task)));
    } catch (error) { console.error(error); }
  };

  const deleteTask = async (id) => {
    if (!window.confirm("Delete this note?")) return;
    try {
      await api.delete(`/tasks/${id}`);
      setTasks((prev) => prev.filter((task) => task.id !== id));
    } catch (error) { console.error(error); }
  };

  return (
    <ul className="notes-grid">
      {tasks.length === 0 && (
        <p style={{ gridColumn: "1 / -1", textAlign: "center", color: "#888", padding: "40px" }}>
          Your notepad is empty. 📝 Write something!
        </p>
      )}

      {tasks.map((task) => (
        <li key={task.id} className={`note-card status-${task.status}`}>
          {editingId === task.id ? (
            <div style={{ display: "flex", flexDirection: "column", gap: "10px", height: "100%" }}>
              <input
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                placeholder="Title"
                autoFocus
                style={{ fontWeight: "bold" }}
              />
              <textarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                placeholder="Note details..."
                style={{ flexGrow: 1, resize: "none" }}
              />
              <input
                type="date"
                value={form.due_date}
                onChange={(e) => setForm({ ...form, due_date: e.target.value })}
              />
              <div style={{ display: "flex", justifyContent: "flex-end", gap: "5px" }}>
                <button className="primary" onClick={() => saveEdit(task.id)}>Save</button>
                <button className="secondary" onClick={() => setEditingId(null)}>Cancel</button>
              </div>
            </div>
          ) : (
            <>
              <div className="note-header">
                <div className="note-title">{task.title}</div>
              </div>

              <div className="note-body">
                {task.description || <span style={{ opacity: 0.5, fontStyle: "italic" }}>No details</span>}
              </div>

              <div className="note-footer">
                <div style={{ display: "flex", gap: "5px", alignItems: "center" }}>
                  {task.due_date && (
                    <span className="note-date">
                      📅 {new Date(task.due_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                    </span>
                  )}
                  {task.status === "completed" && <span style={{ fontSize: "12px", color: "green" }}>✓ Done</span>}
                </div>

                <div className="note-actions">
                  {task.status === "pending" ? (
                    <>
                      <button onClick={() => startEdit(task)} title="Edit">✏️</button>
                      <button onClick={() => completeTask(task.id)} title="Mark Done" style={{ color: "green" }}>✓</button>
                    </>
                  ) : (
                    <button onClick={() => reopenTask(task.id)} title="Reopen">↩️</button>
                  )}
                  <button className="danger" onClick={() => deleteTask(task.id)} title="Delete">🗑️</button>
                </div>
              </div>
            </>
          )}
        </li>
      ))}
    </ul>
  );
}

export default TaskList;
