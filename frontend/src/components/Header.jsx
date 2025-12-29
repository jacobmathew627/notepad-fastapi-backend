function Header({ onLogout }) {
  return (
    <header>
      <h2>📝 Smart Notepad</h2>
      <button onClick={onLogout}>Logout</button>

    </header>

  );
}

export default Header;
