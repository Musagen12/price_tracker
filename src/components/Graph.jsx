import React from 'react';
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

const GraphWithForm = ({ labels, dataPoints }) => {
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

  return (
    <div className="flex flex-col h-screen p-4 bg-white">
      <div className="flex flex-1 space-x-4">
        {/* Graph Section */}
        <div className="flex-1 h-full">
          <Line data={data} />
        </div>

        {/* Form Section */}
        <div className="w-80">
          <h2 className="text-lg font-bold mb-4">Set Target & Notify</h2>
          <form action="#" method="POST" className="space-y-6">
            <div>
              <label htmlFor="target" className="block text-sm font-medium leading-6 text-gray-900">
                Target Price
              </label>
              <div className="mt-2">
                <input
                  id="target"
                  name="target"
                  type="number"
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
                  required
                  autoComplete="email"
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
        </div>
      </div>
    </div>
  );
};

export default GraphWithForm;
