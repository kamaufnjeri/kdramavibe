// Import components
import Banner from "@/components/common/Banner";
import KactorsFilterSection from "@/components/kactors/KactorsFilterSection";
import KactorsList from "@/components/kactors/KactorsList";
// Import interface for filter params
import { KactorsFilter } from "@/interfaces";
// Import API function to fetch kactors
import getKactors from "@/lib/getKactors";
import { notFound } from "next/navigation";
import React from "react";

// Define props for the page
interface PageProps {
  searchParams?: Promise<KactorsFilter>; // Optional search parameters
}

/**
 * KActorsPage component
 * Fetches Kactors based on searchParams and renders the banner, filter section, and list.
 *
 * @param {PageProps} searchParams - Optional search parameters for filtering Kactors.
 * @returns {Promise<JSX.Element>} The rendered KActors page.
 */
export default async function KActorsPage({ searchParams }: PageProps) {
  // Await and destructure search parameters with default values
  const { name = "", age = "", gender = "", ordering = "", page = "1" } =
    (await searchParams) ?? {};

  // Fetch Kactors data from backend/API
  const kactorsResponse = await getKactors({ name, age, gender, ordering, page });

  if (!kactorsResponse) {
    notFound();
  }

  return (
    <div>
      {/* Banner section */}
      <Banner />

      {/* Filter section with current search parameters */}
      <KactorsFilterSection
        searchParams={{
          name,
          gender,
          age,
          ordering,
          page,
        }}
        noOfPages={kactorsResponse.total_pages}
      />

      {/* Render list of Kactors */}
      <KactorsList kactors={kactorsResponse?.results} />
    </div>
  );
}
