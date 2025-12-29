function Filters({ setFilter }) {
  return (
    <div className="filters">
      <h3>Filters</h3>

      <button onClick={() => setFilter("all")}>
        All
      </button>

      <button onClick={() => setFilter("today")}>
        Today
      </button>

      <button onClick={() => setFilter("overdue")}>
        Overdue
      </button>

      <button onClick={() => setFilter("upcoming")}>
        Upcoming (7 days)
      </button>
    </div>
  );
}

export default Filters;
