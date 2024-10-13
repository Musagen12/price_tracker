import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register the necessary chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);
// GraphWithForm Component
const GraphWithForm = ({ labels, dataPoints, productId }) => {
  const [notification, setNotification] = useState(null);
  const [targetPrice, setTargetPrice] = useState('');
  const [email, setEmail] = useState('');

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Price over Time',
        data: dataPoints,
        fill: false,
        borderColor: 'rgba(75,192,192,1)',
        tension: 0.1,
      },
    ],
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!productId) {
      setNotification('Product ID is required.');
      return;
    }
  
    try {
      const response = await fetch('/api/sendEmail', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, targetPrice, productId })  // Include productId
      });
  
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const result = await response.json();
        if (response.ok) {
          setNotification('Email sent successfully!');
        } else {
          setNotification(result.error || 'Failed to send email. Please try again.');
        }
      } else {
        const text = await response.text();
        setNotification('An unexpected error occurred.');
      }
    } catch (error) {
      setNotification('An error occurred while sending the email.');
    }
  
    setTargetPrice('');
    setEmail('');
  };
  

  return (
    <div className="flex flex-col h-screen p-4 bg-white">
      <div className="flex flex-1 space-x-4">
        <div className="flex-1 h-full">
          <Line data={data} />
        </div>

        <div className="w-80">
          <h2 className="text-lg font-bold mb-4">Set Target & Notify</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="id" className="block text-sm font-medium leading-6 text-gray-900">
                Product ID
              </label>
              <div className="mt-2">
                <input
                  id="id"
                  name="id"
                  type="text"
                  value={productId}
                  readOnly
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <label htmlFor="target" className="block text-sm font-medium leading-6 text-gray-900">
                Target Price
              </label>
              <div className="mt-2">
                <input
                  id="target"
                  name="target"
                  type="number"
                  value={targetPrice}
                  onChange={(e) => setTargetPrice(e.target.value)}
                  required
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                Email Address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Set Target
              </button>
            </div>
          </form>

          {notification && (
            <div className="mt-4 p-3 rounded-md bg-green-100 text-green-800 flex items-center">
              <span>{notification}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GraphWithForm;
