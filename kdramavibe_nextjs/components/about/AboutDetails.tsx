"use client";
import React from "react";
import Link from "next/link";
import Banner from "../common/Banner";
import { FaStar, FaEnvelope, FaGlobe, FaUser, FaFilter } from "react-icons/fa";

export default function AboutDetails() {
  return (
    <div className="flex flex-col gap-10 p-6 lg:px-24 lg:py-12 bg-background text-text">

      {/* Banner Header */}
      <Banner />
      

      {/* Introduction */}
      <section className="rounded-2xl bg-background/80 p-6 shadow-lg">
        <h2 className="text-3xl font-bold mb-4">About KdramaVibe</h2>
        <p className="text-base leading-relaxed">
          I created <strong>KdramaVibe</strong> to showcase the vibrant world of Korean dramas and their actors. 
          Using <strong>Next.js, Django, Scrapy, Python, and TypeScript</strong>, I scraped and structured data from Wikipedia to give you accurate and detailed information. 
          Here you can explore K-Dramas, their casts, airing years, genres, plots, and much more.
        </p>
      </section>

      {/* Features with Flex Row on Large Screens */}
      <section className="rounded-2xl bg-background/80 p-6 shadow-lg flex flex-col lg:flex-row gap-6">
        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-4 flex items-center gap-2">
            <FaUser /> Kactors
          </h2>
          <ul className="space-y-2 text-base">
            <li><FaStar className="inline text-accent mr-2"/>Filter by <strong>name, age, or gender</strong></li>
            <li><FaStar className="inline text-accent mr-2"/>View detailed profiles including: alternate names, biography, age, birthplace, occupations, years active, height, agents, partner/spouse, children, dramas they starred and others</li>
          </ul>
        </div>

        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-4 flex items-center gap-2">
            <FaFilter /> K-Dramas
          </h2>
          <ul className="space-y-2 text-base">
            <li><FaStar className="inline text-accent mr-2"/>Filter by <strong>title, genre, or year</strong></li>
            <li><FaStar className="inline text-accent mr-2"/>Explore details: plot, episodes, seasons, running time, languages, networks, directors, writers, alternate titles, casts and others</li>
            <li><FaStar className="inline text-accent mr-2"/>Navigate seamlessly to the actors involved in each drama</li>
          </ul>
        </div>
      </section>

      {/* Data Source */}
     <section className="rounded-2xl bg-background/80 p-6 shadow-lg">
  <h2 className="text-3xl font-bold mb-4">Data & Sources</h2>
  <p className="text-base leading-relaxed ">
    All data has been researched, scraped, and curated by{" "}
    <Link
      href="http://florakamau.tech/"
      target="_blank"
      rel="noopener noreferrer"
      className="text-accent font-semibold hover:underline"
    >
      me
    </Link>{" "}
    from{" "}
    <Link
      href="https://www.wikipedia.org/"
      target="_blank"
      rel="noopener noreferrer"
      className="text-accent hover:underline"
    >
      Wikipedia
    </Link>{" "}
    (available under the{" "}
    <Link
      href="https://creativecommons.org/licenses/by-sa/3.0/"
      target="_blank"
      rel="noopener noreferrer"
      className="text-accent hover:underline"
    >
      Creative Commons Attribution-ShareAlike License
    </Link>
    ) and{" "}
    <Link
      href="https://dramabeans.com/"
      target="_blank"
      rel="noopener noreferrer"
      className="text-accent hover:underline"
    >
      Dramabeans
    </Link>
    . I used{" "}
    <strong >
      Next.js, Django, Scrapy, Python, and TypeScript
    </strong>{" "}
    to collect, process, and present the information efficiently. All
    trademarks, logos, and images belong to their respective owners.
  </p>
</section>

      {/* Future Developments */}
      <section className="rounded-2xl bg-background/80 p-6 shadow-lg">
        <h2 className="text-3xl font-bold mb-4">Future Developments</h2>
        <ul className="space-y-2 text-base">
          <li><FaStar className="inline text-accent mr-2"/>Reviews for K-dramas and K-actors</li>
          <li><FaStar className="inline text-accent mr-2"/>Enhanced search and filter options with multiple criteria</li>
          <li><FaStar className="inline text-accent mr-2"/>User accounts to save favorite K-Dramas and K-Actors</li>
          <li><FaStar className="inline text-accent mr-2"/>Interactive timelines of K-actors’ careers and K-drama releases</li>
        </ul>
      </section>

      {/* Contact & Portfolio */}
      <section className="rounded-2xl bg-background/80 p-6 shadow-lg flex flex-col lg:flex-row gap-6">
        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-4 flex items-center gap-2"><FaEnvelope /> Contact Me</h2>
          <p className="text-base leading-relaxed">
            Have questions or suggestions? Reach out via: {" "}
            <Link href="https://florakamau.tech/#contact" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
              Contact Me
            </Link>.
          </p>
        </div>
        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-4 flex items-center gap-2"><FaGlobe /> Portfolio</h2>
          <p className="text-base leading-relaxed">
            Explore my other projects and works on my portfolio: {" "}
            <Link href="https://florakamau.tech/" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
              Visit Portfolio
            </Link>.
          </p>
        </div>
      </section>

    </div>
  );
}
