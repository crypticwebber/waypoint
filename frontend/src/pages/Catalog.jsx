import { useCallback, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, SlidersHorizontal } from "lucide-react";
import { coursesApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { CourseCard } from "../components/CourseCard";
import { CardGridSkeleton, EmptyState, ErrorState } from "../components/States";

const LEVELS = ["beginner", "intermediate", "advanced"];
const PAGE_SIZE = 9;

export default function Catalog() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const category = searchParams.get("category") || "";
  const level = searchParams.get("level") || "";
  const page = parseInt(searchParams.get("page") || "1", 10);

  const categoriesFetch = useFetch(useCallback(() => coursesApi.categories(), []));

  const coursesFetch = useFetch(
    useCallback(
      () => coursesApi.list({ q: searchParams.get("q") || undefined, category: category || undefined, level: level || undefined, page, page_size: PAGE_SIZE }),
      [searchParams, category, level, page]
    ),
    [searchParams, category, level, page]
  );

  function updateParam(key, value) {
    const next = new URLSearchParams(searchParams);
    if (value) next.set(key, value); else next.delete(key);
    if (key !== "page") next.set("page", "1");
    setSearchParams(next);
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    updateParam("q", query);
  }

  const hasNextPage = coursesFetch.data && coursesFetch.data.length === PAGE_SIZE;

  return (
    <div className="max-w-7xl mx-auto px-5 py-10">
      <h1 className="text-2xl font-display font-semibold mb-1">Course catalog</h1>
      <p className="text-mist mb-7">Find your next module, filtered your way.</p>

      <div className="flex flex-col md:flex-row gap-3 mb-8">
        <form onSubmit={handleSearchSubmit} className="relative flex-1">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-mist" />
          <input
            className="input pl-10" placeholder="Search title, description, or tags…"
            value={query} onChange={(e) => setQuery(e.target.value)}
          />
        </form>
        <div className="flex gap-2">
          <select
            aria-label="Filter by category"
            className="input w-auto" value={category} onChange={(e) => updateParam("category", e.target.value)}
          >
            <option value="">All categories</option>
            {(categoriesFetch.data || []).map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <select
            aria-label="Filter by level"
            className="input w-auto" value={level} onChange={(e) => updateParam("level", e.target.value)}
          >
            <option value="">All levels</option>
            {LEVELS.map((l) => <option key={l} value={l}>{l[0].toUpperCase() + l.slice(1)}</option>)}
          </select>
        </div>
      </div>

      {coursesFetch.isLoading ? (
        <CardGridSkeleton count={9} />
      ) : coursesFetch.error ? (
        <ErrorState description={coursesFetch.error} onRetry={coursesFetch.refetch} />
      ) : coursesFetch.data.length === 0 ? (
        <EmptyState
          icon={SlidersHorizontal}
          title="No courses match those filters"
          description="Try a broader search or clear a filter."
          action={<button onClick={() => { setSearchParams({}); setQuery(""); }} className="btn-secondary">Clear filters</button>}
        />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {coursesFetch.data.map((course) => <CourseCard key={course.id} course={course} />)}
          </div>
          <div className="flex items-center justify-center gap-3 mt-10">
            <button
              className="btn-secondary text-sm" disabled={page <= 1}
              onClick={() => updateParam("page", String(page - 1))}
            >
              Previous
            </button>
            <span className="text-sm text-mist font-mono">Page {page}</span>
            <button
              className="btn-secondary text-sm" disabled={!hasNextPage}
              onClick={() => updateParam("page", String(page + 1))}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
