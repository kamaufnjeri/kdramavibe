// Import the KactorDetails component to display individual Kactor info
import KactorDetails from "@/components/kactors/KactorDetails";
// Import the function that fetches a single Kactor by slug
import getSingleKactor from "@/lib/getSingleKactor";
// Import Next.js helper to trigger 404 page
import { notFound } from "next/navigation";

// Define the props type for this page
interface PageProps {
  params: Promise<{
    slug: string; // slug comes from the URL: /k-actors/[slug]
  }>;
}

/**
 * SingleKactorPage component
 * Fetches a single Kactor by slug and renders the KactorDetails component.
 *
 * @param {PageProps} params - The page parameters containing the slug.
 */
export default async function SingleKactorPage({ params }: PageProps) {
  const { slug } = await params; // Extract slug from URL params


    const kactor = await getSingleKactor(slug);

    // If API returned nothing, trigger Next.js 404 page
    if (!kactor) {
      notFound();
    }

    return (
      // Wrapper container for styling
      <div className="flex justify-center m-4 p-4">
        <KactorDetails kactor={kactor} />
      </div>
    );
  
}
