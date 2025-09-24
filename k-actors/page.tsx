// app/actors/page.tsx
export default function ActorsPage() {
  // Example list of actors
  const actors = [
    "Ahn Hyo-seop",
    "Bae Suzy",
    "Cha Eun-woo",
    "Donghae",
    "Eun Ji-won",
    "Faker Kim", // just an example
    "Gong Yoo",
    "Ha Ji-won",
  ];

  const letters = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));

  return (
    <main className="bg-pink-50 min-h-screen font-sans">
      {/* Hero Section */}
      <section className="bg-pink-100 p-12 text-center rounded-b-3xl shadow-md">
        <h1 className="text-5xl font-bold text-pink-700 mb-4">KDrama Actors</h1>
        <p className="text-pink-800 text-lg">
          Browse your favorite Korean actors by name!
        </p>
      </section>

      {/* Alphabet Navigation */}
      <nav className="flex flex-wrap justify-center gap-2 mt-6 mb-8 px-4">
        {letters.map((letter) => (
          <button
            key={letter}
            className="bg-pink-200 text-pink-700 px-3 py-1 rounded-full hover:bg-pink-300 transition-colors duration-200"
          >
            {letter}
          </button>
        ))}
      </nav>

      {/* Actor List */}
      <section className="p-8">
        {letters.map((letter) => {
          const filtered = actors.filter(
            (actor) => actor.charAt(0).toUpperCase() === letter
          );

          if (filtered.length === 0) return null;

          return (
            <div key={letter} className="mb-10">
              <h2 className="text-2xl font-semibold text-pink-600 mb-4">{letter}</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {filtered.map((actor) => (
                  <div
                    key={actor}
                    className="bg-white text-pink-700 font-medium p-4 rounded-xl text-center shadow-md hover:bg-pink-100 transition-colors duration-300"
                  >
                    {actor}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </section>

      {/* Footer */}
      <footer className="bg-pink-200 text-pink-900 p-6 text-center mt-12 rounded-t-3xl">
        <p>&copy; 2025 KDrama Actors Catalog. All rights reserved.</p>
        <p>Find your favorite actor quickly!</p>
      </footer>
    </main>
  );
}
