// src/app/page.jsx
'use client';

import { useState } from 'react';
import Image from 'next/image';
import axios from 'axios';
import Link from 'next/link'; // Import Link for client-side navigation
import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
} from '@headlessui/react';
import {
  Bars3Icon,
  BellIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Example() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchInput, setSearchInput] = useState('');
  const [amazonResults, setAmazonResults] = useState([]);
  const [jumiaResults, setJumiaResults] = useState([]);
  const [tracking, setTracking] = useState({});
  const [error, setError] = useState(''); // State for error messages
  const [loadingAmazon, setLoadingAmazon] = useState(false); // State for loading Amazon
  const [loadingJumia, setLoadingJumia] = useState(false); // State for loading Jumia

  const handleSearch = async (e) => {
    e.preventDefault();
    setError(''); // Reset error message
    setLoadingAmazon(true); // Start loading for Amazon
    setLoadingJumia(true); // Start loading for Jumia

    try {
      // Fetch Amazon results
      const amazonResponse = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/amazon/search`, {
        query: searchInput,
      });
      console.log('Amazon results:', amazonResponse.data);
      setAmazonResults(amazonResponse.data.products);

      // Fetch Jumia results
      const jumiaResponse = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jumia/search`, {
        query: searchInput,
      });
      console.log('Jumia results:', jumiaResponse.data);
      setJumiaResults(jumiaResponse.data.products);
    } catch (error) {
      console.error('Error fetching search results:', error.response?.data || error.message);
      setError(`Error fetching search results: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoadingAmazon(false); // Stop loading for Amazon
      setLoadingJumia(false); // Stop loading for Jumia
    }
  };

  const handleTrackAmazonItem = async (item) => {
    setTracking((prev) => ({ ...prev, [item.asin]: true }));
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/amazon/add_tracked_url`, {
        url: item.url,
      });
      console.log('Tracked Amazon item:', response.data);
      const trackedId = response.data.id; // Assuming 'id' is returned
      window.location.href = `/track/${trackedId}`;
    } catch (error) {
      console.error('Error tracking Amazon item:', error.response?.data || error.message);
      alert(`Failed to track item: ${error.response?.data?.detail || error.message}`);
    } finally {
      setTracking((prev) => ({ ...prev, [item.asin]: false }));
    }
  };

  const handleTrackJumiaItem = async (item) => {
    setTracking((prev) => ({ ...prev, [item.url]: true }));
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jumia/add_tracked_url`, {
        url: item.url,
      });
      console.log('Tracked Jumia item:', response.data);
      const trackedId = response.data.id; // Assuming 'id' is returned
      window.location.href = `/track/${trackedId}`;
    } catch (error) {
      console.error('Error tracking Jumia item:', error.response?.data || error.message);
      alert(`Failed to track item: ${error.response?.data?.detail || error.message}`);
    } finally {
      setTracking((prev) => ({ ...prev, [item.url]: false }));
    }
  };

  return (
    <>
      <div>
        {/* Sidebar Dialog */}
        <Dialog open={sidebarOpen} onClose={() => setSidebarOpen(false)} className="relative z-50 lg:hidden">
          <DialogBackdrop className="fixed inset-0 bg-gray-900/80 transition-opacity duration-300 ease-linear" />
          <div className="fixed inset-0 flex">
            <DialogPanel className="relative flex w-full max-w-xs flex-1 transform transition duration-300 ease-in-out">
              <div className="absolute left-full top-0 flex w-16 justify-center pt-5 duration-300 ease-in-out">
                <button type="button" onClick={() => setSidebarOpen(false)} className="-m-2.5 p-2.5">
                  <span className="sr-only">Close sidebar</span>
                </button>
              </div>
              {/* Sidebar content goes here */}
            </DialogPanel>
          </div>
        </Dialog>

        {/* Header */}
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button type="button" onClick={() => setSidebarOpen(true)} className="-m-2.5 p-2.5 text-gray-700 lg:hidden">
            <span className="sr-only">Open sidebar</span>
            <Bars3Icon aria-hidden="true" className="h-6 w-6" />
          </button>

          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <form onSubmit={handleSearch} className="relative flex flex-1">
              <label htmlFor="search-field" className="sr-only">Search</label>
              <MagnifyingGlassIcon
                aria-hidden="true"
                className="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-gray-400"
              />
              <input
                id="search-field"
                name="search"
                type="search"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search item ..."
                className="block h-full w-full border-0 py-0 pl-8 pr-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
              />
              <button type="submit" className="hidden">Search</button>
            </form>
            <div className="flex items-center gap-x-4 lg:gap-x-6">
              <button type="button" className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
                <span className="sr-only">View notifications</span>
                <BellIcon aria-hidden="true" className="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <main className="px-4 py-10 sm:px-6 lg:px-8 lg:py-6">
          <h1 className="text-xl font-bold mb-4">Scraped Data</h1>
          {error && <p className="text-red-500">{error}</p>} {/* Display error messages */}
          <div className="flex space-x-4">
            {/* Left Column - Amazon */}
            <div className="flex-1 p-4 border-r border-gray-300">
              <h2 className="font-semibold">Amazon</h2>
              {loadingAmazon && (
                <button disabled type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center mb-4">
                  <svg aria-hidden="true" role="status" className="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                  </svg>
                  Scraping data this may take time...
                </button>
              )}
              <ul className="list-disc pl-5">
                {amazonResults.length > 0 ? (
                  amazonResults.map((item) => (
                    <li key={item.asin} className="mb-4">
                      <Image src={item.image_url} alt={item.name} width={100} height={100} />
                      <h3 className="text-lg font-bold">{item.name}</h3>
                      <p className="text-gray-500">Price: ${item.price}</p>
                      <p className="text-gray-500">Rating: {item.rating}</p>
                      <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">View on Amazon</a>
                      {/* Track Item Button */}
                      <div className="mt-2">
                        {tracking[item.asin] ? (
                          <button disabled className="px-3 py-1 bg-gray-400 text-white rounded">
                            Tracking...
                          </button>
                        ) : (
                          <button
                            onClick={() => handleTrackAmazonItem(item)}
                            disabled={tracking[item.asin]}
                            className={`px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 ${tracking[item.asin] ? 'opacity-50 cursor-not-allowed' : ''}`}
                          >
                            Track Item
                          </button>
                        )}
                      </div>
                    </li>
                  ))
                ) : (
                  <p>No results found.</p>
                )}
              </ul>
            </div>

            {/* Right Column - Jumia */}
            <div className="flex-1 p-4">
              <h2 className="font-semibold">Jumia</h2>
              {loadingJumia && (
                <button disabled type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center mb-4">
                  <svg aria-hidden="true" role="status" className="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                  </svg>
                  scraping data this may take time...
                </button>
              )}
              <ul className="list-disc pl-5">
                {jumiaResults.length > 0 ? (
                  jumiaResults.map((item) => (
                    <li key={item.url} className="mb-4">
                      <Image src={item.image_url} alt={item.name} width={100} height={100} />
                      <h3 className="text-lg font-bold">{item.name}</h3>
                      <p className="text-gray-500">Price: ${item.price}</p>
                      <p className="text-gray-500">Rating: {item.rating}</p>
                      <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">View on Jumia</a>
                      {/* Track Item Button */}
                      <div className="mt-2">
                        {tracking[item.url] ? (
                          <button disabled className="px-3 py-1 bg-gray-400 text-white rounded">
                            Tracking...
                          </button>
                        ) : (
                          <button
                            onClick={() => handleTrackJumiaItem(item)}
                            disabled={tracking[item.url]}
                            className={`px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 ${tracking[item.url] ? 'opacity-50 cursor-not-allowed' : ''}`}
                          >
                            Track Item
                          </button>
                        )}
                      </div>
                    </li>
                  ))
                ) : (
                  <p>No results found.</p>
                )}
              </ul>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
