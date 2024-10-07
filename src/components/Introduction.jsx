import Link from 'next/link'
import { CheckIcon } from '@/components/CheckIcon'
import { Container } from '@/components/Container'

export function Introduction() {
  return (
    <section
      id="introduction"
      aria-label="Introduction"
      className="pb-16 pt-20 sm:pb-20 md:pt-36 lg:py-32"
    >
      <Container className="text-lg tracking-tight text-slate-700">
        <p className="font-display text-4xl font-bold tracking-tight text-slate-900">
          Welcome to the Ultimate eCommerce Data Scraper for Amazon and Jumia
        </p>
        <p className="mt-4">
          Our platform helps you easily scrape and analyze real-time data from top
          eCommerce giants like Amazon and Jumia. Whether you need product details, 
          price comparisons, or reviews, our tool gathers accurate and comprehensive 
          information to empower your business decisions.
        </p>
        <p className="mt-4">
          With just a few clicks, you can automate your data collection process and 
          stay ahead in the competitive market by accessing the latest trends and insights.
        </p>
        <ul role="list" className="mt-8 space-y-3">
          {[
            'Scrape product listings, prices, reviews, and ratings from Amazon and Jumia',
            'Access real-time updates to track price changes and product availability',
            'Get detailed analytics for better decision-making and market insights',
            'User-friendly interface with automated data extraction',
            'Supports multiple categories including electronics, fashion, and more',
          ].map((feature) => (
            <li key={feature} className="flex">
              <CheckIcon className="h-8 w-8 flex-none fill-blue-500" />
              <span className="ml-4">{feature}</span>
            </li>
          ))}
        </ul>
        <p className="mt-8">
          Experience the power of data scraping for your eCommerce needs. Start analyzing
          products from Amazon and Jumia today and make smarter business decisions.
        </p>
        <p className="mt-10">
          <Link
            href="/dashboard"
            className="text-base font-medium text-blue-600 hover:text-blue-800"
          >
            Get started now <span aria-hidden="true">&rarr;</span>
          </Link>
        </p>
      </Container>
    </section>
  )
}
