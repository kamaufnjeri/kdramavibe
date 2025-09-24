"use client";

import React, { useState } from "react";

// Sample data
const dramas = [
  { title: "Angel Eyes", year: 2014 },
  { title: "Ang Shim Jung", year: 2010 },
  { title: "Crash Landing on You", year: 2019 },
  { title: "Extraordinary You", year: 2019 },
  { title: "18 Again", year: 2020 },
  { title: "Boys Over Flowers", year: 2009 },
  { title: "20th Century Girl", year: 2022 },
  { title: "Alice", year: 2020 },
];

// Group dramas by first letter (A-Z, 0-9)
const groupDramas = (list: typeof dramas) => {
  const groups: { [key: string]: typeof dramas } = {};

  list.forEach((drama) => {
    let firstChar = drama.title[0].toUpperCase();
    if (!/[A-Z]/.test(firstChar)) firstChar = "0-9";

    if (!groups[firstChar]) groups[firstChar] = [];
    groups[firstChar].push(drama);
  });

  // Sort letters
  return Object.keys(groups)
    .sort()
    .reduce((obj, key) => {
      obj[key] = groups[key].sort((a, b) => a.title.localeCompare(b.title));
      return obj;
    }, {} as typeof groups);
};

export default function KDramaPage() {
  const [search, setSearch] = useState("");
  const grouped = groupDramas(
    dramas.filter((d) =>
      d.title.toLowerCase().includes(search.toLowerCase())
    )
  );

  return (
    <div className="min-h-screen bg-pink-50 text-pink-900">
      {/* Header */}
      <header className="p-6 bg-pink-200 shadow-md">
        <h1 className="text-4xl font-bold text-center">KDramaVibe</h1>
        <p className="text-center mt-2 text-pink-800">
          Explore your favorite K-Dramas by title and year
        </p>
      </header>

      {/* Search bar */}
      <div className="p-6 flex justify-center">
        <input
          type="text"
          placeholder="Search dramas..."
          className="w-full max-w-md p-2 rounded border-2 border-pink-300 focus:outline-none focus:ring-2 focus:ring-pink-400"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Alphabet navigation */}
      <div className="flex flex-wrap justify-center gap-2 px-6 mb-6">
        {Object.keys(grouped).map((letter) => (
          <a
            key={letter}
            href={`#${letter}`}
            className="px-3 py-1 rounded bg-pink-200 hover:bg-pink-300 transition"
          >
            {letter}
          </a>
        ))}
      </div>

      {/* Drama listings */}
      <main className="px-6 pb-12">
        {Object.keys(grouped).map((letter) => (
          <section key={letter} id={letter} className="mb-10">
            <h2 className="text-2xl font-semibold mb-4">{letter}</h2>
            <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {grouped[letter].map((drama) => (
                <li
                  key={drama.title}
                  className="p-4 rounded bg-pink-100 hover:bg-pink-200 transition shadow"
                >
                  <span className="font-medium">{drama.title}</span>{" "}
                  <span className="text-pink-800">({drama.year})</span>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </main>

      {/* Footer */}
      <footer className="p-6 bg-pink-200 text-center">
        <p className="text-pink-800">
          &copy; 2025 KDramaVibe. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
