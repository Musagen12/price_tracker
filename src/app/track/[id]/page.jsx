'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogBackdrop, DialogPanel, TransitionChild } from '@headlessui/react';
import {
  Bars3Icon,
  ChartPieIcon,
  DocumentDuplicateIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { useParams } from 'next/navigation';
import axios from 'axios';
import Image from 'next/image';
import NavbarDashboard from '@/components/NavbarDashboard';
import ChatBot from '@/components/ChatBot';
import Graph from '@/components/Graph';

const navigation = [
  { name: 'Product Information', key: 'info', icon: DocumentDuplicateIcon },
  { name: 'Price Graph', key: 'graph', icon: ChartPieIcon },
  { name: 'Chat with AI', key: 'chat', icon: Bars3Icon },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function TrackItem() {
  const params = useParams();
  const { id } = params; 
  const [graphData, setGraphData] = useState({ labels: [], dataPoints: [] });   
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('info');
  const [products, setProducts] = useState([]);
  const [jumiaProducts, setJumiaProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [productUrl, setProductUrl] = useState('');
  const [platform, setPlatform] = useState(null); // 'amazon' or 'jumia'


  useEffect(() => {
    const fetchGraphDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/amazon/graph_details/${id}`);
        const productDetails = response.data.products;

        // Extracting labels (timestamps) and data points (prices)
        const labels = productDetails.map((product) =>
          new Date(product.timestamp).toLocaleString()
        );
        const dataPoints = productDetails.map((product) => product.price);

        // Update state with the extracted graph data
        setGraphData({ labels, dataPoints });
      } catch (error) {
        console.error("Error fetching graph details:", error);
      }
    };

    fetchGraphDetails();
  }, [id]);

  useEffect(() => {
    if (!id) return;  
    const fetchItemData = async () => {
      setLoading(true);
      setError(null);
      console.log('Tracking ID:', id); // Log the ID for debugging
  
      try {
        // Attempt to fetch Jumia product data
        const jumiaResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jumia/frontend_data/${id}`);
        console.log('Jumia Response:', jumiaResponse.data); // Log the response for debugging
        
        if (jumiaResponse.data) {
          setJumiaProducts([jumiaResponse.data]);
          setPlatform('jumia');
        }
      } catch (jumiaError) {
        console.error('Error fetching Jumia data:', jumiaError.response?.data || jumiaError.message);
        
        try {
          // If Jumia fetch fails, attempt to fetch Amazon product data
          const amazonResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/amazon/frontend_data/${id}`);
          console.log('Amazon Response:', amazonResponse.data); // Log the response for debugging
          
          if (amazonResponse.data) {
            setProducts([amazonResponse.data]);
            setPlatform('amazon');
          }
        } catch (amazonError) {
          console.error('Error fetching Amazon data:', amazonError.response?.data || amazonError.message);
          setError('No product data available for the given ID.');
        }
      } finally {
        setLoading(false);
      }
    };
  
    fetchItemData();
  }, [id]);
  

  // Fetch product URL based on ID
useEffect(() => {
  const fetchTrackedUrl = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/amazon/get_tracked_url`);
      const trackedUrls = response.data;

      // Find the URL with the matching ID
      const trackedUrlObj = trackedUrls.find(urlObj => urlObj.id === id);
      if (trackedUrlObj) {
        setProductUrl(trackedUrlObj.url);
      } else {
        console.error('No tracked URL found for the given ID');
      }
    } catch (error) {
      console.error('Error fetching tracked URL:', error);
    }
  };

  fetchTrackedUrl();
}, [id]);


  // Function to handle the AI chat button click
const handleChatClick = () => {
  if (!productUrl) {
    alert('Product URL not found!');
    return;
  }

  // Generate a .txt filename
  const filename = `product_${new Date().getTime()}.txt`;

  // Save the filename to local storage
  sessionStorage.setItem('filename', filename);

  // Print the URL and filename to the console
  console.log('Product URL:', productUrl);
  console.log('Filename:', filename);

  // Post the product URL and filename to the appropriate endpoint
  axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/amazon/get_comments`, {
    url: productUrl,
    file_name: filename,
  })
  .then(response => {
    alert('File and product URL sent successfully.');
  })
  .catch(error => {
    console.error('Error posting data:', error);
    alert('Failed to send file and product URL.');
  });
};

const renderContent = () => {
  switch (activeTab) {
    case 'info':
      return (
        <div className="p-4 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Product Details</h2>
          
          {/* Loading Button */}
          <button
            disabled
            type="button"
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center mb-4"
          >
            <svg
              aria-hidden="true"
              role="status"
              className="inline w-4 h-4 me-3 text-white animate-spin"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="#E5E7EB"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentColor"
              />
            </svg>
            scraping data...
          </button>

          {/* Conditional Rendering Based on Platform */}
          {platform === 'jumia' && jumiaProducts.length > 0 ? (
            jumiaProducts.map((product) => (
              <div key={product.id} className="bg-gray-50 shadow rounded p-4 mb-4">
                <Image
                  src={product.image_source}
                  alt={product.name}
                  width={500}
                  height={500}
                  className="w-200 h-180 object-cover"
                />
                <h3 className="text-lg font-semibold">{product.name}</h3>
                <p className="text-gray-700">
                  Price: <span className="font-medium">${product.price}</span>
                </p>
                <p className="text-gray-700">
                  Rating: <span className="font-medium">{product.rating}</span>
                </p>
                <p className="text-gray-700">
                  In Stock: <span className="font-medium">{product.in_stock}</span>
                </p>           
                <p className="text-gray-500 text-sm mt-2">
                  Last Updated: {new Date(product.timestamp).toLocaleString()}
                </p>
              </div>
            ))
          ) : platform === 'amazon' && products.length > 0 ? (
            products.map((product) => (
              <div key={product.id} className="bg-gray-50 shadow rounded p-4 mb-4">
                <Image
                  src={product.image_source}
                  alt={product.name}
                  width={500}
                  height={500}
                  className="w-200 h-180 object-cover"
                />
                <h3 className="text-lg font-semibold">{product.name}</h3>
                <p className="text-gray-700">
                  Price: <span className="font-medium">${product.price}</span>
                </p>
                <p className="text-gray-700">
                  Rating: <span className="font-medium">{product.rating}</span>
                </p>
                <p className="text-gray-700">
                  In Stock: <span className="font-medium">{product.in_stock}</span>
                </p>
                {/* <a
                  href={product.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 underline"
                >
                  View on Amazon
                </a> */}
                <p className="text-gray-500 text-sm mt-2">
                  Last Updated: {new Date(product.timestamp).toLocaleString()}
                </p>
              </div>
            ))
          ) : (
            <p>No product data available.</p>
          )}
        </div>
      );

    case 'graph':
      return (
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-4">Product Price Graph</h2>
          {graphData.labels.length > 0 ? (
            <Graph labels={graphData.labels} dataPoints={graphData.dataPoints} />
          ) : (
            <p>Loading graph data...</p>
          )}
        </div>
      );

    case 'chat':
      return (
        <div className="p-4 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Chat with AI</h2>
          <button
            onClick={handleChatClick}
            className="mt-4 text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            Load product Data to AI
          </button>
          {/* ChatBot component */}
          <ChatBot />
        </div>
      );

    default:
      return null;
  }
};

  

  return (
    <>
    <div className="fixed top-0 left-0 right-0 z-50 bg-white shadow"> 
      <NavbarDashboard />
    </div>
      
      <Dialog open={sidebarOpen} onClose={() => setSidebarOpen(false)} className="relative z-50 lg:hidden">
        <DialogBackdrop className="fixed inset-0 bg-gray-900/80 transition-opacity duration-300 ease-linear" />
        <div className="fixed inset-0 flex">
          <DialogPanel className="relative mr-16 flex w-full max-w-xs flex-1 transform transition duration-300 ease-in-out">
            <TransitionChild>
              <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                <button type="button" onClick={() => setSidebarOpen(false)} className="-m-2.5 p-2.5">
                  <span className="sr-only">Close sidebar</span>
                  <XMarkIcon aria-hidden="true" className="h-6 w-6 text-white" />
                </button>
              </div>
            </TransitionChild>
            <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-2 ">
              <nav className="flex flex-1 flex-col">
                <ul role="list" className="flex flex-1 flex-col gap-y-7 mt-5">
                  {navigation.map((item) => (
                    <li key={item.key}>
                      <button
                        onClick={() => setActiveTab(item.key)}
                        className={classNames(
                          activeTab === item.key ? 'bg-gray-50 text-indigo-600' : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600',
                          'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6'
                        )}
                      >
                        <item.icon
                          aria-hidden="true"
                          className={classNames(
                            activeTab === item.key ? 'text-indigo-600' : 'text-gray-400 group-hover:text-indigo-600',
                            'h-6 w-6 shrink-0'
                          )}
                        />
                        {item.name}
                      </button>
                    </li>
                  ))}
                </ul>
              </nav>
            </div>
          </DialogPanel>
        </div>
      </Dialog>

      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col mt-16"> 
  <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6">
    <nav className="flex flex-1 flex-col">
      <ul role="list" className="flex flex-1 flex-col gap-y-7">
        {navigation.map((item) => (
          <li key={item.key}>
            <button
              onClick={() => setActiveTab(item.key)}
              className={classNames(
                activeTab === item.key ? 'bg-gray-50 text-indigo-600' : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600',
                'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6'
              )}
            >
              <item.icon
                aria-hidden="true"
                className={classNames(
                  activeTab === item.key ? 'text-indigo-600' : 'text-gray-400 group-hover:text-indigo-600',
                  'h-6 w-6 shrink-0'
                )}
              />
              {item.name}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  </div>
</div>



      <div className="sticky top-0 z-40 flex items-center gap-x-6 bg-white px-4 py-4 shadow-sm sm:px-6 lg:hidden">
        <button type="button" onClick={() => setSidebarOpen(true)} className="-m-2.5 p-2.5 text-gray-700 lg:hidden">
          <span className="sr-only">Open sidebar</span>
          <Bars3Icon aria-hidden="true" className="h-6 w-6" />
        </button>
        <div className="flex-1 text-sm font-semibold leading-6 text-gray-900">Track Item</div>
      </div>

      <main className="py-10 lg:pl-72">
        <div className="px-4 sm:px-6 lg:px-8">
          {renderContent()}
        </div>
      </main>
    </>
  );
}