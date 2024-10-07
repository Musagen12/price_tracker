import Image from 'next/image'
import clsx from 'clsx'

import { Container } from '@/components/Container'
import {
  Expandable,
  ExpandableButton,
  ExpandableItems,
} from '@/components/Expandable'
import avatarImage3 from '@/images/avatars/avatar-3.png'
import avatarImage4 from '@/images/avatars/avatar-4.png'
import avatarImage5 from '@/images/avatars/avatar-5.png'
import avatarImage6 from '@/images/avatars/avatar-6.png'
import avatarImage7 from '@/images/avatars/avatar-7.png'
import avatarImage8 from '@/images/avatars/avatar-8.png'
import avatarImage9 from '@/images/avatars/avatar-9.png'
import avatarImage10 from '@/images/avatars/avatar-10.png'
import avatarImage11 from '@/images/avatars/avatar-11.png'

const testimonials = [
  [
    {
      content:
        'This tool has made collecting product data from Jumia a breeze. It saved me hours of manual work!',
      author: {
        name: 'Antonio Littel',
        role: 'eCommerce Manager',
        image: avatarImage3,
      },
    },
    {
      content:
        'I used this scraper to monitor prices on Amazon for my dropshipping business. The real-time data updates are game-changing.',
      author: {
        name: 'Lynn Nolan',
        role: 'Entrepreneur',
        image: avatarImage4,
      },
    },
    {
      content:
        'The accuracy and speed of the data collection from both Amazon and Jumia have helped me stay ahead in a competitive market.',
      author: {
        name: 'Krista Prosacco',
        role: 'Market Analyst',
        image: avatarImage9,
      },
    },
  ],
  [
    {
      content:
        'I run an online store and needed a way to track competitor prices. This platform delivered exactly what I needed.',
      author: {
        name: 'Cameron Considine',
        role: 'Store Owner',
        image: avatarImage7,
      },
    },
    {
      content:
        'The automation of product scraping from Amazon has helped me quickly identify trending products, increasing my profits.',
      author: {
        name: 'Regina Wisoky',
        role: 'Data Scientist',
        image: avatarImage11,
      },
    },
    {
      content:
        'I use this scraper to analyze customer reviews for products on Jumia, and it’s been an invaluable tool for improving my own products.',
      author: {
        name: 'Vernon Cummerata',
        role: 'Product Manager',
        image: avatarImage8,
      },
    },
  ],
  [
    {
      content:
        'As a startup founder, staying up-to-date with market trends is critical. This tool lets me track and analyze key data effortlessly.',
      author: {
        name: 'Steven Hackett',
        role: 'Startup Founder',
        image: avatarImage5,
      },
    },
    {
      content:
        'The user interface is so intuitive, and the data I get is spot-on. I can now focus more on making data-driven decisions rather than data collection.',
      author: {
        name: 'Carla Schoen',
        role: 'Business Analyst',
        image: avatarImage10,
      },
    },
    {
      content:
        'I can’t recommend this enough. It’s the best tool for scraping Amazon and Jumia data that I’ve come across.',
      author: {
        name: 'Leah Kiehn',
        role: 'Operations Manager',
        image: avatarImage6,
      },
    },
  ],
]

function Testimonial({ author, children }) {
  return (
    <figure className="rounded-4xl p-8 shadow-md ring-1 ring-slate-900/5">
      <blockquote>
        <p className="text-lg tracking-tight text-slate-900 before:content-['“'] after:content-['”']">
          {children}
        </p>
      </blockquote>
      <figcaption className="mt-6 flex items-center">
        <div className="overflow-hidden rounded-full bg-slate-50">
          <Image
            className="h-12 w-12 object-cover"
            src={author.image}
            alt=""
            width={48}
            height={48}
          />
        </div>
        <div className="ml-4">
          <div className="text-base font-medium leading-6 tracking-tight text-slate-900">
            {author.name}
          </div>
          <div className="mt-1 text-sm text-slate-600">{author.role}</div>
        </div>
      </figcaption>
    </figure>
  )
}

export function Testimonials() {
  return (
    <section className="py-8 sm:py-10 lg:py-16">
      <Container className="text-center">
        <h2 className="font-display text-4xl font-bold tracking-tight text-slate-900">
          What Our Users Are Saying
        </h2>
        <p className="mt-4 text-lg tracking-tight text-slate-600">
          Discover how our tool is helping entrepreneurs, analysts, and eCommerce professionals make smarter decisions with data from Amazon and Jumia.
        </p>
      </Container>
      <Expandable className="group mt-16">
        <ul
          role="list"
          className="mx-auto grid max-w-2xl grid-cols-1 gap-8 px-4 lg:max-w-7xl lg:grid-cols-3 lg:px-8"
        >
          {testimonials
            .map((column) => column[0])
            .map((testimonial, testimonialIndex) => (
              <li key={testimonialIndex} className="lg:hidden">
                <Testimonial author={testimonial.author}>
                  {testimonial.content}
                </Testimonial>
              </li>
            ))}
          {testimonials.map((column, columnIndex) => (
            <li
              key={columnIndex}
              className="hidden group-data-[expanded]:list-item lg:list-item"
            >
              <ul role="list">
                <ExpandableItems>
                  {column.map((testimonial, testimonialIndex) => (
                    <li
                      key={testimonialIndex}
                      className={clsx(
                        testimonialIndex === 0 && 'hidden lg:list-item',
                        testimonialIndex === 1 && 'lg:mt-8',
                        testimonialIndex > 1 && 'mt-8',
                      )}
                    >
                      <Testimonial author={testimonial.author}>
                        {testimonial.content}
                      </Testimonial>
                    </li>
                  ))}
                </ExpandableItems>
              </ul>
            </li>
          ))}
        </ul>
        <ExpandableButton>Read more testimonials</ExpandableButton>
      </Expandable>
    </section>
  )
}
