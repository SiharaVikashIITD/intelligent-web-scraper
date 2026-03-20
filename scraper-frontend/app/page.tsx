"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        "https://intelligent-web-scraper.onrender.com/scrape",
        {
          method: "POST",
        }
      );

      if (!res.ok) {
        throw new Error(`Server Error: ${res.status}`);
      }

      const result = await res.json();

      if (!result) {
        throw new Error("No response from API");
      }

      let extractedData = result?.data;

      if (!Array.isArray(extractedData)) {
        console.warn("Invalid API format:", result);
        extractedData = [];
      }

      setData(extractedData);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-10">
      <h1 className="text-3xl font-bold mb-6">
        Intelligent Web Scraper 🚀
      </h1>

      <button
        onClick={fetchData}
        className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition"
      >
        {loading ? "Scraping..." : "Run Scraper"}
      </button>

      {error && (
        <p className="text-red-500 mt-4">
          ❌ {error}
        </p>
      )}

      {loading && (
        <p className="mt-4 text-gray-600">
          ⏳ Scraping data... (first run may take ~30s)
        </p>
      )}

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.slice(0, 20).map((item, index) => (
          <div
            key={index}
            className="bg-white p-4 rounded-xl shadow hover:shadow-md transition"
          >
            <h2 className="font-semibold text-lg mb-2">
              {item.title}
            </h2>
            <p>💰 £{item.price}</p>
            <p>📦 {item.availability}</p>
          </div>
        ))}
      </div>
    </div>
  );
}