import { Organization } from '@/components/Organization'
import { Footer } from '@/components/Footer'
import { FreeChapters } from '@/components/FreeChapters'
import { Hero } from '@/components/Hero'
import { Introduction } from '@/components/Introduction'
import { NavBar } from '@/components/NavBar'
import { Resources } from '@/components/Resources'
import { Screencasts } from '@/components/Screencasts'
import { Testimonial } from '@/components/Testimonial'
import { Testimonials } from '@/components/Testimonials'
import avatarImage1 from '@/images/avatars/avatar-1.png'
import avatarImage2 from '@/images/avatars/avatar-2.png'

export default function Home() {
  return (
    <>
      <Hero />
      <Introduction />
      <NavBar />      
      <Testimonial
  id="testimonial-from-jessica-lane"
  author={{
    name: 'Jessica Lane',
    role: 'eCommerce Manager',
    image: avatarImage1, // Update this to the image for Jessica Lane
  }}
>
  <p>
    “I was struggling to gather product data efficiently until I discovered this web scraping service. Now I can easily extract the information I need in minutes!”
  </p>
</Testimonial>

<Screencasts />

<Testimonial
  id="testimonial-from-david-mills"
  author={{
    name: 'David Mills',
    role: 'Digital Marketing Specialist',
    image: avatarImage2, // Update this to the image for David Mills
  }}
>
  <p>
    “This service transformed the way I conduct market research. The ease of accessing data from various eCommerce platforms has made my job so much easier.”
  </p>
</Testimonial>

      <Resources />
      <Testimonials />
      <Organization />
      <Footer />
    </>
  )
}
