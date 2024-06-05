import React from "react";

function Note({ note, onDelete, onEdit }) {
	return (
		<div className="">
			<p className="">{note.title}</p>
			<p className="">{note.content}</p>
			<button className="" onClick={() => onDelete(note.id)}>
				Delete
			</button>
		</div>
	);
}

export default Note;
