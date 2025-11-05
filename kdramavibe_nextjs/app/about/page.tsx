// Import the AboutDetails component from the components directory
import AboutDetails from "@/components/about/AboutDetails";

/**
 * AboutPage component
 * Renders the AboutDetails component inside a wrapper div.
 * @returns {JSX.Element} The rendered About page.
 */
export default function AboutPage() {
  return (
    // Wrapper div for the AboutDetails component
    <div>
      <AboutDetails />
    </div>
  );
}
