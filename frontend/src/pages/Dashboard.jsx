import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { removeToken } from "../auth/auth";
import Header from "../components/Header";
import Filters from "../components/Filters";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import AIAssistant from "../components/AIAssistant";
import Stats from "../components/Stats";

/**
 * Dashboard Component
 * 
 * The primary view for authenticated users. It orchestrates the display of
 * stats, filters, task creation, and the task list.
 * 
 * State:
 * - tasks: Array of task objects from the backend.
 * - filter: Current active filter ('all', 'today', 'overdue', 'upcoming').
 * - refreshStats: A counter to trigger re-renders in the Stats component.
 * 
 * Hooks:
 * - useCallback: Memoizes fetchTasks to prevent unnecessary re-renders.
 * - useEffect: Triggers fetchTasks on mount and filter changes.
 */
function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");
  const [refreshStats, setRefreshStats] = useState(0);
  const navigate = useNavigate();

  /**
   * fetchTasks
   * Fetches task data from the API based on the current filter state.
   */
  const fetchTasks = useCallback(async () => {
    let url = "/tasks";

    if (filter === "today") url += "?today=true";
    if (filter === "overdue") url += "?overdue=true";
    if (filter === "upcoming") url += "?upcoming=7";

    try {
      const res = await api.get(url);
      setTasks(res.data);
      setRefreshStats((prev) => prev + 1); // 🔥 trigger stats refresh
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    }
  }, [filter]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleLogout = () => {
    removeToken();
    navigate("/login");
  };

  return (
    <div className="dashboard">
      <Header onLogout={handleLogout} />

      <AIAssistant />

      <Stats refreshKey={refreshStats} />

      <Filters setFilter={setFilter} />

      <TaskForm setTasks={setTasks} onTaskAdded={fetchTasks} />

      <TaskList
        tasks={tasks}
        setTasks={(updated) => {
          setTasks(updated);
          setRefreshStats((prev) => prev + 1); // 🔥 trigger stats refresh
        }}
      />
    </div>
  );
}

export default Dashboard;
