import React, { useEffect, useState } from "react";
import api from "./api";
import NoteForm from "./components/NoteForm";
import NoteList from "./components/NoteList";
import "./App.css";

function App() {
  const [notes, setNotes] = useState([]);

  const fetchNotes = async () => {
    const res = await api.get("/api/notes");
    setNotes(res.data.notes);
  };

  const addNote = async (content) => {
    const res = await api.post("/api/notes", { content });
    setNotes((prev) => [...prev, res.data.note]);
  };

  const deleteNote = async (id) => {
    await api.delete(`/api/notes/${id}`);
    setNotes((prev) => prev.filter((note) => note.id !== id));
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="App">
      <h1>📝 QuickNotes</h1>
      <NoteForm onAddNote={addNote} />
      <NoteList notes={notes} onDelete={deleteNote} />
    </div>
  );
}

export default App;
