import Banner from "@/components/common/Banner"; // Top banner for homepage
import KdramasFilterSection from "@/components/kdramas/KdramasFilterSection"; // Filter form for Kdramas
import KdramasList from "@/components/kdramas/KdramasList"; // List display of Kdramas
import { KdramasFilter } from "@/interfaces"; // Interface for filter props
import getKdramas from "@/lib/getKdramas"; // Function to fetch Kdramas data
import { notFound } from "next/navigation";
import React from "react";

interface PageProps {
  searchParams?: Promise<KdramasFilter>; // Optional search/filter parameters
}

// Homepage component displaying Banner, Filter, and Kdramas List
export default async function Home({ searchParams }: PageProps) {
  // Destructure and provide default values for filter params
  const { title = "", genre = "", year = "", ordering = "", page = "1" } =
    (await searchParams) ?? {};

  // Fetch Kdramas from API or database based on filters
  const kdramasResponse = await getKdramas({ title, genre, year, ordering, page });
  if (!kdramasResponse) {
    notFound();
  }

  return (
    <div>
      {/* Banner component */}
      <Banner />

      {/* Filter section with current search params and total pages */}
      <KdramasFilterSection
        searchParams={{
          title,
          genre,
          year,
          ordering,
          page,
        }}
        noOfPages={kdramasResponse.total_pages}
      />

      {/* Display list of Kdramas */}
      <KdramasList kdramas={kdramasResponse?.results} />
    </div>
  );
}
