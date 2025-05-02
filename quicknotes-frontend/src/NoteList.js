import React from "react";

const NoteList = ({ notes, onDelete }) => {
  return (
    <ul className="note-list">
      {notes.map((note) => (
        <li key={note.id}>
          {note.content}
          <button onClick={() => onDelete(note.id)}>X</button>
        </li>
      ))}
    </ul>
  );
};

export default NoteList;
