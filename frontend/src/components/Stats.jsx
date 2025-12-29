import { useEffect, useState } from "react";
import api from "../api/axios";

function Stats({ refreshKey }) {
  const [stats, setStats] = useState({
    total_tasks: 0,
    completed_tasks: 0,
    pending: 0,
    completion_percentage: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get("/tasks/progress");
        setStats(res.data);
      } catch (err) {
        console.error("Failed to fetch stats", err);
      }
    };

    fetchStats();
  }, [refreshKey]); // 🔥 re-fetch when tasks change

  return (
    <div className="stats">
      <p>Total <strong>{stats.total_tasks}</strong></p>
      <p>Done <strong>{stats.completed_tasks}</strong></p>
      <p>Pending <strong>{stats.pending}</strong></p>
      <p>Progress <strong>{Math.round(stats.completion_percentage)}%</strong></p>
    </div>
  );
}

export default Stats;
