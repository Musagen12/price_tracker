import { useState } from 'react'
import {
  FaceFrownIcon,
  FaceSmileIcon,
  FireIcon,
  HandThumbUpIcon,
  HeartIcon,
} from '@heroicons/react/20/solid'
import { Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'

const moods = [
  { name: 'Excited', value: 'excited', icon: FireIcon, iconColor: 'text-white', bgColor: 'bg-red-500' },
  { name: 'Loved', value: 'loved', icon: HeartIcon, iconColor: 'text-white', bgColor: 'bg-pink-400' },
  { name: 'Happy', value: 'happy', icon: FaceSmileIcon, iconColor: 'text-white', bgColor: 'bg-green-400' },
  { name: 'Sad', value: 'sad', icon: FaceFrownIcon, iconColor: 'text-white', bgColor: 'bg-yellow-400' },
  { name: 'Thumbsy', value: 'thumbsy', icon: HandThumbUpIcon, iconColor: 'text-white', bgColor: 'bg-blue-500' },
  { name: 'I feel nothing', value: null, icon: null, iconColor: 'text-gray-400', bgColor: 'bg-transparent' },
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function ChatBot() {
  const [selected, setSelected] = useState(moods[5])
  const [comment, setComment] = useState('')
  const [generatedText, setGeneratedText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setGeneratedText(`Generated response for: "${comment}"`)
    setComment('')
  }

  return (
    <div className="flex flex-col space-y-4 p-4 bg-gray-100 rounded-lg shadow-md">
      <form onSubmit={handleSubmit} className="relative">
        <div className="overflow-hidden rounded-lg shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-indigo-600">
          <label htmlFor="comment" className="sr-only">Ask AI for any sentiment</label>
          <textarea
            id="comment"
            name="comment"
            rows={3}
            placeholder="Ask Anything about the product ..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            className="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
          />
        </div>

        <div className="absolute inset-x-0 bottom-0 flex justify-between py-2 pl-3 pr-2">
          <div className="flex items-center space-x-5">
            <div className="flex items-center">
              <Listbox value={selected} onChange={setSelected}>
                <Label className="sr-only">Your mood</Label>
                <div className="relative">
                  <ListboxButton className="relative -m-2.5 flex h-10 w-10 items-center justify-center rounded-full text-gray-400 hover:text-gray-500">
                    <span className="flex items-center justify-center">
                      {selected.value === null ? (
                        <span>
                          <FaceSmileIcon aria-hidden="true" className="h-5 w-5 flex-shrink-0" />
                          <span className="sr-only">Add your mood</span>
                        </span>
                      ) : (
                        <span>
                          <span className={classNames(selected.bgColor, 'flex h-8 w-8 items-center justify-center rounded-full')}>
                            {selected.icon ? (
                              <selected.icon aria-hidden="true" className="h-5 w-5 flex-shrink-0 text-white" />
                            ) : (
                              <span aria-hidden="true" className="h-5 w-5 flex-shrink-0 text-gray-400" />
                            )}
                          </span>
                          <span className="sr-only">{selected.name}</span>
                        </span>
                      )}
                    </span>
                  </ListboxButton>

                  <ListboxOptions
                    transition
                    className="absolute z-10 -ml-6 mt-1 w-60 rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none"
                  >
                    {moods.map((mood) => (
                      <ListboxOption
                        key={mood.value}
                        value={mood}
                        className="relative cursor-default select-none bg-white px-3 py-2 data-[focus]:bg-gray-100"
                      >
                        <div className="flex items-center">
                          <div className={classNames(mood.bgColor, 'flex h-8 w-8 items-center justify-center rounded-full')}>
                            {mood.icon ? (
                              <mood.icon aria-hidden="true" className={classNames(mood.iconColor, 'h-5 w-5 flex-shrink-0')} />
                            ) : null}
                          </div>
                          <span className="ml-3 block truncate font-medium">{mood.name}</span>
                        </div>
                      </ListboxOption>
                    ))}
                  </ListboxOptions>
                </div>
              </Listbox>
            </div>
          </div>
          <div className="flex-shrink-0">
            <button
              type="submit"
              className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Ask AI
            </button>
          </div>
        </div>
      </form>

      {/* Display Generated Text */}
      <div className="bg-white p-4 rounded-lg shadow-md mt-4">
        <h2 className="text-lg font-semibold text-gray-800">Product Response:</h2>
        <p className="mt-2 text-gray-600">{generatedText || 'Your response will appear here...'}</p>
      </div>
    </div>
  )
}
