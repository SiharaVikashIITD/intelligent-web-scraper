"use client";

import { useState } from "react";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        "https://intelligent-web-scraper.onrender.com/scrape"
      );
      const result = await res.json();
      setData(result.data || []);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-3xl font-bold mb-6">
        Intelligent Web Scraper 🚀
      </h1>

      <button
        onClick={fetchData}
        className="bg-black text-white px-6 py-2 rounded-lg"
      >
        {loading ? "Scraping..." : "Run Scraper"}
      </button>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.slice(0, 20).map((item, index) => (
          <div key={index} className="bg-white p-4 rounded-xl shadow">
            <h2 className="font-semibold">{item.title}</h2>
            <p>💰 £{item.price}</p>
            <p>📦 {item.availability}</p>
          </div>
        ))}
      </div>
    </div>
  );
}