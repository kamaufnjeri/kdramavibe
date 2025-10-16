'use client';
import { useState } from "react";

const genres = [
  "Romance",
  "Comedy",
  "Thriller",
  "Historical",
  "Fantasy",
  "Action",
  "Mystery",
  "Drama",
  "Melodrama",
  "Romantic Comedy",
];

export default function GenreAutocomplete() {
  const [inputValue, setInputValue] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);

  const filtered = genres.filter((genre) =>
    genre.toLowerCase().includes(inputValue.toLowerCase())
  );

  return (
    <div className="relative w-full sm:w-1/3">
      <input
        type="text"
        placeholder="Type a genre..."
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          setShowSuggestions(true);
        }}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
        className="border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-[color:var(--color-primary)] bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      />

      {showSuggestions && filtered.length > 0 && (
        <ul className=" absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg max-h-48 overflow-y-auto">
          {filtered.map((genre) => (
            <li
              key={genre}
              onMouseDown={() => {
                setInputValue(genre);
                setShowSuggestions(false);
              }}
              className="px-3 py-2 cursor-pointer hover:bg-[color:var(--color-accent)] text-white transition-colors"
            >
              {genre}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
