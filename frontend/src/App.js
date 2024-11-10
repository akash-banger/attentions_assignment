import { Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import Chat from "./components/pages/Chat";
import Home from "./components/pages/home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat/:userId" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
